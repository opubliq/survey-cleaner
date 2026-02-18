# Critique des Propositions - Pattern Engine Architecture

## Consensus Points
- **Q1 (Modeling):** **Unanimous agreement on Hybrid (Option C)** - Classes with `to_pattern()` method for serialization. Best balance of OOP logic and JSON interoperability.
- **Q2 (Classifier Input):** **Unanimous agreement on both inputs (Option C)** - `pd.Series` + `VariableSchema | None`. Everyone recognizes real-world codebook quality is variable.
- **Q3 (Missing Codes):** **Strong consensus on explicit detection (Option C)** - All but two proposals (oc-glm-5-free and zai-glm-4.7-flash) choose preprocessing over filtering or threshold adjustment.

## Proposal Analysis

### google-gemini-2.5-flash
**Strengths:** Clean separation of concerns, thorough preprocessing step for missing codes.
**Weaknesses:** Detection logic location slightly vague.
**Blind Spot:** Doesn't explicitly state where detection lives (pattern vs matcher).

### oc-big-pickle ⭐
**Strengths:** Excellent `MissingCodeDetector` design, clear separation. Explicitly states detection logic belongs **in the pattern** (`matches()` method).
**Weaknesses:** None major.
**Blind Spot:** Could use more detail on how `to_pattern()` stays synchronized with class logic.

### oc-glm-5-free
**Strengths:** Graceful degradation logic, `_preprocess_missing_codes()` clarity.
**Weaknesses:** **CRITICAL FLAW:** Recommends Option A (filter before n_unique) which loses missing code metadata needed for `clean.py` documentation. Contradicts own rationale.
**Blind Spot:** Doesn't address how filtered series preserves missing code information for downstream.

### oc-kimi-k2.5-free
**Strengths:** Very thorough implementation sketch, good heuristic examples.
**Weaknesses:** Verbose, could be more concise.
**Blind Spot:** Missing code detection heuristics might need configuration per survey.

### oc-minimax-m2.5-free
**Strengths:** Prioritization logic for fallback, clean file structure.
**Weaknesses:** **KEY DISAGREEMENT:** Detection logic in **matcher** not pattern. This creates a "god class" matcher that knows about all patterns.
**Blind Spot:** Doesn't explain how matcher stays maintainable as patterns grow.

### zai-glm-4.5
**Strengths:** Clear, concise recommendations.
**Weaknesses:** High-level, less implementation detail.
**Blind Spot:** Assumes missing code library is comprehensive.

### zai-glm-4.7-flash
**Strengths:** Good threshold discussion, practical Tier 1 criteria.
**Weaknesses:** **CRITICAL FLAW:** Recommends Option A (filter before tiering) without documenting missing codes. Also puts detection logic in matcher implicitly via `_match_tier1()`.
**Blind Spot:** If missing codes are filtered without documentation, `clean.py` can't handle them properly.

### zai-glm-4.7
**Strengths:** Clear separation of concerns argument.
**Weaknesses:** Recommends Option A (pure OOP) not Hybrid for Q1, missing `to_pattern()` requirement.
**Blind Spot:** JSON serialization requirement from schema is understated.

## Key Disagreements

1. **Detection Logic Location:**
   - **In Pattern (oc-big-pickle, oc-kimi-k2.5-free):** Better encapsulation, easier to test, pattern owns its logic.
   - **In Matcher (oc-minimax-m2.5-free):** Centralized, but becomes monolithic.
   - **Lean: In Pattern** - Small team needs modular, testable components.

2. **Missing Code Strategy:**
   - **Explicit Detector (consensus):** Document then filter, preserve metadata.
   - **Pre-filter (oc-glm-5-free, zai-glm-4.7-flash):** Simple but loses documentation.
   - **Lean: Explicit Detector** - Missing codes must be documented for `clean.py` generation.

## TOP PICK: oc-big-pickle

**Why:** Best balance of all requirements. Detection logic **in pattern** (maintainable), **explicit missing code detector** (documented, testable), **both inputs with fallback** (robust). The `MissingCodeDetector` returning both cleaned series AND metadata is exactly what's needed for the pipeline.

**Hybrid Elements I'd Add:**
- Add `to_pattern()` auto-generation script to prevent divergence between class and JSON
- Make missing code detection configurable (not just hardcoded standard values)
- Add validation warning if missing code appears >5% (probably not actually missing)
