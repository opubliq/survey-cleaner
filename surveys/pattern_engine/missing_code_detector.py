"""Detecting missing/sentinel codes in survey series.

Council decision (2026-02-18): Explicit detection as preprocessing step,
BEFORE computing n_unique or tiering. This ensures n_unique reflects
real response values, not artefacts from survey coding conventions.

Common patterns in Quebec/Canadian surveys:
  98 = Ne sait pas (NSP)
  99 = Ne répond pas / Refus (NR)
  -9 = System missing
  -1 = Not applicable / Refus
  97 = Not asked / Filter
  999, 9999 = Long-form missing codes
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pandas as pd

from surveys.pattern_engine.patterns.base_pattern import MissingCodeInfo

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema


# ---------------------------------------------------------------------------
# Known missing code patterns (heuristics)
# ---------------------------------------------------------------------------

# Common numeric missing sentinels in survey data
_COMMON_MISSING_CODES: set[int | float] = {
    -9, -8, -1,
    7, 8, 9,           # for 1-6 or 1-5 scales
    97, 98, 99,
    997, 998, 999,
    9997, 9998, 9999,
}

# Labels that indicate a value is a missing code
_MISSING_LABEL_KEYWORDS: tuple[str, ...] = (
    "ne sait pas", "nsp", "sais pas",
    "ne répond pas", "nr", "refus", "refuse",
    "non applicable", "n/a", "na",
    "non demandé", "non posée",
    "system missing", "missing",
    "don't know", "dk", "refused",
    "not applicable", "not asked",
    "sans objet",
)

# High outlier threshold: a value is suspicious if it's far above the
# apparent scale maximum (e.g. values of 98/99 in a 1-5 Likert scale).
_OUTLIER_MULTIPLIER = 5


def detect_missing_codes(
    series: pd.Series,
    var: Optional["VariableSchema"] = None,
    *,
    warn_threshold: float = 0.05,
) -> MissingCodeInfo:
    """Detect missing/sentinel codes in a survey series.

    Strategy (in order of priority):
    1. Use var.missing_codes if available (parser already identified them).
    2. Use var.value_labels with is_missing=True flag.
    3. Heuristic: known sentinel values present in data (98, 99, -9…).
    4. Heuristic: values that are clear outliers relative to main distribution.

    Args:
        series: Raw pandas Series (may include NaN).
        var: Optional VariableSchema from codebook parser.
        warn_threshold: If missing rate exceeds this, set high_missing_rate=True.

    Returns:
        MissingCodeInfo with detected codes, meanings, and a high-rate flag.
    """
    codes: set[int | float] = set()
    meanings: dict[int | float, str] = {}

    # --- Strategy 1 & 2: Use codebook info when available ---
    if var is not None:
        # Explicit missing_codes list
        for code in var.missing_codes:
            codes.add(code)

        # Value labels flagged is_missing
        for vl in var.value_labels:
            if vl.is_missing:
                codes.add(vl.value)
                meanings[vl.value] = vl.label
            # Also catch by label keyword even if is_missing not set
            elif _label_is_missing(vl.label):
                codes.add(vl.value)
                meanings[vl.value] = vl.label

    # --- Strategy 3 & 4: Heuristics on numeric values ---
    non_null: pd.Series = series.dropna()  # type: ignore[assignment]
    if non_null.empty:
        return MissingCodeInfo(codes=codes, meanings=meanings)

    try:
        _converted = pd.to_numeric(non_null, errors="coerce")
        numeric: pd.Series = pd.Series(_converted).dropna()  # type: ignore[assignment]
    except Exception:
        numeric = pd.Series(dtype=float)

    if numeric.empty:
        return MissingCodeInfo(codes=codes, meanings=meanings)

    present_values: set[int | float] = set(numeric.unique())  # type: ignore[arg-type]

    for candidate in _COMMON_MISSING_CODES:
        if candidate in present_values and candidate not in codes:
            # Check if this looks like a sentinel relative to non-sentinel values
            _non_sentinel_values: pd.Series = numeric[~numeric.isin(codes | {candidate})]  # type: ignore[assignment]
            if _looks_like_sentinel(candidate, _non_sentinel_values):
                codes.add(candidate)
                meanings[candidate] = _infer_meaning(candidate)

    # --- Strategy 4: Outlier heuristic ---
    # Values that are much larger than the apparent main cluster
    non_sentinel = pd.Series(numeric[~numeric.isin(list(codes))])  # type: ignore[arg-type]
    if len(non_sentinel) > 0:
        p95 = float(non_sentinel.quantile(0.95))
        if p95 > 0:
            outlier_candidates = pd.Series(non_sentinel[non_sentinel > p95 * _OUTLIER_MULTIPLIER])  # type: ignore[arg-type]
            for val in outlier_candidates.unique():
                if val not in codes:
                    codes.add(float(val))
                    meanings[float(val)] = "suspected missing (outlier)"

    # --- Compute high missing rate flag ---
    total_non_null = len(non_null)
    n_missing_values = int(non_null.isin(codes).sum()) if codes else 0
    rate = n_missing_values / total_non_null if total_non_null > 0 else 0.0
    high_missing_rate = rate > warn_threshold

    return MissingCodeInfo(
        codes=codes,
        meanings=meanings,
        high_missing_rate=high_missing_rate,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _label_is_missing(label: str) -> bool:
    """Return True if a value label looks like a missing code."""
    label_lower = label.lower().strip()
    return any(kw in label_lower for kw in _MISSING_LABEL_KEYWORDS)


def _looks_like_sentinel(value: int | float, numeric: pd.Series) -> bool:
    """Heuristic: does this value look like a sentinel rather than real data?

    A value is sentinel-like if:
    - It's a known round number (98, 99, -9…) AND
    - It's isolated (far from the bulk of the distribution)
    """
    if numeric.empty:
        return False

    q75 = numeric.quantile(0.75)
    # If value is far above the 75th percentile of the bulk, it's suspect
    if q75 > 0 and abs(value) > abs(q75) * 3:
        return True
    # If value is negative and the bulk is positive
    if value < 0 and numeric.median() > 0:
        return True
    return False


def _infer_meaning(code: int | float) -> str:
    """Return a human-readable meaning for a common missing code."""
    _MEANINGS: dict[int | float, str] = {
        -9: "system missing",
        -8: "not applicable",
        -1: "refus / not applicable",
        7: "NSP (code court)",
        8: "NR (code court)",
        9: "manquant (code court)",
        97: "non demandé",
        98: "ne sait pas (NSP)",
        99: "ne répond pas / refus (NR)",
        997: "non demandé",
        998: "ne sait pas (NSP)",
        999: "ne répond pas / refus (NR)",
        9997: "non demandé",
        9998: "ne sait pas (NSP)",
        9999: "ne répond pas / refus (NR)",
    }
    return _MEANINGS.get(code, f"missing sentinel ({code})")
