from __future__ import annotations
from src.core.board import Board


def test_tc_018_shoot_ship_returns_name_on_hit_none_on_miss_and_marks_cell_shot() -> None:
    board = Board()
    board.add_ship("Carrier", [("a", "1")])

    hit_result = board.shoot_ship(("a", "1"))
    miss_result = board.shoot_ship(("b", "1"))

    assert hit_result == "Carrier"
    assert miss_result is None
    state = board.get_board()
    assert state[0][0]["is_shot"] is True
    assert state[1][0]["is_shot"] is True
