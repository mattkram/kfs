import typer

from . import __version__
from . import console
from . import db

app = typer.Typer()
db_app = typer.Typer()
app.add_typer(db_app, name="db")


@app.command()
def version() -> None:
    """Show project version."""
    console.print(f"kfs version: {__version__}", style="bold green")


@db_app.command()
def init() -> None:
    """Initialize a new database."""
    try:
        db.create()
    except FileExistsError:
        raise typer.Abort()
