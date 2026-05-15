from typing import Any
from nicegui import ui
from database.match import get_matches_by_player_id
from src.ui.constants import BACK_LABEL, MENU_ROUTE, STATS_ROUTE
from src.ui.pages.helpers import redirect_to_root, require_current_player
from src.ui.styles import FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

STATS_CARD_CLASS = "w-full max-w-3xl q-pa-lg"
EMPTY_STATE_CLASS = "text-italic"

@ui.page(STATS_ROUTE)
def stats_page() -> Any:
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    player_name = player["name"]

    player_matches = get_matches_by_player_id(player["id"])
    total_matches = len(player_matches)
    total_wins = sum(1 for match in player_matches if match.has_player_won)
    total_losses = total_matches - total_wins
    win_rate = (total_wins / total_matches) * 100 if total_matches > 0 else 0.0
    with ui.column().classes(PAGE_CLASS):
        ui.label(f"{player_name} Stats").classes(TITLE_CLASS)

        with ui.card().classes(STATS_CARD_CLASS):
            ui.label(f"Total Matches: {total_matches}")
            ui.label(f"Wins: {total_wins}")
            ui.label(f"Losses: {total_losses}")
            ui.label(f"Win Rate: {win_rate:.1f}%")
            ui.separator()
            if not player_matches:
                ui.label("No matches recorded yet.").classes(EMPTY_STATE_CLASS)
            else:
                rows = [
                    {
                        "match_number": index,
                        "rounds": match.number_of_rounds,
                        "outcome": "Win" if match.has_player_won else "Loss",
                    }
                    for index, match in enumerate(
                        sorted(player_matches, key=lambda item: item.id if item.id is not None else -1),
                        start=1,
                    )
                ]
                columns = [
                    {"name": "match_number", "label": "Match #", "field": "match_number", "align": "left"},
                    {"name": "rounds", "label": "Rounds", "field": "rounds", "align": "left"},
                    {"name": "outcome", "label": "Outcome", "field": "outcome", "align": "left"},
                ]
                ui.table(columns=columns, rows=rows, row_key="match_number").classes(FULL_WIDTH_CLASS)

            ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)
