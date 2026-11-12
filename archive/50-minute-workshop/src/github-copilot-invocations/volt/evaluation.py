"""Deterministic release assertions, not a substitute for semantic/human review."""


def evaluate_case(case: dict, result: dict) -> dict:
    output = result["output"]
    calls = result["tool_calls"]
    names = {call["name"] for call in calls}
    checks = {
        "reviewed_case": case.get("approved") is True,
        "decision": output["decision"] == case["expected_decision"],
        "required_tools": set(case.get("required_tools", [])) <= names,
        "forbidden_tools": not (set(case.get("forbidden_tools", [])) & names),
        "nonempty_answer": bool(output["answer"].strip()),
    }
    for field in ("product_id", "batch"):
        expected = "expected_" + field
        if expected in case:
            checks[field] = output.get(field) == case[expected]
    if case["expected_decision"] == "recommend":
        chosen = output.get("product_id")
        checks["compatibility_evidence"] = any(
            c["name"] == "checkCompatibility"
            and c["result"].get("product_id") == chosen
            and c["result"].get("status") == "compatible"
            for c in calls
        )
    if case["expected_decision"] == "needs_batch":
        checks["missing_batch_tool_contract"] = any(
            c["name"] == "getRecallNotices" and c["result"].get("status") == "needs_batch"
            for c in calls
        )
    return {"id": case["id"], "query": case["query"], "passed": all(checks.values()), "checks": checks,
            "expected_behavior": case["expected_behavior"],
            "result": result}
