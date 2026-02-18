# Survey Cleaning System Recommendation

## Summary

**Recommendation**: Approach C (Hybrid rules + LLM) with a lightweight 3-tier model strategy. Build a simple pattern library (1-2 weeks), use free GLM-5 to classify/process 80% of variables deterministically, use Claude Sonnet only for 20% complex cases. Target: **$1-3/survey** vs current $38.

**Why**: Your data follows predictable patterns (Likert, binary, demographics) that can be recognized programmatically. The expensive "LLM decides everything" approach is overkill. The CLI agent (Approach B) has fatal overhead, and pure deterministic (Approach D) lacks flexibility for edge cases.

## Recommendation

### Core Architecture: 3-Tier Model Strategy

```
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (Python script)                               │
│  - Routes variables to appropriate tier                      │
│  - Writes clean.py incrementally                             │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   Tier 1 (Free)        Tier 2 (Free)         Tier 3 (Paid)
   ~50% variables       ~30% variables        ~20% variables
   Standard patterns    Semi-standard         Complex/ambiguous
   Deterministic        LLM: GLM-5            LLM: Claude Sonnet
   $0                   Batch 10-20 vars      Individual calls
```

**Tier 1: Pattern Matching (Free, ~50%)**
- Detect: Likert 5-point, binary yes/no, standard demographics
- Examples: `Q1 = 1-5` → `agreement_scale = "strongly disagree"-"strongly agree"`
- Codebook not even needed - infer from data distribution + pattern library
- Zero tokens, deterministic

**Tier 2: Free Model LLM (Free, ~30%)**
- Semi-standard patterns that need LLM judgment
- Batch 10-20 variables per prompt
- Use GLM-5 (free via opencode): good enough for "what does 97 mean?"
- Example batch: "Transform these 15 demographic variables..."

**Tier 3: Premium Model (~20%)**
- Complex/ambiguous variables, incomplete codebook
- Individual calls to Claude Sonnet
- Use prompt caching: cache codebook once, reuse for each variable
- Most expensive but justifiable for difficult cases

### Pattern Library (Minimal Viable)

```json
{
  "patterns": {
    "likert_5": {
      "signature": "min=1, max=5, unique=5, mode≈3",
      "transform": "agreement_scale",
      "mapping": "1:strongly_disagree, 2:disagree, 3:neutral, 4:agree, 5:strongly_agree",
      "missing_codes": "[98, 99, -9]"
    },
    "yes_no": {
      "signature": "min=0, max=1, unique=2 OR values in [1,2]",
      "transform": "binary_response",
      "mapping": "0/1:no/yes OR 1:yes, 2:no",
      "infer_from_codebook": "true"
    },
    "province_canada": {
      "signature": "min=1, max=13, unique≤13",
      "transform": "province_code",
      "mapping": "1:qc, 2:on, 3:bc, 4:ab, 5:sk, 6:mb, 7:on, 8:qc, 9:nb, 10:ns, 11:pe, 12:nl, 13:yt",
      "ambiguity": "check_codebook"
    }
  }
}
```

**Key insight**: Start with 5-10 patterns. After processing 5-10 surveys, the pattern library will capture 80%+ of your variables.

## Trade-offs

**Pros:**
- **90% cost reduction**: $1-3/survey vs $38
- **Autonomy**: Fully automated after pattern library bootstrap
- **Quality**: LLM used where judgment needed, deterministic where not
- **Scalability**: Patterns compound - each survey makes the next cheaper
- **Simplicity**: Single Python orchestrator, no complex infrastructure

**Cons:**
- **2-week upfront investment**: Building pattern library + tier routing logic
- **Pattern maintenance**: Must add new patterns occasionally (5-10/year)
- **Quality risk on Tier 1**: Deterministic rules may miss edge cases (mitigation: sampling validation)
- **Model dependency**: Free models via opencode may change/disappear (mitigation: easy switch to Haiku)

## Implementation Sketch

### Phase 1: Bootstrap Pattern Library (Week 1)
```python
# 1. Manual analysis of 3 existing surveys
python build_pattern_library.py --survey-id s001,s002,s003 --output patterns/

# 2. Define Tier 1 signatures (data-driven)
# - Likert: min=1, max=5, unique=5, distribution=bell curve
# - Binary: unique=2, values=[0,1] OR [1,2]
# - Province: min=1, max=13, unique≤13

# 3. Write deterministic transforms for 5-10 patterns
# - No LLM needed here
```

### Phase 2: Orchestrator with 3-Tier Routing (Week 1-2)
```python
class SurveyCleaner:
    def clean_survey(self, survey_id):
        variables = self.extract_variables(survey_id)
        
        for var in variables:
            # Tier 1: Pattern match
            pattern = self.match_pattern(var)
            if pattern:
                transform = self.apply_pattern(var, pattern)  # $0
                self.write_clean_code(transform)
                continue
            
            # Tier 2: Semi-standard (batch)
            if var in self.semi_standard_batch:
                transforms = self.call_free_llm(batch, model="GLM-5")  # Free
                self.write_clean_codes(transforms)
                continue
            
            # Tier 3: Complex (individual)
            transform = self.call_claude_sonnet(var, cache_codebook=True)  # $
            self.write_clean_code(transform)
    
    def match_pattern(self, var):
        # Data-driven signature matching
        stats = self.compute_stats(var)  # min, max, unique, distribution
        for pattern in self.pattern_library:
            if self.signature_matches(stats, pattern["signature"]):
                return pattern
        return None
```

### Phase 3: Batch Processing for Tier 2 (Week 2)
```python
def process_tier2_batch(variables, codebook):
    prompt = f"""
    Transform these {len(variables)} semi-standard variables.
    Codebook context: {extract_relevant_codebook_snippets(variables, codebook)}
    
    Output JSON with: new_name, mapping, missing_codes, notes
    """
    return call_free_llm(prompt, model="GLM-5")
```

### Phase 4: Validation & Iteration (Ongoing)
```python
# After processing each survey:
python validate_cleaning.py --survey-id s010 --sample-rate 10%

# This outputs:
# - Variables with low confidence
# - Potential pattern additions
# - Error rate estimate
```

## Cost Estimate

**Per survey (84 variables, typical distribution):**

| Tier | Variables | Cost | Notes |
|------|-----------|------|-------|
| Tier 1 (Pattern) | 42 (50%) | $0 | Deterministic |
| Tier 2 (GLM-5 batch) | 25 (30%) | $0 | Free via opencode, 3 batch calls |
| Tier 3 (Claude Sonnet) | 17 (20%) | $1-2 | With prompt caching, individual calls |
| **Total** | **84** | **$1-2** | vs current $38 |

**Validation assumption**: 5% error rate on Tier 1 (2 variables), acceptable per your constraints.

## Final Recommendation

**Go with Approach C + 3-Tier Strategy**. It's the only approach that:
1. Addresses your cost constraint (90% reduction)
2. Maintains autonomy (automated after 2-week investment)
3. Delivers quality (LLM judgment where needed)
4. Scales with your growing survey corpus (patterns compound)
5. Fits your small team (simple architecture, minimal maintenance)

**Immediate next steps:**
1. Pick 3 existing surveys, manually identify patterns
2. Build pattern library with 5-10 deterministic rules
3. Implement simple tier routing in orchestrator
4. Test on 1 survey, measure cost/quality
5. Iterate: add patterns, refine routing

**Risk mitigation**: Start with Approach A (API direct) as the underlying mechanism - it gives you full control to implement the 3-tier strategy cleanly without fighting agent overhead.
