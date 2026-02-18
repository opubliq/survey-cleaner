## Summary
I recommend a hybrid deterministic rules + targeted LLM approach that reduces API costs by 80-90% while maintaining quality through intelligent pattern recognition and strategic LLM usage only for complex cases.

## Recommendation
**Approach C+ (Enhanced Hybrid Rules + Strategic LLM)**

### Architecture
1. **Pattern Library Builder** (1-time investment):
   - Extract variable patterns from historical surveys
   - Create rule templates for common types (Likert, binary, demographics)
   - Build validation heuristics

2. **Three-Tier Processing Pipeline**:
   - **Tier 1 (Rule-based: ~60-70%)**: Standard patterns with deterministic rules
   - **Tier 2 (Batch LLM: ~25%)**: Complex but similar variables processed together
   - **Tier 3 (Individual LLM: ~5-10%)**: Ambiguous/edge cases requiring individual attention

3. **Smart Codebook Processing**:
   - One-time structured extraction using cheapest capable model
   - Convert to JSON schema for programmatic access
   - Cache for reuse across all variables

### Model Strategy
- **Codebook parsing**: GLM-5 or Kimi K2.5 (free, sufficient for structured extraction)
- **Tier 3 decisions**: Claude Sonnet (quality-critical, minimal usage)
- **Validation**: GLM-4.5 (free, good for verification)

### Workflow
1. **Preprocessing**: Extract and structure codebook (1 call/survey)
2. **Classification**: Auto-categorize variables by pattern complexity
3. **Processing**: Apply appropriate tier to each variable
4. **Validation**: Spot-check 10-15% of processed variables
5. **Generation**: Write clean.py script

## Trade-offs
**Pros:**
- 80-90% cost reduction (~$4-7/survey vs $38)
- Scalable to 100+ surveys
- Maintains quality through targeted LLM use
- Self-improving (pattern library grows with each survey)

**Cons:**
- Initial development effort (2-3 weeks)
- Risk of pattern mismatches in early surveys
- Requires ongoing pattern library maintenance
- Less flexible than pure LLM approach

## Implementation Sketch
1. **Phase 1 (Week 1)**: Build pattern library and classifier
   - Analyze existing 57 surveys to extract common patterns
   - Create rule templates for 80% of cases
   - Implement variable classification logic

2. **Phase 2 (Week 2)**: Develop tiered processing engine
   - Implement deterministic rules for Tier 1
   - Design batch processing for Tier 2
   - Create individual LLM calls for Tier 3

3. **Phase 3 (Week 3)**: Integration and optimization
   - Build orchestrator with auto-retry logic
   - Implement validation and error handling
   - Test on 3-5 existing surveys

**Estimated cost**: $4-7 per 84-variable survey ($0.05-0.08/variable)
**Development effort**: 3 weeks, then minimal maintenance
