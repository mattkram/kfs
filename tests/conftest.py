from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(autouse=True)
def base_dir(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    """A temporary base directory, in which to run CLI commands."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
