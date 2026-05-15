from typing import Any
from nicegui import ui
from src.ui.constants import BACK_LABEL, GAME_ROUTE, MENU_ROUTE
from src.ui.pages.helpers import redirect_to_root, require_current_player
from src.ui.styles import CARD_MEDIUM_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

@ui.page(GAME_ROUTE)
def game_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    player_name = player["name"]

    with ui.column().classes(PAGE_CLASS):
        ui.label("Start Game").classes(TITLE_CLASS)
        with ui.card().classes(CARD_MEDIUM_CLASS):
            ui.label(f"Player: {player_name}")
            ui.label("The full NiceGUI game board flow is currently under implementation.")
            ui.label("CLI interactions are disabled in favor of UI-driven callbacks.")
            ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)
