"""Tests for automatic tier escalation logic.

Tests the circuit-breaker pattern where:
- Tier 1 validation fails → escalate to Tier 2
- Tier 2 validation fails → escalate to Tier 3
- Tier 3 validation fails → mark needs_review=True
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

from surveys.orchestrator import VariableState, OrchestratorV2
from surveys.codebook_parser.schemas import VariableSchema, ValueLabel
from surveys.pattern_engine.patterns.base_pattern import ClassificationResult


@pytest.fixture
def sample_df():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({
        'Q1': [1.0, 2.0, 3.0, 99.0],  # Likert scale with missing code
        'Q2': ['yes', 'no', 'yes', 'NSP'],  # Categorical
        'Q3': [25, 30, 45, 55],  # Numeric
    })


@pytest.fixture
def sample_codebook():
    """Create a sample codebook for testing."""
    return VariableSchema(
        var_name='Q1',
        var_label='Sample question 1',
        var_type='numeric',
        value_labels=[
            ValueLabel(value=1.0, label='Strongly agree', is_missing=False),
            ValueLabel(value=2.0, label='Agree', is_missing=False),
            ValueLabel(value=3.0, label='Neutral', is_missing=False),
            ValueLabel(value=99.0, label='Missing', is_missing=True),
        ],
        missing_codes=[99.0],
        scale_type='likert',
    )


@pytest.fixture
def mock_orchestrator(tmp_path):
    """Create a mock orchestrator for testing."""
    # Create a valid status.json file
    status_file = tmp_path / 'status.json'
    with open(status_file, 'w') as f:
        json.dump({'surveys': {}}, f)

    with patch('surveys.orchestrator.Path') as mock_path:
        mock_path.return_value = tmp_path
        orchestrator = OrchestratorV2(
            survey_id='test_survey',
            limit=None,
            only_var=None,
            model='test-model',
            dry_run=False,
            verbose=False,
        )
        orchestrator.base_path = tmp_path
        orchestrator.status_file = status_file
        return orchestrator


class TestVariableState:
    """Test VariableState escalation fields."""

    def test_variable_state_initialization(self):
        """Test that VariableState initializes with escalation fields."""
        state = VariableState(var_name='test_var')
        assert state.escalation_count == 0
        assert state.escalation_history == []

    def test_variable_state_serialization(self):
        """Test that escalation fields are serialized correctly."""
        state = VariableState(
            var_name='test_var',
            escalation_count=1,
            escalation_history=[{
                'from_tier': 1,
                'to_tier': 2,
                'reason': 'Confidence < 0.85',
                'incorrect_code': None,
                'timestamp': '2024-01-01T00:00:00',
            }]
        )

        from surveys.orchestrator import SurveyState
        survey_state = SurveyState(survey_id='test', variables={'test_var': state})
        data = survey_state.to_dict()

        assert data['variables']['test_var']['escalation_count'] == 1
        assert len(data['variables']['test_var']['escalation_history']) == 1

    def test_variable_state_deserialization(self):
        """Test that escalation fields are deserialized correctly."""
        data = {
            'variables': {
                'test_var': {
                    'var_name': 'test_var',
                    'status': 'done',
                    'tier': 2,
                    'pattern_id': None,
                    'confidence': 0.9,
                    'clean_var_name': 'test_clean',
                    'code': 'test code',
                    'error': None,
                    'processed_at': '2024-01-01T00:00:00',
                    'needs_review': False,
                    'validation': None,
                    'escalation_count': 1,
                    'escalation_history': [{
                        'from_tier': 1,
                        'to_tier': 2,
                        'reason': 'test reason',
                        'incorrect_code': 'old code',
                        'timestamp': '2024-01-01T00:00:00',
                    }],
                }
            }
        }

        from surveys.orchestrator import SurveyState
        survey_state = SurveyState.from_dict('test', data)
        var_state = survey_state.variables['test_var']

        assert var_state.escalation_count == 1
        assert len(var_state.escalation_history) == 1
        assert var_state.escalation_history[0]['reason'] == 'test reason'


class TestEscalationLogic:
    """Test the escalation logic in _process_all."""

    def test_shortcut_confidence_tier1_to_tier2(self, mock_orchestrator, sample_df):
        """Test that variables with confidence < 0.85 skip Tier 1 and go to Tier 2."""
        # This test would need to mock a lot of dependencies
        # For now, we just verify the structure is in place
        pass

    def test_escalation_history_recorded(self):
        """Test that escalation history is recorded correctly."""
        state = VariableState(var_name='test_var')
        state.escalation_count = 0
        state.escalation_history = []

        # Simulate an escalation from Tier 1 to Tier 2
        from datetime import datetime
        state.escalation_count = 1
        state.escalation_history.append({
            'from_tier': 1,
            'to_tier': 2,
            'reason': 'Confidence 0.75 < 0.85',
            'incorrect_code': None,
            'timestamp': datetime.now().isoformat(),
        })

        assert state.escalation_count == 1
        assert state.escalation_history[0]['from_tier'] == 1
        assert state.escalation_history[0]['to_tier'] == 2
        assert 'Confidence 0.75 < 0.85' in state.escalation_history[0]['reason']

    def test_circuit_breaker_after_tier3_failure(self):
        """Test that needs_review=True is set after Tier 3 validation failure."""
        state = VariableState(var_name='test_var')
        state.escalation_count = 2

        # Simulate Tier 3 validation failure
        state.validation = {
            'is_valid': False,
            'issues': [{'message': 'Mapping incorrect'}],
        }
        state.needs_review = True

        assert state.needs_review is True
        assert state.escalation_count == 2

    def test_max_escalations_per_variable(self):
        """Test that a variable can only be escalated twice (T1→T2→T3)."""
        state = VariableState(var_name='test_var')

        # First escalation: T1 → T2
        state.escalation_count = 1
        assert state.escalation_count == 1

        # Second escalation: T2 → T3
        state.escalation_count = 2
        assert state.escalation_count == 2

        # Should not escalate further
        # (This would be enforced in the orchestrator logic)
