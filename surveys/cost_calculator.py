"""
Cost tracking and calculation for Anthropic API usage

Tracks token usage and calculates costs based on model pricing.
Supports prompt caching cost calculations.
"""

from typing import Dict, List
from dataclasses import dataclass
import json
from pathlib import Path


# Anthropic API pricing (per million tokens)
# https://www.anthropic.com/api#pricing
PRICING = {
    "claude-sonnet-4-5-20250929": {
        "input": 3.00,              # $3/MTok
        "output": 15.00,            # $15/MTok
        "cache_write": 3.75,        # $3.75/MTok
        "cache_read": 0.30          # $0.30/MTok
    },
    "claude-3-5-haiku-20241022": {
        "input": 0.80,              # $0.80/MTok
        "output": 4.00,             # $4/MTok
        "cache_write": 1.00,        # $1/MTok
        "cache_read": 0.08          # $0.08/MTok
    }
}

# Shorter model names for convenience
MODEL_ALIASES = {
    "sonnet": "claude-sonnet-4-5-20250929",
    "haiku": "claude-3-5-haiku-20241022"
}


@dataclass
class APICallCost:
    """Cost details for a single API call"""
    model: str
    input_tokens: int
    output_tokens: int
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0

    @property
    def input_cost(self) -> float:
        """Cost for input tokens (non-cached)"""
        pricing = PRICING.get(self.model, PRICING["claude-sonnet-4-5-20250929"])
        return (self.input_tokens / 1_000_000) * pricing["input"]

    @property
    def output_cost(self) -> float:
        """Cost for output tokens"""
        pricing = PRICING.get(self.model, PRICING["claude-sonnet-4-5-20250929"])
        return (self.output_tokens / 1_000_000) * pricing["output"]

    @property
    def cache_write_cost(self) -> float:
        """Cost for writing to cache"""
        pricing = PRICING.get(self.model, PRICING["claude-sonnet-4-5-20250929"])
        return (self.cache_creation_tokens / 1_000_000) * pricing["cache_write"]

    @property
    def cache_read_cost(self) -> float:
        """Cost for reading from cache"""
        pricing = PRICING.get(self.model, PRICING["claude-sonnet-4-5-20250929"])
        return (self.cache_read_tokens / 1_000_000) * pricing["cache_read"]

    @property
    def total_cost(self) -> float:
        """Total cost for this API call"""
        return (self.input_cost + self.output_cost +
                self.cache_write_cost + self.cache_read_cost)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "model": self.model,
            "tokens": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "cache_creation": self.cache_creation_tokens,
                "cache_read": self.cache_read_tokens
            },
            "cost": {
                "input": round(self.input_cost, 4),
                "output": round(self.output_cost, 4),
                "cache_write": round(self.cache_write_cost, 4),
                "cache_read": round(self.cache_read_cost, 4),
                "total": round(self.total_cost, 4)
            }
        }


