from __future__ import annotations
from typing import Any
from src.database.player import create_player, get_all_players, get_player_by_name, register_player
from tests.helpers import run_case


def test_tc_010_create_player_persists_and_is_retrievable(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_010",
        "title": "create_player persists a player that is retrievable by name",
        "preconditions": "Empty in-memory database with Player and Match tables created.",
        "steps": [
            "Call create_player with name 'Niels'.",
            "Call get_player_by_name('Niels').",
            "Assert the returned player has the correct name and a non-None integer id.",
        ],
        "test_data_input": {"name": "Niels"},
        "expected_result": "get_player_by_name returns a player with name 'Niels' and an assigned integer id.",
    }

    def validate() -> str:
        create_player("Niels")
        found = get_player_by_name("Niels")
        assert found is not None
        assert found.name == "Niels"
        assert isinstance(found.id, int)
        return f"Found player {found.name} with id {found.id}"
    run_case(case, validate, case_results)


def test_tc_019_get_all_players_returns_alphabetical_order(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_019",
        "title": "get_all_players returns all players sorted alphabetically by name",
        "preconditions": "Empty in-memory database with three players created in non-alphabetical order.",
        "steps": [
            "Call create_player for 'Zara', 'Alex', and 'Niels'.",
            "Call get_all_players().",
            "Assert the returned names are in alphabetical order.",
        ],
        "test_data_input": {"names": ["Zara", "Alex", "Niels"]},
        "expected_result": "Players returned in order: Alex, Niels, Zara.",
    }

    def validate() -> str:
        create_player("Zara")
        create_player("Alex")
        create_player("Niels")
        players = get_all_players()
        names = [p.name for p in players]
        assert names == ["Alex", "Niels", "Zara"]
        return f"get_all_players() returned {names}"
    run_case(case, validate, case_results)


def test_tc_020_register_player_duplicate_name_returns_failure(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_020",
        "title": "register_player with a duplicate name returns failure and creates no second player",
        "preconditions": "A player named 'Niels' already exists in the database.",
        "steps": [
            "Call register_player('Niels') to create the first player.",
            "Call register_player('Niels') a second time.",
            "Assert success is False, returned player is None.",
            "Assert only one player exists in the database.",
        ],
        "test_data_input": {"name": "Niels"},
        "expected_result": "Second call returns (False, None, <error message>) and the DB still has one player.",
    }

    def validate() -> str:
        register_player("Niels")
        success, player, message = register_player("Niels")
        assert success is False
        assert player is None
        assert len(get_all_players()) == 1
        return f"Second register_player returned (success={success}, player={player}, message={message})"
    run_case(case, validate, case_results)
