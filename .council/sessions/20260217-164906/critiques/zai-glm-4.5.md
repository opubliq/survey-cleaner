## Critique of Survey Cleaning Proposals

**Strengths:**
- Most proposals correctly identify the core issue: over-reliance on expensive LLMs for deterministic tasks
- Strong consensus on using free models (GLM-5, Kimi) for 80%+ of work
- Pattern library approaches show understanding that survey cleaning follows predictable structures
- Realistic cost targeting ($0.50-7/survey vs current $38)

**Weaknesses:**
- Several proposals underestimate the complexity of building robust pattern libraries
- Insufficient attention to validation layers for catching errors in deterministic processing
- Over-optimism about free model capabilities for nuanced cleaning decisions
- Missing concrete implementation details for JSON schema extraction from varied codebook formats

**Blind Spots:**
- Data quality validation before cleaning (garbage in, garbage out)
- Version control for pattern libraries across survey updates
- Performance metrics beyond cost (speed, accuracy, maintainability)
- Integration with existing workflow (how this fits into current processes)

**Consensus Points:**
1. Hybrid approach (deterministic + LLM) is superior to pure API or pure deterministic
2. Free models handle 65-80% of work adequately
3. Batch processing beats per-variable API calls
4. Codebook should be converted to structured format once, not reprocessed per variable

**Key Disagreements:**
- **Cost projections**: Range from $0.05 (optimistic) to $7 (conservative) per survey
- **LLM granularity**: Single-call vs batch vs individual for complex cases
- **Pattern library scope**: Some want 95% rules, others see rules as supplemental

**Critical Flaws:**
- Pure deterministic (D) proposals ignore real-world variability in codebooks
- CLI agent (B) approaches dismiss the proven token overhead issue
- Several cost projections ignore real-world factors like retries, validation, and maintenance

**TOP PICK: Hybrid + 3-Tier Strategy (zai-glm-4.7)**

This proposal strikes the best balance:
1. **Realistic architecture**: 50% Tier 1 (deterministic), 30% Tier 2 (free model batch), 20% Tier 3 (premium)
2. **Pragmatic cost targeting**: $1-3/survey accounts for real-world complexity
3. **Clear implementation path**: Specific phases with deliverables
4. **Quality focus**: Validation layer and pattern learning over time
5. **Sustainability**: Patterns compound with each survey, reducing costs long-term

The approach acknowledges that some variables truly need premium LLM judgment (20%) while being aggressive about automating everything possible. It's the only proposal that treats this as an ongoing system rather than a one-time fix.
