"""Fail closed unless a trusted commit and real approval controls are configured."""

import argparse
import os
import re

from promote_demo import REPO, github, github_checks, validate_pr_checks


def validate_environment(environment):
    rules = [r for r in environment.get("protection_rules", []) if r.get("type") == "required_reviewers"]
    if not rules or not rules[0].get("reviewers") or rules[0].get("prevent_self_review") is not True:
        raise ValueError("Configure required reviewers with self-approval disabled before cloud execution.")
    if environment.get("can_admins_bypass") is not False:
        raise ValueError("Disable administrator bypass on the live environment.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull-request", type=int, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--environment", choices=["volt-dev-evaluation", "volt-demo-promotion"], required=True)
    args = parser.parse_args()
    if os.environ.get("VOLT_LIVE_GATE_ENABLED") != "true":
        raise RuntimeError("Cloud activation is disabled. Obtain approval before configuring the live gate.")
    control_token = os.environ.get("VOLT_GATE_READ_TOKEN")
    if not control_token:
        raise RuntimeError("Configure a repository-scoped read-only control token to inspect protection settings.")
    if os.environ.get("GITHUB_REF") != "refs/heads/main" or os.environ.get("GITHUB_REPOSITORY") != REPO:
        raise ValueError("Run the reviewed workflow from this repository's main branch.")
    if not re.fullmatch(r"[a-f0-9]{40}", args.expected_commit):
        raise ValueError("A full reviewed commit SHA is required.")
    pr = github(f"pulls/{args.pull_request}")
    checks = github_checks(args.expected_commit)
    validate_pr_checks(pr, checks, args.expected_commit)
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
