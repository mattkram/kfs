from typing import Optional

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel
from sqlmodel import create_engine

engine: Optional[Engine] = None


def init(url: str) -> None:
    global engine
    engine = create_engine(url, echo=True)

    SQLModel.metadata.create_all(engine)
