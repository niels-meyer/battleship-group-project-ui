from typing import Any
from nicegui import ui
from src.utils.constants import CELL_SYMBOLS, COLUMNS, ROWS, SHIPS
from src.ui.constants import BACK_LABEL, HELP_ROUTE, MENU_ROUTE
from src.ui.pages.helpers.access_control import require_current_player
from src.ui.pages.helpers.navigation import redirect_to_root
from src.ui.styles import CARD_WIDE_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, SECTION_HEADING_CLASS, TITLE_CLASS

# Text Constants
TITLE = "Help"
OVERVIEW_HEADING = "Overview"
GRID_ROWS = len(ROWS)
GRID_COLS = len(COLUMNS)
OVERVIEW_TEXT = (
    f"This Battleship is a two-player strategy game played on a {GRID_ROWS}×{GRID_COLS} grid "
    f"(rows {ROWS[0].upper()}–{ROWS[-1].upper()}, columns {COLUMNS[0]}–{COLUMNS[-1]}). "
    "You and an AI opponent each secretly place a fleet of ships on your own board, then take turns "
    "calling out coordinates to attack. The first player to sink every enemy ship wins."
)
FLEET_HEADING = "The Fleet"
SHIP_SYMBOL = CELL_SYMBOLS["ship"]
FLEET: list[tuple[str, int]] = [
    (name, data["length"]) for name, data in SHIPS.items()
]
PLACEMENT_HEADING = "Ship Placement"
PLACEMENT_STEPS = (
    "Each ship occupies a consecutive run of cells either horizontally or vertically.",
    "Ships may not overlap or extend beyond the grid boundary.",
    "You choose a starting coordinate and an orientation (horizontal or vertical) for each ship.",
    "The AI places its ships automatically before the game begins.",
)
BATTLE_HEADING = "Battle Phase"
BATTLE_STEPS = (
    "On your turn, choose a coordinate to fire a shot at the opponent's grid.",
    "A Hit is recorded when your shot lands on an enemy ship cell.",
    "A Miss is recorded when your shot lands on open water.",
    "A ship is Sunk when every one of its cells has been hit.",
    "The AI then returns fire on your grid automatically.",
)
WINNING_HEADING = "Winning"
WINNING_TEXT = (
    f"Sink all {len(SHIPS)} of the opponent's ships before they sink yours to win the match. "
    "Results are saved to your stats after each game."
)

# Style Constants
BODY_CLASS = "text-body1"
STEP_CLASS = "text-body1"
SHIP_ROW_CLASS = "w-full items-center gap-4"
LIST_COLUMN_CLASS = "w-full gap-1"

@ui.page(HELP_ROUTE)
def help_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    with ui.column().classes(PAGE_CLASS):
        ui.label(TITLE).classes(TITLE_CLASS)
        with ui.card().classes(CARD_WIDE_CLASS):
            with ui.column().classes("w-full gap-6"):
                _render_overview()
                ui.separator()
                _render_fleet()
                ui.separator()
                _render_placement()
                ui.separator()
                _render_battle()
                ui.separator()
                _render_winning()
                ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)

def _render_overview() -> None:
    ui.label(OVERVIEW_HEADING).classes(SECTION_HEADING_CLASS)
    ui.label(OVERVIEW_TEXT).classes(BODY_CLASS)

def _render_fleet() -> None:
    ui.label(FLEET_HEADING).classes(SECTION_HEADING_CLASS)
    with ui.column().classes(LIST_COLUMN_CLASS):
        for ship_name, length in FLEET:
            with ui.row().classes(SHIP_ROW_CLASS):
                ui.label(ship_name).classes("text-body1 text-weight-medium w-28")
                ui.label(SHIP_SYMBOL * length).classes("text-body1 tracking-widest")
                ui.label(f"{length} cells").classes("text-body2 text-grey")

def _render_placement() -> None:
    ui.label(PLACEMENT_HEADING).classes(SECTION_HEADING_CLASS)
    with ui.column().classes(LIST_COLUMN_CLASS):
        for step in PLACEMENT_STEPS:
            with ui.row().classes("items-start gap-2"):
                ui.label("•").classes(STEP_CLASS)
                ui.label(step).classes(STEP_CLASS)

def _render_battle() -> None:
    ui.label(BATTLE_HEADING).classes(SECTION_HEADING_CLASS)
    with ui.column().classes(LIST_COLUMN_CLASS):
        for step in BATTLE_STEPS:
            with ui.row().classes("items-start gap-2"):
                ui.label("•").classes(STEP_CLASS)
                ui.label(step).classes(STEP_CLASS)

def _render_winning() -> None:
    ui.label(WINNING_HEADING).classes(SECTION_HEADING_CLASS)
    ui.label(WINNING_TEXT).classes(BODY_CLASS)
