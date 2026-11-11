"""Register the native business evaluator and a restricted synthetic memory store."""

import argparse
import hashlib
import json
from datetime import timedelta
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition, MemoryStoreDefaultOptions
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--evaluator-only", action="store_true", help="Do not create or inspect a Memory store.")
    args = parser.parse_args()
    code = (ROOT / "evaluators" / "business_contract.py").read_text(encoding="utf-8")
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential
    ) as project:
        store = None
        if not args.evaluator_only:
            name = "volt-preferences"
            try:
                store = project.beta.memory_stores.get(name)
            except ResourceNotFoundError:
                store = project.beta.memory_stores.create(
                    name=name,
                    definition=MemoryStoreDefaultDefinition(
                        chat_model="gpt-5.4-mini",
                        embedding_model="text-embedding-3-small",
                        options=MemoryStoreDefaultOptions(
                            user_profile_enabled=True,
                            chat_summary_enabled=False,
                            procedural_memory_enabled=False,
                            default_ttl_seconds=timedelta(days=7),
                            user_profile_details=(
                                "Only explicitly requested synthetic response-style preferences. "
                                "Do not retain orders, device safety conclusions, authorization, "
                                "policy facts, credentials, or personal/sensitive information."
                            ),
                        ),
                    ),
                    description="Internal Volt showcase: synthetic response-style preferences only.",
                )
        evaluator_name = "volt_business_contract"
        try:
            matches = [
                version for version in project.evaluators.list_versions(
                    evaluator_name, headers={"Foundry-Features": "Evaluations=V1Preview"}
                )
                if version.metadata and version.metadata.get("source_sha256") == code_hash
            ]
        except ResourceNotFoundError:
            print("No prior Volt business evaluator; registering the first version.")
            matches = []
        if matches:
            evaluator = matches[0]
        else:
            evaluator = project.evaluators.create_version(
                name=evaluator_name,
                headers={"Foundry-Features": "Evaluations=V1Preview"},
                evaluator_version={
                    "display_name": "Volt business contract",
                    "description": "Decision correctness with actual observed tool evidence; not coherence.",
                    "categories": ["quality"],
                    "metadata": {"source_sha256": code_hash},
                    "definition": {
                        "type": "code",
                        "code_text": code,
                        "init_parameters": {
                            "type": "object",
                            "properties": {
                                "deployment_name": {"type": "string"},
                                "pass_threshold": {"type": "number"},
                            },
                            "required": ["deployment_name", "pass_threshold"],
                        },
                        "metrics": {
                            "result": {
                                "type": "continuous",
                                "desirable_direction": "increase",
                                "min_value": 0.0,
                                "max_value": 1.0,
                            }
                        },
                        "data_schema": {
                            "type": "object",
                            "required": ["item"],
                            "properties": {
                                "item": {
                                    "type": "object",
                                    "required": ["response", "observed_tools", "expected_decision", "required_tool"],
                                    "properties": {
                                        name: {"type": "string"}
                                        for name in (
                                            "response", "observed_tools", "expected_decision",
                                            "required_tool", "expected_reference",
                                        )
                                    },
                                }
                            },
                        },
                    },
                },
            )
        result = {
            "project_endpoint": args.project_endpoint,
            "memory_store": store.as_dict() if store else None,
            "evaluator": evaluator.as_dict(),
            "evaluator_source_sha256": code_hash,
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
        print(json.dumps({"memory_store": store.name if store else None, "evaluator": evaluator.name,
                          "evaluator_version": evaluator.version, "evidence": str(args.out)}))


if __name__ == "__main__":
    main()
