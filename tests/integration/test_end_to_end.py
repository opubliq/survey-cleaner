"""Integration tests for end-to-end Survey Cleaner workflow.

Tests the complete pipeline:
1. Load dataset (CSV)
2. Parse codebook (CSV → JSON)
3. Classify variables (Pattern Engine Tier 1/2/3)
4. Generate rules for Tier 1 variables
5. Validate outputs
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from surveys.codebook_parser.parser import CodebookParser
from surveys.pattern_engine import classify
from surveys.pattern_engine.rule_generator import generate_rule


TEST_DATA_DIR = Path(__file__).parent.parent


class TestEndToEndWorkflow:
    """End-to-end integration tests."""

    @pytest.fixture
    def survey_df(self) -> pd.DataFrame:
        """Load test survey data."""
        csv_path = TEST_DATA_DIR / "test_survey.csv"
        return pd.read_csv(csv_path)

    @pytest.fixture
    def codebook(self):
        """Parse test codebook."""
        md_path = TEST_DATA_DIR / "test_codebook.md"
        parser = CodebookParser(
            survey_id="test_survey",
            data_dir=TEST_DATA_DIR,
            codebook_path=md_path,
        )
        return parser.parse()

    def test_load_survey_csv(self, survey_df: pd.DataFrame):
        """Test loading survey CSV."""
        assert len(survey_df) == 20
        assert len(survey_df.columns) == 11
        assert "nom" in survey_df.columns
        assert "age" in survey_df.columns

    def test_parse_codebook_csv(self, codebook):
        """Test parsing codebook CSV to JSON."""
        assert codebook is not None
        variables = codebook.variables
        assert len(variables) == 11

        var_names = [v.var_name for v in variables]
        assert "age" in var_names
        assert "sexe" in var_names
        assert "opinion_immigration" in var_names

    def test_classify_all_variables(self, survey_df: pd.DataFrame, codebook):
        """Test classification of all variables."""
        var_map = {v.var_name: v for v in codebook.variables}

        classifications = []
        for col in survey_df.columns:
            series = survey_df[col]
            var_schema = var_map.get(col)

            result = classify(series, var_schema)

            classifications.append({
                "var_name": col,
                "tier": result.tier,
                "pattern_id": result.pattern_id,
                "confidence": result.confidence,
                "reason": result.reason,
            })

        assert len(classifications) == 11

        tier_counts = {}
        for c in classifications:
            tier_counts[c["tier"]] = tier_counts.get(c["tier"], 0) + 1

        assert tier_counts.get(1, 0) > 0, "Should have at least some Tier 1 variables"
        assert tier_counts.get(2, 0) > 0, "Should have at least some Tier 2 variables"

    def test_classify_likert_variables(self, survey_df: pd.DataFrame, codebook):
        """Test classification of Likert variables."""
        var_map = {v.var_name: v for v in codebook.variables}

        likert_vars = ["opinion_immigration", "opinion_economie",
                       "opinion_environnement", "satisfaction_gouv"]

        for var_name in likert_vars:
            series = survey_df[var_name]
            var_schema = var_map.get(var_name)
            result = classify(series, var_schema)

            assert result.tier in [1, 2], f"{var_name} should be Tier 1 or 2"
            assert result.pattern_id is not None, f"{var_name} should have a pattern"
            assert result.confidence > 0, f"{var_name} should have confidence > 0"

    def test_classify_demographic_variables(self, survey_df: pd.DataFrame, codebook):
        """Test classification of demographic variables."""
        var_map = {v.var_name: v for v in codebook.variables}

        demo_vars = ["sexe", "education", "region"]

        for var_name in demo_vars:
            series = survey_df[var_name]
            var_schema = var_map.get(var_name)
            result = classify(series, var_schema)

            assert result.tier in [1, 2], f"{var_name} should be Tier 1 or 2"
            assert result.pattern_id is not None, f"{var_name} should have a pattern"

    def test_classify_text_variable(self, survey_df: pd.DataFrame, codebook):
        """Test classification of text variable (should be Tier 2 or 3)."""
        var_map = {v.var_name: v for v in codebook.variables}

        series = survey_df["nom"]
        var_schema = var_map.get("nom")
        result = classify(series, var_schema)

        assert result.tier in [2, 3], "Text variable should be Tier 2 or 3"
        assert result.pattern_id is not None, "Should have a pattern"

    def test_rule_generation_for_tier1(self, survey_df: pd.DataFrame, codebook):
        """Test that Tier 1 variables can be identified for rule generation."""
        from surveys.pattern_engine.patterns import get_all_patterns

        var_map = {v.var_name: v for v in codebook.variables}

        patterns = get_all_patterns()
        assert len(patterns) > 0, "Should have pattern classes available"

        tier1_vars = []
        likert_vars = ["opinion_immigration", "opinion_economie"]
        for var_name in likert_vars:
            series = survey_df[var_name]
            var_schema = var_map.get(var_name)
            result = classify(series, var_schema)

            if result.tier == 1 and result.pattern_id:
                tier1_vars.append(var_name)

        assert len(tier1_vars) > 0, "Should have at least one Tier 1 variable for rule generation"

    def test_missing_code_detection(self, survey_df: pd.DataFrame, codebook):
        """Test that missing codes are detected and handled."""
        var_map = {v.var_name: v for v in codebook.variables}

        likert_vars = ["opinion_immigration", "opinion_economie"]

        for var_name in likert_vars:
            series = survey_df[var_name]
            var_schema = var_map.get(var_name)
            result = classify(series, var_schema)

            assert result.missing_codes is not None
            assert result.effective_n_unique > 0

    def test_no_import_errors(self):
        """Test that all required modules can be imported."""
        from surveys.codebook_parser.parser import CodebookParser
        from surveys.pattern_engine import classify, get_all_patterns
        from surveys.pattern_engine.pattern_matcher import PatternMatcher
        from surveys.pattern_engine.rule_generator import generate_rule
        from surveys.orchestrator import SurveyState, VariableState

        assert CodebookParser is not None
        assert classify is not None
        assert get_all_patterns is not None
        assert PatternMatcher is not None
        assert generate_rule is not None
        assert SurveyState is not None
        assert VariableState is not None


class TestPerformanceRequirements:
    """Test performance requirements."""

    def test_classification_performance(self):
        """Test that classification is fast (<30s for ~100 vars)."""
        import time

        csv_path = TEST_DATA_DIR / "test_survey.csv"
        df = pd.read_csv(csv_path)

        codebook_md = TEST_DATA_DIR / "test_codebook.md"
        codebook = CodebookParser(
            survey_id="test_survey",
            data_dir=TEST_DATA_DIR,
            codebook_path=codebook_md,
        ).parse()
        var_map = {v.var_name: v for v in codebook.variables}

        start = time.time()
        for col in df.columns:
            classify(df[col], var_map.get(col))
        elapsed = time.time() - start

        assert elapsed < 5, f"Classification took {elapsed:.2f}s, should be < 5s"
