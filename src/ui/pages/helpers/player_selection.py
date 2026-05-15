"""Player selection and lookup helpers."""

from nicegui import ui
from database.player import Player, create_player, get_all_players, get_player_by_name
from src.ui.constants import MENU_ROUTE
from src.ui.pages.helpers.storage_session import set_current_player

def normalize_player_name(name: str | None) -> str:
    """Normalize a player name by trimming whitespace."""
    return (name or "").strip()

def get_player_name_options() -> list[str]:
    """Get all existing player names as options."""
    return [player.name for player in get_all_players()]

def find_existing_player(name: str) -> Player | None:
    """Find a player by exact match or case-insensitive match."""
    exact_match = get_player_by_name(name)
    
    if exact_match is not None:
        return exact_match

    for player in get_all_players():
        if player.name.casefold() == name.casefold():
            return player
        
    return None

def select_or_create_player(name: str | None) -> None:
    """Select an existing player or create a new one with validation."""
    normalized_name = normalize_player_name(name)
    if not normalized_name:
        ui.notify("Please enter a player name.", type="warning")
        return

    player = find_existing_player(normalized_name)
    created_new_player = False

    if player is None:
        player = create_player(normalized_name)
        created_new_player = True

    if player.id is None:
        ui.notify("Could not open player session.", type="negative")
        return
    
    set_current_player(player.id, player.name)

    if created_new_player:
        ui.notify(f"Created new player \"{player.name}\".", type="positive")

    ui.navigate.to(MENU_ROUTE)
