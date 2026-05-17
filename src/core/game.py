import random
from typing import Optional
from src.ai.difficulty import get_default_ai_difficulty
from src.app_types import EAIDifficulty, TCoord, TBoard
from src.ai.ai import AI
from src.constants import SHIPS
from src.core.player import Player
from src.utils.helpers import suggest_ship_end_coords, get_coords_between, get_row_index, get_column_index


class Game:
    def __init__(self, player_name: str, ai_difficulty: EAIDifficulty | None = None):
        self._player = Player(player_name)
        self._ai_difficulty = ai_difficulty or get_default_ai_difficulty()
        self._ai = AI("enemy", difficulty=self._ai_difficulty)
        self._does_player_start = random.choice([True, False])
        self._is_player_turn = self._does_player_start
        self._number_of_rounds = 1
        self._ships_to_place = self._build_ship_queue()
        self._current_ship_index = 0

    def _build_ship_queue(self) -> list[tuple[str, dict[str, int]]]:
        return list(SHIPS.items())

    def _get_current_ship_data(self) -> tuple[str, dict[str, int]] | None:
        if self.all_ships_placed:
            return None
        return self._ships_to_place[self._current_ship_index]

    def _change_turn(self) -> None:
        self._is_player_turn = not self._is_player_turn
        if self._is_player_turn == self._does_player_start:
            self._number_of_rounds += 1

    def _finish_turn(self, hit: bool) -> bool:
        self._change_turn()
        return hit

    # --- Ship Placement ---

    @property
    def all_ships_placed(self) -> bool:
        return self._current_ship_index >= len(self._ships_to_place)

    def get_current_ship(self) -> Optional[tuple[str, int]]:
        """Returns (name, length) for the ship currently being placed, or None if all placed."""
        current_ship = self._get_current_ship_data()
        if current_ship is None:
            return None
        name, data = current_ship
        return name, data["length"]

    def get_valid_end_coords(self, start_coord: TCoord) -> list[TCoord]:
        """Returns legal end coordinates for the current ship starting at start_coord."""
        current = self.get_current_ship()
        if current is None:
            return []
        _, length = current
        return suggest_ship_end_coords(self._player.board.get_board(), start_coord, length)

    def place_player_ship(self, start_coord: TCoord, end_coord: TCoord) -> None:
        """Places the current ship for both the player and the AI, then advances to the next ship."""
        current_ship = self._get_current_ship_data()
        if current_ship is None:
            return

        ship_name, _ = current_ship
        ship_coords = get_coords_between(start_coord, end_coord)
        self._player.place_ship(ship_name, ship_coords)
        self._ai.place_ship(ship_name)
        self._current_ship_index += 1

    # --- Shooting ---

    @property
    def is_player_turn(self) -> bool:
        return self._is_player_turn

    @property
    def number_of_rounds(self) -> int:
        return self._number_of_rounds

    @property
    def ai_difficulty(self) -> EAIDifficulty:
        return self._ai_difficulty

    def is_valid_shot(self, coord: TCoord) -> bool:
        """Returns True if the coord has not already been shot on the AI's board."""
        row_i = get_row_index(coord[0])
        col_i = get_column_index(coord[1])
        return not self._ai.board.get_board()[row_i][col_i]["is_shot"]

    def player_shoot(self, coord: TCoord) -> bool:
        """Executes the player's shot. Returns True if it was a hit."""
        hit = self._player.shoot_player(self._ai, coord)
        return self._finish_turn(hit)

    def ai_shoot(self) -> tuple[TCoord, bool]:
        """Executes the AI's shot. Returns (coord, was_hit)."""
        coord, hit = self._ai.shoot_player_with_coord(self._player)
        return coord, self._finish_turn(hit)

    # --- Board Access ---

    def get_player_board(self) -> TBoard:
        return self._player.board.get_board()

    def get_ai_board(self) -> TBoard:
        return self._ai.board.get_board()

    # --- Game State ---

    @property
    def is_game_over(self) -> bool:
        return not self._player.ships.has_ships() or not self._ai.ships.has_ships()

    @property
    def has_player_won(self) -> bool:
        return self._player.ships.has_ships()

    def finish(self) -> None:
        """Persists the match outcome to the database."""
        self._player.save_match(
            number_of_rounds=self._number_of_rounds,
            has_player_won=self.has_player_won,
            ai_difficulty=self._ai_difficulty,
        )