"""The same deterministic grader is registered in Foundry and exercised locally."""

import json


def grade(sample: dict, item: dict) -> float:
    """Require the expected decision and evidence of the required business tool."""
    try:
        response = json.loads(item["response"])
        tools = json.loads(item["observed_tools"])
    except (KeyError, TypeError, json.JSONDecodeError):
        return 0.0
    if not isinstance(response, dict) or not isinstance(tools, list):
        return 0.0
    if response.get("synthetic") is not True:
        return 0.0
    expected = item.get("expected_decision")
    if not isinstance(expected, str) or not expected or response.get("decision") != expected:
        return 0.0
    required = item.get("required_tool")
    if not required or not any(
        isinstance(tool, str) and tool.rsplit("___", 1)[-1] == required
        for tool in tools
    ):
        return 0.0
    if not isinstance(response.get("answer"), str) or not response["answer"].strip():
        return 0.0
    reference = item.get("expected_reference")
    citations = response.get("citations")
    if reference and not isinstance(citations, list):
        return 0.0
    if reference and not any(
        isinstance(citation, dict) and citation.get("reference") == reference
        for citation in citations
    ):
        return 0.0
    return 1.0
