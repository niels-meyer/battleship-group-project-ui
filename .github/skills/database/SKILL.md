---
name: database
description: "Design, implement, or extend the Battleship SQLModel/SQLite database layer. Use when asked to add tables, columns, relationships, queries, or migrations; when working with Player or Match models; or when wiring persistence into game/stats logic. Keep this skill focused on database structure, session handling, and data-access functions."
argument-hint: "Implement or extend SQLModel database schema"
---

# Database Skill

All persistence uses **SQLModel** (built on SQLAlchemy) with a local **SQLite** file at
`database/battleship.db`. Tables are created on first run via `create_db_and_tables()`.

## Schema

### Player (`database/player.py`)

| Column          | Type            | Notes                                       |
| --------------- | --------------- | ------------------------------------------- |
| `id`            | `Optional[int]` | Primary key, auto-assigned                  |
| `name`          | `str`           | Unique player name; used as player identity |
| `match_history` | relationship    | One-to-many back-reference to `Match`       |

### Match (`database/match.py`)

| Column             | Type            | Notes                                                        |
| ------------------ | --------------- | ------------------------------------------------------------ |
| `id`               | `Optional[int]` | Primary key, auto-assigned                                   |
| `player_id`        | `Optional[int]` | Foreign key → `player.id`                                    |
| `player`           | relationship    | Many-to-one back-reference, `back_populates="match_history"` |
| `number_of_rounds` | `int`           | Number of rounds persisted for the match                     |
| `has_player_won`   | `bool`          | `True` if the human player won                               |

### Relationship summary

```
Player 1 ──────── * Match
         match_history
```

One Player has many Matches. Each Match references exactly one Player.

## Engine & Session (`database/db.py`)

```python
engine = create_engine("sqlite:///database/battleship.db", echo=True)

def create_db_and_tables():          # call once at startup
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

- `echo=True` means every SQL statement is printed to the terminal — expected behaviour.
- Run from the project root so the relative DB path resolves correctly.
- `create_db_and_tables()` is defined but **must be called explicitly** at app startup.

## Required Patterns

### Writing (insert)

```python
with next(get_session()) as session:
    obj = ModelClass(field=value, ...)
    session.add(obj)
    session.commit()
    session.refresh(obj)   # re-attach to get server-side defaults (e.g. id)
    return obj
```

### Reading (query)

```python
with next(get_session()) as session:
    results = session.exec(select(ModelClass).where(...)).all()
    return results
```

Always keep `select / where` inside the `with` block. Do not return lazy-loaded
relationship objects — if you need related records, query them in the same session.

### Adding a new column

1. Add the field to the SQLModel class with a default value (SQLite has no `ALTER ADD COLUMN` without defaults on existing rows).
2. Delete `database/battleship.db` during development to re-create tables, or add a manual migration.
3. Expose a getter/mutation function in the same file; do not put raw queries in UI or game code.

### Adding a new table

1. Create `database/<model>.py` following the existing `Player` / `Match` pattern.
2. Import the new class inside `create_db_and_tables()` in `database/db.py` so `metadata.create_all` includes it.

## Player Functions (`database/player.py`)

| Function                   | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| `create_player(name)`      | Insert a new player row                                                    |
| `get_player_by_name(name)` | Lookup by name, returns `Optional[Player]`                                 |
| `get_all_players()`        | Returns players ordered by name                                            |
| `register_player(name)`    | Validates, checks uniqueness, creates; returns `(bool, Player\|None, str)` |

## When To Use

- Adding or modifying `Player` or `Match` fields.
- Adding new database tables (e.g., future `Achievement`, `Round`).
- Writing new query helpers in `database/`.
- Wiring `save_match()`, player selection, or `register_player()` into game or UI code.
- Debugging missing data, transaction issues, or session/lazy-load errors.

## Pitfalls

- **Lazy loading after session close**: SQLModel/SQLAlchemy detaches objects when the session exits. Access all needed fields inside the `with` block, or convert to a plain dict/dataclass before returning.
- **Relative DB path**: `database/battleship.db` only resolves correctly when the app is run from the project root. Running tests from subdirectories can create stray DB files.
- **`create_db_and_tables()` not auto-called**: Tables won't exist until this is invoked. Call it once, early in `start.py` or the NiceGUI app init.
- **`echo=True` noise**: SQL logs appear in the terminal at all times; this is expected and not an error.
- **No migration tool**: Schema changes require manually deleting the dev DB or writing raw `ALTER TABLE` SQL for deployed data.
