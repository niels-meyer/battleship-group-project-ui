from collections import defaultdict

from utils.app_types import EAIDifficulty

from .llm_ai import LLMM_AI

testBoard = (
    (
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": "Cruiser"},
        {"is_shot": True, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": "Cruiser"},
        {"is_shot": True, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": "Cruiser"},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": "Battleship"},
        {"is_shot": False, "ship": "Battleship"},
        {"is_shot": False, "ship": "Battleship"},
        {"is_shot": False, "ship": "Battleship"},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": "Submarine"},
        {"is_shot": False, "ship": "Submarine"},
        {"is_shot": False, "ship": "Submarine"},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": "Destroyer"},
    ),
    (
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": "Destroyer"},
    ),
)

def get_remaining_ships(board):
    total_cells = defaultdict(int)
    hit_cells = defaultdict(int)

    for row in board:
        for cell in row:
            ship = cell["ship"]
            if ship is None:
                continue

            total_cells[ship] += 1
            if cell["is_shot"]:
                hit_cells[ship] += 1

    remaining_ships = []

    for ship in total_cells:
        if hit_cells[ship] < total_cells[ship]:
            remaining_ships.append(ship)

    return remaining_ships

def board_to_string(board):
    hits = []
    missed_shots = []
    remaining = []

    for row_idx, row in enumerate(board):
        row_letter = chr(ord('A') + row_idx)  # Convert 0->A, 1->B, etc.
        for col_idx, cell in enumerate(row):
            col_str = str(col_idx + 1)  # Convert 0-indexed to 1-indexed
            coord = row_letter + col_str

            if cell["is_shot"]:
                if cell["ship"]:
                    hits.append(coord)
                else:
                    missed_shots.append(coord)
            else:
                remaining.append(coord)

    return {
        "hits": hits,
        "missed_shots": missed_shots,
        "remaining": remaining
    }

testAI = LLMM_AI(difficulty=EAIDifficulty.HARD)
stringBoard = board_to_string(testBoard)
print(get_remaining_ships(testBoard))
print(stringBoard)
print(testAI.get_next_attack(stringBoard, remaining_ships=get_remaining_ships(testBoard)))
