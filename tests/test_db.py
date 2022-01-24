from pathlib import Path

import pytest

from kfs import db


@pytest.fixture()
def base_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def sqlite_filename() -> str:
    return "kfs.db"


@pytest.fixture()
def sqlite_url(base_dir: Path, sqlite_filename: str) -> str:
    return f"sqlite:///{base_dir / sqlite_filename}"


def test_init(base_dir: Path, sqlite_filename: str, sqlite_url: str) -> None:
    """After init, the database has been created and the file exists"""
    db.init(sqlite_url)
    assert (base_dir / sqlite_filename).exists()
