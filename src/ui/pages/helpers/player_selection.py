"""Player selection and lookup helpers."""

from nicegui import ui
from src.database.player import Player, create_player, get_all_players, get_player_by_name
from src.ai.difficulty import get_default_ai_difficulty
from src.ui.constants import MENU_ROUTE
from src.ui.pages.helpers.storage_session import set_current_player

# Text Constants
PLAYER_NAME_REQUIRED_WARNING = "Please enter a player name."
PLAYER_SESSION_ERROR = "Could not open player session."
PLAYER_CREATED_TEMPLATE = "Created new player \"{player_name}\"."

# Value Constants
NOTIFY_WARNING_TYPE = "warning"
NOTIFY_NEGATIVE_TYPE = "negative"
NOTIFY_POSITIVE_TYPE = "positive"

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
        ui.notify(PLAYER_NAME_REQUIRED_WARNING, type=NOTIFY_WARNING_TYPE)
        return

    player = find_existing_player(normalized_name)
    created_new_player = False

    if player is None:
        player = create_player(normalized_name)
        created_new_player = True

    if player.id is None:
        ui.notify(PLAYER_SESSION_ERROR, type=NOTIFY_NEGATIVE_TYPE)
        return
    
    set_current_player(player.id, player.name, get_default_ai_difficulty())

    if created_new_player:
        ui.notify(PLAYER_CREATED_TEMPLATE.format(player_name=player.name), type=NOTIFY_POSITIVE_TYPE)

    ui.navigate.to(MENU_ROUTE)
