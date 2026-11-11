"""Publish a versioned, curated toolbox without copying credentials into code."""

import argparse
import json

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    name = "volt-support-tools"
    profiles = {
        "volt-policy-knowledge": ["knowledge_base_retrieve"],
        "volt-business-tools": [
            "getRecallNotices",
            "getOrderStatus",
            "getReturnWarrantyEligibility",
        ],
    }
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=args.project_endpoint, credential=credential
    ) as project:
        tools = []
        for connection_name, allowed in profiles.items():
            connection = project.connections.get(connection_name)
            tools.append({
                "type": "mcp",
                "name": connection_name,
                "server_label": connection_name,
                "server_url": connection.target,
                "project_connection_id": connection.id,
                "allowed_tools": allowed,
            })
        versions = list(project.toolboxes.list_versions(name))
        matches = [
            version for version in versions
            if [tool.as_dict() for tool in version.tools] == tools
        ]
        if matches:
            version = matches[0]
        else:
            version = project.toolboxes.create_version(
                name,
                tools=tools,
                description=(
                    "Versioned Volt support capabilities. Synthetic business data "
                    "and policy grounding only."
                ),
            )
        if args.publish:
            project.toolboxes.update(name, default_version=version.version)
        endpoint = (
            f"{args.project_endpoint.rstrip('/')}/toolboxes/{name}"
            f"/versions/{version.version}/mcp?api-version=v1"
        )
        print(json.dumps({
            "name": name, "version": version.version,
            "published": args.publish, "endpoint": endpoint,
            "allowed_tools": profiles,
        }, indent=2))


if __name__ == "__main__":
    main()
