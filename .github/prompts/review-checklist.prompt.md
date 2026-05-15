---
agent: ask
description: "Run a focused code review for Battleship changes: prioritize bugs, regressions, architecture drift, and missing validation/tests."
---

# Battleship Review Checklist

Review the current working changes as a code reviewer.

## Scope

- Prioritize correctness, regressions, and risk over style-only comments.
- Focus on project architecture boundaries and runtime behavior.
- Keep findings actionable with concrete file locations.

## Review Procedure

1. Identify changed files and classify by domain:
   - `src/core` game flow and rules
   - `src/ai` behavior and shot/placement strategy
   - `src/ui` navigation and player gating
   - `src/stats` / `database` persistence and queries
   - `src/config` runtime assumptions
2. For each changed file, check:
   - Behavioral correctness vs expected rules.
   - Regressions in turn handling, win detection, and round counting.
   - Data integrity and DB session handling.
   - UI access control (no main menu without selected player).
   - Type consistency with shared app types.
3. Evaluate validation coverage:
   - Are affected paths covered by existing tests?
   - Are new edge cases introduced without checks?
4. Rank findings by severity: high, medium, low.
5. Provide concise remediation steps per finding.

## Output Format

Use this exact structure:

### Findings

- [Severity] [file path + line or nearest symbol]: problem and impact.

### Open Questions

- Question(s) that block confidence, if any.

### Change Summary

- One short paragraph summarizing what the patch appears to do.

### Validation Gaps

- List missing checks/tests that should be added.

If no issues are found, explicitly say:

- "No material findings detected." and then list residual risks/gaps.

## Project-Specific Checks

- Coordinates remain tuple-of-strings convention.
- Board cell dictionary shape is preserved.
- `EAIDifficulty` values are not broken or renamed unintentionally.
- `with next(get_session()) as session:` pattern remains consistent.
- Config static-load behavior is respected.
