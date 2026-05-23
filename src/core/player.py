from typing import TYPE_CHECKING
from src.utils.app_types import EAIDifficulty
from src.utils.app_types import TCoord, TShipCoords
from src.core.board import Board
from src.core.ships import Ships

if TYPE_CHECKING:
    from src.database.match import Match

class Player:
    def __init__(self, name: str):
        self.db_player = self._get_or_create_player(name)
        self.board: Board = Board()
        self.ships: Ships = Ships()

    def place_ship(self, ship_name: str, ship_coords: TShipCoords) -> None:
        self.ships.add_ship(ship_name, ship_coords)
        self.board.add_ship(ship_name, ship_coords)

    def shoot_player(self, player: "Player", coord: TCoord) -> bool:
        """Shoots at coord on player's board. Returns True if a ship was hit."""
        ship = player.board.shoot_ship(coord)
        if ship:
            player.ships.decrease_ship(ship, coord)
        return ship is not None

    def save_match(self, number_of_rounds: int, has_player_won: bool, ai_difficulty: EAIDifficulty) -> "Match":
        """Persist one finished match for this player."""
        from src.database import match as stats_match

        if self.db_player.id is None:
            raise ValueError("Player ID must be available before saving a match.")

        return stats_match.create_match(
            player_id=self.db_player.id,
            number_of_rounds=number_of_rounds,
            has_player_won=has_player_won,
            ai_difficulty=ai_difficulty.value,
        )

    def _get_or_create_player(self, name: str):
        """Fetch the DB player by name or create it when missing."""
        from src.database import player

        db_player = player.get_player_by_name(name)
        if db_player:
            return db_player
        return player.create_player(name)

