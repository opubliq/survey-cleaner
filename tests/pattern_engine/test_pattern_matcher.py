"""Tests for PatternMatcher (signature-based matching)."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from surveys.pattern_engine import get_default_matcher
from surveys.pattern_engine.pattern_matcher import (
    MatchResult,
    NearMiss,
    PatternMatcher,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_pattern_library(tmp_path: Path) -> Path:
    """Create a temporary pattern library for testing."""
    library_data = {
        "patterns": [
            {
                "pattern_id": "likert_5_agree",
                "pattern_name": "Likert 5 points",
                "pattern_type": "likert",
                "detection_criteria": {
                    "unique_values": [1, 2, 3, 4, 5],
                    "range_min": 1,
                    "range_max": 5,
                    "n_unique": 5,
                    "name_keywords": ["accord", "agree", "satisf"],
                },
                "transformation_template": "df['{clean_var}'] = df['{original_var}'].map({mapping})",
                "examples_used": [],
                "validated": False,
                "metadata": {"notes": "Test pattern"},
            },
            {
                "pattern_id": "binary_yes_no",
                "pattern_name": "Binaire Oui/Non",
                "pattern_type": "binary",
                "detection_criteria": {
                    "unique_values": [1, 2],
                    "range_min": 0,
                    "range_max": 2,
                    "n_unique": 2,
                    "name_keywords": ["oui", "yes", "d'accord", "agree"],
                },
                "transformation_template": "df['{clean_var}'] = df['{original_var}'].map({mapping})",
                "examples_used": [],
                "validated": False,
                "metadata": {"notes": "Test binary"},
            },
        ]
    }

    library_path = tmp_path / "pattern_library.json"
    with open(library_path, "w") as f:
        json.dump(library_data, f)

    return library_path


@pytest.fixture
def matcher(temp_pattern_library: Path) -> PatternMatcher:
    """Create a PatternMatcher instance for testing."""
    return PatternMatcher(temp_pattern_library, threshold=0.8)


# ---------------------------------------------------------------------------
# Test PatternMatcher initialization
# ---------------------------------------------------------------------------


def test_matcher_initialization(temp_pattern_library: Path):
    """Test that matcher loads library correctly."""
    matcher = PatternMatcher(temp_pattern_library)

    assert matcher.threshold == 0.8
    assert len(matcher.library.patterns) == 2
    assert matcher.near_misses == []


def test_matcher_custom_threshold(temp_pattern_library: Path):
    """Test that matcher accepts custom threshold."""
    matcher = PatternMatcher(temp_pattern_library, threshold=0.7)

    assert matcher.threshold == 0.7


def test_matcher_file_not_found(tmp_path: Path):
    """Test that matcher raises error for non-existent library."""
    non_existent = tmp_path / "non_existent.json"

    with pytest.raises(FileNotFoundError):
        PatternMatcher(non_existent)


def test_matcher_log_near_misses_disabled(temp_pattern_library: Path):
    """Test that matcher can disable near-miss logging."""
    matcher = PatternMatcher(temp_pattern_library, log_near_misses=False)

    assert matcher.log_near_misses is False


# ---------------------------------------------------------------------------
# Test value overlap computation
# ---------------------------------------------------------------------------


def test_value_overlap_perfect_match(matcher: PatternMatcher):
    """Test perfect value overlap (observed = expected)."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    assert result is not None
    assert result.confidence >= 0.8
    assert result.pattern.pattern_id == "likert_5_agree"


def test_value_overlap_partial_match(matcher: PatternMatcher):
    """Test partial value overlap (observed subset of expected)."""
    signature = {
        "unique_values": [1, 2, 3],
        "min_val": 1.0,
        "max_val": 3.0,
        "n_unique": 3,
    }

    result = matcher.match(signature)

    # Partial overlap with threshold 0.8: returns None (confidence ~0.665)
    # But near-misses should be logged
    assert result is None
    assert len(matcher.near_misses) > 0
    assert matcher.near_misses[0].pattern.pattern_id == "likert_5_agree"


def test_value_overlap_no_match(matcher: PatternMatcher):
    """Test no value overlap (values outside expected range)."""
    signature = {
        "unique_values": [6, 7, 8, 9, 10],
        "min_val": 6.0,
        "max_val": 10.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    # Should not match any pattern with threshold 0.8
    assert result is None


# ---------------------------------------------------------------------------
# Test range match computation
# ---------------------------------------------------------------------------


def test_range_match_within_expected(matcher: PatternMatcher):
    """Test that observed range within expected gets full score."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    assert result is not None
    assert result.match_details["range_match_score"] == 1.0


def test_range_match_slight_exceed(matcher: PatternMatcher):
    """Test slight range exceed gets partial score."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.5,  # 10% exceed (expected span = 4, tolerance = 0.4)
        "n_unique": 5,
    }

    result = matcher.match(signature)

    # With threshold 0.8, slight exceed returns None (confidence ~0.775)
    # But should log near-miss
    assert result is None
    assert len(matcher.near_misses) > 0
    assert 0.6 <= matcher.near_misses[0].confidence < 0.8


