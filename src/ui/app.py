from nicegui import ui
from src.ui.pages.game_page import game_page
from src.ui.pages.help_page import help_page
from src.ui.pages.main_menu_page import main_menu_page
from src.ui.pages.player_selector_page import player_selector_page
from src.ui.pages.stats_page import stats_page
from src.ui.constants import APP_TITLE

# Value Constants
DEV_STORAGE_SECRET = "dev-secret"

REGISTERED_PAGES = (
    player_selector_page,
    main_menu_page,
    stats_page,
    help_page,
    game_page,
)

def run_app() -> None:
    ui.run(
        title=APP_TITLE,
        reload=False,
        storage_secret=DEV_STORAGE_SECRET,
    )