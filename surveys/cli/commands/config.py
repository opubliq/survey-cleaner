"""Config command - manage user configuration."""

import json
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.table import Table

from surveys.config.config_schema import SurveyCleanerConfig, load_config, save_config

app = typer.Typer(help="Edit or display user configuration")
console = Console()


@app.command()
def show():
    """Show current configuration."""
    config = load_config()
    _print_config(config)


@app.command()
def set(
    key: str = typer.Argument(..., help="Config key (e.g., 'tier1_model', 'data_dir')"),
    value: str = typer.Argument(..., help="Config value"),
):
    """Set a configuration value."""
    config = load_config()

    if "." in key:
        parts = key.split(".")
        obj = config
        for p in parts[:-1]:
            if not hasattr(obj, p):
                typer.echo(f"Error: Unknown config path: {key}", err=True)
                raise typer.Exit(1)
            obj = getattr(obj, p)
        final_key = parts[-1]
    else:
        final_key = key
        obj = config

    if not hasattr(obj, final_key):
        typer.echo(f"Error: Unknown config key: {key}", err=True)
        raise typer.Exit(1)

    current = getattr(obj, final_key)
    if isinstance(current, bool):
        value = value.lower() in ("true", "1", "yes")
    elif isinstance(current, int):
        value = int(value)
    elif isinstance(current, float):
        value = float(value)

    setattr(obj, final_key, value)
    save_config(config)
    typer.echo(f"Updated {key} = {value}")


@app.command()
def init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing config"),
):
    """Initialize default configuration."""
    config_path = Path.home() / ".survey-cleaner" / "config.json"
    if config_path.exists() and not force:
        typer.echo(f"Config already exists at {config_path}. Use --force to overwrite.")
        raise typer.Exit(1)

    config = SurveyCleanerConfig()
    save_config(config)
    typer.echo(f"Created default config at {config_path}")


def _print_config(config: SurveyCleanerConfig):
    table = Table(title="Survey Cleaner Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Default Model", config.default_model or "Not set")
    table.add_row("Tier 1 Model", config.tier1_model or "default")
    table.add_row("Tier 2 Model", config.tier2_model or "default")
    table.add_row("Tier 3 Model", config.tier3_model or "default")
    table.add_row("Data Directory", str(config.data_dir) if config.data_dir else "default")
    table.add_row("Output Directory", str(config.output_dir) if config.output_dir else "default")
    table.add_row("Tier 1 Min Confidence", str(config.tier1_min_confidence))
    table.add_row("Tier 1 Max Unique", str(config.tier1_max_n_unique))
    table.add_row("Tier 2 Batch Size", str(config.tier2_max_batch_size))

    console.print(table)


if __name__ == "__main__":
    app()
