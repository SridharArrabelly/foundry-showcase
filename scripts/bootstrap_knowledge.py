"""Publish the synthetic policies as a real Foundry IQ search-index knowledge source."""

import argparse
import json
from pathlib import Path

import requests
from azure.identity import DefaultAzureCredential

ROOT = Path(__file__).resolve().parents[1]
API_VERSION = "2026-08-01-preview"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-endpoint", required=True)
    parser.add_argument("--model-endpoint", required=True)
    parser.add_argument("--source-base-url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    index_name, source_name, base_name = "volt-policies", "volt-policy-source", "volt-support-knowledge"
    with DefaultAzureCredential() as credential, requests.Session() as session:
        def call(method: str, path: str, body: dict | None = None) -> dict:
            response = session.request(
                method,
                f"{args.search_endpoint.rstrip('/')}/{path}",
                params={"api-version": API_VERSION},
                headers={"Authorization": f"Bearer {credential.get_token('https://search.azure.com/.default').token}"},
                json=body,
                timeout=90,
            )
            response.raise_for_status()
            return response.json()

        call("PUT", f"indexes/{index_name}", {
            "name": index_name,
            "description": "Synthetic Volt replacement policy and recall notice; no customer data.",
            "fields": [
                {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
                {"name": "title", "type": "Edm.String", "searchable": True, "retrievable": True},
                {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True},
                {"name": "reference", "type": "Edm.String", "searchable": True, "retrievable": True},
                {"name": "url", "type": "Edm.String", "retrievable": True},
            ],
            "semantic": {
                "defaultConfiguration": "volt-policy-semantic",
                "configurations": [{
                    "name": "volt-policy-semantic",
                    "prioritizedFields": {
                        "titleField": {"fieldName": "title"},
                        "prioritizedContentFields": [{"fieldName": "content"}],
                        "prioritizedKeywordsFields": [{"fieldName": "reference"}],
                    },
                }],
            },
        })
        documents = []
        for filename, reference in (
            ("replacement-policy.md", "VOLT-REPLACEMENT-2026-11"),
            ("recall-notice.md", "SYNTHETIC-RECALL-001"),
        ):
            content = (ROOT / "knowledge" / filename).read_text(encoding="utf-8")
            documents.append({
                "@search.action": "mergeOrUpload",
                "id": reference,
                "title": content.splitlines()[0].removeprefix("# "),
                "content": content,
                "reference": reference,
                "url": f"{args.source_base_url.rstrip('/')}/{filename}",
            })
        indexed = call("POST", f"indexes/{index_name}/docs/index", {"value": documents})
        if len(indexed.get("value", [])) != len(documents) or any(
            not row["status"] for row in indexed["value"]
        ):
            raise RuntimeError(f"Policy ingestion failed: {indexed}")
        source = call("PUT", f"knowledgesources/{source_name}", {
            "name": source_name,
            "kind": "searchIndex",
            "description": "Authoritative synthetic Volt policy documents for the internal showcase.",
            "searchIndexParameters": {
                "searchIndexName": index_name,
                "semanticConfigurationName": "volt-policy-semantic",
                "sourceDataFields": [{"name": name} for name in ("title", "content", "reference", "url")],
            },
        })
        knowledge = call("PUT", f"knowledgebases/{base_name}", {
            "name": base_name,
            "description": "Volt support policy evidence. This is a fictional demonstration.",
            "retrievalInstructions": "Retrieve the relevant replacement policy and recall notice. Preserve their reference identifiers.",
            "outputMode": "extractiveData",
            "knowledgeSources": [{"name": source_name}],
            "models": [{
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": args.model_endpoint,
                    "deploymentId": "gpt-5.4-mini",
                    "modelName": "gpt-5.4-mini",
                },
            }],
            "retrievalReasoningEffort": {"kind": "low"},
        })
        result = {
            "index": index_name,
            "knowledge_source": source,
            "knowledge_base": knowledge,
            "mcp_endpoint": f"{args.search_endpoint.rstrip('/')}/knowledgebases/{base_name}/mcp?api-version={API_VERSION}",
            "indexed_documents": len(documents),
            "retrieval_verified": False,
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"index": index_name, "knowledge_base": base_name, "documents": len(documents),
                          "next": "Verify retrieval through the authenticated toolbox."}))


if __name__ == "__main__":
    main()
