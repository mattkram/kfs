from pathlib import Path

from rich.table import Table

from kfs import console
from kfs import db


def print_files_table(files: list[db.File], title: str) -> None:
    """Print a table of files to the console."""
    table = Table(title=title)
    table.add_column("Path", justify="left")

    for file in files:
        path = (Path(file.path) / file.name).resolve().relative_to(db.base_dir())
        table.add_row(path.as_posix())
    console.print(table)
