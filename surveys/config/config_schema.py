"""Configuration schema for survey-cleaner using Pydantic."""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class TierModels(BaseModel):
    """Model configurations for each tier."""

    tier1_validator: Optional[str] = Field(
        default="anthropic/claude-sonnet-4-20250514",
        description="Model for Tier 1 pattern validation",
    )
    tier2_batch: Optional[str] = Field(
        default="anthropic/claude-sonnet-4-20250514",
        description="Model for Tier 2 batch processing",
    )
    tier3_individual: Optional[str] = Field(
        default="anthropic/claude-sonnet-4-20250514",
        description="Model for Tier 3 individual processing",
    )


class SurveyCleanerConfig(BaseModel):
    """Main configuration schema for survey-cleaner."""

    default_model: Optional[str] = Field(
        default="anthropic/claude-sonnet-4-20250514",
        description="Default LLM model",
    )
    tier_models: TierModels = Field(default_factory=TierModels)
    tier1_model: Optional[str] = Field(default=None, description="Override tier 1 model")
    tier2_model: Optional[str] = Field(default=None, description="Override tier 2 model")
    tier3_model: Optional[str] = Field(default=None, description="Override tier 3 model")

    data_dir: Optional[Path] = Field(default=None, description="Data directory path")
    output_dir: Optional[Path] = Field(default=None, description="Output directory path")

    tier1_min_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    tier1_max_n_unique: int = Field(default=7, ge=1)
    tier2_max_batch_size: int = Field(default=20, ge=1)

    api_keys: dict[str, str] = Field(default_factory=dict)

    class Config:
        extra = "allow"


def get_config_path() -> Path:
    """Get the config file path."""
    config_dir = Path.home() / ".survey-cleaner"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config() -> SurveyCleanerConfig:
    """Load configuration from file."""
    config_path = get_config_path()
    if config_path.exists():
        import json

        with open(config_path) as f:
            data = json.load(f)
        return SurveyCleanerConfig(**data)
    return SurveyCleanerConfig()


def save_config(config: SurveyCleanerConfig) -> None:
    """Save configuration to file."""
    import json

    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config.model_dump(), f, indent=2, default=str)
