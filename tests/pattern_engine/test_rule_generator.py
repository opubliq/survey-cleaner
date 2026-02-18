"""Tests for RuleGenerator (generates Python code from pattern + codebook)."""

import pytest

from surveys.codebook_parser.schemas.variable_schema import ValueLabel, VariableSchema
from surveys.pattern_engine.pattern_matcher import MatchResult
from surveys.pattern_engine.rule_generator import (
    GeneratedRule,
    RuleGenerator,
    generate_rule,
    generate_rule_from_match,
)
from surveys.pattern_engine.schemas.pattern_schema import (
    DetectionCriteria,
    Pattern,
)


@pytest.fixture
def likert_pattern() -> Pattern:
    return Pattern(
        pattern_id="likert_5_agree",
        pattern_name="Likert 5 points - Accord/Désaccord standard QC",
        pattern_type="likert",
        detection_criteria=DetectionCriteria(
            unique_values=[1, 2, 3, 4, 5],
            range_min=1,
            range_max=5,
            n_unique=5,
            name_keywords=["accord", "agree", "satisf"],
        ),
        transformation_template=(
            "df['{clean_var}'] = df['{original_var}'].map({mapping})\n"
            "df['{clean_var}'] = df['{clean_var}'].astype('category')"
        ),
    )


@pytest.fixture
def thermometer_pattern() -> Pattern:
    return Pattern(
        pattern_id="thermometer_0_10",
        pattern_name="Thermomètre politique 0-10",
        pattern_type="scale",
        detection_criteria=DetectionCriteria(
            range_min=0,
            range_max=10,
            n_unique=11,
            name_keywords=["thermom", "feeling"],
        ),
        transformation_template=(
            "df['{clean_var}'] = df['{original_var}'].astype('float')\n"
            "# Values should be in range [0, 10]\n"
            "df.loc[(df['{clean_var}'] < 0) | (df['{clean_var}'] > 10), '{clean_var}'] = None"
        ),
    )


@pytest.fixture
def codebook_entry() -> VariableSchema:
    return VariableSchema(
        var_name="Q5_satisfaction",
        var_label="Satisfaction with the service",
        var_type="ordinal",
        scale_type="likert",
        value_labels=[
            ValueLabel(value=1, label="Tout à fait d'accord", is_missing=False),
            ValueLabel(value=2, label="Plutôt d'accord", is_missing=False),
            ValueLabel(value=3, label="Ni d'accord ni en désaccord", is_missing=False),
            ValueLabel(value=4, label="Plutôt en désaccord", is_missing=False),
            ValueLabel(value=5, label="Tout à fait en désaccord", is_missing=False),
            ValueLabel(value=98, label="NSP", is_missing=True),
            ValueLabel(value=99, label="NR", is_missing=True),
        ],
        missing_codes=[98, 99],
    )


@pytest.fixture
def codebook_entry_dict() -> dict:
    return {
        "var_name": "Q5_satisfaction",
        "var_label": "Satisfaction with the service",
        "var_type": "ordinal",
        "value_labels": [
            {"value": 1, "label": "Tout à fait d'accord", "is_missing": False},
            {"value": 2, "label": "Plutôt d'accord", "is_missing": False},
            {"value": 3, "label": "Ni d'accord ni en désaccord", "is_missing": False},
            {"value": 4, "label": "Plutôt en désaccord", "is_missing": False},
            {"value": 5, "label": "Tout à fait en désaccord", "is_missing": False},
            {"value": 98, "label": "NSP", "is_missing": True},
            {"value": 99, "label": "NR", "is_missing": True},
        ],
        "missing_codes": [98, 99],
    }


