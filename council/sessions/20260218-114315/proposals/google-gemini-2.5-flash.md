**Summary**
For the Pattern Engine, I recommend an **Hybrid (Option C)** approach for pattern modeling, using Python classes for logic and a `to_pattern()` method for JSON serialization. The **PatternClassifier should accept both Pandas Series and VariableSchema (Option C)** for maximum robustness. Finally, **explicitly detect and handle missing codes as a preliminary step (Option C)** before classifying variables, ensuring `n_unique` accurately reflects actual response values.

---

**Recommendation**

1.  **Modélisation des patterns (zy4.1) — Option C (Hybride)**
    I recommend defining patterns as **Python classes with an explicit `to_pattern() -> Pattern` method** for JSON serialization. This provides the best balance of maintainability, flexibility, and adherence to the `pattern_library.json` schema. The Python classes can encapsulate complex detection logic (in `matches` method) and detailed code generation (`generate_code` method), leveraging Python's full power for type hinting, testing, and complex conditional logic. The `to_pattern()` method ensures a clean, serializable representation for the core metadata of the pattern, allowing the `PatternClassifier` to work with a standardized Pydantic `Pattern` object.

2.  **Input du PatternClassifier (zy4.2) — Option C (Les deux en entrée)**
    The `PatternClassifier` should accept **both the `pandas.Series` and the `VariableSchema`** as input. This provides the most robust and informed classification decision. Codebooks can be incomplete or of variable quality; relying solely on them is risky. By having both, the classifier can:
    *   Prioritize semantic information from a high-quality `VariableSchema` (e.g., an explicit `scale_type="likert"` is a strong hint).
    *   Validate codebook information against actual data distribution from the `pandas.Series`.
    *   Fall back to `pandas.Series` statistics when `VariableSchema` is missing or unreliable. This dual input allows for a sophisticated tiering mechanism that maximizes accuracy and resilience to real-world data imperfections.

3.  **Gestion des codes manquants dans le tiering — Option C (Détection explicite préalable)**
    Missing codes should be **explicitly detected, extracted, and documented as a preliminary step** before the `PatternClassifier` runs. This ensures that the core pattern matching (e.g., Likert, demographics) operates on the "valid" response values. By first identifying and removing (conceptually, not physically for `n_unique` calculation) these missing codes, the `n_unique` count accurately reflects the number of *actual response options*, preventing legitimate Tier 1 patterns from being misclassified due to additional metadata codes. This pre-processing step simplifies the subsequent pattern detection logic and allows for dedicated, consistent handling of missing values across the pipeline.

---

**Trade-offs**

1.  **Modélisation des patterns (Hybride)**
    *   **Pros:** Combines OOP's power for complex logic with Pydantic's benefits for serialization and data validation. Improves testability of individual pattern logic. Provides a clear contract (`to_pattern()`) for the matcher.
    *   **Cons:** Slightly more boilerplate than pure Pydantic instances. Requires careful management to ensure the serialized `Pattern` accurately reflects the class's intent.

2.  **Input du PatternClassifier (Les deux en entrée)**
    *   **Pros:** Highest accuracy and robustness, as it leverages all available information. Can cross-reference data for validation. More adaptable to varying codebook quality.
    *   **Cons:** More complex interface for the `classify` method. The implementation of the classifier will need to intelligently weigh and combine information from both sources, which adds complexity.

3.  **Gestion des codes manquants (Détection explicite préalable)**
    *   **Pros:** Clean separation of concerns: pattern detection focuses solely on response values, while missing code handling is a distinct process. `n_unique` accurately reflects meaningful response options. Improves clarity and consistency in how missing values are managed.
    *   **Cons:** Introduces an additional preprocessing step. Requires careful definition of what constitutes a "missing code" and how to identify it across different data types and surveys.

---

**Implementation sketch**

1.  **Modélisation des patterns (zy4.1):**
    *   Create `base_pattern.py` with an abstract `BasePattern` class that includes abstract methods for `matches(self, series: pd.Series, var: VariableSchema)` and `generate_code(self, var_name: str, codebook_entry: VariableSchema) -> str`, plus a concrete `to_pattern() -> Pattern` method that returns a Pydantic `Pattern` instance.
    *   Implement specific pattern classes (e.g., `Likert5AgreePattern` inheriting from `BasePattern`) in `likert_scales.py`, `demographics.py`, etc., overriding the abstract methods.
    *   The `to_pattern` method in `BasePattern` could be implemented to take the `pattern_id` and `transformation_template` from class attributes, and then potentially aggregate detection criteria from specific methods within the class.

2.  **Input du PatternClassifier (zy4.2):**
    *   Define `classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult` in `pattern_classifier.py`.
    *   Inside `classify`, first attempt to infer information from `var` if it's provided. Then, compute statistics from `series`.
    *   Implement logic to iterate through the available Pydantic `Pattern` objects (loaded from `pattern_library.json` which are derived from `BasePattern.to_pattern()`) and for each, call its `matches` method using both `series` and `var` to determine the confidence score.

3.  **Gestion des codes manquants:**
    *   Create a new module, e.g., `survey_cleaner/data_preprocessing/missing_value_detector.py`.
    *   Implement a function `detect_and_exclude_missing_codes(series: pd.Series, var: VariableSchema | None = None) -> tuple[pd.Series, dict]` that returns the series *without* missing codes for `n_unique` calculation, and a dictionary of detected missing codes. This function would be called *before* passing the series to `PatternClassifier`.
    *   Adjust `PatternClassifier` to receive the "cleaned" series (for `n_unique` and distribution) and potentially the extracted missing codes, which might influence Tier 1 decisions if a pattern explicitly handles them.
