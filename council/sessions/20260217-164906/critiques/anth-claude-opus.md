# Critique of Survey Cleaning Architecture Proposals

Let me read through all seven proposals and provide my assessment.

## Consensus Points

All proposals converge on several key ideas:

1. **One-time codebook parsing to structured JSON** — every single proposal recommends this. It's clearly the right move.
2. **Batch processing over per-variable calls** — unanimous rejection of the 84-call-per-survey pattern that caused the $38 bill.
3. **Free/cheap models are sufficient** — everyone agrees survey cleaning is structured extraction, not creative reasoning.
4. **Deterministic rules for common patterns** — at least partial agreement on a pattern library.
5. **Jinja2/template-based code generation** — several proposals converge on this for the deterministic layer.

These consensus points are strong. When seven independent proposals agree, that's signal.

## Per-Proposal Assessment

### anth-claude-opus (Approach D: Parse Once, Generate Deterministically)

**Strengths:** Cleanest architecture. The "JSON schema as single source of truth" insight is powerful — hand-editing the JSON to fix LLM errors and regenerating `clean.py` instantly is an underrated advantage. The 4-day implementation sketch is realistic and well-sequenced.

**Weaknesses:** Underestimates the variability of codebook formats. The claim that Phase 1 extraction works in "one prompt, one response" assumes codebooks are well-structured. Real codebooks are messy PDFs with inconsistent formatting. Also, the template approach breaks when a variable doesn't fit any known type — what then?

**Blind spots:** No fallback for when the JSON extraction is wrong. Validation catches errors but doesn't fix them automatically.

### anth-claude-sonnet (Approach D-first with C fallback)

**Strengths:** Best diagnosis of *why* the caching failed (dynamic prefix invalidating cache keys). The tiered cost breakdown is the most rigorous. Correctly identifies Haiku over Sonnet — nobody needs Sonnet for this workload.

**Weaknesses:** The 5-day implementation sketch is nearly identical to Opus but adds a classifier layer that may be premature optimization. If 60% of variables are truly Type A, you'd discover that *after* building the templates, not before.

**Blind spots:** Doesn't address what happens when the codebook is a PDF with tables rendered as images.

### google-gemini-2.5-flash (Approach C)

**Strengths:** Most thorough on the classification logic and the concept of a growing pattern library.

**Weaknesses:** Verbose and repetitive. The implementation sketch is vague — "create `codebook_parser.py`" isn't a plan, it's a filename. The cost estimate is suspiciously optimistic ("near zero") because it assumes free models work perfectly. **Critical flaw:** handwaves quality risk with "iteratively improved through prompt engineering" — that's not a mitigation, that's a hope.

### oc-big-pickle (Batch with free model)

**Strengths:** Pragmatic and direct. The "one API call for the whole survey" insight is the simplest possible architecture. The LiteLLM integration suggestion is practical.

**Weaknesses:** Sending 80 variables in a single LLM call is risky — output quality degrades with prompt length, and a single failure means retrying everything. The proposal acknowledges this but the mitigation ("retry on sub-batches") reintroduces the complexity it was trying to avoid.

**Blind spots:** No pattern library, no deterministic rules. This is Approach A with a cheaper model, not Approach C. It'll work but leaves optimization on the table.

### oc-glm-5-free (Hybrid C with free models)

**Strengths:** Best cost estimate ($0.05-0.10/survey) and clearest success metrics. The "start with one survey using only free models" advice is the right first step.

**Weaknesses:** The 3-week implementation timeline contradicts the "simplicity" constraint. Pattern library building is presented as straightforward but is the hardest part of the whole system.

**Blind spots:** Assumes free models produce only 5-10% more errors. This needs to be validated, not assumed.

### oc-kimi-k2.5-free (Hybrid C)

**Strengths:** The `status.json` state machine for resumability is a genuinely useful idea nobody else mentioned. Good risk/timeline framing.

**Weaknesses:** The pattern library example hardcodes province mappings — but these change per survey (different codebooks use different codes for the same provinces). This reveals a misunderstanding of the problem: patterns are about *structure*, not *values*.

### zai-glm-4.5, zai-glm-4.7-flash, zai-glm-4.7

These three are similar enough to critique together. They all propose Approach C with varying levels of detail. GLM-4.7's 3-tier routing is well-articulated but adds complexity. GLM-4.5 is the weakest — highest cost estimate ($4-7/survey) and longest timeline (3 weeks). GLM-4.7-flash has the best "pattern library grows with usage" framing.

**Shared blind spot:** All three overestimate how long the pattern library takes to build. The first 5-10 patterns cover 80% of cases; the long tail matters less.

## Key Disagreements

1. **One giant call vs. batched calls:** Big-Pickle says one call for 80 variables; everyone else says batch 10-20. **I lean toward batches of 15-20.** One call is fragile and hard to debug.

2. **How much deterministic rules matter:** Opus says templates handle everything after JSON extraction; Sonnet/Gemini/others say you need a classifier. **I lean toward Opus's simpler approach** — start with templates, add classification only if needed.

3. **Free models vs. Haiku fallback:** Most say free-first with Haiku fallback. Opus says Sonnet for extraction if needed. **Free-first is correct.** Test GLM-5/Kimi first; escalate only on measured failure.

## Top Pick

**anth-claude-opus**, with two modifications stolen from other proposals:

1. Add **Kimi/oc-kimi's `status.json` resumability** — essential for autonomy.
2. Add **Sonnet's diagnosis of why caching failed** — important institutional knowledge.

Opus wins because it's the simplest architecture that could work. One LLM call to parse the codebook into JSON, then pure deterministic generation. No classifier, no tiers, no pattern library to maintain. The JSON schema is editable when the LLM gets it wrong. The template library is finite and stabilizes quickly.

The other proposals over-engineer the classification layer. If your JSON extraction is good, you don't *need* to classify variables into Type A/B/C — the JSON already tells you the type. The classification step is solving a problem created by not having good structured data, which is exactly what Phase 1 produces.

**Estimated realistic cost: $0.10-0.50/survey with paid models, near $0 with free models.** Build time: 3-4 days. That's the right trade-off for a small team.
