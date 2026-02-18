"""Prompt cache for LLM system prompts.

This module provides caching for system prompts to avoid re-sending
heavy prompts (codebook JSON, instructions) with each LLM call.

Features:
- In-memory dict cache for fast access
- Optional JSON file persistence for session-to-session caching
- Cache key based on prompt content hash
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class CachedPrompt:
    """A cached prompt with metadata."""

    key: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    hit_count: int = 0


class PromptCache:
    """Cache for system prompts.

    Usage:
        cache = PromptCache()
        
        # Check cache first
        cached = cache.get(system_prompt)
        if cached:
            return cached
        
        # Generate new response
        response = llm.generate(system_prompt, user_prompt)
        
        # Store in cache
        cache.set(system_prompt, response, metadata={"model": "glm-4.7"})
    """

    def __init__(self, persist_file: Optional[str | Path] = None):
        """Initialize the prompt cache.

        Args:
            persist_file: Optional path to JSON file for persistence.
        """
        self._cache: dict[str, CachedPrompt] = {}
        self.persist_file = Path(persist_file) if persist_file else None

        if self.persist_file and self.persist_file.exists():
            self._load_from_disk()

    def _generate_key(self, content: str) -> str:
        """Generate a cache key from content using SHA256."""
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str) -> Optional[CachedPrompt]:
        """Get a cached prompt.

        Args:
            prompt: The system prompt to look up.

        Returns:
            CachedPrompt if found, None otherwise.
        """
        key = self._generate_key(prompt)
        cached = self._cache.get(key)

        if cached:
            cached.hit_count += 1

        return cached

    def set(
        self,
        prompt: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> CachedPrompt:
        """Cache a prompt.

        Args:
            prompt: The system prompt used as key.
            content: The cached content (e.g., LLM response).
            metadata: Optional metadata to store with the cache.

        Returns:
            The created CachedPrompt.
        """
        key = self._generate_key(prompt)
        cached = CachedPrompt(
            key=key,
            content=content,
            metadata=metadata or {},
        )

        self._cache[key] = cached

        if self.persist_file:
            self._save_to_disk()

        return cached

    def clear(self) -> None:
        """Clear all cached prompts."""
        self._cache.clear()

        if self.persist_file and self.persist_file.exists():
            self.persist_file.unlink()

    def get_stats(self) -> dict[str, Any]:
        """Return cache statistics."""
        total_hits = sum(p.hit_count for p in self._cache.values())
        total_entries = len(self._cache)

        return {
            "total_entries": total_entries,
            "total_hits": total_hits,
            "avg_hits_per_entry": total_hits / total_entries if total_entries > 0 else 0,
            "persist_file": str(self.persist_file) if self.persist_file else None,
        }

    def _load_from_disk(self) -> None:
        """Load cache from JSON file."""
        if not self.persist_file or not self.persist_file.exists():
            return

        try:
            with open(self.persist_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key, value in data.items():
                self._cache[key] = CachedPrompt(**value)
        except Exception:
            pass

    def _save_to_disk(self) -> None:
        """Save cache to JSON file."""
        if not self.persist_file:
            return

        self.persist_file.parent.mkdir(parents=True, exist_ok=True)

        data = {}
        for key, cached in self._cache.items():
            data[key] = {
                "key": cached.key,
                "content": cached.content,
                "metadata": cached.metadata,
                "hit_count": cached.hit_count,
            }

        with open(self.persist_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def get_default_cache(persist_file: Optional[str | Path] = None) -> PromptCache:
    """Get a default prompt cache instance.

    Args:
        persist_file: Optional path to JSON file for persistence.

    Returns:
        A PromptCache instance.
    """
    if not hasattr(get_default_cache, "_instance"):
        get_default_cache._instance = PromptCache(persist_file=persist_file)

    return get_default_cache._instance
