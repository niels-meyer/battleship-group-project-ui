from src.app_types import EAIDifficulty

AI_DIFFICULTY_RANKS = {
    EAIDifficulty.BABY: 1,
    EAIDifficulty.EASY: 3,
    EAIDifficulty.NORMAL: 5,
    EAIDifficulty.HARD: 8,
    EAIDifficulty.IMPOSSIBLE: 10,
}

AI_DIFFICULTY_DESCRIPTIONS = {
    EAIDifficulty.BABY: "Slow, forgiving opponent for first games.",
    EAIDifficulty.EASY: "Mostly random shots with occasional smart guesses.",
    EAIDifficulty.NORMAL: "Balanced opponent with hunt and destroy behavior.",
    EAIDifficulty.HARD: "Consistent tactical targeting with fewer mistakes.",
    EAIDifficulty.IMPOSSIBLE: "Maximum pressure with perfect ship-finding behavior.",
}


def get_available_ai_difficulties() -> list[EAIDifficulty]:
    return list(EAIDifficulty)


def get_default_ai_difficulty() -> EAIDifficulty:
    return EAIDifficulty.BABY


def parse_ai_difficulty(value: str | None) -> EAIDifficulty:
    try:
        return EAIDifficulty(value or get_default_ai_difficulty().value)
    except ValueError:
        return get_default_ai_difficulty()


def get_ai_difficulty_label(difficulty: EAIDifficulty) -> str:
    return difficulty.name.title()


def get_ai_difficulty_rank(difficulty: EAIDifficulty) -> int:
    return AI_DIFFICULTY_RANKS[difficulty]


def get_ai_difficulty_description(difficulty: EAIDifficulty) -> str:
    return AI_DIFFICULTY_DESCRIPTIONS[difficulty]


def get_ai_difficulty_summary(difficulty: EAIDifficulty) -> str:
    return f"{get_ai_difficulty_label(difficulty)} ({get_ai_difficulty_rank(difficulty)}/10)"