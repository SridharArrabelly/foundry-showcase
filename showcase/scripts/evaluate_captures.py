"""Publish the business metric in Foundry using actual captured hosted outputs."""

import argparse
import hashlib
import json
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from azure.identity import DefaultAzureCredential

HEADERS = {"Foundry-Features": "Evaluations=V1Preview"}
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--eval-id")
    parser.add_argument("--evaluator-version", default="1")
    parser.add_argument("--require-all-pass", action="store_true")
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(f"Evaluation receipt already exists: {args.out}; inspect it instead of submitting twice.")
    rows = [json.loads(line) for line in args.captures.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or len({row["response_id"] for row in rows}) != len(rows):
        raise ValueError("Provide nonempty captures with distinct response IDs.")
    versions = {row["agent_version"] for row in rows}
    code_hashes = {row["code_content_hash"] for row in rows}
    if len(versions) != 1 or len(code_hashes) != 1:
        raise ValueError("A run must compare captures from one verified agent version and code artifact.")
    code = (ROOT / "evaluators" / "business_contract.py").read_text(encoding="utf-8")
    source_hash = hashlib.sha256(code.encode()).hexdigest()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential
    ) as project, project.get_openai_client(default_headers=HEADERS) as client:
        evaluator = project.evaluators.get_version(
            name="volt_business_contract", version=args.evaluator_version, headers=HEADERS
        )
        if hashlib.sha256(evaluator.definition.code_text.encode()).hexdigest() != source_hash:
            raise RuntimeError("The selected remote evaluator differs from the checked-in grader.")
        fields = (
            "id", "query", "response", "observed_tools", "expected_decision",
            "required_tool", "expected_reference", "response_id", "agent_name",
            "agent_version", "code_content_hash",
        )
        if args.eval_id:
            evaluation = client.evals.retrieve(args.eval_id)
            existing = evaluation.model_dump(mode="json")
            criteria = existing.get("testing_criteria", [])
            if (
                len(criteria) != 1 or criteria[0].get("evaluator_name") != evaluator.name
                or criteria[0].get("evaluator_version") != evaluator.version
                or existing.get("metadata", {}).get("evaluator_sha256") != source_hash
            ):
                raise ValueError("Existing evaluation uses a different metric or evaluator artifact.")
        else:
            evaluation = client.evals.create(
                name="Volt business contract - captured hosted responses",
                metadata={"evaluator_sha256": source_hash, "evaluator_version": evaluator.version},
                data_source_config={
                    "type": "custom",
                    "item_schema": {
                        "type": "object",
                        "properties": {field: {"type": "string"} for field in fields},
                        "required": list(fields),
                    },
                    "include_sample_schema": True,
                },
                testing_criteria=[TestingCriterionAzureAIEvaluator(
                    type="azure_ai_evaluator", name="business_contract",
                    evaluator_name=evaluator.name,
                    evaluator_version=evaluator.version,
                    initialization_parameters={"deployment_name": "gpt-5.4-mini", "pass_threshold": 0.5},
                )],
            )
        run = client.evals.runs.create(
            eval_id=evaluation.id, name=args.label,
            metadata={
                "agent_name": rows[0]["agent_name"], "agent_version": next(iter(versions)),
                "code_content_hash": next(iter(code_hashes)),
                "evaluator_version": evaluator.version, "evaluator_sha256": source_hash,
                "source": "captured-live-hosted-responses",
            },
            data_source={
                "type": "jsonl", "source": {
                    "type": "file_content",
                    "content": [{"item": {field: row[field] for field in fields}} for row in rows],
                },
            },
        )
        receipt = {
            "eval_id": evaluation.id, "run_id": run.id, "label": args.label,
            "evaluator_version": evaluator.version, "evaluator_sha256": source_hash,
            "input_count": len(rows), "run": run.model_dump(mode="json"),
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"Native evaluation submitted: {evaluation.id} / {run.id}", flush=True)
        deadline = time.monotonic() + 900
        while run.status not in ("completed", "failed", "canceled"):
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Evaluation still running; inspect the IDs in {args.out}, do not resubmit.")
            time.sleep(5)
            run = client.evals.runs.retrieve(run_id=run.id, eval_id=evaluation.id)
        items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=evaluation.id))
        receipt.update({
            "run": run.model_dump(mode="json"),
            "items": [item.model_dump(mode="json") for item in items],
        })
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        counts = run.result_counts
        print(json.dumps({"status": run.status, "counts": counts.model_dump(), "report_url": run.report_url}))
        if run.status != "completed" or counts.errored or counts.total != len(rows) or len(items) != len(rows):
            raise RuntimeError(f"Native evaluation was incomplete or errored; inspect {args.out}.")
        if args.require_all_pass and counts.passed != len(rows):
            raise RuntimeError(f"Business release gate failed: {counts.passed}/{len(rows)} passed.")


if __name__ == "__main__":
    main()
