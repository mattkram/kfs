from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest
from mypy_extensions import VarArg
from typer.testing import CliRunner
from typer.testing import Result

from kfs import __version__
from kfs.cli import app
from kfs.db import db_path

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


def test_db_init(call_cli: CLICaller, base_dir: Path) -> None:
    """The CLI initializes the database, which creates a file at the specified path."""
    result = call_cli("init")

    assert result.exit_code == 0
    assert db_path().exists()


@pytest.mark.parametrize("from_subdir", [".", "directory", "directory/subdirectory"])
def test_db_init_raises_if_file_exists(
    call_cli: CLICaller, base_dir: Path, from_subdir: str
) -> None:
    """If we try to initialize the database after it exists, an error is raised."""
    # Call once to create the database
    call_cli("init")
    assert db_path().exists()

    # Change to a subdirectory
    subdir = base_dir / from_subdir
    subdir.mkdir(parents=True, exist_ok=True)

    # We still see an error, even from subdirectories
    result = call_cli("init")
    assert result.exit_code == 1


def test_index_files_requires_database(call_cli: CLICaller) -> None:
    """`kfs index` calls the db.create_index() function."""
    result = call_cli("index")
    assert result.exit_code == 1
    call_cli("init")


def test_index_files(call_cli: CLICaller) -> None:
    """`kfs index` calls the db.create_index() function."""
    call_cli("init")

    with patch("kfs.db.create_index") as mock:
        result = call_cli("index")
    assert result.exit_code == 0
    mock.assert_called_once()


def test_add_tag_to_file(call_cli: CLICaller, base_dir: Path) -> None:
    call_cli("init")
    filenames = ["file_1.txt", "file_2.txt"]
    for f in filenames:
        with (base_dir / f).open("w") as fp:
            fp.write("Hi")

    with patch("kfs.db.add_tag_to_file") as mock:
        result = call_cli("tag", "--add", "bank:chase", *filenames)

    assert result.exit_code == 0

    assert mock.call_count == len(filenames)
    mock.assert_has_calls(
        [
            ((base_dir / "file_1.txt", "bank:chase"),),  # type: ignore
            ((base_dir / "file_2.txt", "bank:chase"),),  # type: ignore
        ]
    )
