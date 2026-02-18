"""LLM Processors - Tier 2 batch + Tier 3 individual processing.

This module provides utilities for LLM-based survey cleaning:
- Batcher: Groups variables by tier after classification
- PromptCache: Caches system prompts to avoid re-sending heavy prompts
- Tier2BatchProcessor: Processes 10-20 variables per batch using GLM-5/GLM-4.7
- Tier3IndividualProcessor: Processes complex variables individually using Claude Haiku

Key components:
- batcher.py: Optimal batching for Tier 2 (10-20 vars per batch)
- prompt_cache.py: In-memory + optional disk persistence for system prompts
- tier2_batch.py: Batch LLM processing for semi-standard variables
- tier3_individual.py: Individual LLM processing for complex cases
"""

from surveys.llm_processors.batcher import (
    Batch,
    BatchingResult,
    TIER_2_MAX_BATCH_SIZE,
    TIER_2_MIN_BATCH_SIZE,
    VariableGroup,
    create_batches,
    get_batch_stats,
)
from surveys.llm_processors.prompt_cache import (
    CachedPrompt,
    PromptCache,
    get_default_cache,
)
from surveys.llm_processors.tier2_batch import (
    BatchProcessingResult,
    Tier2BatchProcessor,
    VariableCode,
    process_tier2_batch,
)
from surveys.llm_processors.tier3_individual import (
    Tier3Result,
    process_tier3_variable,
    process_tier3_batch,
    TIER_3_MODEL,
    TIER_3_MAX_TOKENS,
)

__all__ = [
    # Batcher
    "Batch",
    "BatchingResult",
    "TIER_2_MAX_BATCH_SIZE",
    "TIER_2_MIN_BATCH_SIZE",
    "VariableGroup",
    "create_batches",
    "get_batch_stats",
    # Prompt cache
    "CachedPrompt",
    "PromptCache",
    "get_default_cache",
    # Tier 2 batch processor
    "BatchProcessingResult",
    "Tier2BatchProcessor",
    "VariableCode",
    "process_tier2_batch",
    # Tier 3 individual processor
    "Tier3Result",
    "process_tier3_variable",
    "process_tier3_batch",
    "TIER_3_MODEL",
    "TIER_3_MAX_TOKENS",
]

__version__ = "0.1.0"
