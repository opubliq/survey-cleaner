## Summary

Adopt **Option C (Hybrid)** for patterns—classes with `to_pattern()` serialization; **Option C (both inputs)** for the classifier with graceful degradation when codebook is absent; **Option A (filter missing codes before n_unique)** for tiering, with explicit missing code detection as a pre-processing step, not integrated into the classifier.

---

## Recommendation

### Question 1: Hybrid Classes with `to_pattern()`

```python
# base_pattern.py
class BasePattern(ABC):
    pattern_id: str
    tier: int = 1
    
    @abstractmethod
    def matches(self, var: VariableSchema | None, series: pd.Series) -> float: ...
    
    @abstractmethod
    def generate_code(self, var_name: str, var: VariableSchema | None) -> str: ...
    
    def to_pattern(self) -> Pattern:
        return Pattern(pattern_id=self.pattern_id, tier=self.tier, ...)

# likert_scales.py
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    expected_values = {1, 2, 3, 4, 5}
    
    def matches(self, var, series) -> float:
        clean = self._filter_missing(series, var)
        if clean.nunique() != 5:
            return 0.0
        if not self.expected_values.issuperset(clean.unique()):
            return 0.0
        # + heuristic: check label hints in var.value_labels if available
        return 0.85 + self._label_confidence_boost(var)
```

Detection logic lives **in the pattern class**. The matcher (zy4.3) iterates patterns and picks highest confidence. This keeps pattern definition and detection co-located—critical for maintainability.

### Question 2: Both Inputs with `None` Tolerance

```python
@dataclass
class ClassificationResult:
    tier: int
    pattern_id: str | None
    confidence: float
    used_codebook: bool

def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    clean_series = _preprocess_missing_codes(series, var)
    
    if var and var.scale_type == "likert":
        # Fast-path: codebook already tells us
        for pattern in LIKERT_PATTERNS:
            if pattern.matches(var, clean_series) > 0.8:
                return ClassificationResult(tier=1, pattern_id=pattern.pattern_id, ...)
    
    # Fallback: data-driven only
    for pattern in ALL_PATTERNS:
        score = pattern.matches(None, clean_series)
        ...
```

Robustness comes from graceful degradation: codebook enhances detection but isn't required.

### Question 3: Pre-filter Missing Codes

```python
def _preprocess_missing_codes(series: pd.Series, var: VariableSchema | None) -> pd.Series:
    missing_codes = set()
    if var and var.missing_codes:
        missing_codes = set(var.missing_codes)
    else:
        # Heuristic detection: {98, 99, -9, -8, 999}
        missing_codes = _detect_missing_heuristically(series)
    
    return series[~series.isin(missing_codes)]
```

This keeps pattern thresholds simple (n_unique ≤ 7 still means 7 real values). Missing codes are documented in `ClassificationResult.missing_codes` for downstream `clean.py` generation.

---

## Trade-offs

| Choice | Pros | Cons |
|--------|------|------|
| **Hybrid patterns** | Logic co-located; testable; serializable | More boilerplate than pure Pydantic |
| **Both inputs** | Robust to bad codebooks; can cross-validate | Interface complexity; tests need both paths |
| **Pre-filter missing** | Clean thresholds; explicit missing handling | Adds preprocessing step; heuristics may miss edge cases |

---

## Implementation Sketch

1. **Create `base_pattern.py`** with abstract `matches()` and `generate_code()`
2. **Implement 4 pattern files** per zy4.1, each registering patterns in `__all__`
3. **Add `preprocess.py`** with `_preprocess_missing_codes()` and heuristics
4. **Build `pattern_classifier.py`** with the dual-input signature
5. **Test matrix**: 4 scenarios × (codebook present/absent)
6. **Serialize pattern library** to JSON via `[p.to_pattern() for p in ALL_PATTERNS]`
