"""Tests for VariableSchema and ValueLabel."""

import pytest
from pydantic import ValidationError

from surveys.codebook_parser.schemas import VariableSchema, ValueLabel


# --- Fixtures ---

def make_likert5_var(**kwargs) -> VariableSchema:
    """Standard Likert 5 points variable for reuse across tests."""
    defaults = dict(
        var_name="Q12",
        var_label="Satisfaction envers le gouvernement",
        var_type="ordinal",
        value_labels=[
            ValueLabel(value=1, label="Très satisfait"),
            ValueLabel(value=2, label="Satisfait"),
            ValueLabel(value=3, label="Insatisfait"),
            ValueLabel(value=4, label="Très insatisfait"),
            ValueLabel(value=98, label="NSP", is_missing=True),
            ValueLabel(value=99, label="NR", is_missing=True),
        ],
    )
    defaults.update(kwargs)
    return VariableSchema(**defaults)


# --- ValueLabel ---

class TestValueLabel:
    def test_basic(self):
        vl = ValueLabel(value=1, label="Oui")
        assert vl.value == 1
        assert vl.label == "Oui"
        assert vl.is_missing is False

    def test_missing_flag(self):
        vl = ValueLabel(value=99, label="NR", is_missing=True)
        assert vl.is_missing is True

    def test_float_value(self):
        vl = ValueLabel(value=1.5, label="Milieu")
        assert vl.value == 1.5


# --- VariableSchema: champs de base ---

class TestVariableSchemaBasic:
    def test_required_fields(self):
        var = VariableSchema(var_name="Q1", var_label="Question 1")
        assert var.var_name == "Q1"
        assert var.var_label == "Question 1"

    def test_missing_var_name_raises(self):
        with pytest.raises(ValidationError):
            VariableSchema(var_label="Question sans nom")

    def test_missing_var_label_raises(self):
        with pytest.raises(ValidationError):
            VariableSchema(var_name="Q1")

    def test_defaults(self):
        var = VariableSchema(var_name="Q1", var_label="Q")
        assert var.var_type == "unknown"
        assert var.scale_type is None
        assert var.value_labels == []
        assert var.missing_codes == []
        assert var.parser_confidence == 1.0

    def test_invalid_var_type_raises(self):
        with pytest.raises(ValidationError):
            VariableSchema(var_name="Q1", var_label="Q", var_type="invalid_type")

    def test_confidence_out_of_range_raises(self):
        with pytest.raises(ValidationError):
            VariableSchema(var_name="Q1", var_label="Q", parser_confidence=1.5)
        with pytest.raises(ValidationError):
            VariableSchema(var_name="Q1", var_label="Q", parser_confidence=-0.1)


# --- VariableSchema: propriétés dérivées ---

class TestVariableSchemaProperties:
    def test_valid_values_excludes_missing(self):
        var = make_likert5_var()
        assert var.valid_values == [1, 2, 3, 4]

    def test_all_values_includes_missing(self):
        var = make_likert5_var()
        assert var.all_values == [1, 2, 3, 4, 98, 99]

    def test_missing_codes_auto_derived(self):
        var = make_likert5_var()
        assert var.missing_codes == [98, 99]

    def test_missing_codes_explicit_overrides(self):
        """Si missing_codes est explicitement fourni, il est utilisé tel quel."""
        var = make_likert5_var(missing_codes=[-1])
        assert var.missing_codes == [-1]

    def test_range_auto_derived(self):
        var = make_likert5_var()
        assert var.range_min == 1
        assert var.range_max == 4

    def test_range_explicit_overrides(self):
        var = make_likert5_var(range_min=0, range_max=10)
        assert var.range_min == 0
        assert var.range_max == 10

    def test_no_value_labels_no_range(self):
        var = VariableSchema(var_name="Q1", var_label="Q")
        assert var.range_min is None
        assert var.range_max is None

    def test_all_missing_codes_no_valid_range(self):
        """Variable avec seulement des codes manquants → range None."""
        var = VariableSchema(
            var_name="Q1",
            var_label="Q",
            value_labels=[
                ValueLabel(value=98, label="NSP", is_missing=True),
                ValueLabel(value=99, label="NR", is_missing=True),
            ]
        )
        assert var.valid_values == []
        assert var.range_min is None
        assert var.range_max is None


# --- VariableSchema: cas réels de sondages ---

class TestVariableSchemaRealCases:
    def test_binary_yes_no(self):
        var = VariableSchema(
            var_name="VOTE",
            var_label="A voté aux dernières élections",
            var_type="categorical",
            scale_type="binary",
            value_labels=[
                ValueLabel(value=1, label="Oui"),
                ValueLabel(value=2, label="Non"),
                ValueLabel(value=9, label="Refus", is_missing=True),
            ]
        )
        assert var.valid_values == [1, 2]
        assert var.missing_codes == [9]

    def test_province_demographic(self):
        var = VariableSchema(
            var_name="PROV",
            var_label="Province de résidence",
            var_type="categorical",
            scale_type="demographic",
            value_labels=[
                ValueLabel(value=24, label="Québec"),
                ValueLabel(value=35, label="Ontario"),
                ValueLabel(value=59, label="Colombie-Britannique"),
            ]
        )
        assert len(var.valid_values) == 3
        assert var.missing_codes == []

    def test_thermometer_scale(self):
        var = VariableSchema(
            var_name="THERM_CAQ",
            var_label="Thermomètre - Coalition Avenir Québec",
            var_type="numeric",
            scale_type="thermometer",
            range_min=0,
            range_max=100,
            value_labels=[
                ValueLabel(value=998, label="NSP", is_missing=True),
                ValueLabel(value=999, label="NR", is_missing=True),
            ]
        )
        assert var.range_min == 0
        assert var.range_max == 100
        assert var.missing_codes == [998, 999]

    def test_low_confidence_flag(self):
        var = make_likert5_var(parser_confidence=0.45)
        assert var.parser_confidence == 0.45
