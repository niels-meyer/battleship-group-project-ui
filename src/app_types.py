from typing import Dict, List, Sequence, Tuple, TypedDict
from enum import Enum

# --- Config ---
TConfigShips = Dict[str, TypedDict("TConfigShip", {
    "length": int,
})]
TConfigRows = List[str]
TConfigColumns = List[str]
TConfig = TypedDict("TConfig", {
    "ships": TConfigShips,
    "rows": TConfigRows,
    "columns": TConfigColumns
})
TConfigCellSymbols = TypedDict("TConfigCellSymbols", {
    "empty": str,
    "ship": str,
    "hit": str,
    "miss": str
})

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
