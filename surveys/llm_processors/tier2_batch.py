"""Tier 2 batch processor for LLM-based survey cleaning.

Processes 10-20 variables per batch using GLM-5 or GLM-4.7 (free via ZhipuAI).
Cost is shared across multiple variables → very efficient.

Features:
- Batch prompt with multiple variables
- Uses PromptCache for system prompts
- Parses JSON response with Python code per variable
- Individual retry on failure
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema
    from surveys.llm_processors.batcher import Batch
    from surveys.pattern_engine.patterns.base_pattern import ClassificationResult

logger = logging.getLogger(__name__)

DEFAULT_TIER2_MODEL = "opencode/glm-5-free"
FALLBACK_TIER2_MODEL = "opencode/glm-4.7-free"

SYSTEM_PROMPT = """Tu es un expert en nettoyage de données de sondages.

Ta tâche: générer le code Python pour transformer des variables brutes en variables nettoyées.

## Règles de nettoyage

### 1. Mapping catégoriel
Utilise `.map()` pour les variables catégorielles. Les valeurs non-mappées deviennent automatiquement NaN.

```python
df_clean['var_clean'] = df['var_raw'].map({
    1.0: 'label1',
    2.0: 'label2',
    99.0: np.nan  # missing code → NaN
})
```

### 2. Normalisation ordinale (0-1)
Pour les échelles Likert, normalise vers [0, 1] où 1 = valeur la plus positive.

```python
df_clean['var_clean'] = df['var_raw'].map({
    1.0: 1.0,   # Très satisfait
    2.0: 0.75,  # Plutôt satisfait
    3.0: 0.5,   # Neutre
    4.0: 0.25,  # Plutôt insatisfait
    5.0: 0.0,   # Très insatisfait
    98.0: np.nan, 99.0: np.nan
})
```

### 3. Normalisation numérique (0-100 → 0-1)
```python
df_clean['var_clean'] = np.nan
mask = (df['var_raw'] >= 0) & (df['var_raw'] <= 100)
df_clean.loc[mask, 'var_clean'] = df.loc[mask, 'var_raw'] / 100.0
```

### 4. Labels concis
Les labels doivent être simples et sans répétition:
- ✅ "quebec", "ontario" (PAS "province_quebec")
- ✅ "liberal", "conservative" (abréviations anglaises OK)
- ✅ Utilise des underscores, pas des espaces

### 5. Codes manquants
Toujours mapper vers `np.nan`:
- Codes courants: 98, 99, -1, -9, -99, 999
- Labels typiques: NSP, NR, Refus, Ne sait pas

## Format de sortie JSON

Retourne un objet JSON avec le code généré pour chaque variable:

```json
{
  "variables": {
    "nom_variable_clean": {
      "code": "df_clean['nom_variable_clean'] = df['Q1'].map({...})",
      "original_variable": "Q1",
      "type": "categorical",
      "value_labels": {
        "label1": "Label descriptif 1",
        "label2": "Label descriptif 2"
      }
    }
  }
}
```

## Important

- Génère du code Python EXÉCUTABLE
- Respecte la convention de noms: ses_* (démographique), op_* (opinion), behav_* (comportement)
- Si le nom original est ambigu, crée un nom descriptif en anglais
"""


@dataclass
class VariableCode:
    """Generated code and metadata for a single variable."""

    clean_var_name: str
    original_var_name: str
    code: str
    var_type: str
    value_labels: dict[str, str]
    error: Optional[str] = None


@dataclass
class BatchProcessingResult:
    """Result of processing a batch of variables."""

    batch_index: int
    model_used: str
    variables: dict[str, VariableCode] = field(default_factory=dict)
    failed_vars: list[str] = field(default_factory=list)
    tokens_used: int = 0
    cost_usd: float = 0.0

    @property
    def success_count(self) -> int:
        return len([v for v in self.variables.values() if v.error is None])

    @property
    def failure_count(self) -> int:
        return len(self.failed_vars)


class Tier2BatchProcessor:
    """Process batches of Tier 2 variables using LLM.

    Usage:
        processor = Tier2BatchProcessor()
        result = processor.process_batch(batch)
        for var_name, var_code in result.variables.items():
            print(f"{var_name}: {var_code.code}")
    """

    def __init__(
        self,
        model: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        temperature: float = 0.1,
        max_retries: int = 2,
    ):
        self.model = model or DEFAULT_TIER2_MODEL
        self.cache_dir = cache_dir
        self.temperature = temperature
        self.max_retries = max_retries
        self._cache = self._init_cache()

    def _init_cache(self):
        from surveys.llm_processors.prompt_cache import PromptCache

        persist_file = None
        if self.cache_dir:
            persist_file = self.cache_dir / "tier2_cache.json"
        return PromptCache(persist_file=persist_file)

    def process_batch(self, batch: "Batch") -> BatchProcessingResult:
        """Process a batch of variables.

        Args:
            batch: Batch object with tier=2 and list of variables.

        Returns:
            BatchProcessingResult with generated code for each variable.
        """
        if batch.tier != 2:
            raise ValueError(f"Expected tier=2 batch, got tier={batch.tier}")

        variables_data = self._build_variables_json(batch.variables)
        user_prompt = self._build_user_prompt(variables_data)

        response = self._call_llm(user_prompt)
        result = self._parse_response(response, batch.batch_index)

        if result.failed_vars and self.max_retries > 0:
            result = self._retry_failed(batch, result)

        return result

    def _build_variables_json(
        self,
        variables: list[tuple[str, "VariableSchema", "ClassificationResult"]],
    ) -> list[dict[str, Any]]:
        """Build JSON-serializable list of variable data."""
        result = []
        for clean_name, var_schema, classification in variables:
            var_data = {
                "clean_var_name": clean_name,
                "original_var_name": var_schema.var_name,
                "var_label": var_schema.var_label,
                "question_text": var_schema.question_text,
                "var_type": var_schema.var_type,
                "scale_type": var_schema.scale_type,
                "value_labels": [
                    {"value": vl.value, "label": vl.label, "is_missing": vl.is_missing}
                    for vl in var_schema.value_labels
                ],
                "missing_codes": var_schema.missing_codes,
                "range_min": var_schema.range_min,
                "range_max": var_schema.range_max,
                "classification": {
                    "tier": classification.tier,
                    "confidence": classification.confidence,
                    "reason": classification.reason,
                },
            }
            result.append(var_data)
        return result

    def _build_user_prompt(self, variables_data: list[dict]) -> str:
        """Build the user prompt with all variables."""
        return f"""Voici {len(variables_data)} variables à nettoyer.

