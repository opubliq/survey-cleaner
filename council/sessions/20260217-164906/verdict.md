**Vote Tally**:

The proposals received the following votes:
*   **zai-glm-4.7**: 8 votes
*   anth-claude-opus: 0 votes
*   anth-claude-sonnet: 0 votes
*   google-gemini-2.5-flash: 0 votes
*   oc-big-pickle: 0 votes
*   oc-glm-5-free: 0 votes
*   oc-kimi-k2.5-free: 0 votes
*   oc-minimax-m2.5-free: 0 votes
*   zai-glm-4.5: 0 votes
*   zai-glm-4.7-flash: 0 votes

**Winning Direction**:

The council has overwhelmingly chosen **zai-glm-4.7**'s proposal, which advocates for a **Hybrid rules + LLM (Approach C) with a 3-Tier Model Strategy**. This approach is favored for its optimal balance of cost-efficiency, quality, autonomy, and scalability for survey cleaning tasks.

**Key Modifications**:

The following modifications were suggested and will be incorporated into the final recommendation:
1.  **Reduce Tier 3 Model Cost**: Replace Claude Sonnet in Tier 3 with **Claude Haiku**. Haiku is deemed sufficient for well-defined edge cases where structured codebook JSON is available, offering a significant cost reduction (approx. 4x cheaper) while maintaining quality.
2.  **Adjust Tier 3 Coverage**: Reduce the initial allocation for Tier 3 variables from 20% to **5-10% (or even 15% conservatively)**. This is based on the expectation that a robust pattern library will cover more cases deterministically or with free models.
3.  **Start Tier 1 Coverage Conservatively**: Begin with a **40-50% rule coverage for Tier 1** instead of the initially proposed 50-70%, allowing for a more organic growth of the pattern library.
4.  **Initial Pattern Library Focus**: Prioritize building the pattern library with **5-10 core patterns** (e.g., Likert 5/7, binary, province, age, gender) and then expand reactively based on emerging edge cases.
5.  **Prompt Caching for Codebook**: Implement prompt-caching for the structured JSON codebook across all variables to further optimize token usage.
6.  **Consider Sonnet for Tier 2**: Some suggest starting with Sonnet for Tier 2 to ensure quality initially, then downgrading to Haiku or free models as confidence grows. However, the consensus leans towards **free models for Tier 2**.
7.  **Data-Driven Pattern Matching**: Leverage data statistics (min, max, unique, distribution) for pattern matching to enhance robustness against inconsistent codebook documentation.

**Final Recommendation**:

Implement a **Hybrid rules + LLM (Approach C) system based on zai-glm-4.7's 3-Tier Model Strategy**.

**Architecture**:

```
[BOOTSTRAP - one-time per survey]
└─ Parse raw codebook into structured JSON schema (using a free model like GLM-5/Kimi)
   (Implement prompt-caching for this JSON codebook for reuse)

[VARIABLE PROCESSING LOOP - orchestrated by a Python script]
├─ Variable → Classify using data-driven pattern matching (min, max, unique count, distribution shape)
│   ├─ Tier 1 (Rule-Generated + LLM-Validated, ~40-50% variables): Match patterns, rule generates code, LLM validates.
│   │   └─ Examples: Likert scales, binary (yes/no), standard demographics.
│   │   └─ Critical: LLM validation is MANDATORY, not optional (per-survey variations).
│   ├─ Tier 2 (Free LLM Batch, ~40-50% variables): For semi-standard patterns.
│   │   └─ Process 10-20 variables per batch using a free model (e.g., GLM-5 or GLM-4.7 via opencode zen/z.ai).
│   ├─ Tier 3 (Paid LLM Individual, ~5-10% variables): For complex, ambiguous, or poorly documented variables.
│   │   └─ Use Claude Haiku for individual calls, leveraging the structured JSON codebook for context.
│
[GENERATE clean.py - deterministic Python code]
└─ Assemble all transformations into the final `clean.py` script.
```

**Model & Strategy**:
*   **Codebook Parsing (Bootstrap)**: GLM-5 or Kimi K2.5 (free via opencode zen).
*   **Tier 1 (Deterministic)**: Pure Python rules (0 tokens).
*   **Tier 2 (Batch LLM)**: GLM-5 or GLM-4.7 (free via opencode zen/z.ai).
*   **Tier 3 (Individual LLM)**: Claude Haiku.
*   **Granularity**: Batch 10-20 variables per LLM call for Tier 2. Individual calls for Tier 3.

**Codebook Management**:
*   Convert raw codebooks to structured JSON schema (e.g., `codebook.json`) once per survey.
*   This JSON becomes the single source of truth, passed to LLMs (with prompt caching) and deterministic rules.

