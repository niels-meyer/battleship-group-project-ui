from __future__ import annotations
from typing import Any
from src.database.match import create_match, get_matches_by_player_id
from src.database.player import create_player
from tests.helpers import run_case


def test_tc_011_create_match_persists_and_links_to_player(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_011",
        "title": "create_match saves a match record linked to the correct player",
        "preconditions": "A player exists in the in-memory database.",
        "steps": [
            "Create player 'Alex' with create_player.",
            "Call create_match with player id, 10 rounds, has_player_won=True, ai_difficulty='normal'.",
            "Call get_matches_by_player_id with player id.",
            "Assert one match is returned with the expected field values.",
        ],
        "test_data_input": {
            "player_name": "Alex",
            "number_of_rounds": 10,
            "has_player_won": True,
            "ai_difficulty": "normal",
        },
        "expected_result": "One match returned with player_id, rounds=10, won=True, ai_difficulty='normal'.",
    }

    def validate() -> str:
        player = create_player("Alex")
        create_match(
            player_id=player.id,
            number_of_rounds=10,
            has_player_won=True,
            ai_difficulty="normal",
        )
        matches = get_matches_by_player_id(player.id)
        assert len(matches) == 1
        m = matches[0]
        assert m.player_id == player.id
        assert m.number_of_rounds == 10
        assert m.has_player_won is True
        assert m.ai_difficulty == "normal"
        return f"Created match for player {player.id} with rounds={m.number_of_rounds}, won={m.has_player_won}, ai_difficulty={m.ai_difficulty}"
    run_case(case, validate, case_results)


def test_tc_012_no_matches_returns_empty_list(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_012",
        "title": "get_matches_by_player_id returns an empty list for a player with no matches",
        "preconditions": "A player exists in the in-memory database but has played no games.",
        "steps": [
            "Create player 'Héloïse' with create_player.",
            "Call get_matches_by_player_id without creating any matches.",
            "Assert the returned list is empty.",
        ],
        "test_data_input": {"player_name": "Héloïse"},
        "expected_result": "Empty list is returned.",
    }

    def validate() -> str:
        player = create_player("Héloïse")
        matches = get_matches_by_player_id(player.id)
        assert matches == []
        return f"get_matches_by_player_id returned {matches} for player {player.id}"
    run_case(case, validate, case_results)
