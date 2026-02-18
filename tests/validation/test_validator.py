"""Tests for validation/validator.py"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from surveys.validation import CleanValidator, ValidationResult, ValidationIssue, Severity
from surveys.codebook_parser.schemas import VariableSchema, ValueLabel


class TestValidationIssue:
    def test_to_dict(self):
        issue = ValidationIssue(Severity.ERROR, "Q1", "TEST", "Test error", {"line": 10})
        d = issue.to_dict()
        assert d["severity"] == "error"
        assert d["variable_name"] == "Q1"
        assert d["code"] == "TEST"
        assert d["message"] == "Test error"
        assert d["details"] == {"line": 10}


class TestValidationResult:
    def test_empty_result_is_valid(self):
        result = ValidationResult()
        assert result.is_valid
        assert result.syntax_valid
        assert not result.has_errors
        assert not result.has_warnings

    def test_add_error_makes_invalid(self):
        result = ValidationResult()
        result.add_error("Q1", "TEST", "Test error")
        assert not result.is_valid
        assert result.has_errors
        assert len(result.errors) == 1
        assert result.flagged_variables == 1

    def test_add_warning_keeps_valid(self):
        result = ValidationResult()
        result.add_warning("Q1", "TEST", "Test warning")
        assert result.is_valid
        assert result.has_warnings
        assert len(result.warnings) == 1

    def test_syntax_error_makes_invalid(self):
        result = ValidationResult(syntax_valid=False)
        assert result.has_errors
        assert not result.is_valid

    def test_to_dict(self):
        result = ValidationResult()
        result.total_variables = 5
        result.add_error("Q1", "ERR", "Error")
        result.add_warning("Q2", "WARN", "Warning")
        d = result.to_dict()
        assert d["is_valid"] is False
        assert d["syntax_valid"] is True
        assert d["summary"]["total_variables"] == 5
        assert d["summary"]["n_errors"] == 1
        assert d["summary"]["n_warnings"] == 1


class TestCleanValidatorValidateCode:
    def test_valid_syntax(self):
        code = '''
import pandas as pd
import numpy as np

def clean(df):
    df_clean = pd.DataFrame(index=df.index)
    df_clean["op_q1"] = df["Q1"].map({1: "Yes", 2: "No"})
    return df_clean
'''
        validator = CleanValidator()
        result = validator.validate_code(code)
        assert result.syntax_valid
        assert result.is_valid

    def test_syntax_error(self):
        code = '''
def clean(df):
    df_clean["op_q1"] = df["Q1"  # missing bracket
'''
        validator = CleanValidator()
        result = validator.validate_code(code)
        assert not result.syntax_valid
        assert not result.is_valid
        assert any(e.code == "SYNTAX_ERROR" for e in result.errors)

    def test_duplicate_variable_assignment(self):
        code = '''
import pandas as pd

def clean(df):
    df_clean = pd.DataFrame(index=df.index)
    df_clean["op_q1"] = df["Q1"].map({1: "Yes", 2: "No"})
    df_clean["op_q1"] = df["Q1"].map({1: "Oui", 2: "Non"})  # duplicate!
    return df_clean
'''
        validator = CleanValidator()
        result = validator.validate_code(code)
        assert not result.is_valid
        assert any(e.code == "DUPLICATE_VARIABLE" for e in result.errors)
        assert any(e.variable_name == "op_q1" for e in result.errors)

    def test_missing_import_warning(self):
        code = '''
def clean(df):
    df_clean = pd.DataFrame(index=df.index)  # pd not imported
    return df_clean
'''
        validator = CleanValidator()
        result = validator.validate_code(code)
        assert any(w.code == "MISSING_IMPORT" for w in result.warnings)

    def test_missing_clean_function(self):
        code = '''
import pandas as pd

def process(df):
    return df
'''
        validator = CleanValidator()
        result = validator.validate_code(code)
        assert any(w.code == "MISSING_CLEAN_FUNCTION" for w in result.warnings)


class TestCleanValidatorValidateOutput:
    def test_valid_output(self):
        df_raw = pd.DataFrame({"Q1": [1, 2, 1, 2, 1]})
        df_clean = pd.DataFrame({"op_q1": [1.0, 2.0, 1.0, 2.0, 1.0]})

        validator = CleanValidator()
        result = validator.validate_output(df_clean, df_raw)

        assert result.is_valid

    def test_type_mismatch_warning(self):
        df_raw = pd.DataFrame({"Q1": [1, 2, 3, 4, 5]})
        df_clean = pd.DataFrame({"Q1": ["1", "2", "3", "4", "5"]})

        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Test",
            var_type="numeric",
        )

        validator = CleanValidator(variable_schemas=[var_schema])
        result = validator.validate_output(df_clean, df_raw)

        assert any(w.code == "TYPE_MISMATCH" for w in result.warnings)

    def test_out_of_range_warning(self):
        df_clean = pd.DataFrame({"Q1": [1, 2, 3, 4, 5, 6, 7, 8]})

        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Likert scale",
            var_type="ordinal",
            range_min=1.0,
            range_max=5.0,
        )

        validator = CleanValidator(variable_schemas=[var_schema])
        result = validator.validate_output(df_clean)

        assert any(w.code == "VALUE_ABOVE_MAX" for w in result.warnings)

    def test_below_min_warning(self):
        df_clean = pd.DataFrame({"Q1": [0, -1, 1, 2, 3, 4, 5]})

        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Likert scale",
            var_type="ordinal",
            range_min=1.0,
            range_max=5.0,
        )

        validator = CleanValidator(variable_schemas=[var_schema])
        result = validator.validate_output(df_clean)

        assert any(w.code == "VALUE_BELOW_MIN" for w in result.warnings)

    def test_empty_output_error(self):
        df_raw = pd.DataFrame({"Q1": [1, 2, 3, 4, 5]})
        df_clean = pd.DataFrame({"op_q1": [None, None, None, None, None]})

        validator = CleanValidator()
        result = validator.validate_output(df_clean, df_raw)

        assert any(e.code == "EMPTY_OUTPUT" for e in result.errors)


class TestCleanValidatorValidateVariable:
    def test_valid_variable(self):
        raw_series = pd.Series([1, 2, 1, 2, 1])
        clean_series = pd.Series([1.0, 2.0, 1.0, 2.0, 1.0])
        code = 'df_clean["op_q1"] = df["Q1"].map({1: 1.0, 2: 2.0})'

        validator = CleanValidator()
        validation = validator.validate_variable(
            "Q1", "op_q1", code, raw_series, clean_series
        )

        assert validation.is_valid
        assert validation.var_name == "Q1"
        assert validation.clean_var_name == "op_q1"

    def test_unmapped_values_warning(self):
        raw_series = pd.Series([1, 2, 3, 4, 5])
        clean_series = pd.Series([1.0, 2.0, None, 4.0, 5.0])
        code = 'df_clean["op_q1"] = df["Q1"].map({1: 1.0, 2: 2.0, 4: 4.0, 5: 5.0})'

        validator = CleanValidator()
        validation = validator.validate_variable(
            "Q1", "op_q1", code, raw_series, clean_series
        )

        unmapped_issues = [i for i in validation.issues if i.code == "UNMAPPED_VALUES"]
        assert len(unmapped_issues) == 1

    def test_out_of_range_detection(self):
        raw_series = pd.Series([1, 2, 3, 4, 5])
        clean_series = pd.Series([1.0, 2.0, 3.0, 4.0, 6.0])

        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Likert",
            var_type="ordinal",
            range_min=1.0,
            range_max=5.0,
        )

        validator = CleanValidator(variable_schemas=[var_schema])
        validation = validator.validate_variable(
            "Q1", "op_q1", "", raw_series, clean_series
        )

        range_issues = [i for i in validation.issues if i.code == "OUT_OF_RANGE"]
        assert len(range_issues) == 1
        assert 6.0 in validation.out_of_range_values

    def test_type_mismatch_error(self):
        raw_series = pd.Series([1, 2, 3, 4, 5])
        clean_series = pd.Series(["1", "2", "3", "4", "5"])

        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Numeric",
            var_type="numeric",
        )

        validator = CleanValidator(variable_schemas=[var_schema])
        validation = validator.validate_variable(
            "Q1", "op_q1", "", raw_series, clean_series
        )

        type_issues = [i for i in validation.issues if i.code == "TYPE_MISMATCH"]
        assert len(type_issues) == 1
        assert any(i.severity == Severity.ERROR for i in type_issues)


class TestCleanValidatorValidateCodeFile:
    def test_file_not_found(self, tmp_path):
        validator = CleanValidator()
        result = validator.validate_code_file(tmp_path / "nonexistent.py")
        assert not result.is_valid
        assert any(e.code == "FILE_NOT_FOUND" for e in result.errors)

    def test_valid_file(self, tmp_path):
        code = '''
import pandas as pd

def clean(df):
    df_clean = pd.DataFrame(index=df.index)
    return df_clean
'''
        code_file = tmp_path / "clean.py"
        code_file.write_text(code)

        validator = CleanValidator()
        result = validator.validate_code_file(code_file)

        assert result.syntax_valid
        assert result.is_valid
