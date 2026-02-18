## Summary

The team is building a pattern engine with deterministic detection for ~50% of survey variables. For maintainability and flexibility with small team, use **hybrid classes**; **combine Series and VariableSchema** inputs for classification; and **filter missing codes before tiering**.

## Recommendation

### Question 1: Modélisation - **Hybrid Classes**

```python
class BasePattern:
    """Pattern logic encapsulated in classes."""
    
    def matches(self, series: pd.Series) -> float:
        """Returns confidence 0.0-1.0."""
        raise NotImplementedError
    
    def generate_code(self, var_name: str, var_schema: VariableSchema) -> str:
        """Returns transformation code."""
        raise NotImplementedError
    
    def to_pattern(self) -> Pattern:
        """Serializes to Pydantic Pattern for JSON storage."""
        return Pattern(
            pattern_id=self.pattern_id,
            pattern_name=self.pattern_name,
            pattern_type=self.pattern_type,
            detection_criteria=self._build_detection_criteria(),
            transformation_template=self.transformation_template,
            validated=False
        )

class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    
    def matches(self, series: pd.Series) -> float:
        """Returns 1.0 if 5 unique ordered values, 0.0 otherwise."""
        if len(series.unique()) != 5:
            return 0.0
        # Check ordering
        unique = sorted(series.unique())
        if not all(abs(unique[i] - unique[i-1]) == 1 for i in range(1, len(unique))):
            return 0.0
        return 1.0
    
    def generate_code(self, var_name: str, var_schema: VariableSchema) -> str:
        mapping = self._build_mapping(var_schema)
        return f"df_clean['{var_name}'] = df['{var_name}'].map({mapping})"
    
    def _build_mapping(self, var_schema: VariableSchema) -> dict:
        # Extract labels from var_schema.value_labels
        return {vl.value: vl.label for vl in var_schema.value_labels if not vl.is_missing}
```

**Why:**
- OOP classes provide natural encapsulation for complex detection logic
- `to_pattern()` method keeps data serializable via Pydantic
- Easier for small team to understand and extend (each pattern is a file)
- No split between "what" and "how" - these live together

### Question 2: Input du Classifier - **Both (hybrid) with Series first**

```python
class PatternClassifier:
    def classify(self, series: pd.Series, var_schema: VariableSchema | None = None) -> ClassificationResult:
        """
        Classifies variable into Tier 1/2/3.
        Series data for statistical analysis (deterministic).
        var_schema for semantic context (LLM fallback).
        """
        tier1_candidates = self._match_tier1(series)
        
        if tier1_candidates:
            return ClassificationResult(tier=1, pattern_id=candidates[0].pattern_id, confidence=1.0)
        
        # If tier1 fails, use LLM for Tier 2/3
        if var_schema:
            return self._llm_classify(series, var_schema)
        else:
            return ClassificationResult(tier=3, pattern_id=None, confidence=0.0)
```

**Why:**
- Series provides ground truth for deterministic matching (n_unique, distribution)
- var_schema adds semantic context (scale_type="likert" already parsed)
- Missing codes in schema help validation (avoid false tier1 hits)
- Fallback to LLM only when series stats insufficient

### Question 3: Missing Codes - **Filter before tiering**

```python
def filter_missing_codes(series: pd.Series, missing_codes: list[int] | None = None) -> pd.Series:
    """Removes missing codes before statistical analysis."""
    if missing_codes is None:
        # Heuristic: check for common patterns
        return series.dropna()
    
    return series[~series.isin(missing_codes)]
```

```python
def classify(self, series: pd.Series, var_schema: VariableSchema | None = None) -> ClassificationResult:
    # Filter missing codes BEFORE tiering
    filtered = filter_missing_codes(series, var_schema.missing_codes if var_schema else None)
    n_unique = filtered.nunique()
    
    if n_unique <= 5 and self._is_ordered(filtered):
        return ClassificationResult(tier=1, pattern_id="likert_5", confidence=1.0)
    
    return ClassificationResult(tier=3, pattern_id=None, confidence=0.0)
```

**Why:**
- Likert 5 + [98,99] → effective n_unique=5 (not 7)
- Keeps threshold reasonable (Tier1: 5-7 unique values)
- Missing codes documented in schema for transparency
- LLM fallback handles complex patterns even with many unique values

## Trade-offs

