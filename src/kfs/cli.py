from pathlib import Path

import typer

from . import __version__
from . import console
from . import db
from .table import print_files_table

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


def _ensure_db() -> None:
    try:
        db.init(raise_if_missing=True)
    except FileNotFoundError:
        console.print("Must initialize the database first with `kfs init`")
        raise typer.Abort()


@app.command()
def index() -> None:
    """Index the files in the filesystem."""
    _ensure_db()
    db.create_index()


@app.command()
def tag(
    add: list[str] = typer.Option(None), paths: list[Path] = typer.Argument(...)
) -> None:
    """Add one or more tags to one or more files."""
    _ensure_db()
    paths = [Path.cwd() / p for p in paths if p.is_file()]
    for tag in add:
        for path in paths:
            db.add_tag_to_file(path, tag)


@app.command("list")
def list_files(tag: str = typer.Option(...)) -> None:
    """Print a table of files that are tagged with a specific tag."""
    _ensure_db()
    files = db.get_files_with_tag(tag)
    print_files_table(files, f"Files with tag {tag}")
