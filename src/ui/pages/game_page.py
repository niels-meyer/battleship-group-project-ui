from typing import Any, Callable
from nicegui import ui
from src.ai.difficulty import (
    get_ai_difficulty_label,
    get_available_ai_difficulties,
    get_default_ai_difficulty,
    parse_ai_difficulty,
)
from src.app_types import EAIDifficulty, TBoard, TBoardCell, TCoord
from src.constants import CELL_SYMBOLS, COLUMNS, ROWS
from src.core.game import Game
from src.ui.constants import APP_TITLE, BACK_LABEL, GAME_ROUTE, MENU_ROUTE
from src.ui.pages.helpers.access_control import require_current_player
from src.ui.pages.helpers.navigation import redirect_to_root
from src.ui.pages.helpers.storage_session import set_current_player_ai_difficulty
from src.ui.styles import BACKGROUND_CSS, CARD_COMPACT_CLASS, FULL_WIDTH_CLASS, PAGE_CLASS, TITLE_CLASS, GREEN_BUTTON_STYLE, INPUT_SELECT_STYLE

# Style Constants
SETUP_CARD_CLASS = CARD_COMPACT_CLASS
GAME_CARD_CLASS = "w-full max-w-5xl q-pa-lg"
BOARD_CARD_CLASS = "q-pa-md"
BOARD_ROW_CLASS = "w-full justify-evenly items-start"
STATUS_CLASS = "text-subtitle1 text-weight-medium"
HEADING_CLASS = "text-subtitle1 text-weight-medium"
HELPER_TEXT_CLASS = "text-body2"
BOARD_CELL_CLASS = "battle-cell min-w-0"
BOARD_CELL_STYLE = "width: 2rem; height: 2rem; padding: 0;"
BOARD_CELL_GREEN_STYLE = """background-color: #023020 !important; color: #7CFFB2 !important; border: 1px solid #0b5d3b !important; border-radius: 10px !important; box-shadow: inset 0 0 8px rgba(0, 255, 120, 0.18);"""
BOARD_LABEL_STYLE = "width: 1.5rem; text-align: center;"

# Text Constants
CELL_SELECTED = CELL_SYMBOLS["start_coord"]
CELL_HIGHLIGHTED = CELL_SYMBOLS["end_coords"]
CELL_HIT = CELL_SYMBOLS["hit"]
CELL_MISS = CELL_SYMBOLS["miss"]
CELL_SHIP = CELL_SYMBOLS["ship"]
CELL_EMPTY = ""
SHOT_HIT = "Hit"
SHOT_MISS = "Miss"
SHOT_ENEMY_HIT = "hit"
SHOT_ENEMY_MISSED = "missed"
SETUP_TITLE = "Select Opponent"
OPPONENT_LABEL = "Opponent"
START_BTN = "Start Game"
PLAYER_BOARD_TITLE = "Your Board"
ENEMY_BOARD_TITLE = "Enemy Board"
PLACEMENT_FIRST_SHIP = "Place your first ship by choosing a start cell."
PLACEMENT_CLEARED = "Placement selection cleared."
PLACEMENT_INVALID = "That ship position is not valid."
SHOT_WARNING = "That cell was already targeted."
PLACEMENT_HELP = "Place {ship_name} ({ship_length} cells)."
PLACEMENT_HELP_SUB = "Select a start cell, then select one of the marked end cells."
PLACEMENT_STATUS = "Place {ship_name} ({ship_length} cells): choose an end cell from {start_coord}."
PLACED_NEXT = "Placed {placed_ship}. Next: {next_ship} ({next_length} cells)."
PLACED_BATTLE_START = "Placed {placed_ship}. Battle phase is starting."
READY_TO_FIRE = "All ships placed. Your turn to fire."
PLAYER_TURN_PROMPT = "Target the enemy board to fire your next shot."
VICTORY = "Victory"
DEFEAT = "Defeat"
RESULT_TITLE = "Result: {outcome}"
RESULT_ROUNDS = "Rounds played: {rounds}"
RESULT_SAVED = "The match result has been saved to your stats."
PLAYER_WIN = "You fired at {coord}: {result}. You won the battle."
ENEMY_WIN = "You fired at {player_coord}: {player_result}. Enemy fired at {enemy_coord} and {enemy_result}. You lost the battle."
ENEMY_OPENING_WIN = "Enemy fired at {enemy_coord} and {enemy_result}. You lost the battle."
ENEMY_OPENING_TURN = "Enemy fired at {enemy_coord} and {enemy_result}. Your turn."
TURN_RESULT = "You fired at {player_coord}: {player_result}. Enemy fired at {enemy_coord} and {enemy_result}. Your turn."

