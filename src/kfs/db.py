import uuid
from pathlib import Path
from typing import List
from typing import Optional

from sqlalchemy.engine import Engine
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine

from kfs import console

DB_FILENAME = "kfs.sqlite3"


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


class Tag(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    category: Optional[str]
    value: str

    files: List[File] = Relationship(
        back_populates="tags", link_model=FileTagAssociation
    )


def db_path() -> Path:
    """The path to the database file."""
    return Path.cwd() / DB_FILENAME


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


def init() -> None:
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
