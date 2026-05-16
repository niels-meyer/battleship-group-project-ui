from typing import Generator
from sqlalchemy import inspect, text
from sqlmodel import SQLModel, Session, create_engine

sqlite_file_path = "battleship.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables() -> None:
    from src.database.player import Player
    from src.database.match import Match

    SQLModel.metadata.create_all(engine)
    _ensure_match_ai_difficulty_column()


def _ensure_match_ai_difficulty_column() -> None:
    inspector = inspect(engine)
    match_columns = {column["name"] for column in inspector.get_columns("match")}

    if "ai_difficulty" in match_columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE \"match\" ADD COLUMN ai_difficulty VARCHAR NOT NULL DEFAULT 'baby'")
        )

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
