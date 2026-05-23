# Colors
PRIMARY_COLOR = "#023020"

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
GLOBAL_CSS = """
<style>

/* ===== DESIGN TOKENS ===== */

:root {
    --c-surface:      rgba(2, 48, 32, 0.72);
    --c-overlay:      rgba(2, 48, 32, 0.96);
    --c-border:       #0b5d3b;
    --c-glow-faint:   rgba(0, 255, 150, 0.15);
    --c-glow-low:     rgba(0, 255, 120, 0.25);
    --shadow-glow:    0 0 10px rgba(0, 255, 150, 0.25);
}

/* ===== BACKGROUND ===== */

body {
    background-image: url('/assets/menu-background.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* ===== BUTTONS ===== */

.q-btn {
    border: 1px solid var(--c-border) !important;
    border-radius: 10px !important;
    box-shadow: var(--shadow-glow) !important;
}

.q-btn:before {
    box-shadow: none !important;
}

/* ===== CARDS ===== */

.q-card {
    background: rgba(0, 20, 10, 0.82) !important;
    border: 1px solid var(--c-glow-faint);
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

.q-field__control {
    background: var(--c-surface) !important;
    border: 1px solid var(--c-glow-low) !important;
    border-radius: 14px !important;
    box-shadow: 0 0 14px rgba(0, 255, 120, 0.14) !important;
}

.q-field__native,
.q-field__input {
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
    background: var(--c-overlay) !important;
    color: white !important;
    border: 1px solid var(--c-glow-low) !important;
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
    background: var(--c-overlay) !important;
    color: white !important;
    border: 1px solid var(--c-glow-low);
    box-shadow: 0 0 8px rgba(0, 255, 120, 0.10);
}

.q-chip .q-icon {
    color: white !important;
}

/* ===== SEPARATORS ===== */

.q-separator {
    background-color: var(--c-glow-faint) !important;
}

</style>
"""