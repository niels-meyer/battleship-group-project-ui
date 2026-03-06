import asyncio
from llm_ai import LLMM_AI
from app_types import EAIDifficulty

testBoard = (
    (
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": "Carrier"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": "Battleship"},
        {"is_shot": True, "ship": "Battleship"},
        {"is_shot": True, "ship": "Battleship"},
        {"is_shot": True, "ship": "Battleship"},
    ),
    (
        {"is_shot": True, "ship": "Cruiser"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": "Destroyer"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": "Submarine"},
        {"is_shot": True, "ship": "Submarine"},
        {"is_shot": True, "ship": "Submarine"},
    ),
    (
        {"is_shot": True, "ship": "Cruiser"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": False, "ship": "Destroyer"},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": True, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
    (
        {"is_shot": False, "ship": "Cruiser"},
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
        {"is_shot": True, "ship": None},
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
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
        {"is_shot": False, "ship": None},
    ),
)

def board_to_string(board):
    letters = "abcdefghij"
    output = "  1 2 3 4 5 6 7 8 9 10\n"

    for i, row in enumerate(board):
        row_symbols = []

        for cell in row:
            if not cell["is_shot"]:
                row_symbols.append("~")
            elif cell["ship"] is None:
                row_symbols.append("M")
            else:
                row_symbols.append("H")

        output += letters[i] + " " + " ".join(row_symbols) + "\n"

    return output

async def main():
    testAI = LLMM_AI(difficulty=EAIDifficulty.HARD)
    stringBoard = board_to_string(testBoard)
    print(stringBoard)
    print(await testAI.get_next_attack(testBoard))

asyncio.run(main())