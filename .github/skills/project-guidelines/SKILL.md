---
name: project-guidelines
description: >
  Apply this project's engineering guidelines when implementing or refactoring code.
  Focus on OOP principles, design patterns, clean code practices, and strict module
  boundaries for the Battleship codebase.
argument-hint: "Apply project engineering guidelines"
---

# Project Guidelines Skill

Use this skill when a task requires architecture-aware coding decisions and consistent
code quality across the project.

## Code Style

- Use Python 3.10+ features and keep explicit type hints for public functions.
- Reuse shared types from `src/app_types.py` (`TCoord`, `TBoard`, `TShipCoords`, `EAIDifficulty`) instead of redefining shapes.
- Keep module boundaries clear: game logic in `src/core`, AI behavior in `src/ai`, persistence in `database/`, UI in `src/ui`.
- Prefer existing helper utilities in `src/utils/helpers.py` for coordinate parsing/index conversion instead of re-implementing logic.
- Match existing import style (`from src...` and `from database...`) and avoid introducing new path conventions.
- Use `@property` with matching setter decorators when controlled attribute access is needed, instead of exposing mutable internals directly.
- Follow OOP best practices: favor encapsulation, keep class responsibilities focused, and avoid mixing unrelated concerns in one class.
- Prefer small, simple functions or methods that each do one thing well (single responsibility).
- Add concise function-level comments or docstrings that explain intent, expected inputs, and side effects when behavior is not obvious.
- **Whitespace**: Never use double empty lines anywhere. Place all imports with no empty lines between them, then a single blank line before the first code.
- **String Quotes**: Use double quotes `""` for all strings instead of single quotes `''`.

## Project Conventions

- **Scripts**: Entry point and test scripts live at root: `start.py` (app launcher) and `test.py` (test runner).
- Represent coordinates as `(row, column)` string tuples, for example `("a", "1")`.
- Board cells use a consistent dictionary shape: `{"is_shot": bool, "ship": str | None}`.
- AI difficulty is controlled through `EAIDifficulty`; preserve existing enum values when extending behavior.
- `src/config/config.py` values are process-static after import; if config changes during development, restart the app.
- Stats/persistence functions use `with next(get_session()) as session:`; keep this pattern consistent.
- **Player Identity**: Player model requires a unique `name` only (no password). Root flow selects an existing player by name or creates one when no exact match exists.
- **Access Control**: Use `require_current_player()` at the start of protected pages to redirect users without an active player context to the selector page (`/`). Active players accessing `/` are redirected to `/menu`. Player session state is managed through NiceGUI's `app.storage.user` API.
- **UI Page Layout**: Keep one NiceGUI page per file in `src/ui/pages/`. Put reusable CSS class strings in `src/ui/styles.py`, route constants and keys in `src/ui/constants.py`. UI helper functions live in `src/ui/pages/helpers/` split by concern: `storage_session.py` (session state), `access_control.py` (auth guards, logout), `navigation.py` (redirects), `player_selection.py` (player lookup/creation). Import from the specific helper module, not a barrel. Keep page-specific CSS class constants at the top of the page file immediately after imports.
- **UI Readability**: When a page builds several NiceGUI components, store the meaningful components in local variables when it improves readability instead of keeping the whole layout as one long inline block.

## Testing Conventions

- Place all tests under `tests/` at the repository root.
- Mirror the `src/` folder structure inside `tests/` to keep source-to-test mapping predictable.
- Name test files as `<file_name>.test.py`.
- Configure/runs should discover all tests ending in `.test.py` when executing the full test suite.

## Topic References

- OOP principles: `references/01-oop-principles.md`
- Design patterns: `references/02-design-patterns.md`
- Clean code conventions: `references/03-clean-code.md`
- Module boundaries and layering: `references/04-module-boundaries.md`

## When To Use

- Implementing or refactoring code across the project.
- Refactoring classes with mixed responsibilities.
- Designing new features that span multiple modules.
- Reviewing PRs for architecture and maintainability.
- Ensuring consistent code style and conventions.
