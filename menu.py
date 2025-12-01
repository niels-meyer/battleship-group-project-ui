
from InquirerPy import inquirer
import config
from constants import MAIN_MENU_CHOICES, RULES_MENU_CHOICES, STATS_MENU_CHOICES, MENU_MESSAGE, STATS_MENU_CHOICES_NEW, STATS_MENU_CHOICES_VIEW, STATS_MESSAGE, RULES_MESSAGE, END_MESSAGE, STATS_MESSAGE_NEW, STATS_PRINTE_MESSAGE, STATS_VIEW_MESSAGE
from stats import Stats
from game import Game

def main_menu():
    stats = Stats()
    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=[MAIN_MENU_CHOICES.start, MAIN_MENU_CHOICES.stats, MAIN_MENU_CHOICES.rules, MAIN_MENU_CHOICES.exit],
    ).execute()
    match selection:
        case MAIN_MENU_CHOICES.start:
            Game().start()
        case MAIN_MENU_CHOICES.stats:
            stats_menu(stats)
        case MAIN_MENU_CHOICES.rules:
            rules_menu()
        case MAIN_MENU_CHOICES.exite:
            print(END_MESSAGE)
            quit()

def stats_menu(stats):

    if (stats.name is None):
        selection = inquirer.select(
        message=STATS_MESSAGE_NEW,
        choices=[STATS_MENU_CHOICES_NEW.create, STATS_MENU_CHOICES_NEW.load, STATS_MENU_CHOICES_NEW.back],
        ).execute()
        match selection:
            case STATS_MENU_CHOICES_NEW.create:
                print(STATS_PRINTE_MESSAGE.usernNameInput)
                username = str(input())
                stats.create_new(username)
                stats.save_to_file()
                stats_menu(stats)
            case STATS_MENU_CHOICES_NEW.load:
                print(STATS_PRINTE_MESSAGE.fileNameInput)
                filename = str(input())
                stats.load_from_file(filename)
                print(STATS_PRINTE_MESSAGE.successLoadMessage)
                stats_menu(stats)
            case STATS_MENU_CHOICES_NEW.back:
                main_menu()

    selection = inquirer.select(
    message=STATS_MESSAGE,
    choices=[STATS_MENU_CHOICES.view, STATS_MENU_CHOICES.save, STATS_MENU_CHOICES.load, STATS_MENU_CHOICES.back],
    ).execute()
    match selection:
        case STATS_MENU_CHOICES.view:
            stats.printe_stats()
            selection = inquirer.select(
            choices=[STATS_MENU_CHOICES_VIEW.back],
            message=STATS_VIEW_MESSAGE,
            ).execute()
            match selection:
                case STATS_MENU_CHOICES_VIEW.back:
                    stats_menu(stats)
        case STATS_MENU_CHOICES.save:
            stats.save_to_file()
            print(STATS_PRINTE_MESSAGE.successSaveMessage)
            stats_menu(stats)
        case STATS_MENU_CHOICES.load:
            print(STATS_PRINTE_MESSAGE.fileNameInput)
            filename = str(input())
            stats.load_from_file(filename)
            print(STATS_PRINTE_MESSAGE.successLoadMessage)
            stats_menu(stats)
        case STATS_MENU_CHOICES.back:
            main_menu()

def rules_menu():
    print(create_rules())
    selection = inquirer.select(
    choices=[RULES_MENU_CHOICES.back],
    message=RULES_MESSAGE,
    ).execute()
    match selection:
        case RULES_MENU_CHOICES.back:
            main_menu()

def create_rules():
    rules_lines = [
    "Welcome to Battleship against AI!",
    f"Board: {len(config.get_rows())}x{len(config.get_columns())}",
    f"Rows: {', '.join(config.get_rows())}",
    f"Columns: {', '.join(config.get_columns())}",
    "Ships:"
    ]

    for ship, info in config.get_ships().items():
        rules_lines.append(f"- {ship}: {info['length']} cells")

    content_width = max(len(line) for line in rules_lines)
    box_width = content_width + 2  # padding inside box

    RULES_MESSAGE = "       /\\_/\\  \n      ( o.o ) \n       > ^ <  \n"

    RULES_MESSAGE += "  +" + "-"*box_width + "+\n"
    for line in rules_lines:
        RULES_MESSAGE += "  |" + line.ljust(box_width) + "|\n"

    RULES_MESSAGE += "  +" + "-"*box_width + "+"
    
    return RULES_MESSAGE

# def mainMenuSelectionHandler():
#     selection = inquirer.select(
#     message=MENU_MESSAGE,
#     choices=list(MAIN_MENU_CHOICES.values()),
#     ).execute()

#     if selection == MAIN_MENU_CHOICES["start"]:
#         print("Exiting the game...")
#     elif selection == MAIN_MENU_CHOICES["stats"]:
#         statsMenuSelectionHandler()
#     elif selection == MAIN_MENU_CHOICES["rules"]:
#         print("Displaying rules...")
#     elif selection == MAIN_MENU_CHOICES["exit"]:
#         print("Exiting the game...")