Génère le code Python pour chaque variable en suivant les règles définies.

Variables:
```json
{json.dumps({"variables": variables_data}, ensure_ascii=False, indent=2)}
```

Retourne uniquement un objet JSON valide avec le code généré.
"""

    def _call_llm(self, user_prompt: str) -> str:
        """Call the LLM with system + user prompts."""
        try:
            import litellm
        except ImportError as e:
            raise ImportError("litellm is required for Tier2BatchProcessor") from e

        cached = self._cache.get(SYSTEM_PROMPT)
        if cached:
            return cached.content

        response = litellm.completion(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=self.temperature,
        )

        content = response.choices[0].message.content
        self._cache.set(
            SYSTEM_PROMPT,
            content,
            metadata={"model": self.model},
        )

        return content

    def _parse_response(
        self,
        response: str,
        batch_index: int,
    ) -> BatchProcessingResult:
        """Parse LLM response into VariableCode objects."""
        result = BatchProcessingResult(
            batch_index=batch_index,
            model_used=self.model,
        )

        try:
            data = json.loads(response)
            variables = data.get("variables", {})

            for clean_name, var_data in variables.items():
                try:
                    result.variables[clean_name] = VariableCode(
                        clean_var_name=clean_name,
                        original_var_name=var_data.get("original_variable", ""),
                        code=var_data.get("code", ""),
                        var_type=var_data.get("type", "unknown"),
                        value_labels=var_data.get("value_labels", {}),
                    )
                except Exception as e:
                    logger.warning(f"Failed to parse variable {clean_name}: {e}")
                    result.failed_vars.append(clean_name)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            result.failed_vars.extend(["batch_parse_error"])

        return result

    def _retry_failed(
        self,
        batch: "Batch",
        previous_result: BatchProcessingResult,
    ) -> BatchProcessingResult:
        """Retry failed variables individually."""
        failed_vars = [
            (name, var, result)
            for name, var, result in batch.variables
            if name in previous_result.failed_vars
        ]

        if not failed_vars:
            return previous_result

        logger.info(f"Retrying {len(failed_vars)} failed variables individually")

        for clean_name, var_schema, classification in failed_vars:
            single_data = self._build_variables_json(
                [(clean_name, var_schema, classification)]
            )
            user_prompt = self._build_user_prompt(single_data)

            try:
                response = self._call_llm(user_prompt)
                single_result = self._parse_response(response, batch.batch_index)

                if clean_name in single_result.variables:
                    previous_result.variables[clean_name] = single_result.variables[clean_name]
                    if clean_name in previous_result.failed_vars:
                        previous_result.failed_vars.remove(clean_name)
            except Exception as e:
                logger.warning(f"Retry failed for {clean_name}: {e}")
                if clean_name in previous_result.variables:
                    previous_result.variables[clean_name].error = str(e)

        return previous_result


def process_tier2_batch(
    batch: "Batch",
    model: Optional[str] = None,
    cache_dir: Optional[Path] = None,
) -> BatchProcessingResult:
    """Convenience function to process a single Tier 2 batch.

    Args:
        batch: Batch of variables to process.
        model: LLM model to use (default: opencode/glm-5-free).
        cache_dir: Directory for prompt cache persistence.

    Returns:
        BatchProcessingResult with generated code.
    """
    processor = Tier2BatchProcessor(model=model, cache_dir=cache_dir)
    return processor.process_batch(batch)
