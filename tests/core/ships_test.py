from __future__ import annotations
from typing import Any
from src.core.ships import Ships
from tests.helpers import run_case


def test_tc_016_has_ships_is_false_after_last_ship_removed(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_016",
        "title": "has_ships returns False after the last ship is removed",
        "preconditions": "A Ships collection contains one Destroyer occupying two coordinates.",
        "steps": [
            "Create a Ships instance.",
            "Add a Destroyer at coordinates ('a', '1') and ('a', '2').",
            "Remove the Destroyer with remove_ship.",
            "Assert has_ships() returns False.",
        ],
        "test_data_input": {
            "ship_name": "Destroyer",
            "ship_coordinates": [("a", "1"), ("a", "2")],
        },
        "expected_result": "has_ships() returns False after the only ship is removed.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        ships = Ships()
        ships.add_ship("Destroyer", [("a", "1"), ("a", "2")])

        ships.remove_ship("Destroyer")

        assert ships.has_ships() is False

    run_case(case, validate, case_results)


def test_tc_017_decrease_ship_removes_ship_when_last_coord_hit(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_017",
        "title": "decrease_ship removes a ship after its final coordinate is hit",
        "preconditions": "A Ships collection contains one Destroyer occupying two coordinates.",
        "steps": [
            "Create a Ships instance.",
            "Add a Destroyer at coordinates ('a', '1') and ('a', '2').",
            "Call decrease_ship for coordinate ('a', '1').",
            "Call decrease_ship for coordinate ('a', '2').",
            "Assert the Destroyer is removed from get_ships().",
            "Assert has_ships() returns False.",
        ],
        "test_data_input": {
            "ship_name": "Destroyer",
            "ship_coordinates": [("a", "1"), ("a", "2")],
            "hit_coordinates": [("a", "1"), ("a", "2")],
        },
        "expected_result": "Destroyer is no longer stored and has_ships() returns False.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        ships = Ships()
        ships.add_ship("Destroyer", [("a", "1"), ("a", "2")])

        ships.decrease_ship("Destroyer", ("a", "1"))
        ships.decrease_ship("Destroyer", ("a", "2"))

        assert "Destroyer" not in ships.get_ships()
        assert ships.has_ships() is False

    run_case(case, validate, case_results)
