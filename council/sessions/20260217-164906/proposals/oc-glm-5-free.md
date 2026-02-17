## Summary

Recommending **Hybrid (C) with free models via opencode**. Your free model access (GLM-5, Kimi K2.5) is the game-changer—you've been overpaying for tasks that don't require Claude-level reasoning. The key insight: survey cleaning is structured data transformation, not creative problem-solving. Free models excel at this.

---

## Recommendation

### Architecture: 3-Stage Pipeline

```
Stage 1: Codebook → Structured JSON (1 LLM call, free model)
         ↓
Stage 2: Variable classification (deterministic rules)
         ↓
Stage 3: Clean.py generation
         ├─ Type A (65%): deterministic rules → 0 tokens
         ├─ Type B (25%): batch LLM (10-20 vars/call, free model)
         └─ Type C (10%): individual LLM call, fall back to paid only if free fails validation
```

### Model Strategy

**Use free models for 90%+ of work:**
- **Codebook parsing**: GLM-5 or Kimi K2.5 (both handle structured extraction well)
- **Batch variable cleaning**: GLM-5 (fast, consistent)
- **Fallback for edge cases**: Claude Haiku ($0.25/M tokens) only when free model output fails validation

**Why this works**: Survey cleaning = pattern matching + value mapping. This is exactly what these models are trained for. You're currently paying Claude Sonnet rates for tasks a free model can do.

### Granularity

**Batch 15-20 variables per LLM call**. Here's why:
- Single-call-per-variable = 84 API calls × overhead = expensive
- Batch 20 vars = ~5 calls for Type B/C variables
- Free models have no per-call cost, but batching reduces complexity

### Codebook Management

**Convert once to structured JSON schema**:
```
{
  "variables": {
    "Q2_province": {
      "type": "categorical",
      "values": {"1": "Quebec", "2": "Ontario", ...},
      "missing_codes": [98, 99],
      "target_name": "ses_province"
    }
  }
}
```

This JSON becomes the single source of truth. No re-parsing. Include in system prompt once, cache it.

### Cost Estimate

**Per survey (84 variables)**:
- Codebook parsing: 1 call × ~10K tokens = $0 (free model)
- Type A (55 vars): deterministic = $0
- Type B (21 vars): 2 batch calls × ~5K tokens = $0 (free model)
- Type C (8 vars): 1 batch call × ~3K tokens = $0 (free model)
- Validation failures requiring Claude: ~2-3 vars × $0.01 = $0.03

**Total: ~$0.05-0.10 per survey** (basically free, with safety margin)

Compare to current: $38 → **380x cheaper**

---

## Trade-offs

| Aspect | Pro | Con |
|--------|-----|-----|
| Free models | Near-zero cost, fast | May need validation layer |
| Pattern library | Handles 65% deterministically | Upfront investment to build |
| Batching | Fewer API calls, simpler orchestration | Harder to retry single variables |
| JSON codebook | Parse once, reuse | Requires good initial extraction |

**Risk**: Free models produce 5-10% more errors than Claude. **Mitigation**: Build validation rules (check output types, ranges, required fields). Human review of `clean.py` before deployment catches the rest.

---

## Implementation Sketch

### Week 1: Foundation
1. Create `pattern_library.py` with rules for:
   - Likert scales (1-5 → standard labels)
   - Binary (oui/non, 1/2 → True/False)
   - Demographics (province, age groups, gender)

2. Test free models on 5 variables:
   ```bash
   opencode --model glm-5-free "Clean Q2_province with values {1:Quebec, 2:Ontario...}"
   ```
   Validate output quality.

### Week 2: Pipeline
1. Build `codebook_parser.py`:
   - Input: raw codebook (PDF/TXT/MD)
   - Output: `codebook.json`
   - Use GLM-5 with structured output

2. Build `variable_classifier.py`:
   - Read `codebook.json`
   - Classify each variable as A/B/C
   - Output: `variables_todo.json`

3. Build `batch_cleaner.py`:
   - Process Type B/C in batches of 20
   - Use free model
   - Generate clean.py incrementally

### Week 3: Integration
1. Modify `orchestrator.py` to use new pipeline
2. Add validation layer:
   - Syntax check generated `clean.py`
   - Run on sample data, check output types
   - Flag suspicious mappings for review

3. Test on 3 surveys, measure:
   - Cost (tokens used)
   - Quality (% errors caught in validation)
   - Time

### Success Metrics
- Cost < $1/survey
- Validation catches > 90% of errors
- Full survey processes in < 5 minutes
- Human review takes < 10 minutes

---

## Why Not Other Approaches

**A (API direct)**: You're doing this. $38/survey is unsustainable.

**B (CLI coding agent)**: Task tool overhead kills you. 186K tokens/variable is insane. Agents aren't designed for batch structured work.

**D (No LLM)**: Too brittle. Codebooks vary wildly. You need *some* intelligence to interpret them.

**C (Hybrid) wins** because:
- Pattern library handles the predictable (65%)
- Free LLM handles the judgment calls (35%)
- Total cost approaches zero
- Validation catches edge cases

---

## Final Verdict

**Build the hybrid pipeline with free models.** Your current $38/survey is paying for capabilities you don't need. Survey cleaning is 90% pattern matching—exactly what GLM-5 and Kimi excel at. The upfront investment in pattern rules pays off after 2-3 surveys.

Start with one survey using only free models. If quality is acceptable (and it likely will be), you've solved the problem. If not, you've lost one afternoon—not $38 × 57 surveys.
