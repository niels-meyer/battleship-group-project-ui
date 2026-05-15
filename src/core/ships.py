from src.app_types import TShips, TShipCoords, TCoord

class Ships:
    def __init__(self):
        self._ships: TShips = {}
        self._has_ships: bool = False

    def get_ships(self) -> TShips:
        return self._ships

    def has_ships(self) -> bool:
        return self._has_ships

    def add_ship(self, ship_name: str, ship_coords: TShipCoords) -> None:
        self._ships[ship_name] = ship_coords
        self._has_ships = True

    def remove_ship(self, ship_name: str) -> None:
        del self._ships[ship_name]

        if len(self._ships) == 0:
            self._has_ships = False

    def decrease_ship(self, ship_name: str, coord: TCoord) -> None:
        self._ships[ship_name].remove(coord)
        
        if len(self._ships[ship_name]) == 0:
            self.remove_ship(ship_name)