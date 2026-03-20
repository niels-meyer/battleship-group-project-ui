import os
from typing import Sequence, List
from .app_types import TCoord, TBoard, TShipCoords
from config.config import get_rows, get_columns

_row_lookup = {row: i for i, row in enumerate(get_rows())}
_column_lookup = {column: i for i, column in enumerate(get_columns())}

# --- Getter ---

def is_row_exists(row: str) -> bool:
    return row in _row_lookup

def is_column_exists(column: str) -> bool:
    return column in _column_lookup

def get_row(row_index: int) -> str | None:
    rows = get_rows()
    return rows[row_index] if 0 <= row_index < len(rows) else None

def get_column(column_index: int) -> str | None:
    columns = get_columns()
    return columns[column_index] if 0 <= column_index < len(columns) else None

def get_row_index(row: str) -> int | None:
    return _row_lookup[row] if is_row_exists(row) else None

def get_column_index(column: str) -> int | None:
    return _column_lookup[column] if is_column_exists(column) else None

def get_coord_index(coord: TCoord) -> tuple[int, int]:
    row, column = coord
    return (get_row_index(row), get_column_index(column))

def get_coords_between(start_coord: TCoord, end_coord: TCoord) -> TShipCoords:
    """
    Get all coordinates between two coordinates (including).
    """
    start_row, start_column = start_coord
    end_row, end_column = end_coord
    start_row_i, start_column_i = get_row_index(start_row), get_column_index(start_column)
    end_row_i, end_column_i = get_row_index(end_row), get_column_index(end_column)

    # Define the inclusive ranges
    row_range = range(min(start_row_i, end_row_i), max(start_row_i, end_row_i) + 1)
    column_range = range(min(start_column_i, end_column_i), max(start_column_i, end_column_i) + 1)

    return [(get_row(row_i), get_column(column_i)) for row_i in row_range for column_i in column_range]

# --- Validation ---

def is_coord_correct_format(coord: TCoord) -> bool:
    """
    Check if the coordinate input has a valid format.
    - Must be separated by spaces: "row column" (e.g. 'a 1', 'b 10', 'c    5')
    - Multiple spaces are allowed between/before/after parts
    - Max. 2 parts: row and column
    """
    # Must have exactly 2 parts: row and column
    return len(coord) == 2

def is_coord_exists(coord: TCoord) -> bool:
    """
    Check if the coordinate exists in the predefined rows and columns.
    - Inputs are case-sensitive
    """
    row, column = coord

    return is_row_exists(row) and is_column_exists(column)

def is_ship_placeable(board: TBoard, start_coord: TCoord, end_coord: TCoord) -> bool:
    """
    Check if the coordinate exists in the predefined rows and columns.
    - Inputs are case-sensitive
    """
    ship_coords: Sequence[TCoord] = get_coords_between(start_coord, end_coord)

    if not ship_coords:
        return False

    rows_length, columns_length = len(get_rows()), len(get_columns())

    for row, column in ship_coords:
        row_i, column_i = get_row_index(row), get_column_index(column)
        # Bounds check
        if row_i >= rows_length or column_i >= columns_length:
            return False
        # Overlap check
        if board.get_board()[row_i][column_i]["ship"]:
            return False

    return True

# --- Other ---

def parse_coord(input_coord: str) -> TCoord:
    """
    Takes the user's input and returns a structured data. e.g. "a 1" -> ("a", "1")
    - Includes validation that raises 'ValueError' if the input is invalid.
    """
    coord = tuple(input_coord.strip().split())

    if not is_coord_correct_format(coord):
        raise ValueError("Invalid format. Use 'row column', e.g. 'a 1'.")

    if not is_coord_exists(coord):
        raise ValueError(f"Coordinate '{input_coord}' does not exist.")

    return coord

def suggest_ship_end_coords(board: TBoard, start_coord: TCoord, ship_length: int) -> List[TCoord]:
    start_row, start_column = start_coord
    start_row_i, start_column_i = get_row_index(start_row), get_column_index(start_column)

    # Deltas (delta_row, delta_column)
    directions = {
        "top":    (-1,  0),
        "right":  ( 0,  1),
        "bottom": ( 1,  0),
        "left":   ( 0, -1),
    }

    suggestions: List[TCoord] = []

    for delta_row, delta_column in directions.values():
        end_row_i = start_row_i + delta_row * (ship_length - 1)
        end_column_i = start_column_i + delta_column * (ship_length - 1)
        end_row, end_column = get_row(end_row_i), get_column(end_column_i)

        # Exclude if end coord is off the board
        if end_row is None or end_column is None:
            continue

        end_coord: TCoord = (end_row, end_column)

        if is_ship_placeable(board, start_coord, end_coord):
            suggestions.append(end_coord)

    return suggestions

def print_empty_line(number_of_lines: int = 1) -> None:
    print("\n" * (number_of_lines - 1))

def clear_screen():
    """Clear the console screen and scrollback buffer."""
    # Use ANSI escape sequence to clear screen and scrollback buffer
    print('\033[2J\033[H', end='', flush=True)
    # Also call system clear for extra reliability
    os.system("cls" if os.name == "nt" else "clear")
