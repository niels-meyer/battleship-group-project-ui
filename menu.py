
from InquirerPy import inquirer
import config
from constants import MENU_MESSAGE, STATS_MESSAGE, RULES_MESSAGE, END_MESSAGE
from stats import Stats
from game import Game

def main_menu():
    stats = Stats()
    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=["Start", "Stats", "Rules", "Exit"],
    ).execute()
    match selection:
        case "Start":
            Game().start()
        case "Stats":
            stats_menu(stats)
        case "Rules":
            rules_menu()
        case "Exit":
            print(END_MESSAGE)
            quit()

def stats_menu(stats):

    if (stats.name is None):
        selection = inquirer.select(
        message=STATS_MESSAGE+"\nNo stats available. Please create a profile first or load the data from a file.",
        choices=["Create New Profile", "Load from File", "Back to Main Menu"],
        ).execute()
        match selection:
            case "Create New Profile":
                print("Enter your username: ")
                username = str(input())
                stats.create_new(username)
                stats.save_to_file()
                stats_menu(stats)
            case "Load from File":
                print("Enter the filename to load from (including path): ")
                filename = str(input())
                stats.load_from_file(filename)
                stats_menu(stats)
            case "Back to Main Menu":
                main_menu()

    selection = inquirer.select(
    message=STATS_MESSAGE,
    choices=["View Stats", "Save Stats", "Load New Stats from File", "Back to Main Menu"],
    ).execute()
    match selection:
        case "View Stats":
            print(f"Name: {stats.name}")
            print(f"Wins: {stats.winNumber}")
            print(f"Losses: {stats.loseNumber}")
            print(f"ELO Score: {stats.eloScore}")
            stats_menu(stats)
        case "Save Stats":
            stats.save_to_file()
            stats_menu()
        case "Load New Stats from File":
            print("Enter the filename to load from (including path): ")
            filename = str(input())
            stats.load_from_file(filename)
            stats_menu(stats)
        case "Back to Main Menu":
            main_menu()

def rules_menu():
    print(create_rules())
    selection = inquirer.select(
    choices=["Back to Main Menu"],
    message="",
    ).execute()
    match selection:
        case "Back to Main Menu":
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