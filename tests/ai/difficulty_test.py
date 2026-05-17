from src.ai.difficulty import (
    get_ai_difficulty_rank,
    get_ai_difficulty_summary,
    get_available_ai_difficulties,
    get_default_ai_difficulty,
    parse_ai_difficulty,
)
from src.app_types import EAIDifficulty


def test_parse_ai_difficulty_falls_back_to_default_for_invalid_value() -> None:
    assert parse_ai_difficulty("unknown") == get_default_ai_difficulty()


def test_available_difficulties_include_all_enum_values() -> None:
    assert get_available_ai_difficulties() == list(EAIDifficulty)


def test_difficulty_ranks_span_from_one_to_ten() -> None:
    ranks = [get_ai_difficulty_rank(difficulty) for difficulty in get_available_ai_difficulties()]
    assert min(ranks) == 1
    assert max(ranks) == 10


def test_difficulty_summary_includes_label_and_rank() -> None:
    assert get_ai_difficulty_summary(EAIDifficulty.HARD) == "Hard (8/10)"