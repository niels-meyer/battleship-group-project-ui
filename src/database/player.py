from typing import TYPE_CHECKING, List, Optional, Tuple
from sqlmodel import Field, Relationship, SQLModel, select
from src.database.db import get_session

if TYPE_CHECKING:
    from src.database.match import Match

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
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
        return list(session.exec(select(Player).order_by(Player.name)).all())

def get_player_by_name(name: str) -> Optional[Player]:
    with next(get_session()) as session:
        return session.exec(select(Player).where(Player.name == name)).first()

def register_player(name: str) -> Tuple[bool, Optional[Player], str]:
    name = name.strip()

    if not name:
        return False, None, "Name is required."
    if get_player_by_name(name) is not None:
        return False, None, "Name already taken. Please choose a different name."
    try:
        player = create_player(name)
        return True, player, f"Player \"{name}\" registered successfully."
    except Exception as e:
        return False, None, f"Registration failed: {str(e)}"

