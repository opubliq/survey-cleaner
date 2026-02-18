"""Tests for validation/quality_reporter.py"""

import pytest
import json
from pathlib import Path

from surveys.validation.quality_reporter import (
    QualityReporter,
    QualityReport,
    ReportFormat,
    TierStats,
    LLMCostStats,
)


class TestTierStats:
    def test_empty_stats(self):
        stats = TierStats()
        assert stats.percentage == 0.0
        assert stats.success_rate == 0.0

    def test_with_values(self):
        stats = TierStats(count=10, total=100, success=8, errors=2)
        assert stats.percentage == 10.0
        assert stats.success_rate == 80.0


class TestLLMCostStats:
    def test_empty_stats(self):
        stats = LLMCostStats()
        assert stats.token_accuracy == 0.0
        assert stats.cost_variance == 0.0

    def test_token_accuracy(self):
        stats = LLMCostStats(estimated_tokens=1000, actual_tokens=800)
        assert stats.token_accuracy == 0.8

    def test_cost_variance(self):
        stats = LLMCostStats(estimated_cost=1.0, actual_cost=1.2)
        assert abs(stats.cost_variance - 0.2) < 0.01


class TestQualityReport:
    def test_empty_report(self):
        report = QualityReport(survey_id="test")
        assert report.survey_id == "test"
        assert report.completion_rate == 0.0
        assert report.error_rate == 0.0
        assert report.overall_quality_score == 100.0

    def test_to_dict(self):
        report = QualityReport(survey_id="test", n_variables=100, variables_done=50)
        d = report.to_dict()
        assert d["survey_id"] == "test"
        assert d["completion_rate"] == 50.0

    def test_to_markdown(self):
        report = QualityReport(survey_id="test", n_variables=100, variables_done=75)
        md = report.to_markdown()
        assert "# Quality Report: test" in md
        assert "Completion | 75.0%" in md


class TestQualityReporter:
    def test_no_status_file(self, tmp_path):
        reporter = QualityReporter("test", status_file=tmp_path / "nonexistent.json")
        report = reporter.generate_report()
        assert report.survey_id == "test"

    def test_generate_report_with_state(self, tmp_path):
        status_file = tmp_path / "status.json"
        status_file.write_text(json.dumps({
            "surveys": {
                "test_survey": {
                    "status": "completed",
                    "n_variables": 100,
                    "n_observations": 500,
                    "variables": {
                        "Q1": {"status": "done", "tier": 1},
                        "Q2": {"status": "done", "tier": 2},
                        "Q3": {"status": "pending", "tier": 3},
                    }
                }
            }
        }))

        reporter = QualityReporter("test_survey", status_file=status_file)
        report = reporter.generate_report()

        assert report.survey_id == "test_survey"
        assert report.survey_status == "completed"
        assert report.n_variables == 100
        assert report.variables_done == 2
        assert report.variables_pending == 1

    def test_tier_stats_calculated(self, tmp_path):
        status_file = tmp_path / "status.json"
        status_file.write_text(json.dumps({
            "surveys": {
                "test": {
                    "status": "completed",
                    "n_variables": 10,
                    "variables": {
                        f"Q{i}": {"status": "done", "tier": i % 3 + 1}
                        for i in range(1, 11)
                    }
                }
            }
        }))

        reporter = QualityReporter("test", status_file=status_file)
        report = reporter.generate_report()

        assert 1 in report.tier_stats
        assert 2 in report.tier_stats
        assert 3 in report.tier_stats
        assert report.tier_stats[2].count == 4

    def test_generate_and_save_markdown(self, tmp_path):
        status_file = tmp_path / "status.json"
        status_file.write_text(json.dumps({
            "surveys": {
                "test": {
                    "status": "completed",
                    "n_variables": 5,
                    "variables": {
                        "Q1": {"status": "done", "tier": 1},
                    }
                }
            }
        }))

        output_dir = tmp_path / "output"
        reporter = QualityReporter("test", status_file=status_file)
        path = reporter.generate_and_save(output_dir, ReportFormat.MARKDOWN)

        assert path.exists()
        content = path.read_text()
        assert "# Quality Report: test" in content

    def test_generate_and_save_json(self, tmp_path):
        status_file = tmp_path / "status.json"
        status_file.write_text(json.dumps({
            "surveys": {
                "test": {
                    "status": "completed",
                    "n_variables": 5,
                    "variables": {}
                }
            }
        }))

        output_dir = tmp_path / "output"
        reporter = QualityReporter("test", status_file=status_file)
        path = reporter.generate_and_save(output_dir, ReportFormat.JSON)

        assert path.exists()
        data = json.loads(path.read_text())
        assert data["survey_id"] == "test"
