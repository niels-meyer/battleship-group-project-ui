from __future__ import annotations
from typing import Any
from src.ai.difficulty import (
    get_ai_difficulty_rank,
    get_ai_difficulty_summary,
    get_available_ai_difficulties,
    get_default_ai_difficulty,
    parse_ai_difficulty,
)
from src.app_types import EAIDifficulty
from tests.helpers import run_case


def test_tc_006_invalid_difficulty_falls_back_to_default(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_006",
        "title": "Parsing an invalid difficulty string returns the default difficulty",
        "preconditions": "The difficulty module is imported and a default difficulty is defined.",
        "steps": [
            "Call parse_ai_difficulty with an unrecognised string value.",
            "Compare result to get_default_ai_difficulty().",
        ],
        "test_data_input": {"value": "unknown"},
        "expected_result": "Return value equals get_default_ai_difficulty().",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        assert parse_ai_difficulty("unknown") == get_default_ai_difficulty()

    run_case(case, validate, case_results)


def test_tc_007_available_difficulties_match_enum(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_007",
        "title": "get_available_ai_difficulties returns every EAIDifficulty member",
        "preconditions": "EAIDifficulty enum is fully defined.",
        "steps": [
            "Call get_available_ai_difficulties().",
            "Compare result to list(EAIDifficulty).",
        ],
        "test_data_input": {},
        "expected_result": "The returned list equals list(EAIDifficulty) with all five members.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        assert get_available_ai_difficulties() == list(EAIDifficulty)

    run_case(case, validate, case_results)


def test_tc_008_difficulty_ranks_span_one_to_ten(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_008",
        "title": "Difficulty ranks cover the full 1–10 scale",
        "preconditions": "All difficulties are available and each has a defined rank.",
        "steps": [
            "Retrieve ranks for all available difficulties.",
            "Assert minimum rank is 1.",
            "Assert maximum rank is 10.",
        ],
        "test_data_input": {"difficulties": "all EAIDifficulty values"},
        "expected_result": "Minimum rank is 1, maximum rank is 10.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        ranks = [get_ai_difficulty_rank(d) for d in get_available_ai_difficulties()]
        assert min(ranks) == 1
        assert max(ranks) == 10

    run_case(case, validate, case_results)


def test_tc_009_difficulty_summary_format(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_009",
        "title": "get_ai_difficulty_summary returns label and rank string for HARD",
        "preconditions": "HARD difficulty is defined with rank 8.",
        "steps": [
            "Call get_ai_difficulty_summary(EAIDifficulty.HARD).",
            "Assert return value equals 'Hard (8/10)'.",
        ],
        "test_data_input": {"difficulty": "EAIDifficulty.HARD"},
        "expected_result": "Return value is 'Hard (8/10)'.",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    def validate() -> None:
        assert get_ai_difficulty_summary(EAIDifficulty.HARD) == "Hard (8/10)"

    run_case(case, validate, case_results)