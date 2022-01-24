import uuid
from typing import List
from typing import Optional

from sqlalchemy.engine import Engine
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine

engine: Optional[Engine] = None


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


def init(url: str) -> None:
    global engine
    engine = create_engine(url)

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Create a new database session to use as a context manager."""
    return Session(engine)
