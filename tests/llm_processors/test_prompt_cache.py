"""Tests for prompt_cache.py."""

import json
from pathlib import Path

import pytest

from surveys.llm_processors import CachedPrompt, PromptCache, get_default_cache


# ---------------------------------------------------------------------------
# Test PromptCache initialization
# ---------------------------------------------------------------------------


def test_prompt_cache_init_no_persistence():
    """Test PromptCache initialization without persistence."""
    cache = PromptCache()

    assert cache._cache == {}
    assert cache.persist_file is None


def test_prompt_cache_init_with_persistence(tmp_path: Path):
    """Test PromptCache initialization with persistence file."""
    persist_file = tmp_path / "test_cache.json"
    cache = PromptCache(persist_file=persist_file)

    assert cache.persist_file == persist_file


def test_prompt_cache_init_loads_from_disk(tmp_path: Path):
    """Test that PromptCache loads existing cache from disk."""
    persist_file = tmp_path / "test_cache.json"

    # Create a cache file
    data = {
        "key1": {
            "key": "key1",
            "content": "cached content",
            "metadata": {"model": "glm-4.7"},
            "hit_count": 5,
        }
    }
    with open(persist_file, "w") as f:
        json.dump(data, f)

    # Load cache
    cache = PromptCache(persist_file=persist_file)

    assert len(cache._cache) == 1
    assert "key1" in cache._cache
    assert cache._cache["key1"].content == "cached content"
    assert cache._cache["key1"].hit_count == 5


# ---------------------------------------------------------------------------
# Test PromptCache.get and set
# ---------------------------------------------------------------------------


def test_prompt_cache_set_and_get():
    """Test setting and getting cached prompts."""
    cache = PromptCache()
    system_prompt = "You are a helpful assistant."
    response = "Hello! How can I help you?"

    cache.set(system_prompt, response, metadata={"model": "glm-4.7"})

    cached = cache.get(system_prompt)

    assert cached is not None
    assert cached.content == response
    assert cached.metadata == {"model": "glm-4.7"}
    assert cached.hit_count == 1


def test_prompt_cache_get_increments_hit_count():
    """Test that getting a prompt increments hit count."""
    cache = PromptCache()
    system_prompt = "Test prompt"
    response = "Test response"

    cache.set(system_prompt, response)

    assert cache.get(system_prompt).hit_count == 1
    assert cache.get(system_prompt).hit_count == 2
    assert cache.get(system_prompt).hit_count == 3


def test_prompt_cache_get_not_found():
    """Test that get returns None for non-existent prompts."""
    cache = PromptCache()

    cached = cache.get("non-existent prompt")

    assert cached is None


def test_prompt_cache_set_without_metadata():
    """Test setting a cache without metadata."""
    cache = PromptCache()
    system_prompt = "Test prompt"
    response = "Test response"

    cached = cache.set(system_prompt, response)

    assert cached.metadata == {}
    assert cached.content == response


def test_prompt_cache_key_generation():
    """Test that cache key is generated correctly from content."""
    cache = PromptCache()
    prompt1 = "You are a helpful assistant."
    prompt2 = "You are a helpful assistant."
    prompt3 = "You are a helpful assistant!"  # Slight difference

    cache.set(prompt1, "response1")
    cache.set(prompt3, "response3")

    # prompt1 and prompt2 should have the same key
    assert cache.get(prompt1).content == "response1"
    assert cache.get(prompt2).content == "response1"

    # prompt3 should have a different key
    assert cache.get(prompt3).content == "response3"


# ---------------------------------------------------------------------------
# Test PromptCache persistence
# ---------------------------------------------------------------------------


def test_prompt_cache_saves_to_disk(tmp_path: Path):
    """Test that cache saves to disk when persistence is enabled."""
    persist_file = tmp_path / "test_cache.json"
    cache = PromptCache(persist_file=persist_file)

    cache.set("prompt1", "response1", {"model": "glm-4.7"})
    cache.set("prompt2", "response2", {"model": "glm-5"})

    # Check file was created
    assert persist_file.exists()

    # Check file contents
    with open(persist_file) as f:
        data = json.load(f)

    assert len(data) == 2
    assert "response1" in [v["content"] for v in data.values()]
    assert "response2" in [v["content"] for v in data.values()]


def test_prompt_cache_creates_directory_if_needed(tmp_path: Path):
    """Test that cache creates parent directory if it doesn't exist."""
    persist_file = tmp_path / "subdir" / "cache.json"

    cache = PromptCache(persist_file=persist_file)
    cache.set("prompt", "response")

    assert persist_file.exists()


