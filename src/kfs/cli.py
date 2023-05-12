from pathlib import Path

import typer

from . import __version__
from . import console
from . import db

DB_FILENAME = "kfs.sqlite3"

app = typer.Typer()
db_app = typer.Typer()
app.add_typer(db_app, name="db")


@app.command()
def version() -> None:
    """Show project version."""
    console.print(f"kfs version: {__version__}", style="bold green")


@db_app.command()
def init(
    path: Path = typer.Argument(lambda: Path.cwd() / DB_FILENAME),
) -> None:
    """Initialize a new database."""
    try:
        db.create(filename=str(path))
    except FileExistsError:
        raise typer.Abort()
