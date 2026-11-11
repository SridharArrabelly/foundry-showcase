import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evaluate_captures import validate_case_coverage


CASES = [
    {"id": "replacement", "query": "Can I replace it?", "expected_decision": "eligible"},
    {"id": "missing-batch", "query": "I do not have a batch.", "expected_decision": "needs_batch"},
]


def test_complete_captures_accept_response_fields_and_any_order():
    rows = [{**case, "response": "captured output"} for case in reversed(CASES)]
    validate_case_coverage(rows, CASES)


@pytest.mark.parametrize("rows", [[], CASES[:1], [CASES[0], CASES[0]]])
def test_partial_or_duplicate_captures_cannot_pass_a_release_gate(rows):
    with pytest.raises(ValueError, match="every expected case"):
        validate_case_coverage(rows, CASES)


@pytest.mark.parametrize(
    "change",
    [{"expected_decision": "recommendation"}, {"query": "A different question"}],
)
def test_captured_expectations_cannot_weaken_the_fixed_dataset(change):
    rows = [{**CASES[0], **change}, CASES[1]]
    with pytest.raises(ValueError, match="expectations differ"):
        validate_case_coverage(rows, CASES)


def test_duplicate_expected_cases_are_rejected():
    with pytest.raises(ValueError, match="unique cases"):
        validate_case_coverage(CASES, [CASES[0], CASES[0]])
