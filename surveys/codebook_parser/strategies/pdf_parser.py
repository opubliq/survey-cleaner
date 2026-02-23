"""Stratégie de parsing pour fichiers PDF.

Deux modes selon le contenu:

  Mode 1 — SPSS-export "livre de codes" (dominant dans ce projet)
    Structure ASCII: blocs délimités par ===...=== et ---...---
    Ex: cecd_charte_2013_09/Livre de codes - Charte_CROP_2013-09.pdf
    → Parsing par regex, sans LLM

  Mode 2 — Autres formats (questionnaire, prose, codebook académique)
    → Extraction texte brut, envoi au LLM par chunks
    → Prompt dans templates/llm_extract.txt

Détection automatique: si ≥ 30% des blocs suivent la structure SPSS, Mode 1.
Sinon, Mode 2.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from ..schemas.variable_schema import ValueLabel, VariableSchema

# ---------------------------------------------------------------------------
# Regex pour le format SPSS-export PDF
# ---------------------------------------------------------------------------

# Délimiteur de début de variable: ligne de ===
_SPSS_SEP = re.compile(r"^={10,}\s*$", re.MULTILINE)

# Ligne "varname 'variable label'" (avec guillemets simples/doubles ou typographiques)
_SPSS_VAR_LINE = re.compile(
    r"^([A-Za-z_$@#][A-Za-z0-9_$@#.]*)\s+[''\u2019\u201c\u201d\"](.+)[''\u2019\u201c\u201d\"]\s*$"
)

# Ligne de valeur: "  1 'Label'"  ou  "  1.0 'Label'" (tous types de guillemets)
# Note: \s* car certains formats n'ont pas d'indentation
_SPSS_VALUE_LINE = re.compile(
    r"^\s*(-?\d+(?:\.\d+)?)\s+[''\u2019\u201c\u201d\"](.+)[''\u2019\u201c\u201d\"]\s*$"
)

# Measurement level
_SPSS_MEASURE = re.compile(
    r"Measurement:\s*(nominal|ordinal|scale|undefined|continuous)", re.IGNORECASE
)

# Storage mode (pour détecter les variables texte)
_SPSS_STORAGE = re.compile(
    r"Storage mode:\s*(character|double|single|long string)", re.IGNORECASE
)

# Stats continues (pas de value labels): Mean, Std.Dev., Min, Max
_SPSS_CONTINUOUS = re.compile(r"^\s*(Mean|Min|Max|Std\.Dev\.|Skewness):", re.MULTILINE)

# Codes manquants courants
_MISSING_CODES = {98.0, 99.0, 999.0, 9999.0, -1.0, -9.0, -99.0, -999.0,
                  98, 99, 999, 9999, -1, -9, -99, -999}
_MISSING_LABEL_RE = re.compile(
    r"(ne sait pas|nsp|nrp|sans.?réponse|refus|non.?réponse|"
    r"don.?t know|dk|no response|refuse|refused|missing|"
    r"not applicable|n/a|na$)",
    re.IGNORECASE,
)


def parse_pdf(
    path: Path, llm_model: str, verbose: bool = False
) -> tuple[list[VariableSchema], str]:
    """Parse un PDF codebook. Retourne (variables, notes)."""
    text = _extract_text(path)
    notes_parts: list[str] = []

    def log(msg: str) -> None:
        if verbose:
            print(f"  [pdf] {msg}")
        notes_parts.append(msg)

    if not text.strip():
        log("WARNING: PDF vide ou non extractible (scan/images?)")
        return [], "\n".join(notes_parts)

    # Détection du mode
    if _is_spss_export(text):
        log("Mode 1: SPSS-export détecté → parsing par regex")
        variables = _parse_spss_export(text, log)
    else:
        log("Mode 2: Format non-SPSS → envoi au LLM")
        variables = _parse_via_llm(text, llm_model, path.name, log)

    log(f"Total: {len(variables)} variables parsées")
    return variables, "\n".join(notes_parts)


# ---------------------------------------------------------------------------
# Mode 1: SPSS-export parsing
# ---------------------------------------------------------------------------

def _extract_text(path: Path) -> str:
    """Extrait le texte brut d'un PDF avec pymupdf (plus fiable pour les layouts)."""
    try:
        import fitz  # pymupdf
        doc = fitz.open(str(path))
        pages = []
        for page in doc:
            pages.append(page.get_text("text"))
        doc.close()
        return "\n".join(pages)
    except Exception:
        # Fallback: pdfminer
        try:
            from pdfminer.high_level import extract_text
            return extract_text(str(path))
        except Exception as e:
            return ""


