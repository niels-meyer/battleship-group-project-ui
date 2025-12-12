import random
from InquirerPy import inquirer
from config import get_ships
from display import print_boards
from utils import get_column_index, get_row_index, parse_coord, suggest_ship_end_coords, get_coords_between
from player import Player
from ai import AI

class Game:
    def __init__(self):
        self._player = Player("player")
        self._ai = AI("enemy")
        self._is_player_turn = random.choice([True, False])

    def _change_turn(self) -> None:
        self._is_player_turn = not self._is_player_turn

    def _setup_board(self) -> None:
        ships = get_ships()

        print("Place your ships.")

        # --- Ship placement ---
        for ship_name, ship_data in ships.items():
            ship_length = ship_data["length"]
            is_ship_placed: bool = False

            print(f"\nShip: {ship_name}\nLength: {ship_length}")

            while not is_ship_placed:

                # --- Player ---
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

                # --- AI ---
                self._ai.place_ship(ship_name)

                print_boards(self._player.board.get_board(), self._ai.board.get_board())

                is_ship_placed = True

        # --- Shooting ---
        while self._player.ships.has_ships() and self._ai.ships.has_ships():
            if self._is_player_turn:
                # --- Player ---
                print("\nYour turn to shoot.")
                
                # --- Player ---
                try:
                    shoot_input_coord = input(f"\nEnter coordinate to shoot: ")
                    shoot_coord = parse_coord(shoot_input_coord)

                    if self._ai.board.get_board()[get_row_index(shoot_coord[0])][get_column_index(shoot_coord[1])]["is_shot"]:
                        raise ValueError(f"You have already shot at `{shoot_coord[0]} {shoot_coord[1]}`. Try again.")
                except ValueError as e:
                    print(e)
                    continue

                self._player.shoot_player(self._ai, shoot_coord)
            else:
                # --- AI ---
                print("\nEnemy's turn to shoot.")
                
                self._ai.shoot_player(self._player)

            print_boards(self._player.board.get_board(), self._ai.board.get_board())
            
            self._change_turn()

        # --- Declare winner ---
        if self._player.ships.has_ships():
            print("\nCongratulations! You have won the game!")
        else:
            print("\nYou have lost the game. Better luck next time!")

    def start(self) -> None:
        self._setup_board()