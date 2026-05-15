"""Access control helpers for requiring current player and logout functionality."""

from typing import Any
from nicegui import ui
from src.ui.constants import ROOT_ROUTE
from src.ui.pages.helpers.storage_session import get_current_player, clear_current_player

def require_current_player() -> dict[str, Any] | None:
    """Ensure a player is currently logged in. Returns player dict or None."""
    return get_current_player()

def logout() -> None:
    """Clear the current player session and navigate to root."""
    clear_current_player()
    ui.navigate.to(ROOT_ROUTE)
