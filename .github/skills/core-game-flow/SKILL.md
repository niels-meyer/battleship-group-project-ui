---
name: core-game-flow
description: >
  Implement or extend the Battleship core game loop: ship placement, turn management,
  shooting, win detection, and post-match persistence. Use when asked to change game
  rules, adjust round counting, alter ship placement logic, or wire game outcomes
  into persistence. Keep this skill focused on core flow in `src/core/game.py`.
argument-hint: "Implement or extend the Battleship game loop"
---

# Core Game Flow Skill

This skill is only for match-loop behavior in `src/core/game.py`. For AI strategy changes,
use a separate AI-focused skill.

The game is Human Player vs AI. All interaction is driven by NiceGUI event handlers.
There is no blocking terminal I/O. `Game` holds all match state and exposes discrete
methods that NiceGUI callbacks call one at a time.

## High-Level Flow

```
Game(player_name)          ← instantiated when NiceGUI starts the game
  │
  ├─ Ship Placement phase  ← NiceGUI calls get_current_ship() → show UI
  │    NiceGUI provides start coord → get_valid_end_coords(start)
  │    NiceGUI provides end coord   → place_player_ship(start, end)
  │    repeat until all_ships_placed == True
  │
  └─ Shooting phase        ← NiceGUI drives the turn loop
       if game.is_player_turn:
           NiceGUI provides coord → player_shoot(coord) → bool (hit?)
       else:
           coord, hit = ai_shoot()  → update UI
       check game.is_game_over after each shot
       when over: game.finish()  → persists match to DB
```

## Key Classes and Where They Live

| Class           | File                 | Responsibility                                        |
| --------------- | -------------------- | ----------------------------------------------------- |
| `Game`          | `src/core/game.py`   | Match state + event-driven API for NiceGUI            |
| `Player`        | `src/core/player.py` | Human player: owns `Board` + `Ships`, persists to DB  |
| `AI`            | `src/ai/ai.py`       | Opponent integration point called by core flow        |
| `Board`         | `src/core/board.py`  | Grid state, receives ships and shots                  |
| `Ships`         | `src/core/ships.py`  | Tracks remaining ship coordinates; detects sunk/alive |
| `EAIDifficulty` | `src/app_types.py`   | Enum: `BABY` `EASY` `NORMAL` `HARD` `IMPOSSIBLE`      |

## Game API Reference

### Construction

```python
game = Game(player_name="alice")   # player_name is the DB player name
```

`Game.__init__` accepts `player_name: str` (used to look up / create the DB player).

### Ship Placement

```python
game.all_ships_placed          # bool — True when all ships have been placed
game.get_current_ship()        # Optional[tuple[str, int]] — (name, length) or None
game.get_valid_end_coords(start_coord)   # list[TCoord]
game.place_player_ship(start_coord, end_coord)  # places for player + AI, advances index
```

### Shooting

```python
game.is_player_turn            # bool property
game.is_valid_shot(coord)      # bool — False if already shot at
game.player_shoot(coord)       # bool — True = hit; also calls _change_turn()
game.ai_shoot()                # tuple[TCoord, bool] — (coord_shot, was_hit); also calls _change_turn()
```

Core flow should consume the AI as a dependency and not implement shot-selection
algorithms itself.

### Board Access

```python
game.get_player_board()        # TBoard — player's grid
game.get_ai_board()            # TBoard — AI's grid (ships hidden in UI)
```

### Game State & Finish

```python
game.is_game_over              # bool property
game.has_player_won            # bool property
game.finish()                  # persists match to DB via Player.save_match()
```

## Coordinate System

All coordinates follow the convention defined in **project-guidelines**:
`TCoord = Tuple[str, str]` — `("row_letter", "column_string")`, e.g. `("a", "1")`, `("j", "10")`.
Row letters come from `ROWS` in `src/constants.py` (a–j by default).
Column strings come from `COLUMNS` in `src/constants.py` (1–10 by default).

- Convert with `get_row_index(row)` / `get_column_index(col)` in `src/utils/helpers.py`.
- Parse user text input with `parse_coord(input_str)` in `src/utils/helpers.py` — raises `ValueError` on bad format.

## Board Cell Shape

```python
{"is_shot": bool, "ship": str | None}
```

`ship` is the ship name when a ship occupies the cell; `None` otherwise.
After a ship is fully sunk, the `ship` value is **not** cleared from existing cells —
use `Ships.has_ships()` / `game.is_game_over` to check end state.

## Round Counting

- `_number_of_rounds` starts at `1`.
- `_does_player_start` records who went first (random at init).
- Increments when the opening player's turn comes around again (inside `_change_turn`).

```python
def _change_turn(self):
    self._is_player_turn = not self._is_player_turn
    if self._is_player_turn == self._does_player_start:
        self._number_of_rounds += 1
```

## Return Values (no print/input anywhere in core)

| Method                               | Returns                                         |
| ------------------------------------ | ----------------------------------------------- |
| `Player.shoot_player(player, coord)` | `bool` — True = hit                             |
| `AI.shoot_player(player)`            | `tuple[TCoord, bool]` — coord shot + hit result |
| `game.player_shoot(coord)`           | `bool` — True = hit                             |
| `game.ai_shoot()`                    | `tuple[TCoord, bool]`                           |

## Post-Match Persistence

```python
game.finish()
# internally calls:
# player.save_match(number_of_rounds=..., has_player_won=game.has_player_won, ai_difficulty=...)
# which calls: create_match(player_id, rounds, won, ai_difficulty) in database/match.py
```

`has_player_won` is `True` when `player.ships.has_ships()` is still `True` after the loop.

## When To Use

- Changing ship placement logic or board validation.
- Modifying round counting or turn management.
- Wiring game outcome to database (match saving).
- Building the NiceGUI game UI that calls the `Game` API.
- Adding new game rules or win conditions.

## Pitfalls

- **`is_valid_shot` only checks the AI board**: use it before calling `player_shoot`.
- **Constants are static**: `ROWS`, `COLUMNS`, and `SHIPS` are defined in `src/constants.py` and loaded once at import. Changing them requires an app restart.
- **`create_db_and_tables()` must be called before any DB operation**: `Player.__init__` immediately creates/fetches a player row — ensure DB is initialised before `Game(player_name)` is called.

## Skill Boundary

- Use this skill for match orchestration in `src/core/game.py`.
- Use the AI behavior skill for shot-selection strategy and difficulty logic.
