"""Pattern implementations for survey variable cleaning.

All concrete pattern classes are exported here. Patterns are organized by category:
- Likert scales (likert_scales module)
- Demographics (demographics module)
- Binary variables (binary module)
- Numeric scales (scales module)

Usage:
    from surveys.pattern_engine.patterns import Likert5AgreePattern, BinaryYesNoPattern

    pattern = Likert5AgreePattern()
    confidence = pattern.matches(series, var_schema, missing_info)
    if confidence >= 0.8:
        code = pattern.generate_code("Q2", "ses_q2", var_schema)
"""

# Likert scales
from surveys.pattern_engine.patterns.likert_scales import (
    Likert3AgreePattern,
    Likert4AgreePattern,
    Likert5AgreePattern,
    Likert7AgreePattern,
    LikertFrequencyPattern,
)

# Demographics
from surveys.pattern_engine.patterns.demographics import (
    ProvinceQCPattern,
    GenderPattern,
    AgeGroupsPattern,
    AdminRegionQCPattern,
)

# Binary variables
from surveys.pattern_engine.patterns.binary import (
    BinaryYesNoPattern,
    BinaryTrueFalsePattern,
    BinaryPresentPattern,
)

# Numeric scales
from surveys.pattern_engine.patterns.scales import (
    Thermometer0to10Pattern,
    PercentageScalePattern,
    CountScalePattern,
)

# Base classes (for custom patterns)
from surveys.pattern_engine.patterns.base_pattern import (
    BasePattern,
    ClassificationResult,
    MissingCodeInfo,
)


__all__ = [
    # Base
    "BasePattern",
    "ClassificationResult",
    "MissingCodeInfo",
    # Likert
    "Likert3AgreePattern",
    "Likert4AgreePattern",
    "Likert5AgreePattern",
    "Likert7AgreePattern",
    "LikertFrequencyPattern",
    # Demographics
    "ProvinceQCPattern",
    "GenderPattern",
    "AgeGroupsPattern",
    "AdminRegionQCPattern",
    # Binary
    "BinaryYesNoPattern",
    "BinaryTrueFalsePattern",
    "BinaryPresentPattern",
    # Scales
    "Thermometer0to10Pattern",
    "PercentageScalePattern",
    "CountScalePattern",
]

# Helper: get all pattern instances (for pattern matcher)
def get_all_patterns() -> list[BasePattern]:
    """Return list of all pattern instances for pattern matching."""
    return [
        Likert3AgreePattern(),
        Likert4AgreePattern(),
        Likert5AgreePattern(),
        Likert7AgreePattern(),
        LikertFrequencyPattern(),
        ProvinceQCPattern(),
        GenderPattern(),
        AgeGroupsPattern(),
        AdminRegionQCPattern(),
        BinaryYesNoPattern(),
        BinaryTrueFalsePattern(),
        BinaryPresentPattern(),
        Thermometer0to10Pattern(),
        PercentageScalePattern(),
        CountScalePattern(),
    ]
