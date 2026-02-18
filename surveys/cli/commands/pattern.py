"""Pattern command - manage pattern library."""

import typer
from rich.console import Console
from rich.table import Table

from surveys.pattern_engine import get_all_patterns

app = typer.Typer(help="Pattern library management")
console = Console()


@app.command("list")
def list_patterns():
    """List all available patterns."""
    patterns = get_all_patterns()

    table = Table(title=f"Available Patterns ({len(patterns)})")
    table.add_column("Pattern ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Name", style="green")

    for p in patterns:
        table.add_row(p.pattern_id, p.pattern_type, p.pattern_name or "")

    console.print(table)


@app.command("show")
def show_pattern(pattern_id: str = typer.Argument(..., help="Pattern ID to display")):
    """Show details of a specific pattern."""
    patterns = get_all_patterns()
    pattern = next((p for p in patterns if p.pattern_id == pattern_id), None)

    if not pattern:
        typer.echo(f"Pattern not found: {pattern_id}", err=True)
        raise typer.Exit(1)

    console.print(f"\n[bold cyan]Pattern ID:[/bold cyan] {pattern.pattern_id}")
    console.print(f"[bold]Name:[/bold] {pattern.pattern_name or 'N/A'}")
    console.print(f"[bold]Type:[/bold] {pattern.pattern_type}")

    if hasattr(pattern, "generate_code"):
        console.print("\n[bold]Generate Code Method:[/bold]")
        console.print("  Available")


@app.command("validate")
def validate_patterns():
    """Validate all patterns in the library."""
    patterns = get_all_patterns()

    valid = 0
    errors = []

    for p in patterns:
        try:
            if hasattr(p, "generate_code"):
                valid += 1
            else:
                errors.append(f"{p.pattern_id}: missing generate_code method")
        except Exception as e:
            errors.append(f"{p.pattern_id}: {e}")

    console.print(f"\n[bold]Validation Results:[/bold]")
    console.print(f"Valid patterns: {valid}/{len(patterns)}")

    if errors:
        console.print("\n[bold red]Errors:[/bold red]")
        for err in errors:
            console.print(f"  - {err}")
    else:
        console.print("[green]All patterns are valid![/green]")


@app.command("add")
def add_pattern(
    pattern_id: str = typer.Argument(..., help="New pattern ID"),
    pattern_type: str = typer.Argument(..., help="Pattern type (likert, binary, demographic, etc.)"),
):
    """Add a new pattern to the library (placeholder)."""
    typer.echo(f"Adding pattern: {pattern_id} ({pattern_type})")
    typer.echo("Note: Manual pattern creation requires implementing BasePattern subclass.")


if __name__ == "__main__":
    app()
