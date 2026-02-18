"""Tests for CodebookSchema and SurveyMetadata."""

import pytest
from pydantic import ValidationError

from surveys.codebook_parser.schemas import (
    CodebookSchema,
    SurveyMetadata,
    VariableSchema,
    ValueLabel,
)


# --- Fixtures ---

def make_var(name: str, label: str = "Label", n_values: int = 5) -> VariableSchema:
    return VariableSchema(
        var_name=name,
        var_label=label,
        var_type="ordinal",
        value_labels=[
            ValueLabel(value=i, label=f"Val {i}") for i in range(1, n_values + 1)
        ] + [ValueLabel(value=99, label="NR", is_missing=True)],
    )


def make_codebook(n_vars: int = 3, declared: int | None = None) -> CodebookSchema:
    meta = SurveyMetadata(
        survey_id="test_survey",
        n_variables_declared=declared,
    )
    variables = [make_var(f"Q{i}") for i in range(1, n_vars + 1)]
    return CodebookSchema(metadata=meta, variables=variables)


# --- SurveyMetadata ---

class TestSurveyMetadata:
    def test_required_survey_id(self):
        with pytest.raises(ValidationError):
            SurveyMetadata()

    def test_defaults(self):
        meta = SurveyMetadata(survey_id="ces_2019")
        assert meta.language == "fr"
        assert meta.n_variables_declared is None
        assert meta.notes is None

    def test_all_fields(self):
        meta = SurveyMetadata(
            survey_id="ces_2019",
            survey_name="Canadian Election Study 2019",
            year=2019,
            language="en",
            n_variables_declared=620,
            n_respondents=37822,
            source_file="ces_2019_codebook.pdf",
            source_format="pdf",
            parser_model="opencode/glm-5-free",
        )
        assert meta.year == 2019
        assert meta.n_respondents == 37822


# --- CodebookSchema: structure de base ---

class TestCodebookSchemaBasic:
    def test_empty_codebook(self):
        meta = SurveyMetadata(survey_id="test")
        cb = CodebookSchema(metadata=meta)
        assert cb.n_variables == 0
        assert cb.variable_names == []

    def test_n_variables(self):
        cb = make_codebook(n_vars=5)
        assert cb.n_variables == 5

    def test_variable_names(self):
        cb = make_codebook(n_vars=3)
        assert cb.variable_names == ["Q1", "Q2", "Q3"]


# --- CodebookSchema: get_variable ---

class TestGetVariable:
    def test_get_existing(self):
        cb = make_codebook(n_vars=3)
        var = cb.get_variable("Q2")
        assert var is not None
        assert var.var_name == "Q2"

    def test_get_case_insensitive(self):
        cb = make_codebook(n_vars=3)
        assert cb.get_variable("q1") is not None
        assert cb.get_variable("Q1") is not None

    def test_get_nonexistent_returns_none(self):
        cb = make_codebook(n_vars=3)
        assert cb.get_variable("Q99") is None


# --- CodebookSchema: variables_by_type ---

class TestVariablesByType:
    def test_filter_by_type(self):
        meta = SurveyMetadata(survey_id="test")
        vars_ = [
            VariableSchema(var_name="Q1", var_label="L", var_type="ordinal"),
            VariableSchema(var_name="Q2", var_label="L", var_type="categorical"),
            VariableSchema(var_name="Q3", var_label="L", var_type="ordinal"),
        ]
        cb = CodebookSchema(metadata=meta, variables=vars_)
        ordinals = cb.variables_by_type("ordinal")
        assert len(ordinals) == 2
        assert all(v.var_type == "ordinal" for v in ordinals)

    def test_filter_no_match(self):
        cb = make_codebook(n_vars=3)
        assert cb.variables_by_type("text") == []


# --- CodebookSchema: low_confidence_variables ---

class TestLowConfidenceVariables:
    def test_flags_low_confidence(self):
        meta = SurveyMetadata(survey_id="test")
        vars_ = [
            VariableSchema(var_name="Q1", var_label="L", parser_confidence=0.95),
            VariableSchema(var_name="Q2", var_label="L", parser_confidence=0.50),
            VariableSchema(var_name="Q3", var_label="L", parser_confidence=0.30),
        ]
        cb = CodebookSchema(metadata=meta, variables=vars_)
        low = cb.low_confidence_variables(threshold=0.7)
        assert len(low) == 2
        assert {v.var_name for v in low} == {"Q2", "Q3"}

    def test_all_high_confidence(self):
        cb = make_codebook(n_vars=3)  # default confidence=1.0
        assert cb.low_confidence_variables() == []


# --- CodebookSchema: validation count déclaré vs parsé ---

class TestVariableCountValidation:
    def test_count_matches_no_warning(self):
        cb = make_codebook(n_vars=3, declared=3)
        assert cb.metadata.notes is None

    def test_count_mismatch_adds_warning(self):
        cb = make_codebook(n_vars=3, declared=5)
        assert cb.metadata.notes is not None
        assert "WARNING" in cb.metadata.notes
        assert "5" in cb.metadata.notes  # declared
        assert "3" in cb.metadata.notes  # parsed

    def test_mismatch_appends_to_existing_notes(self):
        meta = SurveyMetadata(
            survey_id="test",
            n_variables_declared=10,
            notes="Note initiale du parser."
        )
        cb = CodebookSchema(metadata=meta, variables=[make_var("Q1")])
        assert "Note initiale" in cb.metadata.notes
        assert "WARNING" in cb.metadata.notes

    def test_no_declared_count_no_warning(self):
        cb = make_codebook(n_vars=3, declared=None)
        assert cb.metadata.notes is None
