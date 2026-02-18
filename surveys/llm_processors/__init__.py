"""LLM Processors - Tier 2 batch + Tier 3 individual processing.

This module provides utilities for LLM-based survey cleaning:
- Batcher: Groups variables by tier after classification
- PromptCache: Caches system prompts to avoid re-sending heavy prompts

Key components:
- batcher.py: Optimal batching for Tier 2 (10-20 vars per batch)
- prompt_cache.py: In-memory + optional disk persistence for system prompts
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
]

__version__ = "0.1.0"
