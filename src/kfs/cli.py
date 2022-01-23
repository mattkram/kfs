import typer
from rich.console import Console

from . import __version__

console = Console()
app = typer.Typer()


@app.command()
def version() -> None:
    """Show project version."""
    console.print(f"kfs version: {__version__}", style="bold green")


@app.command()
def dummy() -> None:
    """Temporarily here to make version a sub-command."""
