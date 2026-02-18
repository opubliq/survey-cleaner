"""Tests for RuleValidator (validates generated rules via LLM)."""

import json
from unittest.mock import MagicMock, patch

import pytest

from surveys.codebook_parser.schemas.variable_schema import ValueLabel, VariableSchema
from surveys.pattern_engine.rule_generator import GeneratedRule
from surveys.pattern_engine.rule_validator import (
    RuleValidator,
    ValidationError,
    ValidationResult,
    validate_rule,
)


@pytest.fixture
def generated_rule() -> GeneratedRule:
    return GeneratedRule(
        code="# Likert 5 points (likert_5_agree)\ndf['satisfaction'] = df['Q5'].map({1: 'Très satisfait', 2: 'Plutôt satisfait', 3: 'Neutre', 4: 'Plutôt insatisfait', 5: 'Très insatisfait'})\ndf.loc[df['satisfaction'].isin([98, 99]), 'satisfaction'] = None",
        pattern_id="likert_5_agree",
        pattern_name="Likert 5 points",
        original_var="Q5",
        clean_var="satisfaction",
        has_missing_codes=True,
        missing_codes_handled=[98, 99],
    )


@pytest.fixture
def codebook_entry() -> VariableSchema:
    return VariableSchema(
        var_name="Q5",
        var_label="Satisfaction with the service",
        var_type="ordinal",
        value_labels=[
            ValueLabel(value=1, label="Très satisfait", is_missing=False),
            ValueLabel(value=2, label="Plutôt satisfait", is_missing=False),
            ValueLabel(value=3, label="Neutre", is_missing=False),
            ValueLabel(value=4, label="Plutôt insatisfait", is_missing=False),
            ValueLabel(value=5, label="Très insatisfait", is_missing=False),
            ValueLabel(value=98, label="NSP", is_missing=True),
            ValueLabel(value=99, label="NR", is_missing=True),
        ],
        missing_codes=[98, 99],
    )


@pytest.fixture
def codebook_entry_dict() -> dict:
    return {
        "var_name": "Q5",
        "var_label": "Satisfaction with the service",
        "var_type": "ordinal",
        "value_labels": [
            {"value": 1, "label": "Très satisfait", "is_missing": False},
            {"value": 2, "label": "Plutôt satisfait", "is_missing": False},
            {"value": 3, "label": "Neutre", "is_missing": False},
            {"value": 4, "label": "Plutôt insatisfait", "is_missing": False},
            {"value": 5, "label": "Très insatisfait", "is_missing": False},
            {"value": 98, "label": "NSP", "is_missing": True},
            {"value": 99, "label": "NR", "is_missing": True},
        ],
        "missing_codes": [98, 99],
    }


class TestValidationResult:
    def test_final_code_returns_corrected_when_available(self):
        result = ValidationResult(
            is_valid=True,
            original_code="original code",
            corrected_code="corrected code",
        )
        assert result.final_code == "corrected code"

    def test_final_code_returns_original_when_no_correction(self):
        result = ValidationResult(
            is_valid=True,
            original_code="original code",
            corrected_code=None,
        )
        assert result.final_code == "original code"

    def test_default_values(self):
        result = ValidationResult(
            is_valid=False,
            original_code="code",
        )
        assert result.errors == []
        assert result.attempts == 1
        assert result.escalated is False


class TestValidationError:
    def test_validation_error_creation(self):
        error = ValidationError(
            error_type="mapping",
            message="Missing value 3 in mapping",
            suggested_fix="Add 3: 'Neutre' to mapping",
        )
        assert error.error_type == "mapping"
        assert error.message == "Missing value 3 in mapping"
        assert error.suggested_fix == "Add 3: 'Neutre' to mapping"

    def test_validation_error_without_suggested_fix(self):
        error = ValidationError(
            error_type="missing_code",
            message="Missing code 98 not handled",
        )
        assert error.suggested_fix is None


