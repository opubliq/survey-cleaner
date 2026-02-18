## **Summary**
I recommend a hybrid pattern modeling approach with dual-input classifier and explicit missing code detection. This architecture balances maintainability, robustness, and clarity for a small team building a survey cleaning pipeline.

## **Recommendation**

### **Question 1: Pattern Modeling - Option C (Hybrid)**
Use Python classes with `to_pattern()` method for JSON serialization. This keeps detection logic with patterns while enabling serialization.

```python
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    
    def matches(self, var: VariableSchema, series: pd.Series) -> float:
        # Detection logic here
        return confidence_score
    
    def to_pattern(self) -> Pattern:
        return Pattern(
            pattern_id=self.pattern_id,
            detection_criteria=self._get_criteria(),
            transformation_template=self._get_template()
        )
```

### **Question 2: Classifier Input - Option C (Both)**
Use both pandas stats and VariableSchema with graceful degradation:

```python
def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    # Primary classification using VariableSchema if available
    if var and var.scale_type:
        return _classify_from_schema(var)
    
    # Fallback to statistical analysis
    return _classify_from_stats(series)
```

### **Question 3: Missing Codes - Option C (Explicit Detection)**
Create a preprocessing step that detects, extracts, and documents missing codes before classification:

```python
def detect_missing_codes(series: pd.Series, var: VariableSchema | None = None) -> MissingCodeInfo:
    # Identify common missing codes: 98, 99, -9, -8, etc.
    # Check VariableSchema.missing_codes if available
    # Return documented missing codes for filtering
```

## **Trade-offs**

**Hybrid Patterns (Option C):**
- **Pros:** Logic encapsulation + serialization, extensible, testable
- **Cons:** Slight complexity overhead, requires maintaining two representations

**Dual-input Classifier (Option C):**
- **Pros:** Robust to variable codebook quality, semantic + statistical validation
- **Cons:** More complex interface, requires careful prioritization logic

**Explicit Missing Code Detection (Option C):**
- **Pros:** Transparent, consistent, handles diverse coding schemes, documentation
- **Cons:** Additional preprocessing step, requires comprehensive missing code library

## **Implementation Sketch**

1. **Start with base classes:**
   ```bash
   surveys/pattern_engine/patterns/base_pattern.py
   surveys/pattern_engine/patterns/likert_scales.py
   surveys/pattern_engine/patterns/demographics.py
   ```

2. **Build missing code detector:**
   ```python
   # surveys/pattern_engine/missing_codes.py
   COMMON_MISSING_CODES = {98, 99, -9, -8, -7, 999, 9999}
   ```

3. **Implement classifier with priority:**
   ```python
   # surveys/pattern_engine/pattern_classifier.py
   def classify(series, var=None):
       missing_info = detect_missing_codes(series, var)
       clean_series = series[~series.isin(missing_info.codes)]
       
       if var and var.scale_type:
           return classify_from_schema(var, clean_series)
       return classify_from_stats(clean_series)
   ```

4. **Tier 1 criteria:** Apply patterns to `clean_series` with `n_unique ≤ 7` (after missing code removal).
