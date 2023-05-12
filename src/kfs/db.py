import uuid
from pathlib import Path
from typing import Iterator
from typing import List
from typing import Optional

from rich.progress import track
from sqlalchemy import Index
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine

from kfs import console

DB_FILENAME = "kfs.db"


class FileTagAssociation(SQLModel, table=True):
    file_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="file.id", primary_key=True
    )
    tag_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class File(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    path: str

    tags: List["Tag"] = Relationship(
        back_populates="files", link_model=FileTagAssociation
    )

    __table_args__ = (Index("name_path_unique", "name", "path", unique=True),)


class Tag(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    category: Optional[str]
    value: str

    files: List[File] = Relationship(
        back_populates="tags", link_model=FileTagAssociation
    )


def base_dir() -> Path:
    """The base directory, from which all tracked files are referenced."""
    return db_path().parent


def db_path() -> Path:
    """The path to the database file.

    Recursively searches parents until found. If not found, return path in current working directory.

    """
    cwd = Path.cwd().resolve()

    def _dirs() -> Iterator[Path]:
        yield cwd
        yield from cwd.parents

    for _dir in _dirs():
        if (p := _dir / DB_FILENAME).exists():
            return p
    return cwd / DB_FILENAME


def db_url() -> str:
    """The database connection string."""
    return f"sqlite:///{db_path()}"


def create() -> None:
    """Create the database file if it doesn't exist."""
    path = db_path()

    if path.exists():
        console.print(f"Database already exists at {path}")
        raise FileExistsError

    console.print(f"Creating the database at {path}")
    path.parent.mkdir(exist_ok=True, parents=True)
    init()


_engine: Optional[Engine] = None


def init(raise_if_missing: bool = False) -> None:
    if raise_if_missing and not db_path().exists():
        raise FileNotFoundError("Database file does not exist")

    global _engine
    _engine = create_engine(db_url())

    SQLModel.metadata.create_all(_engine)


def get_engine() -> Engine:
    """Get the global database engine."""
    if _engine is None:  # pragma: no cover
        raise ValueError("Engine must be initialized with `db.init()`")
    return _engine


def get_session() -> Session:
    """Create a new database session to use as a context manager."""
    return Session(get_engine())


def create_index() -> None:
    """Create the file index by writing File records to the database."""
    file_paths = [
        path for path in base_dir().glob("**/*") if path.is_file() and path != db_path()
    ]
    num_new = 0
    num_existing = 0
    for path in track(file_paths, description="Indexing ..."):
        relative_path = path.relative_to(base_dir())
        with get_session() as session:
            session.add(File(name=path.name, path=str(relative_path.parent)))
            try:
                session.commit()
            except IntegrityError:
                # We can't have duplicate rows
                num_existing += 1
            else:
                num_new += 1
    console.print(f"Added {num_new} new files, found {num_existing} existing files.")
