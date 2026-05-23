from typing import Dict, List, Sequence, Tuple, TypedDict
from enum import Enum

# --- Coord ---
TCoord = Tuple[str, str]
TCoordIndex = Tuple[int, int]

# --- Ships ---
TShipCoords = List[TCoord]
TShips = Dict[str, TShipCoords]

# --- Board ---
TBoardShip = str | None
TBoardCell = TypedDict("TBoardCell", {"is_shot": bool, "ship": TBoardShip})
TBoard = Sequence[Sequence[TBoardCell]]

# --- PlayerAI ---
TRemainingCells = Dict[str, List[str]]

class EAIDifficulty(Enum):
    BABY = "baby"
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    IMPOSSIBLE = "impossible"


class TCurrentPlayer(TypedDict):
    id: int
    name: str
    ai_difficulty: str
