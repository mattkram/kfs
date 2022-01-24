from pathlib import Path

import typer
from rich.console import Console

from . import __version__
from . import db

console = Console()
app = typer.Typer()
db_app = typer.Typer()
app.add_typer(db_app, name="db")


@app.command()
def version() -> None:
    """Show project version."""
    console.print(f"kfs version: {__version__}", style="bold green")


@db_app.command()
def init(
    path: Path = typer.Argument(lambda: Path.cwd() / "kfs.sqlite3"),
) -> None:
    """Initialize a new database."""
    path = path.resolve()
    path.parent.mkdir(exist_ok=True, parents=True)

    console.print(f"Initializing the database at {path}")
    db.init(url=f"sqlite:///{path}")
