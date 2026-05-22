from __future__ import annotations
from typing import Any
from src.core.board import Board
from tests.helpers import run_case


def test_tc_018_shoot_ship_returns_name_on_hit_none_on_miss_and_marks_cell_shot(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_018",
        "title": "shoot_ship returns ship name on hit, None on miss, and marks both cells as shot",
        "preconditions": "A board exists with a Carrier placed at coordinate ('a', '1').",
        "steps": [
            "Create a Board instance.",
            "Add a Carrier at coordinate ('a', '1').",
            "Call shoot_ship(('a', '1')) to shoot a ship cell.",
            "Call shoot_ship(('b', '1')) to shoot an empty cell.",
            "Read the board state with get_board().",
            "Assert the hit returns 'Carrier', the miss returns None, and both target cells are marked as shot.",
        ],
        "test_data_input": {
            "ship_name": "Carrier",
            "ship_coordinates": [("a", "1")],
            "hit_coordinate": ("a", "1"),
            "miss_coordinate": ("b", "1"),
        },
        "expected_result": "Hit returns 'Carrier', miss returns None, and both cells have is_shot=True.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        board = Board()
        board.add_ship("Carrier", [("a", "1")])

        hit_result = board.shoot_ship(("a", "1"))
        miss_result = board.shoot_ship(("b", "1"))

        assert hit_result == "Carrier"
        assert miss_result is None
        state = board.get_board()
        assert state[0][0]["is_shot"] is True
        assert state[1][0]["is_shot"] is True

    run_case(case, validate, case_results)
