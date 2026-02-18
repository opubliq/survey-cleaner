"""Basic tests for pattern matching and classifier."""

import pytest

import pandas as pd
from surveys.codebook_parser.schemas.variable_schema import ValueLabel, VariableSchema
from surveys.pattern_engine.pattern_classifier import classify
from surveys.pattern_engine.patterns import (
    BinaryYesNoPattern,
    GenderPattern,
    Likert5AgreePattern,
    Thermometer0to10Pattern,
)


def test_likert_5_pattern():
    pattern = Likert5AgreePattern()
    series = pd.Series([1, 2, 3, 4, 5, 2, 1, 4, 3])

    confidence = pattern.matches(series)

    assert confidence >= 0.8, f"Likert5 should match with high confidence, got {confidence}"


def test_likert_5_with_missing_codes():
    pattern = Likert5AgreePattern()
    series = pd.Series([1, 2, 3, 4, 5, 98, 99, 2, 1, 98])

    from surveys.pattern_engine.missing_code_detector import detect_missing_codes
    missing_info = detect_missing_codes(series)

    confidence = pattern.matches(series, missing_info=missing_info)

    # With missing codes filtered out, should still match
    assert confidence >= 0.8, f"Likert5 with missing codes should match, got {confidence}"
    assert 98 in missing_info.codes and 99 in missing_info.codes


def test_binary_yes_no():
    pattern = BinaryYesNoPattern()
    series = pd.Series([1, 2, 1, 2, 1, 2])

    confidence = pattern.matches(series)

    assert confidence >= 0.8, f"Binary 1/2 should match, got {confidence}"


def test_thermometer_0_10():
    pattern = Thermometer0to10Pattern()
    series = pd.Series([0, 5, 10, 3, 7, 8, 2])

    confidence = pattern.matches(series)

    assert confidence >= 0.5, f"Thermometer 0-10 should match, got {confidence}"


def test_classifier_tier_1_likert():
    series = pd.Series([1, 2, 3, 4, 5, 2, 1, 4, 3, 5])
    result = classify(series)

    assert result.tier == 1, f"Likert series should be Tier 1, got {result.tier}"
    assert result.pattern_id == "likert_5_agree"
    assert result.confidence >= 0.8
    assert result.effective_n_unique == 5


def test_classifier_with_codebook():
    series = pd.Series([1, 2, 3, 4, 5, 98, 99])
    var = VariableSchema(
        var_name="Q1_satisfaction",
        var_label="Satisfaction envers le gouvernement",
        var_type="ordinal",
        scale_type="likert",
        value_labels=[
            ValueLabel(value=1, label="Tout à fait d'accord", is_missing=False),
            ValueLabel(value=2, label="Plutôt d'accord", is_missing=False),
            ValueLabel(value=3, label="Neutre", is_missing=False),
            ValueLabel(value=4, label="Plutôt en désaccord", is_missing=False),
            ValueLabel(value=5, label="Tout à fait en désaccord", is_missing=False),
            ValueLabel(value=98, label="Ne sait pas", is_missing=True),
            ValueLabel(value=99, label="Ne répond pas", is_missing=True),
        ],
        missing_codes=[98, 99],
    )

    result = classify(series, var)

    assert result.tier == 1, f"With codebook, should be Tier 1, got {result.tier}"
    assert result.pattern_id == "likert_5_agree"
    assert result.confidence >= 0.9  # Higher confidence with codebook


def test_classifier_tier_3_text():
    series = pd.Series(["Open response text", "Another answer", "Free form"])
    result = classify(series)

    assert result.tier == 3, f"Text data should be Tier 3, got {result.tier}"
    assert "text" in result.reason.lower() or "open-ended" in result.reason.lower()


def test_missing_code_detection():
    from surveys.pattern_engine.missing_code_detector import detect_missing_codes

    series = pd.Series([1, 2, 3, 98, 99, -9, 2, 1])
    missing_info = detect_missing_codes(series)

    assert missing_info.has_missing
    assert 98 in missing_info.codes
    assert 99 in missing_info.codes
    assert -9 in missing_info.codes


def test_missing_code_with_codebook():
    from surveys.pattern_engine.missing_code_detector import detect_missing_codes

    series = pd.Series([1, 2, 3, 4, 5, 98])
    var = VariableSchema(
        var_name="Q1",
        var_label="Test",
        var_type="ordinal",
        value_labels=[
            ValueLabel(value=1, label="A"),
            ValueLabel(value=2, label="B"),
            ValueLabel(value=3, label="C"),
            ValueLabel(value=4, label="D"),
            ValueLabel(value=5, label="E"),
            ValueLabel(value=98, label="Ne sait pas", is_missing=True),
        ],
        missing_codes=[98],
    )

    missing_info = detect_missing_codes(series, var)

    assert 98 in missing_info.codes
    assert missing_info.meanings.get(98) == "Ne sait pas"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
