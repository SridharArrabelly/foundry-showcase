"""Run one explicitly authorized v2 validation; stop on the first failed gate."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from evaluate_captures import ROOT
from promote_demo import DEV, DEMO


def validation_endpoint(receipt, environment):
    endpoint = DEV if environment == "dev" else DEMO
    project_field = "project_endpoint" if environment == "dev" else "target_project"
    statuses = {"deployed-hash-verified"} if environment == "dev" else {
        "package-verified-smoke-pending", "runtime-verified",
    }
    if (receipt.get(project_field) != endpoint or receipt.get("status") not in statuses
            or receipt.get("memory_enabled") is not False
            or not all(receipt.get(key) for key in ("agent_version", "source_commit", "package_sha256"))):
        raise ValueError("The deployment receipt does not identify a verified package in the selected environment.")
    return endpoint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", choices=["dev", "demo"], required=True)
    parser.add_argument("--deployment-receipt", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        raise ValueError("This operation incurs usage. Explicit --execute and prior approval are required.")
    if args.out.exists():
        raise FileExistsError("Keep the previous validation evidence; choose a fresh directory.")
    receipt = json.loads(args.deployment_receipt.read_text(encoding="utf-8"))
    endpoint = validation_endpoint(receipt, args.environment)
    args.out.mkdir(parents=True)
    dataset = ROOT / "agent/src/.foundry/datasets/volt-regression-v2.jsonl"

    def run(script, *arguments):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, arguments)], check=True)

    registration = args.out / "evaluator.json"
    run("bootstrap_foundry.py", "--project-endpoint", endpoint, "--evaluator-only",
        "--contract-version", "v2", "--out", registration)
    evaluator = json.loads(registration.read_text(encoding="utf-8"))["evaluator"]["version"]
    run("capture_cases.py", "--project-endpoint", endpoint, "--expected-version", receipt["agent_version"],
        "--contract-version", "v2", "--dataset", dataset, "--fresh", "--pause-seconds", "30",
        "--out", args.out / "captures")
    extra = ["--deployment-receipt", args.deployment_receipt] if args.environment == "dev" else []
    run("evaluate_captures.py", "--project-endpoint", endpoint, "--contract-version", "v2",
        "--evaluator-version", evaluator, "--dataset", dataset,
        "--captures", args.out / "captures/captured.jsonl", "--require-all-pass",
        "--label", f"Volt v2 {args.environment} {receipt['source_commit'][:12]}",
        "--out", args.out / "native-evaluation.json", *extra)
    run("score_action_claims.py", "--project-endpoint", endpoint, "--expected-commit", receipt["source_commit"],
        "--package-sha256", receipt["package_sha256"], "--dataset", dataset,
        "--captures", args.out / "captures/captured.jsonl", "--out", args.out / "action-judgments.json")
    if args.environment == "demo":
        run("verify_demo_release.py", "--receipt", args.deployment_receipt,
            "--runtime-evaluation", args.out / "native-evaluation.json",
            "--action-judgments", args.out / "action-judgments.json")
    summary = {
        "status": "passed", "environment": args.environment, "source_commit": receipt["source_commit"],
        "package_sha256": receipt["package_sha256"], "agent_version": receipt["agent_version"],
        "business": "native v2 all cases passed", "action_truthfulness": "calibrated model gate passed",
        "scope": "Synthetic bounded cases, not availability or universal safety.",
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
