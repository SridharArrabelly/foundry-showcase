"""Export a bounded App Insights span tree for one recorded hosted response."""

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--app-id", default="cd5b7842-a755-4fdc-8480-134ad8701c0a")
    args = parser.parse_args()
    record = json.loads(args.capture.read_text(encoding="utf-8"))
    response = record["response"]
    response_id = response["id"]
    if not re.fullmatch(r"caresp_[A-Za-z0-9]+", response_id):
        raise ValueError("Expected a native hosted response ID.")
    created = datetime.fromtimestamp(response["created_at"], timezone.utc)
    start = (created - timedelta(minutes=1)).isoformat()
    end = (created + timedelta(minutes=15)).isoformat()
    query = f"""
let roots = requests
| where timestamp between (datetime({start}) .. datetime({end}))
| where name == 'invoke_agent'
| where tostring(customDimensions['azure.ai.agentserver.response_id']) == '{response_id}'
| distinct operation_Id;
union requests, dependencies
| where timestamp between (datetime({start}) .. datetime({end}))
| where operation_Id in (roots)
| project timestamp, name, duration, success, operation_Id,
    spanId=id, parentSpanId=operation_ParentId,
    operation=tostring(customDimensions['gen_ai.operation.name']),
    model=tostring(customDimensions['gen_ai.request.model']),
    tool=tostring(customDimensions['gen_ai.tool.name']),
    inputTokens=toint(customDimensions['gen_ai.usage.input_tokens']),
    outputTokens=toint(customDimensions['gen_ai.usage.output_tokens'])
| order by timestamp asc
| take 100
""".strip()
    print(f"Project: {record['project_endpoint']}\n```kusto\n{query}\n```", flush=True)
    executable = shutil.which("az")
    if not executable:
        raise RuntimeError("Azure CLI is required for the App Insights query.")
    result = subprocess.run(
        [executable, "monitor", "app-insights", "query", "--app", args.app_id,
         "--analytics-query", " ".join(query.splitlines()), "-o", "json", "--only-show-errors"],
        capture_output=True, text=True, check=True,
    )
    table = json.loads(result.stdout)["tables"][0]
    columns = [column["name"] for column in table["columns"]]
    spans = [dict(zip(columns, row, strict=True)) for row in table["rows"]]
    if not spans:
        raise RuntimeError("No matching exported trace exists; do not present this response as a verified App Insights trace.")
    if len(spans) == 100:
        raise RuntimeError("The span query reached its bound; narrow it before claiming a complete tree.")
    evidence = {
        "kind": "recorded-application-insights-spans",
        "project_endpoint": record["project_endpoint"], "response_id": response_id,
        "application_id": args.app_id, "query": query, "spans": spans,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(spans)} correlated spans to {args.out}")


if __name__ == "__main__":
    main()
