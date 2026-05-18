---
name: nicegui-ui-flow
description: >
  Build or refactor the Battleship UI flow with NiceGUI. Use when asked to implement
  player selection/creation, main menu navigation, help/stats views, logout behavior,
  or access control between the selector page and Main Menu. Keep this skill focused
  on route flow, page behavior, and UI-level acceptance criteria.
argument-hint: "Implement NiceGUI Player Selector -> Main Menu flow"
---

# NiceGUI UI Flow Skill

Implement the UI using NiceGUI with this required navigation contract:

- App launches into the player selector page (`/`).
- Selector page has a single player name input with autocomplete suggestions.
- Empty selector input shows all existing players as suggestions.
- Entering an existing player name opens that player session and navigates to Main Menu (`/menu`).
- Entering a non-existing player name creates the player and navigates to Main Menu (`/menu`).
- Main Menu has exactly four primary buttons: `Start Game`, `Stats`, `Help`, `Logout`.
- `Logout` always returns to the selector page. It is the only way back.
- Active players who visit `/` are immediately redirected to `/menu`.
- Main Menu must not be directly accessible without an active player session.

## When To Use

- User asks for UI implementation or refactor in this project.
- User asks for player selection/creation or session flow.
- User asks for navigation or menu behavior updates in NiceGUI.
- User asks to build or update the Stats view.
- User provides UX acceptance criteria for pages and buttons.

## Required Rules

1. Use NiceGUI for all UI components and page layout.
2. Keep navigation explicit: Player Selector -> Main Menu -> feature views.
3. Keep button labels exact: `Start Game`, `Stats`, `Help`, `Logout`.
4. Enforce access gating: no direct Main Menu access without selected player context.
5. Treat acceptance criteria as testable behavior, not optional suggestions.
6. For UI page layout, code style, and session management patterns, see **project-guidelines**.

## Implementation Procedure

### 1. Build player selector page as app entry point (`/`).

- If the user is already active (`get_current_player()` returns a value), redirect immediately to `/menu`.
- Show a player name input with autocomplete.
- On empty input/focus, show suggestions for all existing players.
- On typed input, filter suggestions case-insensitively.
- On continue:
  - If player exists: set session state and navigate to `/menu`.
  - If player does not exist: create the player, set session state, and navigate to `/menu`.
  - If input is empty: show a `ui.notify` warning.

### 2. Protect Main Menu route/view.

- If player state is missing, immediately redirect to `/` using `require_current_player()`.
- Do not render menu actions before state validation.

### 3. Stats View.

- Triggered by `Stats` button in Main Menu.
- Scoped to the currently logged-in player.
- Fetch match history through existing database helper functions; avoid embedding raw SQL in UI code.
- Display the following for the active player:
  - Player name.
  - Total matches played.
  - Total wins and total losses.
  - Win rate (wins / total, shown as percentage).
  - List of individual matches showing: match number, rounds, outcome (Win / Loss).
- Provide a back action to return to Main Menu.

### 4. Keep navigation readable.

- Prefer small, named handlers for each button action.
- Avoid hidden or implicit transitions.

### 5. Verify acceptance criteria before finishing.

- Start state is the player selector page (`/`).
- Active players visiting `/` are redirected to `/menu`.
- Empty selector input shows all existing players as suggestions.
- Existing name opens that player and navigates to Main Menu.
- New name creates a player and navigates to Main Menu.
- Main Menu has all four required buttons with exact text.
- Stats button opens Stats view scoped to the active player.
- Stats view shows correct win/loss counts and match history.
- Back from Stats returns to Main Menu.
- Logout always returns to `/`. It is the only way back to the selector page.
- Direct Main Menu access without an active player session is blocked.

## Project Fit Notes

- UI helper functions live in `src/ui/pages/helpers/` split by concern:
  - `storage_session.py` — session get/set/clear
  - `access_control.py` — `require_current_player()`, `logout()`
  - `navigation.py` — `redirect_to_root()`, `redirect_to_menu()`
  - `player_selection.py` — name normalisation, lookup, create flow
- Import from the specific helper module, not a barrel `__init__.py`.
- Keep game logic in `src/core` untouched unless explicitly requested.

## Output Expectations

When this skill is used for code changes, the response should:

1. Update only the required UI and navigation files.
2. Preserve module boundaries (`src/ui` for UI, `database/` for persistence calls).
3. Provide a short verification summary mapped to each acceptance criterion.
