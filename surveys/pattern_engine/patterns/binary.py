"""Binary variable patterns (yes/no, true/false, presence/absence).

Covers:
- BinaryYesNoPattern    : Oui/Non (1=Oui/2=Non or variants)
- BinaryTrueFalsePattern : Vrai/Faux (1=True/2=False)
- BinaryPresentPattern   : Présence/Absence
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import BasePattern, MissingCodeInfo
from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Oui/Non patterns
# ---------------------------------------------------------------------------

_YES_NO_KEYWORDS = ("oui_non", "yes_no", "d'accord", "accord", "agree", "agree_disagree")
_YES_LABELS = ("oui", "yes", "1", "vrai", "true")
_NO_LABELS = ("non", "no", "0", "faux", "false", "2")


class BinaryYesNoPattern(BasePattern):
    pattern_id = "binary_yes_no"
    pattern_name = "Binaire Oui/Non"
    pattern_type = "binary"

    # Common encodings
    _ENCODINGS = [
        {1: "Oui", 2: "Non"},
        {0: "Oui", 1: "Non"},
        {1: "Yes", 2: "No"},
        {1: "Oui", 0: "Non"},
    ]

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

        n_unique = effective.nunique()

        if n_unique != 2:
            return 0.0

        observed = set(effective.unique())

        # Check numeric encodings
        for enc in self._ENCODINGS:
            if observed == set(enc.keys()):
                confidence = 0.9
                if var is not None:
                    label = (var.var_name + " " + var.var_label).lower()
                    if any(kw in label for kw in _YES_NO_KEYWORDS):
                        confidence = 1.0
                return confidence

        # Check string values
        if all(isinstance(v, str) for v in observed):
            lower_observed = {v.lower().strip() for v in observed}
            has_yes = any(yl in lo for lo in lower_observed for yl in _YES_LABELS)
            has_no = any(nl in lo for lo in lower_observed for nl in _NO_LABELS)

            if has_yes and has_no:
                return 0.8

        return 0.0

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        else:
            # Infer from observed values (simplified)
            mapping = {1: "Oui", 2: "Non"}
        return "\n".join([
            f"# Binaire Oui/Non",
            f"_mapping_{clean_var} = {repr(mapping)}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=[1, 2],
            range_min=0,
            range_max=2,
            n_unique=2,
            name_keywords=list(_YES_NO_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Vrai/Faux patterns
# ---------------------------------------------------------------------------

_TRUE_FALSE_KEYWORDS = ("vrai", "faux", "true", "false", "boolean", "bool", "correct", "correct")


class BinaryTrueFalsePattern(BasePattern):
    pattern_id = "binary_true_false"
    pattern_name = "Binaire Vrai/Faux"
    pattern_type = "binary"

    _ENCODINGS = [
        {1: "Vrai", 0: "Faux"},
        {1: "True", 0: "False"},
        {1: "Correct", 0: "Incorrect"},
    ]

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

        n_unique = effective.nunique()

        if n_unique != 2:
            return 0.0

        observed = set(effective.unique())

        # Check numeric encodings
        for enc in self._ENCODINGS:
            if observed == set(enc.keys()):
                confidence = 0.8
                if var is not None:
                    label = (var.var_name + " " + var.var_label).lower()
                    if any(kw in label for kw in _TRUE_FALSE_KEYWORDS):
                        confidence = 1.0
                return confidence

        return 0.0

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        else:
            mapping = {1: "Vrai", 0: "Faux"}
        return "\n".join([
            f"# Binaire Vrai/Faux",
            f"_mapping_{clean_var} = {repr(mapping)}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=[0, 1],
            range_min=0,
            range_max=1,
            n_unique=2,
            name_keywords=list(_TRUE_FALSE_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Presence/Absence patterns
# ---------------------------------------------------------------------------

_PRESENCE_KEYWORDS = ("présent", "present", "absent", "absence", "existe", "exist", "disponible", "available")


class BinaryPresentPattern(BasePattern):
    pattern_id = "binary_present"
    pattern_name = "Binaire Présence/Absence"
    pattern_type = "binary"

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

        n_unique = effective.nunique()

        if n_unique != 2:
            return 0.0

        observed = set(effective.unique())

        # Must have keyword match to distinguish from other binary patterns
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if not any(kw in label for kw in _PRESENCE_KEYWORDS):
                return 0.0

            if observed == {0, 1} or observed == {1, 0}:
                return 0.9

        return 0.0

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        if var and var.value_labels:
            mapping = {vl.value: vl.label for vl in var.value_labels if not vl.is_missing}
        else:
            mapping = {1: "Présent", 0: "Absent"}
        return "\n".join([
            f"# Binaire Présence/Absence",
            f"_mapping_{clean_var} = {repr(mapping)}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=[0, 1],
            range_min=0,
            range_max=1,
            n_unique=2,
            name_keywords=list(_PRESENCE_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )
