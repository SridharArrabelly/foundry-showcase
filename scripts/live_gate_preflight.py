"""Fail closed unless a trusted commit and real approval controls are configured."""

import argparse
import json
import os
import re
from pathlib import Path

from promote_demo import REPO, github, github_checks, validate_pr_checks


def validate_environment(environment):
    rules = [r for r in environment.get("protection_rules", []) if r.get("type") == "required_reviewers"]
    if not rules or not rules[0].get("reviewers") or rules[0].get("prevent_self_review") is not True:
        raise ValueError("Configure required reviewers with self-approval disabled before cloud execution.")
    if environment.get("can_admins_bypass") is not False:
        raise ValueError("Disable administrator bypass on the live environment.")


def validate_workflow_context(environment, pr_number=None, commit=None, pr=None, *, env=None, event=None):
    env = os.environ if env is None else env
    if env.get("GITHUB_REPOSITORY") != REPO:
        raise ValueError("Run from the approved repository.")
    name, ref = env.get("GITHUB_EVENT_NAME"), env.get("GITHUB_REF")
    if name == "pull_request":
        supplied = (event or {}).get("pull_request", {})
        if (environment != "volt-dev-evaluation"
                or ref != f"refs/pull/{pr_number}/merge"
                or (event or {}).get("number") != pr_number
                or supplied.get("head", {}).get("sha") != commit
                or supplied.get("head", {}).get("repo", {}).get("full_name") != REPO
                or supplied.get("base", {}).get("ref") != "main"):
            raise ValueError("PR event does not match the reviewed same-repository candidate.")
    elif name in ("workflow_dispatch", "push", "schedule"):
        if ref != "refs/heads/main":
            raise ValueError("Run this operation from main.")
        if name == "push" and (
            environment != "volt-demo-promotion"
            or not pr or pr.get("merge_commit_sha") != env.get("GITHUB_SHA")
        ):
            raise ValueError("Release push must identify the exact merged PR.")
        if name == "schedule" and environment != "volt-demo-monitoring":
            raise ValueError("Scheduled events are for monitoring only.")
    else:
        raise ValueError("Unsupported workflow event; no cloud execution authorized.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull-request", type=int)
    parser.add_argument("--expected-commit")
    parser.add_argument("--environment", choices=["volt-dev-evaluation", "volt-demo-promotion", "volt-demo-monitoring"], required=True)
    args = parser.parse_args()
    if os.environ.get("VOLT_LIVE_GATE_ENABLED") != "true":
        raise RuntimeError("Cloud activation is disabled. Obtain approval before configuring the live gate.")
    control_token = os.environ.get("VOLT_GATE_READ_TOKEN")
    if not control_token:
        raise RuntimeError("Configure a repository-scoped read-only control token to inspect protection settings.")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    event = json.loads(Path(event_path).read_text(encoding="utf-8")) if event_path else {}
    if args.environment == "volt-demo-monitoring":
        if os.environ.get("VOLT_PRODUCTION_WATCH_ENABLED") != "true":
            raise RuntimeError("Scheduled monitoring needs its own explicit activation.")
        validate_workflow_context(args.environment, event=event)
        validate_environment(github(f"environments/{args.environment}", token=control_token))
        print("Monitoring approval configuration verified; no Azure call performed.")
        return
    if not args.pull_request or not re.fullmatch(r"[a-f0-9]{40}", args.expected_commit or ""):
        raise ValueError("A full reviewed commit SHA is required.")
    pr = github(f"pulls/{args.pull_request}")
    validate_workflow_context(args.environment, args.pull_request, args.expected_commit, pr, event=event)
    checks = github_checks(args.expected_commit)
    required = ("unit-and-contract-tests",) if os.environ.get("GITHUB_EVENT_NAME") == "pull_request" else ("contracts",)
    validate_pr_checks(pr, checks, args.expected_commit, required_checks=required)
    if args.environment == "volt-demo-promotion" and not pr["merged"]:
        raise ValueError("The exact evaluated PR must be merged before DEMO promotion.")
    validate_environment(github(f"environments/{args.environment}", token=control_token))
    protection = github("branches/main/protection/required_status_checks", token=control_token)
    contexts = set(protection.get("contexts", [])) | {c["context"] for c in protection.get("checks", [])}
    if "volt/live-behavior" not in contexts:
        raise ValueError("Require volt/live-behavior on main before calling this an enforced PR gate.")
    print(f"Approved configuration verified for PR {args.pull_request} at {args.expected_commit}.")


if __name__ == "__main__":
    main()
