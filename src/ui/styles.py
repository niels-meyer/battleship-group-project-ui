# Colors
PRIMARY_COLOR = "#023020"
COLOR_CARD    = "#00140a"
COLOR_GLOW    = "#00ff78"
COLOR_TEXT    = "#ffffff"
C_BORDER      = "#0b5d3b"

# Layout
PAGE_CLASS = "w-full min-h-screen items-center justify-center q-pa-xl gap-4"
FULL_WIDTH_CLASS = "w-full"

# Cards and Containers
CARD_WIDE_CLASS = "w-full max-w-3xl q-pa-lg"
CARD_MEDIUM_CLASS = "w-full max-w-2xl q-pa-lg"
CARD_COMPACT_CLASS = "w-full max-w-xl q-pa-lg"
BUTTON_COLUMN_CLASS = "w-full gap-2"

# Typography
TITLE_CLASS = "text-h4 text-weight-bold"
SECTION_HEADING_CLASS = "text-h6"

# Global app styles injected once at startup via ui.add_head_html
GLOBAL_CSS = f"""
<style>

/* ===== BACKGROUND ===== */

body {{
    background-image: url('/assets/menu-background.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* ===== BUTTONS ===== */

.q-btn {{
    border: 1px solid {C_BORDER} !important;
    border-radius: 10px !important;
    box-shadow: 0 0 10px {COLOR_GLOW}40 !important;
}}

.q-btn:before {{
    box-shadow: none !important;
}}

/* ===== CARDS ===== */

.q-card {{
    background: {COLOR_CARD}d1 !important;
    border: 1px solid {COLOR_GLOW}26;
    backdrop-filter: blur(6px);
    color: {COLOR_TEXT};
}}

/* ===== TEXT ===== */

body,
.q-card,
.q-field,
.q-input,
.q-select,
.q-table {{
    color: {COLOR_TEXT} !important;
}}

/* ===== INPUTS / SELECTS ===== */

.q-field__control {{
    background: {PRIMARY_COLOR}b8 !important;
    border: 1px solid {COLOR_GLOW}40 !important;
    border-radius: 14px !important;
    box-shadow: 0 0 14px {COLOR_GLOW}24 !important;
}}

.q-field__native,
.q-field__input {{
    color: {COLOR_TEXT} !important;
}}

.q-field__label {{
    color: {COLOR_TEXT}bf !important;
}}

.q-field__append,
.q-field__prepend,
.q-icon {{
    color: {COLOR_TEXT} !important;
}}

/* ===== AUTOCOMPLETE DROPDOWN ===== */

.q-menu,
.q-virtual-scroll__content {{
    background: {PRIMARY_COLOR}f5 !important;
    color: {COLOR_TEXT} !important;
    border: 1px solid {COLOR_GLOW}40 !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}}

.q-item {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
}}

.q-item:hover,
.q-item.q-manual-focusable--focused {{
    background: {COLOR_GLOW}29 !important;
}}

/* ===== CHIPS ===== */

.q-chip {{
    background: {PRIMARY_COLOR}f5 !important;
    color: {COLOR_TEXT} !important;
    border: 1px solid {COLOR_GLOW}40;
    box-shadow: 0 0 8px {COLOR_GLOW}1a;
}}

.q-chip .q-icon {{
    color: {COLOR_TEXT} !important;
}}

/* ===== SEPARATORS ===== */

.q-separator {{
    background-color: {COLOR_GLOW}26 !important;
}}

/* ===== TABLES ===== */

.q-table__container,
.q-table thead tr,
.q-table tbody tr {{
    background: {PRIMARY_COLOR}b8 !important;
    color: {COLOR_TEXT} !important;
}}

.q-table tbody tr:hover {{
    background: {PRIMARY_COLOR}f5 !important;
}}

.q-table th,
.q-table td {{
    border-color: {COLOR_GLOW}26 !important;
    color: {COLOR_TEXT} !important;
}}

</style>
"""