def _is_spss_export(text: str) -> bool:
    """Détecte si le PDF est un export SPSS basé sur la structure ASCII."""
    # Cherche les délimiteurs === typiques de SPSS
    sep_count = len(_SPSS_SEP.findall(text))
    # Cherche les lignes "varname 'label'"
    var_line_count = len(_SPSS_VAR_LINE.findall(text))
    # Si on trouve plusieurs blocs SPSS, c'est le bon format
    return sep_count >= 3 or var_line_count >= 3


def _parse_spss_export(text: str, log) -> list[VariableSchema]:
    """Parse le format SPSS-export en utilisant les séparateurs === et ---."""
    variables: list[VariableSchema] = []

    # Découpe en blocs par les séparateurs ===
    blocks = _SPSS_SEP.split(text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        var = _parse_spss_block(block)
        if var is not None:
            variables.append(var)

    if not variables:
        # Fallback: essai sans séparateurs (certains PDFs ont un layout différent)
        log("Fallback: tentative de parsing ligne par ligne")
        variables = _parse_spss_linewise(text, log)

    return variables


def _parse_spss_block(block: str) -> Optional[VariableSchema]:
    """Parse un bloc SPSS individuel."""
    lines = block.split("\n")

    var_name: Optional[str] = None
    var_label: Optional[str] = None
    measurement: Optional[str] = None
    storage: Optional[str] = None
    value_labels: list[ValueLabel] = []
    is_continuous = bool(_SPSS_CONTINUOUS.search(block))

    for line in lines:
        # Ligne "varname 'label'"
        m = _SPSS_VAR_LINE.match(line.strip())
        if m and var_name is None:
            var_name = m.group(1)
            var_label = m.group(2)
            continue

        # Measurement level
        m = _SPSS_MEASURE.search(line)
        if m:
            measurement = m.group(1).lower()
            continue

        # Storage mode
        m = _SPSS_STORAGE.search(line)
        if m:
            storage = m.group(1).lower()
            continue

        # Ligne de valeur: "  1.0 'Label'  N  %"
        m = _SPSS_VALUE_LINE.match(line)
        if m:
            val = float(m.group(1))
            label = m.group(2).strip()
            is_missing = _is_missing(val, label)
            value_labels.append(ValueLabel(value=val, label=label, is_missing=is_missing))

    if var_name is None:
        return None

    # Déterminer le type
    var_type = _spss_to_var_type(measurement, storage, is_continuous, value_labels)

    return VariableSchema(
        var_name=var_name,
        var_label=var_label or var_name,
        var_type=var_type,
        value_labels=value_labels,
        codebook_page=None,
    )


def _parse_spss_linewise(text: str, log) -> list[VariableSchema]:
    """Parsing ligne par ligne comme fallback pour les SPSS sans séparateurs clairs."""
    variables: list[VariableSchema] = []
    lines = text.split("\n")
    current: Optional[dict] = None

    def _flush():
        if current and current.get("var_name"):
            vl = current.get("value_labels", [])
            variables.append(VariableSchema(
                var_name=current["var_name"],
                var_label=current.get("var_label", current["var_name"]),
                var_type=_spss_to_var_type(
                    current.get("measurement"),
                    current.get("storage"),
                    current.get("is_continuous", False),
                    vl,
                ),
                value_labels=vl,
            ))

    for line in lines:
        m = _SPSS_VAR_LINE.match(line.strip())
        if m:
            _flush()
            current = {
                "var_name": m.group(1),
                "var_label": m.group(2),
                "value_labels": [],
                "is_continuous": False,
            }
            continue

        if current is None:
            continue

        m = _SPSS_MEASURE.search(line)
        if m:
            current["measurement"] = m.group(1).lower()
            continue

        m = _SPSS_STORAGE.search(line)
        if m:
            current["storage"] = m.group(1).lower()
            continue

        if _SPSS_CONTINUOUS.search(line):
            current["is_continuous"] = True
            continue

        m = _SPSS_VALUE_LINE.match(line)
        if m:
            val = float(m.group(1))
            label = m.group(2).strip()
            current["value_labels"].append(
                ValueLabel(value=val, label=label, is_missing=_is_missing(val, label))
            )

    _flush()
    return variables


# ---------------------------------------------------------------------------
# Mode 2: LLM parsing pour les formats non-SPSS
# ---------------------------------------------------------------------------

def _parse_via_llm(
    text: str, llm_model: str, filename: str, log
) -> list[VariableSchema]:
    """Envoie le texte au LLM par chunks et parse les variables retournées."""
    try:
        import litellm
        from pathlib import Path as _Path
    except ImportError:
        log("ERROR: litellm non installé — impossible d'utiliser le mode LLM")
        return []

    # Charge le prompt template
    template_path = _Path(__file__).parents[1] / "templates" / "llm_extract.txt"
    if template_path.exists():
        system_prompt = template_path.read_text(encoding="utf-8")
    else:
        system_prompt = _DEFAULT_LLM_PROMPT

    # Découpe le texte en chunks de ~6000 tokens (~24000 chars)
    MAX_CHUNK = 24_000
    chunks = [text[i:i + MAX_CHUNK] for i in range(0, len(text), MAX_CHUNK)]
    log(f"LLM mode: {len(chunks)} chunks à traiter avec {llm_model}")

    all_variables: list[VariableSchema] = []
    seen_names: set[str] = set()

    for i, chunk in enumerate(chunks):
        log(f"  Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
        try:
            response = litellm.completion(
                model=llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": (
                            f"Source: {filename}\n\n"
                            f"Texte du codebook:\n\n{chunk}"
                        ),
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            raw = response.choices[0].message.content
            parsed = json.loads(raw)
            vars_data = parsed.get("variables", [])

            for v in vars_data:
                var_name = v.get("var_name", "").strip()
                if not var_name or var_name.upper() in seen_names:
                    continue
                seen_names.add(var_name.upper())

                # Construire les ValueLabels
                value_labels = []
                for vl in v.get("value_labels", []):
                    try:
                        value_labels.append(ValueLabel(
                            value=float(vl["value"]),
                            label=str(vl["label"]),
                            is_missing=bool(vl.get("is_missing", False)),
                        ))
                    except (KeyError, ValueError, TypeError):
                        pass

                var_type = v.get("var_type", "unknown")
                if var_type not in ("categorical", "ordinal", "numeric", "text", "unknown"):
                    var_type = "unknown"

                all_variables.append(VariableSchema(
                    var_name=var_name,
                    var_label=v.get("var_label", var_name),
                    var_type=var_type,
                    question_text=v.get("question_text") or None,
                    filter_condition=v.get("filter_condition") or None,
                    value_labels=value_labels,
                    parser_confidence=float(v.get("confidence", 0.8)),
                ))

        except Exception as e:
            log(f"  WARNING: LLM chunk {i + 1} échoué: {e}")
            continue

    return all_variables


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_missing(value: float, label: str) -> bool:
    if value in _MISSING_CODES:
        return True
    if _MISSING_LABEL_RE.search(label):
        return True
    return False


def _spss_to_var_type(
    measurement: Optional[str],
    storage: Optional[str],
    is_continuous: bool,
    value_labels: list[ValueLabel],
) -> str:
    if storage and "character" in storage:
        return "text"
    if is_continuous and not value_labels:
        return "numeric"
    if measurement:
        if "nominal" in measurement:
            return "categorical"
        if "ordinal" in measurement:
            return "ordinal"
        if "scale" in measurement:
            return "numeric"
    if value_labels:
        valid = [vl.value for vl in value_labels if not vl.is_missing]
        if len(valid) <= 2:
            return "categorical"
        if len(valid) <= 10:
            return "ordinal"
    return "unknown"


# Prompt par défaut si le template n'est pas trouvé
_DEFAULT_LLM_PROMPT = """\
Tu es un extracteur de codebooks de sondages. Analyse le texte fourni et extrait toutes les variables.

Retourne un objet JSON avec une clé "variables" contenant une liste d'objets avec:
- var_name: nom de la variable (ex: Q1, AGE, province)
- var_label: label court de la variable
- question_text: texte complet de la question (si disponible)
- var_type: "categorical" | "ordinal" | "numeric" | "text" | "unknown"
- value_labels: liste de {value: nombre, label: string, is_missing: bool}
- filter_condition: condition de filtrage/skip (si mentionné)
- confidence: 0.0-1.0

Règles:
- is_missing=true pour les codes NSP, refus, NR, 98, 99, 999
- Ne répète pas les variables déjà vues
- Si une variable n'a pas de value labels (variable continue), laisse value_labels=[]
"""
