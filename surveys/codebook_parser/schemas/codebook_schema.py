"""Pydantic schema for a complete parsed codebook.

A CodebookSchema is the top-level output of codebook_parser/parser.py.
It contains all variables from a survey plus survey-level metadata.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date

from .variable_schema import VariableSchema


class SurveyMetadata(BaseModel):
    """Survey-level metadata extracted from the codebook."""

    survey_id: str = Field(
        description="Internal survey identifier (matches directory name, e.g., 'ces_2019')"
    )
    survey_name: Optional[str] = Field(
        default=None,
        description="Full name of the survey (e.g., 'Canadian Election Study 2019')"
    )
    year: Optional[int] = Field(
        default=None,
        description="Survey year"
    )
    language: Optional[str] = Field(
        default="fr",
        description="Primary language of the codebook (fr/en)"
    )
    n_variables_declared: Optional[int] = Field(
        default=None,
        description="Number of variables declared in the codebook (for validation cross-check)"
    )
    n_respondents: Optional[int] = Field(
        default=None,
        description="Sample size"
    )
    source_file: Optional[str] = Field(
        default=None,
        description="Original codebook filename (e.g., 'ces_2019_codebook.pdf')"
    )
    source_format: Optional[str] = Field(
        default=None,
        description="Format of source file: pdf | xlsx | md | txt | docx"
    )
    parsed_date: Optional[str] = Field(
        default=None,
        description="ISO date when this codebook was parsed (e.g., '2026-02-18')"
    )
    parser_model: Optional[str] = Field(
        default=None,
        description="LLM model used for parsing (e.g., 'opencode/glm-5-free')"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Parser notes about the codebook (ambiguities, assumptions made, etc.)"
    )


class CodebookSchema(BaseModel):
    """Complete parsed codebook for one survey.

    This is the output contract of codebook_parser/parser.py and the
    input contract for pattern_engine/ and llm_processors/.
    """

    metadata: SurveyMetadata
    variables: list[VariableSchema] = Field(
        default_factory=list,
        description="All variables parsed from the codebook, in order"
    )

    # --- Convenience properties ---

    @property
    def n_variables(self) -> int:
        """Number of variables parsed."""
        return len(self.variables)

    @property
    def variable_names(self) -> list[str]:
        """List of all variable names."""
        return [v.var_name for v in self.variables]

    def get_variable(self, var_name: str) -> VariableSchema | None:
        """Retrieve a variable by name (case-insensitive)."""
        var_name_lower = var_name.lower()
        for v in self.variables:
            if v.var_name.lower() == var_name_lower:
                return v
        return None

    def variables_by_type(self, var_type: str) -> list[VariableSchema]:
        """Filter variables by var_type."""
        return [v for v in self.variables if v.var_type == var_type]

    def low_confidence_variables(self, threshold: float = 0.7) -> list[VariableSchema]:
        """Return variables where the parser had low confidence."""
        return [v for v in self.variables if v.parser_confidence < threshold]

    @model_validator(mode="after")
    def check_declared_count(self) -> "CodebookSchema":
        """Warn if parsed count differs from declared count."""
        declared = self.metadata.n_variables_declared
        if declared is not None and self.n_variables != declared:
            # Don't raise — just note in metadata (parser might have missed some)
            note = (
                f"WARNING: codebook declares {declared} variables "
                f"but {self.n_variables} were parsed."
            )
            existing = self.metadata.notes or ""
            self.metadata.notes = f"{existing}\n{note}".strip()
        return self
