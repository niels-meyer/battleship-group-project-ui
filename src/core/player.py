from utils.app_types import TCoord, TShipCoords
from .board import Board
from .ships import Ships

class Player:
    def __init__(self, name: str):
        self.player = self._get_or_create_player(name)
        self.board: Board = Board()
        self.ships: Ships = Ships()

    def place_ship(self, ship_name: str, ship_coords: TShipCoords) -> None:
        self.ships.add_ship(ship_name, ship_coords)
        self.board.add_ship(ship_name, ship_coords)
    
    def shoot_player(self, player: "Player", coord: TCoord) -> None:
        ship = player.board.shoot_ship(coord)

        if ship:
            player.ships.decrease_ship(ship, coord)

        print(f"{self.player.name.capitalize()} shot at \"{coord[0]} {coord[1]}\" and {'hit a ship!' if ship else 'missed.'}")

    def save_match(self, number_of_rounds: int, has_player_won: bool):
        from src.stats import match as stats_match
        return stats_match.create_match(
            player_id = self.player.id,
            number_of_rounds = number_of_rounds,
            has_player_won = has_player_won
        )

    def _get_or_create_player(self, name: str):
        from src.stats import player

        db_player = player.get_player_by_name(name)
        if db_player:
            return db_player
        
        return player.create_player(name)
    
    