def _board_grid_style(column_count: int) -> str:
    return (
        "display: grid; "
        f"grid-template-columns: 1.5rem repeat({column_count}, 2rem) 1.5rem; "
        "gap: 0.25rem; align-items: center; width: fit-content; margin: 0;"
    )


def _format_coord(coord: TCoord) -> str:
    return f"{coord[0].upper()}{coord[1]}"


def _cell_text(cell: TBoardCell, *, reveal_ship: bool, is_selected: bool, is_highlighted: bool) -> str:
    if is_selected:
        return CELL_SELECTED
    if is_highlighted:
        return CELL_HIGHLIGHTED
    if cell["is_shot"] and cell["ship"]:
        return CELL_HIT
    if cell["is_shot"]:
        return CELL_MISS
    if reveal_ship and cell["ship"]:
        return CELL_SHIP
    return CELL_EMPTY


class GamePageController:
    def __init__(self, player_name: str, ai_difficulty: EAIDifficulty, rows: list[str], columns: list[str]):
        self.player_name = player_name
        self.ai_difficulty = ai_difficulty
        self.rows = rows
        self.columns = columns
        self.game = Game(player_name, ai_difficulty=ai_difficulty)
        self.selected_start: TCoord | None = None
        self.valid_end_coords: set[TCoord] = set()
        self.status_message = PLACEMENT_FIRST_SHIP
        self.match_saved = False
        self._refresh: Callable[..., Any] | None = None

    def set_refresh(self, refresh: Callable[..., Any]) -> None:
        self._refresh = refresh

    def refresh(self) -> None:
        if self._refresh is not None:
            self._refresh()

    def clear_selection(self) -> None:
        self.selected_start = None
        self.valid_end_coords = set()

    def set_status(self, message: str) -> None:
        self.status_message = message

    def save_match_if_needed(self) -> None:
        if not self.match_saved and self.game.is_game_over:
            self.game.finish()
            self.match_saved = True

    def _shoot_ai(self) -> tuple[str, str]:
        """Execute AI's shot. Returns (formatted coord, hit/miss label)."""
        coord, hit = self.game.ai_shoot()
        return _format_coord(coord), SHOT_ENEMY_HIT if hit else SHOT_ENEMY_MISSED

    def begin_battle_phase(self) -> None:
        self.clear_selection()
        if self.game.is_player_turn:
            self.set_status(READY_TO_FIRE)
            return

        enemy_coord_label, enemy_result = self._shoot_ai()
        if self.game.is_game_over:
            self.save_match_if_needed()
            self.set_status(ENEMY_OPENING_WIN.format(enemy_coord=enemy_coord_label, enemy_result=enemy_result))
            return

        self.set_status(ENEMY_OPENING_TURN.format(enemy_coord=enemy_coord_label, enemy_result=enemy_result))

    def handle_back_to_menu(self) -> None:
        ui.navigate.to(MENU_ROUTE)

    def handle_placement_click(self, coord: TCoord) -> None:
        current_ship = self.game.get_current_ship()
        if current_ship is None:
            return

        valid_end_coords = set(self.game.get_valid_end_coords(coord))
        if self.selected_start is None:
            self._start_ship_selection(coord, current_ship, valid_end_coords)
            return

        if coord == self.selected_start:
            self.clear_selection()
            self.set_status(PLACEMENT_CLEARED)
            self.refresh()
            return

        if coord in self.valid_end_coords:
            self._place_current_ship(coord, current_ship)
            return

        self._start_ship_selection(coord, current_ship, valid_end_coords)

    def _start_ship_selection(
        self,
        coord: TCoord,
        current_ship: tuple[str, int],
        valid_end_coords: set[TCoord],
    ) -> None:
        if not valid_end_coords:
            ui.notify(PLACEMENT_INVALID, type="warning")
            return

        ship_name, ship_length = current_ship
        self.selected_start = coord
        self.valid_end_coords = valid_end_coords
        self.set_status(
            PLACEMENT_STATUS.format(
                ship_name=ship_name,
                ship_length=ship_length,
                start_coord=_format_coord(coord),
            )
        )
        self.refresh()

    def _place_current_ship(self, end_coord: TCoord, current_ship: tuple[str, int]) -> None:
        placed_ship, _ = current_ship
        if self.selected_start is None:
            return
        self.game.place_player_ship(self.selected_start, end_coord)
        self.clear_selection()

        next_ship = self.game.get_current_ship()
        if next_ship is None:
            self.set_status(PLACED_BATTLE_START.format(placed_ship=placed_ship))
            self.begin_battle_phase()
        else:
            next_name, next_length = next_ship
            self.set_status(
                PLACED_NEXT.format(
                    placed_ship=placed_ship,
                    next_ship=next_name,
                    next_length=next_length,
                )
            )
        self.refresh()

    def handle_player_shot(self, coord: TCoord) -> None:
        if self.game.is_game_over or not self.game.is_player_turn:
            return

        if not self.game.is_valid_shot(coord):
            ui.notify(SHOT_WARNING, type="warning")
            return

        player_hit = self.game.player_shoot(coord)
        player_result = SHOT_HIT if player_hit else SHOT_MISS
        player_coord = _format_coord(coord)

        if self.game.is_game_over:
            self.save_match_if_needed()
            self.set_status(PLAYER_WIN.format(coord=player_coord, result=player_result))
            self.refresh()
            return

        enemy_coord_label, enemy_result = self._shoot_ai()
        if self.game.is_game_over:
            self.save_match_if_needed()
            self.set_status(
                ENEMY_WIN.format(
                    player_coord=player_coord,
                    player_result=player_result,
                    enemy_coord=enemy_coord_label,
                    enemy_result=enemy_result,
                )
            )
            self.refresh()
            return

        self.set_status(
            TURN_RESULT.format(
                player_coord=player_coord,
                player_result=player_result,
                enemy_coord=enemy_coord_label,
                enemy_result=enemy_result,
            )
        )
        self.refresh()

    def render_board(
        self,
        *,
        title: str,
        board: TBoard,
        reveal_ship: bool,
        on_cell_click: Callable[[TCoord], None] | None,
        highlighted_coords: set[TCoord] | None = None,
        selected_coord: TCoord | None = None,
    ) -> None:
        highlighted_coords = highlighted_coords or set()
        with ui.card().classes(BOARD_CARD_CLASS):
            ui.label(title).classes(HEADING_CLASS + " w-full text-center")
            with ui.element("div").style(_board_grid_style(len(self.columns))):
                ui.label("")
                for column in self.columns:
                    ui.label(column).style(BOARD_LABEL_STYLE)
                ui.label("")
                for row_index, row in enumerate(self.rows):
                    ui.label(row.upper()).style(BOARD_LABEL_STYLE)
                    for column_index, column in enumerate(self.columns):
                        self._render_board_cell(
                            row=row,
                            column=column,
                            cell=board[row_index][column_index],
                            reveal_ship=reveal_ship,
                            on_cell_click=on_cell_click,
                            highlighted_coords=highlighted_coords,
                            selected_coord=selected_coord,
                        )
                    ui.label(row.upper()).style(BOARD_LABEL_STYLE)
                ui.label("")
                for column in self.columns:
                    ui.label(column).style(BOARD_LABEL_STYLE)
                ui.label("")

    def _render_board_cell(
        self,
        *,
        row: str,
        column: str,
        cell: TBoardCell,
        reveal_ship: bool,
        on_cell_click: Callable[[TCoord], None] | None,
        highlighted_coords: set[TCoord],
        selected_coord: TCoord | None,
    ) -> None:
        coord = (row, column)
        is_clickable = on_cell_click is not None and not cell["is_shot"]
        button = ui.button(
            _cell_text(
                cell,
                reveal_ship=reveal_ship,
                is_selected=coord == selected_coord,
                is_highlighted=coord in highlighted_coords,
            ),
            on_click=(lambda _event, target=coord: on_cell_click(target)) if is_clickable and on_cell_click else None,
        )
        button.classes(BOARD_CELL_CLASS)
        button.style(BOARD_CELL_STYLE + BOARD_CELL_GREEN_STYLE)
        if not is_clickable:
            button.disable()

    def render_status_section(self) -> None:
        ui.label(self.status_message).classes(STATUS_CLASS)
        if not self.game.all_ships_placed:
            self._render_placement_help()
        elif self.game.is_game_over:
            self._render_result_help()
        else:
            ui.label(PLAYER_TURN_PROMPT).classes(HELPER_TEXT_CLASS)
        ui.separator()

    def _render_placement_help(self) -> None:
        current_ship = self.game.get_current_ship()
        if current_ship is None:
            return

        ship_name, ship_length = current_ship
        ui.label(PLACEMENT_HELP.format(ship_name=ship_name, ship_length=ship_length)).classes(HELPER_TEXT_CLASS)
        ui.label(PLACEMENT_HELP_SUB).classes(HELPER_TEXT_CLASS)

    def _render_result_help(self) -> None:
        outcome = VICTORY if self.game.has_player_won else DEFEAT
        ui.label(RESULT_TITLE.format(outcome=outcome)).classes(HEADING_CLASS)
        ui.label(RESULT_ROUNDS.format(rounds=self.game.number_of_rounds)).classes(HELPER_TEXT_CLASS)
        ui.label(RESULT_SAVED).classes(HELPER_TEXT_CLASS)

    def render_boards(self) -> None:
        enemy_board_click = self.handle_player_shot if self.game.all_ships_placed and not self.game.is_game_over and self.game.is_player_turn else None
        with ui.row().classes(BOARD_ROW_CLASS):
            if not self.game.all_ships_placed:
                self.render_board(
                    title=PLAYER_BOARD_TITLE,
                    board=self.game.get_player_board(),
                    reveal_ship=True,
                    on_cell_click=self.handle_placement_click,
                    highlighted_coords=self.valid_end_coords,
                    selected_coord=self.selected_start,
                )
                return
            self.render_board(
                title=PLAYER_BOARD_TITLE,
                board=self.game.get_player_board(),
                reveal_ship=True,
                on_cell_click=None,
            )
            self.render_board(
                title=ENEMY_BOARD_TITLE,
                board=self.game.get_ai_board(),
                reveal_ship=False,
                on_cell_click=enemy_board_click,
            )

    def render_content(self) -> None:
        ui.label(APP_TITLE).classes(TITLE_CLASS)
        with ui.card().classes(GAME_CARD_CLASS):
            with ui.column().classes(FULL_WIDTH_CLASS + " gap-4"):
                self.render_status_section()
                self.render_boards()
                ui.button(BACK_LABEL, on_click=lambda _event: self.handle_back_to_menu()).classes(FULL_WIDTH_CLASS).style(GREEN_BUTTON_STYLE)


