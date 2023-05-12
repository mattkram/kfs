from pathlib import Path
from typing import Callable
from typing import Optional

import pytest
from mypy_extensions import VarArg
from typer.testing import CliRunner
from typer.testing import Result

from kfs import __version__
from kfs.cli import app
from kfs.db import DB_FILENAME

CLICaller = Callable[[VarArg(str)], Result]


@pytest.fixture()
def call_cli() -> CLICaller:
    """Returns a function, which can be used to call the CLI."""
    runner = CliRunner()

    def f(*args: str) -> Result:
        return runner.invoke(app, args)

    return f


def test_version(call_cli: CLICaller) -> None:
    result = call_cli("version")
    assert result.exit_code == 0
    assert f"kfs version: {__version__}" in result.stdout


@pytest.mark.parametrize("path_arg", [None, "db/db.sqlite3"])
def test_db_init(call_cli: CLICaller, base_dir: Path, path_arg: Optional[str]) -> None:
    """The CLI initializes the database, which creates a file at the specified path."""
    result = call_cli("init")

    assert result.exit_code == 0
    assert (base_dir / DB_FILENAME).exists()


def test_db_init_raises_if_file_exists(call_cli: CLICaller) -> None:
    """If we try to initialize the database after it exists, an error is raised."""
    # Call once to create the database
    call_cli("init")
    assert Path("kfs.sqlite3").exists()

    result = call_cli("init")
    assert result.exit_code == 1
