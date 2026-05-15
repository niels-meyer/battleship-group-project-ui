# Design Patterns

Apply patterns pragmatically and only when they clarify intent.

## Recommended Patterns

## Strategy

- Use for AI decision behavior by difficulty.
- Keep strategy selection explicit and testable.

## Facade

- Use to expose a small, stable API for complex subsystems.
- `Game` can serve as a facade for UI-facing gameplay actions.

## Factory Method

- Use for controlled creation of objects with configuration-based variants.
- Keep creation logic near boundaries, not spread across UI callbacks.

## Adapter

- Use when integrating external services (for example LLM providers).
- Normalize provider-specific responses into project-native types.

## Anti-Patterns To Avoid

- God classes with mixed UI, game, and persistence concerns.
- Shotgun surgery where one feature requires touching many unrelated files.
- Pattern overuse that increases indirection without clear benefit.
