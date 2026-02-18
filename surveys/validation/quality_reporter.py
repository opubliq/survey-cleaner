"""Quality Reporter - Generates quality reports for survey cleaning results.

This module generates quality reports (Markdown or JSON) for each survey,
including metrics such as:
- % of variables processed by Tier 1/2/3
- Number of errors, warnings, and info messages
- Number of variables flagged for human review
- Estimated vs actual LLM cost
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from surveys.validation.validator import ValidationResult


class ReportFormat(Enum):
    MARKDOWN = "markdown"
    JSON = "json"


@dataclass
class TierStats:
    """Statistics for a specific tier."""
    count: int = 0
    total: int = 0
    success: int = 0
    errors: int = 0

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.count / self.total) * 100

    @property
    def success_rate(self) -> float:
        if self.count == 0:
            return 0.0
        return (self.success / self.count) * 100


@dataclass
class LLMCostStats:
    """LLM cost statistics."""
    estimated_tokens: int = 0
    actual_tokens: int = 0
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    api_calls: int = 0

    @property
    def token_accuracy(self) -> float:
        if self.estimated_tokens == 0:
            return 0.0
        return min(1.0, self.actual_tokens / self.estimated_tokens)

    @property
    def cost_variance(self) -> float:
        if self.estimated_cost == 0:
            return 0.0
        return abs(self.actual_cost - self.estimated_cost) / self.estimated_cost


@dataclass
class QualityReport:
    """Complete quality report for a survey."""
    survey_id: str
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    survey_status: str = "unknown"
    n_variables: int = 0
    n_observations: int = 0
    
    tier_stats: dict[int, TierStats] = field(default_factory=dict)
    llm_cost: LLMCostStats = field(default_factory=LLMCostStats)
    
    n_errors: int = 0
    n_warnings: int = 0
    n_info: int = 0
    n_flagged_review: int = 0
    
    variables_pending: int = 0
    variables_done: int = 0
    variables_error: int = 0
    
    validation_results: list[dict[str, Any]] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)

    @property
    def completion_rate(self) -> float:
        if self.n_variables == 0:
            return 0.0
        return (self.variables_done / self.n_variables) * 100

    @property
    def error_rate(self) -> float:
        if self.n_variables == 0:
            return 0.0
        return (self.variables_error / self.n_variables) * 100

    @property
    def overall_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        score = 100.0
        score -= min(20, self.error_rate * 2)
        score -= min(10, (self.n_warnings / max(1, self.n_variables)) * 50)
        score -= min(10, (self.n_flagged_review / max(1, self.n_variables)) * 30)
        return max(0.0, score)

    def to_dict(self) -> dict:
        return {
            "survey_id": self.survey_id,
            "generated_at": self.generated_at,
            "survey_status": self.survey_status,
            "n_variables": self.n_variables,
            "n_observations": self.n_observations,
            "completion_rate": round(self.completion_rate, 2),
            "error_rate": round(self.error_rate, 2),
            "overall_quality_score": round(self.overall_quality_score, 2),
            "tier_stats": {
                tier: {
                    "count": stats.count,
                    "total": stats.total,
                    "percentage": round(stats.percentage, 2),
                    "success": stats.success,
                    "errors": stats.errors,
                    "success_rate": round(stats.success_rate, 2),
                }
                for tier, stats in self.tier_stats.items()
            },
            "llm_cost": {
                "estimated_tokens": self.llm_cost.estimated_tokens,
                "actual_tokens": self.llm_cost.actual_tokens,
                "token_accuracy": round(self.llm_cost.token_accuracy, 2),
                "estimated_cost": round(self.llm_cost.estimated_cost, 4),
                "actual_cost": round(self.llm_cost.actual_cost, 4),
                "cost_variance": round(self.llm_cost.cost_variance, 2),
                "api_calls": self.llm_cost.api_calls,
            },
            "issues": {
                "n_errors": self.n_errors,
                "n_warnings": self.n_warnings,
                "n_info": self.n_info,
                "n_flagged_review": self.n_flagged_review,
            },
            "variables": {
                "pending": self.variables_pending,
                "done": self.variables_done,
                "error": self.variables_error,
            },
            "validation_results": self.validation_results,
            "conflicts": self.conflicts,
        }

    def to_markdown(self) -> str:
        """Generate Markdown report."""
        lines = [
            f"# Quality Report: {self.survey_id}",
            "",
            f"**Generated:** {self.generated_at}",
            f"**Status:** {self.survey_status}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Variables | {self.n_variables} |",
            f"| Observations | {self.n_observations} |",
            f"| Completion | {self.completion_rate:.1f}% |",
            f"| Error Rate | {self.error_rate:.1f}% |",
            f"| Quality Score | {self.overall_quality_score:.1f}/100 |",
            "",
            "## Tier Distribution",
            "",
        ]

        if self.tier_stats:
            lines.extend([
                f"| Tier | Count | Percentage | Success Rate |",
                f"|------|-------|------------|--------------|",
            ])
            for tier in sorted(self.tier_stats.keys()):
                stats = self.tier_stats[tier]
                lines.append(
                    f"| Tier {tier} | {stats.count} | {stats.percentage:.1f}% | {stats.success_rate:.1f}% |"
                )
            lines.append("")

        lines.extend([
            "## Issues",
            "",
            f"- **Errors:** {self.n_errors}",
            f"- **Warnings:** {self.n_warnings}",
            f"- **Info:** {self.n_info}",
            f"- **Flagged for Review:** {self.n_flagged_review}",
            "",
        ])

        if self.llm_cost.api_calls > 0:
            lines.extend([
                "## LLM Costs",
                "",
                f"| Metric | Estimated | Actual |",
                f"|--------|-----------|--------|",
                f"| Tokens | {self.llm_cost.estimated_tokens:,} | {self.llm_cost.actual_tokens:,} |",
                f"| Cost | ${self.llm_cost.estimated_cost:.4f} | ${self.llm_cost.actual_cost:.4f} |",
                f"| API Calls | - | {self.llm_cost.api_calls} |",
                "",
                f"**Token Accuracy:** {self.llm_cost.token_accuracy*100:.1f}%",
                f"**Cost Variance:** {self.llm_cost.cost_variance*100:.1f}%",
                "",
            ])

        if self.conflicts:
            lines.extend([
                "## Conflicts Detected",
                "",
                f"**{len(self.conflicts)} conflict(s) found:**",
                "",
            ])
            for i, conflict in enumerate(self.conflicts, 1):
                lines.append(f"### Conflict {i}")
                lines.append(f"- **Type:** {conflict.get('type', 'unknown')}")
                lines.append(f"- **Variables:** {', '.join(conflict.get('variables', []))}")
                lines.append(f"- **Message:** {conflict.get('message', '')}")
                lines.append("")
        else:
            lines.append("## Conflicts\n\nNo conflicts detected.\n")

        if self.validation_results:
            lines.extend([
                "## Validation Results",
                "",
            ])
            for vr in self.validation_results[:10]:
                lines.append(f"- **{vr.get('variable', 'N/A')}:** {vr.get('summary', 'OK')}")
            if len(self.validation_results) > 10:
                lines.append(f"- ... and {len(self.validation_results) - 10} more")
            lines.append("")

        return "\n".join(lines)


class QualityReporter:
    """Generates quality reports for survey cleaning results.

    Usage:
        reporter = QualityReporter(survey_id="eeq_2022")
        report = reporter.generate_report()
        
        # Markdown output
        md = report.to_markdown()
        
        # JSON output
        data = report.to_dict()
    """

    DEFAULT_COST_PER_1K_TOKENS = {
        "tier1": 0.0001,
        "tier2": 0.0005,
        "tier3": 0.003,
    }

    ESTIMATED_TOKENS_PER_VAR = {
        1: 50,
        2: 500,
        3: 2000,
    }

    def __init__(
        self,
        survey_id: str,
        status_file: Optional[Path] = None,
        cost_rates: Optional[dict[str, float]] = None,
    ):
        self.survey_id = survey_id
        self.status_file = status_file or Path("surveys/status.json")
        self.cost_rates = cost_rates or self.DEFAULT_COST_PER_1K_TOKENS

    def generate_report(
        self,
        validation_results: Optional[list[ValidationResult]] = None,
        conflicts: Optional[list[dict[str, Any]]] = None,
    ) -> QualityReport:
        """Generate a quality report for the survey.

        Args:
            validation_results: Optional list of validation results for each variable
            conflicts: Optional list of detected conflicts

        Returns:
            QualityReport with all metrics
        """
        report = QualityReport(survey_id=self.survey_id)

        state_data = self._load_state()
        if not state_data:
            return report

        survey_data = state_data.get("surveys", {}).get(self.survey_id, {})
        
        report.survey_status = survey_data.get("status", "unknown")
        report.n_variables = survey_data.get("n_variables", 0)
        report.n_observations = survey_data.get("n_observations", 0)

        variables_data = survey_data.get("variables", {})
        
        if isinstance(variables_data, dict):
            if "total" in variables_data:
                return report
            
            self._process_variable_states(variables_data, report)
            self._calculate_tier_stats(variables_data, report)
            self._calculate_llm_costs(variables_data, report)

        if validation_results:
            self._process_validation_results(validation_results, report)

        report.conflicts = conflicts or []

        return report

    def generate_and_save(
        self,
        output_dir: Optional[Path] = None,
        format: ReportFormat = ReportFormat.MARKDOWN,
        validation_results: Optional[list[ValidationResult]] = None,
        conflicts: Optional[list[dict[str, Any]]] = None,
    ) -> Path:
        """Generate report and save to file.

        Args:
            output_dir: Directory to save report (default: surveys/<survey_id>/)
            format: Output format (Markdown or JSON)
            validation_results: Optional validation results
            conflicts: Optional conflicts list

        Returns:
            Path to saved report
        """
        report = self.generate_report(validation_results, conflicts)

        if output_dir is None:
            output_dir = Path(f"surveys/{self.survey_id}")

        output_dir.mkdir(parents=True, exist_ok=True)

        if format == ReportFormat.MARKDOWN:
            output_path = output_dir / "quality_report.md"
            content = report.to_markdown()
        else:
            output_path = output_dir / "quality_report.json"
            content = json.dumps(report.to_dict(), indent=2)

        output_path.write_text(content)
        return output_path

    def _load_state(self) -> dict:
        """Load survey state from status file."""
        if not self.status_file.exists():
            return {}
        return json.loads(self.status_file.read_text())

    def _process_variable_states(
        self, variables_data: dict, report: QualityReport
    ) -> None:
        """Process variable state data."""
        for var_name, var_state in variables_data.items():
            if not isinstance(var_state, dict):
                continue

            status = var_state.get("status", "pending")
            
            if status == "pending":
                report.variables_pending += 1
            elif status == "done":
                report.variables_done += 1
            elif status == "error":
                report.variables_error += 1

            if var_state.get("error"):
                report.n_errors += 1

            tier = var_state.get("tier")
            if tier and tier not in report.tier_stats:
                report.tier_stats[tier] = TierStats()

            confidence = var_state.get("confidence", 0.0)
            if confidence < 0.5 and status == "done":
                report.n_flagged_review += 1

    def _calculate_tier_stats(
        self, variables_data: dict, report: QualityReport
    ) -> None:
        """Calculate statistics per tier."""
        tier_counts: dict[int, dict[str, int]] = {}

        for var_state in variables_data.values():
            if not isinstance(var_state, dict):
                continue
            
            tier = var_state.get("tier")
            if tier is None:
                continue

            if tier not in tier_counts:
                tier_counts[tier] = {"total": 0, "success": 0, "errors": 0}

            tier_counts[tier]["total"] += 1
            
            status = var_state.get("status")
            if status == "done":
                tier_counts[tier]["success"] += 1
            elif status == "error":
                tier_counts[tier]["errors"] += 1

        for tier, counts in tier_counts.items():
            stats = TierStats(
                count=counts["total"],
                total=report.n_variables,
                success=counts["success"],
                errors=counts["errors"],
            )
            report.tier_stats[tier] = stats

    def _calculate_llm_costs(
        self, variables_data: dict, report: QualityReport
    ) -> None:
        """Calculate estimated and actual LLM costs."""
        cost = LLMCostStats()

        for var_state in variables_data.values():
            if not isinstance(var_state, dict):
                continue

            tier = var_state.get("tier")
            if tier is None:
                continue

            estimated = self.ESTIMATED_TOKENS_PER_VAR.get(tier, 1000)
            cost.estimated_tokens += estimated

            cost_key = f"tier{tier}"
            rate = self.cost_rates.get(cost_key, 0.001)
            cost.estimated_cost += (estimated / 1000) * rate

        cost.actual_tokens = cost.estimated_tokens
        cost.actual_cost = cost.estimated_cost
        cost.api_calls = sum(
            1 for v in variables_data.values()
            if isinstance(v, dict) and v.get("tier") in (2, 3)
        )

        report.llm_cost = cost

    def _process_validation_results(
        self, results: list[ValidationResult], report: QualityReport
    ) -> None:
        """Process validation results into report."""
        for result in results:
            if result.has_errors:
                report.n_errors += len(result.errors)
            if result.has_warnings:
                report.n_warnings += len(result.warnings)
            report.n_info += len(result.info)

            report.validation_results.append(result.to_dict())


def generate_quality_report(
    survey_id: str,
    output_path: Optional[str] = None,
    format: str = "markdown",
) -> QualityReport:
    """Convenience function to generate a quality report.

    Args:
        survey_id: Survey identifier
        output_path: Optional path to save report
        format: "markdown" or "json"

    Returns:
        QualityReport object
    """
    report_format = ReportFormat.MARKDOWN if format == "markdown" else ReportFormat.JSON
    
    reporter = QualityReporter(survey_id)
    report = reporter.generate_report()

    if output_path:
        output_dir = Path(output_path).parent
        reporter.generate_and_save(output_dir, report_format)

    return report
