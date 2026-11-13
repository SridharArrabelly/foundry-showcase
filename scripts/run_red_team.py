# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "azure-ai-evaluation[redteam]==1.18.12",
#   "azure-ai-projects==2.10.0",
#   "azure-identity",
# ]
# ///
"""Opt-in DEV red-team scan; isolated SDK dependencies do not alter the agent.

Run with uv run --script scripts/run_red_team.py. --check-sdk is local only.
--execute incurs Azure usage and requires separate operator approval.
"""

import argparse
import asyncio
import json
import threading
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from capture_cases import invoke_versioned

DEV = "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev"


def invoke_agent(project, client, expected_version, text):
    result = invoke_versioned(project, client, "volt-support", expected_version, text)
    if result.model_dump(mode="json").get("status") != "completed":
        raise RuntimeError("Red-team target response did not complete.")
    answer = json.loads(result.output_text).get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("The target did not return a customer answer.")
    return answer, result.model_dump(mode="json")


def read_scorecard(path):
    result = json.loads(path.read_text(encoding="utf-8"))
    scorecard = result.get("redteaming_scorecard")
    if not isinstance(scorecard, dict) or not scorecard.get("risk_category_summary"):
        raise ValueError("The SDK did not produce a complete red-teaming scorecard.")
    return scorecard


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-sdk", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--project-endpoint", default=DEV, choices=[DEV])
    parser.add_argument("--expected-version")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--objectives", type=int, choices=range(1, 6), default=1)
    parser.add_argument("--max-target-calls", type=int, choices=range(1, 101), default=20)
    args = parser.parse_args()
    if not args.check_sdk and (not args.execute or not args.expected_version or not args.out):
        parser.error("Provide --execute, --expected-version and a fresh --out after obtaining usage approval.")
    from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory

    if args.check_sdk:
        print("RedTeam SDK imports successfully; no Azure call performed.")
        return
    args.out.mkdir(parents=True, exist_ok=False)
    receipt = {"status": "in_progress", "agent_version": args.expected_version,
               "project_endpoint": DEV, "objectives_per_category": args.objectives,
               "max_target_calls": args.max_target_calls, "target_calls": 0,
               "target_failures": 0, "budget_exhausted": False}
    receipt_path = args.out / "scan-receipt.json"

    def save():
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    save()
    with DefaultAzureCredential() as credential, AIProjectClient(
        endpoint=DEV, credential=credential, allow_preview=True
    ) as project, project.get_openai_client(
        agent_name="volt-support", timeout=180, max_retries=0
    ) as client:
        version = project.agents.get_version("volt-support", args.expected_version)
        receipt["target_package_sha256"] = version.definition.code_configuration.content_hash
        save()
        lock = threading.Lock()

        def target(query: str) -> str:
            with lock:
                if receipt["target_calls"] >= args.max_target_calls:
                    receipt["budget_exhausted"] = True
                    save()
                    raise RuntimeError("Approved target-call budget exhausted.")
                receipt["target_calls"] += 1
                save()
                try:
                    answer, response = invoke_agent(project, client, args.expected_version, query)
                except Exception:
                    receipt["target_failures"] += 1
                    save()
                    raise
                (args.out / f"target-{receipt['target_calls']:03}.json").write_text(
                    json.dumps({"query": query, "response": response}, indent=2) + "\n", encoding="utf-8"
                )
                return answer

        red_team = RedTeam(
            azure_ai_project=DEV, credential=credential,
            risk_categories=[RiskCategory.Violence, RiskCategory.HateUnfairness,
                             RiskCategory.Sexual, RiskCategory.SelfHarm],
            num_objectives=args.objectives,
        )
        output = args.out / "redteam-results.json"
        await asyncio.wait_for(red_team.scan(
            target=target, scan_name="volt-support-candidate",
            attack_strategies=[AttackStrategy.EASY, AttackStrategy.Jailbreak],
            output_path=str(output),
        ), timeout=1800)
    if receipt["budget_exhausted"] or receipt["target_failures"] or not receipt["target_calls"]:
        raise RuntimeError("Target failures or an exhausted budget prevent a complete scan claim; inspect partial evidence.")
    scorecard = read_scorecard(output)
    (args.out / "scorecard.json").write_text(json.dumps(scorecard, indent=2) + "\n", encoding="utf-8")
    receipt["status"] = "completed-review-required"
    save()
    print(f"Completed scan at {args.out}; inspect attack success rates, not just completion status.")


if __name__ == "__main__":
    asyncio.run(main())
