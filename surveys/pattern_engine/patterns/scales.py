"""Scale variable patterns (thermometer, percentages, 0-10 scores).

Covers:
- Thermometer0to10Pattern  : Thermomètre politique 0-10 (0=Très défavorable, 10=Très favorable)
- PercentageScalePattern   : Échelle de pourcentage (0-100, 0.0-1.0)
- CountScalePattern        : Comptes numériques entiers
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import BasePattern, MissingCodeInfo
from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Thermomètre 0-10
# ---------------------------------------------------------------------------

_THERMOMETER_KEYWORDS = (
    "thermom", "feeling", "sentiment", "favorable", "favorabl",
    "0 à 10", "0-10", "zero a dix", "zero-dix",
    "échelle", "scale",
)


class Thermometer0to10Pattern(BasePattern):
    pattern_id = "thermometer_0_10"
    pattern_name = "Thermomètre politique 0-10"
    pattern_type = "scale"

    _EXPECTED_RANGE = range(0, 11)

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

        observed = set(numeric.unique())
        expected_set = set(self._EXPECTED_RANGE)

        # Check range
        min_val = float(numeric.min())
        max_val = float(numeric.max())
        if min_val < 0 or max_val > 10:
            return 0.0

        # At least 50% of values must be in expected range
        in_range = sum(1 for v in observed if v in expected_set)
        coverage = in_range / max(len(observed), 1)

        if coverage < 0.5:
            return 0.0

        confidence = 0.5 + coverage * 0.3

        # Big boost on keyword match
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _THERMOMETER_KEYWORDS):
                confidence = min(1.0, confidence + 0.35)
            if var.scale_type in ("thermometer", "scale_0_10"):
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        return "\n".join([
            f"# Thermomètre 0-10",
            f"df['{clean_var}'] = df['{original_var}'].astype('float')",
            f"# Values should be in range [0, 10]",
            f"df.loc[(df['{clean_var}'] < 0) | (df['{clean_var}'] > 10), '{clean_var}'] = None",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            range_min=0,
            range_max=10,
            n_unique=11,
            name_keywords=list(_THERMOMETER_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].astype('float')\n"
            "# Values should be in range [0, 10]\n"
            "df.loc[(df['{clean_var}'] < 0) | (df['{clean_var}'] > 10), '{clean_var}'] = None"
        )


# ---------------------------------------------------------------------------
# Percentage scale (0-100 or 0.0-1.0)
# ---------------------------------------------------------------------------

_PERCENTAGE_KEYWORDS = (
    "pourcent", "percent", "pct", "%", "pourcentag",
    "part", "share", "proportion",
)


class PercentageScalePattern(BasePattern):
    pattern_id = "percentage_scale"
    pattern_name = "Échelle de pourcentage"
    pattern_type = "scale"

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

        min_val = float(numeric.min())
        max_val = float(numeric.max())

        # Check 0-100 range
        if 0 <= min_val and max_val <= 100:
            confidence = 0.7
        # Check 0.0-1.0 range
        elif 0 <= min_val and max_val <= 1.0:
            confidence = 0.6
        else:
            return 0.0

        # Keyword match for boost
        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _PERCENTAGE_KEYWORDS):
                confidence = min(1.0, confidence + 0.3)
            if var.scale_type == "percentage":
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        return "\n".join([
            f"# Pourcentage",
            f"df['{clean_var}'] = df['{original_var}'].astype('float')",
            f"# Values should be in range [0, 100]",
            f"df.loc[(df['{clean_var}'] < 0) | (df['{clean_var}'] > 100), '{clean_var}'] = None",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            range_min=0,
            range_max=100,
            name_keywords=list(_PERCENTAGE_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].astype('float')\n"
            "# Values should be in range [0, 100]\n"
            "df.loc[(df['{clean_var}'] < 0) | (df['{clean_var}'] > 100), '{clean_var}'] = None"
        )


# ---------------------------------------------------------------------------
# Count scale (integer counts)
# ---------------------------------------------------------------------------

_COUNT_KEYWORDS = ("compte", "count", "nombre", "number", "freq", "fréquence", "frequence", "n")


class CountScalePattern(BasePattern):
    pattern_id = "count_scale"
    pattern_name = "Échelle de compte (entiers)"
    pattern_type = "scale"

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

        # Must be all integers (or very close to integers)
        is_int = (numeric % 1 == 0).all()
        if not is_int:
            return 0.0

        min_val = int(numeric.min())
        max_val = int(numeric.max())

        # Must be non-negative
        if min_val < 0:
            return 0.0

        # Reasonable max count (avoid treating codes as counts)
        if max_val > 100:
            return 0.0

        confidence = 0.5

        if var is not None:
            label = (var.var_name + " " + var.var_label).lower()
            if any(kw in label for kw in _COUNT_KEYWORDS):
                confidence = min(1.0, confidence + 0.4)
            if var.scale_type == "count":
                confidence = min(1.0, confidence + 0.1)

        return round(confidence, 3)

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        return "\n".join([
            f"# Compte (entiers)",
            f"df['{clean_var}'] = df['{original_var}'].astype('Int64')",
            f"# Negative values set to missing",
            f"df.loc[df['{clean_var}'] < 0, '{clean_var}'] = None",
        ])

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            range_min=0,
            range_max=100,
            name_keywords=list(_COUNT_KEYWORDS),
        )

    def _transformation_template(self) -> str:
        return (
            "df['{clean_var}'] = df['{original_var}'].astype('Int64')\n"
            "# Negative values set to missing\n"
            "df.loc[df['{clean_var}'] < 0, '{clean_var}'] = None"
        )