class CostTracker:
    """Tracks API costs across a survey processing session"""

    def __init__(self, survey_name: str):
        self.survey_name = survey_name
        self.calls: List[APICallCost] = []
        self.report_file = Path(f"surveys/{survey_name}/cost_report.json")

    def add_call(self, usage_data: dict, model: str):
        """Add an API call to tracking

        Args:
            usage_data: Usage dict from Anthropic API response
            model: Model name (can be alias like "sonnet" or full name)
        """
        # Resolve model alias
        full_model = MODEL_ALIASES.get(model, model)

        call = APICallCost(
            model=full_model,
            input_tokens=usage_data.get("input_tokens", 0),
            output_tokens=usage_data.get("output_tokens", 0),
            cache_creation_tokens=usage_data.get("cache_creation_input_tokens", 0),
            cache_read_tokens=usage_data.get("cache_read_input_tokens", 0)
        )
        self.calls.append(call)

    @property
    def total_calls(self) -> int:
        """Total number of API calls"""
        return len(self.calls)

    @property
    def total_cost(self) -> float:
        """Total cost across all calls"""
        return sum(call.total_cost for call in self.calls)

    @property
    def total_tokens(self) -> Dict[str, int]:
        """Total tokens by type"""
        return {
            "input": sum(call.input_tokens for call in self.calls),
            "output": sum(call.output_tokens for call in self.calls),
            "cache_write": sum(call.cache_creation_tokens for call in self.calls),
            "cache_read": sum(call.cache_read_tokens for call in self.calls)
        }

    @property
    def cache_hit_rate(self) -> float:
        """Cache hit rate (0-1)"""
        total = self.total_tokens
        cache_eligible = total["input"] + total["cache_read"]
        if cache_eligible == 0:
            return 0.0
        return total["cache_read"] / cache_eligible

    @property
    def savings_from_cache(self) -> float:
        """Estimated savings from cache usage

        Calculates what the cost would have been without caching
        """
        saved = 0.0
        for call in self.calls:
            pricing = PRICING.get(call.model, PRICING["claude-sonnet-4-5-20250929"])
            # Cache reads would have been regular input tokens
            regular_input_cost = (call.cache_read_tokens / 1_000_000) * pricing["input"]
            actual_cache_cost = call.cache_read_cost
            saved += (regular_input_cost - actual_cache_cost)
        return saved

    def get_breakdown_by_model(self) -> Dict[str, Dict]:
        """Get cost breakdown by model"""
        breakdown = {}
        for call in self.calls:
            model_short = "haiku" if "haiku" in call.model else "sonnet"
            if model_short not in breakdown:
                breakdown[model_short] = {
                    "calls": 0,
                    "cost": 0.0,
                    "tokens": {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}
                }

            breakdown[model_short]["calls"] += 1
            breakdown[model_short]["cost"] += call.total_cost
            breakdown[model_short]["tokens"]["input"] += call.input_tokens
            breakdown[model_short]["tokens"]["output"] += call.output_tokens
            breakdown[model_short]["tokens"]["cache_write"] += call.cache_creation_tokens
            breakdown[model_short]["tokens"]["cache_read"] += call.cache_read_tokens

        return breakdown

    def save_report(self):
        """Save cost report to JSON file"""
        report = {
            "survey": self.survey_name,
            "summary": {
                "total_calls": self.total_calls,
                "total_cost": round(self.total_cost, 2),
                "cache_hit_rate": round(self.cache_hit_rate * 100, 1),
                "savings_from_cache": round(self.savings_from_cache, 2),
                "tokens": self.total_tokens
            },
            "by_model": {
                model: {
                    "calls": data["calls"],
                    "cost": round(data["cost"], 2),
                    "tokens": data["tokens"]
                }
                for model, data in self.get_breakdown_by_model().items()
            },
            "calls": [call.to_dict() for call in self.calls]
        }

        self.report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

    def print_summary(self):
        """Print cost summary to console"""
        print("\n" + "=" * 60)
        print("API COST REPORT")
        print("=" * 60)
        print(f"Survey: {self.survey_name}")
        print(f"Total API calls: {self.total_calls}")
        print(f"\nCache performance:")
        print(f"  Hit rate: {self.cache_hit_rate * 100:.1f}%")
        print(f"  Savings: ${self.savings_from_cache:.2f}")

        print(f"\nTokens:")
        tokens = self.total_tokens
        print(f"  Input: {tokens['input']:,} ({tokens['input']/1000:.1f}K)")
        print(f"  Output: {tokens['output']:,} ({tokens['output']/1000:.1f}K)")
        print(f"  Cache writes: {tokens['cache_write']:,}")
        print(f"  Cache reads: {tokens['cache_read']:,}")

        print(f"\nCost breakdown by model:")
        for model, data in self.get_breakdown_by_model().items():
            print(f"  {model.capitalize()}: ${data['cost']:.2f} ({data['calls']} calls)")

        print(f"\n{'TOTAL COST':>40}: ${self.total_cost:.2f}")
        print(f"{'Without cache':>40}: ${self.total_cost + self.savings_from_cache:.2f}")
        print("=" * 60 + "\n")
