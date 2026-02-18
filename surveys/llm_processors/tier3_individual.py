"""Tier 3 individual processor for complex survey variables.

Handles variables that require LLM interpretation:
- Non-standard coding schemes
- Complex conditional logic
- Variables with ambiguous mappings
- Codebook-data mismatches

Uses Claude Haiku via LiteLLM for cost efficiency (~$0.001/variable).
Each variable gets focused context (just its codebook snippet, not full codebook).
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("litellm").setLevel(logging.CRITICAL)

import litellm

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema
    from surveys.pattern_engine.patterns.base_pattern import ClassificationResult


TIER_3_MODEL = os.getenv("TIER_3_MODEL", "anthropic/claude-3-5-haiku-20241022")
TIER_3_MAX_TOKENS = 800


@dataclass
class Tier3Result:
    """Result of Tier 3 individual processing."""

    var_name: str
    python_code: str
    explanation: str
    confidence: float
    needs_review: bool
    error: Optional[str] = None


SYSTEM_PROMPT = """You are a survey data cleaning expert. Generate Python code to transform a raw survey variable into a cleaned standardized variable.

RULES:
1. Output ONLY valid Python code that can be inserted into a pandas DataFrame cleaning script
2. Use: df['{clean_var}'] = <transformation>
3. Handle missing codes (NSP, NR, Refus) by mapping to NaN
4. Add a brief comment explaining the transformation logic
5. If uncertain, set needs_review=True in your analysis

OUTPUT FORMAT (JSON):
{
  "python_code": "df['{clean_var}'] = ...",
  "explanation": "Brief explanation of the transformation",
  "confidence": 0.0-1.0,
  "needs_review": false
}
"""


def build_user_prompt(
    var_name: str,
    var: Optional["VariableSchema"],
    classification: "ClassificationResult",
    sample_values: list,
    clean_var_name: str,
    reason: Optional[str] = None,
    incorrect_code: Optional[str] = None,
) -> str:
    """Build focused prompt for a single variable."""
    parts = [f"Variable: {var_name}"]
    parts.append(f"Target cleaned name: {clean_var_name}")

    if reason or incorrect_code:
        parts.append("\n[ESCALATION CONTEXT]")
        if reason:
            parts.append(f"Reason: {reason}")
        if incorrect_code:
            parts.append(f"Previous code (incorrect):\n{incorrect_code}")
        parts.append("")

    if var:
        parts.append(f"\nLabel: {var.var_label}")
        parts.append(f"Type: {var.var_type}")

        if var.value_labels:
            parts.append("\nValue labels from codebook:")
            for vl in var.value_labels[:30]:
                missing_flag = " [MISSING]" if vl.is_missing else ""
                parts.append(f"  {vl.value} → {vl.label}{missing_flag}")
            if len(var.value_labels) > 30:
                parts.append(f"  ... and {len(var.value_labels) - 30} more")

        if var.missing_codes:
            parts.append(f"\nMissing codes: {var.missing_codes}")

        if var.range_min is not None or var.range_max is not None:
            parts.append(f"\nValid range: {var.range_min} to {var.range_max}")

        if var.question_text:
            parts.append(f"\nQuestion: {var.question_text[:200]}")

    parts.append(f"\nClassification reason: {classification.reason}")
    parts.append(f"\nSample values from data: {sample_values[:20]}")

    return "\n".join(parts)


def parse_llm_response(response_text: str, var_name: str) -> Tier3Result:
    """Parse LLM JSON response into Tier3Result."""
    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if not json_match:
        return Tier3Result(
            var_name=var_name,
            python_code=f"# ERROR: Could not parse LLM response for {var_name}",
            explanation="Failed to parse JSON from LLM response",
            confidence=0.0,
            needs_review=True,
            error="No JSON found in response",
        )

    try:
        data = json.loads(json_match.group())
        code = data.get("python_code", "")
        explanation = data.get("explanation", "")
        confidence = float(data.get("confidence", 0.5))
        needs_review = bool(data.get("needs_review", confidence < 0.7))

        if not code:
            code = f"# No code generated for {var_name}"
            needs_review = True

        return Tier3Result(
            var_name=var_name,
            python_code=code,
            explanation=explanation,
            confidence=confidence,
            needs_review=needs_review,
        )
    except json.JSONDecodeError as e:
        return Tier3Result(
            var_name=var_name,
            python_code=f"# ERROR: JSON decode error for {var_name}",
            explanation=f"JSON parse error: {e}",
            confidence=0.0,
            needs_review=True,
            error=str(e),
        )


def process_tier3_variable(
    var_name: str,
    var: Optional["VariableSchema"],
    classification: "ClassificationResult",
    sample_values: list,
    clean_var_name: Optional[str] = None,
    model: Optional[str] = None,
    reason: Optional[str] = None,
    incorrect_code: Optional[str] = None,
) -> Tier3Result:
    """Process a single Tier 3 variable with Claude Haiku.

    Args:
        var_name: Original variable name in raw data
        var: Parsed VariableSchema from codebook (optional)
        classification: ClassificationResult from pattern engine
        sample_values: Sample values from the actual data
        clean_var_name: Target standardized name (defaults to var_name)
        model: Override model (defaults to TIER_3_MODEL env var)
        reason: Optional reason for escalation (e.g., validation error message)
        incorrect_code: Optional incorrect code from previous tier

    Returns:
        Tier3Result with python_code, explanation, confidence, needs_review
    """
    clean_var = clean_var_name or var_name
    model = model or TIER_3_MODEL

    user_prompt = build_user_prompt(var_name, var, classification, sample_values, clean_var, reason=reason, incorrect_code=incorrect_code)

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=TIER_3_MAX_TOKENS,
            temperature=0.1,
        )

        response_text = response.choices[0].message.content or ""
        return parse_llm_response(response_text, var_name)

    except Exception as e:
        return Tier3Result(
            var_name=var_name,
            python_code=f"# ERROR: LLM call failed for {var_name}",
            explanation=f"LLM error: {e}",
            confidence=0.0,
            needs_review=True,
            error=str(e),
        )


def process_tier3_batch(
    variables: list[tuple[str, Optional["VariableSchema"], "ClassificationResult", list]],
    model: Optional[str] = None,
) -> list[Tier3Result]:
    """Process multiple Tier 3 variables individually.

    Args:
        variables: List of (var_name, var_schema, classification, sample_values)
        model: Override model

    Returns:
        List of Tier3Result for each variable
    """
    results = []
    for var_name, var, classification, sample_values in variables:
        result = process_tier3_variable(
            var_name=var_name,
            var=var,
            classification=classification,
            sample_values=sample_values,
            model=model,
        )
        results.append(result)
    return results
