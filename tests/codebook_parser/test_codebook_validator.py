"""Tests for codebook_validator.py"""

import pytest
from typing import Optional

from surveys.codebook_parser.schemas import CodebookSchema, SurveyMetadata, VariableSchema, ValueLabel
from surveys.codebook_parser.validators.codebook_validator import (
    CodebookValidator,
    ValidationReport,
    Severity,
    ValidationError,
)


class TestValidationError:
    def test_to_dict(self):
        error = ValidationError(Severity.ERROR, "Q1", "DUPLICATE", "Duplicate variable")
        d = error.to_dict()
        assert d["severity"] == "error"
        assert d["variable_name"] == "Q1"
        assert d["code"] == "DUPLICATE"
        assert d["message"] == "Duplicate variable"


class TestValidationReport:
    def test_empty_report_is_valid(self):
        report = ValidationReport()
        assert report.is_valid
        assert not report.has_errors
        assert not report.has_warnings

    def test_add_error_makes_invalid(self):
        report = ValidationReport()
        report.add_error("Q1", "TEST", "Test error")
        assert not report.is_valid
        assert report.has_errors
        assert len(report.errors) == 1

    def test_add_warning(self):
        report = ValidationReport()
        report.add_warning("Q1", "TEST", "Test warning")
        assert report.is_valid
        assert report.has_warnings
        assert len(report.warnings) == 1

    def test_to_dict(self):
        report = ValidationReport()
        report.total_variables = 10
        report.add_error("Q1", "ERR", "Error")
        report.add_warning("Q2", "WARN", "Warning")
        d = report.to_dict()
        assert d["is_valid"] is False
        assert d["summary"]["total_variables"] == 10
        assert len(d["errors"]) == 1
        assert len(d["warnings"]) == 1


class TestCodebookValidator:
    def test_valid_codebook(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(
                    var_name="Q1",
                    var_label="Test question",
                    var_type="ordinal",
                    value_labels=[
                        ValueLabel(value=1, label="Strongly agree"),
                        ValueLabel(value=2, label="Agree"),
                        ValueLabel(value=3, label="Neutral"),
                        ValueLabel(value=4, label="Disagree"),
                        ValueLabel(value=5, label="Strongly disagree"),
                    ],
                    parser_confidence=1.0,
                )
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.is_valid
        assert len(report.errors) == 0
        assert report.total_variables == 1

    def test_variable_count_mismatch_missing(self):
        metadata = SurveyMetadata(
            survey_id="test",
            n_variables_declared=10,
        )
        codebook = self._create_test_codebook(
            metadata=metadata,
            variables=[
                VariableSchema(var_name=f"Q{i}", var_label=f"Question {i}", var_type="ordinal")
                for i in range(1, 8)
            ],
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.is_valid
        assert report.has_warnings
        assert any(w.code == "MISSING_VARIABLES" for w in report.warnings)

    def test_variable_count_mismatch_extra(self):
        metadata = SurveyMetadata(
            survey_id="test",
            n_variables_declared=3,
        )
        codebook = self._create_test_codebook(
            metadata=metadata,
            variables=[
                VariableSchema(var_name=f"Q{i}", var_label=f"Question {i}", var_type="ordinal")
                for i in range(1, 7)
            ],
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.is_valid
        assert report.has_warnings
        assert any(w.code == "EXTRA_VARIABLES" for w in report.warnings)

    def test_duplicate_variables(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(var_name="Q1", var_label="Question 1", var_type="ordinal"),
                VariableSchema(var_name="Q2", var_label="Question 2", var_type="ordinal"),
                VariableSchema(var_name="q1", var_label="Question 1 duplicate", var_type="ordinal"),
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert not report.is_valid
        assert any(e.code == "DUPLICATE_VARIABLE" for e in report.errors)

    def test_low_confidence_variables(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(var_name="Q1", var_label="Question 1", var_type="ordinal", parser_confidence=1.0),
                VariableSchema(var_name="Q2", var_label="Question 2", var_type="ordinal", parser_confidence=0.5),
                VariableSchema(var_name="Q3", var_label="Question 3", var_type="ordinal", parser_confidence=0.65),
            ]
        )

        validator = CodebookValidator(confidence_threshold=0.7)
        report = validator.validate(codebook)

        assert report.has_warnings
        low_conf_warnings = [w for w in report.warnings if w.code == "LOW_CONFIDENCE"]
        assert len(low_conf_warnings) == 2

    def test_missing_value_labels(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(var_name="Q1", var_label="Question 1", var_type="categorical", value_labels=[]),
                VariableSchema(var_name="Q2", var_label="Question 2", var_type="ordinal", value_labels=[]),
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.has_warnings
        assert any(w.code == "NO_VALUE_LABELS" for w in report.warnings)

    def test_range_consistency_mismatch(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(
                    var_name="Q1",
                    var_label="Question 1",
                    var_type="ordinal",
                    value_labels=[
                        ValueLabel(value=1, label="Low"),
                        ValueLabel(value=2, label="Medium"),
                        ValueLabel(value=3, label="High"),
                    ],
                    range_min=0.0,
                    range_max=4.0,
                )
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.has_warnings
        assert any(w.code == "RANGE_MIN_MISMATCH" for w in report.warnings)
        assert any(w.code == "RANGE_MAX_MISMATCH" for w in report.warnings)

    def test_value_coherence_unmapped_values(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(
                    var_name="Q1",
                    var_label="Question 1",
                    var_type="ordinal",
                    value_labels=[
                        ValueLabel(value=1, label="Low"),
                        ValueLabel(value=2, label="Medium"),
                        ValueLabel(value=3, label="High"),
                    ],
                )
            ]
        )

        validator = CodebookValidator(
            data_values_by_var={"q1": [1, 2, 3, 4, 5]}
        )
        report = validator.validate(codebook)

        assert report.has_warnings
        assert any(w.code == "UNMAPPED_VALUES" for w in report.warnings)

    def test_missing_var_name(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(var_name="", var_label="Question 1", var_type="ordinal"),
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert not report.is_valid
        assert any(e.code == "MISSING_VAR_NAME" for e in report.errors)

    def test_missing_var_label(self):
        codebook = self._create_test_codebook(
            variables=[
                VariableSchema(var_name="Q1", var_label="", var_type="ordinal"),
            ]
        )

        validator = CodebookValidator()
        report = validator.validate(codebook)

        assert report.has_warnings
        assert any(w.code == "MISSING_VAR_LABEL" for w in report.warnings)

    def _create_test_codebook(
        self, variables: list[VariableSchema], metadata: Optional[SurveyMetadata] = None
    ) -> CodebookSchema:
        if metadata is None:
            metadata = SurveyMetadata(survey_id="test")
        return CodebookSchema(metadata=metadata, variables=variables)
