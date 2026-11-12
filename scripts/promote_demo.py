"""Operator-run gate: promote the tested ZIP, never rebuild it or apply an optimizer candidate."""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

import requests
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import HostedAgentDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

from evaluate_captures import HEADERS, ROOT, validate_case_coverage

REPO = "SridharArrabelly/foundry-showcase"
DEV = "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev"
DEMO = "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-demo"


def github(path: str) -> dict:
    executable = shutil.which("gh")
    if not executable:
        raise RuntimeError("The approved GitHub CLI account is required.")
    result = subprocess.run(
        [executable, "api", f"repos/{REPO}/{path}"], capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def validate_quality(run: dict, items: list[dict], cases: list[dict], commit: str | None, digest: str) -> None:
    counts = run["result_counts"]
    if (
        run["status"] != "completed" or counts["passed"] != len(cases)
        or counts["total"] != len(cases) or counts["failed"] or counts["errored"] or counts["skipped"]
    ):
        raise ValueError("Native business evaluation is not a complete all-pass result.")
    if (
        run["metadata"].get("code_content_hash") != digest
        or (commit is not None and run["metadata"].get("source_commit") != commit)
    ):
        raise ValueError("Native evaluation belongs to a different source commit or package.")
    rows = [item["datasource_item"] for item in items]
    validate_case_coverage(rows, cases)
    if any(row["code_content_hash"] != digest for row in rows):
        raise ValueError("Native case evidence identifies a different package.")
    for item in items:
        results = item.get("results", [])
        if (
            item.get("status") != "completed" or len(results) != 1
            or results[0].get("passed") is not True or results[0].get("score") != 1.0
            or results[0].get("status") != "completed"
        ):
            raise ValueError("Every native business result must explicitly pass with score 1.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--deployment-receipt", type=Path, required=True)
    parser.add_argument("--evaluation-receipt", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--pull-request", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--execute", action="store_true", help="Requires explicit operator approval and a merged PR.")
    args = parser.parse_args()
    if args.execute and args.out.exists():
        raise FileExistsError("A promotion receipt already exists; inspect it rather than submitting again.")
    deployment = json.loads(args.deployment_receipt.read_text(encoding="utf-8"))
    evaluation = json.loads(args.evaluation_receipt.read_text(encoding="utf-8"))
    digest = hashlib.sha256(args.package.read_bytes()).hexdigest()
    if (
        deployment.get("status") != "deployed-hash-verified" or deployment.get("source_clean") is not True
        or deployment.get("memory_enabled") is not False
        or deployment.get("source_commit") != args.expected_commit
        or deployment.get("package_sha256") != digest or deployment.get("code_content_hash") != digest
    ):
        raise ValueError("The ZIP must match the verified, Memory-disabled source deployment receipt.")
    pr = github(f"pulls/{args.pull_request}")
    if pr["head"]["sha"] != args.expected_commit or pr["base"]["ref"] != "feature/volt-citadel":
        raise ValueError("The selected PR does not match the reviewed source and target branch.")
    checks = github(f"commits/{args.expected_commit}/check-runs")["check_runs"]
    successful = {check["name"] for check in checks if check["status"] == "completed" and check["conclusion"] == "success"}
    if not {"contracts", "tool-contract"}.issubset(successful):
        raise ValueError("The expected GitHub CI checks have not passed on this commit.")
    cases_path = ROOT / "agent" / "src" / ".foundry" / "datasets" / "volt-regression.jsonl"
    cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    grader_hash = hashlib.sha256((ROOT / "evaluations" / "business_contract.py").read_text(encoding="utf-8").encode()).hexdigest()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=DEV, credential=credential, allow_preview=True
    ) as source, source.get_openai_client(default_headers=HEADERS) as eval_client, AIProjectClient(
        endpoint=DEMO, credential=credential, allow_preview=True
    ) as target:
        run = eval_client.evals.runs.retrieve(evaluation["run_id"], eval_id=evaluation["eval_id"])
        items = list(eval_client.evals.runs.output_items.list(run_id=run.id, eval_id=evaluation["eval_id"]))
        validate_quality(run.model_dump(mode="json"), [item.model_dump(mode="json") for item in items], cases, args.expected_commit, digest)
        group = eval_client.evals.retrieve(evaluation["eval_id"]).model_dump(mode="json")
        criteria = group["testing_criteria"]
        if (
            len(criteria) != 1 or criteria[0].get("evaluator_name") != "volt_business_contract"
            or criteria[0].get("evaluator_version") != "1"
            or run.metadata.get("evaluator_sha256") != grader_hash
        ):
            raise ValueError("The native run does not use the pinned business evaluator.")
        remote_grader = source.evaluators.get_version("volt_business_contract", "1", headers=HEADERS)
        if hashlib.sha256(remote_grader.definition.code_text.encode()).hexdigest() != grader_hash:
            raise ValueError("The remote grader differs from the checked-in business contract.")
        version = source.agents.get_version(deployment["agent_name"], deployment["agent_version"])
        if version.definition.code_configuration.content_hash != digest:
            raise ValueError("The current DEV version does not identify this package.")
        definition = version.definition.as_dict(exclude_readonly=True)
        environment = definition["environment_variables"]
        if environment.get("VOLT_MEMORY_ENABLED") != "false":
            raise ValueError("The tested configuration must have Memory disabled.")
        environment["VOLT_MODEL_CONNECTION"] = "volt-demo-models-LLM"
        environment["TOOLBOX_ENDPOINT"] = f"{DEMO}/toolboxes/volt-support-tools/versions/1/mcp?api-version=v1"
        try:
            target.agents.get("volt-support")
            exists = True
        except ResourceNotFoundError:
            exists = False
        receipt = {
            "status": "ready" if pr["merged"] else "awaiting-human-merge",
            "source_commit": args.expected_commit, "package_sha256": digest,
            "source_agent_version": deployment["agent_version"],
            "eval_id": evaluation["eval_id"], "eval_run_id": run.id, "report_url": run.report_url,
            "pull_request": pr["html_url"], "target_project": DEMO,
            "model_connection": environment["VOLT_MODEL_CONNECTION"],
            "toolbox_endpoint": environment["TOOLBOX_ENDPOINT"], "memory_enabled": False,
            "operation": "new-version" if exists else "create-agent",
        }
        if not args.execute:
            print(json.dumps(receipt, indent=2))
            return
        if not pr["merged"]:
            raise ValueError("Human merge approval is still required; no deployment performed.")
        metadata = {
            "source_commit": args.expected_commit, "package_sha256": digest,
            "eval_id": evaluation["eval_id"], "eval_run_id": run.id, "source_pr": str(args.pull_request),
        }
        receipt.update({"status": "submitting", "request_id": str(uuid4())})
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        with args.package.open("rb") as code:
            if exists:
                deployed = target.agents.create_version_from_code(
                    "volt-support", definition=HostedAgentDefinition(definition), code=code,
                    code_zip_sha256=digest, metadata=metadata,
                    headers={"x-ms-client-request-id": receipt["request_id"]},
                )
                number = deployed.version
            else:
                # The CLI's new-agent multipart route supports promoting the saved ZIP unchanged.
                response = requests.post(
                    f"{DEMO}/agents", params={"api-version": "v1"},
                    headers={
                        "Authorization": f"Bearer {credential.get_token('https://ai.azure.com/.default').token}",
                        "x-ms-code-zip-sha256": digest, "x-ms-agent-name": "volt-support",
                        "x-ms-client-request-id": receipt["request_id"],
                    },
                    files={
                        "metadata": (None, json.dumps({"name": "volt-support", "definition": definition, "metadata": metadata}), "application/json"),
                        "code": ("agent.zip", code, "application/zip"),
                    },
                    timeout=300,
                )
                response.raise_for_status()
                number = response.json()["versions"]["latest"]["version"]
        receipt.update({"status": "created-verification-pending", "agent_version": number})
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        deployed = target.agents.get_version("volt-support", number)
        if deployed.definition.code_configuration.content_hash != digest:
            raise RuntimeError("DEMO package hash differs; do not mark this release ready.")
        receipt["status"] = "package-verified-smoke-pending"
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
