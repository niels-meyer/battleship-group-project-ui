# Module Boundaries

Respect the project layering to preserve separation of concerns.

## Layer Ownership

- `src/core`: game rules, turn flow, board/ship behavior.
- `src/ai`: AI behavior, difficulty logic, AI-specific state.
- `database`: SQLModel models, sessions, persistence queries.
- `src/ui`: NiceGUI pages, route flow, user interaction.
- `src/config`: configuration loading and getters.

## Boundary Rules

- UI should call core/database helper functions, not perform schema logic inline.
- Core should not import UI modules.
- Database modules should avoid UI/domain presentation concerns.
- AI modules should not own UI navigation or DB schema changes.

## Shared Utilities

- Use `src/utils/helpers.py` for coordinate parsing/index conversion.
- Reuse constants from UI constants/style modules where applicable.
- Avoid duplicate helper implementations across layers.

## Change Planning

- For multi-layer features, define each layer's responsibility before coding.
- Minimize cross-layer coupling by passing typed data, not framework-specific objects.
