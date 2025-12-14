from types import SimpleNamespace

MENU_MESSAGE = "                    /\\_/\\ \n                     ( o.o )\n                      > ^ < \n     ______________________________________________________\n    /   ~  ~  ~  ~  ~  ~  BATTLESHIP  ~  ~  ~  ~  ~  ~    |=====[]>\n __/______________________________________________________|______\n<_______________________________________________________________/\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
STATS_TITLE_ART = "     /\\_/\\  \n      ( o.o ) \n       > ^ <  \n  +--------------------+\n  |       STATS        |\n  +--------------------+"
STATS_MESSAGE = STATS_TITLE_ART + "\nNo stats available. Please create a profile first or load the data from a file."

# AFTER HE LEFT THE GAME section with cat
END_MESSAGE = "       /\\_/\\  \n      ( o.- )  \n       > ^ <  \n      Goodbye!"

CONFIG_MESSAGE = "Back to Main Menu"
STATS_VIEW_MESSAGE = "Back to Stats Menu"


STATS_PRINT_MESSAGE= SimpleNamespace(
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
    config= "Config",
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

CONFIG_MENU_CHOICES = SimpleNamespace(
    back= "Press Enter"
)

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[36m"
COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_BOLD = "\033[1m"