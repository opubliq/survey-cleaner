"""Batcher for grouping variables by tier after classification.

This module provides intelligent batching for LLM processing:
- Groups variables by tier (1, 2, 3)
- Tier 2: optimal batches of 10-20 vars based on type similarity
- Similarity grouping: var_type, scale_type, pattern_id for better prompt coherence
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema
    from surveys.pattern_engine.patterns.base_pattern import ClassificationResult


TIER_2_MIN_BATCH_SIZE = 10
TIER_2_MAX_BATCH_SIZE = 20


@dataclass
class VariableGroup:
    """A group of variables with the same characteristics."""

    tier: int
    var_type: str
    scale_type: Optional[str]
    pattern_id: Optional[str]
    variables: list[tuple[str, VariableSchema, ClassificationResult]] = field(default_factory=list)

    def add_variable(self, var_name: str, var: VariableSchema, result: ClassificationResult) -> None:
        self.variables.append((var_name, var, result))

    @property
    def size(self) -> int:
        return len(self.variables)

    def can_add_more(self) -> bool:
        if self.tier == 2:
            return self.size < TIER_2_MAX_BATCH_SIZE
        return True


@dataclass
class Batch:
    """A batch of variables for LLM processing."""

    tier: int
    batch_index: int
    variables: list[tuple[str, VariableSchema, ClassificationResult]] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.variables)

    def is_full(self) -> bool:
        if self.tier == 2:
            return self.size >= TIER_2_MAX_BATCH_SIZE
        if self.tier == 3:
            return self.size >= 1
        return True


@dataclass
class BatchingResult:
    """Result of the batching process."""

    tier_1_batches: list[Batch]
    tier_2_batches: list[Batch]
    tier_3_batches: list[Batch]


def create_batches(
    classified_vars: dict[str, tuple[VariableSchema, ClassificationResult]],
) -> BatchingResult:
    """Group variables by tier and create optimal batches.

    Args:
        classified_vars: Mapping of var_name → (VariableSchema, ClassificationResult)

    Returns:
        BatchingResult with batches for each tier.
    """
    tier_1: list[tuple[str, VariableSchema, ClassificationResult]] = []
    tier_2: list[tuple[str, VariableSchema, ClassificationResult]] = []
    tier_3: list[tuple[str, VariableSchema, ClassificationResult]] = []

    for var_name, (var, result) in classified_vars.items():
        if result.tier == 1:
            tier_1.append((var_name, var, result))
        elif result.tier == 2:
            tier_2.append((var_name, var, result))
        else:
            tier_3.append((var_name, var, result))

    tier_2_groups = _group_tier_2_by_similarity(tier_2)

    return BatchingResult(
        tier_1_batches=_create_tier_1_batches(tier_1),
        tier_2_batches=_create_tier_2_batches(tier_2_groups),
        tier_3_batches=_create_tier_3_batches(tier_3),
    )


def _group_tier_2_by_similarity(
    variables: list[tuple[str, VariableSchema, ClassificationResult]],
) -> list[VariableGroup]:
    """Group Tier 2 variables by similarity (var_type, scale_type, pattern_id)."""
    groups_dict: dict[tuple[int, str, Optional[str], Optional[str]], VariableGroup] = {}

    for var_name, var, result in variables:
        group_key = (
            result.tier,
            var.var_type,
            var.scale_type,
            result.pattern_id,
        )

        if group_key not in groups_dict:
            groups_dict[group_key] = VariableGroup(
                tier=result.tier,
                var_type=var.var_type,
                scale_type=var.scale_type,
                pattern_id=result.pattern_id,
            )

        groups_dict[group_key].add_variable(var_name, var, result)

    return list(groups_dict.values())


def _create_tier_1_batches(
    variables: list[tuple[str, VariableSchema, ClassificationResult]],
) -> list[Batch]:
    """Create batches for Tier 1 variables.

    Tier 1 variables can be processed by rules, so we return a single batch.
    """
    if not variables:
        return []

    return [
        Batch(
            tier=1,
            batch_index=0,
            variables=variables,
        )
    ]


def _create_tier_2_batches(
    groups: list[VariableGroup],
) -> list[Batch]:
    """Create optimal batches for Tier 2 variables (10-20 vars per batch).

    Groups similar variables together for better prompt coherence.
    Splits groups that exceed TIER_2_MAX_BATCH_SIZE.
    """
    batches: list[Batch] = []
    batch_index = 0

    for group in groups:
        variables = group.variables

        while variables:
            batch_size = min(len(variables), TIER_2_MAX_BATCH_SIZE)
            batch_vars = variables[:batch_size]
            variables = variables[batch_size:]

            batches.append(
                Batch(
                    tier=2,
                    batch_index=batch_index,
                    variables=batch_vars,
                )
            )
            batch_index += 1

    return batches


def _create_tier_3_batches(
    variables: list[tuple[str, VariableSchema, ClassificationResult]],
) -> list[Batch]:
    """Create batches for Tier 3 variables.

    Tier 3 variables are processed individually (1 var per batch).
    """
    batches: list[Batch] = []

    for idx, (var_name, var, result) in enumerate(variables):
        batches.append(
            Batch(
                tier=3,
                batch_index=idx,
                variables=[(var_name, var, result)],
            )
        )

    return batches


def get_batch_stats(result: BatchingResult) -> dict:
    """Return statistics about the batching result."""
    return {
        "tier_1": {
            "n_batches": len(result.tier_1_batches),
            "n_variables": sum(b.size for b in result.tier_1_batches),
        },
        "tier_2": {
            "n_batches": len(result.tier_2_batches),
            "n_variables": sum(b.size for b in result.tier_2_batches),
            "avg_batch_size": sum(b.size for b in result.tier_2_batches) / len(result.tier_2_batches) if result.tier_2_batches else 0,
        },
        "tier_3": {
            "n_batches": len(result.tier_3_batches),
            "n_variables": sum(b.size for b in result.tier_3_batches),
        },
    }
