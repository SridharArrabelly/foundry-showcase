"""Render support decisions from this run's tool evidence before emitting text."""

import json
import logging
import re
from collections.abc import Mapping

from agent_framework import AgentContext, AgentMiddleware, AgentResponse, AgentResponseUpdate, Content, Message, ResponseStream

from response_contract import Citation, SupportResponse

logger = logging.getLogger(__name__)
PREFIX = "volt-business-tools___"
ELIGIBILITY = PREFIX + "getReturnWarrantyEligibility"
RECALL = PREFIX + "getRecallNotices"
POLICIES = {
    "VOLT-REPLACEMENT-2026-11": "Volt & Co synthetic replacement policy",
    "SYNTHETIC-RECALL-001": "Volt & Co synthetic recall notice",
}
ANSWERS = {
    "eligible": "Contact human support for a replacement assessment. The eligibility service reports eligible for assessment, not an approved replacement.",
    "ineligible": "Contact human support to discuss a separate warranty assessment. The eligibility service reports ineligible for a standard return.",
    "needs_order": "Please provide the order ID before an eligibility assessment.",
    "needs_batch": "Please provide the batch code printed on the device. Missing batch information cannot establish recall or replacement eligibility.",
    "unknown": "Human support needs to verify the missing record. The available evidence does not establish a conclusion.",
    "recalled": "Follow the recall notice and contact human support. The register identifies this batch as recalled.",
    "no_recall": "The register has no recall entry for this exact batch. This is not a general guarantee of product safety.",
}
NO_ACTION = "No ticket, handoff, refund, shipment or order change has been performed."


def object_value(value):
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, str):
        decoder = json.JSONDecoder()
        objects = []
        remaining = value.strip()
        while remaining:
            item, end = decoder.raw_decode(remaining)
            objects.append(item)
            remaining = remaining[end:].strip()
        if objects and isinstance(objects[0], dict) and all(item == objects[0] for item in objects):
            return objects[0]
    # MCP can supply both text and structured content for the same result.
    if isinstance(value, list) and value:
        objects = [object_value(item.text if isinstance(item, Content) else item) for item in value]
        if all(item == objects[0] for item in objects):
            return objects[0]
    raise ValueError("Expected one unambiguous tool-result object.")


def request_arguments_match(name, arguments, query):
    fields = {"batch": r"\bCH-\d{4}\b"}
    if name == ELIGIBILITY:
        fields["order_id"] = r"\bVC-\d{5}\b"
    else:
        fields["product_id"] = r"\bVC-[A-Z]\d+\b"
    for field, pattern in fields.items():
        supplied = {value.upper() for value in re.findall(pattern, query, re.I)}
        actual = arguments.get(field)
        if actual is not None and not isinstance(actual, str):
            return False
        actual = actual.strip().upper() if actual else None
        if len(supplied) > 1 or ({actual} if actual else set()) != supplied:
            return False
    return True


def supported_response(messages, query):
    """Never use historical input messages or the model's answer as tool evidence."""
    contents = [content for message in messages for content in message.contents]
    calls = [c for c in contents if c.type == "function_call" and c.name in (ELIGIBILITY, RECALL)]
    eligibility_intent = bool(re.search(r"\breplac\w*|\breturn\b|\beligib\w*|\bassess\w*|\bescalat\w*|\bhandoff\b", query, re.I))
    operation = ELIGIBILITY if eligibility_intent else RECALL
    selected = [c for c in calls if c.name == operation]
    evidence = []
    try:
        if not selected or len({c.call_id for c in selected}) != len(selected):
            raise ValueError("Missing or duplicated authoritative tool call.")
        for call in selected:
            results = [c for c in contents if c.type == "function_result" and c.call_id == call.call_id]
            if not call.call_id or call.exception or len(results) != 1 or results[0].exception:
                raise ValueError("Tool call did not produce exactly one successful result.")
            arguments = object_value(call.arguments)
            body = object_value(results[0].result)
            if not request_arguments_match(operation, arguments, query):
                raise ValueError("Tool arguments do not match identifiers supplied in this request.")
            allowed = {"eligible", "ineligible", "needs_order", "needs_batch", "unknown"} if operation == ELIGIBILITY else {"recalled", "no_recall", "needs_batch", "unknown"}
            if body.get("synthetic") is not True or "error" in body or body.get("status") not in allowed:
                raise ValueError("Tool result is not a valid synthetic business outcome.")
            if operation == ELIGIBILITY and body.get("action_performed") is not False:
                raise ValueError("Eligibility evidence does not establish the read-only boundary.")
            for field in ("product_id", "batch", "order_id"):
                if body.get(field) is not None and str(body[field]).upper() != str(arguments.get(field)).upper():
                    raise ValueError("Tool output identifies different request arguments.")
            evidence.append((arguments, body))
        arguments, body = evidence[0]
        if any(other != evidence[0] for other in evidence):
            raise ValueError("Authoritative tool results conflict within this request.")
        references = [body.get(key) for key in ("policy_reference", "recall_reference", "reference")]
        citations = [Citation(reference=key, title=POLICIES[key]) for key in dict.fromkeys(references) if key in POLICIES]
        return SupportResponse(
            answer=f"{ANSWERS[body['status']]} {NO_ACTION}",
            decision=body["status"], product_id=arguments.get("product_id"),
            batch=arguments.get("batch"), citations=citations, synthetic=True,
        )
    except (ValueError, TypeError) as error:
        logger.warning("volt.contract rejected evidence: %s", error)
        return SupportResponse(
            answer=f"I cannot verify the required business evidence for this request. Please contact human support. {NO_ACTION}",
            decision="unavailable", product_id=None, batch=None, citations=[], synthetic=True,
        )


class EvidenceContract(AgentMiddleware):
    """Buffer model text; retain actual tool events, then emit one validated answer."""

    async def process(self, context: AgentContext, call_next):
        query = next((message.text for message in reversed(context.messages) if message.role == "user"), "")
        await call_next()
        if context.stream:
            source = context.result
            if not isinstance(source, ResponseStream):
                raise TypeError("Expected the framework response stream.")

            async def guarded():
                updates = [update async for update in source]
                result = AgentResponse.from_updates(updates)
                answer = supported_response(result.messages, query)
                for update in updates:
                    evidence = [c for c in update.contents if c.type in ("function_call", "function_result", "usage")]
                    if evidence:
                        yield AgentResponseUpdate(
                            contents=evidence, role=update.role, message_id=update.message_id,
                            response_id=update.response_id, agent_id=update.agent_id,
                        )
                yield AgentResponseUpdate(
                    contents=[Content.from_text(answer.model_dump_json())],
                    role="assistant", response_id=result.response_id,
                    message_id="volt-validated-answer", finish_reason="stop",
                )

            context.result = ResponseStream(
                guarded(), finalizer=lambda updates: AgentResponse.from_updates(updates, output_format_type=SupportResponse),
            )
        else:
            result = context.result
            if not isinstance(result, AgentResponse):
                raise TypeError("Expected the framework agent response.")
            answer = supported_response(result.messages, query)
            messages = [
                Message(role=m.role, contents=[c for c in m.contents if c.type in ("function_call", "function_result")])
                for m in result.messages if any(c.type in ("function_call", "function_result") for c in m.contents)
            ]
            context.result = AgentResponse(
                messages=[*messages, Message(role="assistant", contents=[answer.model_dump_json()])],
                response_id=result.response_id, usage_details=result.usage_details,
                value=answer, response_format=SupportResponse, finish_reason="stop",
            )
