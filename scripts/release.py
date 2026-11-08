"""Write the demo client's release pointer only after a passing live scorecard."""
import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", default="evidence/release.json")
    args = parser.parse_args()
    data = Path(args.report).read_bytes()
    report = json.loads(data)
    if report.get("mode") != "live-agent-deterministic-evaluation":
        raise ValueError("A live evaluation report is required; offline fixtures cannot authorize release")
    if not report.get("gate_passed") or report["passed"] != report["total"] or report["total"] < 9:
        raise ValueError("The complete core plus regression suite must pass")
    if report.get("requested_version") != args.version:
        raise ValueError("Report version differs from the requested release")
    rows = report["cases"]
    required_ids = {
        json.loads(line)["id"]
        for path in (Path("datasets/core.jsonl"), Path("datasets/regression.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    }
    ids = [row["id"] for row in rows]
    if len(set(ids)) != len(ids) or not required_ids <= set(ids):
        raise ValueError("Missing or duplicate required release cases")
    if any(
        not row["passed"] or not all(row["checks"].values())
        or row["result"]["variant"] != "improved"
        or row["result"]["mode"] != "live-copilot-sdk"
        or row["result"]["hosting"] != "foundry"
        or row["result"].get("requested_version") != args.version
        for row in rows
    ):
        raise ValueError("Every case must pass against the improved candidate")
    for dataset in report["datasets"]:
        content = Path(dataset["path"]).read_bytes()
        hashes = {hashlib.sha256(content).hexdigest(),
                  hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()}
        if dataset["sha256"] not in hashes:
            raise ValueError(f"Dataset changed since evaluation: {dataset['path']}")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    release = {
        "agent": "volt-assistant", "version": args.version,
        "review_workspace_revision": revision,
        "deployment_source_revision": os.environ.get("GITHUB_SHA"),
        "report_sha256": hashlib.sha256(data).hexdigest(),
        "datasets": report["datasets"], "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Approved demo-client version pointer. Does not change Foundry portal default routing.",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_suffix(".tmp")
    temporary.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    temporary.replace(out)
    print(json.dumps(release, indent=2))


if __name__ == "__main__":
    main()
