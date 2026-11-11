import sys
from copy import deepcopy
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evaluate_captures import validate_case_coverage
from promote_demo import validate_quality


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


def release_evidence():
    run = {
        "status": "completed",
        "result_counts": {"passed": 2, "total": 2, "failed": 0, "errored": 0, "skipped": 0},
        "metadata": {"source_commit": "commit", "code_content_hash": "digest"},
    }
    items = [{
        "status": "completed", "datasource_item": {**case, "code_content_hash": "digest"},
        "results": [{"status": "completed", "passed": True, "score": 1.0}],
    } for case in CASES]
    return run, items


def test_promotion_accepts_complete_native_evidence_for_the_exact_package():
    run, items = release_evidence()
    validate_quality(run, items, CASES, "commit", "digest")


def test_promotion_rejects_another_commit_even_when_all_scores_pass():
    run, items = release_evidence()
    with pytest.raises(ValueError, match="different source commit"):
        validate_quality(run, items, CASES, "another-commit", "digest")


def test_promotion_rejects_pass_labels_with_a_weakened_threshold():
    run, items = release_evidence()
    items = deepcopy(items)
    items[0]["results"][0]["score"] = 0.0
    with pytest.raises(ValueError, match="score 1"):
        validate_quality(run, items, CASES, "commit", "digest")


def test_promotion_rejects_missing_case_evidence_despite_all_pass_counts():
    run, items = release_evidence()
    with pytest.raises(ValueError, match="every expected case"):
        validate_quality(run, items[:1], CASES, "commit", "digest")
