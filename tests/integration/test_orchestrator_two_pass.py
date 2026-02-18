"""Tests for orchestrator two-pass batching refactor (survey-cleaner-xiy.3).

Validates that:
- Tier 2 variables are grouped into batches, not processed one-by-one
- status.json is updated after each batch (not each variable)
- The pipeline is resumable after interruption
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from surveys.codebook_parser.schemas import ValueLabel, VariableSchema
from surveys.llm_processors import Batch, VariableCode, create_batches
from surveys.orchestrator import OrchestratorV2, SurveyState, VariableState
from surveys.pattern_engine.patterns.base_pattern import ClassificationResult, MissingCodeInfo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_classification(tier: int, pattern_id: str = "likert_5_agree", confidence: float = 0.9) -> ClassificationResult:
    return ClassificationResult(
        tier=tier,
        pattern_id=pattern_id,
        confidence=confidence,
        reason="test",
        missing_codes=MissingCodeInfo(),
        effective_n_unique=4,
    )


def make_var_schema(name: str, var_type: str = "ordinal") -> VariableSchema:
    return VariableSchema(
        var_name=name,
        var_label=f"Label for {name}",
        var_type=var_type,
        value_labels=[
            ValueLabel(value=1, label="Oui"),
            ValueLabel(value=2, label="Non"),
        ],
    )


def make_df(var_names: list[str], n_rows: int = 10) -> pd.DataFrame:
    import numpy as np
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {name: rng.choice([1, 2, 3, 4, 5], size=n_rows) for name in var_names},
    )


def make_vc(var_name: str) -> VariableCode:
    """Create a minimal VariableCode for testing."""
    return VariableCode(
        clean_var_name=f"op_{var_name}",
        original_var_name=var_name,
        code=f"df_clean['op_{var_name}'] = df['{var_name}']",
        var_type="ordinal",
        value_labels={},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestTwoPassBatching:
    """Tests for the two-pass orchestration logic."""

    def _make_orchestrator(self, tmp_path: Path) -> OrchestratorV2:
        """Create a minimal orchestrator pointing to tmp_path."""
        orch = OrchestratorV2.__new__(OrchestratorV2)
        orch.survey_id = "test_survey"
        orch.limit = None
        orch.only_var = None
        orch.dry_run = False
        orch.verbose = False
        orch.model = "mock-model"
        orch.base_path = tmp_path / "surveys"
        orch.survey_path = orch.base_path / "test_survey"
        orch.shared_folder = tmp_path / "shared" / "test_survey"
        orch.status_file = orch.base_path / "status.json"
        orch.base_path.mkdir(parents=True, exist_ok=True)
        orch.state = {"surveys": {}}
        orch.codebook = None
        from surveys.pattern_engine import get_all_patterns
        orch.patterns = get_all_patterns()
        orch._pattern_map = {p.pattern_id: p for p in orch.patterns}
        return orch

    def test_tier2_grouped_into_batches(self, tmp_path):
        """Tier 2 variables must be sent in batches, not one-by-one."""
        orch = self._make_orchestrator(tmp_path)

        # 15 Tier 2 variables → should be 1 batch of 15 (< MAX_BATCH_SIZE=20)
        var_names = [f"q{i}" for i in range(15)]
        classified = {
            name: (make_var_schema(name), make_classification(tier=2))
            for name in var_names
        }
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        batch_call_count = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            batch_call_count.append(batch.size)
            return {f"op_{v[0]}": make_vc(v[0]) for v in batch.variables}

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._process_tier3_variable = MagicMock(return_value="# no tier3")
        orch._update_survey_state = MagicMock()

        orch._process_all(classified, survey_state, df, var_names)

        # Should be 1 batch call for 15 vars, not 15 individual calls
        assert len(batch_call_count) == 1, (
            f"Expected 1 batch call, got {len(batch_call_count)} calls: {batch_call_count}"
        )
        assert batch_call_count[0] == 15

    def test_tier2_split_at_max_batch_size(self, tmp_path):
        """25 Tier 2 vars should be split into 2 batches (20 + 5)."""
        orch = self._make_orchestrator(tmp_path)

        var_names = [f"q{i}" for i in range(25)]
        classified = {
            name: (make_var_schema(name), make_classification(tier=2))
            for name in var_names
        }
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        batch_sizes = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            batch_sizes.append(batch.size)
            return {f"op_{v[0]}": make_vc(v[0]) for v in batch.variables}

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._process_tier3_variable = MagicMock(return_value="# no tier3")
        orch._update_survey_state = MagicMock()

        orch._process_all(classified, survey_state, df, var_names)

        assert len(batch_sizes) == 2, f"Expected 2 batches, got {len(batch_sizes)}: {batch_sizes}"
        assert sorted(batch_sizes) == [5, 20]

    def test_state_saved_after_each_batch(self, tmp_path):
        """status.json must be saved after each Tier 2 batch."""
        orch = self._make_orchestrator(tmp_path)

        # 21 vars → 2 batches (20 + 1)
        var_names = [f"q{i}" for i in range(21)]
        classified = {
            name: (make_var_schema(name), make_classification(tier=2))
            for name in var_names
        }
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        save_calls = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            return {f"op_{v[0]}": make_vc(v[0]) for v in batch.variables}

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._process_tier3_variable = MagicMock(return_value="# no tier3")
        orch._update_survey_state = lambda ss: save_calls.append(
            sum(1 for v in ss.variables.values() if v.status == "done")
        )

        orch._process_all(classified, survey_state, df, var_names)

        # Should have 2 saves (one per batch), with progressive done counts
        assert len(save_calls) == 2, f"Expected 2 saves, got {len(save_calls)}: {save_calls}"
        assert save_calls[0] == 20
        assert save_calls[1] == 21

    def test_tier1_processed_immediately(self, tmp_path):
        """Tier 1 variables are processed via pattern (no LLM call)."""
        orch = self._make_orchestrator(tmp_path)

        var_names = ["t1_a", "t1_b"]
        classified = {
            name: (make_var_schema(name), make_classification(tier=1))
            for name in var_names
        }
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        tier2_calls = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            tier2_calls.append(batch.size)
            return {}

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._process_tier3_variable = MagicMock(return_value="# no tier3")
        # Mock _process_tier1 to avoid real pattern matching complexity
        orch._process_tier1 = lambda var_name, var_schema, classification, df: f"df_clean['{var_name}'] = df['{var_name}']"
        orch._update_survey_state = MagicMock()

        orch._process_all(classified, survey_state, df, var_names)

        # No Tier 2 calls for Tier 1 variables
        assert tier2_calls == [], f"Tier 1 vars should not trigger Tier 2: {tier2_calls}"

    def test_mixed_tiers_correct_routing(self, tmp_path):
        """Mixed T1/T2/T3 vars are routed correctly."""
        orch = self._make_orchestrator(tmp_path)

        classified = {
            "t1_var": (make_var_schema("t1_var"), make_classification(tier=1)),
            "t2_a": (make_var_schema("t2_a"), make_classification(tier=2)),
            "t2_b": (make_var_schema("t2_b"), make_classification(tier=2)),
            "t3_var": (make_var_schema("t3_var"), make_classification(tier=3)),
        }
        var_names = list(classified.keys())
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        tier2_batch_vars: list[list[str]] = []
        tier3_processed: list[str] = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            tier2_batch_vars.append([v[0] for v in batch.variables])
            return {f"op_{v[0]}": make_vc(v[0]) for v in batch.variables}

        def mock_process_tier3(var_name, var_schema, classification, df):
            tier3_processed.append(var_name)
            return f"df_clean['{var_name}'] = df['{var_name}']"

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._process_tier3_variable = mock_process_tier3
        # Mock _process_tier1 to avoid real pattern matching
        orch._process_tier1 = lambda var_name, var_schema, classification, df: f"df_clean['{var_name}'] = df['{var_name}']"
        orch._update_survey_state = MagicMock()

        orch._process_all(classified, survey_state, df, var_names)

        # T2 vars are batched together
        assert len(tier2_batch_vars) == 1, f"Expected 1 T2 batch, got {tier2_batch_vars}"
        assert set(tier2_batch_vars[0]) == {"t2_a", "t2_b"}

        # T3 var processed individually
        assert tier3_processed == ["t3_var"]

    def test_dry_run_no_processing(self, tmp_path):
        """dry_run=True should classify but not process."""
        orch = self._make_orchestrator(tmp_path)
        orch.dry_run = True

        var_names = [f"q{i}" for i in range(5)]
        classified = {
            name: (make_var_schema(name), make_classification(tier=2))
            for name in var_names
        }
        df = make_df(var_names)
        survey_state = SurveyState(survey_id="test_survey")
        for name in var_names:
            survey_state.variables[name] = VariableState(var_name=name)

        tier2_calls = []

        def mock_process_tier2_batch(batch: Batch) -> dict[str, VariableCode]:
            tier2_calls.append(batch.size)
            return {}

        orch._process_tier2_batch = mock_process_tier2_batch
        orch._update_survey_state = MagicMock()
        orch._process_tier1 = MagicMock(return_value="code")

        orch._process_all(classified, survey_state, df, var_names)

        assert tier2_calls == [], "dry_run should not call _process_tier2_batch"