**Hybrid Classes:**
- ✅ Encapsulation makes patterns self-contained and testable
- ✅ Natural separation of concerns (logic in classes, data in Pydantic)
- ✅ Easy to extend with new patterns (just add file)
- ❌ More code than pure Pydantic (but small overhead for small team)
- ❌ Two representations to maintain (class ↔ JSON)

**Both Inputs:**
- ✅ Robust: uses ground truth (Series) + context (Schema)
- ✅ Flexible: can run without schema (e.g., early validation)
- ✅ Better tiering: schema informs LLM fallback prompts
- ❌ More complex interface (one optional parameter)
- ❌ Duplicate info (n_unique from Series, also in schema)

**Filter Missing Codes:**
- ✅ Keeps tier1 threshold realistic (5-7 unique values)
- ✅ Clear separation of "valid values" vs "missing codes"
- ✅ Works well for codebooks with standardized missing codes
- ❌ Requires schema to know missing codes (if codebook missing → heuristic)
- ❌ Loss of information (if missing codes are not true missing but valid low-prob values)

## Implementation Sketch

**Step 1: Create pattern base class**

```python
# surveys/pattern_engine/base_pattern.py
from abc import ABC, abstractmethod
from .schemas.pattern_schema import Pattern

class BasePattern(ABC):
    pattern_id: str
    pattern_name: str
    pattern_type: str
    transformation_template: str
    
    @abstractmethod
    def matches(self, series: pd.Series) -> float:
        """Returns confidence 0.0-1.0 if pattern detected."""
        pass
    
    @abstractmethod
    def generate_code(self, var_name: str, var_schema) -> str:
        """Returns transformation code."""
        pass
    
    def to_pattern(self) -> Pattern:
        """Convert to Pydantic for JSON storage."""
        return Pattern(
            pattern_id=self.pattern_id,
            pattern_name=self.pattern_name,
            pattern_type=self.pattern_type,
            detection_criteria=self._build_criteria(),
            transformation_template=self.transformation_template,
            validated=False
        )
    
    def _build_criteria(self) -> dict:
        return {}
```

**Step 2: Implement likert pattern**

```python
# surveys/pattern_engine/patterns/likert.py
import pandas as pd
from typing import list
from ..base_pattern import BasePattern
from ...schemas.variable_schema import VariableSchema

class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    pattern_name = "Likert 5 agree scale"
    pattern_type = "ordinal"
    transformation_template = "df_clean['{var}'] = df['{var}'].map({mapping})"
    
    def matches(self, series: pd.Series) -> float:
        if len(series.unique()) != 5:
            return 0.0
        unique = sorted(series.unique())
        if not all(abs(unique[i] - unique[i-1]) == 1 for i in range(1, len(unique))):
            return 0.0
        return 1.0
    
    def generate_code(self, var_name: str, var_schema: VariableSchema) -> str:
        mapping = {vl.value: vl.label for vl in var_schema.value_labels if not vl.is_missing}
        return self.transformation_template.format(
            var=var_name,
            mapping=mapping
        )
```

**Step 3: Create classifier with hybrid input**

```python
# surveys/pattern_engine/pattern_classifier.py
from typing import list, Optional
from .schemas.pattern_schema import Pattern, ClassificationResult
from .base_pattern import BasePattern

class PatternClassifier:
    def __init__(self, patterns: list[BasePattern]):
        self.patterns = patterns
    
    def classify(self, series: pd.Series, var_schema: Optional[VariableSchema] = None) -> ClassificationResult:
        # Filter missing codes before tiering
        filtered = self._filter_missing(series, var_schema)
        n_unique = filtered.nunique()
        
        # Check Tier1 patterns
        tier1 = self._match_tier1(filtered, var_schema)
        if tier1:
            return ClassificationResult(tier=1, pattern_id=tier1.pattern_id, confidence=1.0)
        
        # Fallback to LLM for Tier2/3
        return self._llm_classify(series, var_schema)
    
    def _filter_missing(self, series, var_schema):
        if var_schema and var_schema.missing_codes:
            return series[~series.isin(var_schema.missing_codes)]
        return series.dropna()
    
    def _match_tier1(self, series, var_schema) -> Optional[Pattern]:
        for pattern in self.patterns:
            if pattern.matches(series) >= 0.8:
                return pattern.to_pattern()
        return None
```

**Step 4: Update classification threshold**

```python
# Tier1 threshold: <= 7 unique values (after filtering missing)
# Likert 5 + [98,99] = effective 5 unique values (not 7)
if n_unique <= 5:
    confidence = 1.0
elif n_unique <= 7:
    confidence = 0.7
else:
    confidence = 0.0
```
