"""Prepare, but never submit, the reviewed two-candidate instruction experiment."""

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "agent" / "src"


def read_cases(name: str) -> list[dict]:
    path = AGENT / ".foundry" / "datasets" / name
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or len({row["id"] for row in rows}) != len(rows):
        raise ValueError(f"Dataset must contain distinct cases: {path}")
    if any(not isinstance(row.get("query"), str) or not row["query"].strip() for row in rows):
        raise ValueError(f"Dataset contains an empty or invalid query: {path}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-version", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(f"Review the existing request rather than overwriting it: {args.out}")
    training = read_cases("volt-optimization-train.jsonl")
    validation = read_cases("volt-optimization-validation.jsonl")
    regression = read_cases("volt-regression.jsonl")
    queries = [{row["query"] for row in rows} for rows in (training, validation, regression)]
    if queries[0] & queries[1] or queries[0] & queries[2] or queries[1] & queries[2]:
        raise ValueError("Training, validation and fixed regression queries must be separate.")
    baseline = AGENT / ".agent_configs" / "baseline"
    metadata = yaml.safe_load((baseline / "metadata.yaml").read_text(encoding="utf-8"))
    if metadata["model"] != "gpt-5.4-mini" or metadata["instruction_file"] != "instructions.md":
        raise ValueError("The baseline changed; review the model and instruction choices again.")
    request = {
        "display_name": "Volt instruction experiment - two candidates",
        "target_configuration": {
            "type": "foundry_agent", "name": "volt-support", "version": args.agent_version,
        },
        "optimization_model_configuration": {"model": "gpt-5.4"},
        "optimization_configuration": {
            "type": "agent_optimization",
            "goal": "improve_quality",
            "baseline_agent_configuration": {
                "current_model": metadata["model"],
                "system_prompt": (baseline / "instructions.md").read_text(encoding="utf-8"),
            },
            "agent_optimization_space": {"target_attributes": ["instructions"]},
            "candidate_search_configuration": {"max_candidates": 2},
            "evaluation_configuration": {
                "training_set": {
                    "type": "target_completion",
                    "source": {"type": "inline", "test_cases": training},
                },
                "validation_set": {
                    "type": "target_completion",
                    "source": {"type": "inline", "test_cases": validation},
                },
                "evaluators": [{"name": "builtin.task_adherence"}],
                "evaluation_model": {"model": "gpt-5.4-mini"},
                "max_concurrent_agent_runs": 1,
            },
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {args.out}: {len(training)} training and {len(validation)} validation cases.")
    print("Task-adherence scores are exploratory; the separate nine-case business gate still governs release.")
    print("No job submitted and no candidate applied.")


if __name__ == "__main__":
    main()
