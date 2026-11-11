"""Initialize azd's managed existing-project state without provisioning an account."""

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "showcase" / "volt-support"
RUNTIME_SETTINGS = (
    "AZURE_AI_PROJECT_ENDPOINT", "AZURE_AI_PROJECT_ID", "AZURE_TENANT_ID",
    "AZURE_SUBSCRIPTION_ID", "AZURE_LOCATION", "AZURE_RESOURCE_GROUP",
    "AZURE_AI_ACCOUNT_NAME", "AZURE_AI_PROJECT_NAME", "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "TOOLBOX_ENDPOINT", "VOLT_MODEL_CONNECTION", "VOLT_MEMORY_ENABLED",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--model-deployment", required=True)
    parser.add_argument("--environment", default="volt-support-dev")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.environment):
        parser.error("Use an environment name containing letters, digits, hyphens or underscores.")
    azd = shutil.which("azd")
    if not azd:
        raise RuntimeError("Azure Developer CLI is required.")
    relative_env = Path(".azure") / args.environment / ".env"
    env_file = PROJECT / relative_env
    old = dotenv_values(env_file) if env_file.exists() else {}
    if old.get("FOUNDRY_PROJECT_ENDPOINT"):
        if old.get("AZURE_AI_PROJECT_ID") != args.project_id:
            raise RuntimeError("Existing environment has a different or unverified project ID; use a separate environment.")
        print(f"Existing azd binding retained: {args.environment}")
        return
    if any(key.startswith("AGENT_") and key.endswith("_VERSION") for key in old):
        raise RuntimeError("Existing deployment state needs explicit migration; refusing to overwrite it.")
    with tempfile.TemporaryDirectory(prefix="volt-foundry-init-") as workdir:
        staged = Path(workdir) / "project"
        # Local template adoption needs a destination outside its source and Git ignore rules.
        subprocess.run(
            [azd, "ai", "agent", "init", "-t", str(PROJECT / "azure.yaml"),
             "--src", "project", "--project-id", args.project_id,
             "--model-deployment", args.model_deployment,
             "--environment", args.environment, "--no-prompt"],
            cwd=workdir, check=True,
        )
        generated = dotenv_values(staged / relative_env)
        endpoint = generated.get("FOUNDRY_PROJECT_ENDPOINT")
        if not endpoint:
            raise RuntimeError("azd did not generate the required project endpoint binding.")
        if old.get("AZURE_AI_PROJECT_ENDPOINT") not in (None, endpoint):
            raise RuntimeError("Generated target differs from the existing endpoint; original state was not changed.")
        settings = {key: old[key] for key in RUNTIME_SETTINGS if old.get(key) is not None}
        settings.update({
            "AZURE_AI_PROJECT_ENDPOINT": endpoint,
            "AZURE_AI_PROJECT_ID": args.project_id,
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": args.model_deployment,
        })
        for key, value in settings.items():
            result = subprocess.run(
                [azd, "env", "set", key, value, "--environment", args.environment],
                cwd=staged, capture_output=True, text=True,
            )
            if result.returncode:
                raise RuntimeError(f"Could not preserve {key}: {result.stderr.replace(value, '[REDACTED]')}")
        if env_file.exists():
            backup = ROOT / ".runtime" / f"{args.environment}-before-binding.env"
            if backup.exists():
                raise RuntimeError(f"Preserving existing backup {backup}; review it before rebinding.")
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(env_file, backup)
        env_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(staged / relative_env, env_file)
    subprocess.run([azd, "env", "select", args.environment], cwd=PROJECT, check=True)
    print(f"Bound {args.environment} to {endpoint}; no account or model was provisioned.")
    print("Configure the remaining runtime settings before deploying; see showcase/volt-support/README.md.")


if __name__ == "__main__":
    main()
