import random
from InquirerPy import inquirer
from config import get_ships
from display import print_boards
from utils import get_column_index, get_row_index, parse_coord, print_empty_line, suggest_ship_end_coords, get_coords_between, clear_screen
from constants import COLOR_BOLD, COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_RESET, COLOR_CYAN
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

        # --- Ship placement ---
        for ship_name, ship_data in ships.items():
            ship_length = ship_data["length"]
            is_ship_placed: bool = False

            clear_screen()
            print(f"{COLOR_BOLD}{COLOR_YELLOW}⚓ Place your ships.{COLOR_RESET}")
            print_empty_line(2)
            print(f"{COLOR_BOLD}Ship: {COLOR_RESET}{ship_name}")
            print(f"{COLOR_BOLD}Length: {COLOR_RESET}{ship_length}")
            print_boards(self._player.board.get_board(), self._ai.board.get_board())

            while not is_ship_placed:
                # --- Player ---
                try:
                    start_input_coord = input(f"Enter start coordinate: ")
                    start_coord = parse_coord(start_input_coord)
                except ValueError as e:
                    print(f"{COLOR_RED}✗ {e}{COLOR_RESET}")
                    print_empty_line()
                    continue

                valid_end_coords = suggest_ship_end_coords(self._player.board, start_coord, ship_length)

                if not len(valid_end_coords):
                    print(f"{COLOR_RED}✗ Ship cannot be placed there, overlaps or out of bounds.{COLOR_RESET}")
                    print_empty_line()
                    continue
                
                end_input_coord = inquirer.select(
                    message="Choose legal end coordinate:",
                    choices=[f"{row} {column}" for row, column in valid_end_coords]+["Back"]
                ).execute()

                if end_input_coord == "Back":
                    print_empty_line()
                    continue

                end_coord = parse_coord(end_input_coord)
                ship_coords = get_coords_between(start_coord, end_coord)

                self._player.place_ship(ship_name, ship_coords)

                # --- AI ---
                self._ai.place_ship(ship_name)

                clear_screen()

                is_ship_placed = True

        # --- Shooting ---
        turn_count = 0
        while self._player.ships.has_ships() and self._ai.ships.has_ships():
            clear_screen()
            turn_count += 1
            round_count = (turn_count + 1) // 2
            print(f"{COLOR_BOLD}{COLOR_YELLOW}⏱ Round {round_count}{COLOR_RESET}")

            if self._is_player_turn:
                # --- Player ---
                print(f"{COLOR_BOLD}{COLOR_YELLOW}⚔ Your turn to shoot.{COLOR_RESET}")
                print_boards(self._player.board.get_board(), self._ai.board.get_board())

                # --- Player ---
                has_not_shot = True
                while has_not_shot:
                    try:
                        shoot_input_coord = input(f"Enter coordinate to shoot: ")
                        shoot_coord = parse_coord(shoot_input_coord)

                        if self._ai.board.get_board()[get_row_index(shoot_coord[0])][get_column_index(shoot_coord[1])]["is_shot"]:
                            raise ValueError(f"You have already shot at `{shoot_coord[0]} {shoot_coord[1]}`. Try again.")
                    except ValueError as e:
                        print(f"{COLOR_RED}✗ {e}{COLOR_RESET}")
                        print_empty_line()
                        continue
                    has_not_shot = False

                self._player.shoot_player(self._ai, shoot_coord)

                print_boards(self._player.board.get_board(), self._ai.board.get_board(), show_legend=False)
            else:
                # --- AI ---
                print(f"{COLOR_BOLD}{COLOR_YELLOW}⚔ Enemy's turn to shoot.{COLOR_RESET}")
                print_empty_line(2)

                self._ai.shoot_player(self._player)

                print_boards(self._player.board.get_board(), self._ai.board.get_board())
            
            self._change_turn()
            
            if self._player.ships.has_ships() and self._ai.ships.has_ships():
                input(f"{COLOR_BOLD}Press Enter to continue...{COLOR_RESET}")

        # --- Declare winner ---
        clear_screen()
        if self._player.ships.has_ships():
            print(f"{COLOR_BOLD}{COLOR_GREEN}")
            print("╔════════════════════════════════════╗")
            print("║  🎉 CONGRATULATIONS! YOU WON! 🎉   ║")
            print("╚════════════════════════════════════╝")
            print(f"{COLOR_RESET}")
        else:
            print(f"{COLOR_BOLD}{COLOR_RED}")
            print("╔═════════════════════════════╗")
            print("║   GAME OVER - YOU LOST! 😢  ║")
            print("║   Better luck next time!    ║")
            print("╚═════════════════════════════╝")
            print(f"{COLOR_RESET}")
        
        input(f"{COLOR_BOLD}Press Enter to return to main menu...{COLOR_RESET}")

    def start(self) -> None:
        self._setup_board()