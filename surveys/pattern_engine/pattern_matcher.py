"""Pattern matcher for signature-based matching against pattern_library.json.

This module provides a lightweight matching engine that:
1. Loads patterns from pattern_library.json
2. Matches variable signatures against patterns using detection criteria
3. Computes confidence scores (0-1) based on multiple factors
4. Logs near-misses for pattern library improvement

The matcher is designed to work independently from the OOP pattern classes,
enabling fast signature-based matching without loading Python pattern classes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from surveys.pattern_engine.schemas.pattern_schema import (
    DetectionCriteria,
    Pattern,
    PatternLibrary,
)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class MatchResult:
    """Result of pattern matching."""
    pattern: Pattern
    confidence: float
    match_details: dict  # Breakdown of how confidence was computed


@dataclass
class NearMiss:
    """A pattern that almost matched (confidence in [0.6, threshold))."""
    pattern: Pattern
    confidence: float
    variable_id: str
    reason: str


# ---------------------------------------------------------------------------
# Main PatternMatcher class
# ---------------------------------------------------------------------------


class PatternMatcher:
    """Signature-based pattern matcher against pattern_library.json.

    The matcher computes confidence scores based on:
    - Value overlap: how many observed unique values match pattern's unique_values
    - Range match: whether observed min/max fit within pattern's range_min/max
    - Keyword match: whether variable name/label contains pattern's keywords
    - n_unique match: whether observed n_unique matches pattern's expected count

    Confidence is a weighted average of these factors (see _compute_confidence).
    """

    # Weights for different matching factors (sum to 1.0)
    _WEIGHT_VALUE_OVERLAP = 0.40
    _WEIGHT_RANGE_MATCH = 0.25
    _WEIGHT_KEYWORD_MATCH = 0.20
    _WEIGHT_N_UNIQUE_MATCH = 0.15

    def __init__(
        self,
        library_path: str | Path,
        threshold: float = 0.8,
        log_near_misses: bool = True,
    ):
        """Initialize pattern matcher.

        Args:
            library_path: Path to pattern_library.json
            threshold: Minimum confidence to return a match (default: 0.8)
            log_near_misses: Whether to track near-misses for library improvement
        """
        self.library_path = Path(library_path)
        self.threshold = threshold
        self.log_near_misses = log_near_misses
        self.near_misses: list[NearMiss] = []

        # Load pattern library
        self.library = self._load_library()

    def _load_library(self) -> PatternLibrary:
        """Load pattern library from JSON file."""
        if not self.library_path.exists():
            raise FileNotFoundError(
                f"Pattern library not found: {self.library_path}"
            )

        with open(self.library_path) as f:
            data = json.load(f)

        return PatternLibrary(**data)

    def match(
        self,
        variable_signature: dict,
        codebook_entry: Optional[dict] = None,
    ) -> Optional[MatchResult]:
        """Match a variable signature against all patterns.

        Args:
            variable_signature: Dictionary with variable statistics from classifier:
                - unique_values: list[int] - observed unique values
                - min_val: Optional[float] - minimum value
                - max_val: Optional[float] - maximum value
                - n_unique: int - number of unique values
                - variable_id: str - variable identifier
            codebook_entry: Optional dictionary from parsed codebook JSON:
                - var_name: Optional[str]
                - var_label: Optional[str]

        Returns:
            MatchResult with best pattern if confidence >= threshold, else None.
            Near-misses are logged internally if log_near_misses is True.
        """
        best_match = None
        best_confidence = 0.0
        best_details = {}

        for pattern in self.library.patterns:
            confidence, details = self._compute_confidence(
                variable_signature,
                pattern,
                codebook_entry,
            )

            # Update best match
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = pattern
                best_details = details

            # Log near-misses (confidence in [0.6, threshold))
            if self.log_near_misses and 0.6 <= confidence < self.threshold:
                self.near_misses.append(
                    NearMiss(
                        pattern=pattern,
                        confidence=confidence,
                        variable_id=variable_signature.get("variable_id", "unknown"),
                        reason=f"Near-miss: {details['summary']}",
                    )
                )

        # Return match only if above threshold
        if best_match and best_confidence >= self.threshold:
            return MatchResult(
                pattern=best_match,
                confidence=best_confidence,
                match_details=best_details,
            )

        return None

    def _compute_confidence(
        self,
        variable_signature: dict,
        pattern: Pattern,
        codebook_entry: Optional[dict],
    ) -> tuple[float, dict]:
        """Compute confidence score [0-1] for a pattern.

        Returns:
            Tuple of (confidence_score, details_dict)
        """
        details = {
            "value_overlap_score": 0.0,
            "range_match_score": 0.0,
            "keyword_match_score": 0.0,
            "n_unique_match_score": 0.0,
            "summary": "",
        }

        criteria = pattern.detection_criteria
        scores = []

        # 1. Value overlap score (40% weight)
        value_overlap_score = self._compute_value_overlap(
            variable_signature.get("unique_values", []),
            criteria.unique_values,
        )
        details["value_overlap_score"] = value_overlap_score
        scores.append(
            (value_overlap_score, self._WEIGHT_VALUE_OVERLAP, "value_overlap")
        )

        # 2. Range match score (25% weight)
        range_match_score = self._compute_range_match(
            variable_signature.get("min_val"),
            variable_signature.get("max_val"),
            criteria.range_min,
            criteria.range_max,
        )
        details["range_match_score"] = range_match_score
        scores.append(
            (range_match_score, self._WEIGHT_RANGE_MATCH, "range_match")
        )

        # 3. Keyword match score (20% weight)
        keyword_match_score = self._compute_keyword_match(
            codebook_entry,
            criteria.name_keywords,
        )
        details["keyword_match_score"] = keyword_match_score
        scores.append(
            (keyword_match_score, self._WEIGHT_KEYWORD_MATCH, "keyword_match")
        )

        # 4. n_unique match score (15% weight)
        n_unique_match_score = self._compute_n_unique_match(
            variable_signature.get("n_unique"),
            criteria.n_unique,
        )
        details["n_unique_match_score"] = n_unique_match_score
        scores.append(
            (n_unique_match_score, self._WEIGHT_N_UNIQUE_MATCH, "n_unique_match")
        )

        # Compute weighted average
        confidence = sum(score * weight for score, weight, _ in scores)

        # Build summary
        detail_strings = [
            f"{name}={score:.2f}" for score, _, name in scores
        ]
        details["summary"] = ", ".join(detail_strings)

        return confidence, details

    def _compute_value_overlap(
        self,
        observed_values: list[int],
        expected_values: Optional[list[int]],
    ) -> float:
        """Compute overlap score between observed and expected values.

        Score formula:
        - 1.0 if observed is subset of expected and covers >=80% of expected
        - 0.0 if observed has values outside expected range
        - Otherwise: (observed ∩ expected) / expected * coverage_factor

        Returns:
            Score in [0, 1]
        """
        if not expected_values:
            return 0.5  # Neutral score if no expected values defined

        if not observed_values:
            return 0.0

        observed_set = set(observed_values)
        expected_set = set(expected_values)

        # Reject if any value outside expected
        if not observed_set.issubset(expected_set):
            # Partial overlap: penalize heavily
            overlap = len(observed_set & expected_set)
            return min(0.3, overlap / len(expected_set))

        # Perfect match coverage
        coverage = len(observed_set) / len(expected_set)

        if coverage >= 0.8:
            return 1.0

        # Partial coverage
        return coverage * 0.8  # Max 0.8 for partial coverage

    def _compute_range_match(
        self,
        observed_min: Optional[float],
        observed_max: Optional[float],
        expected_min: Optional[int],
        expected_max: Optional[int],
    ) -> float:
        """Compute range match score.

        Score formula:
        - 1.0 if observed range is within expected range
        - 0.5 if observed range overlaps but exceeds slightly (≤10%)
        - 0.0 if observed range is completely outside

        Returns:
            Score in [0, 1]
        """
        if expected_min is None or expected_max is None:
            return 0.5  # Neutral score if no range defined

        if observed_min is None or observed_max is None:
            return 0.0

        # Perfect match
        if expected_min <= observed_min and observed_max <= expected_max:
            return 1.0

        # Slight exceed (≤10%)
        expected_span = expected_max - expected_min
        tolerance = expected_span * 0.1

        min_diff = max(0, expected_min - observed_min)
        max_diff = max(0, observed_max - expected_max)

        if min_diff <= tolerance and max_diff <= tolerance:
            return 0.5

        # No match
        return 0.0

    def _compute_keyword_match(
        self,
        codebook_entry: Optional[dict],
        expected_keywords: Optional[list[str]],
    ) -> float:
        """Compute keyword match score.

        Score formula:
        - 1.0 if any keyword found in var_name or var_label
        - 0.0 if no keywords or no match

        Returns:
            Score in [0, 1]
        """
        if not expected_keywords:
            return 0.5  # Neutral score if no keywords defined

        if not codebook_entry:
            return 0.5  # Neutral score if no codebook info

        var_name = codebook_entry.get("var_name", "") or ""
        var_label = codebook_entry.get("var_label", "") or ""

        search_text = f"{var_name} {var_label}".lower()

        # Check for keyword matches
        for keyword in expected_keywords:
            if keyword.lower() in search_text:
                return 1.0

        return 0.0

    def _compute_n_unique_match(
        self,
        observed_n_unique: Optional[int],
        expected_n_unique: Optional[int],
    ) -> float:
        """Compute n_unique match score.

        Score formula:
        - 1.0 if exact match
        - 0.7 if within 1 of expected
        - 0.5 if within 2 of expected
        - 0.0 otherwise

        Returns:
            Score in [0, 1]
        """
        if expected_n_unique is None:
            return 0.5  # Neutral score if no n_unique defined

        if observed_n_unique is None:
            return 0.0

        diff = abs(observed_n_unique - expected_n_unique)

        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.7
        elif diff == 2:
            return 0.5
        else:
            return 0.0

    def get_near_misses(self) -> list[NearMiss]:
        """Return all logged near-misses.

        Useful for:
        - Identifying patterns that need adjustment
        - Discovering new pattern types
        - Improving detection criteria

        Returns:
            List of NearMiss objects sorted by confidence (descending).
        """
        return sorted(
            self.near_misses,
            key=lambda nm: nm.confidence,
            reverse=True,
        )

    def clear_near_misses(self) -> None:
        """Clear logged near-misses."""
        self.near_misses.clear()

    def update_pattern_library(
        self,
        pattern_id: str,
        new_criteria: DetectionCriteria,
    ) -> None:
        """Update a pattern's detection criteria in the library.

        This method modifies the in-memory library and saves to disk.

        Args:
            pattern_id: ID of pattern to update
            new_criteria: New detection criteria to apply
        """
        for pattern in self.library.patterns:
            if pattern.pattern_id == pattern_id:
                pattern.detection_criteria = new_criteria
                break
        else:
            raise ValueError(f"Pattern not found: {pattern_id}")

        # Save to disk
        with open(self.library_path, "w") as f:
            json.dump(
                self.library.model_dump(),
                f,
                indent=2,
                ensure_ascii=False,
            )


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------


def get_default_matcher(threshold: float = 0.8) -> PatternMatcher:
    """Get a PatternMatcher instance with default library path.

    Args:
        threshold: Minimum confidence for matches

    Returns:
        PatternMatcher instance
    """
    library_path = Path(__file__).parent / "pattern_library.json"
    return PatternMatcher(library_path, threshold=threshold)
