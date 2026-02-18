"""Tests for tier2_batch.py."""

import json
import pytest
from unittest.mock import MagicMock, patch

from surveys.codebook_parser.schemas import VariableSchema, ValueLabel
from surveys.llm_processors import Batch
from surveys.llm_processors.tier2_batch import (
    BatchProcessingResult,
    Tier2BatchProcessor,
    VariableCode,
    process_tier2_batch,
    SYSTEM_PROMPT,
)
from surveys.pattern_engine.patterns.base_pattern import ClassificationResult, MissingCodeInfo


@pytest.fixture
def tier_2_var():
    var = VariableSchema(
        var_name="Q45",
        var_label="Thermomètre - CAQ",
        var_type="numeric",
        scale_type="thermometer",
        range_min=0,
        range_max=100,
        value_labels=[
            ValueLabel(value=998, label="NSP", is_missing=True),
        ],
    )
    result = ClassificationResult(
        tier=2,
        pattern_id="thermometer_0_10",
        confidence=0.6,
        reason="Semi-standard pattern",
        missing_codes=MissingCodeInfo(),
        effective_n_unique=15,
    )
    return var, result


@pytest.fixture
def tier_2_batch(tier_2_var):
    var, result = tier_2_var
    return Batch(
        tier=2,
        batch_index=0,
        variables=[("op_thermometer_caq", var, result)],
    )


class TestVariableCode:
    def test_init(self):
        code = VariableCode(
            clean_var_name="ses_province",
            original_var_name="Q2",
            code="df_clean['ses_province'] = df['Q2'].map({...})",
            var_type="categorical",
            value_labels={"quebec": "Québec"},
        )
        assert code.clean_var_name == "ses_province"
        assert code.error is None

    def test_with_error(self):
        code = VariableCode(
            clean_var_name="test",
            original_var_name="Q1",
            code="",
            var_type="unknown",
            value_labels={},
            error="Parse error",
        )
        assert code.error == "Parse error"


class TestBatchProcessingResult:
    def test_init(self):
        result = BatchProcessingResult(
            batch_index=0,
            model_used="opencode/glm-5-free",
        )
        assert result.batch_index == 0
        assert result.variables == {}
        assert result.failed_vars == []

    def test_success_count(self):
        result = BatchProcessingResult(
            batch_index=0,
            model_used="test",
            variables={
                "v1": VariableCode("v1", "Q1", "code", "cat", {}),
                "v2": VariableCode("v2", "Q2", "code", "cat", {}, error="failed"),
            },
        )
        assert result.success_count == 1

    def test_failure_count(self):
        result = BatchProcessingResult(
            batch_index=0,
            model_used="test",
            failed_vars=["v3", "v4"],
        )
        assert result.failure_count == 2


class TestTier2BatchProcessor:
    def test_init_defaults(self):
        processor = Tier2BatchProcessor()
        assert processor.model == "opencode/glm-5-free"
        assert processor.temperature == 0.1
        assert processor.max_retries == 2

    def test_init_custom(self, tmp_path):
        processor = Tier2BatchProcessor(
            model="custom-model",
            cache_dir=tmp_path,
            temperature=0.2,
            max_retries=3,
        )
        assert processor.model == "custom-model"
        assert processor.temperature == 0.2
        assert processor.max_retries == 3

    def test_build_variables_json(self, tier_2_batch):
        processor = Tier2BatchProcessor()
        data = processor._build_variables_json(tier_2_batch.variables)

        assert len(data) == 1
        assert data[0]["clean_var_name"] == "op_thermometer_caq"
        assert data[0]["original_var_name"] == "Q45"
        assert data[0]["var_type"] == "numeric"
        assert data[0]["classification"]["tier"] == 2

    def test_build_user_prompt(self, tier_2_batch):
        processor = Tier2BatchProcessor()
        variables_data = processor._build_variables_json(tier_2_batch.variables)
        prompt = processor._build_user_prompt(variables_data)

        assert "1 variables à nettoyer" in prompt
        assert "op_thermometer_caq" in prompt
        assert "Q45" in prompt

    def test_parse_response_valid(self):
        processor = Tier2BatchProcessor()
        response = json.dumps({
            "variables": {
                "ses_province": {
                    "original_variable": "Q2",
                    "code": "df_clean['ses_province'] = df['Q2'].map({1: 'quebec'})",
                    "type": "categorical",
                    "value_labels": {"quebec": "Québec"}
                }
            }
        })

        result = processor._parse_response(response, 0)

        assert "ses_province" in result.variables
        assert result.variables["ses_province"].code == "df_clean['ses_province'] = df['Q2'].map({1: 'quebec'})"
        assert result.success_count == 1
        assert result.failure_count == 0

    def test_parse_response_invalid_json(self):
        processor = Tier2BatchProcessor()
        result = processor._parse_response("not valid json", 0)

        assert result.failure_count == 1
        assert "batch_parse_error" in result.failed_vars

    def test_process_batch_wrong_tier(self):
        processor = Tier2BatchProcessor()
        batch = Batch(tier=1, batch_index=0, variables=[])

        with pytest.raises(ValueError, match="Expected tier=2"):
            processor.process_batch(batch)

    @patch("surveys.llm_processors.tier2_batch.Tier2BatchProcessor._call_llm")
    def test_process_batch_with_mock(self, mock_call_llm, tier_2_batch):
        mock_call_llm.return_value = json.dumps({
            "variables": {
                "op_thermometer_caq": {
                    "original_variable": "Q45",
                    "code": "df_clean['op_thermometer_caq'] = df['Q45'] / 100.0",
                    "type": "numeric",
                    "value_labels": {}
                }
            }
        })

        processor = Tier2BatchProcessor()
        result = processor.process_batch(tier_2_batch)

        assert result.success_count == 1
        assert "op_thermometer_caq" in result.variables
        mock_call_llm.assert_called_once()


class TestProcessTier2Batch:
    def test_convenience_function(self, tier_2_batch):
        with patch.object(Tier2BatchProcessor, "process_batch") as mock_process:
            mock_process.return_value = BatchProcessingResult(
                batch_index=0,
                model_used="test",
            )

            result = process_tier2_batch(tier_2_batch)

            assert result.batch_index == 0
            mock_process.assert_called_once()


class TestSystemPrompt:
    def test_system_prompt_exists(self):
        assert len(SYSTEM_PROMPT) > 100
        assert "nettoyage" in SYSTEM_PROMPT.lower()
        assert ".map(" in SYSTEM_PROMPT
        assert "np.nan" in SYSTEM_PROMPT
