"""Clean command - runs survey cleaning pipeline."""

import sys
from typing import Optional

import typer

from surveys.cli.output.formatters import (
    print_clean_summary,
    print_progress_bar,
    print_survey_status,
)
from surveys.orchestrator import OrchestratorV2

app = typer.Typer(help="Run cleaning on a survey")


@app.command()
def clean(
    survey_id: str = typer.Argument(..., help="Survey ID to clean"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Classify only, don't generate code"),
    tier_max: int = typer.Option(3, "--tier-max", help="Maximum tier to process (1, 2, or 3)"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Limit number of variables to process"),
    only_var: Optional[str] = typer.Option(None, "--only-var", help="Process only this variable"),
    model: Optional[str] = typer.Option(None, "--model", help="LLM model for Tier 2/3"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", help="Verbose output"),
):
    """Clean a survey using the tier-based pipeline."""
    if tier_max not in [1, 2, 3]:
        typer.echo("Error: --tier-max must be 1, 2, or 3", err=True)
        raise typer.Exit(1)

    typer.echo(f"\n{'='*60}")
    typer.echo(f"Survey Cleaner - {survey_id}")
    typer.echo(f"Max tier: {tier_max}, Dry run: {dry_run}")
    typer.echo(f"{'='*60}\n")

    try:
        orchestrator = OrchestratorV2(
            survey_id=survey_id,
            limit=limit,
            only_var=only_var,
            model=model,
            dry_run=dry_run,
            verbose=verbose,
        )
        orchestrator.run()

        survey_state = orchestrator._get_survey_state()
        print_survey_status(survey_state)

        if not dry_run:
            done_count = sum(1 for v in survey_state.variables.values() if v.status == "done")
            total_count = len(survey_state.variables)
            print_clean_summary(done_count, total_count)

    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error during cleaning: {e}", err=True)
        if verbose:
            raise
        raise typer.Exit(1)
