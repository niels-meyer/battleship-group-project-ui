from typing import Any
from nicegui import ui
from src.ui.constants import ROOT_ROUTE
from src.ui.pages.helpers import get_current_player, get_player_name_options, redirect_to_menu, select_or_create_player
from src.ui.styles import CARD_MEDIUM_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS

SELECTOR_TITLE_CLASS = "text-h3 text-weight-bold"
SELECTOR_HEADING_CLASS = "text-h6"
SELECT_INPUT_PROPS = "use-input fill-input hide-selected input-debounce=0 new-value-mode=add-unique clearable"

@ui.page(ROOT_ROUTE)
def player_selector_page() -> Any:
    player = get_current_player()
    if player is not None:
        return redirect_to_menu()

    player_name_options = get_player_name_options()

    with ui.column().classes(PAGE_CLASS):
        ui.label("Battleship").classes(SELECTOR_TITLE_CLASS)
        with ui.card().classes(CARD_MEDIUM_CLASS):
            ui.label("Select or create player").classes(SELECTOR_HEADING_CLASS)
            ui.label("Start typing to find an existing player. Use a new name to create one.")
            player_select = ui.select(
                options=player_name_options,
                label="Player name",
                with_input=True,
            ).props(SELECT_INPUT_PROPS).classes(FULL_WIDTH_CLASS)
            ui.button(
                "Continue",
                on_click=lambda: select_or_create_player(player_select.value),
            ).classes(FULL_WIDTH_CLASS)
