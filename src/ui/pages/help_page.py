from typing import Any
from nicegui import ui
from src.ui.constants import BACK_LABEL, HELP_ROUTE, MENU_ROUTE
from src.ui.pages.helpers import redirect_to_root, require_current_player
from src.ui.styles import CARD_MEDIUM_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

@ui.page(HELP_ROUTE)
def help_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    with ui.column().classes(PAGE_CLASS):
        ui.label("Help").classes(TITLE_CLASS)
        with ui.card().classes(CARD_MEDIUM_CLASS):
            ui.label("Game setup and play are now event-driven through NiceGUI.")
            ui.label("Ship placement and battle boards are being migrated from CLI to full UI screens.")
            ui.label("Use Start Game to enter the in-progress game flow.")
            ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)
