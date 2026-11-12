"""Presenter CLI: live invocations, transparent evaluations and reviewed feedback."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "github-copilot-invocations"))
from volt.evaluation import evaluate_case


def stamp():
    return datetime.now(timezone.utc).isoformat()


def read_cases(paths):
    cases = []
    ids = set()
    for path in paths:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            case = json.loads(line)
            if case["id"] in ids:
                raise ValueError(f"Duplicate case ID: {case['id']}")
            ids.add(case["id"])
            cases.append(case)
    if not cases:
        raise ValueError("Dataset is empty")
    return cases


def invoke(prompt, local_url=None, version=None):
    body = json.dumps({"input": prompt}).encode()
    if local_url:
        if not local_url.startswith(("http://127.0.0.1:", "http://localhost:")):
            raise ValueError("Local URL must point to a loopback address")
        request = Request(local_url.rstrip("/") + "/invocations", body,
                          {"Content-Type": "application/json"})
        with urlopen(request, timeout=180) as response:
            return json.load(response)
    if not version:
        release_file = ROOT / "evidence" / "release.json"
        if not release_file.exists():
            raise ValueError("Use --version for a candidate, or create a passing release manifest first")
        version = json.loads(release_file.read_text(encoding="utf-8"))["version"]
    with tempfile.TemporaryDirectory(prefix="volt-request-") as directory:
        request_file = Path(directory) / "request.json"
        request_file.write_bytes(body)
        command = ["azd", "ai", "agent", "invoke", "volt-assistant",
                   "--protocol", "invocations", "--input-file", str(request_file),
                   "--output", "raw", "--new-session", "--timeout", "180"]
        if version:
            command += ["--version", version]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                encoding="utf-8", timeout=240, check=True)
    # Raw azd output contains HTTP headers. Accept only the explicit agent envelope.
    decoder = json.JSONDecoder()
    for index, character in enumerate(result.stdout):
        if character == "{":
            try:
                value, _ = decoder.raw_decode(result.stdout[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and value.get("mode") == "live-copilot-sdk":
                value["requested_version"] = version
                return value
    raise RuntimeError("Invocation returned no valid Volt result. Inspect the azd invocation logs.")


def write_json(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ask = commands.add_parser("ask")
    ask.add_argument("prompt")
    ask.add_argument("--out", default="evidence/last-invocation.json")
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("--dataset", action="append", required=True)
    evaluate.add_argument("--out", required=True)
    for command in [ask, evaluate]:
        command.add_argument("--local-url")
        command.add_argument("--version")
    feedback = commands.add_parser("feedback")
    feedback.add_argument("--trace", required=True)
    feedback.add_argument("--id", required=True)
    feedback.add_argument("--query", required=True)
    feedback.add_argument("--expected-decision", required=True)
    feedback.add_argument("--expected-behavior", required=True)
    feedback.add_argument("--reviewer", required=True)
    feedback.add_argument("--approve", action="store_true", required=True)
    feedback.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.command == "ask":
        result = invoke(args.prompt, args.local_url, args.version)
        result["captured_at"] = stamp()
        write_json(args.out, result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "feedback":
        source_bytes = Path(args.trace).read_bytes()
        source = json.loads(source_bytes)
        if source.get("mode") != "live-copilot-sdk":
            raise ValueError("Only a captured live invocation can seed reviewed feedback")
        row = {
            "id": args.id, "query": args.query, "expected_decision": args.expected_decision,
            "expected_behavior": args.expected_behavior, "required_tools": ["getRecallNotices"],
            "approved": True, "reviewed_by": args.reviewer, "reviewed_at": stamp(),
            "source_invocation_id": source["invocation_id"],
            "source_trace_id": source.get("trace_id"),
            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        }
        target = Path(args.out)
        if target.exists():
            raise ValueError("Feedback output already exists; choose a new file to preserve review history")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(row) + "\n", encoding="utf-8")
        print(f"Reviewed case saved to {target}")
        return 0
    cases = read_cases(args.dataset)
    rows = []
    for case in cases:
        result = invoke(case["query"], args.local_url, args.version)
        row = evaluate_case(case, result)
        rows.append(row)
        print(f"{'PASS' if row['passed'] else 'FAIL'} {case['id']}", flush=True)
    passed = sum(row["passed"] for row in rows)
    report = {
        "mode": "live-agent-deterministic-evaluation", "created_at": stamp(),
        "requested_version": args.version, "passed": passed, "total": len(rows),
        "gate_passed": passed == len(rows), "threshold": "all reviewed deterministic checks pass",
        "dataset_hash_format": "sha256-normalized-lf",
        "datasets": [{"path": str(p), "sha256": hashlib.sha256(Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()}
                     for p in args.dataset],
        "limitations": "Small synthetic set. Not an LLM judge, safety certification, benchmark or ROI measurement.",
        "cases": rows,
    }
    write_json(args.out, report)
    print(f"Release gate: {'PASS' if report['gate_passed'] else 'BLOCK'} ({passed}/{len(rows)})")
    return 0 if report["gate_passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
