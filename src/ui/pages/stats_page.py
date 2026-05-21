from typing import Any
from nicegui import ui
from src.database.match import get_matches_by_player_id
from src.ai.difficulty import get_ai_difficulty_rank, get_ai_difficulty_summary, parse_ai_difficulty
from src.ui.constants import BACK_LABEL, MENU_ROUTE, STATS_ROUTE
from src.ui.pages.helpers import redirect_to_root, require_current_player
from src.ui.styles import BACKGROUND_CSS, CARD_WIDE_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS

# Style Constants
CARD_CLASS = CARD_WIDE_CLASS
EMPTY_STATE_CLASS = "text-italic"

# Text Constants
TITLE = "Stats"
TOTAL_MATCHES_TEMPLATE = "Total Matches: {total_matches}"
WINS_TEMPLATE = "Wins: {total_wins}"
LOSSES_TEMPLATE = "Losses: {total_losses}"
WIN_RATE_TEMPLATE = "Win Rate: {win_rate:.1f}%"
AVG_ROUNDS_TEMPLATE = "Average Rounds: {average_rounds:.1f}"
AVG_DIFFICULTY_TEMPLATE = "Average Opponent Difficulty: {average_opponent_difficulty:.1f}/10"
EMPTY_TEXT = "No matches recorded yet."
MATCH_OUTCOME_WIN = "Win"
MATCH_OUTCOME_LOSS = "Lose"

# Value Constants
TABLE_ROW_KEY = "match_number"
MATCH_ID_FALLBACK = -1
TABLE_ALIGN_LEFT = "left"
TABLE_COLUMNS = [
    {"name": "match_number", "label": "Match #", "field": "match_number", "align": TABLE_ALIGN_LEFT},
    {"name": "rounds", "label": "Rounds", "field": "rounds", "align": TABLE_ALIGN_LEFT},
    {"name": "difficulty", "label": "Opponent", "field": "difficulty", "align": TABLE_ALIGN_LEFT},
    {"name": "outcome", "label": "Outcome", "field": "outcome", "align": TABLE_ALIGN_LEFT},
]

@ui.page(STATS_ROUTE)
def stats_page() -> Any:
    ui.add_css(BACKGROUND_CSS)
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    player_matches = get_matches_by_player_id(player["id"])
    total_matches = len(player_matches)
    total_wins = sum(1 for match in player_matches if match.has_player_won)
    total_losses = total_matches - total_wins
    win_rate = (total_wins / total_matches) * 100 if total_matches > 0 else 0.0
    total_difficulty_rank = sum(get_ai_difficulty_rank(parse_ai_difficulty(match.ai_difficulty)) for match in player_matches)
    average_opponent_difficulty = (total_difficulty_rank / total_matches) if total_matches > 0 else 0.0
    average_rounds = (sum(match.number_of_rounds for match in player_matches) / total_matches) if total_matches > 0 else 0.0
    with ui.column().classes(PAGE_CLASS):
        ui.label(TITLE).classes(TITLE_CLASS)

        with ui.card().classes(CARD_CLASS):
            ui.label(TOTAL_MATCHES_TEMPLATE.format(total_matches=total_matches))
            ui.label(WINS_TEMPLATE.format(total_wins=total_wins))
            ui.label(LOSSES_TEMPLATE.format(total_losses=total_losses))
            ui.label(WIN_RATE_TEMPLATE.format(win_rate=win_rate))
            ui.label(AVG_ROUNDS_TEMPLATE.format(average_rounds=average_rounds))
            ui.label(
                AVG_DIFFICULTY_TEMPLATE.format(average_opponent_difficulty=average_opponent_difficulty)
            )
            ui.separator()
            if not player_matches:
                ui.label(EMPTY_TEXT).classes(EMPTY_STATE_CLASS)
            else:
                rows = [
                    {
                        TABLE_ROW_KEY: index,
                        "rounds": match.number_of_rounds,
                        "outcome": MATCH_OUTCOME_WIN if match.has_player_won else MATCH_OUTCOME_LOSS,
                        "difficulty": get_ai_difficulty_summary(parse_ai_difficulty(match.ai_difficulty)),
                    }
                    for index, match in enumerate(
                        sorted(player_matches, key=lambda item: item.id if item.id is not None else MATCH_ID_FALLBACK),
                        start=1,
                    )
                ]
                ui.table(columns=TABLE_COLUMNS, rows=rows, row_key=TABLE_ROW_KEY).classes(FULL_WIDTH_CLASS)

            ui.button(BACK_LABEL, on_click=lambda: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS)
