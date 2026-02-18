"""Integration tests for CleanValidator integration into the orchestrator (survey-cleaner-26m.3).

Validates:
- Static validation runs post-assembly and errors appear in status.json
- A clean.py with invalid syntax is detected automatically
- Per-variable dynamic validation stores results in var_state.validation
- Variables with errors/warnings are flagged needs_review=True
- GLM-5 semantic check is called for Tier 1 variables that fail validation
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from surveys.codebook_parser.schemas import ValueLabel, VariableSchema
from surveys.llm_processors import Batch, VariableCode, create_batches
from surveys.orchestrator import OrchestratorV2, SurveyState, VariableState
from surveys.pattern_engine.patterns.base_pattern import ClassificationResult, MissingCodeInfo
from surveys.validation import CleanValidator, ValidationResult


# ---------------------------------------------------------------------------
# Helpers (shared with test_orchestrator_two_pass)
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
        {name: rng.choice([1, 2], size=n_rows) for name in var_names},
    )


def make_vc(var_name: str) -> VariableCode:
    return VariableCode(
        clean_var_name=f"op_{var_name}",
        original_var_name=var_name,
        code=f"df_clean['op_{var_name}'] = df['{var_name}'].map({{1: 'Oui', 2: 'Non'}})",
        var_type="ordinal",
        value_labels={},
    )


def _make_orchestrator(tmp_path: Path) -> OrchestratorV2:
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
    orch.survey_path.mkdir(parents=True, exist_ok=True)
    orch.state = {"surveys": {}}
    orch.codebook = None
    from surveys.pattern_engine import get_all_patterns
    orch.patterns = get_all_patterns()
    orch._pattern_map = {p.pattern_id: p for p in orch.patterns}
    return orch


# ---------------------------------------------------------------------------
# Tests: per-variable validation (Step 2)
# ---------------------------------------------------------------------------


class TestPerVariableValidation:
    """_validate_variable_code stores validation results in var_state."""

    def test_valid_code_stores_validation(self, tmp_path):
        """A valid code snippet should store is_valid=True in var_state.validation."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1")

        var_state = VariableState(
            var_name="q1",
            clean_var_name="op_q1",
            code="df_clean['op_q1'] = df['q1'].map({1: 'Oui', 2: 'Non'})",
            status="done",
        )

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=1)

        assert var_state.validation is not None
        assert "is_valid" in var_state.validation

    def test_execution_error_sets_needs_review(self, tmp_path):
        """Code that fails at execution should set needs_review=True."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1")

        var_state = VariableState(
            var_name="q1",
            clean_var_name="op_q1",
            code="raise ValueError('bad code')",
            status="done",
        )

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=1)

        assert var_state.needs_review is True
        assert var_state.validation is not None
        assert "error" in var_state.validation

    def test_no_code_skips_validation(self, tmp_path):
        """Variables with no code should not have validation set."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1")

        var_state = VariableState(var_name="q1", status="error")

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=1)

        assert var_state.validation is None
        assert var_state.needs_review is False


# ---------------------------------------------------------------------------
# Tests: GLM-5 semantic check (Step 3)
# ---------------------------------------------------------------------------


class TestGlmSemanticCheck:
    """Tier 1 variables that fail validation trigger a GLM-5 semantic check."""

    def test_glm_called_when_tier1_validation_fails(self, tmp_path):
        """If a Tier 1 variable fails dynamic validation, _llm_semantic_check is called."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1", var_type="numeric")  # numeric but we'll give string output

        # Code that produces a type mismatch (numeric expected, string produced)
        var_state = VariableState(
            var_name="q1",
            clean_var_name="q1",
            code="df_clean['q1'] = df['q1'].astype(str)",  # string output on numeric schema
            status="done",
        )

        semantic_called = []

        original_llm = orch._llm_semantic_check

        def mock_semantic(var_name, var_schema, code, df):
            semantic_called.append(var_name)
            return {"passed": True, "issues": []}

        orch._llm_semantic_check = mock_semantic

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=1)

        assert "q1" in semantic_called, (
            "GLM-5 semantic check should be called for Tier 1 validation failure"
        )

    def test_glm_not_called_for_tier2(self, tmp_path):
        """Tier 2 validation failures should NOT trigger GLM-5 semantic check."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1", var_type="numeric")

        var_state = VariableState(
            var_name="q1",
            clean_var_name="q1",
            code="df_clean['q1'] = df['q1'].astype(str)",
            status="done",
        )

        semantic_called = []

        def mock_semantic(var_name, var_schema, code, df):
            semantic_called.append(var_name)
            return {"passed": True, "issues": []}

        orch._llm_semantic_check = mock_semantic

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=2)

        assert semantic_called == [], "GLM-5 should NOT be called for Tier 2 failures"

    def test_glm_flagged_sets_needs_review(self, tmp_path):
        """If GLM-5 returns passed=False, variable is flagged needs_review=True."""
        orch = _make_orchestrator(tmp_path)
        df = make_df(["q1"])
        var_schema = make_var_schema("q1", var_type="numeric")

        var_state = VariableState(
            var_name="q1",
            clean_var_name="q1",
            code="df_clean['q1'] = df['q1'].astype(str)",
            status="done",
        )

        def mock_semantic(var_name, var_schema, code, df):
            return {"passed": False, "issues": ["Inverted mapping detected"]}

        orch._llm_semantic_check = mock_semantic

        orch._validate_variable_code("q1", var_schema, var_state, df, tier=1)

        assert var_state.needs_review is True
        assert var_state.validation is not None
        semantic = var_state.validation.get("semantic_check", {})
        assert semantic.get("passed") is False


# ---------------------------------------------------------------------------
# Tests: post-assembly static validation (Step 1)
# ---------------------------------------------------------------------------


