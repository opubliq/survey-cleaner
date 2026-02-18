## Critique of Survey Cleaning Proposals

### Consensus Points (Strong Agreement)
All 9 proposals converge on:
1. **Hybrid approach (C/D blend)**: Deterministic rules for standard patterns, LLM for edge cases
2. **Batch, don't iterate**: One call per survey or per 15-20 variables, not per variable
3. **Structured codebook**: Parse once to JSON, reuse
4. **Free models first**: GLM-5/Kimi for 90%+ of work, paid only as fallback

### Proposal-by-Proposal Analysis

| Proposal | Strengths | Weaknesses | Blind Spots |
|----------|-----------|------------|-------------|
| **anth-claude-opus** | Cleanest architecture; <$0.50/survey | Underestimates codebook parsing edge cases | No fallback when JSON extraction fails |
| **anth-claude-sonnet** | Correctly diagnoses caching failure; realistic costs | Still complex to build | None major |
| **google-gemini-2.5-flash** | Comprehensive architecture | Overly optimistic "near zero" costs | Validation layer under-specified |
| **oc-big-pickle** | Simplest: single batch call | Single point of failure; retry is painful | No graceful degradation |
| **oc-glm-5-free** | Aggressive cost reduction | $0.05-0.10/survey is unrealistic | Assumes free models work perfectly |
| **oc-kimi-k2.5-free** | Good state machine; realistic trade-offs | None | None major |
| **oc-minimax-m2.5-free** | Practical classifier structure | $0 cost is fantasy | Free model reliability untested |
| **zai-glm-4.5** | Most conservative/realistic costs ($4-7) | 2-3 week investment is heavy | None |
| **zai-glm-4.7-flash** | Balanced; good implementation sketch | None major | None major |
| **zai-glm-4.7** | Detailed tier breakdown | 2-week upfront is significant | None major |

### Key Disagreements

1. **Upfront investment**: Ranges from 2 days to 3 weeks. I lean toward **1 week**—enough to build core patterns without over-engineering.

2. **Cost estimates**: Range from $0 (unrealistic) to $7 (conservative). **$1-3/survey** is defensible.

3. **LLM for code generation**: Opus says pure deterministic; others want LLM for Type B/C. I lean toward **deterministic templates + LLM fallback**—templates for 70%, LLM for 30%.

### Critical Flaws

- **oc-glm-5-free** and **oc-minimax-m2.5-free**: Claiming $0-0.10/survey ignores validation overhead and retry costs when free models produce malformed JSON.

- **oc-big-pickle**: Single 80-variable batch has no graceful failure mode.

### TOP PICK: anth-claude-sonnet + zai-glm-4.7-flash hybrid

**Why**: Sonnet correctly identifies why your caching failed (dynamic prompts break cache keys) and provides the most honest cost diagnosis. zai-glm-4.7-flash has the best implementation roadmap.

**Winning architecture**:
```
Parse codebook → JSON (GLM-5, 1 call)
     ↓
Classify variables (deterministic regex)
     ↓
├─ Type A (65%): deterministic templates → $0
├─ Type B (25%): batch LLM (10-15 vars) → $0 (free model)
└─ Type C (10%): individual, fallback to Haiku → $0.20
     ↓
Generate clean.py from outputs
```

**Estimated cost**: $0.50-2.00/survey (vs $38 current)
**Investment**: 5-7 days to build pattern library + orchestrator
**Risk mitigation**: Validation layer catches free model errors before writing clean.py
