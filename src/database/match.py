from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel, select
from src.database.db import get_session

if TYPE_CHECKING:
    from src.database.player import Player

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")
    player: Optional["Player"] = Relationship(back_populates="match_history")
    number_of_rounds: int
    has_player_won: bool
    ai_difficulty: str = Field(default="baby")

def create_match(player_id: int, number_of_rounds: int, has_player_won: bool, ai_difficulty: str) -> Match:
    with next(get_session()) as session:
        match = Match(
            player_id=player_id,
            number_of_rounds=number_of_rounds,
            has_player_won=has_player_won,
            ai_difficulty=ai_difficulty,
        )
        session.add(match)
        session.commit()
        session.refresh(match)
        return match

def get_all_matches() -> List[Match]:
    with next(get_session()) as session:
        return list(session.exec(select(Match)).all())

def get_matches_by_player_id(player_id: int) -> List[Match]:
    with next(get_session()) as session:
        return list(session.exec(select(Match).where(Match.player_id == player_id)).all())
