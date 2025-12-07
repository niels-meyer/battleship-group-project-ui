from typing import List
from app_types import TBoard
from config import get_rows, get_columns, get_cell_symbols

_cell_symbols = get_cell_symbols()
_row_labels = get_rows()
_column_labels = get_columns()

_cell_width = 3
_cell_separator_width = 1
_cell_separator = " " * _cell_separator_width
_board_separator_width = 5
_board_separator = " " * _board_separator_width
_board_length = len(_column_labels)
_board_width = ((_board_length+1) * _cell_width) + (_board_length * _cell_separator_width)

_PLAYER_BOARD = "PLAYER BOARD"
_ENEMY_BOARD = "ENEMY BOARD"

def _get_cell_data(board: TBoard,row_index: int, column_index: int):
    return board[row_index][column_index]

def _get_cell_symbol(cell, reveal_ship = False):
    if cell["is_shot"] and cell["ship"]:
        return _cell_symbols["hit"]
    elif cell["is_shot"] and not cell["ship"]:
        return _cell_symbols["miss"]
    elif not cell["is_shot"] and cell["ship"] and reveal_ship:
        return _cell_symbols["ship"]
    else:
        return _cell_symbols["empty"]

def _render_cell(symbol: str):
    return f"{symbol:^{_cell_width}}"

def _join_cells(cells: List[str]):
    return _cell_separator.join(cells)

def _render_board_battleground_row_cells(board: TBoard, row_index: int, reveal_ship: bool):
    cells = []
    for column_index in range(_board_length):
        cell_data = _get_cell_data(board, row_index, column_index)
        cell_symbol = _get_cell_symbol(cell_data, reveal_ship=reveal_ship)
        cell = _render_cell(cell_symbol)
        cells.append(cell)
    return cells

def _print_empty_line():
    print("")

def print_boards(player_board, enemy_board):
    _print_empty_line()

    # Legend
    print("\nLegend:")
    print(f"  {_cell_symbols['empty']} : water")
    print(f"  {_cell_symbols['miss']} : miss")
    print(f"  {_cell_symbols['hit']} : hit")
    print(f"  {_cell_symbols['ship']} : ship")

    _print_empty_line()

    # Header line
    player_board_header = f"{_PLAYER_BOARD:^{_board_width}}"
    enemy_board_header = f"{_ENEMY_BOARD:^{_board_width}}"
    print(player_board_header + _board_separator + enemy_board_header)

    # Column labels line
    row_label_placeholder_cell = _render_cell(" ")
    column_label_cells = [_render_cell(column_label) for column_label in _column_labels]
    board_column_labels_row = _join_cells([row_label_placeholder_cell] + column_label_cells)
    print(board_column_labels_row + _board_separator + board_column_labels_row)

    # Battleground row lines
    for row_index, row_label in enumerate(_row_labels):
        row_label_cell = _render_cell(row_label)
        player_board_battleground_row_cells = _render_board_battleground_row_cells(player_board, row_index, reveal_ship=True)
        enemy_board_battleground_row_cells = _render_board_battleground_row_cells(enemy_board, row_index, reveal_ship=False)
        player_board_row = _join_cells([row_label_cell] + player_board_battleground_row_cells)
        enemy_board_row = _join_cells([row_label_cell] + enemy_board_battleground_row_cells)
        print(player_board_row + _board_separator + enemy_board_row)

    _print_empty_line()