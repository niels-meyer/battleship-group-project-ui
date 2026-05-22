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

/* ===== BATTLESHIP CELLS ===== */

.battle-cell {
    background: rgba(0, 70, 40, 0.85) !important;

    border: 1px solid rgba(0, 255, 120, 0.35) !important;

    color: #7CFFB2 !important;

    border-radius: 10px !important;

    transition: all 0.18s ease;

    box-shadow:
        inset 0 0 8px rgba(0, 255, 100, 0.08),
        0 0 4px rgba(0, 255, 100, 0.12);

    backdrop-filter: blur(2px);
}

/* Hover */

.battle-cell:hover {
    background: rgba(0, 110, 60, 0.95) !important;

    box-shadow:
        0 0 12px rgba(0, 255, 120, 0.45),
        inset 0 0 10px rgba(0, 255, 150, 0.2);

    transform: scale(1.05);
}

/* Click */

.battle-cell:active {
    transform: scale(0.96);
}

/* Disabled */

.battle-cell:disabled {
    opacity: 0.9 !important;
}

/* Hit cells */

.battle-hit {
    background: #00ff88 !important;
    color: black !important;
}

/* Miss cells */

.battle-miss {
    background: rgba(20, 40, 30, 0.9) !important;
    color: #8fa39a !important;
}

/* Ship placement */

.battle-ship {
    background: rgba(0, 180, 90, 0.35) !important;
}
/* ===== SELECT / INPUT CONTAINER ===== */

.q-field__control {
    background: transparent !important;
    color: white !important;
}

.q-field__native,
.q-field__input,
.q-field input {
    color: white !important;
    background: transparent !important;
}

.q-field__label {
    color: rgba(255, 255, 255, 0.75) !important;
}

.q-field__append,
.q-field__prepend,
.q-icon {
    color: white !important;
}
/* ===== AUTOCOMPLETE DROPDOWN ===== */

.q-menu {
    background: rgba(2, 48, 32, 0.96) !important;
    border: 1px solid rgba(0,255,120,0.25) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}

/* Items */

.q-item {
    color: white !important;
    background: transparent !important;
}

/* Hover */

.q-item:hover,
.q-item.q-manual-focusable--focused {
    background: rgba(0,255,120,0.14) !important;
}

/* ===== REMOVE WHITE CHIP ===== */

.q-chip {
    background: rgba(2, 48, 32, 0.92) !important;
    color: white !important;

    border: 1px solid rgba(0,255,120,0.22);

    box-shadow: 0 0 8px rgba(0,255,120,0.10);
}

/* X icon */

.q-chip .q-icon {
    color: white !important;
}

.q-menu,
.q-virtual-scroll__content {
    background: rgba(2, 48, 32, 0.96) !important;
    color: white !important;
    border-radius: 12px !important;
}

.q-item {
    background: transparent !important;
    color: white !important;
}

.q-item:hover,
.q-item.q-manual-focusable--focused {
    background: rgba(0, 255, 120, 0.16) !important;
}

.q-field__control,
.q-field__native,
.q-field__input {
    background: transparent !important;
    color: white !important;
}
</style>
""", shared=True)

    ui.run(
        title=APP_TITLE,
        reload=False,
        storage_secret=DEV_STORAGE_SECRET,
    )