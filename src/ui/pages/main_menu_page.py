from typing import Any
from nicegui import ui
from src.ui.constants import GAME_ROUTE, HELP_ROUTE, MENU_ROUTE, STATS_ROUTE
from src.ui.pages.helpers.access_control import logout, require_current_player
from src.ui.pages.helpers.navigation import redirect_to_root
from src.ui.styles import BACKGROUND_CSS, BUTTON_COLUMN_CLASS, CARD_COMPACT_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

# Text Constants
WELCOME_TEMPLATE = "Welcome, {player_name}"
START_GAME_LABEL = "Start Game"
STATS_LABEL = "Stats"
HELP_LABEL = "Help"
LOGOUT_LABEL = "Logout"

# Style Constants
CARD_CLASS = CARD_COMPACT_CLASS

@ui.page(MENU_ROUTE)
def main_menu_page() -> Any:
    ui.add_css(BACKGROUND_CSS)
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    player_name = player["name"]

    with ui.column().classes(PAGE_CLASS):
        ui.label(WELCOME_TEMPLATE.format(player_name=player_name)).classes(TITLE_CLASS)
        with ui.card().classes(CARD_CLASS):
            with ui.column().classes(BUTTON_COLUMN_CLASS):
                ui.button(START_GAME_LABEL, on_click=lambda: ui.navigate.to(GAME_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button(STATS_LABEL, on_click=lambda: ui.navigate.to(STATS_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button(HELP_LABEL, on_click=lambda: ui.navigate.to(HELP_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button(LOGOUT_LABEL, on_click=logout).classes(FULL_WIDTH_CLASS)
