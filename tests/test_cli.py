from typing import Callable

import pytest
from click.testing import Result
from mypy_extensions import VarArg
from typer.testing import CliRunner

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
