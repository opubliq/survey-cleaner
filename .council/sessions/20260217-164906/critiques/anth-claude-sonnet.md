---

## Critique of Proposals

### Individual Reviews

**anth-claude-opus (Approach D — Parse Once, Generate Deterministically)**

*Strengths*: Most intellectually honest about what you're actually buying with LLM calls. The "parse once, generate deterministically" framing is clean. Correctly identifies that the JSON schema becomes a reusable, hand-editable artifact — that's a real operational win. Cost projection is credible.

*Weaknesses*: Underestimates the variance in codebook quality. "The information is explicitly stated" is optimistic — survey codebooks are notoriously inconsistent. Template building for 6-8 types in 3 days is realistic, but the proposal sidesteps what happens when variables straddle multiple types or have custom naming conventions.

*Blind spots*: No discussion of what happens when Phase 1 extraction fails (5-15% of real surveys). The validation step is mentioned but not architected. Also quietly assumes codebook-to-clean.py is a 1:1 mapping, which isn't always true (derived variables, scale scores).

---

**anth-claude-sonnet (Approach D+C hybrid)**

*Strengths*: The caching failure diagnosis is the most technically precise of any proposal — identifying that prompts built with variable-specific context injected *before* the codebook would break the cache key is actionable. The 5-day implementation sketch is realistic and phased correctly.

*Weaknesses*: The cost estimate ($0.13-0.50) assumes >60% Type A classification, which needs empirical validation. The proposal says "fix the caching" but doesn't fully commit to the architectural implication: if caching actually works, does that change the recommendation? It's a bit hedged.

*Blind spots*: The explanation for *why* the $38 caching attempt failed is stated confidently but is speculative without seeing the actual orchestrator code. Could be right, could be wrong.

---

**google-gemini-2.5-flash (Approach C)**

*Strengths*: Most thorough on implementation sketch. Correctly notes that free model quality for Type B/C is the key unknown.

*Weaknesses*: The cost estimate is **fatally naive** — claiming near-zero cost by assuming free models handle everything, then estimating the codebook parsing at "$0.03" using Sonnet at "$3/M tokens" is a math error. 10K tokens × $3/M = $0.03, technically correct, but the proposal then says "near zero" as if that's the dominant cost, ignoring the actual LLM call costs for Type B/C in early iterations before the pattern library matures.

*Blind spots*: Doesn't grapple with free model reliability. GLM-5 producing malformed JSON 15% of the time requires retry logic that isn't budgeted.

**Critical flaw**: The near-$0 cost claim depends entirely on free models working reliably for Type B/C. No empirical basis provided. This could be true, could be false — but presenting it as settled is misleading.

---

**oc-big-pickle (Approach C, simplified — single batch call)**

*Strengths*: The simplest possible implementation. "1 API call for the whole survey" is a genuine insight that gets lost in over-engineered proposals. The honest acknowledgment that GLM-5 < Claude for edge cases is refreshing.

*Weaknesses*: Sending 80 variables in a single call to a free model and trusting the output is brittle. What does the retry strategy look like when the model returns partial JSON? The proposal sketches a retry on sub-batches but doesn't architect it. Also, cost table shows "$0.50" total but the model is free — where does the $0.50 come from?

*Blind spots*: Validation is listed as "human_validate.py — review interactif," which contradicts the autonomy requirement. If a human must review 80 transformations per survey × 57 surveys, you've just created a different bottleneck.

---

**oc-glm-5-free (Approach C with free models)**

*Strengths*: The "380x cheaper" framing is honest math. The success metrics are concrete and testable. The "why not other approaches" section is the clearest comparative reasoning in any proposal.

*Weaknesses*: Cost estimate of "$0.05-0.10/survey" is almost certainly too optimistic — it assumes free models work on first try with acceptable quality. Real-world error rates on structured JSON generation from mid-tier models are 10-20%, which means retry costs and occasional Claude fallback costs that aren't priced in.

*Blind spots*: Pattern library "Week 1" — building rule coverage for Likert, binary, demographics in a week is doable, but the proposal doesn't account for the time to validate those rules against real survey data.

---

**oc-kimi-k2.5-free (Approach C)**

*Strengths*: The state machine for autonomy (`status.json`) is a practical implementation detail that most proposals skip. The fallback chain (GLM-5 → Claude Haiku, not Sonnet) is sensible. Realistic about "learning curve" in early surveys.

