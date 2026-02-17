```
VOTE: zai-glm-4.7
CONFIDENCE: high
REASON: The 3-tier strategy with data-driven pattern matching is the only approach that balances cost ($1-2/survey), quality (LLM judgment where needed), and maintainability for a small team. Using statistical signatures (min, max, distribution) rather than just codebook text makes the pattern library robust against messy documentation.
MODIFICATION: Start with 50% Tier 1 (deterministic), 40% Tier 2 (GLM-5 batch), 10% Tier 3 (Claude Haiku—not Sonnet). Begin with just 5 patterns (Likert 5/7, binary, province, age, gender) and add patterns reactively as edge cases emerge, rather than investing 2 weeks upfront building a comprehensive library.
```
