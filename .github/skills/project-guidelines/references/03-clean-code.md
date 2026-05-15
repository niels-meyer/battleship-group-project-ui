# Clean Code

Follow these conventions for readability and consistency.

## Function and Method Design

- Keep methods small and focused on one behavior.
- Use intention-revealing names.
- Prefer early returns to reduce nesting.
- Keep side effects explicit.

## Types and Contracts

- Use explicit type hints for public functions.
- Reuse shared types from `src/app_types.py`.
- Validate inputs at boundaries and fail with clear messages.

## Comments and Docstrings

- Add concise comments only when logic is non-obvious.
- Prefer docstrings for non-trivial public methods.
- Keep comments aligned with real behavior and update when code changes.

## Formatting Rules

- Use double quotes for strings.
- Avoid double empty lines.
- Keep imports grouped without blank lines between import statements, then one blank line before code.

## Testing Mindset

- Add tests for non-trivial logic changes.
- Focus tests on behavior, not implementation details.
- Keep test names descriptive and scenario-oriented.
