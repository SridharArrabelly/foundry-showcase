"""Package a clean exact commit; optional approved DEV upload, never provision."""

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import HostedAgentDefinition
from azure.identity import DefaultAzureCredential

from evaluate_captures import ROOT
from promote_demo import DEV


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--deploy", action="store_true", help="Usage-billed DEV deployment; separate authorization required.")
    args = parser.parse_args()
    if git("rev-parse", "HEAD").decode().strip() != args.expected_commit or git("status", "--porcelain").strip():
        raise ValueError("Package only the clean approved commit, never an edited checkout.")
    if args.out.exists():
        raise FileExistsError("Keep prior candidate evidence; use a new directory.")
    args.out.mkdir(parents=True)
    package = args.out / "agent.zip"
    tracked = git("ls-files", "-z", "--", "agent/src").decode().split("\0")
    selected = [
        path for path in tracked if path and (
            Path(path).parent.as_posix() == "agent/src" and Path(path).suffix == ".py"
            or path in ("agent/src/requirements.txt", "agent/src/.agentignore",
                        "agent/src/.azdignore", "agent/src/.dockerignore")
            or path.startswith("agent/src/.agent_configs/")
        )
    ]
    with zipfile.ZipFile(package, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(selected):
            info = zipfile.ZipInfo(path.removeprefix("agent/src/"), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, git("show", f"{args.expected_commit}:{path}"))
    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    receipt = {"status": "packaged-not-deployed", "source_commit": args.expected_commit,
               "source_clean": True, "package_sha256": digest, "memory_enabled": False,
               "agent_name": "volt-support", "project_endpoint": DEV}
    path = args.out / "deployment.json"

    def save():
        path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    save()
    if args.deploy:
        with DefaultAzureCredential() as credential, AIProjectClient(
            endpoint=DEV, credential=credential, allow_preview=True
        ) as project:
            baseline = project.agents.get_version("volt-support", "6")
            definition = baseline.definition.as_dict(exclude_readonly=True)
            definition["environment_variables"]["VOLT_MEMORY_ENABLED"] = "false"
            receipt["status"] = "submitting"
            save()
            with package.open("rb") as code:
                created = project.agents.create_version_from_code(
                    "volt-support", definition=HostedAgentDefinition(definition), code=code,
                    code_zip_sha256=digest, metadata={"source_commit": args.expected_commit, "package_sha256": digest},
                )
            receipt.update(status="created-verification-pending", agent_version=created.version)
            save()
            observed = project.agents.get_version("volt-support", created.version)
            if observed.definition.code_configuration.content_hash != digest:
                raise RuntimeError("DEV did not report the uploaded ZIP hash.")
            receipt.update(status="deployed-hash-verified", code_content_hash=digest)
            save()
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
