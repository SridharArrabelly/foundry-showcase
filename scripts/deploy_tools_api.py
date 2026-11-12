"""Pass the function-scoped backend credential directly to a secure ARM parameter."""

import json
import shutil
import subprocess
import time
from pathlib import Path

import requests
from azure.identity import DefaultAzureCredential

ROOT = Path(__file__).resolve().parents[1]
SUBSCRIPTION = "40b687ca-31b5-4374-bea2-4c178369b9c0"
GROUP = "rg-volt-citadel"


def main() -> None:
    az = shutil.which("az")
    if az is None:
        raise RuntimeError("Azure CLI is required to compile the deployment template.")
    compiled = subprocess.run(
        [az, "bicep", "build", "--file", str(ROOT / "infra" / "tools-api.bicep"),
         "--stdout", "--only-show-errors"],
        check=True, capture_output=True, text=True, shell=False,
    )
    template = json.loads(compiled.stdout)
    scope = f"/subscriptions/{SUBSCRIPTION}/resourceGroups/{GROUP}"
    function_id = f"{scope}/providers/Microsoft.Web/sites/func-volt-tools-261111"
    deployment = f"https://management.azure.com{scope}/providers/Microsoft.Resources/deployments/volt-tools-gateway"
    with DefaultAzureCredential() as credential, requests.Session() as session:
        def call(method: str, url: str, version: str, body: dict | None = None) -> dict:
            response = session.request(
                method, url, params={"api-version": version},
                headers={"Authorization": f"Bearer {credential.get_token('https://management.azure.com/.default').token}"},
                json=body, timeout=90,
            )
            response.raise_for_status()
            return response.json()

        app = call("GET", "https://management.azure.com" + function_id, "2024-04-01")
        key = call(
            "POST",
            "https://management.azure.com" + function_id + "/functions/business_tool/listkeys",
            "2024-04-01",
        )["default"]
        if not key:
            raise RuntimeError("The function-scoped credential is unavailable.")
        call("PUT", deployment, "2022-09-01", {
            "properties": {
                "mode": "Incremental",
                "template": template,
                "parameters": {
                    "functionKey": {"value": key},
                    "toolsEndpoint": {"value": f"https://{app['properties']['defaultHostName']}/api"},
                },
            }
        })
        deadline = time.monotonic() + 900
        while time.monotonic() < deadline:
            state = call("GET", deployment, "2022-09-01")["properties"]
            status = state["provisioningState"]
            if status == "Succeeded":
                print(json.dumps({"status": status, "mcp_endpoint": state["outputs"]["mcpEndpoint"]["value"]}))
                return
            if status in ("Failed", "Canceled"):
                message = json.dumps(state.get("error", {})).replace(key, "[REDACTED]")
                raise RuntimeError(f"Tool gateway deployment {status}: {message}")
            time.sleep(5)
        raise TimeoutError("Tool gateway deployment is still running; inspect volt-tools-gateway before retrying.")


if __name__ == "__main__":
    main()
