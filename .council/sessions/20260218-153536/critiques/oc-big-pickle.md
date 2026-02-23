# Architectural Critique: Survey Cleaner Pipeline

## Consensus Points

All four proposals agree on:
1. **True batching for Tier 2 is essential** — current sequential 1-var-at-a-time is wasteful
2. **Classification should remain deterministic** — no LLM in the critical path for tier assignment
3. **Validation must be connected** — the validator exists but isn't used; this is critical debt
4. **Automatic escalation is needed** — tier fallback on validation failure
5. **Variable naming should use codebook labels** — current `op_q15_m2_eval_gvt` is unreadable

## Key Disagreements

### Q1: Orchestrator Structure
- **Option A (two-pass)**: kimI and big-pickle favor explicit two-pass: classify all → group by tier → process
- **Option B (accumulator)**: google and minimax prefer in-loop buffer that flushes at N=15
- **My lean**: **Option A** is cleaner and more testable. The "accumulator" approach is functionally equivalent but mixes classification and processing phases awkwardly. Two-pass makes batching explicit and state between phases clear.

### Q3: Battue on 500 Variables
- **Do it now**: google (prioritizes as #1 after fixing batching/validation), big-pickle
- **Wait**: kimi wants to wait for real metrics from 5-10 surveys; minimax suggests 100 vars, not 500
- **My lean**: **100 vars (minimax) is sufficient** for first calibration. 500 is overkill. But waiting is wrong — you need baseline data before optimizing.

### Q6: Escalation & Threshold
- **Keep 0.8**: kimi, minimax — escalation handles false positives
- **Bump to 0.85**: google, big-pickle — reduce incoming failures
- **My lean**: **Bump to 0.85** — cheaper than managing escalation overhead. But max 2 attempts (not 3), as minimax correctly notes.

### Q5: Validation Integration
- **Per-variable**: google — immediate feedback
- **End-of-pipeline**: kimi, minimax — more efficient, catches inter-variable conflicts
- **My lean**: **End-of-pipeline** is correct. Dynamic validation (ranges, types) needs full DataFrame context. Per-variable validation adds latency with minimal benefit.

## Critical Flaws in Proposals

### Flaw 1: No fallback when codebook labels are missing
**Every proposal recommends Option C for naming (use codebook label) but ignores the fallback case.** The codebook may not have labels for all variables. The naming logic must handle this gracefully.

### Flaw 2: Conflicting priority orders
- google: Q1 → Q2 → Q3 → Q4 → Q5 → Q6
- big-pickle: Q1 → Q5 → Q3 → Q4 → Q6
- kimi: **Q5 → Q1 → Q6 → Q4 → Q3**
- minimax: Q5 → Q1 → Q3 → Q4 → Q6

**kimi correctly prioritizes validation (Q5) first** — this is the critical integration gap. Most proposals put it later, but an unvalidated pipeline is dangerous regardless of how well-tiered the classification is.

### Flaw 3: Underestimating Q3 effort
minimax says 1 day for 100 vars. Realistically: 30 min to extract data + 2-3 hours manual annotation + 1-2 hours analysis = **1 work day minimum**. Not a "quick check."

---

## Proposal Strengths & Weaknesses

| Proposal | Strengths | Weaknesses |
|----------|-----------|------------|
| **google-gemini-2.5-flash** | Comprehensive; good implementation sketches; LLM-light for Tier 1 validation is smart | Over-engineers Q2 (adds LLM to classification); 500 vars battue is excessive; priority order puts Q3 before Q5 |
| **oc-big-pickle** | Clear priority with time estimates; good two-pass structure; correct emphasis on connecting existing code | "Lower threshold to 0.85" contradicts "keep classification deterministic"; vague Q3 implementation; Q5 per-variable validation is wrong approach |
| **oc-kimi-k2.5-free** | **Correctly prioritizes Q5 first**; two-pass is clean; good circuit-breaker logic; conservative on unnecessary complexity | Two-pass may be overkill vs simple accumulator; Q3 "wait" is wrong direction; threshold advice inconsistent |
| **oc-minimax-m2.5-free** | Most pragmatic; 100 vars is right size; clear time estimates; good threshold (40% Tier 1) | Incomplete code sketch for Q1; "max 1 escalation" is too restrictive; vague on escalation context transmission |

---

## My TOP PICK: **oc-kimi-k2.5-free** (with modifications)

### Why
1. **Correct priority order**: Validation connection (Q5) first — this is the highest-impact gap
2. **Two-pass structure** is cleaner than accumulator buffer for maintainability
3. **Conservative on complexity**: Doesn't add LLM where deterministic solutions exist
4. **Circuit-breaker logic**: Max 2 attempts is appropriate

### Required Modifications
1. **Q1**: Add explicit batching in second pass using `create_batches()` — not just "group by tier"
2. **Q3**: Do NOT wait — run 100-var battue in parallel with Q5 integration (get baseline data early)
3. **Q4**: Add fallback to raw name when codebook label is missing
4. **Q6**: Bump threshold to 0.85 (not keep at 0.8); allow max 2 escalations (T1→T2→T3)

### Recommended Priority Order
1. **Week 1**: Connect validation non-LLM to orchestrator (Q5)
2. **Week 1**: Restructure orchestrator with two-pass + true batching (Q1)
3. **Week 2**: Implement escalation with circuit-breaker (Q6)
4. **Week 2**: Fix naming with label-based + fallback (Q4)
5. **Week 3**: Run 100-var battue, calibrate patterns if Tier 1 < 50% (Q3)
6. **Ongoing**: Audit 5% of Tier 1 decisions periodically (Q2 Option C)
