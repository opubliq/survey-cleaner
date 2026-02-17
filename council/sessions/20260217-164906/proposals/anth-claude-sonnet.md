**Summary**

The $38/survey cost comes from a misdiagnosed caching failure and over-reliance on LLM judgment for decisions that can be made deterministically. The right architecture is approach **D-first with C as fallback** — parse the codebook into structured JSON once, apply deterministic rules for 60-70% of variables, and invoke a cheap/free LLM only for genuine ambiguity. This gets you to $0.50-2.00/survey realistically.

---

**Recommendation: Structured Pipeline with Tiered LLM Fallback**

The core insight you're missing: **the codebook already contains most of the information needed to generate `clean.py` deterministically**. If `Q2_province: 1=QC, 2=ON, 3=BC`, you don't need an LLM to output `ses_province = df['Q2_province'].map({1: 'qc', 2: 'on', 3: 'bc'})`. That's a regex + template problem.

**Proposed Architecture:**

```
codebook_source (PDF/XLSX/MD)
        ↓
[Step 1] Codebook Parser — ONE LLM call, whole codebook
        ↓ outputs structured JSON
{variables: [{raw_name, label, values: {1: "QC", 2: "ON"}, type: "categorical", ...}]}
        ↓
[Step 2] Variable Classifier — pure Python, zero tokens
  → Type A: fully specified mapping → deterministic template → clean.py block
  → Type B: ambiguous naming/missing codes → LLM batch (10-20 vars/call)
  → Type C: incomplete codebook → LLM individual call
        ↓
[Step 3] Code Generator — Jinja2 templates for Type A, LLM for B/C
        ↓
clean.py assembled
```

**Why this works:**

1. **Step 1 is the only expensive call** — one `claude-haiku` or `GLM-5` call with the full codebook (maybe 20-30K tokens input). This produces a canonical JSON that all downstream steps use. Cache this aggressively.

2. **Step 2 is free** — Python regex identifies Likert scales (1-5 with "strongly agree" etc.), binary yes/no, province/country lists, age ranges. These patterns are finite and enumerable.

3. **Step 3 batches LLM calls** — instead of 84 calls, you make 2-4 batch calls covering all ambiguous variables. Include 10-20 variables per prompt: "Given these variable definitions, generate the clean.py code block for each."

---

**Model Strategy**

- **Step 1 (codebook parsing):** Try `GLM-4.5` or `Kimi K2.5` free tier first. If JSON output is unreliable, use `claude-haiku-3-5` (~$0.25 for a 84-var codebook). This is a structured extraction task — free models handle it adequately.
- **Step 3 batch LLM (Type B):** `GLM-5` or `Minimax M2.5` free. Test on 20 variables first with manual validation. If error rate >15%, switch to haiku.
- **Step 3 individual (Type C):** `claude-haiku-3-5`. Reserve Sonnet for nothing — it's overkill.

Never use Sonnet for this workload.

---

**Why your caching failed**

The $38 cost on attempt 2 suggests your cache wasn't hitting. Anthropic prompt caching requires: (1) identical byte-for-byte prefix, (2) >1024 tokens in cached block, (3) cache reuse within 5 minutes (beta) or based on TTL. If your orchestrator was building prompts dynamically with variable-specific context injected *before* the codebook, the cache key changed every call. Fix: put the full codebook as a static `system` block with `cache_control: {type: "ephemeral"}`, then variable-specific instructions in the `user` turn only.

---

**Trade-offs**

| | Pros | Cons |
|---|---|---|
| This approach | Cheap, predictable, auditable | Upfront investment in classifier + templates (~3-5 days) |
| Pure API (current) | Already exists | $38/survey, unacceptable |
| CLI agent | Zero dev work | Unpredictable token spend, can't run 57 surveys autonomously |
| Free models only | $0 | Need validation layer; unreliable JSON output |

---

**Implementation Sketch**

1. **Day 1:** Write `codebook_parser.py` — takes codebook source, calls haiku once, outputs `variables.json` schema. Validate on 3 known surveys.
2. **Day 2:** Write `classifier.py` — regex rules for Type A/B/C. Aim: >60% classified as Type A. Log everything for tuning.
3. **Day 3:** Write Jinja2 templates for top 8 Type A patterns (Likert, binary, categorical mapping, numeric range, date, text passthrough, province/country, missing-code handling).
4. **Day 4:** Write batch LLM caller for Type B — one prompt per 15 variables, structured JSON output `{var_name: "python_code_block"}`.
5. **Day 5:** Integration + `assembler.py` that stitches Type A templates + LLM outputs into final `clean.py`.

**Cost estimate for 84-variable survey:**
- Step 1: ~25K tokens haiku input/output → ~$0.08
- Type A (55 vars): $0
- Type B batch (22 vars, 2 calls): ~8K tokens haiku → ~$0.03
- Type C individual (7 vars): ~7K tokens haiku → ~$0.02
- **Total: ~$0.13-0.50/survey** depending on codebook complexity

At worst, with a messy codebook requiring Sonnet for Step 1: ~$1.50.

**Autonomy:** run `python orchestrator.py <survey_id>` → completes in 2-5 minutes without intervention. Add `--validate` flag that samples 5 generated code blocks and runs them against a 10-row data slice to catch obvious errors before writing final `clean.py`.
