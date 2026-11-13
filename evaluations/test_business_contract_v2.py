import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evaluations"))
from business_contract import grade as grade_v1
from business_contract_v2 import grade
from observed_tools import successful_business_calls, successful_business_tools


def escaped_case():
    source = json.loads((ROOT / "recordings/demo-v1.json").read_text(encoding="utf-8"))
    row = next(r for r in source["cases"] if r["case"]["id"] == "replacement-recall")
    response = {"output": row["protocol_output"]}
    return row, {**row["case"], "response": row["output_text"],
                 "observed_tools": json.dumps(successful_business_tools(response)),
                 "observed_calls": json.dumps(successful_business_calls(response)),
                 "expected_arguments": '{"order_id":"VC-10482","batch":"CH-0722"}'}


def test_actual_post_release_finding_passes_v1_and_fails_v2_with_matching_trace():
    row, item = escaped_case()
    trace = json.loads((ROOT / "recordings/demo-trace.json").read_text(encoding="utf-8"))
    assert row["response_id"] == trace["response_id"]
    assert grade_v1({}, item) == 1
    assert grade({}, item) == 0


def test_advice_and_denial_are_not_confused_with_an_executed_action():
    _, item = escaped_case()
    response = json.loads(item["response"])
    for answer in ["Contact support for assessment. No action was performed.",
                   "I cannot escalate or create a ticket. You can contact support."]:
        response["answer"] = answer
        assert grade({}, {**item, "response": json.dumps(response)}) == 1


def test_tool_and_answer_agreeing_does_not_replace_the_reviewed_expectation():
    _, item = escaped_case()
    response = json.loads(item["response"])
    response.update(decision="ineligible", answer="Contact support.")
    calls = json.loads(item["observed_calls"])
    for call in calls:
        if call["name"].endswith("getReturnWarrantyEligibility"):
            call["result"]["status"] = "ineligible"
    assert grade({}, {**item, "response": json.dumps(response), "observed_calls": json.dumps(calls)}) == 0


@pytest.mark.parametrize("change", ["status", "arguments", "action", "duplicate"])
def test_positive_answer_needs_matching_successful_tool_outcome(change):
    _, item = escaped_case()
    response = json.loads(item["response"])
    response["answer"] = "Contact human support for assessment."
    calls = json.loads(item["observed_calls"])
    selected = next(c for c in calls if c["name"].endswith("getReturnWarrantyEligibility"))
    if change == "status":
        selected["result"]["status"] = "ineligible"
    elif change == "arguments":
        selected["arguments"]["order_id"] = "VC-99999"
    elif change == "action":
        selected["result"]["action_performed"] = True
    else:
        calls.append(copy.deepcopy(selected))
    assert grade({}, {**item, "response": json.dumps(response), "observed_calls": json.dumps(calls)}) == 0


def test_v2_preserves_all_original_cases_and_expectations():
    folder = ROOT / "agent/src/.foundry/datasets"
    original = [json.loads(line) for line in (folder / "volt-regression.jsonl").read_text().splitlines()]
    updated = [json.loads(line) for line in (folder / "volt-regression-v2.jsonl").read_text().splitlines()]
    assert len(updated) == len(original) + 2
    for before, after in zip(original, updated):
        assert all(after[key] == value for key, value in before.items())
