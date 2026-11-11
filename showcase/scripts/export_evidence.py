"""Export an explicitly labeled, credential-free subset of the synthetic recording."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--evaluation-receipt", type=Path)
    args = parser.parse_args()
    receipt_path = args.evaluation_receipt or args.capture_dir / "evaluation.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    rows = [
        json.loads(line) for line in (args.capture_dir / "captured.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    run = receipt["run"]
    if run["status"] != "completed" or run["result_counts"]["total"] != len(rows):
        raise ValueError("Only a complete native evaluation can be exported.")
    records = []
    projects = set()
    for row in rows:
        captured = json.loads((args.capture_dir / f"{row['id']}.json").read_text(encoding="utf-8"))
        projects.add(captured["project_endpoint"])
        raw = captured["response"]
        if json.loads(row["response"]).get("synthetic") is not True:
            raise ValueError("This exporter is restricted to the synthetic Volt fixture.")
        records.append({
            "case": captured["case"],
            "created_at": raw["created_at"],
            "response_id": raw["id"],
            "agent_reference": raw["agent_reference"],
            "code_content_hash": captured["code_content_hash"],
            "output_text": captured["output_text"],
            "observed_tools": json.loads(row["observed_tools"]),
            "protocol_output": raw["output"],
        })
    if len(projects) != 1:
        raise ValueError("A recording must identify one Foundry project.")
    failed_attempts = []
    for path in sorted((args.capture_dir / "failed-attempts").glob("*.json")):
        failed = json.loads(path.read_text(encoding="utf-8"))
        raw = failed["response"]
        failed_attempts.append({
            "case_id": failed["case"]["id"], "response_id": raw["id"],
            "created_at": raw["created_at"], "status": raw["status"],
            "error_code": (raw.get("error") or {}).get("code"),
        })
    artifact = {
        "kind": "recorded-synthetic-evidence",
        "notice": "Recorded live calls, not a live runtime or a guarantee of future model behavior.",
        "project_endpoint": next(iter(projects)),
        "eval_id": receipt["eval_id"], "run_id": receipt["run_id"],
        "report_url": run["report_url"], "native_counts": run["result_counts"],
        "evaluator_version": receipt["evaluator_version"],
        "evaluator_sha256": receipt["evaluator_sha256"],
        "failed_invocation_attempts": failed_attempts,
        "quality_scope": "Business grading of completed responses, not an invocation availability rate.",
        "cases": records,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(records)} recorded cases with native counts to {args.out}")


if __name__ == "__main__":
    main()
