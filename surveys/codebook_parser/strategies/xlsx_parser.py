"""Stratégie de parsing pour fichiers Excel (.xlsx).

Supporte 3 patterns observés dans le projet:

  Pattern A — "liste des codes" (simple 3 colonnes)
    Ex: elxnqc_particip_egp_2018/Participation ÉGP 2018_Liste des codes.xlsx
    Col A: variable_name (uniquement sur la 1re ligne de chaque variable)
    Col B: valeur numérique
    Col C: label
    → Pas de question text, pas de type

  Pattern B — SPSS export 2 feuilles ("Variable Labels" + "Value Labels")
    Ex: provincial_qc_2012/Codebook_Quebec_provincial_2012.xlsx
        govcan_06822_wave*/068-22-wave*-data-dictionary.xlsx
    Feuille 1: Variable | Position | Label | Measurement Level | ...
    Feuille 2: Variable | Value | Label   (variable répété sur chaque ligne)
              OU: variable seulement sur 1re ligne (pattern A)
    → Question text dans Label (souvent "VARNAME. Question text.")
    → Type dans "Measurement Level"

  Pattern C — Data + Index sheet
    Ex: elxnqc_particip_egm_2021/Participation ÉGM 2021_Base de données.xlsx
    Une feuille "Index" avec 2 cols: variable_name | question_label
    → Pas de value labels dans cette feuille
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import openpyxl

from ..schemas.variable_schema import ValueLabel, VariableSchema

# Codes typiques pour les valeurs manquantes dans les sondages québécois/canadiens
_MISSING_CODE_HINTS = {
    98, 99, 999, 9999, 98.0, 99.0, 999.0, 9999.0, -1, -1.0, -9, -9.0,
    -99, -99.0, -999, -999.0,
}
_MISSING_LABEL_PATTERNS = re.compile(
    r"(ne sait pas|nsp|nrp|sans réponse|refus|non réponse|"
    r"don't know|dk|no response|refuse|refused|missing|"
    r"not applicable|n/a|na\b)",
    re.IGNORECASE,
)

# Noms courants de feuilles pour les patterns B et C
_VAR_SHEET_NAMES = {"variable labels", "variable", "variables", "variable information"}
_VAL_SHEET_NAMES = {"value labels", "value", "values", "variable values"}
_INDEX_SHEET_NAMES = {"index", "liste des codes", "feuil1", "sheet1", "codebook"}


def parse_xlsx(
    path: Path, verbose: bool = False
) -> tuple[list[VariableSchema], str]:
    """Parse un fichier Excel et retourne (variables, notes).

    Détecte automatiquement le pattern (A, B ou C) et l'applique.

    Returns:
        (variables, notes) où notes est une chaîne de log/avertissements.
    """
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet_names_lower = {s.lower(): s for s in wb.sheetnames}
    notes_parts: list[str] = []

    def log(msg: str) -> None:
        if verbose:
            print(f"  [xlsx] {msg}")
        notes_parts.append(msg)

    # --- Détection du pattern ---
    var_sheet_name = _find_sheet(sheet_names_lower, _VAR_SHEET_NAMES)
    val_sheet_name = _find_sheet(sheet_names_lower, _VAL_SHEET_NAMES)
    idx_sheet_name = _find_sheet(sheet_names_lower, _INDEX_SHEET_NAMES)

    if var_sheet_name and val_sheet_name:
        log(f"Pattern B détecté: feuilles '{var_sheet_name}' + '{val_sheet_name}'")
        variables = _parse_pattern_b(
            wb, var_sheet_name, val_sheet_name, log
        )
    elif idx_sheet_name and len(wb.sheetnames) >= 2:
        log(f"Pattern C détecté: feuille index '{idx_sheet_name}'")
        variables = _parse_pattern_c(wb, idx_sheet_name, log)
    else:
        # Pattern A: 1 seule feuille, 3 colonnes, variable sur 1re ligne seulement
        first_sheet = wb[wb.sheetnames[0]]
        log(f"Pattern A détecté: feuille unique '{wb.sheetnames[0]}'")
        variables = _parse_pattern_a(first_sheet, log)

    log(f"Total: {len(variables)} variables parsées")
    return variables, "\n".join(notes_parts)


# ---------------------------------------------------------------------------
# Pattern A: liste simple (variable | valeur | label) — variable sur 1re ligne
# ---------------------------------------------------------------------------

def _parse_pattern_a(sheet, log) -> list[VariableSchema]:
    """Parse une feuille avec le pattern 3-colonnes simple."""
    variables: list[VariableSchema] = []
    current_var_name: Optional[str] = None
    current_value_labels: list[ValueLabel] = []

    rows = list(sheet.iter_rows(values_only=True))

    def _flush():
        if current_var_name and current_value_labels:
            variables.append(VariableSchema(
                var_name=current_var_name,
                var_label=current_var_name,  # Pas de label disponible dans ce pattern
                var_type=_infer_type_from_values(current_value_labels),
                value_labels=current_value_labels,
            ))

    for row in rows:
        # Skip lignes complètement vides
        if all(cell is None for cell in row):
            continue

        # Skip ligne de header (contient des mots-clés)
        row_str = " ".join(str(c).lower() for c in row if c is not None)
        if any(h in row_str for h in ("valeur", "value", "etiquette", "label", "variable")):
            if current_var_name is None:  # Seulement si on n'a pas encore commencé
                continue

        col_a = _clean_str(row[0]) if len(row) > 0 else None
        col_b = row[1] if len(row) > 1 else None
        col_c = _clean_str(row[2]) if len(row) > 2 else None

        if col_a:
            # Nouvelle variable
            _flush()
            current_var_name = col_a
            current_value_labels = []

        # Ajouter la valeur si présente
        if col_b is not None and col_c is not None:
            try:
                val = float(col_b) if isinstance(col_b, (int, float)) else float(str(col_b))
                is_missing = _is_missing_code(val, col_c)
                current_value_labels.append(ValueLabel(
                    value=val,
                    label=col_c,
                    is_missing=is_missing,
                ))
            except (ValueError, TypeError):
                pass  # Valeur non numérique, on ignore

    _flush()
    return variables


# ---------------------------------------------------------------------------
# Pattern B: SPSS 2 feuilles
# ---------------------------------------------------------------------------

def _parse_pattern_b(
    wb, var_sheet_name: str, val_sheet_name: str, log
) -> list[VariableSchema]:
    """Parse le format SPSS 2-feuilles."""

    # --- Feuille variables ---
    var_sheet = wb[var_sheet_name]
    var_rows = list(var_sheet.iter_rows(values_only=True))

    # Trouver les indices de colonnes utiles
    header_row = _find_header_row(var_rows, {"variable", "label", "measurement"})
    if header_row is None:
        log("WARNING: Pas de ligne d'en-tête trouvée dans la feuille variables")
        header_row = 0

    col_idx = _map_columns(var_rows[header_row])
    var_col = col_idx.get("variable", 0)
    label_col = col_idx.get("label", 2)
    measure_col = col_idx.get("measurement level", col_idx.get("measurement", 3))

    # Construire le dict variable_name → (label, measurement_level)
    var_info: dict[str, tuple[str, str]] = {}
    for row in var_rows[header_row + 1:]:
        if all(c is None for c in row):
            continue
        name = _clean_str(row[var_col]) if len(row) > var_col else None
        if not name:
            continue
        label = _clean_str(row[label_col]) if len(row) > label_col else None
        measure = _clean_str(row[measure_col]) if measure_col and len(row) > measure_col else None

        # Nettoyer le label: souvent "VARNAME. Question text." → extraire juste question text
        if label and label.upper().startswith(name.upper() + "."):
            label = label[len(name) + 1:].strip()
        elif label and label.upper().startswith(name.upper() + " "):
            label = label[len(name):].strip()

        var_info[name.upper()] = (label or name, measure or "")

    # --- Feuille valeurs ---
    val_sheet = wb[val_sheet_name]
    val_rows = list(val_sheet.iter_rows(values_only=True))

    val_header = _find_header_row(val_rows, {"variable", "value", "label"})
    if val_header is None:
        val_header = 0

    val_col_idx = _map_columns(val_rows[val_header])
    vname_col = val_col_idx.get("variable", 0)
    vval_col = val_col_idx.get("value", 1)
    vlabel_col = val_col_idx.get("label", 2)

    # Construire dict variable_name → list[ValueLabel]
    # Support des 2 cas: variable répété sur chaque ligne OU seulement sur 1re ligne
    value_labels_map: dict[str, list[ValueLabel]] = {}
    current_vname: Optional[str] = None

    for row in val_rows[val_header + 1:]:
        if all(c is None for c in row):
            continue
        raw_name = _clean_str(row[vname_col]) if len(row) > vname_col else None
        if raw_name:
            current_vname = raw_name.upper()
        if current_vname is None:
            continue

        raw_val = row[vval_col] if len(row) > vval_col else None
        raw_label = _clean_str(row[vlabel_col]) if len(row) > vlabel_col else None

        if raw_val is None or raw_label is None:
            continue
        try:
            val = float(raw_val) if isinstance(raw_val, (int, float)) else float(str(raw_val))
            is_missing = _is_missing_code(val, raw_label)
            value_labels_map.setdefault(current_vname, []).append(
                ValueLabel(value=val, label=raw_label, is_missing=is_missing)
            )
        except (ValueError, TypeError):
            pass

    # --- Assembler les VariableSchema ---
    variables: list[VariableSchema] = []
    for var_name_upper, (label, measure) in var_info.items():
        vl = value_labels_map.get(var_name_upper, [])
        var_type = _spss_measure_to_var_type(measure) if measure else _infer_type_from_values(vl)
        variables.append(VariableSchema(
            var_name=var_name_upper,
            var_label=label,
            var_type=var_type,
            value_labels=vl,
        ))

    return variables


# ---------------------------------------------------------------------------
# Pattern C: Data + Index sheet (variable_name | question_label uniquement)
# ---------------------------------------------------------------------------

def _parse_pattern_c(wb, idx_sheet_name: str, log) -> list[VariableSchema]:
    """Parse une feuille Index avec 2 colonnes: var_name | question_label."""
    idx_sheet = wb[idx_sheet_name]
    rows = list(idx_sheet.iter_rows(values_only=True))

    variables: list[VariableSchema] = []
    for row in rows:
        if all(c is None for c in row):
            continue
        name = _clean_str(row[0]) if len(row) > 0 else None
        label = _clean_str(row[1]) if len(row) > 1 else None
        if not name:
            continue
        # Skip ligne de header
        if name.lower() in ("variable", "nom", "name", "colonne"):
            continue

        # Nettoyer le label: "VARNAME. Question text." → "Question text."
        if label and label.upper().startswith(name.upper() + "."):
            label = label[len(name) + 1:].strip()

        variables.append(VariableSchema(
            var_name=name,
            var_label=label or name,
            var_type="unknown",
            notes="Pattern C: pas de value labels dans cette feuille",
        ))

    log(f"Pattern C: {len(variables)} variables avec question text seulement (pas de value labels)")
    return variables


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_sheet(
    sheet_names_lower: dict[str, str], candidates: set[str]
) -> Optional[str]:
    """Retourne le nom réel de la feuille si elle correspond à un candidat."""
    for candidate in candidates:
        if candidate in sheet_names_lower:
            return sheet_names_lower[candidate]
    return None


def _find_header_row(rows: list, keywords: set[str]) -> Optional[int]:
    """Trouve la ligne d'en-tête contenant les mots-clés."""
    for i, row in enumerate(rows[:5]):  # Cherche dans les 5 premières lignes
        row_lower = {str(c).lower().strip() for c in row if c is not None}
        if row_lower & keywords:
            return i
    return None


