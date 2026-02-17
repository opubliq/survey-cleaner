**Summary:**
The high costs of previous LLM-intensive survey cleaning efforts necessitate a strategic shift. I recommend implementing a **Hybrid rules + LLM (Approach C)** strategy. This approach will leverage deterministic rule-based cleaning for common variable patterns, while selectively using a cost-effective LLM for complex variables, significantly reducing token consumption and achieving scalability and economy.

**Recommendation:**
Adopt **Approach C: Hybrid rules + LLM** as the primary strategy. This approach allows for the intelligent allocation of resources, using deterministic logic where possible to avoid LLM costs, and reserving LLM capabilities for nuanced decision-making.

Here's the recommended architecture and workflow:

1.  **Codebook Structuring (Initial LLM or deterministic parsing):**
    *   **Process:** The raw codebook (PDF, TXT, PPTX, MD) for each survey must first be parsed into a standardized, machine-readable format, preferably **JSON Schema**. This one-time process per survey can be handled by an initial, carefully crafted LLM call (e.g., a Sonnet model for complex parsing) if the source formats are highly varied, or by deterministic parsers if the input formats are consistent. The structured JSON codebook will then serve as the authoritative source for all subsequent steps.
    *   **Why:** Provides a clean, unambiguous input for both the rule engine and the LLM, drastically reducing the LLM's context window for per-variable tasks.

2.  **Variable Classification & Cleaning Engine:**
    *   **Classification:** Implement a robust classifier that, for each variable, determines its "type" based on patterns in the structured codebook and preliminary data analysis (e.g., value distribution, variable names).
        *   **Type A (Deterministic):** Variables with well-defined, common patterns (e.g., 5-point Likert scales, binary yes/no, standard demographic categories). These will be handled by a deterministic rule engine.
        *   **Type B (LLM Batch):** Variables with recognizable but slightly non-standard patterns, where the LLM can resolve ambiguities (e.g., non-standard missing codes, complex re-coding logic). These will be processed in batches.
        *   **Type C (LLM Individual):** Truly unique, complex, or poorly documented variables requiring specific LLM judgment. These should be rare.
    *   **Deterministic Cleaner:** Develop a growing library of Python functions (the "pattern library") that apply specific cleaning rules for Type A variables. This component will generate Python code snippets for `clean.py` without any LLM interaction.

3.  **LLM Integration (for Type B and C):**
    *   **Model Choice:** Prioritize **free models** available via opencode zen or z.ai, specifically **GLM-4.7 or GLM-5**. Conduct rigorous testing to assess their quality for the specific cleaning tasks (standardized naming, missing value identification, normalization). Only if these models consistently fail to meet quality thresholds should a move to a more expensive, smaller commercial model (like Anthropic Haiku or GPT-3.5 Turbo) be considered.
    *   **Granularity:**
        *   For **Type B variables**, use **batch processing (10-20 variables per LLM call)**. The prompt will include the structured codebook entries for all variables in the batch, raw data snippets if helpful, and the desired output format (Python cleaning code). This optimizes token usage while providing sufficient context.
        *   For **Type C variables**, use individual LLM calls, ensuring the prompt is highly focused and provides all relevant structured codebook information.

4.  **Autonomy & Orchestration:**
    *   The existing `orchestrator.py` should be enhanced to manage this entire hybrid pipeline:
        *   Call the codebook structuring logic.
        *   Iterate through variables, classifying each.
        *   Route Type A variables to the deterministic cleaner.
        *   Batch Type B variables for LLM processing.
        *   Send Type C variables for individual LLM processing.
        *   Aggregate all generated Python cleaning snippets into the final `clean.py`.
    *   Implement robust error handling, logging any LLM failures or unexpected outputs for infrequent human review, but aiming for full end-to-end automation once launched.

**Trade-offs:**

*   **Pros:**
    *   **Drastic Cost Reduction:** By eliminating LLM calls for 65%+ of variables, and batching others, token costs will plummet, likely well below the $4-5 target.
    *   **Scalability:** Deterministic rules process variables quickly and predictably, allowing for high throughput.
    *   **Maintainable Quality:** Rule-based cleaning is consistent. LLM quality can be iteratively improved through prompt engineering and model selection for complex cases.
    *   **Autonomy:** Designed for set-and-forget operation, reducing human intervention.
*   **Cons:**
    *   **Initial Development Overhead:** Building the variable classifier and the comprehensive deterministic rule engine (pattern library) will require significant upfront engineering effort.
    *   **Rule Maintenance:** The deterministic rule library will need ongoing maintenance as new data patterns emerge or requirements change.
    *   **Dependence on Free LLM Quality:** The quality of the overall output for Type B and C variables will be directly tied to the performance of the chosen free LLM, which might be less consistent than paid, larger models.

**Implementation Sketch (Next Steps):**

1.  **Codebook JSON Transformation:**
    *   Create `surveys/codebook_parser.py` that takes raw codebook paths and outputs `codebook.json`. Start with a simple regex-based parser for markdown, then expand to handle PDF/PPTX (potentially using an LLM for complex extraction as a one-time per-survey cost).
2.  **Variable Classifier Module:**
    *   Develop `surveys/variable_classifier.py` that reads `codebook.json` and infers variable types (A, B, C). This will involve keyword matching, pattern recognition, and basic data inspection.
3.  **Deterministic Cleaner Module:**
    *   Create `surveys/deterministic_cleaner.py` with functions like `clean_likert()`, `clean_binary()`, `standardize_demographic()`, etc., each generating Python code snippets.
4.  **Update `orchestrator.py`:**
    *   Integrate `codebook_parser.py`, `variable_classifier.py`, and `deterministic_cleaner.py`.
    *   Modify the `clean-variable` step to conditionally call the deterministic cleaner or the LLM based on variable type.
    *   Implement batching logic for Type B LLM calls.
    *   Configure LLM API calls to use GLM-4.7 or GLM-5.
5.  **Comprehensive Testing:**
    *   Develop unit tests for all new modules.
    *   Run end-to-end tests on a subset of existing surveys, carefully validating the generated `clean.py` and the cleaned output data for accuracy and cost.

**Estimated Cost for an 84-variable survey (using free GLM models where applicable):**

*   **Codebook JSON Transformation:** (One-time, assuming an initial complex parse by a paid model like Claude Sonnet at ~$3/M tokens) ~10,000 tokens = **~$0.03**.
*   **Type A Variables (Deterministic, ~55 variables):** **$0** (no LLM usage).
*   **Type B Variables (LLM Batch, ~21 variables):** ~2 batches * ~1000 tokens/batch (using free GLM model) = **$0**.
*   **Type C Variables (LLM Individual, ~8 variables):** ~8 calls * ~500 tokens/call (using free GLM model) = **$0**.

With this approach, the per-survey cost related to LLM token consumption can be reduced to near zero, with the primary cost being the initial (and potentially infrequent) codebook parsing. This makes the system extremely economical and scalable for a growing number of surveys.
