"""Capture real hosted responses with checked version lineage for native evaluation."""

import argparse
import json
import re
import sys
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import VersionRefIndicator
from azure.identity import DefaultAzureCredential

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evaluations"))
from business_contract import grade
from observed_tools import successful_business_tools


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--agent", default="volt-support")
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--reuse-response", action="append", default=[], metavar="CASE_ID=RESPONSE_ID")
    parser.add_argument("--pause-seconds", type=float, default=20)
    parser.add_argument("--case", help="Run one selected case for the live walkthrough; the full release gate still requires all cases.")
    parser.add_argument("--fresh", action="store_true", help="Require a new output directory and prohibit recorded-response reuse.")
    args = parser.parse_args()
    if args.pause_seconds < 0:
        parser.error("Pause must not be negative.")
    cases = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [case["id"] for case in cases]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[a-z0-9-]+", value) for value in ids):
        raise ValueError("Case IDs must be unique lowercase identifiers.")
    if args.case:
        if args.case not in ids:
            parser.error(f"Unknown case: {args.case}")
        cases = [case for case in cases if case["id"] == args.case]
        ids = [args.case]
    if args.fresh and args.reuse_response:
        parser.error("A fresh live invocation cannot reuse a recorded response.")
    if args.fresh and args.out.exists():
        raise FileExistsError("Fresh live capture requires a new output directory, not cached responses.")
    reused = dict(value.split("=", 1) for value in args.reuse_response)
    if not set(reused).issubset(ids):
        raise ValueError("A reused response must identify a case in this dataset.")
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential, allow_preview=True
    ) as project, project.get_openai_client(
        agent_name=args.agent, timeout=180, max_retries=0
    ) as client:
        version = project.agents.get_version(agent_name=args.agent, agent_version=args.expected_version)
        code_hash = version.definition.code_configuration.content_hash
        for case in cases:
            path = args.out / f"{case['id']}.json"
            was_cached = path.exists()
            if was_cached:
                record = json.loads(path.read_text(encoding="utf-8"))
                if (
                    record["case"] != case or record["project_endpoint"] != args.project_endpoint
                    or record.get("code_content_hash") != code_hash
                ):
                    raise ValueError(f"Cached case differs from the requested inputs: {path}")
                response = record["response"]
                output_text = record["output_text"]
                print(f"Using captured response for {case['id']}", flush=True)
            else:
                if case["id"] in reused:
                    result = client.responses.retrieve(reused[case["id"]])
                    inputs = list(client.responses.input_items.list(result.id))
                    user_texts = [
                        content["text"]
                        for item in inputs
                        for data in [item.model_dump(mode="json")]
                        if data.get("role") == "user"
                        for content in data.get("content", [])
                        if content.get("type") == "input_text"
                    ]
                    if not user_texts or user_texts[-1] != case["query"]:
                        raise ValueError("Existing response input does not match the selected case.")
                else:
                    session = project.agents.create_session(
                        agent_name=args.agent,
                        version_indicator=VersionRefIndicator(agent_version=args.expected_version),
                    )
                    if session.version_indicator.agent_version != args.expected_version:
                        raise RuntimeError("The created session is not bound to the requested version.")
                    conversation = client.conversations.create()
                    result = client.responses.create(
                        input=case["query"], conversation={"id": conversation.id},
                        extra_body={"agent_session_id": session.agent_session_id},
                    )
                    if result.model_dump().get("agent_session_id") != session.agent_session_id:
                        raise RuntimeError("The response did not use the requested version-bound session.")
                response = result.model_dump(mode="json")
                output_text = result.output_text
                record = {
                    "case": case, "project_endpoint": args.project_endpoint,
                    "code_content_hash": code_hash, "response": response,
                    "output_text": output_text,
                }
            reference = response.get("agent_reference") or {}
            if reference.get("name") != args.agent or reference.get("version") != args.expected_version:
                raise RuntimeError(f"Unexpected serving version in {path}; refusing to mislabel the result.")
            if response.get("status") != "completed":
                failure_dir = args.out / "failed-attempts"
                failure_dir.mkdir(exist_ok=True)
                failure_path = failure_dir / f"{case['id']}-{time.time_ns()}.json"
                failure_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                raise RuntimeError(f"Hosted response did not complete; evidence saved to {failure_path}")
            if not path.exists():
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            row = {
                **case, "response": output_text,
                "observed_tools": json.dumps(successful_business_tools(response)),
                "response_id": response["id"], "agent_name": args.agent,
                "agent_version": reference["version"], "code_content_hash": code_hash,
            }
            row["local_business_score"] = grade({}, row)
            rows.append(row)
            print(f"{case['id']}: score={row['local_business_score']} response={response['id']}", flush=True)
            if args.case:
                print(output_text, flush=True)
            (args.out / "captured.jsonl").write_text(
                "".join(json.dumps(item) + "\n" for item in rows), encoding="utf-8"
            )
            if not was_cached and case["id"] not in reused and len(rows) < len(cases):
                time.sleep(args.pause_seconds)
    print(f"Captured {len(rows)} responses; business passes: {sum(row['local_business_score'] for row in rows):g}/{len(rows)}")


if __name__ == "__main__":
    main()
