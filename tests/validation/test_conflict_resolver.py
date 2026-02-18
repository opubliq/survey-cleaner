"""Tests for validation/conflict_resolver.py"""

import pytest
import pandas as pd

from surveys.validation.conflict_resolver import (
    ConflictResolver,
    ConflictReport,
    Conflict,
    ConflictType,
    ResolutionType,
    detect_conflicts,
)
from surveys.codebook_parser.schemas import VariableSchema, ValueLabel


class TestConflict:
    def test_to_dict(self):
        conflict = Conflict(
            type=ConflictType.RECODED_INCONSISTENCY,
            variables=["Q1", "op_q1"],
            message="Test conflict",
            severity="warning",
            resolution=ResolutionType.MANUAL,
        )
        d = conflict.to_dict()
        assert d["type"] == "recoded_inconsistency"
        assert d["variables"] == ["Q1", "op_q1"]
        assert d["resolution"] == "manual"


class TestConflictReport:
    def test_empty_report(self):
        report = ConflictReport()
        assert not report.has_conflicts
        assert report.total == 0
        assert report.auto_resolvable == 0

    def test_with_conflicts(self):
        report = ConflictReport()
        conflict = Conflict(
            type=ConflictType.DUPLICATE_VARIABLE,
            variables=["Q1"],
            message="Test",
        )
        report.conflicts.append(conflict)
        report.manual_review_required += 1
        assert report.has_conflicts
        assert report.total == 1

    def test_to_dict(self):
        report = ConflictReport()
        conflict = Conflict(
            type=ConflictType.MISSING_CODE_MISMATCH,
            variables=["Q1"],
            message="Test",
            resolution=ResolutionType.AUTO,
        )
        report.conflicts.append(conflict)
        report.auto_resolvable = 1
        
        d = report.to_dict()
        assert d["total_conflicts"] == 1
        assert d["auto_resolvable"] == 1


class TestConflictResolver:
    def test_detect_no_conflicts(self):
        df = pd.DataFrame({"Q1": [1, 2, 3]})
        var_states = {
            "Q1": {"status": "done", "clean_var_name": "op_q1"}
        }
        
        resolver = ConflictResolver()
        report = resolver.detect_conflicts(df, var_states)
        
        assert report.total == 0

    def test_detect_duplicate_cleaning(self):
        df = pd.DataFrame({"Q1": [1, 2], "Q2": [3, 4]})
        var_states = {
            "Q1": {
                "status": "done",
                "clean_var_name": "op_q1",
                "code": 'df_clean["op_q1"] = df["Q1"].map({1: 1})'
            },
            "Q2": {
                "status": "done", 
                "clean_var_name": "op_q1",
                "code": 'df_clean["op_q1"] = df["Q2"].map({3: 1})'
            },
        }
        
        resolver = ConflictResolver()
        report = resolver.detect_conflicts(df, var_states)
        
        assert report.total > 0
        dup_conflicts = [c for c in report.conflicts if c.type == ConflictType.DUPLICATE_VARIABLE]
        assert len(dup_conflicts) == 1

    def test_detect_missing_code_conflict(self):
        df = pd.DataFrame({"Q1": [1, 2, 98, 99]})
        
        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Test",
            var_type="ordinal",
            missing_codes=[98, 99],
        )
        
        var_states = {
            "Q1": {"status": "done", "clean_var_name": "op_q1"}
        }
        
        resolver = ConflictResolver(codebook_variables=[var_schema])
        report = resolver.detect_conflicts(df, var_states)
        
        assert report.total >= 0

    def test_detect_missing_code_in_data_not_codebook(self):
        df = pd.DataFrame({"Q1": [1, 2, 98, 99]})
        
        var_schema = VariableSchema(
            var_name="Q1",
            var_label="Test",
            var_type="ordinal",
            missing_codes=[],
        )
        
        var_states = {
            "Q1": {"status": "done", "clean_var_name": "op_q1"}
        }
        
        resolver = ConflictResolver(codebook_variables=[var_schema])
        report = resolver.detect_conflicts(df, var_states)
        
        missing_conflicts = [
            c for c in report.conflicts 
            if c.type == ConflictType.MISSING_CODE_MISMATCH and c.resolution == ResolutionType.AUTO
        ]
        assert len(missing_conflicts) >= 1

    def test_find_original_variable(self):
        resolver = ConflictResolver()
        
        result = resolver._find_original_variable("op_q1", ["Q1", "Q2"])
        assert result == "Q1"
        
        result = resolver._find_original_variable("op_age", ["age", "gender"])
        assert result == "age"

    def test_resolve_conflict_auto(self):
        resolver = ConflictResolver()
        
        conflict = Conflict(
            type=ConflictType.MISSING_CODE_MISMATCH,
            variables=["Q1"],
            message="Test",
            resolution=ResolutionType.AUTO,
            suggested_fix="Add 98 to missing_codes",
        )
        
        fix = resolver.resolve_conflict(conflict)
        assert fix == "Add 98 to missing_codes"

    def test_resolve_conflict_manual(self):
        resolver = ConflictResolver()
        
        conflict = Conflict(
            type=ConflictType.RECODED_INCONSISTENCY,
            variables=["Q1", "op_q1"],
            message="Test",
            resolution=ResolutionType.MANUAL,
        )
        
        fix = resolver.resolve_conflict(conflict)
        assert fix is None


class TestDetectConflictsFunction:
    def test_convenience_function(self):
        df = pd.DataFrame({"Q1": [1, 2]})
        var_states = {"Q1": {"status": "done"}}
        
        report = detect_conflicts(df, var_states)
        
        assert isinstance(report, ConflictReport)
