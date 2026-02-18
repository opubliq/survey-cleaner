## Summary

You should go with **Approach D (pipeline sans LLM) with a thin LLM layer for codebook parsing only** — essentially a two-phase architecture where an LLM converts the codebook into structured JSON once, then a deterministic Python generator produces `clean.py` from that JSON without any further LLM calls. This targets **<$0.50/survey** instead of $38, and is the only approach that scales to 57+ surveys on a small-team budget.

## Recommendation

**Architecture: "Parse Once, Generate Deterministically"**

**Phase 1 — Codebook Extraction (LLM, one call per survey)**
A single LLM call takes the raw codebook (PDF/PPTX converted to text) and outputs a structured JSON schema describing every variable:

```json
{
  "Q2_province": {
    "type": "categorical",
    "mapping": {"1": "qc", "2": "on", "3": "bc"},
    "missing_codes": [98, 99, -9],
    "standard_name": "ses_province",
    "scale": null
  },
  "Q5_satisfaction": {
    "type": "likert_5",
    "mapping": {"1": "strongly_disagree", ...},
    "missing_codes": [99],
    "standard_name": "att_satisfaction",
    "scale": "agreement"
  }
}
```

This is one prompt, one response. The entire codebook goes in as context (~10-30K tokens input), and you get back structured JSON (~5-15K tokens output). **Cost: ~$0.10-0.40 per survey with Sonnet.** Even cheaper with a free model.

**Phase 2 — Deterministic Code Generation (zero LLM)**
A Python script reads the JSON schema and generates `clean.py` using templates:

- `categorical` → lookup dict + `.map()`
- `likert_N` → recode + ordered categorical
- `binary` → boolean mapping
- `numeric` → type cast + range validation
- `missing_codes` → always replaced with `np.nan`
- `standard_name` → column rename

This is straightforward Jinja2/string templating. No LLM needed. Each variable type gets a code template. The JSON schema is the single source of truth.

**Phase 3 — Validation (deterministic)**
Run the generated `clean.py` on the actual data. Check: no unmapped values, no unexpected NaNs beyond missing codes, output columns match schema. Log warnings for human review. This catches the ~5-10% of cases where the LLM misread the codebook.

**Model choice:** Start with a **free model via opencode zen** (GLM-5 or Kimi K2.5) for Phase 1. The task is structured extraction, not creative reasoning — mid-tier models handle this well. If extraction quality is below 90%, fall back to Sonnet for that survey. In practice, codebook parsing is a well-constrained task: the information is explicitly stated in the document, the model just needs to restructure it.

**Granularity:** One call per survey for Phase 1. The codebook for 84 variables fits comfortably in a single context window. Batching variables individually was your cost problem — don't repeat it.

**Codebook handling:** Convert PDF/PPTX to text (use `pdfplumber` or `python-pptx`), pass the full text as user message with a strict JSON schema in the system prompt. No RAG, no embeddings — unnecessary complexity for documents that fit in context.

## Trade-offs

**Pros:**
- Cost drops from $38/survey to ~$0.10-0.50 (or $0 with free models). 57 surveys = $6-28 total instead of $2,166.
- Deterministic generation means reproducible, testable, debuggable output.
- No orchestration complexity — it's just a Python script, not an agent framework.
- The JSON schema becomes a reusable artifact: you can hand-edit it if the LLM gets something wrong, then regenerate `clean.py` instantly.

**Cons:**
- You need to build the code templates for each variable type (~2-3 days of work for 6-8 templates).
- Edge cases the LLM would have "figured out" now require either a template or a manual JSON edit.
- If codebook formats vary wildly, Phase 1 extraction quality may fluctuate — you need the validation step to catch this.
- You lose the "magic" of an agent that handles everything — this requires you to understand and maintain the templates.

## Implementation Sketch

1. **Day 1:** Build the Phase 1 prompt. Take one real codebook, write the system prompt with JSON schema spec, test with GLM-5/Kimi and Sonnet. Compare outputs. Pick the cheapest model that gets >90% of variables right.

2. **Day 2:** Build the code generator. Start with 3 templates (`categorical`, `likert`, `binary`) — these cover ~80% of variables. Use one existing `clean.py` as your ground truth to validate output.

3. **Day 3:** Build validation. Run generated `clean.py` against real data, assert no unmapped values, log discrepancies. Add a `--dry-run` flag that shows what would change without writing.

4. **Day 4:** Run on 5 real surveys. Measure extraction accuracy. Add templates for remaining variable types as needed. Fix the prompt based on real failures.

5. **Ongoing:** Each new survey that introduces a novel pattern → add a template (~30 min). After 15-20 surveys, the template library stabilizes.

**Estimated cost at scale:** $0.10-0.50/survey with paid models, $0/survey with free models (LLM only parses the codebook). For 57 surveys: **under $30 total** vs. $2,166 with your current approach.
