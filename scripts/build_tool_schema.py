"""Generate the APIM operation contract from the API's actual validation schemas."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from function_app import OPERATIONS

DESCRIPTIONS = {
    "searchProductCatalog": "Find fictional Volt products within a category and EUR budget.",
    "checkCompatibility": "Check a fictional charger and device using catalog specifications.",
    "getRecallNotices": "Check the synthetic batch-specific recall register. Missing batch is not evidence of no recall.",
    "getOrderStatus": "Read the single synthetic order fixture. Does not authorize ownership or change the order.",
    "getReturnWarrantyEligibility": "Assess the synthetic replacement policy; never issue refunds, ship goods, or approve a replacement.",
}


def openapi_schema(value):
    if isinstance(value, list):
        return [openapi_schema(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {key: openapi_schema(item) for key, item in value.items()}
    alternatives = result.get("anyOf", [])
    if len(alternatives) == 2 and {"type": "null"} in alternatives:
        non_null = next(item for item in alternatives if item != {"type": "null"})
        result.pop("anyOf")
        result.update(non_null)
        result["nullable"] = True
    return result


def main():
    paths = {}
    for name, (schema, _) in OPERATIONS.items():
        definition = openapi_schema(schema.model_json_schema())
        path = f"/tools/{name}"
        if name == "getRecallNotices":
            path += "/{product_id}"
        paths[path] = {"get": {
            "operationId": name,
            "summary": name,
            "description": DESCRIPTIONS[name],
            "parameters": [
                {
                    "name": field,
                    "in": "path" if name == "getRecallNotices" and field == "product_id" else "query",
                    "required": field in definition.get("required", []),
                    "description": spec.get("description", ""),
                    "schema": spec,
                }
                for field, spec in definition["properties"].items()
            ],
            "responses": {
                "200": {"description": "Read-only synthetic business result",
                        "content": {"application/json": {"schema": {"type": "object"}}}},
                "400": {"description": "Invalid arguments"},
                "401": {"description": "Authentication required"},
            },
        }}
    document = {
        "openapi": "3.0.3",
        "info": {"title": "Volt synthetic business API", "version": "1.0.0"},
        "paths": paths,
    }
    output = ROOT / "tools" / "openapi.json"
    output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(paths)} operations: {output}")


if __name__ == "__main__":
    main()
