from enum import Enum

MENU_MESSAGE = "                    /\\_/\\ \n                     ( o.o )\n                      > ^ < \n     ______________________________________________________\n    /   ~  ~  ~  ~  ~  ~  BATTLESHIP  ~  ~  ~  ~  ~  ~    |=====[]>\n __/______________________________________________________|______\n<_______________________________________________________________/\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
STATS_MESSAGE = "     /\\_/\\  \n      ( o.o ) \n       > ^ <  \n  +--------------------+\n  |       STATS        |\n  +--------------------+"

# RULES section with cat
RULES_MESSAGE = "     /\\_/\\  \n      ( o.o ) \n       > ^ <  \n  +--------------------+\n  |       RULES        |\n  +--------------------+"

# AFTER HE LEFT THE GAME section with cat
END_MESSAGE = "       /\\_/\\  \n      ( o.- )  \n       > ^ <  \n      Goodbye!"


MAIN_MENU_CHOICES = {
    "start": "Start Game",
    "stats": "Stats",
    "rules": "Rules",
    "exit": "Exit"
}

STATS_MENU_CHOICES = {
    "view": "View Stats",
    "save": "Save Stats",
    "load": "Load Stats from File",
    "back": "Back to Main Menu"
}

class PlayerType(Enum):
    HUMAN = "human"
    AI = "ai"