# Architecture Critique: Pattern Engine

## Consensus Points

1. **Q1 (Pattern Modeling)**: Universal agreement on **Option C (Hybrid)** — classes with `to_pattern()` method for JSON serialization. The only outlier (zai-glm-4.7) suggests Option A but provides weaker justification.

2. **Q2 (Classifier Input)**: Near-unanimous **Option C (both inputs)** — accept both `pd.Series` and `VariableSchema` with graceful degradation.

3. **Q3 (Missing Codes)**: Strong trend toward **Option C or A** (explicit detection / filter before tiering), rejecting the fragile threshold adjustment approach.

## Key Disagreements

### Q1: Where does detection logic live?

- **Most**: Logic in the pattern class itself (`matches()` method)
- **oc-minimax-m2.5-free**: Logic in a separate **matcher**, pattern is pure data

I **lean toward the majority**: Detection logic in the pattern class follows SRP better. A matcher that iterates patterns is just a loop — keeping detection with its pattern makes the code more modular and testable.

### Q3: Filter vs. Explicit Detection

- **oc-glm-5-free, zai-glm-4.7-flash**: Option A — filter before `n_unique`
- **Others**: Option C — explicit detection step that documents

I **lean toward Option C**: The argument from oc-kimi-k2.5-free is compelling — filtering silently loses the metadata about *which* codes are missing (98=NSP vs 99=NR). This matters for the generated `clean.py` script which should document missing value handling.

## Blind Spots

1. **oc-big-pickle** — Claims Option C for all three, but Q1 table shows "sérialisation JSON" as only ★★★★☆ for hybrid. This is the key advantage of hybrid over pure OOP — unclear why rated lower.

2. **zai-glm-4.7** — Rejects hybrid despite recommending Option C elsewhere. The critique of "double maintenance" is valid but applies to all Option C proposals — they all use hybrid.

3. **No proposal addresses**: What happens when two patterns both match with high confidence? (e.g., Likert 5 vs binary with values 1-5)

## Critical Flaws

**oc-glm-5-free (Q3)**: Claims Option A but describes Option C — "Pre-filter Missing Codes" still involves explicit detection via `_preprocess_missing_codes()` with heuristics. Inconsistent.

**zai-glm-4.7**: Recommends Option A for Q1 but contradicts itself by also recommending `to_pattern()` in implementation sketch. Unclear actual position.

## Top Pick

**Consensus architecture** (aligns with google-gemini-2.5-flash, oc-big-pickle, oc-kimi-k2.5-free, zai-glm-4.5):

- **Q1**: Hybrid classes with `to_pattern()`, detection in pattern
- **Q2**: Both inputs, series validates schema
- **Q3**: Explicit detection preprocessing, results passed to classifier

**Why**: This combination maximizes robustness for variable codebook quality while keeping pattern logic encapsulated and testable. The explicit missing code step is essential for auditability — downstream `clean.py` needs to know which codes represent missing data vs. actual responses.

The one addition I'd make: **conflict resolution** — add logic for when multiple patterns match. Suggested priority: most specific pattern wins (binary > likert > demographics).
