## **FINAL VERDICT: Pattern Engine Architecture**

### **Vote Tally**

| Proposal | Votes | Supporters |
|----------|-------|------------|
| **oc-big-pickle** | **8/8 (100%)** | gemini-2.5-flash, oc-big-pickle, oc-glm-5-free, oc-kimi-k2.5-free, oc-minimax-m2.5-free, zai-glm-4.5, zai-glm-4.7-flash, zai-glm-4.7 |
| *Others* | 0/8 | - |

**Unanimous decision**: The council adopts **oc-big-pickle** as the foundation, with the agreed-upon modifications below.

---

### **Winning Direction**

**Architecture**: Hybrid Python classes with JSON serialization, dual-input classifier with graceful degradation, and explicit missing code detection as preprocessing.

**Core Philosophy**: 
- **Defensive by default**: Works without codebook, enhanced by it
- **Co-located logic**: Pattern detection lives WITHIN pattern classes
- **Document everything**: Missing codes detected, not silently filtered

---

### **Key Modifications from Critiques**

| Modification | Justification | Source |
|-------------|---------------|--------|
| **Confidence threshold for Tier 1** (>0.8) | Prevent false positives when patterns partially match | Multiple voters |
| **Conflict resolution priority** (binary > likert > demographics) | Handle ambiguous matches deterministically | oc-glm-5-free, oc-kimi-k2.5-free |
| **Warning on high missing code %** (>5%) | Flag potential false positives (maybe not actually missing) | oc-kimi-k2.5-free |
| **Auto-generation script for pattern_library.json** | Prevent divergence between class and JSON | gemini-2.5-flash |

---

### **Final Recommendation**

#### **Q1: Pattern Modeling — Hybrid Classes (Option C)**

```python
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    
    def matches(self, var: VariableSchema | None, series: pd.Series) -> float:
        # Detection logic HERE, not in a matcher god-class
        ...
        return confidence  # 0.0-1.0
    
    def to_pattern(self) -> Pattern:
        # Serialization for pattern_library.json
        return Pattern(pattern_id=..., detection_criteria=..., ...)
```

**Why**: Detection logic belongs with the pattern (SRP). Each pattern has unique heuristics—co-location aids maintainability for small teams. `to_pattern()` enables JSON serialization while keeping logic in Python.

---

#### **Q2: Classifier Input — Both with Prioritization (Option C)**

```python
def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    # 1. Detect missing codes FIRST (see Q3)
    effective_stats = compute_effective_stats(series)
    
    # 2. Cross-validate: Schema says "likert" but data shows 500 unique?
    if var and var.scale_type == "likert" and not looks_like_likert(effective_stats):
        return tier_2_or_3(var, effective_stats, reason="scale_type mismatch")
    
    # 3. Schema-first if reliable, fallback to stats
    if var and var.scale_type and matches_known_pattern(effective_stats, var):
        return tier_1_result(pattern_id, confidence=0.95)
    
    # 4. Stats-only fallback
    return stats_based_classify(effective_stats)
```

**Why**: Robust to variable codebook quality. Defensive: parser fails → use stats only. Codebook is good → validate against data. Cross-validation catches bad codebooks.

---

#### **Q3: Missing Codes — Explicit Detection Preprocessing (Option C)**

```python
@dataclass
class MissingCodeInfo:
    codes: set[int | float]
    meanings: dict[int, str]  # {98: "NSP", 99: "NR"}
    has_legitimate_range: bool

def detect_missing_codes(series: pd.Series, var: VariableSchema | None = None) -> MissingCodeInfo:
    # Use var.missing_codes if available, else heuristics (98, 99, -9, etc.)
    ...

# In classifier:
def classify(series: pd.Series, var: VariableSchema | None = None):
    missing = detect_missing_codes(series, var)
    effective_series = series[~series.isin(missing.codes)]
    effective_stats = compute_stats(effective_series)  # n_unique now meaningful!
    
    # Document missing codes in result for clean.py generation
    return ClassificationResult(..., missing_codes=missing, ...)
```

**Why**: `n_unique` reflects REAL response values (Likert 5 + 2 missing = effective n_unique=5). Preserves metadata for downstream `clean.py` (must document which codes are missing). Avoids fragile threshold adjustments.

---

### **Dissenting Views**

- **zai-glm-4.7** initially recommended pure OOP (Option A) for Q1, acknowledging C would be better for serialization but preferring simplicity. The council overruled: serialization is a hard requirement (`pattern_library.json` exists), so hybrid is necessary.

- **oc-minimax-m2.5-free** proposed detection logic in a centralized matcher. The council rejected this as it creates a "God class" that violates SRP and becomes unmaintainable as patterns grow.

---

### **Next Steps**

1. **Create infrastructure** (15 min)
   ```bash
   mkdir -p surveys/pattern_engine/patterns
   touch surveys/pattern_engine/{__init__.py,patterns/__init__.py}
   touch surveys/pattern_engine/patterns/base_pattern.py
   touch surveys/pattern_engine/missing_code_detector.py
   touch surveys/pattern_engine/pattern_classifier.py
   ```

2. **Implement `MissingCodeDetector`** — Critical preprocessing step

3. **Create 3 MVP patterns** (likert_5, binary_yn, province_qc) to validate architecture

4. **Build `PatternClassifier`** with conflict resolution and confidence thresholds

5. **Add auto-generation script** for `pattern_library.json` from pattern classes

6. **Test matrix**: 4 scenarios × (codebook present/absent)

---

**The architecture is decided. Implementation can proceed.**