class TestRuleGeneratorBasic:
    def test_generate_categorical_with_codebook(
        self, likert_pattern: Pattern, codebook_entry: VariableSchema
    ):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5_satisfaction",
            clean_var="satisfaction",
            codebook_entry=codebook_entry,
        )

        assert isinstance(result, GeneratedRule)
        assert result.pattern_id == "likert_5_agree"
        assert result.original_var == "Q5_satisfaction"
        assert result.clean_var == "satisfaction"
        assert result.has_missing_codes is True
        assert result.missing_codes_handled == [98, 99]

        assert "df['satisfaction']" in result.code
        assert "df['Q5_satisfaction']" in result.code
        assert "Tout à fait d'accord" in result.code
        assert "98" in result.code or "99" in result.code

    def test_generate_categorical_with_dict_codebook(
        self, likert_pattern: Pattern, codebook_entry_dict: dict
    ):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5_satisfaction",
            clean_var="satisfaction",
            codebook_entry=codebook_entry_dict,
        )

        assert isinstance(result, GeneratedRule)
        assert "Tout à fait d'accord" in result.code

    def test_generate_categorical_without_codebook(self, likert_pattern: Pattern):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5_satisfaction",
            clean_var="satisfaction",
            codebook_entry=None,
        )

        assert isinstance(result, GeneratedRule)
        assert "df['satisfaction']" in result.code
        assert result.has_missing_codes is False
        assert result.missing_codes_handled is None

    def test_generate_scale_pattern(self, thermometer_pattern: Pattern):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=thermometer_pattern,
            original_var="Q10_feeling",
            clean_var="feeling_thermometer",
            codebook_entry=None,
        )

        assert isinstance(result, GeneratedRule)
        assert ".astype('float')" in result.code
        assert "mapping" not in result.code.lower() or "{}" in result.code


class TestRuleGeneratorMissingCodes:
    def test_missing_codes_excluded_from_mapping(
        self, likert_pattern: Pattern, codebook_entry: VariableSchema
    ):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5_satisfaction",
            clean_var="satisfaction",
            codebook_entry=codebook_entry,
        )

        assert "98: 'NSP'" not in result.code
        assert "99: 'NR'" not in result.code
        assert result.has_missing_codes is True

    def test_missing_code_handling_added(self, likert_pattern: Pattern, codebook_entry: VariableSchema):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5_satisfaction",
            clean_var="satisfaction",
            codebook_entry=codebook_entry,
        )

        assert ".isin([" in result.code or "98" in result.code


class TestRuleGeneratorFormatting:
    def test_mapping_sorted_correctly(self, likert_pattern: Pattern, codebook_entry: VariableSchema):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5",
            clean_var="clean_q5",
            codebook_entry=codebook_entry,
        )

        one_pos = result.code.find("1:")
        two_pos = result.code.find("2:")
        three_pos = result.code.find("3:")
        four_pos = result.code.find("4:")
        five_pos = result.code.find("5:")

        assert one_pos < two_pos < three_pos < four_pos < five_pos

    def test_header_comment_included(self, likert_pattern: Pattern, codebook_entry: VariableSchema):
        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q5",
            clean_var="clean_q5",
            codebook_entry=codebook_entry,
        )

        assert "# Likert 5 points" in result.code
        assert "likert_5_agree" in result.code


class TestConvenienceFunctions:
    def test_generate_rule_function(self, likert_pattern: Pattern):
        result = generate_rule(
            pattern=likert_pattern,
            original_var="Q1",
            clean_var="q1_clean",
        )

        assert isinstance(result, GeneratedRule)
        assert result.original_var == "Q1"
        assert result.clean_var == "q1_clean"

    def test_generate_rule_from_match_function(self, likert_pattern: Pattern):
        match_result = MatchResult(
            pattern=likert_pattern,
            confidence=0.95,
            match_details={"summary": "test"},
        )

        result = generate_rule_from_match(
            match_result=match_result,
            original_var="Q1",
            clean_var="q1_clean",
        )

        assert isinstance(result, GeneratedRule)
        assert result.pattern_id == "likert_5_agree"


class TestEdgeCases:
    def test_empty_value_labels(self, likert_pattern: Pattern):
        empty_codebook = VariableSchema(
            var_name="Q_empty",
            var_label="Empty variable",
            var_type="unknown",
            value_labels=[],
        )

        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q_empty",
            clean_var="empty_clean",
            codebook_entry=empty_codebook,
        )

        assert isinstance(result, GeneratedRule)
        assert "{}" in result.code

    def test_codebook_with_only_missing_codes(self, likert_pattern: Pattern):
        all_missing_codebook = VariableSchema(
            var_name="Q_missing",
            var_label="All missing",
            var_type="categorical",
            value_labels=[
                ValueLabel(value=98, label="NSP", is_missing=True),
                ValueLabel(value=99, label="NR", is_missing=True),
            ],
            missing_codes=[98, 99],
        )

        generator = RuleGenerator()
        result = generator.generate(
            pattern=likert_pattern,
            original_var="Q_missing",
            clean_var="missing_clean",
            codebook_entry=all_missing_codebook,
        )

        assert isinstance(result, GeneratedRule)
        assert "{}" in result.code
