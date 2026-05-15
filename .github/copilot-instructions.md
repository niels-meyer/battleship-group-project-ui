# Project Guidelines

For code style, conventions, and engineering guidelines, see the **project-guidelines** skill.

## Project Architecture

- Entry point is `start.py`, which launches `src/ui/app.py` (NiceGUI application launcher).
- NiceGUI route registration and page imports live in `src/ui/app.py`, but each page implementation lives in its own file under `src/ui/pages/`.
- Root page (`/`) is a player selector page that handles selecting or creating a player before accessing the application.
- After selecting or creating a player, the user is redirected to Main Menu (`/menu`) and session is maintained via the simple NiceGUI `app.storage.user` mechanism.
- Active players cannot access the selector page directly; using the `Logout` button is the only way to return to selector.
- `src/core/game.py` contains the turn loop, ship placement flow, shooting flow, and win/loss handling.
- `src/core/player.py` composes `Board` + `Ships` and persists players/matches through `database/`.
- `src/ai/ai.py` subclasses `Player` and controls AI ship placement and shot selection by difficulty.
- Configuration is loaded once at import time from `src/config/config.json` via `src/config/config.py` getters.
- Database layer is SQLModel + SQLite in `database/db.py`; models and query functions live in `database/player.py` and `database/match.py`.

## Build and Test

- Setup:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Run app:
  - `python start.py`
- Run tests:
  - `python test.py` (runs all `*.test.py` files)
  - `python -m pytest tests/ai/algorithmic_ai.test.py` (run specific test)
- LLM-related code in `src/ai/llm_ai.py` depends on local Ollama availability and model configuration.

## Conventions

All code style, naming, and architectural conventions are defined in the **project-guidelines** skill.
