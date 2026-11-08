import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "github-copilot-invocations"))
from volt.domain import call_tool, check_compatibility, recall_notices, search_catalog
from volt.evaluation import evaluate_case


class DomainTests(unittest.TestCase):
    def test_catalog_sorted_and_budgeted(self):
        self.assertEqual(["VC-C30", "VC-C65"],
                         [r["id"] for r in search_catalog("charger", 50)["products"]])

    def test_compatibility(self):
        self.assertEqual("incompatible", check_compatibility("VC-C30", "VC-BOOK14")["status"])
        self.assertEqual("compatible", check_compatibility("VC-C65", "VC-BOOK14")["status"])

    def test_unknown_and_invalid_pair(self):
        self.assertEqual("unknown", check_compatibility("missing", "VC-BOOK14")["status"])
        self.assertEqual("unknown", check_compatibility("VC-CABLE", "VC-BOOK14")["status"])

    def test_missing_batch_contract(self):
        self.assertEqual("needs_batch", recall_notices("VC-C65", None)["status"])
        self.assertEqual("needs_batch", recall_notices("VC-C65", "   ")["status"])

    def test_unknown_batch_is_not_negative_evidence(self):
        self.assertEqual("unknown", recall_notices("VC-C65", "CH-9999")["status"])

    def test_registered_batches(self):
        self.assertEqual("recalled", recall_notices("VC-C65", "ch-0722")["status"])
        self.assertEqual("no_recall", recall_notices("VC-C65", "CH-0926")["status"])

    def test_baseline_defect_is_explicit(self):
        self.assertEqual("no_recall", recall_notices("VC-C65", None, "baseline")["status"])

    def test_only_allowlisted_tools(self):
        with self.assertRaises(ValueError):
            call_tool("shell", {}, "improved")

    def test_invalid_budget(self):
        for value in [-1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                search_catalog(max_price_eur=value)

    def test_bad_variant_rejected(self):
        with self.assertRaises(ValueError):
            recall_notices("VC-C65", None, "typo")

    def test_regression_detects_baseline_tool_bug(self):
        case = json.loads((ROOT / "datasets" / "regression.jsonl").read_text().splitlines()[0])
        for variant in ["baseline", "improved"]:
            tool_result = recall_notices("VC-C65", None, variant)
            result = {"output": {"decision": tool_result["status"], "answer": "A test response"},
                      "tool_calls": [{"name": "getRecallNotices", "result": tool_result}]}
            self.assertEqual(variant == "improved", evaluate_case(case, result)["passed"])

    def test_unreviewed_case_never_passes_gate(self):
        case = {"id": "unreviewed", "query": "Unknown query", "expected_decision": "unknown",
                "expected_behavior": "Human review required"}
        result = {"output": {"decision": "unknown", "answer": "Unknown"}, "tool_calls": []}
        self.assertFalse(evaluate_case(case, result)["passed"])


if __name__ == "__main__":
    unittest.main()