def _map_columns(header_row) -> dict[str, int]:
    """Crée un mapping {nom_colonne_lower: index} à partir d'une ligne d'en-tête."""
    mapping: dict[str, int] = {}
    for i, cell in enumerate(header_row):
        if cell is not None:
            mapping[str(cell).lower().strip()] = i
    return mapping


def _clean_str(val) -> Optional[str]:
    """Nettoie une valeur de cellule en chaîne (None si vide)."""
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def _is_missing_code(value: float, label: str) -> bool:
    """Détermine si une valeur est un code manquant."""
    if value in _MISSING_CODE_HINTS:
        return True
    if label and _MISSING_LABEL_PATTERNS.search(label):
        return True
    return False


def _spss_measure_to_var_type(measure: str) -> str:
    """Convertit un niveau de mesure SPSS en var_type."""
    m = measure.lower()
    if "nominal" in m:
        return "categorical"
    if "ordinal" in m:
        return "ordinal"
    if "scale" in m or "continuous" in m or "ratio" in m or "interval" in m:
        return "numeric"
    return "unknown"


def _infer_type_from_values(value_labels: list[ValueLabel]) -> str:
    """Infère le type de variable à partir de la liste de valeurs."""
    if not value_labels:
        return "unknown"
    valid = [vl.value for vl in value_labels if not vl.is_missing]
    if not valid:
        return "unknown"
    # Si toutes les valeurs sont des entiers consécutifs → ordinal probable
    int_vals = sorted(set(int(v) for v in valid if v == int(v)))
    if len(int_vals) == len(valid) and len(int_vals) <= 15:
        return "ordinal" if len(int_vals) > 2 else "categorical"
    return "numeric"
