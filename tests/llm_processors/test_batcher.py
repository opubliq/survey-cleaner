"""Tests for batcher.py."""

import pytest

from surveys.codebook_parser.schemas import VariableSchema, ValueLabel
from surveys.llm_processors import (
    Batch,
    BatchingResult,
    TIER_2_MAX_BATCH_SIZE,
    TIER_2_MIN_BATCH_SIZE,
    VariableGroup,
    create_batches,
    get_batch_stats,
)
from surveys.pattern_engine.patterns.base_pattern import ClassificationResult, MissingCodeInfo


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tier_1_var():
    """A Tier 1 variable (Likert 5)."""
    var = VariableSchema(
        var_name="Q12",
        var_label="Satisfaction envers le gouvernement",
        var_type="ordinal",
        scale_type="likert",
        value_labels=[
            ValueLabel(value=1, label="Très satisfait"),
            ValueLabel(value=2, label="Satisfait"),
            ValueLabel(value=3, label="Insatisfait"),
            ValueLabel(value=4, label="Très insatisfait"),
            ValueLabel(value=98, label="NSP", is_missing=True),
        ],
    )
    result = ClassificationResult(
        tier=1,
        pattern_id="likert_5_agree",
        confidence=0.95,
        reason="Pattern matched",
        missing_codes=MissingCodeInfo(),
        effective_n_unique=4,
    )
    return var, result


@pytest.fixture
def tier_2_var():
    """A Tier 2 variable (semi-standard)."""
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
def tier_3_var():
    """A Tier 3 variable (complex)."""
    var = VariableSchema(
        var_name="Q100",
        var_label="Commentaire libre",
        var_type="text",
    )
    result = ClassificationResult(
        tier=3,
        pattern_id=None,
        confidence=0.0,
        reason="Text data - requires LLM",
        missing_codes=MissingCodeInfo(),
        effective_n_unique=150,
    )
    return var, result


@pytest.fixture
def classified_vars(tier_1_var, tier_2_var, tier_3_var):
    """Create a set of classified variables."""
    vars_dict = {
        "tier_1_var": tier_1_var,
        "tier_2_var_1": tier_2_var,
        "tier_2_var_2": (
            VariableSchema(
                var_name="Q46",
                var_label="Thermomètre - PLQ",
                var_type="numeric",
                scale_type="thermometer",
                range_min=0,
                range_max=100,
            ),
            ClassificationResult(
                tier=2,
                pattern_id="thermometer_0_10",
                confidence=0.6,
                reason="Semi-standard pattern",
                missing_codes=MissingCodeInfo(),
                effective_n_unique=15,
            ),
        ),
        "tier_3_var": tier_3_var,
    }
    return vars_dict


# ---------------------------------------------------------------------------
# Test VariableGroup
# ---------------------------------------------------------------------------


def test_variable_group_creation():
    """Test creating a VariableGroup."""
    group = VariableGroup(
        tier=2,
        var_type="numeric",
        scale_type="thermometer",
        pattern_id="thermometer_0_10",
    )

    assert group.tier == 2
    assert group.var_type == "numeric"
    assert group.scale_type == "thermometer"
    assert group.pattern_id == "thermometer_0_10"
    assert group.size == 0


def test_variable_group_add_variable(tier_2_var):
    """Test adding a variable to a group."""
    group = VariableGroup(
        tier=2,
        var_type="numeric",
        scale_type="thermometer",
        pattern_id="thermometer_0_10",
    )

    var, result = tier_2_var
    group.add_variable("Q45", var, result)

    assert group.size == 1
    assert group.variables[0] == ("Q45", var, result)


def test_variable_group_can_add_more():
    """Test can_add_more for different tiers."""
    tier_2_group = VariableGroup(tier=2, var_type="numeric", scale_type="thermometer", pattern_id="thermometer_0_10")
    tier_3_group = VariableGroup(tier=3, var_type="text", scale_type=None, pattern_id=None)

    # Tier 2: can add more until max
    for _ in range(TIER_2_MAX_BATCH_SIZE):
        assert tier_2_group.can_add_more()
        tier_2_group.variables.append(("var", None, None))

    assert not tier_2_group.can_add_more()

    # Tier 3: always can add more
    assert tier_3_group.can_add_more()


# ---------------------------------------------------------------------------
# Test Batch
# ---------------------------------------------------------------------------


def test_batch_creation():
    """Test creating a Batch."""
    batch = Batch(tier=2, batch_index=0)

    assert batch.tier == 2
    assert batch.batch_index == 0
    assert batch.size == 0


