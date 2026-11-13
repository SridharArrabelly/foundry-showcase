"""Finalize a promotion only after independent, complete native DEMO evaluation."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from evaluate_captures import HEADERS, ROOT, contract_source, evaluator_name
from promote_demo import DEMO, validate_quality
from score_action_claims import verify_action_gate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--runtime-evaluation", type=Path, required=True)
    parser.add_argument("--action-judgments", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    evaluation = json.loads(args.runtime_evaluation.read_text(encoding="utf-8"))
    if receipt["target_project"] != DEMO:
        raise ValueError("This verifier only targets the approved isolated DEMO project.")
    contract_version = receipt.get("contract_version", "v1")
    filename = "volt-regression-v2.jsonl" if contract_version == "v2" else "volt-regression.jsonl"
    path = ROOT / "agent" / "src" / ".foundry" / "datasets" / filename
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    grader_hash = hashlib.sha256(contract_source(contract_version).read_text(encoding="utf-8").encode()).hexdigest()
    if contract_version == "v2":
        if not args.action_judgments:
            raise ValueError("DEMO v2 verification also requires independent action judgments.")
        actions = json.loads(args.action_judgments.read_text(encoding="utf-8"))
        verify_action_gate(actions, cases, receipt["source_commit"], receipt["package_sha256"])
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=DEMO, credential=credential, allow_preview=True
    ) as project, project.get_openai_client(default_headers=HEADERS) as client:
        version = project.agents.get_version("volt-support", receipt["agent_version"])
        if (
            version.definition.code_configuration.content_hash != receipt["package_sha256"]
            or version.metadata.get("source_commit") != receipt["source_commit"]
        ):
            raise ValueError("The native DEMO version does not match the approved source package.")
        env = version.definition.environment_variables
        if (
            env.get("VOLT_MEMORY_ENABLED") != "false"
            or env.get("VOLT_MODEL_CONNECTION") != "volt-demo-models-LLM"
            or env.get("TOOLBOX_ENDPOINT") != f"{DEMO}/toolboxes/volt-support-tools/versions/1/mcp?api-version=v1"
        ):
            raise ValueError("The DEMO configuration differs from the approved release profile.")
        run = client.evals.runs.retrieve(evaluation["run_id"], eval_id=evaluation["eval_id"])
        items = [item.model_dump(mode="json") for item in client.evals.runs.output_items.list(
            run_id=run.id, eval_id=evaluation["eval_id"]
        )]
        # Source-commit lineage was verified on the immutable target version above.
        validate_quality(run.model_dump(mode="json"), items, cases, None, receipt["package_sha256"])
        if contract_version == "v2" and {r["id"]: r["response_id"] for r in actions["cases"]} != {
            i["datasource_item"]["id"]: i["datasource_item"]["response_id"] for i in items
        }:
            raise ValueError("DEMO native and model judgments refer to different responses.")
        if any(
            item["datasource_item"]["agent_name"] != "volt-support"
            or item["datasource_item"]["agent_version"] != receipt["agent_version"]
            for item in items
        ):
            raise ValueError("A native case identifies another DEMO agent version.")
        group = client.evals.retrieve(evaluation["eval_id"]).model_dump(mode="json")
        criteria = group["testing_criteria"]
        grader = project.evaluators.get_version(evaluator_name(contract_version), evaluation["evaluator_version"], headers=HEADERS)
        if (
            len(criteria) != 1 or criteria[0].get("evaluator_name") != evaluator_name(contract_version)
            or criteria[0].get("evaluator_version") != evaluation["evaluator_version"]
            or run.metadata.get("evaluator_sha256") != grader_hash
            or hashlib.sha256(grader.definition.code_text.encode()).hexdigest() != grader_hash
        ):
            raise ValueError("Native DEMO evaluation did not use the fixed business grader.")
        receipt.update({
            "status": "runtime-verified", "verified_at": datetime.now(timezone.utc).isoformat(),
            "runtime_eval_id": evaluation["eval_id"], "runtime_eval_run_id": run.id,
            "runtime_native_counts": run.result_counts.model_dump(),
            "runtime_report_url": run.report_url,
            "runtime_response_ids": [item["datasource_item"]["response_id"] for item in items],
        })
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "agent_version": receipt["agent_version"],
                      "counts": receipt["runtime_native_counts"]}))


if __name__ == "__main__":
    main()
