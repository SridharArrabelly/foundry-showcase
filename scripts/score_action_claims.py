"""Bounded model-rubric gate. Running this incurs Azure usage; never run implicitly."""

import argparse
import hashlib
import json
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel, ConfigDict

from evaluate_captures import ROOT, validate_case_coverage

RUBRIC = ROOT / "evaluations/action_truthfulness.json"
CALIBRATION = ROOT / "evaluations/action_truthfulness_calibration.jsonl"


class Judgment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    passed: bool
    reason: str
    evidence: str


def verify_action_gate(receipt, cases, commit, digest):
    if (
        receipt.get("status") != "passed" or receipt.get("source_commit") != commit
        or receipt.get("package_sha256") != digest
        or receipt.get("model") != "gpt-5.4-mini"
        or receipt.get("rubric_sha256") != hashlib.sha256(RUBRIC.read_bytes()).hexdigest()
        or receipt.get("calibration_sha256") != hashlib.sha256(CALIBRATION.read_bytes()).hexdigest()
    ):
        raise ValueError("Action-truthfulness evidence does not match the candidate and reviewed rubric.")
    calibration = [json.loads(line) for line in CALIBRATION.read_text(encoding="utf-8").splitlines()]
    labels = {row["id"]: row["expected_pass"] for row in calibration}
    actual = receipt.get("calibration", [])
    if len(actual) != len(labels) or {row["id"] for row in actual} != set(labels) or any(row["passed"] != labels[row["id"]] for row in actual):
        raise ValueError("Model judge calibration did not pass all reviewed examples.")
    rows = receipt.get("cases", [])
    if len(rows) != len(cases) or {row["id"] for row in rows} != {case["id"] for case in cases}:
        raise ValueError("Action judgments must cover every case exactly once.")
    if any(row.get("passed") is not True or not row.get("reason") or not row.get("evidence") or not row.get("response_id") for row in rows):
        raise ValueError("Every action-truthfulness judgment must explicitly pass with evidence.")
    if len({row["response_id"] for row in rows}) != len(rows):
        raise ValueError("Action judgments reuse a response.")


def main():
    parser = argparse.ArgumentParser()
    for name in ("project-endpoint", "expected-commit", "package-sha256"):
        parser.add_argument("--" + name, required=True)
    for name in ("captures", "dataset", "out"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--model", choices=["gpt-5.4-mini"], default="gpt-5.4-mini")
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Preserve the existing model-judge receipt; choose another output.")
    rows = [json.loads(line) for line in args.captures.read_text(encoding="utf-8").splitlines()]
    cases = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines()]
    validate_case_coverage(rows, cases)
    if not 1 <= len(rows) <= 20 or any(row["code_content_hash"] != args.package_sha256 for row in rows):
        raise ValueError("Judge a bounded complete dataset from the selected package.")
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    calibration = [json.loads(line) for line in CALIBRATION.read_text(encoding="utf-8").splitlines()]
    receipt = {
        "status": "in_progress", "source_commit": args.expected_commit,
        "package_sha256": args.package_sha256, "model": args.model,
        "rubric_sha256": hashlib.sha256(RUBRIC.read_bytes()).hexdigest(),
        "calibration_sha256": hashlib.sha256(CALIBRATION.read_bytes()).hexdigest(),
        "calibration": [], "cases": [],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)

    def save():
        args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    save()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential
    ) as project, project.get_openai_client(timeout=90, max_retries=0) as client:
        def judge(data):
            response = client.responses.parse(
                model=args.model, text_format=Judgment, max_output_tokens=600,
                input=[{"role": "system", "content": rubric["instructions"]},
                       {"role": "user", "content": json.dumps(data)}],
            )
            result = response.output_parsed
            if (not isinstance(result, Judgment) or not result.reason.strip()
                    or not result.evidence.strip() or result.evidence not in data["answer"]):
                raise ValueError("Model judge returned no complete structured verdict.")
            return result.model_dump()
        for example in calibration:
            receipt["calibration"].append({"id": example["id"], **judge({"answer": example["answer"], "tools": []})})
            save()
        if any(result["passed"] != example["expected_pass"] for result, example in zip(receipt["calibration"], calibration)):
            receipt["status"] = "calibration-failed"
            save()
            raise RuntimeError("The judge failed calibration; no candidate quality claim is permitted.")
        for row in rows:
            receipt["cases"].append({
                "id": row["id"], "response_id": row["response_id"],
                **judge({"query": row["query"], "answer": json.loads(row["response"])["answer"],
                         "tools": json.loads(row["observed_calls"])}),
            })
            save()
    receipt["status"] = "passed" if all(row["passed"] for row in receipt["cases"]) else "failed"
    save()
    verify_action_gate(receipt, cases, args.expected_commit, args.package_sha256)
    print(json.dumps({"status": receipt["status"], "cases": len(rows), "receipt": str(args.out)}))


if __name__ == "__main__":
    main()
