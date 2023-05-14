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
    filenames = [
        "first_file_at_root.csv",
        "single_nesting/test_file.dat",
        "some/directory/test_file.dat",
    ]

    file_paths = [base_dir / filename for filename in filenames]

    for file_path in file_paths:
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with file_path.open("w") as fp:
            fp.write("Hello")

    return file_paths


@pytest.mark.parametrize("index_times", [1, 2])
def test_create_index(base_dir: Path, file_paths: list[Path], index_times: int) -> None:
    # Indexing should be idempotent
    for _ in range(index_times):
        db.create_index()

    with db.get_session() as session:
        files = session.exec(select(db.File)).all()

    assert len(files) == len(file_paths)

    for path in file_paths:
        # Check that the file exists by name
        file = db.get_file_by_path(path)
        assert file is not None

        # Check that the directory is correct
        rel_directory = path.relative_to(base_dir).parent
        assert Path(file.path) == rel_directory


@pytest.fixture()
def tag_index_map(file_paths: list[Path]) -> dict[str, list[int]]:
    db.create_index()
    tag_index_map: dict[str, list[int]] = {
        "bank:chase": [0],
        "bank:citi": [0, 1],
        "no-category": [2],
        "non-existent": [],
    }
    for tag, indices in tag_index_map.items():
        for index in indices:
            db.add_tag_to_file(file_paths[index], tag)
    return tag_index_map


def test_add_tag_to_file(tag_index_map: dict[str, list[int]]) -> None:
    for tag, indices in tag_index_map.items():
        files = db.get_files_with_tag(tag)
        assert len(files) == len(indices)
        assert all(isinstance(f, db.File) for f in files)


def test_add_tag_to_file_idempotent(file_paths: list[Path]) -> None:
    db.create_index()
    tag = "bank:chase"
    for _ in range(2):
        db.add_tag_to_file(file_paths[0], tag)

    files = db.get_files_with_tag(tag)
    assert len(files) == 1
