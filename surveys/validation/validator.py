"""Clean.py Validator - Validates generated cleaning code.

This validator checks:
1. Python syntax validity (ast.parse)
2. All unique CSV values are covered in mappings
3. Column types match expectations
4. Ranges are valid (e.g., Likert 1-5 shouldn't have 6)
5. No duplicate variable cleaning
6. Output: errors/warnings/info per variable with severity levels
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import pandas as pd

import pandas as pd

from surveys.codebook_parser.schemas import VariableSchema


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    severity: Severity
    variable_name: Optional[str] = None
    code: str = ""
    message: str = ""
    details: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict:
        return {
            "severity": self.severity.value,
            "variable_name": self.variable_name,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class ValidationResult:
    is_valid: bool = True
    total_variables: int = 0
    passed_variables: int = 0
    flagged_variables: int = 0
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    info: list[ValidationIssue] = field(default_factory=list)
    syntax_valid: bool = True

    def __post_init__(self):
        if not self.syntax_valid:
            self.is_valid = False

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0 or not self.syntax_valid

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def add_error(self, variable_name: Optional[str], code: str, message: str, details: Optional[dict] = None):
        self.is_valid = False
        self.errors.append(ValidationIssue(Severity.ERROR, variable_name, code, message, details))
        if variable_name:
            self.flagged_variables += 1

    def add_warning(self, variable_name: Optional[str], code: str, message: str, details: Optional[dict] = None):
        self.warnings.append(ValidationIssue(Severity.WARNING, variable_name, code, message, details))
        if variable_name:
            self.flagged_variables += 1

    def add_info(self, variable_name: Optional[str], code: str, message: str, details: Optional[dict] = None):
        self.info.append(ValidationIssue(Severity.INFO, variable_name, code, message, details))

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "syntax_valid": self.syntax_valid,
            "summary": {
                "total_variables": self.total_variables,
                "passed_variables": self.passed_variables,
                "flagged_variables": self.flagged_variables,
                "n_errors": len(self.errors),
                "n_warnings": len(self.warnings),
                "n_info": len(self.info),
            },
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "info": [i.to_dict() for i in self.info],
        }


@dataclass
class VariableValidation:
    var_name: str
    clean_var_name: Optional[str] = None
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    mapped_values: set[Any] = field(default_factory=set)
    unmapped_values: set[Any] = field(default_factory=set)
    expected_type: Optional[str] = None
    actual_type: Optional[str] = None
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    out_of_range_values: set[Any] = field(default_factory=set)


class CleanValidator:
    """Validates generated clean.py code and its output.

    Usage:
        validator = CleanValidator(
            source_data=df_raw,
            variable_schemas=codebook.variables,
        )
        result = validator.validate_code(clean_py_path)
        result = validator.validate_output(df_clean)
    """

    def __init__(
        self,
        source_data: Optional[pd.DataFrame] = None,
        variable_schemas: Optional[list[VariableSchema]] = None,
        expected_ranges: Optional[dict[str, tuple[float, float]]] = None,
    ):
        self.source_data = source_data
        self.var_schemas = {v.var_name: v for v in variable_schemas} if variable_schemas else {}
        self.expected_ranges = expected_ranges or {}

    def validate_code(self, code: str) -> ValidationResult:
        """Validate Python syntax of generated clean.py."""
        result = ValidationResult()

        try:
            ast.parse(code)
        except SyntaxError as e:
            result.syntax_valid = False
            result.add_error(
                None,
                "SYNTAX_ERROR",
                f"Python syntax error at line {e.lineno}: {e.msg}",
                {"line": e.lineno, "offset": e.offset, "text": e.text},
            )
            return result

        self._check_duplicate_assignments(code, result)
        self._check_missing_imports(code, result)
        self._check_function_signature(code, result)

        return result

    def validate_code_file(self, path: Path) -> ValidationResult:
        """Validate a clean.py file."""
        if not path.exists():
            result = ValidationResult()
            result.add_error(None, "FILE_NOT_FOUND", f"File not found: {path}")
            return result

        with open(path) as f:
            code = f.read()
        return self.validate_code(code)

    def validate_output(
        self,
        df_clean: pd.DataFrame,
        df_raw: Optional[pd.DataFrame] = None,
    ) -> ValidationResult:
        """Validate cleaned DataFrame output."""
        result = ValidationResult()
        raw = df_raw if df_raw is not None else self.source_data

        if raw is None:
            result.add_warning(None, "NO_SOURCE_DATA", "No source data provided for comparison")

        result.total_variables = len(df_clean.columns)
        self._check_column_types(df_clean, result)
        self._check_ranges(df_clean, result)
        if raw is not None:
            self._check_value_coverage(df_clean, raw, result)

        result.passed_variables = result.total_variables - result.flagged_variables
        return result

    def validate_variable(
        self,
        var_name: str,
        clean_var_name: str,
        code: str,
        raw_series: pd.Series,
        clean_series: pd.Series,
    ) -> VariableValidation:
        """Validate a single variable transformation."""
        validation = VariableValidation(var_name=var_name, clean_var_name=clean_var_name)

        self._extract_mappings_from_code(code, validation)
        self._check_value_mapping(raw_series, validation)
        self._check_series_range(clean_series, validation)
        self._check_series_type(clean_series, validation)

        validation.is_valid = not any(
            issue.severity == Severity.ERROR for issue in validation.issues
        )
        return validation

    def _check_duplicate_assignments(self, code: str, result: ValidationResult):
        """Detect duplicate variable assignments in clean.py."""
        pattern = r"df_clean\[(['\"])(\w+)\1\]\s*="
        assignments: dict[str, list[int]] = {}

        for i, line in enumerate(code.split("\n"), 1):
            for match in re.finditer(pattern, line):
                var_name = match.group(2)
                if var_name not in assignments:
                    assignments[var_name] = []
                assignments[var_name].append(i)

        for var_name, lines in assignments.items():
            if len(lines) > 1:
                result.add_error(
                    var_name,
                    "DUPLICATE_VARIABLE",
                    f"Variable '{var_name}' is assigned multiple times",
                    {"lines": lines},
                )

    def _check_missing_imports(self, code: str, result: ValidationResult):
        """Check for required imports."""
        required = {"pandas", "numpy"}
        found_imports = set()

        for node in ast.walk(ast.parse(code)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found_imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    found_imports.add(node.module.split(".")[0])

        missing = required - found_imports
        if "pd" in code and "pandas" not in found_imports:
            missing.add("pandas")
        if "np" in code and "numpy" not in found_imports:
            missing.add("numpy")

        for pkg in missing:
            result.add_warning(None, "MISSING_IMPORT", f"Missing import: {pkg}")

    def _check_function_signature(self, code: str, result: ValidationResult):
        """Check that clean function has expected signature."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "clean":
                    args = [arg.arg for arg in node.args.args]
                    if not args or args[0] not in ("df", "data"):
                        result.add_warning(
                            None,
                            "FUNCTION_SIGNATURE",
                            "clean() function should take 'df' as first argument",
                        )
                    return
            result.add_warning(None, "MISSING_CLEAN_FUNCTION", "No clean() function found")
        except Exception:
            pass

    def _check_column_types(self, df_clean: pd.DataFrame, result: ValidationResult):
        """Check that column types are appropriate."""
        for col in df_clean.columns:
            schema = self.var_schemas.get(col)
            if not schema:
                continue

            dtype = df_clean[col].dtype
            expected_type = schema.var_type

            if expected_type in ("categorical", "ordinal"):
                if dtype == "object":
                    result.add_info(
                        col,
                        "TYPE_STRING",
                        f"Column '{col}' is string type, consider converting to category",
                    )
            elif expected_type == "numeric":
                if not pd.api.types.is_numeric_dtype(dtype):
                    result.add_warning(
                        col,
                        "TYPE_MISMATCH",
                        f"Expected numeric type for '{col}', got {dtype}",
                    )

    def _check_ranges(self, df_clean: pd.DataFrame, result: ValidationResult):
        """Check that values are within expected ranges."""
        for col in df_clean.columns:
            schema = self.var_schemas.get(col)
            range_info = self.expected_ranges.get(col)

            if not schema and not range_info:
                continue

            range_min = None
            range_max = None

            if schema:
                range_min = schema.range_min
                range_max = schema.range_max
            if range_info:
                range_min = range_min if range_min is not None else range_info[0]
                range_max = range_max if range_max is not None else range_info[1]

            if range_min is None and range_max is None:
                continue

            col_values = df_clean[col].dropna()
            if len(col_values) == 0:
                continue

            if range_min is not None:
                below_min = col_values[col_values < range_min]
                if len(below_min) > 0:
                    result.add_warning(
                        col,
                        "VALUE_BELOW_MIN",
                        f"Column '{col}' has {len(below_min)} values below min ({range_min})",
                        {"min": range_min, "sample_values": below_min.head(5).tolist()},
                    )

            if range_max is not None:
                above_max = col_values[col_values > range_max]
                if len(above_max) > 0:
                    result.add_warning(
                        col,
                        "VALUE_ABOVE_MAX",
                        f"Column '{col}' has {len(above_max)} values above max ({range_max})",
                        {"max": range_max, "sample_values": above_max.head(5).tolist()},
                    )

    def _check_value_coverage(
        self,
        df_clean: pd.DataFrame,
        df_raw: pd.DataFrame,
        result: ValidationResult,
    ):
        """Check that all source values are mapped."""
        raw_cols_lower = {c.lower(): c for c in df_raw.columns}

        for col in df_clean.columns:
            raw_col = col.replace("op_", "").replace("ses_", "")
            raw_col_actual = raw_cols_lower.get(raw_col.lower())
            if raw_col_actual is None:
                continue

            raw_values = set(df_raw[raw_col_actual].dropna().unique())
            clean_values = set(df_clean[col].dropna().unique())

            schema = self.var_schemas.get(col)
            if schema and schema.missing_codes:
                raw_values = raw_values - set(schema.missing_codes)

            raw_values.discard(None)

            if raw_values and not clean_values:
                result.add_error(
                    col,
                    "EMPTY_OUTPUT",
                    f"Column '{col}' has no values after cleaning",
                    {"raw_unique_count": len(raw_values)},
                )

    def _extract_mappings_from_code(self, code: str, validation: VariableValidation):
        """Extract value mappings from generated code."""
        mapping_pattern = r"(\d+(?:\.\d+)?)\s*:\s*['\"]?(\w+)['\"]?"
        for match in re.finditer(mapping_pattern, code):
            try:
                value = float(match.group(1))
                if value == int(value):
                    value = int(value)
                validation.mapped_values.add(value)
            except ValueError:
                pass

    def _check_value_mapping(self, raw_series: pd.Series, validation: VariableValidation):
        """Check if all raw values are mapped."""
        if not validation.mapped_values:
            return

        raw_unique = set(raw_series.dropna().unique())

        schema = self.var_schemas.get(validation.var_name)
        if schema and schema.missing_codes:
            raw_unique = raw_unique - set(schema.missing_codes)

        unmapped = raw_unique - validation.mapped_values
        if unmapped:
            validation.unmapped_values = unmapped
            validation.issues.append(
                ValidationIssue(
                    Severity.WARNING,
                    validation.var_name,
                    "UNMAPPED_VALUES",
                    f"{len(unmapped)} values not mapped: {sorted(list(unmapped))[:10]}",
                    {"unmapped_values": sorted(list(unmapped))},
                )
            )

    def _check_series_range(self, clean_series: pd.Series, validation: VariableValidation):
        """Check if values are within expected range."""
        schema = self.var_schemas.get(validation.var_name)
        if not schema:
            return

        range_min = schema.range_min
        range_max = schema.range_max

        if range_min is None and range_max is None:
            return

        values = clean_series.dropna()
        if not pd.api.types.is_numeric_dtype(values):
            return  # cannot compare ranges on non-numeric series

        out_of_range: set[Any] = set()

        if range_min is not None:
            out_of_range.update(values[values < range_min].unique())
        if range_max is not None:
            out_of_range.update(values[values > range_max].unique())

        if out_of_range:
            validation.out_of_range_values = out_of_range
            validation.issues.append(
                ValidationIssue(
                    Severity.WARNING,
                    validation.var_name,
                    "OUT_OF_RANGE",
                    f"{len(out_of_range)} values outside expected range [{range_min}, {range_max}]",
                    {"out_of_range": sorted(list(out_of_range))},
                )
            )

    def _check_series_type(self, clean_series: pd.Series, validation: VariableValidation):
        """Check series type matches expectations."""
        schema = self.var_schemas.get(validation.var_name)
        if not schema:
            return

        validation.expected_type = schema.var_type
        validation.actual_type = str(clean_series.dtype)

        if schema.var_type == "numeric":
            if not pd.api.types.is_numeric_dtype(clean_series):
                validation.issues.append(
                    ValidationIssue(
                        Severity.ERROR,
                        validation.var_name,
                        "TYPE_MISMATCH",
                        f"Expected numeric, got {clean_series.dtype}",
                    )
                )
