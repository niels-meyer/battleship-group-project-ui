from typing import Any
from nicegui import ui
from src.ui.constants import GAME_ROUTE, HELP_ROUTE, MENU_ROUTE, STATS_ROUTE
from src.ui.pages.helpers import logout, redirect_to_root, require_current_player
from src.ui.styles import BUTTON_COLUMN_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

MENU_CARD_CLASS = "w-full max-w-xl q-pa-lg"
MENU_HEADING_CLASS = "text-h6"

@ui.page(MENU_ROUTE)
def main_menu_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    player_name = player["name"]

    with ui.column().classes(PAGE_CLASS):
        ui.label(f"Welcome, {player_name}").classes(TITLE_CLASS)
        with ui.card().classes(MENU_CARD_CLASS):
            ui.label("Main Menu").classes(MENU_HEADING_CLASS)
            with ui.column().classes(BUTTON_COLUMN_CLASS):
                ui.button("Start Game", on_click=lambda: ui.navigate.to(GAME_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button("Stats", on_click=lambda: ui.navigate.to(STATS_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button("Help", on_click=lambda: ui.navigate.to(HELP_ROUTE)).classes(FULL_WIDTH_CLASS)
                ui.button("Logout", on_click=logout).classes(FULL_WIDTH_CLASS)
