"""Conflict Resolver - Detects and resolves conflicts between variables.

This module detects conflicts between variables such as:
- Recoded variables that are inconsistent with their original versions
- Contradictory missing codes between codebook and actual data
- Proposed automatic resolution when possible, otherwise flag for review
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import pandas as pd

from surveys.codebook_parser.schemas import VariableSchema


class ConflictType(Enum):
    RECODED_INCONSISTENCY = "recoded_inconsistency"
    MISSING_CODE_MISMATCH = "missing_code_mismatch"
    DUPLICATE_VARIABLE = "duplicate_variable"
    RANGE_OVERLAP = "range_overlap"
    VALUE_CONTRADICTION = "value_contradiction"


class ResolutionType(Enum):
    AUTO = "auto"
    MANUAL = "manual"
    IGNORE = "ignore"


@dataclass
class Conflict:
    """Represents a detected conflict between variables."""
    type: ConflictType
    variables: list[str]
    message: str
    severity: str = "warning"
    details: dict[str, Any] = field(default_factory=dict)
    resolution: Optional[ResolutionType] = None
    suggested_fix: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "variables": self.variables,
            "message": self.message,
            "severity": self.severity,
            "details": self.details,
            "resolution": self.resolution.value if self.resolution else None,
            "suggested_fix": self.suggested_fix,
        }


@dataclass
class ConflictReport:
    """Report of all detected conflicts."""
    conflicts: list[Conflict] = field(default_factory=list)
    auto_resolvable: int = 0
    manual_review_required: int = 0

    @property
    def has_conflicts(self) -> bool:
        return len(self.conflicts) > 0

    @property
    def total(self) -> int:
        return len(self.conflicts)

    def to_dict(self) -> dict:
        return {
            "total_conflicts": self.total,
            "auto_resolvable": self.auto_resolvable,
            "manual_review_required": self.manual_review_required,
            "conflicts": [c.to_dict() for c in self.conflicts],
        }


class ConflictResolver:
    """Detects and resolves conflicts between survey variables.

    Usage:
        resolver = ConflictResolver(codebook_variables=codebook.variables)
        report = resolver.detect_conflicts(df, var_states)
        
        # Get auto-resolvable conflicts
        auto = [c for c in report.conflicts if c.resolution == ResolutionType.AUTO]
    """

    COMMON_RECODES = {
        r"^op_": "",
        r"_recoded$": "",
        r"_cleaned$": "",
        r"_r$": "",
    }

    COMMON_MISSING_CODES = {98, 99, -1, -2, 97, 996, 997, 998, 999}

    def __init__(
        self,
        codebook_variables: Optional[list[VariableSchema]] = None,
    ):
        self.var_schemas: dict[str, VariableSchema] = {}
        if codebook_variables:
            self.var_schemas = {v.var_name: v for v in codebook_variables}

    def detect_conflicts(
        self,
        df: pd.DataFrame,
        var_states: dict[str, dict[str, Any]],
    ) -> ConflictReport:
        """Detect all conflicts in the dataset.

        Args:
            df: Raw DataFrame with original variables
            var_states: Variable states from cleaning (includes clean_var_name, code, etc.)

        Returns:
            ConflictReport with all detected conflicts
        """
        report = ConflictReport()

        self._detect_recoded_inconsistencies(df, var_states, report)
        self._detect_missing_code_conflicts(df, var_states, report)
        self._detect_duplicate_cleaning(df, var_states, report)
        self._detect_range_conflicts(df, var_states, report)

        return report

    def _detect_recoded_inconsistencies(
        self,
        df: pd.DataFrame,
        var_states: dict[str, dict[str, Any]],
        report: ConflictReport,
    ) -> None:
        """Detect inconsistencies between recoded and original variables."""
        cleaned_vars = {
            name: state for name, state in var_states.items()
            if state.get("status") == "done" and state.get("clean_var_name")
        }

        for var_name, state in cleaned_vars.items():
            clean_name = state.get("clean_var_name", "")

            original = self._find_original_variable(var_name, list(df.columns))
            if not original:
                continue

            if original not in df.columns:
                continue

            orig_values = set(df[original].dropna().unique())
            clean_values = set(df[clean_name].dropna().unique()) if clean_name in df.columns else set()

            if not orig_values or not clean_values:
                continue

            schema = self.var_schemas.get(var_name)
            if schema and schema.missing_codes:
                orig_values = orig_values - set(schema.missing_codes)

            unaccounted = orig_values - clean_values

            if unaccounted and len(unaccounted) > 0:
                if len(unaccounted) < len(orig_values) * 0.5:
                    conflict = Conflict(
                        type=ConflictType.RECODED_INCONSISTENCY,
                        variables=[var_name, clean_name],
                        message=f"Recoded variable '{clean_name}' missing values from '{var_name}'",
                        details={
                            "original_values": sorted(list(orig_values)),
                            "clean_values": sorted(list(clean_values)),
                            "unaccounted": sorted(list(unaccounted)),
                        },
                        severity="warning",
                        resolution=ResolutionType.MANUAL,
                    )
                    report.conflicts.append(conflict)
                    report.manual_review_required += 1
                else:
                    conflict = Conflict(
                        type=ConflictType.RECODED_INCONSISTENCY,
                        variables=[var_name, clean_name],
                        message=f"Major inconsistency: recoded variable '{clean_name}' has very different values from '{var_name}'",
                        details={
                            "original_count": len(orig_values),
                            "clean_count": len(clean_values),
                        },
                        severity="error",
                        resolution=ResolutionType.MANUAL,
                    )
                    report.conflicts.append(conflict)
                    report.manual_review_required += 1

    def _detect_missing_code_conflicts(
        self,
        df: pd.DataFrame,
        var_states: dict[str, dict[str, Any]],
        report: ConflictReport,
    ) -> None:
        """Detect contradictory missing codes between codebook and data."""
        for var_name, state in var_states.items():
            schema = self.var_schemas.get(var_name)
            if not schema:
                continue

            if var_name not in df.columns:
                continue

            data_values = set(df[var_name].dropna().unique())
            codebook_missing = set(schema.missing_codes) if schema.missing_codes else set()

            unexpected_missing = codebook_missing - self.COMMON_MISSING_CODES

            for code in unexpected_missing:
                if code in data_values:
                    count = (df[var_name] == code).sum()
                    if count > 0:
                        conflict = Conflict(
                            type=ConflictType.MISSING_CODE_MISMATCH,
                            variables=[var_name],
                            message=f"Code '{code}' in codebook missing codes but appears as valid value in data ({count} occurrences)",
                            details={"code": code, "count": count},
                            severity="warning",
                            resolution=ResolutionType.MANUAL,
                        )
                        report.conflicts.append(conflict)
                        report.manual_review_required += 1

            common_in_data = data_values & self.COMMON_MISSING_CODES - codebook_missing
            if common_in_data:
                conflict = Conflict(
                    type=ConflictType.MISSING_CODE_MISMATCH,
                    variables=[var_name],
                    message=f"Common missing codes {common_in_data} found in data but not in codebook missing_codes",
                    details={"missing_in_codebook": sorted(list(common_in_data))},
                    severity="info",
                    resolution=ResolutionType.AUTO,
                    suggested_fix=f"Add {common_in_data} to missing_codes for {var_name}",
                )
                report.conflicts.append(conflict)
                report.auto_resolvable += 1

    def _detect_duplicate_cleaning(
        self,
        df: pd.DataFrame,
        var_states: dict[str, dict[str, Any]],
        report: ConflictReport,
    ) -> None:
        """Detect variables that are cleaned multiple times."""
        clean_targets: dict[str, list[str]] = {}

        for var_name, state in var_states.items():
            if state.get("status") != "done":
                continue

            code = state.get("code", "")
            if not code:
                continue

            match = re.search(r'df_clean\[([\'"])(\w+)\1\]', code)
            if match:
                target = match.group(2)
                if target not in clean_targets:
                    clean_targets[target] = []
                clean_targets[target].append(var_name)

        for target, sources in clean_targets.items():
            if len(sources) > 1:
                conflict = Conflict(
                    type=ConflictType.DUPLICATE_VARIABLE,
                    variables=sources,
                    message=f"Variable '{target}' is being cleaned from multiple sources: {sources}",
                    severity="error",
                    resolution=ResolutionType.MANUAL,
                )
                report.conflicts.append(conflict)
                report.manual_review_required += 1

    def _detect_range_conflicts(
        self,
        df: pd.DataFrame,
        var_states: dict[str, dict[str, Any]],
        report: ConflictReport,
    ) -> None:
        """Detect range overlaps between different variables."""
        range_info: dict[str, tuple[float, float]] = {}

        for var_name, state in var_states.items():
            schema = self.var_schemas.get(var_name)
            if schema and schema.range_min is not None and schema.range_max is not None:
                range_info[var_name] = (schema.range_min, schema.range_max)

        var_names = list(range_info.keys())
        for i, var1 in enumerate(var_names):
            for var2 in var_names[i + 1:]:
                r1 = range_info[var1]
                r2 = range_info[var2]

                if r1[0] <= r2[0] <= r1[1] or r1[0] <= r2[1] <= r1[1]:
                    if var1 in df.columns and var2 in df.columns:
                        overlap = max(r1[0], r2[0]), min(r1[1], r2[1])
                        common_values = set(range(int(overlap[0]), int(overlap[1]) + 1))

                        actual_overlap = common_values & set(df[var1].dropna().unique()) & set(
                            df[var2].dropna().unique()
                        )

                        if actual_overlap:
                            conflict = Conflict(
                                type=ConflictType.RANGE_OVERLAP,
                                variables=[var1, var2],
                                message=f"Range overlap between '{var1}' [{r1[0]}-{r1[1]}] and '{var2}' [{r2[0]}-{r2[1]}]",
                                details={
                                    var1: r1,
                                    var2: r2,
                                    "overlap_range": list(overlap),
                                    "actual_overlap_values": sorted(list(actual_overlap)),
                                },
                                severity="info",
                                resolution=ResolutionType.IGNORE,
                            )
                            report.conflicts.append(conflict)

    def _find_original_variable(
        self, clean_var_name: str, all_columns: list[str]
    ) -> Optional[str]:
        """Find the original variable from a cleaned variable name."""
        for pattern, replacement in self.COMMON_RECODES.items():
            base = re.sub(pattern, replacement, clean_var_name.lower())
            for col in all_columns:
                if col.lower().replace("_", "") == base.replace("_", ""):
                    return col

        candidates = [c for c in all_columns if clean_var_name.lower().replace("op_", "") in c.lower()]
        return candidates[0] if candidates else None

    def resolve_conflict(self, conflict: Conflict) -> Optional[str]:
        """Attempt to automatically resolve a conflict.

        Returns:
            Resolution action or None if manual resolution required
        """
        if conflict.resolution == ResolutionType.AUTO:
            return conflict.suggested_fix

        if conflict.type == ConflictType.MISSING_CODE_MISMATCH:
            if conflict.suggested_fix:
                return conflict.suggested_fix

        return None


def detect_conflicts(
    df: pd.DataFrame,
    var_states: dict[str, dict[str, Any]],
    codebook_variables: Optional[list[VariableSchema]] = None,
) -> ConflictReport:
    """Convenience function to detect conflicts.

    Args:
        df: Raw DataFrame
        var_states: Variable states from cleaning
        codebook_variables: Optional codebook variables

    Returns:
        ConflictReport with detected conflicts
    """
    resolver = ConflictResolver(codebook_variables)
    return resolver.detect_conflicts(df, var_states)