*Weaknesses*: "$2-4/survey" estimate is more conservative than peers but still lacks sensitivity analysis. What if the classifier misidentifies 30% of Type A variables?

*Blind spots*: Embeddings suggestion for codebook matching is unnecessary complexity for this use case. Sentence-transformers setup cost vs. benefit isn't justified.

---

**oc-minimax-m2.5-free (Approach C)**

*Strengths*: "The cost becomes development time, not tokens" is the most honest reframing of the problem. Good directory structure sketch.

*Weaknesses*: Thinnest proposal of the set. The implementation sketch is too high-level to be actionable. Missing code for calling GLM-5 (beyond a placeholder client).

---

**zai-glm-4.5 (Approach C, 2-3 week build)**

*Strengths*: The 3-week phased implementation is the most realistic timeline estimate.

*Weaknesses*: "$4-7/survey" estimate is higher than peers without clear justification. Recommends Claude Sonnet for Tier 3 (quality-critical) while other proposals successfully argue Haiku is sufficient — this deserves more argument.

---

**zai-glm-4.7-flash (Approach C+D hybrid)**

*Strengths*: The "pattern library compounds" observation is important and often missed. "$85-114 for 57 surveys" total framing is useful.

*Weaknesses*: Province mapping in the pattern library contains an error (ON appears twice: index 2 and 7). Suggests GLM-4.7 at "$0.005 per variable" — but GLM-4.7 is listed as a free model. Cost attribution is confused.

---

**zai-glm-4.7 (Approach C, 3-tier)**

*Strengths*: The most complete technical proposal. Pattern library signature matching against data statistics (min, max, unique, distribution shape) is the right implementation approach — it doesn't rely solely on codebook text parsing. The implementation sketch is the most production-ready of the set.

*Weaknesses*: "2 week upfront investment" is probably 3-4 weeks for a small team doing this alongside other work. The 50%/30%/20% tier split is stated without empirical basis.

---

### Consensus Points

All 9 proposals agree on:

1. **Approach C (Hybrid) is the answer** — no proposal defends the current approach
2. **One LLM call per variable is the root cause of $38 cost**, not model choice per se
3. **Codebook → structured JSON is step 1**, not Markdown injection
4. **Free models (GLM-5, Kimi) are worth testing** for structured extraction tasks
5. **Batch processing** (10-20 vars per call) is better than individual calls
6. **Cost target: $0.50-$4/survey** is achievable

### Key Disagreements

**Disagreement 1: Approach D (deterministic only) vs. C (hybrid)**
- Opus argues "just use rules + templates, LLM only for codebook parsing"
- Everyone else says you need LLM for variable-level decisions

**My lean**: Sonnet's diagnosis is right — "the codebook already contains most of the information." But Opus oversimplifies. The real problem isn't that you need LLM judgment per variable; it's that you're paying Sonnet rates for judgment that free models can provide. The hybrid C is correct, but D is worth attempting first on a single survey as a lower bound on cost.

**Disagreement 2: $0/survey vs. $1-4/survey**
- Gemini, Minimax, GLM-5 claim near-zero cost with free models
- GLM-4.7, Kimi, GLM-4.5 estimate $1-4/survey

**My lean**: The $1-4 range is more honest. Free model reliability on structured JSON output has real failure rates. Budget for 15-20% retries.

---

### Critical Flag

**google-gemini-2.5-flash**: The near-$0 cost claim for a production pipeline with no empirical validation of free model JSON reliability is a critical flaw. Presenting this as a cost estimate rather than a best-case scenario could lead to building without a fallback budget.

---

### Top Pick: **zai-glm-4.7**

Reason: It's the only proposal that uses **data-driven pattern matching** (min, max, unique count, distribution shape) rather than relying purely on codebook text parsing. This is architecturally superior because:

1. Pattern library enriches from data, not just documentation — survives bad codebooks
2. The 3-tier routing logic is the most implementable sketch
3. "$1-2/survey" estimate includes failure modes
4. The compound benefit observation ("each survey makes the next cheaper") is the correct long-term framing

**One modification**: Replace Claude Sonnet in Tier 3 with Claude Haiku. Sonnet is overkill for well-defined edge cases where you have structured codebook JSON available. This brings Tier 3 cost down by ~4x.

**Immediate action**: Don't build all of this at once. Take one survey, manually inspect 84 variables, classify them into A/B/C by hand, and see what the real distribution is. Every proposal assumes 50-70% Type A — verify that before building the classifier.
