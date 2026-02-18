"""Pattern Engine - Core system for hybrid rule + LLM cleaning.

This module provides:
- Pattern definitions (Likert scales, demographics, binary, scales)
- Pattern matching logic
- Rule generation from patterns + codebook
- Classification of variables by type and pattern
- Missing code detection

Key components:
- patterns/: All pattern implementations (Likert, demographics, binary, scales)
- missing_code_detector: Preprocessing to identify sentinel codes
- pattern_classifier: Tier 1/2/3 routing based on data + codebook
"""

from surveys.pattern_engine.missing_code_detector import detect_missing_codes
from surveys.pattern_engine.pattern_classifier import classify
from surveys.pattern_engine.pattern_matcher import (
    MatchResult,
    NearMiss,
    PatternMatcher,
    get_default_matcher,
)
from surveys.pattern_engine.patterns import (
    BasePattern,
    BinaryPresentPattern,
    BinaryTrueFalsePattern,
    BinaryYesNoPattern,
    ClassificationResult,
    MissingCodeInfo,
    get_all_patterns,
    Likert3AgreePattern,
    Likert4AgreePattern,
    Likert5AgreePattern,
    Likert7AgreePattern,
    LikertFrequencyPattern,
)

__all__ = [
    # Core classifier
    "classify",
    "detect_missing_codes",
    # Pattern matcher
    "PatternMatcher",
    "MatchResult",
    "NearMiss",
    "get_default_matcher",
    # Base classes
    "BasePattern",
    "ClassificationResult",
    "MissingCodeInfo",
    # Pattern accessors
    "get_all_patterns",
    # Likert patterns
    "Likert3AgreePattern",
    "Likert4AgreePattern",
    "Likert5AgreePattern",
    "Likert7AgreePattern",
    "LikertFrequencyPattern",
    # Binary patterns
    "BinaryYesNoPattern",
    "BinaryTrueFalsePattern",
    "BinaryPresentPattern",
]

__version__ = "0.2.0"
