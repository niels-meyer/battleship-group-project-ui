# OOP Principles

Use these principles to keep the Battleship codebase maintainable and extensible.

## Single Responsibility Principle

- Each class should have one reason to change.
- Keep game orchestration in `src/core/game.py`.
- Keep AI strategy logic in `src/ai/`.
- Keep persistence logic in `database/`.
- Keep page rendering and event handlers in `src/ui/`.

## Encapsulation

- Prefer private attributes with controlled access through methods/properties.
- Avoid exposing mutable internal state directly when invariants matter.
- Keep cross-object mutations explicit and validated.

## Composition Over Inheritance

- Favor composition for assembling behavior.
- Keep `Player` composed of `Board` and `Ships` responsibilities.
- Use inheritance for true subtype behavior, not code reuse convenience.

## Open/Closed Principle

- Extend behavior through new methods/strategies where possible.
- Avoid editing multiple existing modules for one feature when extension points exist.

## Dependency Direction

- High-level flow should depend on stable interfaces/abstractions.
- UI should call domain methods, not manipulate low-level internals directly.
