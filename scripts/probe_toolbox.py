"""Verify domain outcomes, not merely successful MCP transport."""

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
from azure.identity.aio import DefaultAzureCredential
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

CASES = [
    ("getRecallNotices", {"product_id": "VC-C65", "batch": "CH-0722"}, "recalled"),
    ("getRecallNotices", {"product_id": "VC-C65"}, "needs_batch"),
    ("getRecallNotices", {"product_id": "VC-C65", "batch": "CH-9999"}, "unknown"),
    ("getOrderStatus", {"order_id": "VC-10482"}, "delivered"),
    ("getReturnWarrantyEligibility", {"order_id": "VC-10482", "batch": "CH-0722"}, "eligible"),
    ("getReturnWarrantyEligibility", {"batch": "CH-0722"}, "needs_order"),
]


class FoundryAuth(httpx.Auth):
    def __init__(self, credential: DefaultAzureCredential):
        self.credential = credential

    async def async_auth_flow(self, request):
        token = await self.credential.get_token("https://ai.azure.com/.default")
        request.headers["Authorization"] = f"Bearer {token.token}"
        yield request


async def probe(endpoint: str, out: Path) -> None:
    records = []
    async with DefaultAzureCredential() as credential, httpx.AsyncClient(
        auth=FoundryAuth(credential), timeout=120
    ) as http:
        async with streamable_http_client(endpoint, http_client=http) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = sorted(tool.name for tool in tools.tools)
                expected_names = sorted({
                    "volt-policy-knowledge___knowledge_base_retrieve",
                    *("volt-business-tools___" + case[0] for case in CASES),
                })
                if names != expected_names:
                    raise RuntimeError(f"Unexpected toolbox surface: {names}")
                for name, arguments, expected in CASES:
                    result = await session.call_tool("volt-business-tools___" + name, arguments)
                    texts = [content.text for content in result.content if content.type == "text"]
                    body = json.loads(texts[0]) if texts else None
                    passed = (
                        not result.isError and isinstance(body, dict)
                        and body.get("synthetic") is True
                        and body.get("status") == expected and "error" not in body
                    )
                    records.append({
                        "tool": name, "arguments": arguments, "expected_status": expected,
                        "passed": passed, "result": result.model_dump(mode="json"),
                    })
                    print(f"{'PASS' if passed else 'FAIL'} {name}: expected {expected}; received {body}")
                query = (
                    "For Volt Charge 65 batch CH-0722 and order VC-10482 outside the normal return window, "
                    "retrieve both the recall notice and replacement policy, with their reference identifiers."
                )
                knowledge = await session.call_tool(
                    "volt-policy-knowledge___knowledge_base_retrieve", {"query_variants": [query]}
                )
                references = set()
                for content in knowledge.content:
                    if content.type == "text":
                        value = json.loads(content.text)
                        if isinstance(value, dict) and value.get("kind") == "reference":
                            source = value.get("sourceData", {})
                            if source.get("content") and source.get("id") == source.get("reference"):
                                references.add(source["reference"])
                expected_references = {"VOLT-REPLACEMENT-2026-11", "SYNTHETIC-RECALL-001"}
                passed = not knowledge.isError and expected_references.issubset(references)
                records.append({
                    "tool": "knowledge_base_retrieve", "passed": passed,
                    "expected_references": sorted(expected_references),
                    "observed_references": sorted(references),
                    "result": knowledge.model_dump(mode="json"),
                })
                print(f"{'PASS' if passed else 'FAIL'} IQ source documents: {sorted(references)}")
    evidence = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint, "tool_names": names, "cases": records,
        "passed": all(record["passed"] for record in records),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    if not evidence["passed"]:
        raise RuntimeError(f"Business-tool verification failed; see {out}")
    print(f"Verified {len(records)} live cases; evidence: {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    parsed = urlparse(args.project_endpoint)
    if (
        parsed.scheme != "https" or not parsed.hostname
        or not parsed.hostname.endswith(".services.ai.azure.com")
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or not parsed.path.startswith("/api/projects/") or args.version < 1
    ):
        parser.error("Provide a Microsoft Foundry project HTTPS endpoint and a positive toolbox version.")
    endpoint = (
        f"{args.project_endpoint.rstrip('/')}/toolboxes/volt-support-tools"
        f"/versions/{args.version}/mcp?api-version=v1"
    )
    asyncio.run(probe(endpoint, args.out))


if __name__ == "__main__":
    main()
