from pathlib import Path

import pytest
from sqlmodel import select

from kfs import db
from kfs.db import db_path


@pytest.fixture(autouse=True)
def database() -> None:
    db.init()


def test_init() -> None:
    """After init, the database has been created and the file exists"""
    assert db_path().exists()


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


@pytest.fixture()
def file_paths(base_dir: Path) -> list[Path]:
    """Write a number of files and return the paths to those files."""
    file_path = base_dir / "files"
    file_path.mkdir()

    filenames = ["some_file.txt"]

    for path in filenames:
        with (file_path / path).open("w") as fp:
            fp.write("Hello")

    return list(file_path.glob("**/*"))


def test_create_index(file_paths: list[Path]) -> None:
    db.create_index()
    with db.get_session() as session:
        # Retrieve the file from database
        files = session.exec(select(db.File)).all()

    assert len(files) == len(file_paths)
