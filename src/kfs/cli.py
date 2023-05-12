import typer

from . import __version__
from . import console
from . import db

app = typer.Typer()


@app.command()
def version() -> None:
    """Show project version."""
    console.print(f"kfs version: {__version__}", style="bold green")


@app.command()
def init() -> None:
    """Initialize a new database."""
    try:
        db.create()
    except FileExistsError:
        raise typer.Abort()


@app.command()
def index() -> None:
    """Index the files in the filesystem."""
    db.init()
    db.create_index()
