"""Foundry Invocations adapter for a constrained GitHub Copilot SDK agent."""

import asyncio
import hashlib
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Literal

from azure.ai.agentserver.invocations import InvocationAgentServerHost
from azure.identity import DefaultAzureCredential
from copilot import CopilotClient, ProviderConfig, define_tool
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.context import get_current
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from volt.domain import VARIANTS, call_tool

load_dotenv(override=False)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("volt")
ROOT = Path(__file__).parent
CONTRACT = (ROOT / "instructions.md").read_text(encoding="utf-8")
VARIANT = os.environ.get("VOLT_VARIANT", "improved")
if VARIANT not in VARIANTS:
    raise ValueError(f"VOLT_VARIANT must be one of {VARIANTS}")

if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    logger.warning("No Application Insights connection string: inspect host-provided telemetry configuration.")

tracer = trace.get_tracer("volt.showcase", "1.0.0")
app = InvocationAgentServerHost()


class Parameters(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Search(Parameters):
    category: str = "charger"
    max_price_eur: float = Field(default=1000, ge=0, allow_inf_nan=False)


class Compatibility(Parameters):
    product_id: str
    device_id: str


class Recall(Parameters):
    product_id: str
    batch: str | None = None


class Input(Parameters):
    input: str = Field(min_length=1, max_length=4000)


class Answer(Parameters):
    decision: Literal["recommend", "no_option", "compatible", "incompatible",
                      "recalled", "no_recall", "needs_batch", "unknown", "refuse"]
    answer: str = Field(min_length=1, max_length=4000)
    product_id: str | None
    batch: str | None


def build_tools(calls: list[dict]) -> list:
    # SDK callbacks arrive on a separate RPC task; preserve the invocation parent.
    parent_context = get_current()
    specs = [
        ("searchProductCatalog", Search, "Search the fictional catalog by category and maximum EUR price."),
        ("checkCompatibility", Compatibility, "Check a fictional charger against the device's required power."),
        ("getRecallNotices", Recall, "Look up a fictional product and batch. Use null if no batch was supplied."),
    ]
    tools = []
    for name, params_type, description in specs:
        def make_handler(tool_name):
            def handler(params, _invocation):
                arguments = params.model_dump()
                with tracer.start_as_current_span(f"execute_tool {tool_name}", context=parent_context) as span:
                    span.set_attribute("gen_ai.operation.name", "execute_tool")
                    span.set_attribute("gen_ai.tool.name", tool_name)
                    span.set_attribute("gen_ai.tool.call.arguments", json.dumps(arguments))
                    result = call_tool(tool_name, arguments, VARIANT)
                    span.set_attribute("gen_ai.tool.call.result", json.dumps(result))
                    calls.append({"name": tool_name, "arguments": arguments, "result": result})
                    return json.dumps(result)
            return handler
        tools.append(define_tool(
            name, description=description, params_type=params_type,
            handler=make_handler(name), skip_permission=True, defer="never",
        ))
    return tools


async def run_agent(prompt: str, invocation_id: str) -> dict:
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    if not endpoint or not model:
        raise RuntimeError("FOUNDRY_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME are required")
    calls: list[dict] = []
    usage: list[dict] = []
    started = time.monotonic()
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    provider = ProviderConfig(
        type="openai", base_url=endpoint.rstrip("/") + "/openai/v1", wire_api="responses",
        bearer_token_provider=lambda _request: credential.get_token("https://ai.azure.com/.default").token,
    )
    try:
        with tracer.start_as_current_span("invoke_agent volt-assistant") as span:
            span.set_attribute("gen_ai.operation.name", "invoke_agent")
            span.set_attribute("gen_ai.agent.name", "volt-assistant")
            span.set_attribute("volt.variant", VARIANT)
            span.set_attribute("volt.invocation_id", invocation_id)
            span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "user", "content": prompt}]))
            sdk_environment = {**os.environ, "COPILOT_TELEMETRY_DISABLED": "true"}
            async with CopilotClient(
                mode="empty", use_logged_in_user=False, env=sdk_environment,
                base_directory=str(Path.home() / ".volt-runtime"),
            ) as client:
                tools = build_tools(calls)
                async with await client.create_session(
                    model=model, provider=provider, tools=tools,
                    available_tools=[tool.name for tool in tools],
                    system_message={"mode": "replace", "content": CONTRACT},
                    streaming=False, enable_skills=False,
                    enable_config_discovery=False, skip_custom_instructions=True,
                ) as session:
                    def collect_usage(event):
                        if event.type.value == "assistant.usage":
                            raw = event.to_dict()["data"]
                            usage.append({k: v for k, v in raw.items()
                                          if "token" in k.lower() and isinstance(v, (int, float))})
                    session.on(collect_usage)
                    event = await session.send_and_wait(prompt, timeout=120)
                    if event is None:
                        raise RuntimeError("The harness completed without an assistant response")
                    text = event.data.content.strip()
                    if text.startswith("```") and text.endswith("```"):
                        text = "\n".join(text.splitlines()[1:-1])
                    output = Answer.model_validate_json(text).model_dump()
            span.set_attribute("gen_ai.output.messages", json.dumps([{"role": "assistant", "content": output["answer"]}]))
            span.set_attribute("volt.decision", output["decision"])
            trace_id = f"{span.get_span_context().trace_id:032x}"
            return {
                "mode": "live-copilot-sdk", "synthetic_data": True,
                "hosting": "foundry" if os.environ.get("FOUNDRY_AGENT_SESSION_ID") else "local",
                "invocation_id": invocation_id, "trace_id": trace_id if int(trace_id, 16) else None,
                "variant": VARIANT, "model": model,
                "contract_sha256": hashlib.sha256(CONTRACT.encode()).hexdigest(),
                "output": output, "tool_calls": calls, "usage": usage,
                "duration_ms": round((time.monotonic() - started) * 1000),
            }
    finally:
        credential.close()


@app.invoke_handler
async def handle_invoke(request: Request) -> Response:
    invocation_id = getattr(request.state, "invocation_id", str(uuid.uuid4()))
    try:
        data = Input.model_validate(await request.json())
        if not data.input.strip():
            raise ValueError("input cannot be blank")
    except (ValidationError, json.JSONDecodeError, ValueError) as error:
        logger.warning("Invalid invocation %s: %s", invocation_id, type(error).__name__)
        return JSONResponse({"error": "invalid_request", "message": "Provide a nonblank input string of at most 4000 characters."}, status_code=400)
    try:
        async with asyncio.timeout(150):
            return JSONResponse(await run_agent(data.input, invocation_id))
    except TimeoutError:
        logger.exception("Invocation timed out: %s", invocation_id)
        return JSONResponse({"error": "timeout", "invocation_id": invocation_id}, status_code=504)
    except (RuntimeError, ValidationError) as error:
        logger.exception("Invocation failed: %s (%s)", invocation_id, type(error).__name__)
        return JSONResponse({"error": "agent_failed", "invocation_id": invocation_id}, status_code=502)


if __name__ == "__main__":
    app.run()
