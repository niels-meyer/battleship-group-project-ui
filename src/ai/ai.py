import random
from typing import Any
from src.ai.algorithmic_ai import SimpleBattleshipAI
try:
    from src.ai.llm_ai import LLMM_AI
except ImportError:
    LLMM_AI = None
from src.app_types import EAIDifficulty, TRemainingCells, TCoord, TShipCoords, TBoard
from src.config.config import get_rows, get_columns, get_ships
from src.core.player import Player
from src.utils.helpers import suggest_ship_end_coords, get_coords_between

class AI(Player):
    def __init__(self, name: str, difficulty: EAIDifficulty):
        super().__init__(name)
        self._opponent_remaining_cells: TRemainingCells = self._generate_opponent_remaining_cells()
        self.difficulty = difficulty

    def _generate_opponent_remaining_cells(self) -> TRemainingCells:
        return {row: get_columns().copy() for row in get_rows()}

    def _get_random_opponent_remaining_cell(self) -> TCoord | None:
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
        
        valid_end_coords = suggest_ship_end_coords(self.board.get_board(), start_coord, ship_length)
        
        if not valid_end_coords:
            return self.get_random_ship_placement_coords(ship_length)

        end_coord = random.choice(valid_end_coords)
        return get_coords_between(start_coord, end_coord)

    # --- Override ---
    def place_ship(self, ship_name: str, ship_coords: TShipCoords | None = None) -> None:
        ships = get_ships()
        ship_length = ships[ship_name]["length"]
        if ship_coords is None:
            ship_coords = self.get_random_ship_placement_coords(ship_length)

        super().place_ship(ship_name, ship_coords)

    def _select_target_coord(self, player: "Player") -> TCoord:
        """Select a target coordinate routed by difficulty level."""
        if self.difficulty in (EAIDifficulty.NORMAL, EAIDifficulty.HARD, EAIDifficulty.IMPOSSIBLE):
            coord = self._get_algorithmic_ai_coord(player)
            if coord is not None:
                return coord
        if self.difficulty == EAIDifficulty.EASY:
            coord = self._get_llm_ai_coord(player)
            if coord is not None:
                return coord
        coord = self._get_random_opponent_remaining_cell()
        if coord is None:
            raise RuntimeError("No remaining target cells available for AI")
        return coord

    def shoot_player(self, player: Player, coord: TCoord | None = None) -> bool:
        """Shoots at the provided coord or picks one automatically if missing."""
        if coord is None:
            coord = self._select_target_coord(player)

        if coord is None or not self._is_valid_remaining_coord(coord):
            coord = self._get_random_opponent_remaining_cell()

        if coord is None:
            raise ValueError("AI could not determine a valid coordinate to shoot.")

        row, column = coord
        self._opponent_remaining_cells[row].remove(column)

        if not self._opponent_remaining_cells[row]:
            del self._opponent_remaining_cells[row]

        return super().shoot_player(player, coord)

    def shoot_player_with_coord(self, player: Player) -> tuple[TCoord, bool]:
        """Selects a coordinate based on difficulty and shoots. Returns (coord, was_hit)."""
        coord = self._select_target_coord(player)
        hit = self.shoot_player(player, coord)
        return coord, hit

    def _is_valid_remaining_coord(self, coord: TCoord) -> bool:
        row, column = coord
        return row in self._opponent_remaining_cells and column in self._opponent_remaining_cells[row]

    def _get_board_snapshot(self, player: Player) -> dict[str, Any]:
        board = player.board.get_board()
        remaining_ship_names = set(player.ships.get_ships().keys())

        board_view: TBoard = tuple(
            tuple(
                {
                    "is_shot": cell["is_shot"],
                    "ship": cell["ship"] if cell["ship"] in remaining_ship_names else None,
                }
                for cell in row
            )
            for row in board
        )

        hits: list[str] = []
        missed_shots: list[str] = []
        rows = get_rows()
        columns = get_columns()

        for row_i, row in enumerate(board):
            for col_i, cell in enumerate(row):
                if not cell["is_shot"]:
                    continue

                coord = f"{rows[row_i]}{columns[col_i]}"
                if cell["ship"]:
                    hits.append(coord)
                else:
                    missed_shots.append(coord)

        remaining = [
            f"{row}{column}"
            for row, cols in self._opponent_remaining_cells.items()
            for column in cols
        ]

        return {
            "board_view": board_view,
            "llm_payload": {"hits": hits, "missed_shots": missed_shots, "remaining": remaining},
            "remaining_ships": list(remaining_ship_names),
        }

    def _get_algorithmic_ai_coord(self, player: Player) -> TCoord | None:
        snapshot = self._get_board_snapshot(player)
        algorithmic_ai = SimpleBattleshipAI(board_size=len(get_rows()), difficulty=self.difficulty)
        row_index, column_index = algorithmic_ai.decide_shot(snapshot["board_view"])
        coord = (get_rows()[row_index], get_columns()[column_index])
        return coord if self._is_valid_remaining_coord(coord) else None

    def _get_llm_ai_coord(self, player: Player) -> TCoord | None:
        if self.difficulty != EAIDifficulty.EASY or LLMM_AI is None:
            return None

        try:
            llm_ai = LLMM_AI(difficulty=self.difficulty)
        except Exception:
            return None

        snapshot = self._get_board_snapshot(player)

        for _ in range(3):
            try:
                coord = llm_ai.get_next_attack(snapshot["llm_payload"], snapshot["remaining_ships"])
            except Exception:
                continue

            if coord is not None:
                return coord

        return None
