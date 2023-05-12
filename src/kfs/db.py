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

_engine: Optional[Engine] = None


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


def create(filename: str) -> None:
    """Create the database file if it doesn't exist."""
    path = Path.cwd() / filename

    if path.exists():
        console.print(f"Database already exists at {path}")
        raise FileExistsError

    console.print(f"Initializing the database at {path}")
    path.parent.mkdir(exist_ok=True, parents=True)
    init(url=f"sqlite:///{path}")


def init(url: str) -> None:
    global _engine
    _engine = create_engine(url)

    SQLModel.metadata.create_all(_engine)


def get_engine() -> Engine:
    """Get the global database engine."""
    if _engine is None:  # pragma: no cover
        raise ValueError("Engine must be initialized with `db.init()`")
    return _engine


def get_session() -> Session:
    """Create a new database session to use as a context manager."""
    return Session(get_engine())
