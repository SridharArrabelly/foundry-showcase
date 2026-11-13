"""Extract successful business calls from the hosted protocol, not assistant prose."""

import json


def successful_business_tools(response: dict) -> list[str]:
    items = response.get("output", [])
    names = set()
    for call in items:
        if call.get("type") != "function_call" or call.get("status") != "completed":
            continue
        name = call.get("name")
        if not isinstance(name, str) or not name.startswith("volt-business-tools___"):
            continue
        results = [
            item for item in items
            if item.get("type") == "function_call_output"
            and item.get("call_id") == call.get("call_id")
            and item.get("status") == "completed"
        ]
        if not call.get("call_id") or len(results) != 1:
            continue
        try:
            body = json.loads(results[0]["output"])
        except (KeyError, TypeError, json.JSONDecodeError):
            continue
        if isinstance(body, dict) and body.get("synthetic") is True and "error" not in body:
            names.add(name)
    return sorted(names)


def successful_business_calls(response: dict) -> list[dict]:
    """Keep arguments and matched results for v2; a tool name alone is insufficient."""
    items = response.get("output", [])
    calls = []
    for call in items:
        if call.get("type") != "function_call" or call.get("status") != "completed":
            continue
        name, call_id = call.get("name"), call.get("call_id")
        if not isinstance(name, str) or not name.startswith("volt-business-tools___") or not call_id:
            continue
        results = [item for item in items if item.get("type") == "function_call_output"
                   and item.get("call_id") == call_id and item.get("status") == "completed"]
        if len(results) != 1:
            continue
        try:
            arguments = json.loads(call["arguments"]) if isinstance(call.get("arguments"), str) else call.get("arguments")
            body = json.loads(results[0]["output"])
        except (KeyError, TypeError, json.JSONDecodeError):
            continue
        if isinstance(arguments, dict) and isinstance(body, dict) and body.get("synthetic") is True and "error" not in body:
            calls.append({"call_id": call_id, "name": name, "arguments": arguments, "result": body})
    return calls
