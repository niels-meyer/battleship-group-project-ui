from __future__ import annotations
from typing import Any, Callable


def run_case(case: dict[str, Any], validator: Callable[[], None], case_results: list[dict[str, Any]]) -> None:
    """Execute validator() and record the structured test-case result."""
    case["actual_result"] = ""
    case["status"] = "fail"
    case.setdefault("comments", "")
    try:
        validator()
        case["actual_result"] = "Observed behavior matched expected result."
        case["status"] = "pass"
    except AssertionError as error:
        case["actual_result"] = f"Assertion failed: {error}"
        case["comments"] = "Defect found: behavior did not match expected result."
        raise
    finally:
        case_results.append(case)
