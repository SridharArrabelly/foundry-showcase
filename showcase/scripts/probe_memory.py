"""Verify one authenticated caller's Memory lifecycle using native item receipts."""

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import VersionRefIndicator
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "volt-support" / "src" / "agent-framework-agent-basic-responses"))
from preferences import PREFERENCE, STORE


def tool_result(response: dict, name: str) -> dict:
    calls = [
        item for item in response["output"]
        if item.get("type") == "function_call" and item.get("name") == name
        and item.get("status") == "completed"
    ]
    for call in calls:
        for item in response["output"]:
            if (
                item.get("type") == "function_call_output"
                and item.get("call_id") == call["call_id"] and item.get("status") == "completed"
            ):
                try:
                    result = json.loads(item["output"])
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"{name} did not return a verifiable native receipt.") from exc
                if isinstance(result, dict) and result.get("synthetic") is True:
                    return result
    raise RuntimeError(f"No successful native {name} receipt was observed.")


def wait_for_item(project, memory_id: str, *, present: bool):
    deadline = time.monotonic() + 60
    while True:
        try:
            item = project.beta.memory_stores.get_memory(STORE, memory_id)
        except ResourceNotFoundError:
            if not present:
                return None
        else:
            if present:
                return item
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Native memory item did not become {'visible' if present else 'absent'} within 60 seconds.")
        time.sleep(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records = []
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential, allow_preview=True
    ) as project, project.get_openai_client(
        agent_name="volt-support", timeout=180, max_retries=0
    ) as client:
        def invoke(name: str, prompt: str) -> dict:
            session = project.agents.create_session(
                agent_name="volt-support",
                version_indicator=VersionRefIndicator(agent_version=args.expected_version),
            )
            if session.version_indicator.agent_version != args.expected_version:
                raise RuntimeError("The created session is not bound to the requested version.")
            conversation = client.conversations.create()
            response = client.responses.create(
                input=prompt, conversation={"id": conversation.id},
                extra_body={"agent_session_id": session.agent_session_id},
            )
            data = response.model_dump(mode="json")
            reference = data.get("agent_reference") or {}
            binding = project.agents.get_session("volt-support", session.agent_session_id)
            record = {
                "step": name, "input": prompt, "response": data, "output_text": response.output_text,
                "requested_session_id": session.agent_session_id,
                "session_version_indicator": binding.version_indicator.as_dict(),
            }
            (args.out / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            if (
                binding.version_indicator.agent_version != args.expected_version
                or data.get("agent_session_id") != session.agent_session_id
                or reference.get("name") != "volt-support" or data.get("status") != "completed"
            ):
                raise RuntimeError(f"Unexpected session binding or incomplete response for {name}.")
            if reference.get("version") != args.expected_version:
                warnings.warn(
                    f"{name}: response agent_reference reports v{reference.get('version')}, "
                    f"but native session readback is pinned to v{args.expected_version}. "
                    "This preview metadata discrepancy is preserved in the evidence.",
                    RuntimeWarning,
                )
            records.append(record)
            print(f"{name}: {response.output_text}", flush=True)
            return data

        remembered = invoke(
            "remember",
            "For this synthetic demonstration, please remember only this response-style preference: "
            "I prefer concise responses with the next step first. Do not store personal or order information.",
        )
        receipt = tool_result(remembered, "remember_response_style")
        memory_id = receipt["memory_id"]
        item = wait_for_item(project, memory_id, present=True)
        if item.content != PREFERENCE or item.kind != "user_profile":
            raise RuntimeError("The native memory item does not match the permitted preference.")
        stored = item.as_dict()
        invoke(
            "recall",
            "What response-style preference, if any, did I explicitly ask you to remember in a "
            "previous conversation? Distinguish saved memory from your default style instructions.",
        )
        forgotten = invoke(
            "forget",
            "Please forget my saved concise, next-step-first response-style preference. "
            "Do not delete any unrelated information.",
        )
        deleted = tool_result(forgotten, "forget_response_style")
        if memory_id not in deleted.get("deleted_memory_ids", []):
            raise RuntimeError("The forget receipt did not identify the remembered item.")
        wait_for_item(project, memory_id, present=False)
        invoke(
            "after-forget",
            "What response-style preference, if any, is saved for me now? "
            "Do not infer a saved preference from your default instructions.",
        )
    conversations = [record["response"].get("conversation") for record in records]
    conversation_ids = [value.get("id") for value in conversations if isinstance(value, dict)]
    if len(conversation_ids) != len(records) or len(set(conversation_ids)) != len(records):
        raise RuntimeError("Distinct conversation IDs were not observed; do not claim cross-conversation proof.")
    summary = {
        "kind": "single-authenticated-caller-memory-proof",
        "session_bound_version": args.expected_version,
        "response_reported_versions": sorted({
            record["response"]["agent_reference"]["version"] for record in records
        }),
        "memory_item": stored, "memory_deleted": True,
        "distinct_conversation_ids": conversation_ids,
        "distinct_session_ids": [record["response"]["agent_session_id"] for record in records],
        "response_ids": [record["response"]["id"] for record in records],
        "cross_identity_verified": False,
        "notice": "Native item persistence/deletion verified. Review the recorded model answers separately.",
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print("Native persistence and deletion verified across distinct conversations; second-identity proof remains pending.")


if __name__ == "__main__":
    main()
