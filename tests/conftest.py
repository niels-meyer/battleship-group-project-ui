from __future__ import annotations
from typing import Any
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine
from src.database.player import Player as DbPlayer  # noqa: F401 – registers table in SQLModel.metadata
from src.database.match import Match  # noqa: F401 – registers table in SQLModel.metadata
import src.database.db as db_module


STATUS_COLORS = {
    "pass": "\033[32m",
    "fail": "\033[31m",
}
RESET_COLOR = "\033[0m"


@pytest.fixture
def case_results() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    yield results

    if not results:
        return

    headers = ["ID", "Status", "Expected", "Actual", "Comments"]
    # Prepare rows and compute column widths, with sensible caps to avoid ultra-wide output
    import textwrap

    rows = [
        [
            str(case.get("id", "")),
            str(case.get("status", "")),
            str(case.get("expected_result", "")),
            str(case.get("actual_result", "")),
            str(case.get("comments", "")),
        ]
        for case in results
    ]

    # maximum column widths (chars) to keep table readable
    max_caps = [10, 6, 60, 80, 40]

    widths = [
        min(max(len(header), *(len(row[index]) for row in rows)), max_caps[index])
        for index, header in enumerate(headers)
    ]

    def color_status(text: str) -> str:
        color = STATUS_COLORS.get(text.strip().lower())
        return f"{color}{text}{RESET_COLOR}" if color else text

    def format_row(values: list[str]) -> str:
        return "| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(values)) + " |"

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    print("Test Case Results")
    print(format_row(headers))
    print(separator)

    # Print each case as a wrapped, multi-line row
    for case in results:
        cols = [
            str(case.get("id", "")),
            str(case.get("status", "")),
            str(case.get("expected_result", "")),
            str(case.get("actual_result", "")),
            str(case.get("comments", "")),
        ]

        wrapped_cols = [textwrap.wrap(cols[i], widths[i]) or [""] for i in range(len(cols))]
        max_lines = max(len(w) for w in wrapped_cols)

        for line_index in range(max_lines):
            line_values: list[str] = []
            for i in range(len(cols)):
                part = wrapped_cols[i][line_index] if line_index < len(wrapped_cols[i]) else ""
                line_values.append(part)

            # pad values first, then apply color to the padded status field to avoid misalignment
            formatted_values: list[str] = []
            for i, val in enumerate(line_values):
                padded = val.ljust(widths[i])
                if i == 1 and line_index == 0:
                    padded = color_status(padded)
                formatted_values.append(padded)

            print("| " + " | ".join(formatted_values) + " |")

        print(separator)
        print()


@pytest.fixture
def in_memory_db():
    """Replace the global DB engine with a fresh in-memory SQLite database for one test."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    original_engine = db_module.engine
    db_module.engine = test_engine
    yield test_engine
    db_module.engine = original_engine
