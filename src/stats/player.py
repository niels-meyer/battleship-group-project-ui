from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel, select
from database.db import get_session

if TYPE_CHECKING:
    from .match import Match

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    match_history: List["Match"] = Relationship(back_populates="player")

def create_player(name: str) -> Player:
    with next(get_session()) as session:
        player = Player(name=name)
        session.add(player)
        session.commit()
        session.refresh(player)
        return player

def get_all_players() -> List[Player]:
    with next(get_session()) as session:
        players = session.exec(select(Player)).all()
        return players
    
def get_player_by_name(name: str) -> Optional[Player]:
    with next(get_session()) as session:
        statement = select(Player).where(Player.name == name)
        player = session.exec(statement).first()
        return player

from src.stats.match import Match
