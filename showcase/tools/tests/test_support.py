import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src" / "github-copilot-invocations"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import azure.functions as func

from function_app import business_tool
from support import order_status, replacement_eligibility


def test_missing_batch_never_becomes_clearance():
    for batch in (None, "", "  "):
        assert replacement_eligibility("VC-10482", batch)["status"] == "needs_batch"


def test_recall_override_is_read_only_and_requires_approval():
    result = replacement_eligibility("VC-10482", "CH-0722")
    assert result["status"] == "eligible"
    assert result["requires_human_approval"] is True
    assert result["action_performed"] is False


def test_unknown_evidence_is_not_a_negative_recall():
    assert replacement_eligibility("VC-10482", "CH-9999")["status"] == "unknown"
    assert replacement_eligibility("UNKNOWN", "CH-0722")["status"] == "unknown"
    assert replacement_eligibility(None, "CH-0722")["status"] == "needs_order"


def test_nonrecalled_old_order_is_outside_standard_window():
    assert replacement_eligibility("VC-10482", "CH-0926")["status"] == "ineligible"
    assert order_status("vc-10482")["product_id"] == "VC-C65"


def test_client_cannot_select_the_deliberately_faulty_variant():
    request = func.HttpRequest(
        method="POST", url="https://example.test/api/tools/getRecallNotices",
        route_params={"operation": "getRecallNotices"},
        body=json.dumps({"product_id": "VC-C65", "variant": "baseline"}).encode(),
    )
    assert business_tool(request).status_code == 400


def test_actual_handler_returns_missing_batch_contract():
    request = func.HttpRequest(
        method="POST", url="https://example.test/api/tools/getRecallNotices",
        route_params={"operation": "getRecallNotices"},
        body=json.dumps({"product_id": "VC-C65"}).encode(),
    )
    assert json.loads(business_tool(request).get_body())["status"] == "needs_batch"


def test_invalid_transport_payload_is_explicit_without_echoing_input():
    for payload, expected in ((b"{", "invalid_json"), (b'"private-input"', "invalid_arguments")):
        request = func.HttpRequest(
            method="POST", url="https://example.test/api/tools/getOrderStatus",
            route_params={"operation": "getOrderStatus"}, body=payload,
        )
        response = business_tool(request)
        assert response.status_code == 400
        assert json.loads(response.get_body())["error"] == expected
        assert b"private-input" not in response.get_body()


def test_read_only_get_transport_preserves_single_and_missing_arguments():
    cases = [
        ("getOrderStatus", {"order_id": "VC-10482"}, "delivered"),
        ("getRecallNotices", {"product_id": "VC-C65"}, "needs_batch"),
        ("getReturnWarrantyEligibility", {"batch": "CH-0722"}, "needs_order"),
    ]
    for operation, params, expected in cases:
        request = func.HttpRequest(
            method="GET", url=f"https://example.test/api/tools/{operation}",
            route_params={"operation": operation}, params=params, body=b"",
        )
        response = business_tool(request)
        assert response.status_code == 200
        assert json.loads(response.get_body())["status"] == expected


def test_get_transport_still_rejects_undeclared_arguments():
    request = func.HttpRequest(
        method="GET", url="https://example.test/api/tools/getRecallNotices",
        route_params={"operation": "getRecallNotices"},
        params={"product_id": "VC-C65", "variant": "baseline"}, body=b"",
    )
    assert business_tool(request).status_code == 400


def test_recall_resource_path_preserves_optional_batch_and_rejects_ambiguity():
    for params, expected in (({}, "needs_batch"), ({"batch": "CH-0722"}, "recalled")):
        request = func.HttpRequest(
            method="GET", url="https://example.test/api/tools/getRecallNotices/VC-C65",
            route_params={"operation": "getRecallNotices", "product_id": "VC-C65"},
            params=params, body=b"",
        )
        response = business_tool(request)
        assert response.status_code == 200
        assert json.loads(response.get_body())["status"] == expected
    request = func.HttpRequest(
        method="GET", url="https://example.test/api/tools/getRecallNotices/VC-C65",
        route_params={"operation": "getRecallNotices", "product_id": "VC-C65"},
        params={"product_id": "VC-C45"}, body=b"",
    )
    assert business_tool(request).status_code == 400
