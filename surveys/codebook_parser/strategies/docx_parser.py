"""Stratégie de parsing pour fichiers Word (.docx et .doc legacy).

Deux sous-types observés dans ce projet:

  Type 1 — govcan POR003: table 3 colonnes (Variable | Position | Label)
    Ex: govcan_por003_q1_2023/POR003-22-variable-information-Q1-2023.docx
    → Un seul tableau, parsing direct python-docx
    → Pas de value labels (seulement var_name + question text)

  Type 2 — EEQ CATI scripts: prose avec structure "VARNAME:\nQuestion\n  Option 01\n..."
    Ex: eeq_2007/Quebec Election Study 2007 FR.doc (legacy binaire)
        eeq_2018/Quebec Election Study 2018 FR with programmed answer values.docx
    → Parsing par regex sur le texte extrait
    → Value labels présents inline

Detection:
  - Si le document contient un grand tableau avec headers "Variable" + "Label" → Type 1
  - Sinon → Type 2 (regex sur texte brut)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from ..schemas.variable_schema import ValueLabel, VariableSchema

# ---------------------------------------------------------------------------
# Regex pour le format CATI EEQ (Type 2)
# ---------------------------------------------------------------------------

# Ligne "VARNAME:" ou "Q12:" (début de bloc variable)
_CATI_VAR_START = re.compile(
    r"^([A-Za-z_$][A-Za-z0-9_$@#.]*)\s*:\s*$"
)

# Ligne "VARNAME. Question text" (variante sans les deux-points séparés)
_CATI_VAR_INLINE = re.compile(
    r"^([A-Za-z_$][A-Za-z0-9_$@#.]*)\.\s+(.+)$"
)

# Option de réponse: "  Label text    01" ou "  Label   => Q15"
_CATI_OPTION = re.compile(
    r"^\s{2,}(.+?)\s{2,}(\d{2,3})\s*(?:=>.*)?$"
)

# Codes manquants
_MISSING_CODES = {98.0, 99.0, 999.0, -1.0, -9.0}
_MISSING_LABEL_RE = re.compile(
    r"(ne sait pas|nsp|nrp|sans.?réponse|refus|non.?réponse|"
    r"don.?t know|dk|no response|refuse|refused|missing)",
    re.IGNORECASE,
)


def parse_docx(
    path: Path, llm_model: str, verbose: bool = False
) -> tuple[list[VariableSchema], str]:
    """Parse un fichier Word (.docx ou .doc). Retourne (variables, notes)."""
    notes_parts: list[str] = []

    def log(msg: str) -> None:
        if verbose:
            print(f"  [docx] {msg}")
        notes_parts.append(msg)

    # Extraction du texte et des tables
    text, tables = _extract_docx(path, log)

    if not text.strip() and not tables:
        log("WARNING: Document vide ou non lisible")
        return [], "\n".join(notes_parts)

    # Détection du type
    if _is_govcan_table(tables):
        log(f"Type 1 détecté: table govcan ({len(tables[0])} lignes)")
        variables = _parse_govcan_table(tables[0], log)
    else:
        log("Type 2 détecté: script CATI ou prose → parsing regex")
        variables = _parse_cati_text(text, log)

    log(f"Total: {len(variables)} variables parsées")
    return variables, "\n".join(notes_parts)


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _extract_docx(path: Path, log) -> tuple[str, list[list[list[str]]]]:
    """Extrait texte et tables d'un .docx/.doc.

    Returns:
        (text, tables) où tables est une liste de tableaux,
        chaque tableau étant une liste de lignes, chaque ligne une liste de cellules.
    """
    ext = path.suffix.lower()
    try:
        import docx
        doc = docx.Document(str(path))

        # Texte des paragraphes
        paragraphs = [p.text for p in doc.paragraphs]
        text = "\n".join(paragraphs)

        # Tables
        tables = []
        for table in doc.tables:
            rows = []
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                rows.append(cells)
            tables.append(rows)

        return text, tables

    except Exception as e:
        if ext == ".doc":
            log(f"WARNING: .doc legacy non supporté par python-docx: {e}")
            log("Tentative avec extraction texte brut (strings)")
            text = _extract_doc_legacy(path)
            return text, []
        log(f"ERROR lors de l'extraction: {e}")
        return "", []


def _extract_doc_legacy(path: Path) -> str:
    """Extrait le texte d'un .doc legacy via antiword ou strings."""
    import subprocess

    # Essayer antiword
    try:
        result = subprocess.run(
            ["antiword", str(path)], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: strings (extrait le texte brut, avec noise)
    try:
        result = subprocess.run(
            ["strings", str(path)], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return ""


# ---------------------------------------------------------------------------
# Type 1: Table govcan POR003
# ---------------------------------------------------------------------------

def _is_govcan_table(tables: list[list[list[str]]]) -> bool:
    """Détecte si le doc contient une table govcan (Variable | Position | Label)."""
    if not tables:
        return False
    first = tables[0]
    if len(first) < 3:
        return False
    # Cherche les headers dans les 5 premières lignes
    for row in first[:5]:
        row_lower = [c.lower() for c in row]
        # Cherche "variable" comme mot isolé, pas dans "variable information"
        has_variable = any(c == "variable" or c.strip() == "variable" for c in row_lower)
        has_label = any(c == "label" or c.strip() == "label" for c in row_lower)
        has_position = any("position" in c for c in row_lower)
        if has_variable and (has_label or has_position):
            return True
    return False


def _parse_govcan_table(
    table: list[list[str]], log
) -> list[VariableSchema]:
    """Parse la table govcan 3-colonnes (Variable | Position | Label)."""
    variables: list[VariableSchema] = []

    # Trouver les indices de colonnes et la ligne d'en-tête
    header_row = None
    for i, row in enumerate(table[:5]):
        row_lower = [c.lower() for c in row]
        # Cherche "variable" comme mot exact
        if any(c == "variable" or c.strip() == "variable" for c in row_lower):
            header_row = i
            break

    if header_row is None:
        header_row = 0

    col_map = {}
    for j, cell in enumerate(table[header_row]):
        cell_l = cell.lower()
        if cell_l == "variable" or cell_l.strip() == "variable":
            col_map["variable"] = j
        elif "label" in cell_l:
            col_map["label"] = j
        elif "position" in cell_l:
            col_map["position"] = j

    var_col = col_map.get("variable", 0)
    label_col = col_map.get("label", 2)

    for row in table[header_row + 1:]:
        if not row or all(c == "" for c in row):
            continue
        var_name = row[var_col].strip() if len(row) > var_col else ""
        label = row[label_col].strip() if len(row) > label_col else ""
        if not var_name:
            continue

        # Nettoyer le label: "VARNAME. Question text." → "Question text."
        if label.upper().startswith(var_name.upper() + "."):
            question_text = label[len(var_name) + 1:].strip()
        elif label.upper().startswith(var_name.upper() + " "):
            question_text = label[len(var_name):].strip()
        else:
            question_text = label

        variables.append(VariableSchema(
            var_name=var_name,
            var_label=question_text or var_name,
            question_text=question_text or None,
            var_type="unknown",
            notes="govcan POR003: pas de value labels dans ce document",
        ))

    return variables


# ---------------------------------------------------------------------------
# Type 2: Script CATI (EEQ)
# ---------------------------------------------------------------------------

def _parse_cati_text(text: str, log) -> list[VariableSchema]:
    """Parse un script CATI style EEQ en regex."""
    variables: list[VariableSchema] = []
    lines = text.split("\n")

    current_name: Optional[str] = None
    current_label: Optional[str] = None
    current_question: list[str] = []
    current_values: list[ValueLabel] = []

    def _flush():
        if current_name:
            question_text = " ".join(current_question).strip() or None
            variables.append(VariableSchema(
                var_name=current_name,
                var_label=current_label or current_name,
                question_text=question_text,
                var_type=_infer_type(current_values),
                value_labels=current_values,
            ))

    for line in lines:
        # Nouvelle variable (VARNAME:)
        m = _CATI_VAR_START.match(line)
        if m:
            _flush()
            current_name = m.group(1)
            current_label = None
            current_question = []
            current_values = []
            continue

        if current_name is None:
            # Avant la première variable: cherche "VARNAME. Question"
            m = _CATI_VAR_INLINE.match(line)
            if m:
                _flush()
                current_name = m.group(1)
                current_label = m.group(2).strip()
                current_question = [current_label]
                current_values = []
            continue

        # Option de réponse
        m = _CATI_OPTION.match(line)
        if m:
            label_text = m.group(1).strip()
            code = float(m.group(2))
            is_missing = _is_missing(code, label_text)
            current_values.append(ValueLabel(
                value=code, label=label_text, is_missing=is_missing
            ))
            continue

        # Question text (ligne non vide, non-option)
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            if current_label is None:
                current_label = stripped
            current_question.append(stripped)

    _flush()
    return variables


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_missing(value: float, label: str) -> bool:
    if value in _MISSING_CODES:
        return True
    if _MISSING_LABEL_RE.search(label):
        return True
    return False


def _infer_type(value_labels: list[ValueLabel]) -> str:
    if not value_labels:
        return "unknown"
    valid = [vl for vl in value_labels if not vl.is_missing]
    if len(valid) <= 2:
        return "categorical"
    if len(valid) <= 10:
        return "ordinal"
    return "categorical"