def test_prompt_cache_no_persistence_without_file():
    """Test that cache doesn't save when persist_file is None."""
    cache = PromptCache()

    cache.set("prompt", "response")

    # No exception should be raised
    assert len(cache._cache) == 1


# ---------------------------------------------------------------------------
# Test PromptCache.clear
# ---------------------------------------------------------------------------


def test_prompt_cache_clear():
    """Test clearing the cache."""
    cache = PromptCache()

    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")

    assert len(cache._cache) == 2

    cache.clear()

    assert len(cache._cache) == 0


def test_prompt_cache_clear_with_persistence(tmp_path: Path):
    """Test that clear removes persistence file."""
    persist_file = tmp_path / "test_cache.json"
    cache = PromptCache(persist_file=persist_file)

    cache.set("prompt", "response")
    assert persist_file.exists()

    cache.clear()

    assert len(cache._cache) == 0
    assert not persist_file.exists()


# ---------------------------------------------------------------------------
# Test PromptCache.get_stats
# ---------------------------------------------------------------------------


def test_prompt_cache_get_stats_empty():
    """Test get_stats with empty cache."""
    cache = PromptCache()

    stats = cache.get_stats()

    assert stats["total_entries"] == 0
    assert stats["total_hits"] == 0
    assert stats["avg_hits_per_entry"] == 0
    assert stats["persist_file"] is None


def test_prompt_cache_get_stats_with_data():
    """Test get_stats with cached data."""
    cache = PromptCache()

    cache.set("prompt1", "response1")
    cache.set("prompt2", "response2")

    # Hit some entries multiple times
    cache.get("prompt1")
    cache.get("prompt1")
    cache.get("prompt2")

    stats = cache.get_stats()

    assert stats["total_entries"] == 2
    assert stats["total_hits"] == 3
    assert stats["avg_hits_per_entry"] == 1.5


def test_prompt_cache_get_stats_with_persistence(tmp_path: Path):
    """Test that get_stats includes persist_file path."""
    persist_file = tmp_path / "test_cache.json"
    cache = PromptCache(persist_file=persist_file)

    stats = cache.get_stats()

    assert stats["persist_file"] == str(persist_file)


# ---------------------------------------------------------------------------
# Test get_default_cache
# ---------------------------------------------------------------------------


def test_get_default_cache_singleton():
    """Test that get_default_cache returns a singleton."""
    cache1 = get_default_cache()
    cache2 = get_default_cache()

    assert cache1 is cache2


def test_get_default_cache_with_persistence(tmp_path: Path):
    """Test that get_default_cache with persistence works."""
    # Reset singleton to avoid interference from other tests
    if hasattr(get_default_cache, "_instance"):
        delattr(get_default_cache, "_instance")

    persist_file = tmp_path / "default_cache.json"

    cache = get_default_cache(persist_file=persist_file)

    assert cache.persist_file == persist_file
    assert isinstance(cache, PromptCache)


def test_get_default_cache_persists_singleton_with_persistence(tmp_path: Path):
    """Test that get_default_cache singleton persists even with different persistence files."""
    # Reset singleton to avoid interference from other tests
    if hasattr(get_default_cache, "_instance"):
        delattr(get_default_cache, "_instance")

    persist_file1 = tmp_path / "cache1.json"
    persist_file2 = tmp_path / "cache2.json"

    cache1 = get_default_cache(persist_file=persist_file1)
    cache2 = get_default_cache(persist_file=persist_file2)

    # Same instance, so second persistence file is ignored
    assert cache1 is cache2
    assert cache1.persist_file == persist_file1


# ---------------------------------------------------------------------------
# Test CachedPrompt
# ---------------------------------------------------------------------------


def test_cached_prompt_creation():
    """Test creating a CachedPrompt."""
    prompt = CachedPrompt(
        key="test_key",
        content="test content",
        metadata={"model": "glm-4.7"},
        hit_count=5,
    )

    assert prompt.key == "test_key"
    assert prompt.content == "test content"
    assert prompt.metadata == {"model": "glm-4.7"}
    assert prompt.hit_count == 5


def test_cached_prompt_defaults():
    """Test CachedPrompt default values."""
    prompt = CachedPrompt(key="test_key", content="test content")

    assert prompt.metadata == {}
    assert prompt.hit_count == 0