**Estimated Cost Realistically**: **$0.50-$2.50 per 84-variable survey** (down from $38). This accounts for free model usage, occasional paid fallback for edge cases, and validation overhead.

**Trade-offs**:
*   **Pros**: Drastic cost reduction (90% lower), high autonomy after setup, maintained quality through tiered approach, scalable (pattern library compounds), manageable for a small team.
*   **Cons**: Initial development effort (approx. 3-4 weeks) for the pattern library and orchestrator, ongoing (but minimal) pattern library maintenance, need for a robust validation layer to catch LLM or rule-based errors.

**Dissenting Views**:

While `zai-glm-4.7` was the clear winner, some proposals like `oc-big-pickle` suggested an even simpler approach of a single, massive LLM call for all 80 variables with a free model. This was critically flagged as being too brittle and prone to catastrophic failure, making it difficult to debug and retry.

---

## User Feedback & Critical Clarifications

**Feedback on Tier 1 (Deterministic Rules)**:

The user correctly points out that even "standard" variables have meaningful variations across surveys that require LLM judgment:

1. **Different missing value codes**: Survey A uses 98/99 for NSP/Refus, Survey B uses -9/-1, Survey C uses "NSP"/"REF"
2. **Different variable names**: Same concept appears as `Q2_province`, `prov`, `province_residence` across surveys
3. **Different encoding schemes**: Same Likert scale but reversed (5=strongly agree vs 5=strongly disagree)
4. **Ambiguous codebook entries**: "See question text for exact labels" vs explicit value mappings

**Implication**: Tier 1 cannot be purely rule-based. The correct approach is:
- Rules generate the **initial cleaning code** based on pattern matching
- LLM validates and **adjusts** the mapping per-survey (e.g., "which missing codes apply?", "is this scale reversed?")
- This validation is **mandatory** for Tier 1, not optional

**Revised Tier 1 Definition**:
- **Rule generates** transformation code from pattern + codebook JSON
- **LLM validates**: "Does this mapping make sense given the specific survey's codebook and data distribution?"
- **Cost**: Minimal LLM calls per variable (1 quick validation vs full generation)

---

**Workflow & Tooling Clarifications**:

The user needs a concrete, portable workflow for processing new surveys:

### Recommended Tool: `survey-cleaner` CLI Package

**Installation**:
```bash
# Option 1: Install via npm (portable, includes all dependencies)
npm install -g @opubliq/survey-cleaner

# Option 2: Run from source (for development)
git clone https://github.com/opubliq/survey-cleaner.git
cd survey-cleaner
npm link  # or source setup.sh for venv
```

**Usage**:
```bash
# Basic usage - clean a single survey
survey-cleaner clean <survey_id>

# Example
survey-cleaner clean elxnqc_particip_egm_2021

# What happens:
# 1. Detects new survey in _SharedFolder_data_produit/
# 2. Parses codebook into structured JSON (using configured model)
# 3. Builds/cleans from pattern_library.json
# 4. Processes each variable through Tier 1→2→3 routing
# 5. Generates surveys/<survey_id>/clean.py
# 6. Validates and saves processed/data_cleaned.csv
# 7. Runs autonomously to completion
```

**Configuration File** (`~/.survey-cleaner/config.json`):
```json
{
  "models": {
    "codebook_parser": "opencode/glm-5-free",
    "tier1_validator": "opencode/kimi-k2.5-free",
    "tier2_batch": "opencode/glm-5-free",
    "tier3_individual": "anthropic/claude-3-5-haiku-20241022"
  },
  "paths": {
    "data_root": "/path/to/_SharedFolder_data_produit",
    "pattern_library": "~/.survey-cleaner/pattern_library.json"
  },
  "api_keys": {
    "anthropic": "sk-ant-...",
    "opencode": "auto"  # uses ~/.opencode/config
  }
}
```

**Pattern Library Persistence**:
- Location: `~/.survey-cleaner/pattern_library.json`
- Shared across all surveys (not per-survey)
- Updates automatically when user confirms a new pattern is correct
- User can manually add patterns via `survey-cleaner pattern add`

### Alternative: No Install Required

If a full CLI package is overkill, the workflow can be:

```bash
# Existing orchestrator.py, just make it more ergonomic
python surveys/orchestrator.py clean <survey_id>  # New command
```

This keeps everything in the repo, no install, but requires the user to be in the project directory.

### Triggering for New Surveys

**Option 1: Manual trigger (recommended initially)**
```bash
# When a new survey arrives in _SharedFolder_data_produit/
survey-cleaner clean new_survey_id
```

