# Architecture Review: Survey Cleaner Pipeline

## Individual Critiques

### google-gemini-2.5-flash

**Strengths:** Comprehensive implementation sketches, clear trade-off analysis, good prioritization of validation. Strong focus on immediate activation of existing components.

**Weaknesses:** Over-recommends LLM usage (classification + validation). Two LLM calls per borderline variable adds latency and complexity for marginal gain.

**Blind Spot:** Underestimates the cost of "validation after each variable" — with 500-2000 variables, this adds significant overhead vs. one final validation pass.

---

### oc-big-pickle

**Strengths:** Most pragmatic prioritization table. Correctly identifies integration debt as the real issue. Code examples are concrete and actionable.

**Weaknesses:** Lowering Tier 1 threshold to 0.85 contradicts the goal of maximizing Tier 1 — this sends *more* variables to Tier 2, not fewer.

**Blind Spot:** The `create_batches()` function groups by *similarity*, not just count. The proposal glosses over whether similarity-based batching helps or hurts GLM-5 performance.

---

### oc-kimi-k2.5-free

**Strengths:** Sharpest analysis of the actual problem (sequential processing prevents batching). Circuit-breaker escalation is well-designed. Correctly prioritizes connecting validation over optimizing patterns.

**Weaknesses:** Two-pass architecture adds complexity without clear benefit — you can batch within a single pass. Postponing the battue indefinitely means flying blind on pattern performance.

**Blind Spot:** Underestimates value of empirical pattern validation. "Wait for 10 surveys" means 2-4 weeks of uncertain classification quality.

---

### oc-minimax-m2.5-free

**Strengths:** Best risk assessment (audit-first approach). Realistic time estimates. "Max 1 escalation" rule prevents escalation loops elegantly.

**Weaknesses:** 100 variables may be insufficient for statistical confidence on pattern performance. "Max 1 escalation" means Tier 2 failures go straight to manual review, bypassing Tier 3.

**Blind Spot:** CSV annotation tool is naive — 100 variables with manual classification will take 2-3 hours, not 1, given context switching between codebook labels and value mappings.

---

## Consensus Points

1. **Naming:** All four agree on Option C (codebook labels for Tier 1). This is a clear, no-regrets improvement.

2. **Escalation:** All agree on automatic escalation. All set max attempts to 2-3.

3. **Validation timing:** Three of four prefer end-of-pipeline validation vs. per-variable (only Gemini disagrees).

4. **Tier 1 threshold:** All recommend keeping it at 0.8-0.85 (not increasing to 0.9).

---

## Key Disagreements

| Issue | Options | My Lean |
|-------|---------|---------|
| **Orchestrator** | Two-pass (Kimi) vs Accumulator (others) | **Accumulator (Option B)** — simpler, achieves same batching |
| **LLM in classification** | Yes (Gemini) vs Audit-first (Minimax) vs No (Kimi/Big-Pickle) | **Audit-first (Option C)** — data before complexity |
| **Battue scope** | 500 vars (Gemini/Big-Pickle) vs 100 (Minimax) vs postpone (Kimi) | **100 vars (Minimax)** — sufficient for directional data |
| **LLM in validation** | Yes (Gemini) vs No-first (others) | **No-first** — connect existing validator before adding LLM |

---

## Critical Flaws

**Gemini's "validation after each variable"** is a critical flaw for performance. With 1000 variables and 50ms validation time, that's 50 seconds of overhead vs. one 50ms pass at the end. Validation should catch inter-variable conflicts (duplicate names) which requires the full context anyway.

---

## TOP PICK: Hybrid of Big-Pickle + Minimax

**Orchestrator:** Option B (accumulator with flush) — minimal change, activates existing `batcher.py`

**Classification:** Option C (audit first) — log 100 variables, manually classify, decide on LLM assistance only if error rate >15%

**Battue:** 100 variables, 1 day, target ≥40% Tier 1 rate (sufficient given GLM-5 is free)

**Naming:** Option C (codebook labels) — immediate implementation

**Validation:** Connect existing validator after assembly, non-LLM first. Add LLM-light only if >20% Tier 1 failures.

**Escalation:** Automatic with max 2 attempts (Tier 1→2→3), pass validation reason + failed code to next tier.

**Priority:** (1) Connect validation, (2) Activate batching, (3) Naming fix, (4) Battue, (5) Escalation, (6) Classification audit.

This balances pragmatism (Big-Pickle's prioritization) with empirical discipline (Minimax's audit-first approach) while avoiding premature LLM complexity.
