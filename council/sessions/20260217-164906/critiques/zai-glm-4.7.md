## Critique

### Proposal Analysis

**anth-claude-opus** (Approach D)
- Strengths: Cleanest architecture, true "$0.10-0.50/survey" path, leverages determinism intelligently
- Weaknesses: Underestimates edge case complexity, validation will catch >5-10% errors
- Blind spot: Assumes codebooks are consistently parseable—reality is messier

**anth-claude-sonnet** (D-first with C fallback)
- Strengths: Best analysis of caching failure, pragmatic tier approach, honest about quality trade-offs
- Weaknesses: 60% Type A coverage may be optimistic
- Blind spot: Underestimates free model reliability issues

**google-gemini-2.5-flash** (C, free models)
- Strengths: Embraces $0 target, solid implementation sketch
- Weaknesses: Unrealistic quality assumption for free models on all tasks
- Blind spot: $0 estimate fails if free models prove unreliable (likely)

**oc-big-pickle** (Batch + free models)
- Strengths: Correctly identifies "1 call not 80" as key insight
- Weaknesses: Batch 84 variables at once risks catastrophic failure
- Blind spot: Debugging a failed 84-var batch is harder than fixing 10 individual failures

**oc-glm-5-free** (C, free models)
- Strengths: Most realistic cost ($0.05-0.10), good validation emphasis
- Weaknesses: Overestimates free model capabilities for judgment tasks
- Blind spot: 10% error rate from free models may exceed quality threshold

**oc-kimi-k2.5-free** (C, 70% rules)
- Strengths: Most honest about development trade-offs, conservative cost estimate
- Weaknesses: $2-4/survey still significantly higher than hybrid approaches
- Blind spot: Pattern library may require ongoing maintenance beyond initial 3 days

**oc-minimax-m2.5-free** (C, free models)
- Strengths: Simple architecture, good model abstraction layer
- Weaknesses: Minimal detail on pattern library construction
- Blind spot: "2-3 hour test" assumption—real validation will take longer

**zai-glm-4.5** (C+ with strategic LLM)
- Strengths: Self-improving pattern library concept, realistic 3-week timeline
- Weaknesses: $4-7/survey on the expensive side of proposals
- Blind spot: Pattern extraction may require more manual curation than expected

**zai-glm-4.7-flash** (C with bootstrap)
- Strengths: Good balance of determinism and flexibility, clear implementation phases
- Weaknesses: Bootstrap parsing still costs $0.25/survey—adds up
- Blind spot: Pattern library "80% coverage in 10 surveys" may be optimistic

**zai-glm-4.7** (3-tier)
- Strengths: Best architectural clarity, realistic cost ($1-3), quality-focused tier model
- Weaknesses: More complex than necessary for initial implementation
- Blind spot: Tier 3 at 20% may be too high—could be 5-10% with better rules

### Consensus Points
1. All agree: Approach B (CLI agent) is dead due to token overhead
2. All agree: Structure codebook into JSON, don't pass raw Markdown repeatedly
3. All agree: Free models (GLM-5, Kimi) adequate for structured tasks
4. All agree: Batch variables instead of per-variable calls

### Key Disagreements

**Deterministic balance**: Some want 90% rules (D), others 60% (C). Reality: ~70-80% deterministically solvable.

**Free model reliance**: Anthropic/Google/oc proposals lean heavily on free models. Risk: 5-15% quality issues may exceed acceptance threshold.

**Cost reality**: Estimates range $0-7/survey. Most are too optimistic. Realistic range: $1-4/survey.

### Critical Flaws Flagged

**google-gemini-2.5-flash**: $0 estimate is irresponsible. Free models will fail validation on some variables, requiring retries or paid fallback.

**oc-big-pickle**: Batch 84 variables = single point of failure. When it fails, you lose everything and start over.

### Top Pick

**zai-glm-4.7's 3-tier strategy** with modifications:

- Keep tier model (pattern-based routing is smart)
- Reduce Tier 3 to 5-10% (better rules initially)
- Use Sonnet for Tier 3, not just edge cases
- Combine with anth-claude-opus's JSON parsing (Phase 1) and deterministic templates
- Target: $1.50-2.50/survey realistically

**Why**: Best balance of quality, cost, and maintainability. Clear architecture, honest trade-offs, handles edge cases properly. The tier model scales—invest more in rules over time, reduce LLM usage progressively.

**Immediate action**: Start with pattern library for top 5 patterns (Likert 5/7, binary, province, age). Process 3 surveys manually to validate rule coverage. If 70%+, proceed with tier routing.
