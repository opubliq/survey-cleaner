## Summary
Your current approach costs $38/survey with 84 variables—unscalable. The solution: **Hybrid deterministic rules + LLM** (Option C) with a bootstrap JSON extraction (Option D), using GLM-4.7 at $0.01-0.05 per variable processed.

## Recommendation

**Hybrid deterministic rules + LLM** with a bootstrap pattern extraction system.

**Why:** You have 65-70% variables with standard patterns (Likert, binary, demographics) that should cost $0 using rules, while 30-35% are non-standard and require LLM judgment. This is realistic, maintainable, and reduces cost by ~85%.

## Architecture

```
[BOOTSTRAP - one-time per survey, ~500 tokens]
└─ Parse codebook → JSON schema (variable types, patterns, missing codes)

[VARIABLE PROCESSING LOOP - deterministic + selective LLM]
├─ Variable → Check pattern library
│   ├─ Match → Apply rule (0 tokens) 
│   │   ├─ Likert: normalize scale, map missing codes
│   │   ├─ Binary: 0/1, detect alternatives
│   │   └─ Demographics: standard names (province, age group)
│   └─ No match → Call LLM with pattern suggestions (10-20 vars/batch)
│       ├─ Generate transformations
│       └─ Update pattern library (learn for next time)
│
[GENERATE clean.py - deterministic Python code]
└─ Write clean.py with all transformations
```

**Key components:**
- `pattern_library.json`: Stores discovered patterns (auto-populated)
- `codebook_parser.py`: LLM extracts structure (one-time)
- `cleaner.py`: Main orchestrator (deterministic + selective LLM)
- `generator.py`: Creates clean.py

## Model & Strategy

**Primary model:** **GLM-4.7** (via z.ai or opencode zen)
- Cost: ~$0.005 per variable call (batch 10 vars = $0.05)
- Sufficient for pattern detection + naming
- Cheaper than Claude Sonnet but better than cheap models

**Fallback:** Claude Sonnet for edge cases where GLM-4.7 struggles

**Granularity:** Batch 10-20 variables per LLM call (saves context tokens vs 1 per variable)

## Codebook Management

**JSON schema extraction (bootstrap):**
```json
{
  "survey_id": "abc123",
  "variables": [
    {
      "name": "Q2_province",
      "type": "categorical",
      "pattern": "province_codes",
      "values": {"1": "qc", "2": "on", "3": "bc"},
      "missing_codes": ["98", "99"],
      "standard_name": "province"
    },
    {
      "name": "Q7_age",
      "type": "ordinal",
      "pattern": "likert",
      "scale": 5,
      "values": {"1": "15-24", "2": "25-34", ...}
    }
  ]
}
```

**Processing:** Use this JSON schema as the source of truth, not prompts.

## Estimated Costs

**Per survey (84 variables):**
- Variables with patterns (70% = 59 vars): **$0** (rules only)
- Variables needing LLM (30% = 25 vars, batched 10-15 per call): **~$1.25**
- Bootstrap parsing: **$0.25**
- **Total: $1.50-2.00 per survey**

**For 57 surveys: $85-114** (down from ~$2,166)

## Trade-offs

**Pros:**
- 90% cost reduction
- Scalable to hundreds of surveys
- Pattern library grows with usage
- Human intervention only for edge cases

**Cons:**
- Pattern library maintenance required
- Bootstrap step adds complexity
- Learning curve for new patterns
- Less flexible than pure agent approach

**Reality check:** Pattern library is worth it because you'll encounter the same variable types repeatedly (demographics, Likert scales, yes/no questions). This is a known problem domain, not exploratory AI.

## Implementation Sketch

**Phase 1 (2-3 days):**
1. Build `pattern_library.json` structure
2. Implement bootstrap parser using GLM-4.7
3. Create deterministic rule library (Likert, binary, demographics)

**Phase 2 (1-2 days):**
4. Build `cleaner.py` with variable loop
5. Add selective LLM batching (10-20 vars)
6. Integrate pattern library updates

**Phase 3 (1 day):**
7. Build `generator.py` for clean.py
8. Test on 5 surveys, adjust patterns
9. Deploy to remaining 52 surveys

**Milestones:** Pattern library will reach 80% coverage in 10 surveys, then compounds.

---

**Defensible choice:** This isn't "going all-in on AI." It's using AI for what it's good at (pattern detection, naming) while automating everything else. The math is clear: $2/survey is sustainable, $38/survey is not.
