"""Synthetic replacement policy. All operations are read-only."""

from datetime import date

from volt.domain import recall_notices

AS_OF = date(2026, 11, 11)
ORDER = {
    "order_id": "VC-10482",
    "product_id": "VC-C65",
    "purchased_on": "2026-09-01",
    "delivered_on": "2026-09-05",
    "status": "delivered",
    "synthetic": True,
}


def order_status(order_id: str) -> dict:
    if order_id.strip().upper() != ORDER["order_id"]:
        return {
            "synthetic": True,
            "status": "unknown",
            "reason": "Order is absent from the synthetic demonstration fixture.",
        }
    return dict(ORDER)


def replacement_eligibility(order_id: str | None, batch: str | None) -> dict:
    result = {
        "synthetic": True,
        "policy_reference": "VOLT-REPLACEMENT-2026-11",
        "as_of": AS_OF.isoformat(),
        "action_performed": False,
    }
    if not order_id or not order_id.strip():
        return {**result, "status": "needs_order", "reason": "Ask for an order ID."}
    order = order_status(order_id)
    if order["status"] == "unknown":
        return {**result, "status": "unknown", "reason": order["reason"]}
    recall = recall_notices(order["product_id"], batch, variant="improved")
    if recall["status"] in ("needs_batch", "unknown"):
        return {**result, "status": recall["status"], "reason": recall["reason"]}
    if recall["status"] == "recalled":
        return {
            **result,
            "status": "eligible",
            "reason": "The synthetic recall policy permits a replacement assessment outside the return window.",
            "recall_reference": recall["reference"],
            "requires_human_approval": True,
        }
    days_since_delivery = (AS_OF - date.fromisoformat(order["delivered_on"])).days
    return {
        **result,
        "status": "eligible" if days_since_delivery <= 30 else "ineligible",
        "reason": "Standard unopened returns use a 30-day window; warranty assessment is a separate human workflow.",
        "days_since_delivery": days_since_delivery,
        "requires_human_approval": True,
    }
