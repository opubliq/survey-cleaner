"""Watch command - monitors a folder for new surveys and triggers cleaning."""

import time
from pathlib import Path
from typing import Optional

import typer
from tqdm import tqdm

from surveys.cli.output.formatters import print_watch_status
from surveys.orchestrator import OrchestratorV2

app = typer.Typer(help="Watch folder mode - poll and trigger clean automatically")


@app.command()
def watch(
    dir: Optional[Path] = typer.Option(None, "--dir", help="Directory to watch"),
    interval: int = typer.Option(5, "--interval", help="Poll interval in minutes (default: 5)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Classify only, don't generate code"),
    tier_max: int = typer.Option(3, "--tier-max", help="Maximum tier to process"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", help="Verbose output"),
):
    """Watch a folder for new surveys and automatically clean them."""
    if dir is None:
        base_path = Path(__file__).parent.parent.parent
        dir = base_path / "_SharedFolder_data_produit"

    if not dir.exists():
        typer.echo(f"Error: Directory does not exist: {dir}", err=True)
        raise typer.Exit(1)

    typer.echo(f"\n{'='*60}")
    typer.echo(f"Watch Mode - Monitoring: {dir}")
    typer.echo(f"Poll interval: {interval} minutes")
    typer.echo(f"{'='*60}\n")

    processed_surveys = set()
    interval_seconds = interval * 60

    try:
        with tqdm(desc="Watching for surveys", unit="check") as pbar:
            while True:
                surveys = [d for d in dir.iterdir() if d.is_dir()]

                for survey_dir in surveys:
                    survey_id = survey_dir.name
                    if survey_id in processed_surveys:
                        continue

                    data_files = list(survey_dir.glob("*.csv")) + list(survey_dir.glob("*.xlsx"))
                    if not data_files:
                        continue

                    typer.echo(f"\n[NEW] Found survey: {survey_id}")
                    processed_surveys.add(survey_id)

                    try:
                        orchestrator = OrchestratorV2(
                            survey_id=survey_id,
                            dry_run=dry_run,
                            verbose=verbose,
                        )
                        orchestrator.run()
                        typer.echo(f"[DONE] Cleaned: {survey_id}")
                    except Exception as e:
                        typer.echo(f"[ERROR] {survey_id}: {e}", err=True)

                pbar.update(1)
                time.sleep(interval_seconds)

    except KeyboardInterrupt:
        typer.echo("\n\nStopped watching.")
        print_watch_status(processed_surveys)
