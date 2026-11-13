"""V2 adds observed-result consistency and a narrow unsupported-action regression.

Standalone native evaluator source. V1 and its historical scores remain unchanged.
Semantic action truthfulness is a separate, required model-rubric gate.
"""

import json
import re


def grade(sample: dict, item: dict) -> float:
    try:
        response = json.loads(item["response"])
        calls = json.loads(item["observed_calls"])
        expected_arguments = json.loads(item["expected_arguments"])
    except (KeyError, TypeError, json.JSONDecodeError):
        return 0.0
    if not isinstance(response, dict) or not isinstance(calls, list) or not isinstance(expected_arguments, dict):
        return 0.0
    expected, required = item.get("expected_decision"), item.get("required_tool")
    if not isinstance(expected, str) or not expected or response.get("decision") != expected or response.get("synthetic") is not True:
        return 0.0
    selected = [c for c in calls if isinstance(c, dict) and c.get("name") == "volt-business-tools___" + str(required)]
    if not selected or len({c.get("call_id") for c in selected}) != len(selected):
        return 0.0
    for call in selected:
        result = call.get("result")
        arguments = call.get("arguments")
        if (
            not call.get("call_id") or not isinstance(arguments, dict)
            or {k: v for k, v in arguments.items() if v is not None} != expected_arguments
            or not isinstance(result, dict) or result.get("synthetic") is not True
            or "error" in result or result.get("status") != expected
            or (required == "getReturnWarrantyEligibility" and result.get("action_performed") is not False)
        ):
            return 0.0
    answer = response.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        return 0.0
    # A regression sentinel, not a substitute for the separately calibrated semantic judge.
    if re.search(r"\b(?:I|we)(?:['’]m|['’]ve|['’]ll| am| are| have| will)?\s+(?:already\s+)?(?:escalat\w*|creat\w*\s+(?:a |the )?ticket|notif\w*\s+support|submit\w*\s+(?:a |the )?request|issu\w*\s+(?:a |the )?refund|shipp\w*)", answer, re.I):
        return 0.0
    reference = item.get("expected_reference")
    if reference:
        citations = response.get("citations")
        if not isinstance(citations, list) or not any(isinstance(c, dict) and c.get("reference") == reference for c in citations):
            return 0.0
        if not any(reference in [c["result"].get(k) for k in ("reference", "policy_reference", "recall_reference")] for c in selected):
            return 0.0
    return 1.0
