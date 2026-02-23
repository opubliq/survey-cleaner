"""Stratégie de parsing pour fichiers Markdown (.md, .txt).

Les fichiers .md dans ce projet sont des codebooks générés automatiquement
à partir d'autres sources (généralement via Python scripts).

Format typique (voir eeq_2022/codebook.md):

# Codebook: [Survey Name]

Source: [source file description]

Total variables documented: N

---

### variable_name

**Question**: Full question text

**Type**: categorical | ordinal | numeric

**Choix de réponse**:
- 1 = Label for value 1
- 2 = Label for value 2

**Notes**: Skip logic, missing values, etc.

---

### next_variable_name
...
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from ..schemas.variable_schema import ValueLabel, VariableSchema

# ---------------------------------------------------------------------------
# Regex pour le format markdown structuré
# ---------------------------------------------------------------------------

# Header de variable: "### variable_name"
_MD_VAR_HEADER = re.compile(r"^###\s+([A-Za-z_$][A-Za-z0-9_$@#.\s]*)\s*$")

# Ligne **Question**: ou **Type**: ou **Notes**:
_MD_FIELD = re.compile(r"^\*\*([^*]+)\*\*:\s*(.+)$")

# Ligne de choix de réponse: "- 1 = Label" ou "- 1.0 = Label"
_MD_CHOICE = re.compile(r"^\s*-\s*(-?\d+(?:\.\d+)?)\s*=\s*(.+)$")

# Codes manquants
_MISSING_CODES = {98.0, 99.0, 999.0, 9999.0, -1.0, -9.0}
_MISSING_LABEL_RE = re.compile(
    r"(ne sait pas|nsp|nrp|sans.?réponse|refus|non.?réponse|"
    r"don.?t know|dk|no response|refuse|refused|missing)",
    re.IGNORECASE,
)


def parse_md(
    path: Path, verbose: bool = False
) -> tuple[list[VariableSchema], str]:
    """Parse un fichier markdown codebook. Retourne (variables, notes)."""
    text = path.read_text(encoding="utf-8")
    notes_parts: list[str] = []

    def log(msg: str) -> None:
        if verbose:
            print(f"  [md] {msg}")
        notes_parts.append(msg)

    if not text.strip():
        log("WARNING: Fichier vide")
        return [], "\n".join(notes_parts)

    variables = _parse_markdown_text(text, log)

    log(f"Total: {len(variables)} variables parsées")
    return variables, "\n".join(notes_parts)


# ---------------------------------------------------------------------------
# Parsing principal
# ---------------------------------------------------------------------------

def _parse_markdown_text(text: str, log) -> list[VariableSchema]:
    """Parse le texte markdown extrait."""
    variables: list[VariableSchema] = []
    lines = text.split("\n")

    current_name: Optional[str] = None
    current_question: Optional[str] = None
    current_type: str = "unknown"
    current_notes: Optional[str] = None
    current_value_labels: list[ValueLabel] = []

    def _flush():
        if current_name:
            variables.append(VariableSchema(
                var_name=current_name,
                var_label=current_question or current_name,
                question_text=current_question or None,
                var_type=current_type,
                value_labels=current_value_labels,
                notes=current_notes or None,
            ))

    for line in lines:
        # Header de variable: "### variable_name"
        m = _MD_VAR_HEADER.match(line)
        if m:
            _flush()
            current_name = m.group(1).strip()
            current_question = None
            current_type = "unknown"
            current_notes = None
            current_value_labels = []
            continue

        if current_name is None:
            # Avant la première variable: chercher le bloc de métadonnées
            if "Source:" in line or "Total variables" in line:
                pass  # Metadata, on ignore
            continue

        # Ligne **Field**: valeur
        m = _MD_FIELD.match(line)
        if m:
            field = m.group(1).strip().lower()
            value = m.group(2).strip()

            if field == "question":
                current_question = value
            elif field == "type":
                if value in ("categorical", "ordinal", "numeric", "text"):
                    current_type = value
                else:
                    current_type = "unknown"
            elif field == "notes":
                current_notes = value
            continue

        # Ligne de choix de réponse: "- 1 = Label"
        m = _MD_CHOICE.match(line)
        if m:
            val = float(m.group(1))
            label = m.group(2).strip()
            is_missing = _is_missing(val, label)
            current_value_labels.append(ValueLabel(
                value=val, label=label, is_missing=is_missing
            ))

        # Ligne de séparation "---"
        if line.strip() == "---":
            continue

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
