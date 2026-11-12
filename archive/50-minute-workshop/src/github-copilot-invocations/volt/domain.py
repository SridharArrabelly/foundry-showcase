"""Read-only business tools. The baseline bug is deliberate and isolated."""

import json
import math
from pathlib import Path

DATA = json.loads(Path(__file__).with_name("data.json").read_text(encoding="utf-8"))
VARIANTS = ("baseline", "improved")


def product(product_id: str) -> dict | None:
    return next((row for row in DATA["catalog"] if row["id"] == product_id), None)


def search_catalog(category: str = "charger", max_price_eur: float = 1000) -> dict:
    if not math.isfinite(max_price_eur) or max_price_eur < 0:
        raise ValueError("max_price_eur must be a finite nonnegative number")
    rows = sorted(
        (row for row in DATA["catalog"]
         if row["category"] == category and row["price"] <= max_price_eur),
        key=lambda row: (row["price"], row["id"]),
    )
    return {"synthetic": True, "currency": "EUR", "products": rows}


def check_compatibility(product_id: str, device_id: str) -> dict:
    charger, device = product(product_id), product(device_id)
    if not charger or not device:
        return {"synthetic": True, "status": "unknown", "reason": "Unknown catalog ID"}
    if charger["category"] != "charger" or "required_power_w" not in device:
        return {"synthetic": True, "status": "unknown", "reason": "Not a charger/device pair"}
    compatible = (
        charger["connector"] == device["connector"]
        and charger["power_w"] >= device["required_power_w"]
    )
    return {
        "synthetic": True, "status": "compatible" if compatible else "incompatible",
        "product_id": product_id, "device_id": device_id,
        "available_power_w": charger["power_w"],
        "required_power_w": device["required_power_w"],
    }


def recall_notices(product_id: str, batch: str | None, variant: str = "improved") -> dict:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown variant: {variant}")
    if not product(product_id):
        return {"synthetic": True, "status": "unknown", "reason": "Unknown product"}
    batch = batch.strip().upper() if batch else None
    if not batch:
        if variant == "baseline":
            # Intentional demo defect: missing evidence is mistaken for a negative result.
            return {"synthetic": True, "status": "no_recall", "product_id": product_id,
                    "batch": None, "reference": None, "demo_defect": "missing_batch"}
        return {"synthetic": True, "status": "needs_batch", "product_id": product_id,
                "reason": "Ask for the batch code before a batch-specific recall conclusion"}
    record = next(
        (row for row in DATA["batches"]
         if row["product_id"] == product_id and row["batch"] == batch), None
    )
    if record is None:
        return {"synthetic": True, "status": "unknown", "product_id": product_id,
                "batch": batch, "reason": "Batch is absent from the synthetic register"}
    return {"synthetic": True, **record}


def call_tool(name: str, arguments: dict, variant: str) -> dict:
    if name == "searchProductCatalog":
        return search_catalog(**arguments)
    if name == "checkCompatibility":
        return check_compatibility(**arguments)
    if name == "getRecallNotices":
        return recall_notices(**arguments, variant=variant)
    raise ValueError(f"Tool not allowed: {name}")