def test_batch_is_full(tier_2_var):
    """Test is_full for different tiers."""
    tier_2_batch = Batch(tier=2, batch_index=0)
    tier_3_batch = Batch(tier=3, batch_index=0)

    # Tier 2: not full until max
    assert not tier_2_batch.is_full()

    for _ in range(TIER_2_MAX_BATCH_SIZE):
        tier_2_batch.variables.append(("var", None, None))

    assert tier_2_batch.is_full()

    # Tier 3: full after 1 variable
    assert not tier_3_batch.is_full()
    tier_3_batch.variables.append(("var", None, None))
    assert tier_3_batch.is_full()


# ---------------------------------------------------------------------------
# Test create_batches
# ---------------------------------------------------------------------------


def test_create_batches_empty():
    """Test create_batches with empty input."""
    result = create_batches({})

    assert isinstance(result, BatchingResult)
    assert len(result.tier_1_batches) == 0
    assert len(result.tier_2_batches) == 0
    assert len(result.tier_3_batches) == 0


def test_create_batches_single_tier(tier_1_var):
    """Test create_batches with only Tier 1 variables."""
    classified_vars = {"var1": tier_1_var, "var2": tier_1_var}

    result = create_batches(classified_vars)

    assert len(result.tier_1_batches) == 1
    assert len(result.tier_2_batches) == 0
    assert len(result.tier_3_batches) == 0

    assert result.tier_1_batches[0].size == 2


def test_create_batches_mixed_tiers(classified_vars):
    """Test create_batches with mixed tiers."""
    result = create_batches(classified_vars)

    assert len(result.tier_1_batches) == 1
    assert len(result.tier_2_batches) >= 1
    assert len(result.tier_3_batches) == 1

    assert result.tier_1_batches[0].size == 1
    assert result.tier_3_batches[0].size == 1


def test_create_batches_tier_2_batching(classified_vars):
    """Test that Tier 2 variables are batched by similarity."""
    result = create_batches(classified_vars)

    # Two Tier 2 vars with same type should be in same batch
    tier_2_batch = result.tier_2_batches[0]
    assert tier_2_batch.size == 2

    # Check they have the same characteristics
    var_names = [v[0] for v in tier_2_batch.variables]
    assert "tier_2_var_1" in var_names
    assert "tier_2_var_2" in var_names


def test_create_batches_tier_3_individual(tier_3_var):
    """Test that Tier 3 variables are batched individually."""
    classified_vars = {"var1": tier_3_var, "var2": tier_3_var}

    result = create_batches(classified_vars)

    assert len(result.tier_3_batches) == 2
    assert all(batch.size == 1 for batch in result.tier_3_batches)


# ---------------------------------------------------------------------------
# Test get_batch_stats
# ---------------------------------------------------------------------------


def test_get_batch_stats_empty():
    """Test get_batch_stats with empty result."""
    result = BatchingResult(
        tier_1_batches=[],
        tier_2_batches=[],
        tier_3_batches=[],
    )

    stats = get_batch_stats(result)

    assert stats["tier_1"]["n_batches"] == 0
    assert stats["tier_1"]["n_variables"] == 0
    assert stats["tier_2"]["n_batches"] == 0
    assert stats["tier_2"]["n_variables"] == 0
    assert stats["tier_3"]["n_batches"] == 0
    assert stats["tier_3"]["n_variables"] == 0


def test_get_batch_stats_with_data(classified_vars):
    """Test get_batch_stats with actual data."""
    result = create_batches(classified_vars)

    stats = get_batch_stats(result)

    assert stats["tier_1"]["n_batches"] >= 1
    assert stats["tier_1"]["n_variables"] >= 1
    assert stats["tier_2"]["n_batches"] >= 1
    assert stats["tier_2"]["n_variables"] >= 2
    assert stats["tier_3"]["n_batches"] == 1
    assert stats["tier_3"]["n_variables"] == 1


def test_get_batch_stats_avg_batch_size():
    """Test that avg_batch_size is calculated correctly."""
    result = BatchingResult(
        tier_1_batches=[Batch(tier=1, batch_index=0, variables=[("v1", None, None), ("v2", None, None)])],
        tier_2_batches=[
            Batch(tier=2, batch_index=0, variables=[("v3", None, None)] * 15),
            Batch(tier=2, batch_index=1, variables=[("v4", None, None)] * 10),
        ],
        tier_3_batches=[],
    )

    stats = get_batch_stats(result)

    assert stats["tier_2"]["n_variables"] == 25
    assert stats["tier_2"]["n_batches"] == 2
    assert stats["tier_2"]["avg_batch_size"] == 12.5


# ---------------------------------------------------------------------------
# Test constants
# ---------------------------------------------------------------------------


def test_constants():
    """Test that constants are defined correctly."""
    assert TIER_2_MIN_BATCH_SIZE == 10
    assert TIER_2_MAX_BATCH_SIZE == 20
