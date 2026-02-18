"""Codebook Validator - Validates parsed codebook outputs.

This validator checks:
1. Pydantic schema validation (handled automatically by CodebookSchema)
2. Variable count consistency (declared vs parsed)
3. Value coherence (values in data vs codebook)
4. Variable duplicates and suspicious variables
5. Returns validation report with errors/warnings/info
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from ..schemas import CodebookSchema, VariableSchema


class Severity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """Single validation issue."""
    severity: Severity
    variable_name: Optional[str] = None
    code: str = ""
    message: str = ""

    def to_dict(self) -> dict:
        return {
            "severity": self.severity.value,
            "variable_name": self.variable_name,
            "code": self.code,
            "message": self.message,
        }


@dataclass
class ValidationReport:
    """Complete validation report for a parsed codebook."""
    is_valid: bool = True
    total_variables: int = 0
    ok_variables: int = 0
    problem_variables: int = 0
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    info: list[ValidationError] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def add_error(self, variable_name: Optional[str], code: str, message: str):
        self.is_valid = False
        self.errors.append(ValidationError(Severity.ERROR, variable_name, code, message))

    def add_warning(self, variable_name: Optional[str], code: str, message: str):
        self.warnings.append(ValidationError(Severity.WARNING, variable_name, code, message))

    def add_info(self, variable_name: Optional[str], code: str, message: str):
        self.info.append(ValidationError(Severity.INFO, variable_name, code, message))

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "summary": {
                "total_variables": self.total_variables,
                "ok_variables": self.ok_variables,
                "problem_variables": self.problem_variables,
            },
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [e.to_dict() for e in self.warnings],
            "info": [i.to_dict() for i in self.info],
        }


class CodebookValidator:
    """Validates parsed codebook outputs from LLM parsers.

    Usage:
        validator = CodebookValidator(data_values_by_var={"Q1": [1,2,3,1,2]})
        report = validator.validate(codebook)
        if not report.is_valid:
            print(f"Found {len(report.errors)} errors")
    """

    DEFAULT_CONFIDENCE_THRESHOLD = 0.7

    def __init__(
        self,
        data_values_by_var: Optional[dict[str, list]] = None,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    ):
        """Initialize validator.

        Args:
            data_values_by_var: Optional dict mapping variable names to lists of
                               values from actual data (for value coherence checks).
            confidence_threshold: Threshold for flagging low-confidence variables.
        """
        self.data_values_by_var = data_values_by_var or {}
        self.confidence_threshold = confidence_threshold

    def validate(self, codebook: CodebookSchema) -> ValidationReport:
        """Validate a complete parsed codebook.

        Args:
            codebook: Parsed codebook from CodebookParser.

        Returns:
            ValidationReport with all issues found.
        """
        report = ValidationReport()
        report.total_variables = len(codebook.variables)

        self._check_variable_count(codebook, report)
        self._check_duplicate_variables(codebook, report)
        self._check_low_confidence_variables(codebook, report)
        self._check_missing_value_labels(codebook, report)
        self._check_range_consistency(codebook, report)
        self._check_value_coherence(codebook, report)
        self._check_required_fields(codebook, report)

        report.ok_variables = report.total_variables - report.problem_variables
        return report

    def _check_variable_count(self, codebook: CodebookSchema, report: ValidationReport):
        """Check if parsed variable count matches declared count."""
        declared = codebook.metadata.n_variables_declared
        if declared is not None:
            parsed = len(codebook.variables)
            if parsed != declared:
                delta = declared - parsed
                if delta > 0:
                    report.add_warning(
                        None,
                        "MISSING_VARIABLES",
                        f"Codebook declares {declared} variables but {parsed} were parsed ({delta} missing)",
                    )
                else:
                    report.add_warning(
                        None,
                        "EXTRA_VARIABLES",
                        f"Codebook declares {declared} variables but {parsed} were parsed ({-delta} extra)",
                    )

    def _check_duplicate_variables(self, codebook: CodebookSchema, report: ValidationReport):
        """Check for duplicate variable names."""
        seen_names = {}
        for var in codebook.variables:
            var_name_lower = var.var_name.lower()
            if var_name_lower in seen_names:
                report.add_error(
                    var.var_name,
                    "DUPLICATE_VARIABLE",
                    f"Duplicate variable name (previous: {seen_names[var_name_lower]})",
                )
                report.problem_variables += 1
            else:
                seen_names[var_name_lower] = var.var_name

    def _check_low_confidence_variables(self, codebook: CodebookSchema, report: ValidationReport):
        """Flag variables with low parser confidence."""
        for var in codebook.variables:
            if var.parser_confidence < self.confidence_threshold:
                report.add_warning(
                    var.var_name,
                    "LOW_CONFIDENCE",
                    f"Parser confidence {var.parser_confidence:.2f} below threshold {self.confidence_threshold}",
                )
                report.problem_variables += 1

    def _check_missing_value_labels(self, codebook: CodebookSchema, report: ValidationReport):
        """Check for variables that should have value labels but don't."""
        for var in codebook.variables:
            if var.var_type in ("categorical", "ordinal"):
                if not var.value_labels:
                    report.add_warning(
                        var.var_name,
                        "NO_VALUE_LABELS",
                        f"Variable type '{var.var_type}' but no value labels defined",
                    )
                    report.problem_variables += 1

    def _check_range_consistency(self, codebook: CodebookSchema, report: ValidationReport):
        """Check if range_min/range_max are consistent with value_labels."""
        for var in codebook.variables:
            if var.value_labels and var.var_type in ("ordinal", "numeric"):
                valid_values = var.valid_values
                if valid_values:
                    actual_min = min(valid_values)
                    actual_max = max(valid_values)

                    if var.range_min is not None and abs(var.range_min - actual_min) > 1e-9:
                        report.add_warning(
                            var.var_name,
                            "RANGE_MIN_MISMATCH",
                            f"range_min={var.range_min} but value labels start at {actual_min}",
                        )

                    if var.range_max is not None and abs(var.range_max - actual_max) > 1e-9:
                        report.add_warning(
                            var.var_name,
                            "RANGE_MAX_MISMATCH",
                            f"range_max={var.range_max} but value labels end at {actual_max}",
                        )

    def _check_value_coherence(self, codebook: CodebookSchema, report: ValidationReport):
        """Check if values in data match values in codebook."""
        if not self.data_values_by_var:
            return

        for var in codebook.variables:
            var_name_lower = var.var_name.lower()
            if var_name_lower not in self.data_values_by_var:
                continue

            data_values = set(self.data_values_by_var[var_name_lower])
            codebook_values = set(var.all_values)

            in_data_not_codebook = data_values - codebook_values
            in_codebook_not_data = codebook_values - data_values

            if in_data_not_codebook:
                report.add_warning(
                    var.var_name,
                    "UNMAPPED_VALUES",
                    f"Values in data not in codebook: {sorted(in_data_not_codebook)[:10]}",
                )

            if in_codebook_not_data and len(in_codebook_not_data) < 10:
                report.add_info(
                    var.var_name,
                    "UNUSED_VALUES",
                    f"Values in codebook not in data: {sorted(in_codebook_not_data)}",
                )

    def _check_required_fields(self, codebook: CodebookSchema, report: ValidationReport):
        """Check that required fields are present."""
        for var in codebook.variables:
            if not var.var_name or not var.var_name.strip():
                report.add_error(
                    None,
                    "MISSING_VAR_NAME",
                    "Variable has empty or missing var_name",
                )

            if not var.var_label or not var.var_label.strip():
                report.add_warning(
                    var.var_name or "UNKNOWN",
                    "MISSING_VAR_LABEL",
                    "Variable has empty or missing var_label",
                )
