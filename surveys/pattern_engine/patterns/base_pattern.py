"""Base class for all survey cleaning patterns.

All patterns inherit from BasePattern. Each pattern encapsulates:
- Detection logic (matches method returning confidence 0-1)
- Code generation (generate_code method)
- JSON serialization (to_pattern method → Pattern Pydantic model)

Architecture decision (council 2026-02-18): Hybrid OOP + Pydantic.
Detection logic lives IN the pattern class (not in a central matcher).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.schemas.pattern_schema import (
    DetectionCriteria,
    Pattern,
    PatternMetadata,
)

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class MissingCodeInfo:
    """Info about missing/sentinel codes detected in a series."""

    codes: set[int | float] = field(default_factory=set)
    meanings: dict[int | float, str] = field(default_factory=dict)
    # True when >5% of non-null values are missing codes (potential false positives)
    high_missing_rate: bool = False

    @property
    def has_missing(self) -> bool:
        return bool(self.codes)


@dataclass
class ClassificationResult:
    """Output of PatternClassifier.classify()."""

    tier: int  # 1, 2, or 3
    pattern_id: Optional[str]  # None if tier 2/3
    confidence: float  # 0.0-1.0
    reason: str  # human-readable explanation
    missing_codes: MissingCodeInfo = field(default_factory=MissingCodeInfo)
    effective_n_unique: Optional[int] = None  # n_unique after removing missing codes
    all_confidences: dict[str, float] = field(default_factory=dict)  # score par pattern


# ---------------------------------------------------------------------------
# BasePattern
# ---------------------------------------------------------------------------


class BasePattern(ABC):
    """Abstract base for all survey variable patterns.

    Subclasses must implement:
    - pattern_id (class attribute)
    - pattern_name (class attribute)
    - pattern_type (class attribute): 'likert' | 'demographic' | 'binary' | 'scale'
    - matches(): confidence that a variable fits this pattern
    - generate_code(): Python code snippet for transformation
    - _detection_criteria(): DetectionCriteria for JSON serialization
    - _transformation_template(): template string for JSON serialization
    """

    pattern_id: str = ""
    pattern_name: str = ""
    pattern_type: str = ""

    @abstractmethod
    def matches(
        self,
        series: pd.Series,
        var: Optional["VariableSchema"] = None,
        missing_info: Optional[MissingCodeInfo] = None,
    ) -> float:
        """Return confidence [0.0-1.0] that this series matches the pattern.

        Args:
            series: Raw pandas Series from the survey CSV.
            var: Optional VariableSchema from parsed codebook.
            missing_info: Pre-computed missing code info (avoids recomputing).

        Returns:
            Confidence score. >=0.8 qualifies for Tier 1.
        """
        ...

    @abstractmethod
    def generate_code(
        self,
        original_var: str,
        clean_var: str,
        var: Optional["VariableSchema"] = None,
    ) -> str:
        """Return Python code snippet that transforms original_var → clean_var.

        Args:
            original_var: Column name in raw CSV (e.g. 'Q2_province').
            clean_var: Target standardized name (e.g. 'ses_province').
            var: Optional VariableSchema for label-aware mappings.

        Returns:
            Python code string (one or more lines, no leading indentation).
        """
        ...

    @abstractmethod
    def _detection_criteria(self) -> DetectionCriteria:
        """Return DetectionCriteria for JSON serialization."""
        ...

    @abstractmethod
    def _transformation_template(self) -> str:
        """Return transformation template string for JSON serialization."""
        ...

    def to_pattern(self) -> Pattern:
        """Serialize this pattern to a Pydantic Pattern (→ pattern_library.json)."""
        return Pattern(
            pattern_id=self.pattern_id,
            pattern_name=self.pattern_name,
            pattern_type=self.pattern_type,
            detection_criteria=self._detection_criteria(),
            transformation_template=self._transformation_template(),
            metadata=PatternMetadata(
                notes=f"Auto-generated from {self.__class__.__name__}"
            ),
        )

    # ------------------------------------------------------------------
    # Shared helpers (used by multiple patterns)
    # ------------------------------------------------------------------

    @staticmethod
    def _effective_values(
        series: pd.Series,
        missing_codes: Optional[set[int | float]] = None,
    ) -> pd.Series:
        """Return series with NaN and missing codes removed."""
        s: pd.Series = series.dropna()  # type: ignore[assignment]
        if missing_codes:
            s = s[~s.isin(missing_codes)]  # type: ignore[assignment]
        return s

    @staticmethod
    def _value_set(
        series: pd.Series,
        missing_codes: Optional[set[int | float]] = None,
    ) -> set:
        """Return set of unique effective values."""
        return set(BasePattern._effective_values(series, missing_codes).unique())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.pattern_id!r})"
