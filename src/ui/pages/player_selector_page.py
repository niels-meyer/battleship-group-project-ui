from typing import Any
from nicegui import ui
from src.ui.constants import APP_TITLE, ROOT_ROUTE
from src.ui.pages.helpers import (
    get_current_player,
    get_player_name_options,
    redirect_to_menu,
    select_or_create_player,
)
from src.ui.styles import (
    CARD_MEDIUM_CLASS,
    FULL_WIDTH_CLASS,
    PAGE_CLASS,
    SECTION_HEADING_CLASS,
    TITLE_CLASS,
)

# Text Constants
INPUT_LABEL = "Player name"
EXISTING_PLAYER_HEADING = "Select existing player"
NEW_PLAYER_HEADING = "Create new player"
CREATE_PLAYER_BUTTON_LABEL = "Create Player"

# Value Constants
PLAYER_INPUT_PROPS = "clearable standout dark"
DIVIDER_CLASS = "w-full"
SECTION_CLASS = "w-full gap-2"

@ui.page(ROOT_ROUTE)
def player_selector_page() -> Any:
    player = get_current_player()
    if player is not None:
        return redirect_to_menu()

    player_name_options = get_player_name_options()

    def continue_with_player() -> None:
        select_or_create_player(new_player_input.value)

    with ui.column().classes(PAGE_CLASS):
        ui.label(APP_TITLE).classes(TITLE_CLASS)

        with ui.card().classes(CARD_MEDIUM_CLASS):

            with ui.column().classes(SECTION_CLASS):
                ui.label(EXISTING_PLAYER_HEADING)
                ui.select(
                    options=player_name_options,
                    label=INPUT_LABEL,
                    on_change=lambda e: select_or_create_player(e.value),
                    with_input=True,
                ).props(
                    PLAYER_INPUT_PROPS
                ).classes(
                    FULL_WIDTH_CLASS
                )

            ui.separator().classes(DIVIDER_CLASS)

            with ui.column().classes(SECTION_CLASS):
                ui.label(NEW_PLAYER_HEADING)
                new_player_input = ui.input(
                    label=INPUT_LABEL,
                ).props(
                    PLAYER_INPUT_PROPS
                ).on(
                    "keydown.enter",
                    continue_with_player,
                ).classes(
                    FULL_WIDTH_CLASS
                )
                ui.button(
                    CREATE_PLAYER_BUTTON_LABEL,
                    on_click=continue_with_player,
                ).classes(
                    FULL_WIDTH_CLASS
                )