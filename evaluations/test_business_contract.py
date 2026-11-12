import json

from business_contract import grade


def row(decision, tools=None):
    return {
        "response": json.dumps({"decision": decision, "synthetic": True, "answer": "Please supply the batch code."}),
        "observed_tools": json.dumps(tools if tools is not None else ["volt___getRecallNotices"]),
        "expected_decision": "needs_batch",
        "required_tool": "getRecallNotices",
    }


def test_original_business_failure_is_not_a_coherence_pass():
    assert grade({}, row("no_recall")) == 0
    assert grade({}, row("needs_batch")) == 1


def test_answer_without_observed_tool_evidence_fails():
    assert grade({}, row("needs_batch", [])) == 0


def test_malformed_output_and_invented_citation_fail():
    case = row("needs_batch")
    case["response"] = "A fluent answer, but not the structured contract."
    assert grade({}, case) == 0
    case = row("needs_batch")
    case["expected_reference"] = "VOLT-REPLACEMENT-2026-11"
    assert grade({}, case) == 0