def test_range_match_outside(matcher: PatternMatcher):
    """Test range completely outside expected gets no score."""
    signature = {
        "unique_values": [10, 11, 12, 13, 14],
        "min_val": 10.0,
        "max_val": 14.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    assert result is None


# ---------------------------------------------------------------------------
# Test keyword match computation
# ---------------------------------------------------------------------------


def test_keyword_match_in_var_name(matcher: PatternMatcher):
    """Test keyword found in variable name."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    codebook_entry = {
        "var_name": "q_agreement_satisfaction",
        "var_label": "Agreement level",
    }

    result = matcher.match(signature, codebook_entry)

    assert result is not None
    assert result.match_details["keyword_match_score"] == 1.0


def test_keyword_match_in_var_label(matcher: PatternMatcher):
    """Test keyword found in variable label."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    codebook_entry = {
        "var_name": "q2",
        "var_label": "Satisfaction with service (satisfait ou non)",
    }

    result = matcher.match(signature, codebook_entry)

    assert result is not None
    assert result.match_details["keyword_match_score"] == 1.0


def test_keyword_match_no_keywords(matcher: PatternMatcher):
    """Test no keyword match when keywords not in name/label."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    codebook_entry = {
        "var_name": "q2_response",
        "var_label": "Response to question 2",
    }

    result = matcher.match(signature, codebook_entry)

    # Should still match likert_5_agree based on values alone
    assert result is not None
    # But keyword score is 0.0
    assert result.match_details["keyword_match_score"] == 0.0


def test_keyword_match_no_codebook(matcher: PatternMatcher):
    """Test neutral keyword score when no codebook entry provided."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    result = matcher.match(signature, codebook_entry=None)

    assert result is not None
    # Neutral score when no codebook info
    assert result.match_details["keyword_match_score"] == 0.5


# ---------------------------------------------------------------------------
# Test n_unique match computation
# ---------------------------------------------------------------------------


