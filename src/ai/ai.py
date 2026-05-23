import random
from typing import Any, Callable
from src.ai.algorithmic_ai import SimpleBattleshipAI
try:
    from src.ai.llm_ai import LLM_AI
except ImportError:
    LLM_AI = None
from src.utils.app_types import EAIDifficulty, TRemainingCells, TCoord, TShipCoords, TBoard
from src.utils.constants import ROWS, COLUMNS, SHIPS
from src.core.player import Player

class AI(Player):
    def __init__(self, name: str, difficulty: EAIDifficulty):
        super().__init__(name)
        self._opponent_remaining_cells: TRemainingCells = self._generate_opponent_remaining_cells()
        self.difficulty = difficulty

    def _generate_opponent_remaining_cells(self) -> TRemainingCells:
        return {row: COLUMNS.copy() for row in ROWS}

    def _get_random_opponent_remaining_cell(self) -> TCoord | None:
        if not self._opponent_remaining_cells:
            return None

        row = random.choice(list(self._opponent_remaining_cells.keys()))
        column = random.choice(self._opponent_remaining_cells[row])
        return (row, column)

    def get_random_ship_placement_coords(self, ship_length: int) -> TShipCoords:
        board = self.board.get_board()
        row_count, column_count = len(ROWS), len(COLUMNS)
        placements: list[tuple[int, TShipCoords]] = []

        for row_i in range(row_count):
            for column_i in range(column_count):
                for delta_row, delta_column in ((0, 1), (1, 0)):
                    end_row_i = row_i + delta_row * (ship_length - 1)
                    end_column_i = column_i + delta_column * (ship_length - 1)
                    if end_row_i >= row_count or end_column_i >= column_count:
                        continue

                    ship_coords = [
                        (ROWS[row_i + delta_row * offset], COLUMNS[column_i + delta_column * offset])
                        for offset in range(ship_length)
                    ]
                    if any(board[r][c]["ship"] for r, c in (
                        (row_i + delta_row * offset, column_i + delta_column * offset)
                        for offset in range(ship_length)
                    )):
                        continue

                    occupied = {
                        (row_i + delta_row * offset, column_i + delta_column * offset)
                        for offset in range(ship_length)
                    }
                    score = 0
                    for ship_row_i, ship_column_i in occupied:
                        score += min(ship_row_i, row_count - 1 - ship_row_i)
                        score += min(ship_column_i, column_count - 1 - ship_column_i)

                        for neighbor_row_i in range(ship_row_i - 1, ship_row_i + 2):
                            for neighbor_column_i in range(ship_column_i - 1, ship_column_i + 2):
                                if not (0 <= neighbor_row_i < row_count and 0 <= neighbor_column_i < column_count):
                                    continue
                                if (neighbor_row_i, neighbor_column_i) in occupied:
                                    continue
                                if board[neighbor_row_i][neighbor_column_i]["ship"]:
                                    score -= 8
                                else:
                                    score += 1

                    placements.append((score, ship_coords))

        if not placements:
            raise ValueError(f"No valid placement available for ship length {ship_length}.")

        best_score = max(score for score, _ in placements)
        best_placements = [coords for score, coords in placements if score == best_score]
        return random.choice(best_placements)

    # --- Override ---
    def place_ship(self, ship_name: str, ship_coords: TShipCoords | None = None) -> None:
        ship_length = SHIPS[ship_name]["length"]
        if ship_coords is None:
            ship_coords = self.get_random_ship_placement_coords(ship_length)

        super().place_ship(ship_name, ship_coords)

    def _select_target_coord(self, player: "Player") -> TCoord:
        """Select a target coordinate routed by difficulty level."""
        strategy_chain = self._get_target_strategies(player)

        for strategy in strategy_chain:
            coord = strategy()
            if coord is not None:
                return coord

        raise RuntimeError("No remaining target cells available for AI")


    def _get_target_strategies(self, player: "Player") -> list[Callable[[], TCoord | None]]:
        if self.difficulty in (EAIDifficulty.NORMAL, EAIDifficulty.HARD, EAIDifficulty.IMPOSSIBLE):
            return [
                lambda: self._get_algorithmic_ai_coord(player),
                self._get_random_opponent_remaining_cell,
            ]

        if self.difficulty == EAIDifficulty.EASY:
            return [
                lambda: self._get_llm_ai_coord(player),
                self._get_random_opponent_remaining_cell,
            ]

        return [self._get_random_opponent_remaining_cell]

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
        for row_i, row in enumerate(board):
            for col_i, cell in enumerate(row):
                if not cell["is_shot"]:
                    continue

                coord = f"{ROWS[row_i]}{COLUMNS[col_i]}"
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
        algorithmic_ai = SimpleBattleshipAI(difficulty=self.difficulty)
        row_index, column_index = algorithmic_ai.decide_shot(snapshot["board_view"])
        coord = (ROWS[row_index], COLUMNS[column_index])
        return coord if self._is_valid_remaining_coord(coord) else None

    def _get_llm_ai_coord(self, player: Player) -> TCoord | None:
        if self.difficulty != EAIDifficulty.EASY or LLM_AI is None:
            return None

        try:
            llm_ai = LLM_AI(difficulty=self.difficulty)
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
