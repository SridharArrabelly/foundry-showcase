"""Bounded AI red-teaming scan of the DEV candidate (Prove stage of the inner loop).

Uses the Azure AI Evaluation SDK's AI Red Teaming Agent (preview). Verify the import
path and parameters against your installed `azure-ai-evaluation[redteam]` version
before first use; preview APIs change.

    uv add "azure-ai-evaluation[redteam]"
    uv run python ../../scripts/run_red_team.py --project-endpoint <DEV project endpoint> \
        --expected-version <n> --out ../../.runtime/case-file/redteam --objectives 5

The scorecard (attack success rate per risk category and strategy) goes into the case
file next to the business and action-truthfulness results.
"""

import argparse
import asyncio
import json
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory


def invoke_agent(project_endpoint: str, expected_version: str, text: str) -> str:
    """ADAPTER: call the hosted volt-support agent once and return its customer text.

    Reuse the exact invocation code from scripts/capture_cases.py (same endpoint,
    same version pinning, same authentication) so the red-team traffic hits the
    candidate the gate evaluates. Return the `answer` field of the SupportResponse.
    """
    raise NotImplementedError("Wire this to the invocation helper used by capture_cases.py")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-endpoint", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--objectives", type=int, default=5)
    args = parser.parse_args()

    def target(query: str) -> str:
        return invoke_agent(args.project_endpoint, args.expected_version, query)

    red_team = RedTeam(
        azure_ai_project=args.project_endpoint,
        credential=DefaultAzureCredential(),
        risk_categories=[RiskCategory.Violence, RiskCategory.HateUnfairness,
                         RiskCategory.Sexual, RiskCategory.SelfHarm],
        num_objectives=args.objectives,
    )
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    result = await red_team.scan(
        target=target,
        scan_name="volt-support-candidate",
        attack_strategies=[AttackStrategy.EASY, AttackStrategy.Jailbreak],
        output_path=str(out / "redteam-results.json"),
    )
    scorecard = getattr(result, "scan_result", None) or getattr(result, "to_scorecard", lambda: None)()
    (out / "scorecard.json").write_text(json.dumps(scorecard, indent=2, default=str))
    print(f"Red-team scorecard written to {out / 'scorecard.json'}")


if __name__ == "__main__":
    asyncio.run(main())
