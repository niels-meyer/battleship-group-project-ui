import random
from app_types import TRemainingCells, TCoord
from player import Player
from config import get_rows, get_columns

class AI(Player):
    def __init__(self):
        super().__init__("AI")
        self._opponent_remaining_cells: TRemainingCells = self._generate_opponent_remaining_cells()

    def _generate_opponent_remaining_cells(self) -> TRemainingCells:
        return { row: get_columns().copy() for row in get_rows() }

    def _get_random_opponent_remaining_cell(self) -> TCoord | None:
        if not self._opponent_remaining_cells:
            return None

        row = random.choice(list(self._opponent_remaining_cells.keys()))
        column = random.choice(self._opponent_remaining_cells[row])

        return (row, column)
    
    def _get_random_ship_placement_coord(self) -> TCoord | None:
        pass

    # --- Override ---
    
    def place_ship(self, ship_name: str) -> None:
        start_coord, end_coord = self._get_random_ship_placement_coord()
        
        super().place_ship(ship_name, start_coord, end_coord)

    def shoot_player(self, player: Player) -> bool:
        coord = self._get_random_opponent_remaining_cell()
        row, column = coord

        self._opponent_remaining_cells[row].remove(column)

        if not self._opponent_remaining_cells[row]:
            del self._opponent_remaining_cells[row]

        return super().shoot_player(player, coord)

    