from typing import Any
from nicegui import ui
from src.ui.constants import BACK_LABEL, HELP_ROUTE, MENU_ROUTE
from src.ui.pages.helpers import redirect_to_root, require_current_player
from src.ui.styles import CARD_MEDIUM_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

# Text Constants
HELP_TITLE = "Help"
HELP_INTRO_TEXT = "Battleship is a two-player strategy game played on a 10×10 grid."
HELP_PLACEMENT_TEXT = "Place your five ships on the board by selecting a start cell and then an end cell."
HELP_SHOOTING_TEXT = "Take turns firing at the enemy grid. A hit is marked with □, a miss with x."
HELP_WIN_TEXT = "Win by sinking all five enemy ships before the AI sinks yours."
HELP_BULLET_TEXT = (
    HELP_INTRO_TEXT,
    HELP_PLACEMENT_TEXT,
    HELP_SHOOTING_TEXT,
    HELP_WIN_TEXT,
)

@ui.page(HELP_ROUTE)
def help_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    with ui.column().classes(PAGE_CLASS):
        ui.label(HELP_TITLE).classes(TITLE_CLASS)
        with ui.card().classes(CARD_MEDIUM_CLASS):
            for help_text in HELP_BULLET_TEXT:
                ui.label(help_text)
            ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)
