"""Pattern classifier for Tier 1/2/3 routing.

Council decision (2026-02-18):
- Defensive by default: works WITHOUT codebook, enhanced by it
- Dual input: series + optional VariableSchema
- Conflict resolution: binary > likert > demographics > scales
- Confidence threshold: >=0.8 for Tier 1

The classifier:
1. Detects missing codes (preprocessing)
2. Computes effective statistics (after removing missing codes)
3. Cross-validates codebook info against data
4. Matches against all patterns
5. Returns tier + best pattern + confidence
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.missing_code_detector import detect_missing_codes
from surveys.pattern_engine.patterns import get_all_patterns
from surveys.pattern_engine.patterns.base_pattern import (
    BasePattern,
    ClassificationResult,
    MissingCodeInfo,
)

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Pattern priority (for conflict resolution)
# ---------------------------------------------------------------------------
# Higher priority patterns are checked first and preferred in ties

_PATTERN_PRIORITY = {
    "binary_yes_no": 100,
    "binary_true_false": 100,
    "binary_present": 95,
    "likert_5_agree": 80,
    "likert_7_agree": 80,
    "likert_4_agree": 75,
    "likert_3_agree": 70,
    "likert_frequency": 70,
    "gender": 60,
    "province_qc": 60,
    "admin_region_qc": 55,
    "age_groups": 50,
    "thermometer_0_10": 40,
    "percentage_scale": 35,
    "count_scale": 30,
}

# ---------------------------------------------------------------------------
# Tiering thresholds
# ---------------------------------------------------------------------------

TIER_1_MIN_CONFIDENCE = 0.8
TIER_1_MAX_N_UNIQUE = 7
TIER_2_MIN_N_UNIQUE = 5
TIER_2_MAX_N_UNIQUE = 20

# ---------------------------------------------------------------------------
# Main classifier
# ---------------------------------------------------------------------------


def classify(
    series: pd.Series,
    var: Optional["VariableSchema"] = None,
) -> ClassificationResult:
    """Classify a variable and determine Tier 1/2/3 recommendation.

    Args:
        series: Raw pandas Series from the survey CSV.
        var: Optional VariableSchema from parsed codebook.

    Returns:
        ClassificationResult with tier (1/2/3), best pattern_id, confidence, and reason.
    """
    # Step 1: Detect missing codes (critical preprocessing)
    missing_info = detect_missing_codes(series, var)

    # Step 2: Compute effective statistics (after removing missing codes)
    effective_series = pd.Series(series[~series.isin(list(missing_info.codes))]).dropna()  # type: ignore[arg-type]
    if effective_series.empty:
        return _empty_series_result(missing_info)

    n_unique = effective_series.nunique()
    try:
        min_val = float(effective_series.min())
        max_val = float(effective_series.max())
    except Exception:
        min_val, max_val = None, None

    # Step 3: Cross-validate codebook info against data (if available)
    if var is not None:
        validation_result = _cross_validate(var, effective_series, min_val, max_val, n_unique)
        if validation_result is not None:
            return validation_result

    # Step 4: Fast path to Tier 3 for clearly complex variables
    if _is_tier_3_candidate(effective_series, n_unique, min_val, max_val):
        return ClassificationResult(
            tier=3,
            pattern_id=None,
            confidence=0.0,
            reason=_tier_3_reason(effective_series, n_unique, min_val, max_val),
            missing_codes=missing_info,
            effective_n_unique=n_unique,
        )

    # Step 5: Match against all patterns
    patterns = get_all_patterns()
    best_pattern = None
    best_confidence = 0.0
    all_confidences = {}

    for pattern in patterns:
        confidence = pattern.matches(effective_series, var, missing_info)
        all_confidences[pattern.pattern_id] = confidence

        if confidence > best_confidence:
            best_confidence = confidence
            best_pattern = pattern

    # Step 6: Resolve conflicts (multiple patterns with similar confidence)
    best_pattern = _resolve_conflicts(best_pattern, all_confidences, patterns)

    # Step 7: Determine tier based on best match confidence
    if best_pattern is not None:
        best_confidence = all_confidences[best_pattern.pattern_id]

        if best_confidence >= TIER_1_MIN_CONFIDENCE and n_unique <= TIER_1_MAX_N_UNIQUE:
            return ClassificationResult(
                tier=1,
                pattern_id=best_pattern.pattern_id,
                confidence=best_confidence,
                reason=f"Pattern {best_pattern.pattern_id} matched with confidence {best_confidence:.2f}",
                missing_codes=missing_info,
                effective_n_unique=n_unique,
            )

    # Step 8: Tier 2: semi-standard or ambiguous
    return ClassificationResult(
        tier=2,
        pattern_id=best_pattern.pattern_id if best_pattern else None,
        confidence=best_confidence,
        reason=_tier_2_reason(best_pattern, best_confidence, n_unique, var),
        missing_codes=missing_info,
        effective_n_unique=n_unique,
    )


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _empty_series_result(missing_info: MissingCodeInfo) -> ClassificationResult:
    """Return result when series is all NaN or missing codes."""
    return ClassificationResult(
        tier=3,
        pattern_id=None,
        confidence=0.0,
        reason="Series contains only missing values or NaN",
        missing_codes=missing_info,
        effective_n_unique=0,
    )


def _cross_validate(
    var: "VariableSchema",
    effective_series: pd.Series,
    min_val: Optional[float],
    max_val: Optional[float],
    n_unique: int,
) -> Optional[ClassificationResult]:
    """Cross-validate codebook info against actual data.

    Returns None if validation passes, or a Tier 3 result if severe mismatch.
    """
    # Check scale_type mismatch
    if var.scale_type:
        data_n_unique = effective_series.nunique()

        if var.scale_type == "likert" and data_n_unique > 10:
            return ClassificationResult(
                tier=3,
                pattern_id=None,
                confidence=0.0,
                reason=f"Codebook says 'likert' but data has {data_n_unique} unique values (too many for Likert)",
                missing_codes=MissingCodeInfo(),
                effective_n_unique=n_unique,
            )

        if var.scale_type == "binary" and data_n_unique != 2:
            return ClassificationResult(
                tier=3,
                pattern_id=None,
                confidence=0.0,
                reason=f"Codebook says 'binary' but data has {data_n_unique} unique values (expected 2)",
                missing_codes=MissingCodeInfo(),
                effective_n_unique=n_unique,
            )

    # Check range mismatch (if codebook specifies range)
    if var.range_min is not None and min_val is not None:
        if min_val < var.range_min:
            return ClassificationResult(
                tier=3,
                pattern_id=None,
                confidence=0.0,
                reason=f"Data min ({min_val}) below codebook range_min ({var.range_min}) - codebook may be incorrect",
                missing_codes=MissingCodeInfo(),
                effective_n_unique=n_unique,
            )

    return None


def _is_tier_3_candidate(
    series: pd.Series,
    n_unique: int,
    min_val: Optional[float],
    max_val: Optional[float],
) -> bool:
    """Quick check for clearly complex/complex variables."""
    # Text data (dtype 'object' or 'str' in pandas 3)
    if str(series.dtype) in ("object", "str", "string"):
        # Check if first non-null value is a string
        _dropped = series.dropna()
        first_non_null = _dropped.iloc[0] if len(_dropped) > 0 else None  # type: ignore[arg-type]
        if first_non_null is not None and isinstance(first_non_null, str):
            return True

    # Too many unique values
    if n_unique > TIER_2_MAX_N_UNIQUE:
        return True

    # Numeric but with huge range (not a scale)
    if min_val is not None and max_val is not None:
        range_span = max_val - min_val
        if range_span > 1000 and n_unique > 50:
            return True

    return False


def _tier_3_reason(
    series: pd.Series,
    n_unique: int,
    min_val: Optional[float],
    max_val: Optional[float],
) -> str:
    """Generate explanation for Tier 3 classification."""
    if str(series.dtype) in ("object", "str", "string"):
        _dropped = series.dropna()
        if len(_dropped) > 0 and isinstance(_dropped.iloc[0], str):  # type: ignore[arg-type]
            return "Text data (open-ended) - requires LLM interpretation"

    if n_unique > TIER_2_MAX_N_UNIQUE:
        return f"Too many unique values ({n_unique}) - not a pattern match"

    if min_val is not None and max_val is not None:
        range_span = max_val - min_val
        if range_span > 1000 and n_unique > 50:
            return f"Wide numeric range ({range_span:.0f}) with many values - not a standard scale"

    return "Complex structure - Tier 3 (individual LLM processing)"


def _tier_2_reason(
    best_pattern: Optional["BasePattern"],
    confidence: float,
    n_unique: int,
    var: Optional["VariableSchema"],
) -> str:
    """Generate explanation for Tier 2 classification."""
    parts = []

    if best_pattern:
        parts.append(f"Semi-standard pattern {best_pattern.pattern_id} with confidence {confidence:.2f} (<{TIER_1_MIN_CONFIDENCE})")
    else:
        parts.append("No clear pattern match")

    if n_unique > TIER_1_MAX_N_UNIQUE:
        parts.append(f"n_unique={n_unique} (> Tier 1 max {TIER_1_MAX_N_UNIQUE})")

    if var and var.parser_confidence < 0.7:
        parts.append("Low codebook parser confidence")

    return "; ".join(parts) or "Ambiguous classification"


def _resolve_conflicts(
    best_pattern: Optional["BasePattern"],
    all_confidences: dict[str, float],
    patterns: list["BasePattern"],
) -> Optional["BasePattern"]:
    """Resolve conflicts when multiple patterns have similar confidence.

    Priority: binary > likert > demographics > scales (see _PATTERN_PRIORITY)
    """
    if best_pattern is None:
        return None

    # Get all patterns with confidence within 0.1 of best
    best_conf = all_confidences.get(best_pattern.pattern_id, 0.0)
    threshold = max(0.0, best_conf - 0.1)
    candidates = [
        p for p in patterns
        if all_confidences.get(p.pattern_id, 0.0) >= max(0.1, threshold - 0.1)
    ]

    if len(candidates) <= 1:
        return best_pattern

    # Sort by priority, then by confidence
    candidates_sorted = sorted(
        candidates,
        key=lambda p: (
            _PATTERN_PRIORITY.get(p.pattern_id, 0),
            all_confidences[p.pattern_id],
        ),
        reverse=True,
    )

    return candidates_sorted[0]
