from InquirerPy import inquirer
import config
from constants import MAIN_MENU_CHOICES, CONFIG_MENU_CHOICES, STATS_MENU_CHOICES, MENU_MESSAGE, STATS_MENU_CHOICES_NEW, STATS_MENU_CHOICES_VIEW, STATS_MESSAGE, STATS_TITLE_ART, CONFIG_MESSAGE, END_MESSAGE, STATS_PRINT_MESSAGE, STATS_VIEW_MESSAGE
from stats import Stats
from game import Game
from utils import clear_screen

def main_menu():
    clear_screen()
    stats = Stats()
    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=[MAIN_MENU_CHOICES.start, MAIN_MENU_CHOICES.stats, MAIN_MENU_CHOICES.config, MAIN_MENU_CHOICES.exit],
    ).execute()
    match selection:
        case MAIN_MENU_CHOICES.start:
            game_menu()
        case MAIN_MENU_CHOICES.stats:
            stats_menu(stats)
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

def stats_menu(stats):
    clear_screen()
    if (stats.name is None):
        selection = inquirer.select(
        message=STATS_MESSAGE,
        choices=[STATS_MENU_CHOICES_NEW.create, STATS_MENU_CHOICES_NEW.load, STATS_MENU_CHOICES_NEW.back],
        ).execute()
        match selection:
            case STATS_MENU_CHOICES_NEW.create:
                print(STATS_PRINT_MESSAGE.usernNameInput)
                username = str(input())
                stats.create_new(username)
                stats.save_to_file()
                stats_menu(stats)
            case STATS_MENU_CHOICES_NEW.load:
                print(STATS_PRINT_MESSAGE.fileNameInput)
                filename = str(input())
                stats.load_from_file(filename)
                stats_menu(stats)
            case STATS_MENU_CHOICES_NEW.back:
                main_menu()

    selection = inquirer.select(
    message=STATS_TITLE_ART,
    choices=[STATS_MENU_CHOICES.view, STATS_MENU_CHOICES.save, STATS_MENU_CHOICES.load, STATS_MENU_CHOICES.back],
    ).execute()
    match selection:
        case STATS_MENU_CHOICES.view:
            stats.print_stats()
            selection = inquirer.select(
            choices=[STATS_MENU_CHOICES_VIEW.back],
            message=STATS_VIEW_MESSAGE,
            ).execute()
            match selection:
                case STATS_MENU_CHOICES_VIEW.back:
                    stats_menu(stats)
        case STATS_MENU_CHOICES.save:
            stats.save_to_file()
            print(STATS_PRINT_MESSAGE.successSaveMessage)
            stats_menu(stats)
        case STATS_MENU_CHOICES.load:
            print(STATS_PRINT_MESSAGE.fileNameInput)
            filename = str(input())
            stats.load_from_file(filename)
            print(STATS_PRINT_MESSAGE.successLoadMessage)
            stats_menu(stats)
        case STATS_MENU_CHOICES.back:
            main_menu()

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