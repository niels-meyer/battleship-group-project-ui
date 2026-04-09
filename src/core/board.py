from typing import Sequence
from src.utils.app_types import TBoard, TBoardShip, TCoord, TShipCoords
from src.config.config import get_rows, get_columns
from src.utils.helper import get_coord_index, get_row_index, get_column_index, get_row, get_column, get_coords_between


class Board:
    def __init__(self):
        self._board: TBoard = self._generate_empty_board()

    def _generate_empty_board(self) -> TBoard:
        return tuple(
            tuple({ "is_shot": False, "ship" : None} for _ in get_columns())
            for _ in get_rows()
        )

    def get_board(self) -> TBoard:
        return self._board


    def add_ship(self, ship_name, ship_coords: TShipCoords) -> None:
        for row, column in ship_coords:
            row_i, column_i = get_row_index(row), get_column_index(column)

            self._board[row_i][column_i]["ship"] = ship_name
    
    def shoot_ship(self, coord: TCoord) -> TBoardShip:
        row_i, column_i = get_coord_index(coord)
        cell = self._board[row_i][column_i]

        cell["is_shot"] = True

        return cell["ship"]