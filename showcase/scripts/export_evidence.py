"""Export an explicitly labeled, credential-free subset of the synthetic recording."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = json.loads((args.capture_dir / "evaluation.json").read_text(encoding="utf-8"))
    rows = [
        json.loads(line) for line in (args.capture_dir / "captured.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    run = receipt["run"]
    if run["status"] != "completed" or run["result_counts"]["total"] != len(rows):
        raise ValueError("Only a complete native evaluation can be exported.")
    records = []
    for row in rows:
        captured = json.loads((args.capture_dir / f"{row['id']}.json").read_text(encoding="utf-8"))
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
    artifact = {
        "kind": "recorded-synthetic-evidence",
        "notice": "Recorded live calls, not a live runtime or a guarantee of future model behavior.",
        "eval_id": receipt["eval_id"], "run_id": receipt["run_id"],
        "report_url": run["report_url"], "native_counts": run["result_counts"],
        "evaluator_version": receipt["evaluator_version"],
        "evaluator_sha256": receipt["evaluator_sha256"],
        "cases": records,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(records)} recorded cases with native counts to {args.out}")


if __name__ == "__main__":
    main()
