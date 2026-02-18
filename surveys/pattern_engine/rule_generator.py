"""Rule generator - generates Python cleaning code from patterns + codebook.

This module takes a matched pattern (from PatternMatcher) and a codebook entry,
and produces valid Python code ready to insert into a clean.py script.

The generator:
1. Reads the transformation_template from the pattern
2. Extracts value labels from the codebook (excluding missing codes)
3. Fills in template placeholders: {original_var}, {clean_var}, {mapping}
4. Handles missing codes (98, 99, -1, etc.) by excluding them from mappings
5. Supports scale patterns (no mapping) and categorical patterns (with mapping)

Example output:
    df['satisfaction'] = df['Q5_satisfaction'].map({1: 'Très satisfait', ...})
    df['satisfaction'] = df['satisfaction'].astype('category')
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from surveys.pattern_engine.schemas.pattern_schema import Pattern

if TYPE_CHECKING:
    from surveys.codebook_parser.schemas.variable_schema import VariableSchema
    from surveys.pattern_engine.pattern_matcher import MatchResult


@dataclass
class GeneratedRule:
    code: str
    pattern_id: str
    pattern_name: str
    original_var: str
    clean_var: str
    has_missing_codes: bool = False
    missing_codes_handled: list[int | float] | None = None


class RuleGenerator:
    pattern: Pattern
    codebook_entry: Optional[Union["VariableSchema", dict]]

    def generate(
        self,
        pattern: Pattern,
        original_var: str,
        clean_var: str,
        codebook_entry: Optional[Union["VariableSchema", dict]] = None,
    ) -> GeneratedRule:
        self.pattern = pattern
        self.codebook_entry = codebook_entry

        template = pattern.transformation_template

        mapping = self._build_mapping(codebook_entry)
        missing_codes = self._get_missing_codes(codebook_entry)

        if "{mapping}" in template:
            mapping_str = self._format_mapping(mapping)
            code = template.format(
                original_var=original_var,
                clean_var=clean_var,
                mapping=mapping_str,
            )
        else:
            code = template.format(
                original_var=original_var,
                clean_var=clean_var,
            )

        if missing_codes and not self._template_handles_missing(template):
            code = self._add_missing_code_handling(code, clean_var, missing_codes)

        header = f"# {pattern.pattern_name} ({pattern.pattern_id})"
        code = f"{header}\n{code}"

        return GeneratedRule(
            code=code,
            pattern_id=pattern.pattern_id,
            pattern_name=pattern.pattern_name,
            original_var=original_var,
            clean_var=clean_var,
            has_missing_codes=bool(missing_codes),
            missing_codes_handled=missing_codes if missing_codes else None,
        )

    def generate_from_match(
        self,
        match_result: "MatchResult",
        original_var: str,
        clean_var: str,
        codebook_entry: Optional[Union["VariableSchema", dict]] = None,
    ) -> GeneratedRule:
        return self.generate(
            pattern=match_result.pattern,
            original_var=original_var,
            clean_var=clean_var,
            codebook_entry=codebook_entry,
        )

    def _build_mapping(
        self,
        codebook_entry: Optional[Union["VariableSchema", dict]],
    ) -> dict[int | float, str]:
        if codebook_entry is None:
            return {}

        value_labels: list

        if hasattr(codebook_entry, "value_labels"):
            value_labels = codebook_entry.value_labels
        elif isinstance(codebook_entry, dict):
            value_labels = codebook_entry.get("value_labels", [])
        else:
            return {}

        mapping = {}
        for vl in value_labels:
            if hasattr(vl, "is_missing") and hasattr(vl, "value") and hasattr(vl, "label"):
                if not vl.is_missing:
                    mapping[vl.value] = vl.label
            elif isinstance(vl, dict):
                if not vl.get("is_missing", False):
                    mapping[vl.get("value")] = vl.get("label", "")

        return mapping

    def _get_missing_codes(
        self,
        codebook_entry: Optional[Union["VariableSchema", dict]],
    ) -> list[int | float]:
        if codebook_entry is None:
            return []

        if hasattr(codebook_entry, "missing_codes"):
            return list(codebook_entry.missing_codes)
        elif isinstance(codebook_entry, dict):
            return codebook_entry.get("missing_codes", [])

        return []

    def _format_mapping(self, mapping: dict[int | float, str]) -> str:
        if not mapping:
            return "{}"

        items = []
        for key in sorted(mapping.keys(), key=lambda x: (isinstance(x, float), x)):
            value = mapping[key]
            items.append(f"{key}: {value!r}")

        return "{" + ", ".join(items) + "}"

    def _template_handles_missing(self, template: str) -> bool:
        missing_indicators = [
            "df.loc[",
            "| (df['",
            "df['{clean_var}'] < 0",
            "df['{clean_var}'] >",
        ]
        return any(ind in template for ind in missing_indicators)

    def _add_missing_code_handling(
        self,
        code: str,
        clean_var: str,
        missing_codes: list[int | float],
    ) -> str:
        if not missing_codes:
            return code

        codes_str = ", ".join(str(c) for c in sorted(set(missing_codes)))
        missing_line = f"df.loc[df['{clean_var}'].isin([{codes_str}]), '{clean_var}'] = None  # Missing codes"

        return f"{code}\n{missing_line}"


def generate_rule(
    pattern: Pattern,
    original_var: str,
    clean_var: str,
    codebook_entry: Optional[Union["VariableSchema", dict]] = None,
) -> GeneratedRule:
    generator = RuleGenerator()
    return generator.generate(pattern, original_var, clean_var, codebook_entry)


def generate_rule_from_match(
    match_result: "MatchResult",
    original_var: str,
    clean_var: str,
    codebook_entry: Optional[Union["VariableSchema", dict]] = None,
) -> GeneratedRule:
    generator = RuleGenerator()
    return generator.generate_from_match(match_result, original_var, clean_var, codebook_entry)