class TestRuleValidatorPrompt:
    def test_build_prompt_includes_codebook_info(
        self, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        validator = RuleValidator()
        prompt = validator._build_prompt(
            rule=generated_rule,
            codebook_entry=codebook_entry,
            sample_data=[1, 2, 3],
            current_code=generated_rule.code,
        )

        assert "Q5" in prompt
        assert "Satisfaction with the service" in prompt
        assert "ordinal" in prompt
        assert "Très satisfait" in prompt
        assert "[98, 99]" in prompt

    def test_build_prompt_with_dict_codebook(
        self, generated_rule: GeneratedRule, codebook_entry_dict: dict
    ):
        validator = RuleValidator()
        prompt = validator._build_prompt(
            rule=generated_rule,
            codebook_entry=codebook_entry_dict,
            sample_data=None,
            current_code=generated_rule.code,
        )

        assert "Q5" in prompt
        assert "Satisfaction with the service" in prompt
        assert "Très satisfait" in prompt

    def test_build_prompt_without_codebook(self, generated_rule: GeneratedRule):
        validator = RuleValidator()
        prompt = validator._build_prompt(
            rule=generated_rule,
            codebook_entry=None,
            sample_data=None,
            current_code=generated_rule.code,
        )

        assert "Q5" in prompt
        assert "unknown" in prompt

    def test_build_prompt_with_sample_data(
        self, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        validator = RuleValidator()
        sample = [1.0, 2.0, 3.0, 98.0, 5.0]
        prompt = validator._build_prompt(
            rule=generated_rule,
            codebook_entry=codebook_entry,
            sample_data=sample,
            current_code=generated_rule.code,
        )

        assert "[1.0, 2.0, 3.0, 98.0, 5.0]" in prompt


class TestRuleValidatorParseResponse:
    def test_parse_valid_response(self):
        validator = RuleValidator()
        response = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        result = validator._parse_response(response)
        assert result["valid"] is True
        assert result["errors"] == []
        assert result["corrected_code"] is None

    def test_parse_invalid_response_with_errors(self):
        validator = RuleValidator()
        response = json.dumps({
            "valid": False,
            "errors": ["Missing value 3 in mapping", "Missing code 98 not handled"],
            "corrected_code": "corrected code here",
        })

        result = validator._parse_response(response)
        assert result["valid"] is False
        assert len(result["errors"]) == 2
        assert result["corrected_code"] == "corrected code here"

    def test_parse_malformed_json(self):
        validator = RuleValidator()
        response = "This is not JSON but says valid: true"

        result = validator._parse_response(response)
        assert result["valid"] is False
        assert "Failed to parse LLM response" in result["errors"][0]


class TestRuleValidatorWithMockedLLM:
    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_returns_valid_on_ok_response(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        validator = RuleValidator()
        result = validator.validate(generated_rule, codebook_entry, [1, 2, 3])

        assert result.is_valid is True
        assert result.escalated is False
        assert result.attempts == 1

    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_retries_on_error_then_succeeds(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        mock_call_llm.side_effect = [
            json.dumps({
                "valid": False,
                "errors": ["Missing value 3"],
                "corrected_code": "corrected code",
            }),
            json.dumps({
                "valid": True,
                "errors": [],
                "corrected_code": None,
            }),
        ]

        validator = RuleValidator(max_attempts=2)
        result = validator.validate(generated_rule, codebook_entry, [1, 2, 3])

        assert result.is_valid is True
        assert result.attempts == 2
        assert result.corrected_code == "corrected code"

    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_escalates_after_max_attempts(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": False,
            "errors": ["Persistent error"],
            "corrected_code": None,
        })

        validator = RuleValidator(max_attempts=2)
        result = validator.validate(generated_rule, codebook_entry, [1, 2, 3])

        assert result.is_valid is False
        assert result.escalated is True
        assert result.attempts == 2
        assert len(result.errors) == 2

    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_uses_corrected_code_on_retry(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        corrected_code = "df['satisfaction'] = df['Q5'].map({1: 'OK', 2: 'OK'})"

        mock_call_llm.side_effect = [
            json.dumps({
                "valid": False,
                "errors": ["Wrong labels"],
                "corrected_code": corrected_code,
            }),
            json.dumps({
                "valid": True,
                "errors": [],
                "corrected_code": None,
            }),
        ]

        validator = RuleValidator(max_attempts=2)
        result = validator.validate(generated_rule, codebook_entry, [1, 2])

        assert result.is_valid is True
        assert mock_call_llm.call_count == 2


class TestConvenienceFunction:
    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_rule_function(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        result = validate_rule(generated_rule, codebook_entry, [1, 2, 3])

        assert isinstance(result, ValidationResult)
        assert result.is_valid is True


class TestEdgeCases:
    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_without_codebook(
        self, mock_call_llm, generated_rule: GeneratedRule
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        validator = RuleValidator()
        result = validator.validate(generated_rule, None, [1, 2, 3])

        assert result.is_valid is True

    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_without_sample_data(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry: VariableSchema
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        validator = RuleValidator()
        result = validator.validate(generated_rule, codebook_entry, None)

        assert result.is_valid is True

    @patch("surveys.pattern_engine.rule_validator.RuleValidator._call_llm")
    def test_validate_with_dict_codebook(
        self, mock_call_llm, generated_rule: GeneratedRule, codebook_entry_dict: dict
    ):
        mock_call_llm.return_value = json.dumps({
            "valid": True,
            "errors": [],
            "corrected_code": None,
        })

        validator = RuleValidator()
        result = validator.validate(generated_rule, codebook_entry_dict, [1, 2, 3])

        assert result.is_valid is True
