# Critique: Pattern Engine Architecture Proposals

## Consensus Points

All 8 proposals converge on **three key architectural decisions**:

1. **Option C (Hybrid)** for pattern modeling: Python classes with `to_pattern()` method for JSON serialization
2. **Option C (both inputs)** for classifier: accept `series` + `var` with graceful degradation
3. **Option C (explicit detection)** for missing codes: preprocessing step before classification

This near-unanimity suggests these are the correct defaults for this problem.

## Individual Analysis

### Strengths

- **oc-big-pickle**: Best trade-off table, clearest reasoning for small team. The missing code integration sketch is production-ready.
- **oc-glm-5-free**: Clean code examples, fast-path optimization when codebook is trustworthy.
- **zai-glm-4.7-flash**: Most detailed implementation sketch with concrete threshold recommendations (≤5 = 1.0, ≤7 = 0.7).

### Weaknesses / Blind Spots

- **google-gemini-2.5-flash**: Implementation sketch is too abstract, no concrete threshold values for Tier 1.
- **oc-kimi-k2.5-free**: The `MissingCodeDetector` warning logic (flag if >5% responses) is a good idea but not implemented.
- **oc-minimax-m2.5-free**: Contradicts consensus on Q1—puts detection in **matcher**, not pattern. This fragments logic and makes patterns harder to test.
- **zai-glm-4.7**: Recommends Option A for Q1 despite everyone else choosing C. No explanation for diverging from consensus.

### Critical Flaw

**zai-glm-4.7** has a critical inconsistency: recommends Option A (OOP only) for Q1, but acknowledges serialization is needed. This creates the exact "class vs data" problem Option C solves. Without `to_pattern()`, the `pattern_library.json` requirement becomes impossible.

## Key Disagreements

| Topic | Positions | My Lean |
|-------|-----------|---------|
| Detection logic location | Most: in pattern class; oc-minimax: in matcher | **In pattern** - keeps logic co-located with definition |
| Classifier priority | Series-first vs Schema-first | **Schema-first if reliable** - semantic info is higher signal when available |
| Missing code threshold | n_unique ≤ 5 vs ≤ 7 | **≤7 with confidence scoring** (zai-glm-4.7-flash) - more realistic |

## TOP PICK: **oc-big-pickle**

**Why:**

1. **Best structured trade-off analysis** — the comparison table makes decisions explicit for team discussion
2. **Complete Q3 solution** — integrates missing code detection directly into classifier flow with `effective_series` + `MissingCodeInfo`
3. **Defensive design philosophy** — "Le parser échoue → on utilise stats seulement" captures the reality of imperfect codebooks
4. **Actionable implementation sketch** — prioritized steps (1→2→3) with clear file locations

The proposal explicitly addresses the "small team" context throughout, which aligns with the stated constraint. It also correctly places detection logic **in the pattern** (opposing oc-minimax), maintaining SRP.

### Minor Improvements I'd Add

1. Add confidence threshold for Tier 1 (e.g., >0.8) — currently only implied
2. Specify what happens when both inputs contradict (e.g., var says "likert" but n_unique=50)
3. Consider a "confidence boost" when both sources agree

## Honorable Mention

**oc-glm-5-free** is a close second and would be equally valid. Its strength is the fast-path optimization: if codebook confirms scale_type, skip statistical analysis entirely. This is worth adopting regardless of which proposal is chosen.
