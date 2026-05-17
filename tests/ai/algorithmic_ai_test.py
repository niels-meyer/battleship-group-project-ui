from __future__ import annotations

from typing import Any, Callable, Dict, Iterable

import pytest

from src.ai.algorithmic_ai import AIStrategy, SimpleBattleshipAI
from src.app_types import EAIDifficulty, TBoard, TCoordIndex

Coord = TCoordIndex


def make_board(
    board_size: int = 10,
    ship_cells: Dict[Coord, str] | None = None,
    shot_cells: Iterable[Coord] | None = None,
) -> TBoard:
    ship_cells = ship_cells or {}
    shot_set = set(shot_cells or [])

    return tuple(
        tuple(
            {
                "is_shot": (row, col) in shot_set,
                "ship": ship_cells.get((row, col)),
            }
            for col in range(board_size)
        )
        for row in range(board_size)
    )


@pytest.fixture
def case_results() -> list[dict[str, Any]]:
    return []


def run_case(case: dict[str, Any], validator: Callable[[], None], case_results: list[dict[str, Any]]) -> None:
    case["actual_result"] = ""
    case["status"] = "fail"
    case.setdefault("comments", "")

    try:
        validator()
        case["actual_result"] = "Observed behavior matched expected result."
        case["status"] = "pass"
    except AssertionError as error:
        case["actual_result"] = f"Assertion failed: {error}"
        case["comments"] = "Defect found: behavior did not match expected result."
        raise
    finally:
        case_results.append(case)

def test_tc_001_impossible_targets_unshot_ship(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_001",
        "title": "Impossible AI selects an unshot ship cell when one exists",
        "preconditions": "Board contains at least one unshot ship cell.",
        "steps": [
            "Create AI with IMPOSSIBLE difficulty.",
            "Provide board containing unshot ship cells.",
            "Call decide_shot(board).",
        ],
        "test_data_input": {
            "difficulty": "IMPOSSIBLE",
            "ship_cells": [(2, 3), (7, 8)],
            "shot_cells": [],
        },
        "expected_result": "Returned coordinate is one of the unshot ship cells.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.IMPOSSIBLE)
    board = make_board(ship_cells={(2, 3): "Destroyer", (7, 8): "Submarine"})

    def validate() -> None:
        shot = ai.decide_shot(board)
        assert shot in {(2, 3), (7, 8)}

    run_case(case, validate, case_results)


def test_tc_002_hard_extends_known_ship_line(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_002",
        "title": "Hard AI extends a horizontal hit group",
        "preconditions": "Board has two adjacent horizontal hits on the same ship.",
        "steps": [
            "Create AI with HARD difficulty.",
            "Provide board with hits at (3,0) and (3,1).",
            "Call decide_shot(board).",
        ],
        "test_data_input": {
            "difficulty": "HARD",
            "ship_cells": [(3, 0), (3, 1), (3, 2)],
            "shot_cells": [(3, 0), (3, 1)],
        },
        "expected_result": "Returned coordinate is (3,2) to continue destroying the ship.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.HARD)
    board = make_board(
        ship_cells={(3, 0): "Cruiser", (3, 1): "Cruiser", (3, 2): "Cruiser"},
        shot_cells=[(3, 0), (3, 1)],
    )

    def validate() -> None:
        shot = ai.decide_shot(board)
        assert shot == (3, 2)

    run_case(case, validate, case_results)


def test_tc_003_normal_never_repeats_shot(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_003",
        "title": "Normal AI never returns an already-shot coordinate",
        "preconditions": "Board contains several previously shot cells.",
        "steps": [
            "Create AI with NORMAL difficulty.",
            "Provide board with existing shot history.",
            "Call decide_shot(board).",
        ],
        "test_data_input": {
            "difficulty": "NORMAL",
            "shot_cells": [(0, 0), (1, 1), (2, 2), (4, 4)],
        },
        "expected_result": "Returned coordinate has not been shot before.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.NORMAL)
    previous_shots = {(0, 0), (1, 1), (2, 2), (4, 4)}
    board = make_board(shot_cells=previous_shots)

    def validate() -> None:
        shot = ai.decide_shot(board)
        assert shot not in previous_shots

    run_case(case, validate, case_results)


def test_tc_004_reset_clears_state(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_004",
        "title": "Reset clears tracked shots and strategy",
        "preconditions": "AI has non-empty shot history and non-default strategy.",
        "steps": [
            "Create AI instance and manually set state.",
            "Call reset().",
            "Inspect AI state fields.",
        ],
        "test_data_input": {
            "initial_last_shots": [(5, 5)],
            "initial_strategy": "DESTROY",
        },
        "expected_result": "Shot history is empty and strategy is SEARCH.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.NORMAL)
    ai.last_shots.add((5, 5))
    ai.current_strategy = AIStrategy.DESTROY

    def validate() -> None:
        ai.reset()
        assert ai.last_shots == set()
        assert ai.current_strategy == AIStrategy.SEARCH

    run_case(case, validate, case_results)


def test_tc_005_find_unsunk_hits_returns_only_shot_ship_cells(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_005",
        "title": "Unsunk hit detection returns only valid shot ship coordinates",
        "preconditions": "Board contains mix of misses, hits, and unshot ship cells.",
        "steps": [
            "Create AI instance.",
            "Call _find_unsunk_hits(board) with mixed board data.",
            "Verify returned coordinates.",
        ],
        "test_data_input": {
            "ship_cells": [(1, 1), (1, 2), (2, 2)],
            "shot_cells": [(1, 1), (0, 0), (9, 9)],
        },
        "expected_result": "Only (1,1) is returned as an unsunk hit.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    ai = SimpleBattleshipAI()
    board = make_board(
        ship_cells={(1, 1): "Destroyer", (1, 2): "Destroyer", (2, 2): "Submarine"},
        shot_cells=[(1, 1), (0, 0), (9, 9)],
    )

    def validate() -> None:
        hits = ai._find_unsunk_hits(board)
        assert hits == [(1, 1)]

    run_case(case, validate, case_results)
