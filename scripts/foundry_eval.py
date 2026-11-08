"""Publish captured live responses to a native Foundry coherence evaluation."""
import argparse
import json
import os
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", default="evidence/foundry-evaluation.json")
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    if report["mode"] != "live-agent-deterministic-evaluation":
        raise ValueError("Native scoring accepts only captured live-agent evaluation reports")
    rows = [{"item": {"query": row["query"], "response": row["result"]["output"]["answer"]}}
            for row in report["cases"]]
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=credential
    ) as project:
        with project.get_openai_client() as client:
            evaluation = client.evals.create(
                name="Volt showcase - response coherence (not domain correctness)",
                data_source_config={
                    "type": "custom",
                    "item_schema": {"type": "object", "properties": {
                        "query": {"type": "string"}, "response": {"type": "string"}},
                        "required": ["query", "response"]},
                },
                testing_criteria=[{
                    "type": "azure_ai_evaluator", "name": "coherence",
                    "evaluator_name": "builtin.coherence",
                    "initialization_parameters": {"model": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]},
                    "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
                }],
            )
            run = client.evals.runs.create(
                evaluation.id, name=f"Volt captured responses {report['created_at']}",
                data_source={"type": "jsonl", "source": {"type": "file_content", "content": rows}},
            )
            target = Path(args.out)
            target.parent.mkdir(parents=True, exist_ok=True)
            deadline = time.monotonic() + 600
            while True:
                state = {"eval_id": evaluation.id, "run_id": run.id, "status": run.status,
                         "report_url": run.report_url,
                         "scope": "Native Foundry model-judged coherence on captured outputs; not replay, task correctness or safety certification."}
                target.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
                if run.status in ("completed", "failed", "canceled"):
                    print(json.dumps(state, indent=2))
                    return 0 if run.status == "completed" else 1
                if time.monotonic() > deadline:
                    raise TimeoutError(f"Run still {run.status}; saved IDs in {target}. Do not resubmit.")
                time.sleep(10)
                run = client.evals.runs.retrieve(run.id, eval_id=evaluation.id)


if __name__ == "__main__":
    raise SystemExit(main())