@ui.page(GAME_ROUTE)
def game_page() -> Any:
    ui.add_css(BACKGROUND_CSS)
    player = require_current_player()
    if player is None:
        return redirect_to_root()

    selected_difficulty = get_default_ai_difficulty().value
    controller: GamePageController | None = None

    def start_game(difficulty_value: str | None) -> None:
        nonlocal controller
        ai_difficulty = parse_ai_difficulty(difficulty_value)
        set_current_player_ai_difficulty(ai_difficulty)
        controller = GamePageController(player["name"], ai_difficulty, ROWS, COLUMNS)
        controller.set_refresh(content.refresh)
        content.refresh()

    @ui.refreshable
    def content() -> None:
        with ui.column().classes(PAGE_CLASS):
            if controller is None:
                ui.label(APP_TITLE).classes(TITLE_CLASS)
                with ui.card().classes(SETUP_CARD_CLASS):
                    ui.label(SETUP_TITLE).classes(HEADING_CLASS)
                    opponent_options = {
                        difficulty.value: get_ai_difficulty_label(difficulty)
                        for difficulty in get_available_ai_difficulties()
                    }
                    opponent_select = ui.select(
                        options=opponent_options,
                        value=selected_difficulty,
                        label=OPPONENT_LABEL,
                    ).classes(FULL_WIDTH_CLASS).style(INPUT_SELECT_STYLE)
                    ui.button(
                        START_BTN,
                        on_click=lambda _event: start_game(opponent_select.value),
                    ).classes(FULL_WIDTH_CLASS).style(GREEN_BUTTON_STYLE)
                    ui.button(BACK_LABEL, on_click=lambda _event: ui.navigate.to(MENU_ROUTE)).classes(FULL_WIDTH_CLASS).style(GREEN_BUTTON_STYLE)
                return

            controller.render_content()

    content()
