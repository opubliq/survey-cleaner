import typer
from typing import Optional

from surveys.cli.commands import clean, watch, config, pattern

app = typer.Typer(
    name="survey-cleaner",
    help="Survey Cleaning CLI - Orchestrates tier-based survey data cleaning",
    add_completion=False,
)

app.add_typer(config.app, name="config")
app.add_typer(pattern.app, name="pattern")

app.command(name="clean")(clean.clean)
app.command(name="watch")(watch.watch)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Survey Cleaner CLI - Hybrid tier-based cleaning orchestration.
    
    Run 'survey-cleaner --help' for usage information.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
