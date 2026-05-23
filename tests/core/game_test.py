from __future__ import annotations
from typing import Any
from src.utils.app_types import EAIDifficulty
from src.core.game import Game
from src.database.match import get_matches_by_player_id
from src.database.player import get_player_by_name
from tests.helpers import run_case


def _place_all_ships(game: Game) -> None:
    """Place all five ships via the game API using valid non-overlapping horizontal positions."""
    placements = [
        (("a", "1"), ("a", "5")),  # Carrier: 5 cells
        (("b", "1"), ("b", "4")),  # Battleship: 4 cells
        (("c", "1"), ("c", "3")),  # Cruiser: 3 cells
        (("d", "1"), ("d", "3")),  # Submarine: 3 cells
        (("e", "1"), ("e", "2")),  # Destroyer: 2 cells
    ]
    for start, end in placements:
        game.place_player_ship(start, end)


def test_tc_013_player_win_is_persisted_correctly(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_013",
        "title": "game.finish() after a player win persists a match record with has_player_won=True",
        "preconditions": "In-memory database is active. All five ships are placed for both sides.",
        "steps": [
            "Create Game for 'Niels' with BABY difficulty.",
            "Place all five ships for player and AI via game API.",
            "Remove all AI ships to simulate the player sinking them.",
            "Assert game.has_player_won is True.",
            "Call game.finish().",
            "Query get_matches_by_player_id for 'Niels'.",
            "Assert one match exists with has_player_won=True and ai_difficulty='baby'.",
        ],
        "test_data_input": {"player_name": "Niels", "ai_difficulty": "EAIDifficulty.BABY"},
        "expected_result": "One match record with has_player_won=True and ai_difficulty='baby'.",
    }

    def validate() -> str:
        game = Game("Niels", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game)
        for ship_name in list(game._ai.ships.get_ships()):
            game._ai.ships.remove_ship(ship_name)
        assert game.has_player_won is True
        game.finish()
        player = get_player_by_name("Niels")
        assert player is not None
        matches = get_matches_by_player_id(player.id)
        assert len(matches) == 1
        assert matches[0].has_player_won is True
        assert matches[0].ai_difficulty == EAIDifficulty.BABY.value
        return f"Recorded match count: {len(matches)}, has_player_won={matches[0].has_player_won}"

    run_case(case, validate, case_results)


def test_tc_014_player_loss_is_persisted_correctly(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_014",
        "title": "game.finish() after an AI win persists a match record with has_player_won=False",
        "preconditions": "In-memory database is active. All five ships are placed for both sides.",
        "steps": [
            "Create Game for 'Alex' with BABY difficulty.",
            "Place all five ships for player and AI via game API.",
            "Remove all player ships to simulate the AI sinking them.",
            "Assert game.has_player_won is False.",
            "Call game.finish().",
            "Query get_matches_by_player_id for 'Alex'.",
            "Assert one match exists with has_player_won=False.",
        ],
        "test_data_input": {"player_name": "Alex", "ai_difficulty": "EAIDifficulty.BABY"},
        "expected_result": "One match record with has_player_won=False.",
    }

    def validate() -> str:
        game = Game("Alex", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game)
        for ship_name in list(game._player.ships.get_ships()):
            game._player.ships.remove_ship(ship_name)
        assert game.has_player_won is False
        game.finish()
        player = get_player_by_name("Alex")
        assert player is not None
        matches = get_matches_by_player_id(player.id)
        assert len(matches) == 1
        assert matches[0].has_player_won is False
        return f"Recorded match count: {len(matches)}, has_player_won={matches[0].has_player_won}"

    run_case(case, validate, case_results)


def test_tc_015_two_games_produce_two_match_records(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_015",
        "title": "Two completed games for the same player produce two distinct match records",
        "preconditions": "In-memory database is active.",
        "steps": [
            "Create and finish a first Game for 'Héloïse' ending in a player win.",
            "Create and finish a second Game for 'Héloïse' ending in a player loss.",
            "Query get_matches_by_player_id for 'Héloïse'.",
            "Assert two match records exist with opposite has_player_won values.",
        ],
        "test_data_input": {
            "player_name": "Héloïse",
            "game_1_outcome": "win",
            "game_2_outcome": "loss",
        },
        "expected_result": "Two match records: one with has_player_won=True, one with has_player_won=False.",
    }

    def validate() -> str:
        game1 = Game("Héloïse", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game1)
        for ship_name in list(game1._ai.ships.get_ships()):
            game1._ai.ships.remove_ship(ship_name)
        game1.finish()

        game2 = Game("Héloïse", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game2)
        for ship_name in list(game2._player.ships.get_ships()):
            game2._player.ships.remove_ship(ship_name)
        game2.finish()

        player = get_player_by_name("Héloïse")
        assert player is not None
        matches = get_matches_by_player_id(player.id)
        assert len(matches) == 2
        outcomes = {m.has_player_won for m in matches}
        assert outcomes == {True, False}
        return f"Recorded matches outcomes: {outcomes}"

    run_case(case, validate, case_results)


def test_tc_021_number_of_rounds_increments_after_full_round(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_021",
        "title": "number_of_rounds increments by 1 only after both players have taken a shot",
        "preconditions": "All ships placed. Player is set to move first.",
        "steps": [
            "Create Game for 'Niels' with BABY difficulty and place all ships.",
            "Pin player as the starting player.",
            "Assert number_of_rounds is 1.",
            "Call player_shoot — assert number_of_rounds is still 1.",
            "Call ai_shoot — assert number_of_rounds is now 2.",
        ],
        "test_data_input": {"player_name": "Niels", "ai_difficulty": "EAIDifficulty.BABY"},
        "expected_result": "number_of_rounds equals 2 after one complete player + AI round.",
    }

    def validate() -> str:
        game = Game("Niels", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game)
        game._does_player_start = True
        game._is_player_turn = True

        assert game.number_of_rounds == 1

        game.player_shoot(("j", "10"))
        assert game.number_of_rounds == 1

        game.ai_shoot()
        assert game.number_of_rounds == 2
        return f"number_of_rounds after full round: {game.number_of_rounds}"

    run_case(case, validate, case_results)


def test_tc_022_is_game_over_is_true_after_all_player_ships_removed(in_memory_db, case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_022",
        "title": "is_game_over is True once all player ships have been removed",
        "preconditions": "All ships placed for both sides.",
        "steps": [
            "Create Game for 'Niels' with BABY difficulty and place all ships.",
            "Assert is_game_over is False.",
            "Remove all player ships to simulate the AI sinking them.",
            "Assert is_game_over is True.",
        ],
        "test_data_input": {"player_name": "Niels", "ai_difficulty": "EAIDifficulty.BABY"},
        "expected_result": "is_game_over is False before, True after all player ships are removed.",
    }

    def validate() -> str:
        game = Game("Niels", ai_difficulty=EAIDifficulty.BABY)
        _place_all_ships(game)

        assert game.is_game_over is False

        for ship_name in list(game._player.ships.get_ships()):
            game._player.ships.remove_ship(ship_name)

        assert game.is_game_over is True
        return f"is_game_over after removing player ships: {game.is_game_over}"

    run_case(case, validate, case_results)
