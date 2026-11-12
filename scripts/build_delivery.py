"""Bundle committed showcase files plus the verified, secret-free release artifact."""

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SCOPES = [
    "agent", "tools", "evaluations", "infra", "scripts", "knowledge",
    "recordings", "presentation", "docs", "README.md", "AGENTS.md",
    "CLAUDE.md", "THIRD_PARTY_NOTICES.txt", ".gitignore",
    ".github/workflows/citadel-quality.yml",
]


def git(*arguments: str) -> bytes:
    executable = shutil.which("git")
    if not executable:
        raise RuntimeError("Git is required to select the committed delivery files.")
    return subprocess.run(
        [executable, "-C", str(ROOT), *arguments], capture_output=True, check=True,
    ).stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Choose a new delivery filename rather than overwriting a previous handoff.")
    if git("status", "--porcelain", "--untracked-files=all", "--", *SCOPES).strip():
        raise RuntimeError("Commit the showcase deliverables before packaging them.")
    paths = [value.decode("utf-8") for value in git("ls-files", "-z", "--", *SCOPES).split(b"\0") if value]
    source = json.loads((ROOT / ".runtime" / "volt-candidate-package.json").read_text(encoding="utf-8"))
    promotion = json.loads((ROOT / ".runtime" / "volt-demo-release.json").read_text(encoding="utf-8"))
    package = ROOT / ".runtime" / "volt-candidate-1d01eaa.zip"
    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    if (
        source["status"] != "deployed-hash-verified" or source["source_clean"] is not True
        or promotion["status"] != "runtime-verified"
        or source["package_sha256"] != digest or promotion["package_sha256"] != digest
        or source["source_commit"] != promotion["source_commit"]
    ):
        raise ValueError("The package and verified promotion receipts do not agree.")
    start = """Volt & Co: governed and improving agents

1. Open presentation/Volt & Co - Governed and improving agents.pptx.
2. Read presentation/Presenter manuscript.pdf for the full spoken script.
3. Use presentation/Recorded evidence.html only as a clearly labeled offline fallback.
4. Follow docs/OPERATIONS.md for prerequisites, exact live commands and boundaries.
5. The tested code ZIP and receipts are under .runtime. They contain no credentials.

The full repository retains the original 50-minute demo; this bundle contains
the current Citadel path and its shared synthetic Volt domain fixtures.

Verified: DEV baseline 8/9, reviewed fix 9/9, unchanged ZIP promoted to DEMO with
fresh native 9/9 results, native guardrail blocking, real IQ retrieval and traces.
Memory works for one authenticated DEV caller; it is disabled in DEMO.
Optimizer completed without an accepted improvement; no candidate was applied.
Human 90-minute timing rehearsal and cross-user Memory authorization remain open.
Do not treat this synthetic internal profile as production-ready.
"""
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "x", zipfile.ZIP_DEFLATED) as archive:
        for relative in paths:
            parts = PurePosixPath(relative).parts
            if any(part in {".azure", ".venv", "__pycache__", "results"} for part in parts):
                raise ValueError(f"Local/generated state unexpectedly tracked: {relative}")
            path = ROOT.joinpath(*parts)
            if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError(f"Refusing a path outside the checked-out project: {relative}")
            if path.name.startswith(".env") and path.name != ".env.example":
                raise ValueError(f"Refusing an environment file: {relative}")
            if path.resolve() == args.out.resolve():
                raise ValueError("The archive cannot include itself.")
            archive.write(path, relative)
        archive.writestr("START HERE.txt", start)
        archive.write(package, ".runtime/volt-candidate-1d01eaa.zip")
        archive.writestr(".runtime/volt-candidate-package.json", json.dumps(source, indent=2))
        archive.writestr(".runtime/volt-demo-release.json", json.dumps(promotion, indent=2))
        prefix = "agent/src/.foundry/results"
        for folder, filename in (("candidate-v6", "native-evaluation.json"), ("demo-v1", "evaluation.json")):
            receipt = json.loads((ROOT.joinpath(*PurePosixPath(prefix).parts) / folder / filename).read_text(encoding="utf-8"))
            archive.writestr(
                f"{prefix}/{folder}/{filename}",
                json.dumps({"eval_id": receipt["eval_id"], "run_id": receipt["run_id"]}, indent=2),
            )
        archive.writestr("DELIVERY MANIFEST.json", json.dumps({
            "source_repository_commit": git("rev-parse", "HEAD").decode().strip(),
            "tested_agent_source_commit": source["source_commit"],
            "tested_agent_zip_sha256": digest,
            "demo_agent_version": promotion["agent_version"],
            "native_demo_report": promotion["runtime_report_url"],
            "evaluation_files": "Minimal native-run pointers; complete synthetic recordings are in recordings.",
        }, indent=2))
    with zipfile.ZipFile(args.out) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Delivery archive integrity check failed.")
        if hashlib.sha256(archive.read(".runtime/volt-candidate-1d01eaa.zip")).hexdigest() != digest:
            raise RuntimeError("The bundled agent artifact differs from the verified ZIP.")
    print(json.dumps({
        "delivery": str(args.out), "bytes": args.out.stat().st_size,
        "sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
