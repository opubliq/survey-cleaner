"""Pattern Engine - Core system for hybrid rule + LLM cleaning.

This module provides:
- Pattern definitions (Likert scales, demographics, binary, etc.)
- Pattern matching logic
- Rule generation from patterns + codebook
- Classification of variables by type and pattern
"""

from .patterns.likert_scales import Likert5AgreePattern, Likert7AgreePattern, LikertFrequencyPattern
from .patterns.demographics import ProvinceQCPattern, GenderPattern, AgeGroupsPattern
from .patterns.binary import BinaryYesNoPattern

# Export key patterns for external use
__all__ = [
    "likert_5_agree",
    "likert_7_agree",
    "likert_frequency",
    "province_qc",
    "gender",
    "age_groups",
    "binary_yes_no",
]

__version__ = "0.1.0"
