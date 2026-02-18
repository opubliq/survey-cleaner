"""Demographic variable patterns for Quebec/Canadian survey data.

Covers:
- ProvinceQCPattern   : Province/territoire canadien (codes → labels FR)
- GenderPattern       : Sexe/genre (1=Homme/2=Femme ou variantes)
- AgeGroupsPattern    : Groupes d'âge catégoriels (tranches)
- IncomeGroupsPattern : Tranches de revenu
- AdminRegionQCPattern: Régions administratives du Québec (01-17)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import BasePattern, MissingCodeInfo
from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Province / Territory
# ---------------------------------------------------------------------------

# Standard Statistics Canada province codes
_PROVINCE_CODES: dict[int, str] = {
    10: "Terre-Neuve-et-Labrador",
    11: "Île-du-Prince-Édouard",
    12: "Nouvelle-Écosse",
    13: "Nouveau-Brunswick",
    24: "Québec",
    35: "Ontario",
    46: "Manitoba",
    47: "Saskatchewan",
    48: "Alberta",
    59: "Colombie-Britannique",
    60: "Yukon",
    61: "Territoires du Nord-Ouest",
    62: "Nunavut",
}

# Alternative sequential codes (1-10, 1-13) used in some surveys
_PROVINCE_SEQ_CODES: dict[int, str] = {
    1: "Terre-Neuve-et-Labrador",
    2: "Île-du-Prince-Édouard",
    3: "Nouvelle-Écosse",
    4: "Nouveau-Brunswick",
    5: "Québec",
    6: "Ontario",
    7: "Manitoba",
    8: "Saskatchewan",
    9: "Alberta",
    10: "Colombie-Britannique",
    11: "Yukon",
    12: "Territoires du Nord-Ouest",
    13: "Nunavut",
}

_PROVINCE_KEYWORDS = ("province", "prov", "region", "territoire", "territory")


class ProvinceQCPattern(BasePattern):
    pattern_id = "province_qc"
    pattern_name = "Province/Territoire canadien"
    pattern_type = "demographic"

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        missing_codes = missing_info.codes if missing_info else set()
        effective = self._effective_values(series, missing_codes)

        if effective.empty:
            return 0.0

        try:
            _converted = pd.to_numeric(effective, errors="coerce")
            numeric: pd.Series = pd.Series(_converted).dropna()  # type: ignore[assignment]
        except Exception:
            return 0.0

        observed = set(int(v) for v in numeric.unique())  # type: ignore[union-attr]
        confidence = 0.0

        # Check StatsCan codes (10-62)
        statscan_match = len(observed & set(_PROVINCE_CODES.keys())) / max(len(observed), 1)
        # Check sequential codes (1-13)
        seq_match = len(observed & set(_PROVINCE_SEQ_CODES.keys())) / max(len(observed), 1)

        if statscan_match >= 0.6:
            confidence = 0.85 + statscan_match * 0.1
        elif seq_match >= 0.5 and max(observed, default=0) <= 13:
            confidence = 0.65 + seq_match * 0.15
        else:
            return 0.0

        # Boost on keyword match
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _PROVINCE_KEYWORDS):
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        mapping = self._build_mapping(var)
        mapping_repr = repr(mapping)
        return "\n".join([
            f"# Province/Territoire canadien",
            f"_mapping_{clean_var} = {mapping_repr}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _build_mapping(self, var: Optional["VariableSchema"]) -> dict:
        if var and var.value_labels:
            return {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        return _PROVINCE_CODES

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=sorted(_PROVINCE_CODES.keys()),
            n_unique=13,
            name_keywords=list(_PROVINCE_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Gender / Sexe
# ---------------------------------------------------------------------------

_GENDER_KEYWORDS = ("sexe", "sex", "genre", "gender")

_GENDER_MAPPINGS = [
    {1: "Homme", 2: "Femme"},
    {1: "Homme", 2: "Femme", 3: "Autre"},
    {0: "Femme", 1: "Homme"},
    {1: "Male", 2: "Female"},
]


class GenderPattern(BasePattern):
    pattern_id = "gender"
    pattern_name = "Sexe/Genre"
    pattern_type = "demographic"

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        missing_codes = missing_info.codes if missing_info else set()
        effective = self._effective_values(series, missing_codes)

        if effective.empty:
            return 0.0

        try:
            _converted = pd.to_numeric(effective, errors="coerce")
            numeric: pd.Series = pd.Series(_converted).dropna()  # type: ignore[assignment]
        except Exception:
            return 0.0

        observed = set(int(v) for v in numeric.unique())  # type: ignore[union-attr]

        # Must have 2-3 values in expected range
        if not (2 <= len(observed) <= 3):
            return 0.0
        if max(observed, default=99) > 3 or min(observed, default=-1) < 0:
            return 0.0

        confidence = 0.6  # base: small n_unique + values 0-3

        # Keyword match gives big boost
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _GENDER_KEYWORDS):
                confidence = min(1.0, confidence + 0.35)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        else:
            mapping = {1: "Homme", 2: "Femme"}
        return "\n".join([
            f"# Sexe/Genre",
            f"_mapping_{clean_var} = {repr(mapping)}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=[1, 2],
            range_min=1,
            range_max=3,
            n_unique=2,
            name_keywords=list(_GENDER_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Age groups
# ---------------------------------------------------------------------------

_AGE_KEYWORDS = ("age", "âge", "groupe_age", "grp_age", "age_group")


class AgeGroupsPattern(BasePattern):
    pattern_id = "age_groups"
    pattern_name = "Groupes d'âge catégoriels"
    pattern_type = "demographic"

    # Typical category counts for age groups
    _TYPICAL_N_UNIQUE = range(4, 10)

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        missing_codes = missing_info.codes if missing_info else set()
        effective = self._effective_values(series, missing_codes)

        if effective.empty:
            return 0.0

        try:
            _converted = pd.to_numeric(effective, errors="coerce")
            numeric: pd.Series = pd.Series(_converted).dropna()  # type: ignore[assignment]
        except Exception:
            return 0.0

        n_unique = numeric.nunique()
        if n_unique not in self._TYPICAL_N_UNIQUE:
            return 0.0

        # Values must be sequential integers starting from 1 or 0
        observed = sorted(set(int(v) for v in numeric.unique()))  # type: ignore[union-attr]
        is_sequential = (
            observed == list(range(min(observed), max(observed) + 1))
            and min(observed) in (0, 1)
        )

        confidence = 0.5 if is_sequential else 0.0
        if confidence == 0.0:
            return 0.0

        # Big boost on keyword match
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _AGE_KEYWORDS):
                confidence = min(1.0, confidence + 0.4)
            if var.scale_type == "demographic":
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
            mapping_repr = repr(mapping)
            return "\n".join([
                f"# Groupes d'âge",
                f"_mapping_{clean_var} = {mapping_repr}",
                f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
                f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
            ])
        # No codebook: keep as ordered numeric category
        return "\n".join([
            f"# Groupes d'âge (sans codebook - conserver les codes numériques)",
            f"df['{clean_var}'] = df['{original_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            range_min=1,
            range_max=9,
            n_unique=6,
            name_keywords=list(_AGE_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Région administrative du Québec (01-17)
# ---------------------------------------------------------------------------

_ADMIN_REGION_QC: dict[int, str] = {
    1: "Bas-Saint-Laurent",
    2: "Saguenay–Lac-Saint-Jean",
    3: "Capitale-Nationale",
    4: "Mauricie",
    5: "Estrie",
    6: "Montréal",
    7: "Outaouais",
    8: "Abitibi-Témiscamingue",
    9: "Côte-Nord",
    10: "Nord-du-Québec",
    11: "Gaspésie–Îles-de-la-Madeleine",
    12: "Chaudière-Appalaches",
    13: "Laval",
    14: "Lanaudière",
    15: "Laurentides",
    16: "Montérégie",
    17: "Centre-du-Québec",
}

_REGION_KEYWORDS = ("region", "région", "reg_adm", "regadm")


class AdminRegionQCPattern(BasePattern):
    pattern_id = "admin_region_qc"
    pattern_name = "Région administrative du Québec (01-17)"
    pattern_type = "demographic"

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        missing_codes = missing_info.codes if missing_info else set()
        effective = self._effective_values(series, missing_codes)

        if effective.empty:
            return 0.0

        try:
            _converted = pd.to_numeric(effective, errors="coerce")
            numeric: pd.Series = pd.Series(_converted).dropna()  # type: ignore[assignment]
        except Exception:
            return 0.0

        observed = set(int(v) for v in numeric.unique())  # type: ignore[union-attr]
        valid = set(_ADMIN_REGION_QC.keys())
        coverage = len(observed & valid) / max(len(observed), 1)

        if coverage < 0.5 or max(observed, default=99) > 17:
            return 0.0

        confidence = 0.7 + coverage * 0.2

        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _REGION_KEYWORDS):
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        else:
            mapping = _ADMIN_REGION_QC
        return "\n".join([
            f"# Région administrative QC",
            f"_mapping_{clean_var} = {repr(mapping)}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=sorted(_ADMIN_REGION_QC.keys()),
            range_min=1,
            range_max=17,
            n_unique=17,
            name_keywords=list(_REGION_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )
