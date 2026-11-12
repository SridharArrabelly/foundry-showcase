"""Index actual captured artifacts and their matching deployed versions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
directory = ROOT / "evidence"
baseline = json.loads((directory / "baseline.json").read_text(encoding="utf-8"))
candidate = json.loads((directory / "candidate.json").read_text(encoding="utf-8"))
release = json.loads((directory / "release.json").read_text(encoding="utf-8"))
if candidate["requested_version"] != release["version"] or not candidate["gate_passed"]:
    raise ValueError("Candidate and release are inconsistent")
index = {
    "baseline_version": baseline["requested_version"],
    "improved_version": candidate["requested_version"],
    "baseline_passed": baseline["passed"],
    "candidate_passed": candidate["passed"],
    "total_cases": candidate["total"],
    "baseline_recorded_at": baseline["created_at"],
    "candidate_recorded_at": candidate["created_at"],
    "release_workflow": "https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42460045951",
    "intentional_blocked_workflow": "https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42459859840",
    "passing_quality_workflow": "https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42459993922",
    "note": "Recorded synthetic-data rehearsal. Verify these retained versions before presenting.",
}
(directory / "rehearsal-index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
print(json.dumps(index, indent=2))
