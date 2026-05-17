---
name: tests
description: >
  Write or extend pytest tests for the Battleship codebase. Use when asked to add
  tests, fix failing tests, increase coverage, or review testing conventions. Covers
  pytest idioms, fixture usage, parametrization, and the project's two established
  test styles.
argument-hint: "Write or fix pytest tests"
---

# Tests Skill

Use this skill for any task that involves writing, fixing, or reviewing tests.

## Scope

- All test files under `tests/`, mirroring the `src/` folder structure.
- Test helpers, fixtures, and shared utilities that support the test suite.
- Integration points: verifying behavior across `src/core/`, `src/ai/`, `src/database/`, and `src/ui/`.

## Out Of Scope

- Production source code in `src/` — limit edits to `tests/` unless a bug is found and must be fixed in source.
- Changing NiceGUI page routing or database schema purely for testability.

---

## File and Folder Conventions

- Place all tests under `tests/` at the repository root.
- Mirror the `src/` structure: `tests/ai/`, `tests/core/`, `tests/database/`, `tests/ui/`.
- Name test files with the `*_test.py` suffix (e.g., `board_test.py`, not `test_board.py`).
- Name test functions with the `test_` prefix and a descriptive snake_case label that reads like a sentence.
- Do **not** use `conftest.py` unless sharing fixtures across multiple test files is strictly necessary.

---

## Pytest Conventions

### Assertions

- Always use plain `assert` statements — never `assertEqual`, `assertTrue`, or unittest-style methods.
- Include a readable failure message in the assert when the reason for failure would not be obvious from the expression alone: `assert result == expected, f"got {result}"`.

### Fixtures

- Define fixtures with `@pytest.fixture` in the same file unless they are shared across multiple test files.
- Use the lowest scope that satisfies the need: default `function` scope first, then `module`, then `session`.
- Fixtures should return or yield data, not assert anything themselves.
- Prefer fixture composition (one fixture calling another) over large setup blocks inside test bodies.

### Parametrize

- Use `@pytest.mark.parametrize` for data-driven tests instead of loops inside a test body.
- Provide an `ids` argument when tuple parameters would produce unreadable auto-generated IDs.

```python
@pytest.mark.parametrize("value,expected", [
    ("EASY", EAIDifficulty.EASY),
    ("HARD", EAIDifficulty.HARD),
], ids=["easy", "hard"])
def test_parse_ai_difficulty_valid(value: str, expected: EAIDifficulty) -> None:
    assert parse_ai_difficulty(value) == expected
```

### Markers

- Use `@pytest.mark.skip(reason="...")` when a test is intentionally disabled; never comment out a test.
- Use `@pytest.mark.xfail(reason="...")` for known failures that are tracked but not yet fixed.
- Gate tests that require local infrastructure (e.g., Ollama) behind a custom marker or `pytest.importorskip`.

### Test Classes

- Avoid test classes unless you are grouping a large set of tightly related cases that share significant setup not easily expressed with fixtures.
- When using a class, do not inherit from `unittest.TestCase`; pytest can discover plain classes.

---

## Project Test Styles

The codebase uses two established styles. Match the style that best fits the type of behavior being tested.

### Style A — Plain Pytest (preferred for unit tests)

Use for testing a single function or method with focused inputs and outputs. Keep the test body short and direct — import, call, assert.

```python
def test_difficulty_ranks_span_from_one_to_ten() -> None:
    ranks = [get_ai_difficulty_rank(d) for d in get_available_ai_difficulties()]
    assert min(ranks) == 1
    assert max(ranks) == 10
```

Rules:

- One behavior per test function.
- Arrange → Act → Assert, with a blank line between each phase when the phases are non-trivial.
- Do not add `case` dicts, result lists, or `run_case` wrappers.

### Style B — Structured Test-Case (for integration / acceptance tests)

Use when a test maps to a numbered acceptance criterion, a QA test-case document, or a multi-step scenario that benefits from structured metadata. Each test uses a `case` dict and delegates to `run_case`.

```python
def test_tc_001_impossible_targets_unshot_ship(case_results: list[dict[str, Any]]) -> None:
    case = {
        "id": "TC_001",
        "title": "...",
        "preconditions": "...",
        "steps": [...],
        "test_data_input": {...},
        "expected_result": "...",
        "actual_result": "",
        "status": "",
        "comments": "",
    }

    # arrange
    ai = SimpleBattleshipAI(difficulty=EAIDifficulty.IMPOSSIBLE)
    board = make_board(ship_cells={(2, 3): "Destroyer"})

    def validate() -> None:
        shot = ai.decide_shot(board)
        assert shot == (2, 3)

    run_case(case, validate, case_results)
```

Rules:

- ID format: `TC_NNN` (zero-padded three digits).
- Function name: `test_tc_NNN_short_snake_case_label`.
- `case_results` fixture is injected from a `@pytest.fixture` defined in the same file.
- `run_case` sets `"actual_result"`, `"status"`, and `"comments"` in the case dict; it must be defined locally or imported from a shared helper once one exists.
- The `validate` inner function contains only `assert` statements.

---

## Shared Test Utilities

- Board factory helpers (e.g., `make_board`) belong at the top of the test file. If the same helper is needed in two or more test files, move it to `tests/helpers.py` (create if absent) and import from there.
- Avoid re-implementing logic found in `src/` — import and call the real functions.

---

## Type Hints

- Annotate all test functions and fixtures with return types (`-> None`, `-> list[...]`, etc.).
- Use `from __future__ import annotations` at the top of files that use forward references or `|` union syntax for compatibility.

---

## What Not To Do

- Do not use `print()` inside tests for debugging; use `pytest`'s `-s` flag or `capfd` fixture instead.
- Do not mutate shared fixtures; return a new object or use `copy.deepcopy` when mutation is needed.
- Do not catch exceptions inside tests to suppress them — let pytest capture and report them.
- Do not import from `src/ui/` in unit tests for game logic; test layers independently.

---

## Running Tests

```bash
pytest                                          # run all tests
pytest tests/ai/algorithmic_ai_test.py         # run a specific file
pytest tests/ai/algorithmic_ai_test.py::test_tc_001_impossible_targets_unshot_ship  # run one test
pytest -k "impossible"                         # filter by keyword
pytest -v                                      # verbose output
pytest --tb=short                              # shorter tracebacks
```

---

## When To Use

- Adding tests for a new feature in any module.
- Increasing coverage for uncovered branches in `src/core/`, `src/ai/`, or `src/database/`.
- Fixing a failing test without changing its intent.
- Reviewing whether a test follows the project's established style.
