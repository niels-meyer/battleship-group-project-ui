from types import SimpleNamespace

MENU_MESSAGE = "                    /\\_/\\ \n                     ( o.o )\n                      > ^ < \n     ______________________________________________________\n    /   ~  ~  ~  ~  ~  ~  BATTLESHIP  ~  ~  ~  ~  ~  ~    |=====[]>\n __/______________________________________________________|______\n<_______________________________________________________________/\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# AFTER HE LEFT THE GAME section with cat
END_MESSAGE = "       /\\_/\\  \n      ( o.- )  \n       > ^ <  \n      Goodbye!"

CONFIG_MESSAGE = "Back to Main Menu"

# Menu choices as constants
MAIN_MENU_CHOICES = SimpleNamespace(
    start= "Start Game",
    stats= "Stats",
    config= "Config",
    exit= "Exit"
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