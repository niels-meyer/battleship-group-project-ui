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
TCoord = Tuple[str, str] # ("row", "column") e.g. ("a", "1"), ("b", "10")
TCoordIndex = Tuple[int, int] # (row_index, column_index) e.g. (0, 0), (1, 9)

# --- Ships ---
TShipCoords = List[TCoord]
TShips = Dict[str, TShipCoords] # e.g. { "Carrier": ["a 1", "a 2", "a 3", "a 4", "a 5"] }

# --- Board ---
TBoardShip = str | None
TBoardCell = TypedDict("TBoardCell", { "is_shot": bool, "ship": TBoardShip })
TBoard = Sequence[Sequence[TBoardCell]]

# --- PlayerAI ---
TRemainingCells = Dict[str, List[str]]

class EAIDifficulty(Enum):
    BABY = "baby"
    EASY = "easy"
    NORMAL = "normal" 
    HARD = "hard"
    IMPOSSIBLE = "impossible"