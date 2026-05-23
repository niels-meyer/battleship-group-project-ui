# Background
BACKGROUND_CSS = """
body {
    background-image: url('/assets/menu-background.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
"""

# Layout
PAGE_CLASS = "w-full min-h-screen items-center justify-center q-pa-xl gap-4"
VIEWPORT_PAGE_CLASS = "w-full h-full items-center q-pa-md gap-4"
FULL_WIDTH_CLASS = "w-full"

# Cards and Containers
CARD_WIDE_CLASS = "w-full max-w-3xl q-pa-lg"
CARD_MEDIUM_CLASS = "w-full max-w-2xl q-pa-lg"
CARD_COMPACT_CLASS = "w-full max-w-xl q-pa-lg"
BUTTON_COLUMN_CLASS = "w-full gap-2"

# Typography
TITLE_CLASS = "text-h4 text-weight-bold"
SECTION_HEADING_CLASS = "text-h6"

# Buttons
GREEN_BUTTON_STYLE = """
background-color: #023020 !important;
color: white !important;
border: 1px solid #0b5d3b !important;
border-radius: 10px !important;
box-shadow: 0 0 10px rgba(0, 255, 150, 0.25) !important;
"""
#Input and Selects
INPUT_SELECT_STYLE = """
background: rgba(2, 48, 32, 0.72) !important;
color: white !important;
border: 1px solid rgba(0, 255, 120, 0.30) !important;
border-radius: 14px !important;
box-shadow: 0 0 14px rgba(0, 255, 120, 0.14);
"""

# Global app styles injected once at startup via ui.add_head_html
GLOBAL_CSS = """
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

.q-btn:before {
    box-shadow: none !important;
}

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

/* ===== TEXT ===== */

body,
.q-card,
.q-field,
.q-input,
.q-select,
.q-table {
    color: white !important;
}

/* ===== INPUTS / SELECTS ===== */

.q-field__control,
.q-field__native,
.q-field__input {
    background: transparent !important;
    color: white !important;
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

.q-menu,
.q-virtual-scroll__content {
    background: rgba(2, 48, 32, 0.96) !important;
    color: white !important;
    border: 1px solid rgba(0, 255, 120, 0.25) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}

.q-item {
    background: transparent !important;
    color: white !important;
}

.q-item:hover,
.q-item.q-manual-focusable--focused {
    background: rgba(0, 255, 120, 0.16) !important;
}

/* ===== CHIPS ===== */

.q-chip {
    background: rgba(2, 48, 32, 0.92) !important;
    color: white !important;
    border: 1px solid rgba(0, 255, 120, 0.22);
    box-shadow: 0 0 8px rgba(0, 255, 120, 0.10);
}

.q-chip .q-icon {
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

.battle-cell:hover {
    background: rgba(0, 110, 60, 0.95) !important;
    box-shadow:
        0 0 12px rgba(0, 255, 120, 0.45),
        inset 0 0 10px rgba(0, 255, 150, 0.2);
    transform: scale(1.05);
}

.battle-cell:active {
    transform: scale(0.96);
}

.battle-cell:disabled {
    opacity: 0.9 !important;
}

.battle-hit {
    background: #00ff88 !important;
    color: black !important;
}

.battle-miss {
    background: rgba(20, 40, 30, 0.9) !important;
    color: #8fa39a !important;
}

.battle-ship {
    background: rgba(0, 180, 90, 0.35) !important;
}

</style>
"""