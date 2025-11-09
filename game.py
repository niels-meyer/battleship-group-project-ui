import random
from InquirerPy import inquirer
from constants import PlayerType
from config import get_ships
from utils import parse_coord, suggest_ship_end_coords, get_coords_between
from player import Player
from ai import AI

class Game:
    def __init__(self):
        self._player = Player("player")
        self._ai = AI()
        self._current_turn = random.choice(list(PlayerType))

    def _setup_board(self) -> None:
        ships = get_ships()

        print("Place your ships.")

        # --- Player ship placement ---
        for ship_name, ship_data in ships.items():
            ship_length = ship_data["length"]
            is_ship_placed: bool = False

            print(f"\nShip: {ship_name}\nLength: {ship_length}")

            while not is_ship_placed:
                try:
                    start_input_coord = input(f"\nEnter start coordinate: ")
                    start_coord = parse_coord(start_input_coord)
                except ValueError as e:
                    print(e)
                    continue

                valid_end_coords = suggest_ship_end_coords(self._player.board, start_coord, ship_length)

                if not len(valid_end_coords):
                    print(f"Ship cannot be placed there, overlaps or out of bounds.")
                    continue
                
                end_input_coord = inquirer.select(
                    message="Choose legal end coordinate:",
                    choices=[f"{row} {column}" for row, column in valid_end_coords]+["Back"]
                ).execute()

                if end_input_coord == "Back":
                    continue

                end_coord = parse_coord(end_input_coord)
                ship_coords = get_coords_between(start_coord, end_coord)

                self._player.place_ship(ship_name, ship_coords)
                is_ship_placed = True

        print(self._player.ships.get_ships())
        print(self._player.board.get_board())

        # --- AI ship placement ---

        # TODO: Smart AI

    def start(self) -> None:
        self._setup_board()