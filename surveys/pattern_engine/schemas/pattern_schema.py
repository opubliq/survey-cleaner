"""Pydantic models for pattern library."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DetectionCriteria(BaseModel):
    """Rules to automatically match variables to this pattern."""
    unique_values: Optional[list[int]] = None
    range_min: Optional[int] = None
    range_max: Optional[int] = None
    n_unique: Optional[int] = None
    name_keywords: Optional[list[str]] = None


class PatternMetadata(BaseModel):
    """Metadata for a pattern."""
    source_survey: Optional[str] = None
    created_date: Optional[str] = None
    notes: Optional[str] = None


class Pattern(BaseModel):
    """A cleaning pattern definition."""
    pattern_id: str
    pattern_name: str
    pattern_type: str
    detection_criteria: DetectionCriteria
    transformation_template: str
    examples_used: list[str] = []
    validated: bool = False
    metadata: Optional[PatternMetadata] = None


class PatternLibrary(BaseModel):
    """Container for all patterns."""
    patterns: list[Pattern] = Field(default_factory=list)