**Option 2: Watch directory (later)**
```bash
# Automatically detect and process new surveys
survey-cleaner watch --dir _SharedFolder_data_produit
# Polls every 5 minutes, triggers clean when new folder detected
```

The user starts with manual trigger (Option 1), and once the system proves reliable, can set up the watch mode for true autonomy.

**Next Steps**:

### Phase 1: Core Engine (1-2 weeks)

1. **Pattern Library Structure (1 day)**:
    *   Create `pattern_library.json` schema with fields for pattern signatures, transformation templates, and per-survey overrides
    *   Location: `~/.survey-cleaner/pattern_library.json` (shared, persistent)
    *   Design to be user-editable (manual pattern additions)

2. **Codebook Parser (2 days)**:
    *   Create `codebook_parser.py` to convert raw codebooks (PDF/Excel/MD) into structured JSON schema
    *   Use free model (GLM-5/Kimi) with robust error handling
    *   Output: `codebook.json` with variable definitions, value mappings, missing codes

3. **Tier 1: Rule Generator + Validator (3-4 days)**:
    *   `rule_generator.py`: Generate Python code from pattern + codebook JSON
    *   `rule_validator.py`: LLM validates per-survey variations (missing codes, reversed scales, etc.)
    *   This is CRITICAL: Tier 1 is NOT pure rule-based; LLM validation is mandatory

4. **Tier 2: Batch LLM Processor (2-3 days)**:
    *   `batch_llm_processor.py`: Group 10-20 variables per call to free models
    *   Prompts include codebook JSON snippet for context (token-efficient)
    *   Output structured transformations

5. **Tier 3: Individual LLM Handler (1-2 days)**:
    *   `individual_llm_handler.py`: Claude Haiku for complex cases
    *   Focused prompts: single variable + relevant codebook entry + pattern hints
    *   Error handling with retry logic

6. **Core Orchestrator (3-4 days)**:
    *   Enhance `surveys/orchestrator.py` or create new CLI entry point
    *   Variable classification logic (data-driven: min/max/unique/distribution)
    *   Tier routing (1→2→3) based on pattern match confidence
    *   State management with `status.json` for resumability

### Phase 2: CLI Tooling (3-5 days)

7. **CLI Interface (2-3 days)**:
    *   Create `survey-cleaner` CLI entry point (npm package or Python entry)
    *   Commands: `clean`, `watch`, `pattern add`, `pattern list`, `config`
    *   User-friendly output: progress bars, stage indicators, clear error messages

8. **Configuration System (1 day)**:
    *   `~/.survey-cleaner/config.json` for user-specific settings
    *   Model selection (tier1_validator, tier2_batch, tier3_individual)
    *   Path configuration (data_root, pattern_library location)
    *   API key management (Anthropic, optional override for opencode)

9. **Directory Watcher (Optional, 2 days)**:
    *   `survey-cleaner watch`: Poll `_SharedFolder_data_produit/` for new folders
    *   Auto-trigger `clean` when new survey detected
    *   Log file with timestamps for audit trail

### Phase 3: Testing & Validation (1-2 weeks)

10. **End-to-End Testing (3-5 days)**:
    *   Run on 5-10 existing surveys (varying complexity)
    *   Measure: actual cost, time, accuracy (sample validation)
    *   Stress test: 200+ variable survey, 84 variable survey, 20 variable survey

11. **Pattern Library Bootstrap (2-3 days)**:
    *   Manually analyze 3-5 existing surveys to identify top patterns
    *   Populate `pattern_library.json` with initial 5-10 core patterns
    *   Add examples and test cases for each pattern

12. **Documentation (1-2 days)**:
    *   README with quick start guide
    *   Pattern library documentation (how to add custom patterns)
    *   Configuration guide (API keys, model selection)
    *   Troubleshooting guide for common issues

### Phase 4: Production Deployment (Ongoing)

13. **Initial Rollout**:
    *   Deploy CLI package (npm publish or pip install)
    *   Train users on basic usage
    *   Process backlog of 5-10 surveys with manual oversight

14. **Pattern Library Maintenance**:
    *   Review pattern matches weekly for first month
    *   Add new patterns as they emerge (user-confirmed)
    *   Remove or merge duplicate patterns
    *   Goal: 80%+ coverage within 10-15 processed surveys

15. **Monitoring & Iteration**:
    *   Track metrics: cost/survey, time/survey, tier distribution
    *   Alerts when Tier 3 usage > 15% (pattern library needs expansion)
    *   User feedback mechanism for pattern approval/adjustment