def test_n_unique_exact_match(matcher: PatternMatcher):
    """Test exact n_unique match."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    assert result is not None
    assert result.match_details["n_unique_match_score"] == 1.0


def test_n_unique_within_one(matcher: PatternMatcher):
    """Test n_unique within 1 of expected."""
    signature = {
        "unique_values": [1, 2, 3, 4],
        "min_val": 1.0,
        "max_val": 4.0,
        "n_unique": 4,
    }

    result = matcher.match(signature)

    assert result is not None
    assert result.match_details["n_unique_match_score"] == 0.7


def test_n_unique_far_off(matcher: PatternMatcher):
    """Test n_unique far off from expected."""
    signature = {
        "unique_values": [1, 2],
        "min_val": 1.0,
        "max_val": 2.0,
        "n_unique": 2,
    }

    result = matcher.match(signature)

    # Should match binary instead
    assert result is not None
    assert result.pattern.pattern_id == "binary_yes_no"
    # Likert_5_agree n_unique score is 0.0


# ---------------------------------------------------------------------------
# Test near-miss logging
# ---------------------------------------------------------------------------


def test_near_miss_logging(matcher: PatternMatcher):
    """Test that near-misses are logged."""
    signature = {
        "unique_values": [1, 2, 3],  # Partial match for likert_5_agree
        "min_val": 1.0,
        "max_val": 3.0,
        "n_unique": 3,
        "variable_id": "test_var_123",
    }

    result = matcher.match(signature)

    # Near-misses should be logged
    assert len(matcher.near_misses) > 0

    # Check that near-miss has required attributes
    near_miss = matcher.near_misses[0]
    assert isinstance(near_miss, NearMiss)
    assert near_miss.confidence < matcher.threshold
    assert 0.6 <= near_miss.confidence
    assert near_miss.variable_id == "test_var_123"


def test_clear_near_misses(matcher: PatternMatcher):
    """Test clearing near-misses."""
    signature = {
        "unique_values": [1, 2, 3],
        "min_val": 1.0,
        "max_val": 3.0,
        "n_unique": 3,
        "variable_id": "test_var",
    }

    matcher.match(signature)
    assert len(matcher.near_misses) > 0

    matcher.clear_near_misses()
    assert len(matcher.near_misses) == 0


def test_get_near_misses_sorted(matcher: PatternMatcher):
    """Test that get_near_misses returns sorted list."""
    signature = {
        "unique_values": [1, 2, 3],
        "min_val": 1.0,
        "max_val": 3.0,
        "n_unique": 3,
        "variable_id": "test_var",
    }

    matcher.match(signature)

    near_misses = matcher.get_near_misses()

    assert len(near_misses) > 0

    # Check sorted descending by confidence
    confidences = [nm.confidence for nm in near_misses]
    assert confidences == sorted(confidences, reverse=True)


# ---------------------------------------------------------------------------
# Test threshold behavior
# ---------------------------------------------------------------------------


def test_threshold_filtering_high_threshold(matcher: PatternMatcher):
    """Test that high threshold filters out low-confidence matches."""
    matcher.threshold = 0.9

    signature = {
        "unique_values": [1, 2, 3],  # Partial match
        "n_unique": 3,
    }

    result = matcher.match(signature)

    # Should return None due to high threshold
    assert result is None


def test_threshold_filtering_low_threshold(matcher: PatternMatcher):
    """Test that low threshold allows more matches."""
    matcher.threshold = 0.5

    signature = {
        "unique_values": [1, 2, 3],  # Partial match
        "min_val": 1.0,
        "max_val": 3.0,
        "n_unique": 3,
    }

    result = matcher.match(signature)

    # Should return match with low threshold
    assert result is not None


# ---------------------------------------------------------------------------
# Test pattern library updates
# ---------------------------------------------------------------------------


def test_update_pattern_library(temp_pattern_library: Path):
    """Test updating pattern library."""
    from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

    matcher = PatternMatcher(temp_pattern_library)

    new_criteria = DetectionCriteria(
        unique_values=[1, 2, 3, 4, 5, 6, 7],
        range_min=1,
        range_max=7,
        n_unique=7,
        name_keywords=["accord", "agree"],
    )

    matcher.update_pattern_library("likert_5_agree", new_criteria)

    # Check that library was updated in memory
    pattern = next(
        (p for p in matcher.library.patterns if p.pattern_id == "likert_5_agree"),
        None,
    )
    assert pattern is not None
    assert pattern.detection_criteria.n_unique == 7

    # Check that library was saved to disk
    with open(temp_pattern_library) as f:
        saved_data = json.load(f)

    saved_pattern = next(
        (p for p in saved_data["patterns"] if p["pattern_id"] == "likert_5_agree"),
        None,
    )
    assert saved_pattern is not None
    assert saved_pattern["detection_criteria"]["n_unique"] == 7


def test_update_pattern_library_nonexistent(temp_pattern_library: Path):
    """Test updating non-existent pattern raises error."""
    matcher = PatternMatcher(temp_pattern_library)

    from surveys.pattern_engine.schemas.pattern_schema import DetectionCriteria

    new_criteria = DetectionCriteria(
        unique_values=[1, 2],
        range_min=1,
        range_max=2,
        n_unique=2,
        name_keywords=["test"],
    )

    with pytest.raises(ValueError, match="Pattern not found"):
        matcher.update_pattern_library("nonexistent_pattern", new_criteria)


# ---------------------------------------------------------------------------
# Test get_default_matcher
# ---------------------------------------------------------------------------


def test_get_default_matcher():
    """Test get_default_matcher convenience function."""
    matcher = get_default_matcher()

    assert isinstance(matcher, PatternMatcher)
    assert matcher.threshold == 0.8
    assert matcher.log_near_misses is True
    assert len(matcher.library.patterns) > 0


def test_get_default_matcher_custom_threshold():
    """Test get_default_matcher with custom threshold."""
    matcher = get_default_matcher(threshold=0.7)

    assert matcher.threshold == 0.7


# ---------------------------------------------------------------------------
# Test MatchResult details
# ---------------------------------------------------------------------------


def test_match_result_details_structure(matcher: PatternMatcher):
    """Test that MatchResult has correct structure."""
    signature = {
        "unique_values": [1, 2, 3, 4, 5],
        "min_val": 1.0,
        "max_val": 5.0,
        "n_unique": 5,
    }

    result = matcher.match(signature)

    assert isinstance(result, MatchResult)
    assert hasattr(result, "pattern")
    assert hasattr(result, "confidence")
    assert hasattr(result, "match_details")

    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.match_details, dict)

    # Check detail keys
    expected_keys = {
        "value_overlap_score",
        "range_match_score",
        "keyword_match_score",
        "n_unique_match_score",
        "summary",
    }
    assert set(result.match_details.keys()) == expected_keys