class TestStaticValidationIntegration:
    """Static validation runs after assembly; results appear in status.json."""

    def test_valid_clean_py_passes_static_validation(self, tmp_path):
        """A valid assembled clean.py should not generate errors in status.json."""
        orch = _make_orchestrator(tmp_path)

        var_names = ["q1"]
        df = make_df(var_names)

        survey_state = SurveyState(survey_id="test_survey", status="initialized")
        survey_state.variables["q1"] = VariableState(
            var_name="q1",
            clean_var_name="op_q1",
            code="df_clean['op_q1'] = df['q1'].map({1: 'Oui', 2: 'Non'})",
            status="done",
            tier=1,
            confidence=0.9,
        )

        clean_py = orch._assemble_clean_py(survey_state)
        assert "SyntaxError" not in clean_py

        validator = CleanValidator()
        result = validator.validate_code(clean_py)
        assert result.syntax_valid
        assert not result.has_errors

    def test_invalid_syntax_detected(self, tmp_path):
        """A clean.py with Python syntax error should be detected by validate_code."""
        validator = CleanValidator()
        bad_code = "def clean(df:\n    return df"  # missing closing paren
        result = validator.validate_code(bad_code)
        assert not result.syntax_valid
        assert result.has_errors
        assert any(e.code == "SYNTAX_ERROR" for e in result.errors)

    def test_static_validation_stored_in_status_json(self, tmp_path):
        """Static validation result is stored under surveys.<id>.validation.static."""
        orch = _make_orchestrator(tmp_path)

        survey_state = SurveyState(survey_id="test_survey", status="initialized")
        survey_state.variables["q1"] = VariableState(
            var_name="q1",
            clean_var_name="op_q1",
            code="df_clean['op_q1'] = df['q1'].map({1: 'Oui', 2: 'Non'})",
            status="done",
            tier=1,
            confidence=0.9,
        )

        clean_py = orch._assemble_clean_py(survey_state)
        validator = CleanValidator()
        static_result = validator.validate_code(clean_py)

        # Simulate what run() does: _update_survey_state then persist validation
        orch._update_survey_state(survey_state)
        orch.state.setdefault("surveys", {})[orch.survey_id].setdefault(
            "validation", {}
        )["static"] = static_result.to_dict()
        orch._save_state()

        import json
        with open(orch.status_file) as f:
            saved = json.load(f)

        assert "validation" in saved["surveys"]["test_survey"]
        assert "static" in saved["surveys"]["test_survey"]["validation"]
        static = saved["surveys"]["test_survey"]["validation"]["static"]
        assert "is_valid" in static
        assert "summary" in static

    def test_duplicate_variable_flags_needs_review(self, tmp_path):
        """Variables flagged by DUPLICATE_VARIABLE error should have needs_review=True."""
        orch = _make_orchestrator(tmp_path)

        # Build a clean.py with a duplicate variable assignment
        survey_state = SurveyState(survey_id="test_survey", status="initialized")
        survey_state.variables["q1"] = VariableState(
            var_name="q1",
            clean_var_name="op_q1",
            code="df_clean['op_q1'] = df['q1'].map({1: 'Oui', 2: 'Non'})",
            status="done",
            tier=1,
            confidence=0.9,
        )

        clean_py = orch._assemble_clean_py(survey_state)
        # Inject a duplicate
        duplicate_code = clean_py + "\n    df_clean['op_q1'] = df['q1']  # duplicate\n"

        validator = CleanValidator()
        static_result = validator.validate_code(duplicate_code)

        # Simulate orchestrator flagging the variable (using clean_var_name → raw reverse lookup)
        clean_to_raw = {
            vs.clean_var_name: vn
            for vn, vs in survey_state.variables.items()
            if vs.clean_var_name
        }
        for err in static_result.errors:
            if err.variable_name:
                raw_name = clean_to_raw.get(err.variable_name, err.variable_name)
                if raw_name in survey_state.variables:
                    survey_state.variables[raw_name].needs_review = True

        assert survey_state.variables["q1"].needs_review is True


# ---------------------------------------------------------------------------
# Tests: validation data stored per-variable in status.json (Step 2)
# ---------------------------------------------------------------------------


class TestVariableValidationInState:
    """Per-variable validation results are persisted in status.json."""

    def test_validation_field_serialized_in_to_dict(self):
        """VariableState.to_dict() includes needs_review and validation."""
        state = SurveyState(survey_id="test")
        state.variables["q1"] = VariableState(
            var_name="q1",
            status="done",
            needs_review=True,
            validation={"is_valid": False, "issues": [{"code": "TYPE_MISMATCH"}]},
        )

        d = state.to_dict()
        assert d["variables"]["q1"]["needs_review"] is True
        assert d["variables"]["q1"]["validation"] is not None
        assert d["variables"]["q1"]["validation"]["is_valid"] is False

    def test_validation_field_loaded_from_dict(self):
        """SurveyState.from_dict() restores needs_review and validation."""
        data = {
            "status": "completed",
            "variables": {
                "q1": {
                    "status": "done",
                    "tier": 1,
                    "confidence": 0.9,
                    "needs_review": True,
                    "validation": {"is_valid": False, "issues": []},
                }
            },
        }
        state = SurveyState.from_dict("test", data)
        assert state.variables["q1"].needs_review is True
        assert state.variables["q1"].validation == {"is_valid": False, "issues": []}

    def test_validation_field_defaults_false_when_missing(self):
        """Old status.json without needs_review/validation loads with defaults."""
        data = {
            "status": "completed",
            "variables": {
                "q1": {"status": "done", "tier": 1, "confidence": 0.9},
            },
        }
        state = SurveyState.from_dict("test", data)
        assert state.variables["q1"].needs_review is False
        assert state.variables["q1"].validation is None
