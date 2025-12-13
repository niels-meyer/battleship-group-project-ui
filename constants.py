from enum import Enum
from types import SimpleNamespace

MENU_MESSAGE = "                    /\\_/\\ \n                     ( o.o )\n                      > ^ < \n     ______________________________________________________\n    /   ~  ~  ~  ~  ~  ~  BATTLESHIP  ~  ~  ~  ~  ~  ~    |=====[]>\n __/______________________________________________________|______\n<_______________________________________________________________/\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
STATS_MESSAGE = "     /\\_/\\  \n      ( o.o ) \n       > ^ <  \n  +--------------------+\n  |       STATS        |\n  +--------------------+"
STATS_MESSAGE_NEW = STATS_MESSAGE + "\nNo stats available. Please create a profile first or load the data from a file."

# RULES section with cat
RULES_MESSAGE = "     /\\_/\\  \n      ( o.o ) \n       > ^ <  \n  +--------------------+\n  |       RULES        |\n  +--------------------+"

# AFTER HE LEFT THE GAME section with cat
END_MESSAGE = "       /\\_/\\  \n      ( o.- )  \n       > ^ <  \n      Goodbye!"

RULES_MESSAGE = "Back to Main Menu"
STATS_VIEW_MESSAGE = "Back to Stats Menu"


STATS_PRINTE_MESSAGE= SimpleNamespace(
    usernNameInput= "Enter your username: ",
    successSaveMessage= "Stats saved successfully.",
    successLoadMessage= "Stats successfully loaded from file.",
    successCreateMessage= "Profile created successfully.",
    fileNameInput= "Enter the filename to load from (including path): ",
)
    

# Menu choices as constants
MAIN_MENU_CHOICES = SimpleNamespace(
    start= "Start Game",
    stats= "Stats",
    rules= "Rules",
    exit= "Exit"
)

STATS_MENU_CHOICES_NEW = SimpleNamespace(
    create= "Create New Profile",
    load= "Load from File",
    back= "Back to Main Menu"
)

STATS_MENU_CHOICES = SimpleNamespace(
    view= "View Stats",
    save= "Save Stats",
    load= "Load Stats from File",
    back= "Back to Main Menu"
)

STATS_MENU_CHOICES_VIEW = SimpleNamespace(
    back= "Press Enter"
)

RULES_MENU_CHOICES = SimpleNamespace(
    back= "Press Enter"
)


class PlayerType(Enum):
    HUMAN = "human"
    AI = "ai"
