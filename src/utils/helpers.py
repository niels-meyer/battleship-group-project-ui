from typing import Sequence
from src.app_types import TBoard, TCoord, TShipCoords
from src.config.config import get_columns, get_rows

_row_lookup = {row: i for i, row in enumerate(get_rows())}
_column_lookup = {column: i for i, column in enumerate(get_columns())}

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

def get_row_index(row: str) -> int:
    if not is_row_exists(row):
        raise ValueError(f"Row '{row}' does not exist.")
    return _row_lookup[row]

def get_column_index(column: str) -> int:
    if not is_column_exists(column):
        raise ValueError(f"Column '{column}' does not exist.")
    return _column_lookup[column]

def get_coord_index(coord: TCoord) -> tuple[int, int]:
    row, column = coord
    return (get_row_index(row), get_column_index(column))

def get_coords_between(start_coord: TCoord, end_coord: TCoord) -> TShipCoords:
    start_row, start_column = start_coord
    end_row, end_column = end_coord
    start_row_i, start_column_i = get_row_index(start_row), get_column_index(start_column)
    end_row_i, end_column_i = get_row_index(end_row), get_column_index(end_column)
    row_range = range(min(start_row_i, end_row_i), max(start_row_i, end_row_i) + 1)
    column_range = range(min(start_column_i, end_column_i), max(start_column_i, end_column_i) + 1)
    coords: TShipCoords = []
    for row_i in row_range:
        for column_i in column_range:
            row_value = get_row(row_i)
            column_value = get_column(column_i)
            if row_value is None or column_value is None:
                raise ValueError("Generated coordinate is out of bounds.")
            coords.append((row_value, column_value))
    return coords

def is_coord_correct_format(coord: tuple[str, ...]) -> bool:
    return len(coord) == 2

def is_coord_exists(coord: TCoord) -> bool:
    row, column = coord
    return is_row_exists(row) and is_column_exists(column)

def is_ship_placeable(board: TBoard, start_coord: TCoord, end_coord: TCoord) -> bool:
    ship_coords: Sequence[TCoord] = get_coords_between(start_coord, end_coord)
    if not ship_coords:
        return False
    rows_length, columns_length = len(get_rows()), len(get_columns())
    for row, column in ship_coords:
        row_i, column_i = get_row_index(row), get_column_index(column)
        if row_i >= rows_length or column_i >= columns_length:
            return False
        if board[row_i][column_i]["ship"]:
            return False
    return True

def parse_coord(input_coord: str) -> TCoord:
    raw_coord = tuple(input_coord.strip().split())
    if not is_coord_correct_format(raw_coord):
        raise ValueError("Invalid format. Use 'row column', e.g. 'a 1'.")
    coord: TCoord = (raw_coord[0], raw_coord[1])
    if not is_coord_exists(coord):
        raise ValueError(f"Coordinate '{input_coord}' does not exist.")
    return coord

def suggest_ship_end_coords(board: TBoard, start_coord: TCoord, ship_length: int) -> list[TCoord]:
    start_row, start_column = start_coord
    start_row_i, start_column_i = get_row_index(start_row), get_column_index(start_column)
    directions = {
        "top": (-1, 0),
        "right": (0, 1),
        "bottom": (1, 0),
        "left": (0, -1),
    }
    suggestions: list[TCoord] = []
    for delta_row, delta_column in directions.values():
        end_row_i = start_row_i + delta_row * (ship_length - 1)
        end_column_i = start_column_i + delta_column * (ship_length - 1)
        end_row, end_column = get_row(end_row_i), get_column(end_column_i)
        if end_row is None or end_column is None:
            continue
        end_coord: TCoord = (end_row, end_column)
        if is_ship_placeable(board, start_coord, end_coord):
            suggestions.append(end_coord)
    return suggestions