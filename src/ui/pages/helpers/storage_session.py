"""Session storage management via NiceGUI app.storage.user."""

from nicegui import app
from src.ai.difficulty import get_default_ai_difficulty, parse_ai_difficulty
from src.app_types import EAIDifficulty, TCurrentPlayer
from src.ui.constants import CURRENT_AI_DIFFICULTY_KEY, CURRENT_PLAYER_KEY

# Value Constants
LEGACY_AI_DIFFICULTY_KEY = "ai_difficulty"


def _build_current_player(player_id: int, player_name: str, ai_difficulty: EAIDifficulty) -> TCurrentPlayer:
    return {
        "id": player_id,
        "name": player_name,
        "ai_difficulty": ai_difficulty.value,
    }


def get_current_player() -> TCurrentPlayer | None:
    """Get the currently logged-in player session, or None if no player is active."""
    current_player = app.storage.user.get(CURRENT_PLAYER_KEY)
    if current_player is None:
        return None

    stored_value = current_player.get(CURRENT_AI_DIFFICULTY_KEY) or current_player.get(LEGACY_AI_DIFFICULTY_KEY)
    if not isinstance(stored_value, str):
        stored_value = get_default_ai_difficulty().value

    current_player[CURRENT_AI_DIFFICULTY_KEY] = stored_value
    current_player[LEGACY_AI_DIFFICULTY_KEY] = stored_value
    return current_player


def set_current_player(
    player_id: int,
    player_name: str,
    ai_difficulty: EAIDifficulty | None = None,
) -> None:
    """Set the current player session."""
    resolved_difficulty = ai_difficulty or get_default_ai_difficulty()
    current_player = _build_current_player(player_id, player_name, resolved_difficulty)
    current_player[CURRENT_AI_DIFFICULTY_KEY] = resolved_difficulty.value
    app.storage.user[CURRENT_PLAYER_KEY] = current_player


def set_current_player_ai_difficulty(ai_difficulty: EAIDifficulty) -> None:
    current_player = get_current_player()
    if current_player is None:
        return

    current_player[CURRENT_AI_DIFFICULTY_KEY] = ai_difficulty.value
    current_player[LEGACY_AI_DIFFICULTY_KEY] = ai_difficulty.value
    app.storage.user[CURRENT_PLAYER_KEY] = current_player


def get_current_player_ai_difficulty() -> EAIDifficulty:
    current_player = get_current_player()
    if current_player is None:
        return get_default_ai_difficulty()

    stored_value = current_player.get(CURRENT_AI_DIFFICULTY_KEY) or current_player.get(LEGACY_AI_DIFFICULTY_KEY)
    return parse_ai_difficulty(stored_value if isinstance(stored_value, str) else None)

def clear_current_player() -> None:
    """Clear the current player session."""
    app.storage.user.pop(CURRENT_PLAYER_KEY, None)
