from typing import Any
from nicegui import ui
from src.ui.constants import APP_TITLE, ROOT_ROUTE
from src.ui.pages.helpers import get_current_player, get_player_name_options, redirect_to_menu, select_or_create_player
from src.ui.styles import CARD_MEDIUM_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, SECTION_HEADING_CLASS, TITLE_CLASS

# Text Constants
PLAYER_SELECTOR_HEADING = "Select or create player"
PLAYER_SELECTOR_HELP_TEXT = "Start typing to find an existing player. Use a new name to create one."
PLAYER_SELECTOR_INPUT_LABEL = "Player name"
CONTINUE_LABEL = "Continue"

# Style Constants
SELECTOR_TITLE_CLASS = TITLE_CLASS
SELECTOR_HEADING_CLASS = SECTION_HEADING_CLASS

# Value Constants
PLAYER_INPUT_PROPS = "clearable"

@ui.page(ROOT_ROUTE)
def player_selector_page() -> Any:
    player = get_current_player()
    if player is not None:
        return redirect_to_menu()

    player_name_options = get_player_name_options()

    def continue_with_player() -> None:
        select_or_create_player(player_input.value)

    with ui.column().classes(PAGE_CLASS):
        ui.label(APP_TITLE).classes(SELECTOR_TITLE_CLASS)
        with ui.card().classes(CARD_MEDIUM_CLASS):
            ui.label(PLAYER_SELECTOR_HEADING).classes(SELECTOR_HEADING_CLASS)
            ui.label(PLAYER_SELECTOR_HELP_TEXT)
            player_input = ui.input(
                label=PLAYER_SELECTOR_INPUT_LABEL,
                autocomplete=player_name_options,
            ).props(PLAYER_INPUT_PROPS).on("keydown.enter", continue_with_player).classes(FULL_WIDTH_CLASS)
            ui.button(
                CONTINUE_LABEL,
                on_click=continue_with_player,
            ).classes(FULL_WIDTH_CLASS)