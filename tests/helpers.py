from __future__ import annotations
from typing import Any, Callable


def run_case(case: dict[str, Any], validator: Callable[[], Any], case_results: list[dict[str, Any]]) -> None:
    """Execute validator() and record the structured test-case result."""
    case["actual_result"] = ""
    case["status"] = "fail"
    case["comments"] = case.get("comments", "")
    try:
        observed_result = validator()
        if observed_result is not None:
            case["actual_result"] = str(observed_result)
        elif case.get("actual_result"):
            case["actual_result"] = str(case["actual_result"])
        else:
            case["actual_result"] = "Observed behavior matched expected result."
        case["status"] = "pass"
        if not case["comments"]:
            case["comments"] = "No issues found."
    except AssertionError as error:
        case["actual_result"] = f"Assertion failed: {error}"
        case["comments"] = case.get("comments") or "Defect found: behavior did not match expected result."
        raise
    finally:
        case_results.append(case)
