import json
import logging

import azure.functions as func
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from support import order_status, replacement_eligibility
from volt.domain import check_compatibility, recall_notices, search_catalog

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
logger = logging.getLogger(__name__)


class Arguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CatalogArguments(Arguments):
    category: str = "charger"
    max_price_eur: float = Field(default=1000, ge=0, allow_inf_nan=False)


class CompatibilityArguments(Arguments):
    product_id: str
    device_id: str


class RecallArguments(Arguments):
    product_id: str = Field(description="Volt product identifier, for example VC-C65.")
    batch: str | None = Field(default=None, description="Batch printed on the device. Omit when unknown; never infer.")


class OrderArguments(Arguments):
    order_id: str = Field(description="Synthetic customer-supplied order identifier, for example VC-10482.")


class EligibilityArguments(Arguments):
    order_id: str | None = Field(default=None, description="Customer-supplied synthetic order identifier. Omit when unknown.")
    batch: str | None = Field(default=None, description="Batch printed on the device. Omit when unknown; never infer.")


OPERATIONS = {
    "searchProductCatalog": (CatalogArguments, search_catalog),
    "checkCompatibility": (CompatibilityArguments, check_compatibility),
    "getRecallNotices": (RecallArguments, recall_notices),
    "getOrderStatus": (OrderArguments, order_status),
    "getReturnWarrantyEligibility": (EligibilityArguments, replacement_eligibility),
}


@app.route(route="tools/{operation}/{product_id?}", methods=["GET", "POST"])
def business_tool(req: func.HttpRequest) -> func.HttpResponse:
    operation = req.route_params.get("operation", "")
    if operation not in OPERATIONS:
        logger.warning("Rejected unknown business operation")
        return func.HttpResponse(
            json.dumps({"error": "unknown_operation"}),
            status_code=404, mimetype="application/json",
        )
    schema, handler = OPERATIONS[operation]
    try:
        payload = dict(req.params) if req.method == "GET" else req.get_json()
        if "product_id" in req.route_params:
            if req.method != "GET" or operation != "getRecallNotices" or "product_id" in payload:
                logger.warning("Rejected ambiguous product identifier for operation %s", operation)
                return func.HttpResponse(
                    json.dumps({"error": "invalid_route_arguments", "operation": operation}),
                    status_code=400, mimetype="application/json",
                )
            payload["product_id"] = req.route_params["product_id"]
        arguments = schema.model_validate(payload)
    except ValidationError as exc:
        errors = exc.errors(include_url=False, include_context=False, include_input=False)
        logger.warning("Invalid arguments for business operation %s: %s", operation, errors)
        return func.HttpResponse(
            json.dumps({"error": "invalid_arguments", "operation": operation, "details": errors}),
            status_code=400, mimetype="application/json",
        )
    except ValueError:
        logger.warning("Invalid JSON for business operation %s", operation)
        return func.HttpResponse(
            json.dumps({"error": "invalid_json", "operation": operation}),
            status_code=400, mimetype="application/json",
        )
    result = handler(**arguments.model_dump())
    logger.info("volt.tool operation=%s status=%s", operation, result.get("status", "ok"))
    return func.HttpResponse(json.dumps(result), mimetype="application/json")
