"""Use a harmless marker to verify native enforcement, not a model's refusal text."""

import argparse
import json
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import APIStatusError

MARKER = "VOLT_DEMO_BLOCK_MARKER_261111"


def codes(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() == "code" and isinstance(item, str):
                yield item.lower().replace("_", "").replace("-", "")
            yield from codes(item)
    elif isinstance(value, list):
        for item in value:
            yield from codes(item)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--agent", default="volt-support")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential, allow_preview=True
    ) as project, project.get_openai_client(
        agent_name=args.agent, timeout=180, max_retries=0
    ) as client:
        try:
            response = client.responses.create(input=f"Harmless guardrail demonstration marker: {MARKER}")
            result = {"http_status": 200, "response": response.model_dump(mode="json")}
        except APIStatusError as exc:
            result = {"http_status": exc.status_code, "error": exc.body}
    found = set(codes(result))
    result["native_filter_observed"] = bool(
        found & {"contentfilter", "contentfiltererror", "responsibleaipolicyviolation"}
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"http_status": result["http_status"], "codes": sorted(found),
                      "native_filter_observed": result["native_filter_observed"]}))
    if not result["native_filter_observed"]:
        raise RuntimeError(f"No native content-filter evidence; do not present this as a passed guardrail test. See {args.out}")


if __name__ == "__main__":
    main()
