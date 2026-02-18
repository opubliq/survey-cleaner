"""Pydantic schema for a single codebook variable.

This is the atomic unit of the codebook parser output. Every variable
extracted from a raw codebook (PDF/Excel/MD) must conform to this schema
before being used by the pattern engine or LLM processors.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


class ValueLabel(BaseModel):
    """A single value → label mapping for a categorical variable."""

    value: int | float
    label: str
    is_missing: bool = False  # True for codes like 98=NSP, 99=NR, -1=Refus


class VariableSchema(BaseModel):
    """Schema for a single survey variable as extracted from a codebook.

    Designed to be the contract between:
    - codebook_parser/parser.py (producer, LLM output)
    - pattern_engine/pattern_matcher.py (consumer)
    - llm_processors/ (consumer, fallback)
    """

    # --- Identity ---
    var_name: str = Field(
        description="Variable name as it appears in the CSV/SPSS file (e.g., 'Q12_M2')"
    )
    var_label: str = Field(
        description="Human-readable question label from codebook (e.g., 'Satisfaction envers le gouvernement')"
    )

    # --- Type classification ---
    var_type: Literal["categorical", "ordinal", "numeric", "text", "unknown"] = Field(
        default="unknown",
        description="Variable type inferred from codebook"
    )
    scale_type: Optional[Literal[
        "likert", "binary", "demographic", "scale_0_10", "thermometer",
        "percentage", "count", "identifier", "open_ended", "other"
    ]] = Field(
        default=None,
        description="More specific scale type when known (filled by pattern engine, not required from parser)"
    )

    # --- Values ---
    value_labels: list[ValueLabel] = Field(
        default_factory=list,
        description="All value→label mappings from codebook, including missing codes"
    )
    missing_codes: list[int | float] = Field(
        default_factory=list,
        description="Codes representing missing data (e.g., [98, 99, -1]). Extracted separately for quick access."
    )

    # --- Range info (for numeric/scale variables) ---
    range_min: Optional[float] = Field(
        default=None,
        description="Minimum valid value (exclusive of missing codes)"
    )
    range_max: Optional[float] = Field(
        default=None,
        description="Maximum valid value (exclusive of missing codes)"
    )

    # --- Context ---
    question_text: Optional[str] = Field(
        default=None,
        description="Full question wording if available in codebook (may differ from var_label)"
    )
    filter_condition: Optional[str] = Field(
        default=None,
        description="Filter/skip condition from codebook (e.g., 'Posée seulement si Q1=1')"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Parser notes, ambiguities, or warnings about this variable"
    )

    # --- Source tracing ---
    codebook_page: Optional[int] = Field(
        default=None,
        description="Page number in source PDF where this variable was found"
    )
    parser_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="LLM parser confidence for this variable (0-1). Low confidence → flag for review."
    )

    @field_validator("missing_codes", mode="before")
    @classmethod
    def extract_missing_codes_from_labels(cls, v: list, info) -> list:
        """If missing_codes not explicitly set, derive from value_labels."""
        if v:
            return v
        # Will be populated post-init if value_labels has is_missing=True entries
        return v

    @property
    def valid_values(self) -> list[int | float]:
        """Return only non-missing values."""
        return [vl.value for vl in self.value_labels if not vl.is_missing]

    @property
    def all_values(self) -> list[int | float]:
        """Return all values including missing codes."""
        return [vl.value for vl in self.value_labels]

    def model_post_init(self, __context) -> None:
        """Auto-populate missing_codes and range from value_labels if not set."""
        if not self.missing_codes and self.value_labels:
            self.missing_codes = [vl.value for vl in self.value_labels if vl.is_missing]

        valid = self.valid_values
        if valid:
            if self.range_min is None:
                self.range_min = min(valid)
            if self.range_max is None:
                self.range_max = max(valid)
