"""Session storage management via NiceGUI app.storage.user."""

from typing import Any
from nicegui import app
from src.ui.constants import CURRENT_PLAYER_KEY

def get_current_player() -> dict[str, Any] | None:
    """Get the currently logged-in player session, or None if no player is active."""
    return app.storage.user.get(CURRENT_PLAYER_KEY)

def set_current_player(player_id: int, player_name: str) -> None:
    """Set the current player session."""
    app.storage.user[CURRENT_PLAYER_KEY] = {"id": player_id, "name": player_name}

def clear_current_player() -> None:
    """Clear the current player session."""
    app.storage.user.pop(CURRENT_PLAYER_KEY, None)
