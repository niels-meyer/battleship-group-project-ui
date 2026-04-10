from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

sqlite_file_path = "database/battleship.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    from src.stats.player import Player
    from src.stats.match import Match
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
