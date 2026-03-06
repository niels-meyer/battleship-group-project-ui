import random
from app_types import EAIDifficulty, TRemainingCells, TCoord, TShipCoords
from player import Player
from config import get_rows, get_columns, get_ships
from utils import suggest_ship_end_coords, get_coords_between

class AI(Player):
    def __init__(self, name: str, difficulty: EAIDifficulty):
        super().__init__(name)
        self._opponent_remaining_cells: TRemainingCells = self._generate_opponent_remaining_cells()
        self.difficulty = difficulty

    def _generate_opponent_remaining_cells(self) -> TRemainingCells:
        return { row: get_columns().copy() for row in get_rows() }

    def _get_random_opponent_remaining_cell(self) -> TCoord | None:
        # TODO: Improve AI shooting logic, make it smarter
        if not self._opponent_remaining_cells:
            return None

        row = random.choice(list(self._opponent_remaining_cells.keys()))
        column = random.choice(self._opponent_remaining_cells[row])

        return (row, column)

    def get_random_ship_placement_coords(self, ship_length: int) -> TShipCoords:
        # TODO: Improve AI ship placement logic, make it smarter
        rows = get_rows()
        columns = get_columns()
        
        start_coord = (random.choice(rows), random.choice(columns))
        
        valid_end_coords = suggest_ship_end_coords(self.board, start_coord, ship_length)
        
        if not valid_end_coords:
            return self.get_random_ship_placement_coords(ship_length)
        
        end_coord = random.choice(valid_end_coords)
        
        return get_coords_between(start_coord, end_coord)

    # --- Override ---
    def place_ship(self, ship_name) -> None:
        ships = get_ships()
        ship_length = ships[ship_name]["length"]
        ship_coords = self.get_random_ship_placement_coords(ship_length)

        super().place_ship(ship_name, ship_coords)

    def shoot_player(self, player: Player) -> None:
        if self.difficulty == EAIDifficulty.BABY:
            # BABY AI shoots randomly without any strategy
            coord = self._get_random_opponent_remaining_cell()
        else:
            # TODO: Implement more sophisticated AI shooting logic based on difficulty
            coord = None

        row, column = coord

        self._opponent_remaining_cells[row].remove(column)

        if not self._opponent_remaining_cells[row]:
            del self._opponent_remaining_cells[row]

        super().shoot_player(player, coord)

    