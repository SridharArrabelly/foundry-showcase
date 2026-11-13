import asyncio
import json
import sys
from pathlib import Path

import pytest
from agent_framework import BaseChatClient, ChatResponse, ChatResponseUpdate, Content, FunctionInvocationLayer, Message, ResponseStream, tool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence_contract import ELIGIBILITY, RECALL, NO_ACTION, supported_response
from main import create_support_agent

QUERY = "Check replacement eligibility for order VC-10482, batch CH-0722."
ARGUMENTS = {"order_id": "VC-10482", "batch": "CH-0722"}


def outcome(status="eligible"):
    return {"synthetic": True, "status": status, "action_performed": False,
            "policy_reference": "VOLT-REPLACEMENT-2026-11"}


def evidence(name=ELIGIBILITY, arguments=None, body=None, call_id="call-1"):
    return [
        Message(role="assistant", contents=[Content.from_function_call(
            call_id, name, arguments=arguments if arguments is not None else ARGUMENTS)]),
        Message(role="tool", contents=[Content.from_function_result(
            call_id, result=body if body is not None else outcome())]),
    ]


@pytest.mark.parametrize("status", ["eligible", "ineligible", "needs_batch", "needs_order", "unknown"])
def test_authoritative_status_is_preserved_and_no_action_is_claimed(status):
    answer = supported_response(evidence(body=outcome(status)), QUERY)
    assert answer.decision == status
    assert NO_ACTION in answer.answer
    assert "I'm escalating" not in answer.answer


def test_recall_intent_does_not_inherit_eligibility_decision():
    messages = evidence() + evidence(
        RECALL, {"product_id": "VC-C65", "batch": "CH-0722"},
        {"synthetic": True, "status": "recalled", "product_id": "VC-C65",
         "batch": "CH-0722", "reference": "SYNTHETIC-RECALL-001"}, "recall-1")
    answer = supported_response(messages, "Check recall VC-C65 CH-0722")
    assert answer.decision == "recalled"
    assert answer.citations[0].reference == "SYNTHETIC-RECALL-001"


@pytest.mark.parametrize("messages", [
    [], evidence(arguments={"order_id": "VC-99999", "batch": "CH-0722"}),
    evidence(body={"synthetic": True, "error": "failed", "status": "eligible"}),
    evidence() + evidence(body=outcome("ineligible"), call_id="call-2"),
    evidence() + evidence(), evidence()[:1],
    evidence(body={"synthetic": True, "status": "eligible", "action_performed": True}),
])
def test_missing_wrong_failed_or_conflicting_evidence_fails_closed(messages, caplog):
    assert supported_response(messages, QUERY).decision == "unavailable"
    assert "rejected evidence" in caplog.text


def test_cannot_invent_missing_identifiers_and_mcp_duplicate_content_is_supported():
    assert supported_response(evidence(), "Check replacement eligibility, no order or batch supplied").decision == "unavailable"
    result = [Content.from_text(json.dumps(outcome())), Content.from_text(json.dumps(outcome()))]
    assert supported_response(evidence(body=result), QUERY).decision == "eligible"


class ScriptedClient(FunctionInvocationLayer, BaseChatClient):
    def _inner_get_response(self, *, messages, stream, options, **kwargs):
        has_result = any(c.type == "function_result" for m in messages for c in m.contents)
        if has_result:
            content = Content.from_text(json.dumps({
                "answer": "I'm escalating this to human support.",
                "decision": "recommendation", "product_id": None, "batch": "CH-0722",
                "citations": [], "synthetic": True,
            }))
        else:
            content = Content.from_function_call("real-tool-call", ELIGIBILITY, arguments=ARGUMENTS)
        if stream:
            async def updates():
                yield ChatResponseUpdate(
                    contents=[content], role="assistant", message_id="answer" if has_result else "tool-call",
                    response_id="model-2" if has_result else "model-1",
                )
            return ResponseStream(updates(), finalizer=ChatResponse.from_updates)
        async def response():
            return ChatResponse(messages=[Message(role="assistant", contents=[content])])
        return response()


@pytest.mark.parametrize("stream", [False, True])
def test_real_agent_tool_loop_and_registered_boundary_never_emit_unvalidated_text(stream):
    async def exercise():
        @tool(name=ELIGIBILITY)
        def eligibility(order_id: str, batch: str) -> dict:
            """Read the synthetic eligibility result."""
            assert order_id == "VC-10482" and batch == "CH-0722"
            return outcome()
        agent = create_support_agent(ScriptedClient(), [eligibility], "Synthetic test.")
        if stream:
            response = agent.run(QUERY, stream=True)
            updates = [update async for update in response]
            assert all("escalating" not in c.text for u in updates for c in u.contents if c.type == "text")
            result = await response.get_final_response()
        else:
            result = await agent.run(QUERY)
        answer = json.loads(result.text)
        assert answer["decision"] == "eligible"
        assert NO_ACTION in answer["answer"]
        assert any(c.type == "function_result" for m in result.messages for c in m.contents)
    asyncio.run(exercise())


def test_responses_host_http_stream_contains_only_the_enforced_customer_answer(tmp_path, monkeypatch):
    from agent_framework_foundry_hosting import ResponsesHostServer
    from starlette.testclient import TestClient

    @tool(name=ELIGIBILITY)
    def eligibility(order_id: str, batch: str) -> dict:
        """Read synthetic eligibility."""
        return outcome()

    monkeypatch.setenv("AGENTSERVER_STATE_ROOT", str(tmp_path))
    monkeypatch.delenv("FOUNDRY_PROJECT_ENDPOINT", raising=False)
    host = ResponsesHostServer(
        create_support_agent(ScriptedClient(), [eligibility], "Synthetic test."),
        configure_observability=None,
    )
    with TestClient(host) as client:
        response = client.post("/responses", json={"input": QUERY, "stream": True, "store": False})
        assert response.status_code == 200, response.text
        assert "escalating" not in response.text
        assert "No ticket" in response.text
        assert "response.completed" in response.text
        response = client.post("/responses", json={"input": QUERY, "stream": False, "store": False})
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "completed"
        function_calls = [item for item in payload["output"] if item["type"] == "function_call"]
        function_results = [item for item in payload["output"] if item["type"] == "function_call_output"]
        assert len(function_calls) == len(function_results) == 1
        assert function_calls[0]["call_id"] == function_results[0]["call_id"]
        assert function_calls[0]["status"] == function_results[0]["status"] == "completed"
        assert json.loads(function_results[0]["output"])["status"] == "eligible"
