from pathlib import Path
from typing import Callable
from typing import Optional

import pytest
from _pytest.monkeypatch import MonkeyPatch
from mypy_extensions import VarArg
from typer.testing import CliRunner
from typer.testing import Result

from kfs import __version__
from kfs.cli import app

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


@pytest.fixture()
def base_dir(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.mark.parametrize("path_arg", [None, "db/db.sqlite3"])
def test_db_init(call_cli: CLICaller, base_dir: Path, path_arg: Optional[str]) -> None:
    """The CLI initializes the database, which creates a file at the specified path."""
    if path_arg is None:
        result = call_cli("db", "init")
        db_path = base_dir / "kfs.sqlite3"
    else:
        result = call_cli("db", "init", path_arg)
        db_path = base_dir / path_arg

    assert result.exit_code == 0
    assert db_path.exists()
