from InquirerPy import inquirer
from config import config
from utils.constants import MAIN_MENU_CHOICES, CONFIG_MENU_CHOICES, STATS_MENU_CHOICES, MENU_MESSAGE, STATS_MENU_CHOICES_NEW, STATS_MENU_CHOICES_VIEW, STATS_MESSAGE, STATS_TITLE_ART, CONFIG_MESSAGE, END_MESSAGE, STATS_PRINT_MESSAGE, STATS_VIEW_MESSAGE
from core.game import Game
from utils.helper import clear_screen

def main_menu():
    clear_screen()
    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=[MAIN_MENU_CHOICES.start, MAIN_MENU_CHOICES.stats, MAIN_MENU_CHOICES.config, MAIN_MENU_CHOICES.exit],
    ).execute()
    match selection:
        case MAIN_MENU_CHOICES.start:
            game_menu()
        case MAIN_MENU_CHOICES.stats:
            stats_menu()
        case MAIN_MENU_CHOICES.config:
            config_menu()
        case MAIN_MENU_CHOICES.exit:
            exit_menu()

def exit_menu():
    clear_screen()
    print(END_MESSAGE)
    quit()

def game_menu():
    clear_screen()
    Game().start()
    main_menu()

def stats_menu():
    pass
    # clear_screen()

def config_menu():
    clear_screen()
    print(create_config())
    selection = inquirer.select(
    choices=[CONFIG_MENU_CHOICES.back],
    message=CONFIG_MESSAGE,
    ).execute()
    match selection:
        case CONFIG_MENU_CHOICES.back:
            main_menu()

def create_config():
    config_lines = [
    "Welcome to Battleship against AI!",
    f"Board: {len(config.get_rows())}x{len(config.get_columns())}",
    f"Rows: {', '.join(config.get_rows())}",
    f"Columns: {', '.join(config.get_columns())}",
    "Ships:"
    ]

    for ship, info in config.get_ships().items():
        config_lines.append(f"- {ship}: {info['length']} cells")

    content_width = max(len(line) for line in config_lines)
    box_width = content_width + 2  # padding inside box

    CONFIG_MESSAGE = "       /\\_/\\  \n      ( o.o ) \n       > ^ <  \n"
    CONFIG_MESSAGE += "  +" + "-" * box_width + "+\n"
    CONFIG_MESSAGE += "  |" + "CONFIG".center(box_width) + "|\n"

    CONFIG_MESSAGE += "  +" + "-"*box_width + "+\n"
    for line in config_lines:
        CONFIG_MESSAGE += "  |" + line.ljust(box_width) + "|\n"

    CONFIG_MESSAGE += "  +" + "-"*box_width + "+"
    return CONFIG_MESSAGE