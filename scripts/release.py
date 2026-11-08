"""Write the demo client's release pointer only after a passing live scorecard."""
import argparse
import hashlib
import json
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
    if any(not row["passed"] or row["result"]["variant"] != "improved" for row in report["cases"]):
        raise ValueError("Every case must pass against the improved candidate")
    for dataset in report["datasets"]:
        if hashlib.sha256(Path(dataset["path"]).read_bytes()).hexdigest() != dataset["sha256"]:
            raise ValueError(f"Dataset changed since evaluation: {dataset['path']}")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    release = {
        "agent": "volt-assistant", "version": args.version, "source_revision": revision,
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
