from app_types import TBoard, TCoord, TShipCoords, TShips
from board import Board
from ships import Ships

class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.board: TBoard = Board()
        self.ships: TShips = Ships()

    def place_ship(self, ship_name: str, ship_coords: TShipCoords) -> None:
        self.ships.add_ship(ship_name, ship_coords)
        self.board.add_ship(ship_name, ship_coords)
    
    def shoot_player(self, player: "Player", coord: TCoord) -> None:
        ship = player.board.shoot_ship(coord)

        if ship:
            player.ships.decrease_ship(ship, coord)

        print(f"{self.name.capitalize()} shot at \"{coord[0]} {coord[1]}\" and {'hit a ship!' if ship else 'missed.'}")