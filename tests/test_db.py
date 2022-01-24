from pathlib import Path

import pytest
from sqlmodel import select

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


@pytest.fixture(autouse=True)
def database(sqlite_url: str) -> None:
    db.init(sqlite_url)


def test_init(base_dir: Path, sqlite_filename: str, sqlite_url: str) -> None:
    """After init, the database has been created and the file exists"""
    assert (base_dir / sqlite_filename).exists()


def test_database() -> None:
    with db.get_session() as session:
        # Create a new file with a tag
        tag = db.Tag(category="vendor", value="chevron")
        file = db.File(name="test_file.csv", path="/some/directory", tags=[tag])
        session.add(file)
        session.commit()

    with db.get_session() as session:
        # Retrieve the file from database
        read_file = session.exec(select(db.File)).one()

        assert file is not read_file
        assert read_file.name == "test_file.csv"
        assert read_file.path == "/some/directory"
        assert len(read_file.tags) == 1

        read_tag = read_file.tags[0]
        assert read_tag.category == "vendor"
        assert read_tag.value == "chevron"
        assert len(read_tag.files) == 1
