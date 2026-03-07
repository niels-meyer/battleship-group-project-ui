from AI.algorithmic_ai import SimpleBattleshipAI
from app_types import EAIDifficulty


def create_initial_board():
    """Create the initial game board with all ships placed."""
    return (
        (
            {"is_shot": False, "ship": "Carrier"},
            {"is_shot": False, "ship": "Carrier"},
            {"is_shot": False, "ship": "Carrier"},
            {"is_shot": False, "ship": "Carrier"},
            {"is_shot": False, "ship": "Carrier"},
            {"is_shot": False, "ship": None},
            {"is_shot": False, "ship": None},
            {"is_shot": False, "ship": "Cruiser"},
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
            {"is_shot": False, "ship": "Cruiser"},
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


def update_board(board, shot_row, shot_col):
    """
    Update the board after a shot at the given coordinates.
    If a ship is fully sunk, remove its ship value from all cells.
    """
    board_list = [list(row) for row in board]
    cell = board_list[shot_row][shot_col]
    
    # Mark cell as shot
    board_list[shot_row][shot_col] = {
        "is_shot": True,
        "ship": cell["ship"]
    }
    
    # If this was a hit, check if the ship is now fully sunk
    if cell["ship"] is not None:
        ship_name = cell["ship"]
        # Count remaining unhit cells for this ship
        remaining_hits = 0
        for row in range(10):
            for col in range(10):
                if board_list[row][col]["ship"] == ship_name and not board_list[row][col]["is_shot"]:
                    remaining_hits += 1
        
        # If no remaining hits, sink the ship (remove ship value from all cells)
        if remaining_hits == 0:
            for row in range(10):
                for col in range(10):
                    if board_list[row][col]["ship"] == ship_name:
                        board_list[row][col] = {
                            "is_shot": board_list[row][col]["is_shot"],
                            "ship": None
                        }
    
    # Convert back to tuple structure
    return tuple(tuple(row) for row in board_list)


def print_board(board, title="Board State"):
    """Print a visual representation of the board."""
    print(f"\n{title}")
    print("   ", end="")
    for col in range(10):
        print(f"{col:2} ", end="")
    print()
    print("   " + "-" * 33)
    
    for row in range(10):
        print(f"{row:2}|", end="")
        for col in range(10):
            cell = board[row][col]
            if cell["is_shot"]:
                if cell["ship"]:
                    print(" X ", end="")  # Hit
                else:
                    print(" O ", end="")  # Miss
            else:
                if cell["ship"]:
                    print(" S ", end="")  # Ship (unexposed)
                else:
                    print(" . ", end="")  # Empty
        print("|")


def run_simulation(num_turns=50, verbose=False):
    """Simulate AI gameplay for a specified number of turns."""
    if verbose:
        print("=" * 50)
        print("BATTLESHIP AI V2 SIMULATION")
        print("=" * 50)
    
    board = create_initial_board()
    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.IMPOSSIBLE)
    
    if verbose:
        print_board(board, "Initial Board (S=Ship, .=Empty, X=Hit, O=Miss)")
    
    unsunk_count_history = []
    strategy_history = []
    
    for turn in range(1, num_turns + 1):
        # Get AI decision
        shot_row, shot_col = ai.decide_shot(board)
        
        # Check result
        cell = board[shot_row][shot_col]
        is_hit = cell["ship"] is not None
        
        if verbose:
            print(f"\n{'='*50}")
            print(f"TURN {turn}/{num_turns}")
            print(f"{'='*50}")
            print(f"AI Strategy: {ai.current_strategy.value.upper()}")
            print(f"AI Shoots at: ({shot_row}, {shot_col})", end="")
        
        if is_hit:
            if verbose:
                print(f" - HIT on {cell['ship']}! 🎯")
        else:
            if verbose:
                print(f" - MISS! 💧")
        
        # Update board
        board = update_board(board, shot_row, shot_col)
        
        if verbose:
            print_board(board, f"Board after Turn {turn}")
        
        # Count unsunk hits on board
        unsunk = sum(1 for r in range(10) for c in range(10) 
                     if board[r][c]["is_shot"] and board[r][c]["ship"] is not None)
        
        if verbose:
            print(f"\nAI Stats:")
            print(f"  Shots Fired: {len(ai.last_shots)}")
            print(f"  Unsunk Hits: {unsunk}")
        
        unsunk_count_history.append(unsunk)
        strategy_history.append(ai.current_strategy.value)
    
    # Print final summary
    if verbose:
        print(f"\n{'='*50}")
        print("SIMULATION COMPLETE")
        print(f"{'='*50}")
    
    print(f"Final Stats after {num_turns} turns:")
    print(f"  Shots fired: {len(ai.last_shots)}")
    print(f"  Final unsunk hits: {unsunk_count_history[-1]}")
    
    # Count strategy switches
    changes = sum(1 for i in range(1, len(strategy_history)) 
                  if strategy_history[i] != strategy_history[i-1])
    print(f"  Strategy switches: {changes}")
    
    print(f"\nStrategy Timeline:")
    last_strategy = None
    for turn, strategy in enumerate(strategy_history, 1):
        if strategy != last_strategy:
            unsunk = unsunk_count_history[turn-1]
            print(f"  Turn {turn:2d}: → {strategy.upper():6} (unsunk ships: {unsunk})")
            last_strategy = strategy
    
    return ai, board


if __name__ == "__main__":
    print("\n" + "="*50)
    print("V2: STATELESS ALGORITHM - 50 TURNS VERBOSE")
    print("="*50)
    ai, board = run_simulation(num_turns=17, verbose=True)