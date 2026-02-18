"""Likert scale patterns for Quebec/Canadian survey data.

Covers:
- Likert3AgreePattern    : 3-point agree/disagree (1=D'accord, 2=Neutre, 3=En désaccord)
- Likert4AgreePattern    : 4-point (no neutral)
- Likert5AgreePattern    : 5-point standard QC (1=Tout à fait d'accord … 5=Tout à fait en désaccord)
- Likert7AgreePattern    : 7-point (1=Fortement d'accord … 7=Fortement en désaccord)
- LikertFrequencyPattern : Frequency scale (1=Jamais … 5=Toujours)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import BasePattern, MissingCodeInfo
from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


class _BaseLikertPattern(BasePattern):
    """Shared logic for all Likert scale patterns."""

    pattern_type = "likert"
    _expected_values: set[int]  # subclasses define this
    _scale_min: int
    _scale_max: int

    # Keywords in var_name or var_label that hint at Likert
    _LIKERT_KEYWORDS = (
        "accord", "agree", "satisf", "appui", "support",
        "confian", "trust", "appréci", "appreci", "opinion",
        "perception", "attitude", "favorable", "important",
    )

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

        if numeric.empty:
            return 0.0

        observed = set(numeric.astype(int).unique())
        expected = self._expected_values

        # Perfect match: observed values are a subset of expected and
        # cover at least 50% of expected values
        coverage = len(observed & expected) / len(expected)
        if coverage < 0.5:
            return 0.0

        # Reject if any value outside expected range
        if any(v < self._scale_min or v > self._scale_max for v in observed):
            return 0.0

        confidence = coverage  # 0.5-1.0 based on value coverage

        # Boost if codebook provides scale_type confirmation
        if var is not None:
            if var.scale_type == "likert":
                confidence = min(1.0, confidence + 0.15)
            # Boost on keyword match in label
            label_lower = (var.var_label + " " + (var.var_name or "")).lower()
            if any(kw in label_lower for kw in self._LIKERT_KEYWORDS):
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        # Use codebook labels if available, else default labels
        mapping = self._build_mapping(var)
        mapping_repr = repr(mapping)
        lines = [
            f"# Likert scale: {self.pattern_name}",
            f"_mapping_{clean_var} = {mapping_repr}",
            f"df['{clean_var}'] = df['{original_var}'].map(_mapping_{clean_var})",
            f"df['{clean_var}'] = df['{clean_var}'].astype('category')",
        ]
        return "\n".join(lines)

    def _build_mapping(self, var: Optional["VariableSchema"]) -> dict:
        """Build value→label mapping, preferring codebook labels."""
        if var and var.value_labels:
            return {
                vl.value: vl.label
                for vl in var.value_labels
                if not vl.is_missing
            }
        return self._default_mapping()

    def _default_mapping(self) -> dict:
        """Subclasses override with domain-appropriate default labels."""
        raise NotImplementedError

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            unique_values=sorted(self._expected_values),
            range_min=self._scale_min,
            range_max=self._scale_max,
            n_unique=len(self._expected_values),
            name_keywords=list(self._LIKERT_KEYWORDS[:5]),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        )


# ---------------------------------------------------------------------------
# Concrete Likert patterns
# ---------------------------------------------------------------------------


class Likert3AgreePattern(_BaseLikertPattern):
    pattern_id = "likert_3_agree"
    pattern_name = "Likert 3 points - Accord/Neutre/Désaccord"
    _expected_values = {1, 2, 3}
    _scale_min = 1
    _scale_max = 3

    def _default_mapping(self) -> dict:
        return {
            1: "D'accord",
            2: "Ni d'accord ni en désaccord",
            3: "En désaccord",
        }


class Likert4AgreePattern(_BaseLikertPattern):
    pattern_id = "likert_4_agree"
    pattern_name = "Likert 4 points - Accord/Désaccord (sans neutre)"
    _expected_values = {1, 2, 3, 4}
    _scale_min = 1
    _scale_max = 4

    def _default_mapping(self) -> dict:
        return {
            1: "Tout à fait d'accord",
            2: "Plutôt d'accord",
            3: "Plutôt en désaccord",
            4: "Tout à fait en désaccord",
        }


class Likert5AgreePattern(_BaseLikertPattern):
    pattern_id = "likert_5_agree"
    pattern_name = "Likert 5 points - Accord/Désaccord standard QC"
    _expected_values = {1, 2, 3, 4, 5}
    _scale_min = 1
    _scale_max = 5

    def _default_mapping(self) -> dict:
        return {
            1: "Tout à fait d'accord",
            2: "Plutôt d'accord",
            3: "Ni d'accord ni en désaccord",
            4: "Plutôt en désaccord",
            5: "Tout à fait en désaccord",
        }


class Likert7AgreePattern(_BaseLikertPattern):
    pattern_id = "likert_7_agree"
    pattern_name = "Likert 7 points - Accord/Désaccord"
    _expected_values = {1, 2, 3, 4, 5, 6, 7}
    _scale_min = 1
    _scale_max = 7

    def _default_mapping(self) -> dict:
        return {
            1: "Fortement d'accord",
            2: "D'accord",
            3: "Plutôt d'accord",
            4: "Neutre",
            5: "Plutôt en désaccord",
            6: "En désaccord",
            7: "Fortement en désaccord",
        }


class LikertFrequencyPattern(_BaseLikertPattern):
    pattern_id = "likert_frequency"
    pattern_name = "Échelle de fréquence (Jamais → Toujours)"
    _expected_values = {1, 2, 3, 4, 5}
    _scale_min = 1
    _scale_max = 5

    _FREQUENCY_KEYWORDS = (
        "fréquence", "frequen", "souvent", "jamais", "toujours",
        "fois", "times", "often", "never", "always",
    )

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        base_confidence = super().matches(series, var, missing_info)
        if base_confidence == 0.0:
            return 0.0

        # Boost only if frequency keywords present, else slight penalty
        # (avoid confusion with Likert5Agree which has same values)
        if var is not None:
            label_lower = (var.var_label + " " + (var.var_name or "")).lower()
            if any(kw in label_lower for kw in self._FREQUENCY_KEYWORDS):
                return min(1.0, base_confidence + 0.2)
            # If it looks like agree/disagree, reduce frequency confidence
            if any(kw in label_lower for kw in self._LIKERT_KEYWORDS):
                return max(0.0, base_confidence - 0.2)

        # Without codebook, can't distinguish from Likert5Agree — low confidence
        return min(base_confidence, 0.6)

    def _default_mapping(self) -> dict:
        return {
            1: "Jamais",
            2: "Rarement",
            3: "Parfois",
            4: "Souvent",
            5: "Toujours",
        }
