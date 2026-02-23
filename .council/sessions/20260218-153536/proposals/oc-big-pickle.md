Now I have a clear picture. Let me provide my architectural recommendations.

---

# Recommendations Architectural Review

## Summary

After reviewing the codebase, here's my assessment: the architecture is fundamentally sound but suffers from **integration debt** (unused components, disconnected validation). The core 3-tier design is correct; the issue is execution, not design. I recommend Option B for orchestration (activate existing batching), keeping classification deterministic, running a focused battue, standardizing naming via labels, and implementing tiered validation with escalation.

---

## Question 1: Orchestrator Structure

**Recommendation: Option B — Activate true batching with accumulation buffer**

The `batcher.py` is already implemented correctly (`create_batches()` exists and groups by similarity). The fix is minimal: after classification, create batches once, then process them:

```python
# Replace lines 517-559 in orchestrator.py with:
from surveys.llm_processors import create_batches, get_batch_stats

# After classification (line 495)
batching_result = create_batches(classified)
self._log(f"Batches: {get_batch_stats(batching_result)}")

# Process Tier 1 (instant)
for batch in batching_result.tier_1_batches:
    for var_name, var_schema, classification in batch.variables:
        code = self._process_tier1(var_name, var_schema, classification, df)
        # ... store result

# Process Tier 2 (true batches)
for batch in batching_result.tier_2_batches:
    results = self._process_tier2_batch(batch)
    # ... merge results

# Process Tier 3 (individual)
for batch in batching_result.tier_3_batches:
    # ... process each
```

**Trade-offs**: Minimal change, activates existing code, reduces API calls ~10-20x. No downside.

---

## Question 2: Classification — LLM in the Loop?

**Recommendation: Keep it deterministic (Option A) — but lower the Tier 1 threshold temporarily**

The 0.8 confidence threshold is causing false positives that require escalation anyway. Instead of adding LLM to classification:

1. **Lower Tier 1 threshold to 0.85** (be more conservative on what goes to pattern engine)
2. **Accept that Tier 2 will catch misclassifications** — it's free (GLM-5)
3. **Run the battue (Q3)** first to validate if patterns are underperforming

**Rationale**: Adding LLM to classification adds complexity and latency. The current design already routes ambiguous cases to Tier 2. The real problem is likely pattern calibration, not missing LLM in classification.

**Trade-offs**: Simpler architecture, but may over-rely on Tier 2. However, Tier 2 is free, so this is acceptable.

---

## Question 3: Battue on 500 Variables

**Recommendation: Yes, do it — but efficiently**

**Sous-question A**: Worth it. You need empirical data to calibrate patterns. Even with free Tier 2, knowing your Tier 1 rate helps budget time and understand the system.

**Sous-question B: Structured approach**

1. **Sampling**: Random 500 vars from all surveys (stratified by survey to avoid overfitting to one dataset)
2. **Tool**: Simple Google Sheets or CSV with columns: `var_name, pattern_id, confidence, manual_tier, manual_notes`
3. **Metric**: Primary = Tier 1 match rate (target: ≥50%), Secondary = pattern_id accuracy

**Sous-question C**: Threshold. If Tier 1 rate is ≥60%, stop optimizing patterns — diminishing returns. If <40%, investigate missing patterns.

**Implementation sketch**:
```python
# Quick script to extract sample
import pandas as pd
from pathlib import Path

# List all surveys with data files
surveys_dir = Path("_SharedFolder_data_produit")
survey_ids = [d.name for d in surveys_dir.iterdir() if d.is_dir()]

# Sample 10 vars per survey = ~570 vars
sample_vars = []
for sid in survey_ids[:57]:
    df = load_one_survey(sid)
    sample_vars.extend(random.sample(list(df.columns), min(10, len(df.columns))))
```

---

## Question 4: Naming Strategy

**Recommendation: Option C — Use codebook labels for Tier 1, LLM for Tier 2**

The current naming is unreadable (`op_q15_m2_eval_gvt`). Fix:

1. **Tier 1**: Use `var_label` from codebook, convert to snake_case, apply prefix:
   ```python
   # _generate_clean_var_name() rewrite
   def _generate_clean_var_name(var_name: str, var_schema: VariableSchema, pattern) -> str:
       label = var_schema.var_label or var_name
       # Clean: "Satisfaction toward government" → "satisfaction_toward_government"
       clean = re.sub(r'[^a-z0-9]+', '_', label.lower()).strip('_')[:25]
       
       prefix = {"demographic": "ses", "likert": "op", "binary": "op", "scale": "op"}.get(
           pattern.pattern_type, "op"
       )
       return f"{prefix}_{clean}"
   ```

2. **Tier 2**: GLM-5 already names well — keep as-is, but validate prefix in prompt

**Trade-offs**: Requires codebook labels to exist. Fallback to current logic if no label. Better names improve downstream analysis significantly.

---

## Question 5: Validation Integration

**Recommendation: Tiered validation — static first, then LLM-light for Tier 1 only**

**Integration point**: After all variables processed, before `assemble_clean_py()`:

```python
# In orchestrator.py, after processing loop, before line 565
from surveys.validation.validator import CleanValidator

validator = CleanValidator()
validation_results = validator.validate(survey_state.variables)

# For Tier 1 failures only, run semantic check
tier1_failures = [v for v in validation_results.failed if v.tier == 1]
if tier1_failures:
    self._log(f"Retrying {len(tier1_failures)} Tier 1 variables with semantic check...")
    # Retry via Tier 2 or escalate
```

**LLM in validation**: Only for Tier 1 failures — ask GLM-5: "Does this mapping make sense semantically?" (free, fast).

**Trade-offs**: Static validation catches syntax errors cheaply. LLM-light catches semantic errors (inverted Likert) before escalation. Full LLM review is overkill.

---

## Question 6: Escalation Strategy

**Recommendation: Automatic escalation with confidence-based shortcut**

```python
def _process_with_escalation(var_name, var_schema, classification, df, max_tier=3):
    current_tier = classification.tier
    
    # Shortcut: low confidence → skip Tier 1, go straight to Tier 2
    if current_tier == 1 and classification.confidence < 0.85:
        current_tier = 2
    
    for tier in range(current_tier, max_tier + 1):
        try:
            code = process(var_name, var_schema, tier)
            if validate(code):
                return code
        except ValidationError as e:
            if tier == max_tier:
                return error_code(f"needs_review: {e}")
            # Escalate automatically
            continue
```

**Key rules**:
- **A**: Auto-escalate on validation failure
- **B**: Pass the validation error reason to next tier
- **C**: Max 3 attempts (Tier 1 → 2 → 3), then `needs_review=True`
- **D**: Yes, bump threshold to 0.85 for Tier 1 to reduce false positives

---

## Priority Order for Implementation

1. **Week 1**: Activate batching (Question 1) — 2 hours
2. **Week 1**: Add validation to orchestrator (Question 5) — 4 hours  
3. **Week 2**: Run battue on 500 vars (Question 3) — 2-4 days
4. **Week 2**: Fix naming (Question 4) — 2 hours
5. **Week 3**: Add escalation (Question 6) — 4 hours

This gives you a working, validated pipeline with empirical data to guide future optimization.
