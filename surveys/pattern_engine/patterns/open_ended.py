"""Pattern for open-ended/free-text variables.

Free text is copied as-is without transformation. This is Tier 1 since
the operation is deterministic and requires no LLM processing.

Detection:
- dtype is object/str/string
- OR var.scale_type == "open_ended" from codebook
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import (
    BasePattern,
    ClassificationResult,
    MissingCodeInfo,
)
from surveys.pattern_engine.schemas.pattern_schema import (
    DetectionCriteria,
    PatternMetadata,
    Pattern,
)

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


class OpenEndedPattern(BasePattern):
    """Pattern for open-ended/free-text variables - direct copy to clean df."""

    pattern_id = "open_ended_text"
    pattern_name = "Open-ended text (direct copy)"
    pattern_type = "text"

    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        """Check if this is an open-ended text variable.

        Returns 1.0 if:
        - Codebook explicitly says scale_type == "open_ended"
        - OR dtype is text and no value_labels defined

        Returns 0.0 otherwise.
        """
        if var is not None and var.scale_type == "open_ended":
            return 1.0

        dtype_str = str(series.dtype)
        if dtype_str in ("object", "str", "string"):
            _dropped = series.dropna()
            if len(_dropped) == 0:
                return 0.0
            first_val = _dropped.iloc[0]
            if isinstance(first_val, str):
                if var is None or not var.value_labels:
                    return 1.0
                if len(var.value_labels) > 50:
                    return 0.95

        return 0.0

    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        """Generate simple copy code for text variables."""
        return f"df['{clean_var}'] = df['{original_var}'].copy()"

    def _detection_criteria(self) -> DetectionCriteria:
        return DetectionCriteria(
            dtype=["object", "string", "str"],
            n_unique_max=None,
            value_range=None,
            value_set=None,
            notes="Text dtype OR scale_type='open_ended' from codebook",
        )

    def _transformation_template(self) -> str:
        return "df['{clean_var}'] = df['{original_var}'].copy()"
