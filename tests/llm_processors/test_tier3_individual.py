"""Tests for Tier 3 individual processor."""

import pytest
from unittest.mock import patch, MagicMock

from surveys.llm_processors.tier3_individual import (
    Tier3Result,
    parse_llm_response,
    build_user_prompt,
    process_tier3_variable,
)
from surveys.pattern_engine.patterns.base_pattern import (
    ClassificationResult,
    MissingCodeInfo,
)
from surveys.codebook_parser.schemas.variable_schema import VariableSchema, ValueLabel


class TestParseLLMResponse:
    """Test LLM response parsing."""

    def test_parse_valid_json(self):
        response = '''
        {
            "python_code": "df['clean_var'] = df['raw_var'].map({1: 'Yes', 2: 'No'})",
            "explanation": "Binary mapping",
            "confidence": 0.9,
            "needs_review": false
        }
        '''
        result = parse_llm_response(response, "test_var")
        assert result.var_name == "test_var"
        assert "clean_var" in result.python_code
        assert result.confidence == 0.9
        assert not result.needs_review

    def test_parse_json_with_text_before(self):
        response = '''
        Here's the transformation:
        ```json
        {
            "python_code": "df['x'] = df['y']",
            "explanation": "Copy",
            "confidence": 0.8,
            "needs_review": false
        }
        ```
        '''
        result = parse_llm_response(response, "var1")
        assert result.python_code == "df['x'] = df['y']"

    def test_parse_missing_json(self):
        result = parse_llm_response("No JSON here", "test_var")
        assert result.error == "No JSON found in response"
        assert result.needs_review
        assert result.confidence == 0.0

    def test_parse_invalid_json(self):
        result = parse_llm_response("{invalid json}", "test_var")
        assert "JSON parse error" in result.explanation
        assert result.needs_review

    def test_parse_missing_code_flags_review(self):
        response = '{"explanation": "No code", "confidence": 0.5}'
        result = parse_llm_response(response, "var")
        assert result.needs_review
        assert "No code generated" in result.python_code

    def test_low_confidence_flags_review(self):
        response = '{"python_code": "df[\\"x\\"] = 1", "explanation": "", "confidence": 0.3}'
        result = parse_llm_response(response, "var")
        assert result.needs_review


class TestBuildUserPrompt:
    """Test prompt building."""

    def test_basic_prompt(self):
        classification = ClassificationResult(
            tier=3,
            pattern_id=None,
            confidence=0.0,
            reason="Complex coding scheme",
        )
        prompt = build_user_prompt(
            var_name="Q1",
            var=None,
            classification=classification,
            sample_values=[1, 2, 3],
            clean_var_name="clean_q1",
        )
        assert "Variable: Q1" in prompt
        assert "clean_q1" in prompt
        assert "Complex coding scheme" in prompt
        assert "[1, 2, 3]" in prompt

    def test_prompt_with_codebook_info(self):
        var = VariableSchema(
            var_name="Q2",
            var_label="Satisfaction level",
            var_type="ordinal",
            value_labels=[
                ValueLabel(value=1, label="Very unsatisfied"),
                ValueLabel(value=5, label="Very satisfied"),
                ValueLabel(value=99, label="NR", is_missing=True),
            ],
            missing_codes=[99],
        )
        classification = ClassificationResult(
            tier=3,
            pattern_id=None,
            confidence=0.0,
            reason="Non-standard scale",
        )
        prompt = build_user_prompt(
            var_name="Q2",
            var=var,
            classification=classification,
            sample_values=[1, 2, 3, 4, 5, 99],
            clean_var_name="sat_level",
        )
        assert "Satisfaction level" in prompt
        assert "ordinal" in prompt
        assert "Very unsatisfied" in prompt
        assert "[MISSING]" in prompt
        assert "99" in prompt


class TestProcessTier3Variable:
    """Test main processing function."""

    @patch("surveys.llm_processors.tier3_individual.litellm.completion")
    def test_successful_processing(self, mock_completion):
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='{"python_code": "df[\\"clean\\"] = df[\\"raw\\"]", "explanation": "Copy", "confidence": 0.95, "needs_review": false}'))
        ]
        mock_completion.return_value = mock_response

        classification = ClassificationResult(
            tier=3,
            pattern_id=None,
            confidence=0.0,
            reason="Test",
        )

        result = process_tier3_variable(
            var_name="test_var",
            var=None,
            classification=classification,
            sample_values=[1, 2, 3],
        )

        assert result.var_name == "test_var"
        assert result.confidence == 0.95
        assert not result.needs_review
        mock_completion.assert_called_once()

    @patch("surveys.llm_processors.tier3_individual.litellm.completion")
    def test_llm_error_handling(self, mock_completion):
        mock_completion.side_effect = Exception("API error")

        classification = ClassificationResult(
            tier=3,
            pattern_id=None,
            confidence=0.0,
            reason="Test",
        )

        result = process_tier3_variable(
            var_name="fail_var",
            var=None,
            classification=classification,
            sample_values=[1],
        )

        assert result.error == "API error"
        assert result.needs_review
        assert "ERROR" in result.python_code


class TestTier3Result:
    """Test Tier3Result dataclass."""

    def test_default_values(self):
        result = Tier3Result(
            var_name="test",
            python_code="df['x'] = 1",
            explanation="Test",
            confidence=0.8,
            needs_review=False,
        )
        assert result.error is None

    def test_with_error(self):
        result = Tier3Result(
            var_name="test",
            python_code="# Error",
            explanation="Failed",
            confidence=0.0,
            needs_review=True,
            error="Something went wrong",
        )
        assert result.error == "Something went wrong"
