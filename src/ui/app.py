from pathlib import Path
from nicegui import app, ui
from src.ui.pages.game_page import game_page
from src.ui.pages.help_page import help_page
from src.ui.pages.main_menu_page import main_menu_page
from src.ui.pages.player_selector_page import player_selector_page
from src.ui.pages.stats_page import stats_page
from src.ui.constants import APP_TITLE, DEV_STORAGE_SECRET
from src.ui.styles import GLOBAL_CSS, PRIMARY_COLOR

app.add_media_files("/assets", str(Path(__file__).parent.parent / "assets"))

def run_app() -> None:
    app.colors(primary=PRIMARY_COLOR)
    ui.add_head_html(GLOBAL_CSS, shared=True)

    ui.run(
        title=APP_TITLE,
        reload=False,
        storage_secret=DEV_STORAGE_SECRET,
    )