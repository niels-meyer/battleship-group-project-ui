from pathlib import Path
from nicegui import app, ui
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

app.add_media_files("/static", str(Path(__file__).parent.parent / "assets"))

def run_app() -> None:
    ui.add_head_html("""
<style>

/* ===== QUASAR PRIMARY COLOR OVERRIDE ===== */

:root {
    --q-primary: #023020;
}

/* ===== BUTTONS ===== */

.q-btn,
.q-btn.bg-primary,
.q-btn--standard,
.q-btn--unelevated,
.q-btn--flat {

    background: #023020 !important;
    color: white !important;
    border: 1px solid #0b5d3b !important;
    border-radius: 10px !important;
}

/* Remove blue focus ring */

.q-btn:before {
    box-shadow: none !important;
}

/* Hover */

.q-btn:hover {
    background: #034d33 !important;
    box-shadow: 0 0 15px rgba(0, 255, 150, 0.35) !important;
}

/* ===== CARDS ===== */

.q-card {
    background: rgba(0, 20, 10, 0.82) !important;
    border: 1px solid rgba(0, 255, 150, 0.15);
    backdrop-filter: blur(6px);
    color: white;
}

/* ===== INPUTS ===== */

.q-field__control {
    background: rgba(0, 20, 10, 0.85) !important;
    color: white !important;
}

/* ===== TEXT ===== */

body,
.q-card,
.q-field,
.q-input,
.q-select,
.q-table {
    color: white !important;
}

</style>
""", shared=True)

    ui.run(
        title=APP_TITLE,
        reload=False,
        storage_secret=DEV_STORAGE_SECRET,
    )