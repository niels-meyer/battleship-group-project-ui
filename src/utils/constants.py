ROWS: list[str] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
COLUMNS: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
SHIPS: dict[str, dict[str, int]] = {
    "Carrier": {"length": 5},
    "Battleship": {"length": 4},
    "Cruiser": {"length": 3},
    "Submarine": {"length": 3},
    "Destroyer": {"length": 2},
}
CELL_SYMBOLS: dict[str, str] = {
    "ship": "■",
    "hit": "□",
    "miss": "x",
    "start_coord": "S",
    "end_coords": "E",
}
