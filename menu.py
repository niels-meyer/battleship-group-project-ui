
from InquirerPy import inquirer
from constants import MENU_MESSAGE
from stats import Stats
from game import Game

def main_menu():
    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=["Start", "Stats", "Rules", "Exit"],
    ).execute()
    match selection:
        case "Start":
            Game().start()
        case "Stats":
            stats_menu()
        case "Rules":
            print("Displaying rules...")
        case "Exit":
            print("Exiting the game...")

def stats_menu():
    stats = Stats()

    if (stats.name is None):
        print("No stats available. Please create a profile first or load the data from a file.")
        selection = inquirer.select(
        message=MENU_MESSAGE,
        choices=["Create New Profile", "Load from File", "Back to Main Menu"],
        ).execute()
        match selection:
            case "Create New Profile":
                print("Enter your username: ")
                username = str(input())
                stats.create_new(username)
                stats.save_to_file()
            case "Load from File":
                print("Enter the filename to load from (including path): ")
                filename = str(input())
                stats.load_from_file(filename)
            case "Back to Main Menu":
                main_menu()

    selection = inquirer.select(
    message=MENU_MESSAGE,
    choices=["View Stats", "Save Stats", "Load New Stats from File", "Back to Main Menu"],
    ).execute()
    match selection:
        case "View Stats":
            print(f"Name: {stats.name}")
            print(f"Wins: {stats.winNumber}")
            print(f"Losses: {stats.loseNumber}")
            print(f"ELO Score: {stats.eloScore}")
            stats_menu()
        case "Save Stats":
            stats.save_to_file()
            stats_menu()
        case "Load New Stats from File":
            print("Enter the filename to load from (including path): ")
            filename = str(input())
            stats.load_from_file(filename)
            stats_menu()
        case "Back to Main Menu":
            main_menu()

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