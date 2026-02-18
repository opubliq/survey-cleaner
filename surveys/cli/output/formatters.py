"""Output formatters for CLI - progress bars and summary tables."""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from tqdm import tqdm

from surveys.orchestrator import SurveyState

console = Console()


def print_progress_bar(current: int, total: int, desc: str = "") -> None:
    """Print a tqdm progress bar."""
    with tqdm(total=total, desc=desc, unit="var") as pbar:
        pbar.update(current)


def print_survey_status(survey_state: SurveyState) -> None:
    """Print survey status table using rich."""
    table = Table(title=f"Survey Status: {survey_state.survey_id}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Status", survey_state.status)
    table.add_row("Observations", str(survey_state.n_observations or "N/A"))
    table.add_row("Variables", str(survey_state.n_variables or "N/A"))

    done_count = sum(1 for v in survey_state.variables.values() if v.status == "done")
    error_count = sum(1 for v in survey_state.variables.values() if v.status == "error")
    pending_count = sum(1 for v in survey_state.variables.values() if v.status == "pending")

    table.add_row("Done", str(done_count))
    table.add_row("Error", str(error_count))
    table.add_row("Pending", str(pending_count))

    console.print(table)


def print_clean_summary(done_count: int, total_count: int) -> None:
    """Print cleaning summary."""
    percentage = (done_count / total_count * 100) if total_count > 0 else 0

    table = Table(title="Cleaning Summary", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Variables Done", f"{done_count}/{total_count}")
    table.add_row("Progress", f"{percentage:.1f}%")

    console.print(table)


def print_watch_status(processed_surveys: set) -> None:
    """Print watch mode summary."""
    console.print(f"\n[bold]Processed Surveys:[/bold] {len(processed_surveys)}")
    for survey_id in sorted(processed_surveys):
        console.print(f"  - {survey_id}")


def create_progress() -> Progress:
    """Create a rich progress bar for CLI."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )
