---
name: ai-behavior
description: >
  Implement or extend Battleship AI behavior only. Use when changing shot-selection
  strategy, ship-placement strategy, AI difficulty behavior, or AI-specific tests.
  Keep this skill limited to `src/ai` and AI integration touchpoints.
argument-hint: "Implement or refine Battleship AI behavior"
---

# AI Behavior Skill

This skill is dedicated to AI concerns and should not include core game-loop,
UI flow, or database schema design decisions.

## Scope

- AI shot-selection behavior in `src/ai/ai.py`.
- Difficulty-level behavior for `EAIDifficulty` values.
- Algorithmic AI behavior in `src/ai/algorithmic_ai.py`.
- LLM AI integration behavior in `src/ai/llm_ai.py`.
- AI tests in `tests/ai/` using mirrored structure and `*.test.py` naming. Run tests with `python test.py`.

## Out Of Scope

- Core turn-loop orchestration in `src/core/game.py`.
- NiceGUI route and page behavior in `src/ui/`.
- SQLModel schema/session changes in `database/`.

## AI Conventions

- Keep AI strategy logic encapsulated inside AI classes, not in UI callbacks.
- See **project-guidelines** for shared types, coordinate formats, difficulty enum handling, and code structure principles.

## Difficulty Extension Guidance

1. Implement deterministic or probabilistic logic per difficulty level in AI code.
2. Keep fallback behavior safe when strategy state is exhausted.
3. Ensure shot deduplication to avoid firing at the same coordinate twice.
4. Add or update AI tests for each new behavior branch.

## LLM AI Guidance

- Treat LLM output as untrusted input and validate/parse robustly.
- Keep model-dependent behavior isolated from deterministic AI logic.
- Gate LLM tests behind local availability checks.

## When To Use

- Add a new AI difficulty mode.
- Improve target-selection after a hit.
- Refactor AI state tracking for hunt/target behavior.
- Fix flaky or failing AI tests.
