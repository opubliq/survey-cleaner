## Architecture Review: Survey Cleaning Pipeline

The proposals offer valuable insights into refining the survey cleaning pipeline. While all demonstrate a solid understanding of the problem, some approaches are more pragmatic and efficient for a small team.

### Proposal 1: google-gemini-2.5-flash (G-F)

*   **Strengths:** Comprehensive, well-structured, clear justifications and trade-offs. Good emphasis on LLM-light for quality.
*   **Weaknesses:** Integration details for existing `Batcher` and `CleanValidator` could be more explicit.
*   **Blind Spots:** Recommending per-variable validation might be inefficient if `CleanValidator` is built for whole-script analysis.

### Proposal 2: oc-big-pickle (BP)

*   **Strengths:** Excellent focus on leveraging *existing* (but unused) code, which is critical for a small team. Provides concrete implementation sketches, especially for batching.
*   **Weaknesses:** Proposing to keep classification 100% deterministic might miss early quality gains from a free LLM.
*   **Blind Spots:** None major.

### Proposal 3: oc-minimax-m2.5-free (MM)

*   **Strengths:** Concise, pushes back on unnecessary complexity (e.g., event-driven). Realistic effort estimates for some tasks.
*   **Weaknesses:**
    *   **Critical Flaw:** Contradicts itself on the Tier 1 confidence threshold in Question 6, recommending both keeping it at 0.8 and using a shortcut for <0.85.
    *   Limiting escalation to "Max 1 escalation" is likely too restrictive, potentially leaving solvable problems unaddressed.
    *   Delaying LLM in classification and validation misses immediate, free quality improvements.
*   **Blind Spots:** Underestimates the sample size needed for robust pattern optimization.

---

### Consensus Points

*   **Orchestrator Batching:** All agree on `Option B` – activating true batching within the existing sequential structure. BP's explicit use of the `create_batches` function is the most direct.
*   **Variable Naming:** All recommend `Option C` – using codebook labels for Tier 1 naming to improve readability and consistency.
*   **Automatic Escalation:** All agree that escalation should be automatic upon validation failure.
*   **GLM-5 is Free:** All proposals acknowledge and aim to leverage the free GLM-5 for various quality checks, though in different parts of the pipeline.

### Key Disagreements & My Leanings

*   **LLM in Classification (Q2):**
    *   G-F advocates for using GLM-5 for borderline cases (confidence 0.5-0.79).
    *   BP and MM prefer keeping it deterministic or delaying.
    *   **My Lean:** G-F. Using the free LLM for borderline classification is a low-cost, high-impact way to improve accuracy upfront, preventing mis-tiered variables from entering the wrong path.
*   **Validation Integration (Q5):**
    *   G-F suggests per-variable validation.
    *   BP and MM propose after *all variables processed*.
    *   **My Lean:** BP. Integrating the `CleanValidator` *after all variables are processed* (before `clean.py` assembly) is more aligned with typical static analysis and likely more efficient than per-variable runs. Then, a targeted LLM check for Tier 1 *failures* adds semantic robustness.
*   **Escalation Logic (Q6):** There's a slight disagreement on the maximum number of escalations and Tier 1 threshold adjustments.
    *   **My Lean:** A robust system needs at least 2 escalations (T1 → T2 → T3). BP's idea of a T1 confidence shortcut (if confidence < 0.85, skip T1) is a smart optimization to avoid wasted processing for highly uncertain cases.

---

### TOP PICK: A Hybrid Approach (Strongly influenced by BP & G-F)

My top pick is a hybrid that prioritizes leveraging existing assets, applying free LLM resources intelligently, and establishing robust error handling, all while maintaining simplicity.

1.  **Orchestrator Role (Q1):** **Activate true batching with the existing `create_batches` function (BP's recommendation).** This is the most efficient and least disruptive way to address the current problem.
2.  **LLM in Classification (Q2):** **Add a lightweight GLM-5 for variables with 0.5–0.79 confidence (G-F's Option B).** Proactively improving classification for borderline cases is a high-value, no-cost enhancement.
3.  **Pattern Optimization (Q3):** **Proceed with the "battue" on 500 stratified variables (BP's recommendation).** This empirical data is crucial for calibrating patterns and understanding the pipeline's true performance. Target a ≥50% Tier 1 rate.
4.  **Variable Naming (Q4):** **Use codebook labels for Tier 1 naming, with fallback to raw names (BP/G-F/MM Option C).** This ensures consistent and readable names.
5.  **Validation (Q5):** **Integrate `CleanValidator` after all variables are processed and *then* apply a lightweight GLM-5 for semantic checks on Tier 1 failures only (BP's recommendation).** This balances efficiency with targeted, free semantic validation.
6.  **Escalation Strategy (Q6):**
    *   **Automatic escalation** on validation failure.
    *   **Confidence-based shortcut:** If initial Tier 1 confidence is below 0.85, skip Tier 1 and send directly to Tier 2 (BP).
    *   **Information to transmit:** Pass both the detailed `reason` for failure and the `incorrect_code` generated (G-F).
    *   **Circuit-breaker:** Implement a maximum of 2 escalations per variable (T1 → T2 → T3), marking as `needs_review=True` if Tier 3 also fails (G-F).
    *   **Tier 1 Threshold:** Keep the initial classification threshold at 0.8. The shortcut handles lower confidence cases.

This hybrid approach offers the best balance of immediate impact, long-term robustness, and maintainability for a small team by strategically integrating LLMs and leveraging existing project components.
