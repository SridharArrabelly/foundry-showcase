import copy
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from promote_demo import REPO, validate_pr_checks
from live_gate_preflight import validate_environment, validate_workflow_context
from score_action_claims import RUBRIC, CALIBRATION, verify_action_gate
from validate_live_release import DEV, DEMO, validation_endpoint
import prepare_candidate


def test_current_main_target_uses_contracts_and_rejects_stale_green_rerun():
    pr = {"head": {"sha": "abc", "repo": {"full_name": REPO}}, "base": {"ref": "main"}, "draft": False}
    success = {"id": 1, "name": "contracts", "status": "completed", "conclusion": "success",
               "app": {"slug": "github-actions"}}
    validate_pr_checks(pr, [success], "abc")
    with pytest.raises(ValueError, match="Latest"):
        validate_pr_checks(pr, [success, {**success, "id": 2, "conclusion": "failure"}], "abc")
    with pytest.raises(ValueError, match="trusted"):
        validate_pr_checks({**pr, "head": {"sha": "abc", "repo": {"full_name": "fork/untrusted"}}}, [success], "abc")


def test_workflow_context_binds_pr_events_to_the_reviewed_head_and_dev_only():
    env = {"GITHUB_REPOSITORY": REPO, "GITHUB_EVENT_NAME": "pull_request",
           "GITHUB_REF": "refs/pull/5/merge"}
    event = {"number": 5, "pull_request": {
        "head": {"sha": "head", "repo": {"full_name": REPO}}, "base": {"ref": "main"}}}
    validate_workflow_context("volt-dev-evaluation", 5, "head", env=env, event=event)
    for environment, number, commit in [
        ("volt-demo-promotion", 5, "head"), ("volt-dev-evaluation", 6, "head"),
        ("volt-dev-evaluation", 5, "stale"),
    ]:
        with pytest.raises(ValueError, match="PR event"):
            validate_workflow_context(environment, number, commit, env=env, event=event)
    fork = copy.deepcopy(event)
    fork["pull_request"]["head"]["repo"]["full_name"] = "fork/untrusted"
    with pytest.raises(ValueError, match="PR event"):
        validate_workflow_context("volt-dev-evaluation", 5, "head", env=env, event=fork)


def test_release_push_and_scheduled_watch_have_distinct_trusted_contexts():
    env = {"GITHUB_REPOSITORY": REPO, "GITHUB_REF": "refs/heads/main",
           "GITHUB_EVENT_NAME": "push", "GITHUB_SHA": "merged"}
    validate_workflow_context("volt-demo-promotion", pr={"merge_commit_sha": "merged"}, env=env)
    with pytest.raises(ValueError, match="exact merged PR"):
        validate_workflow_context("volt-demo-promotion", pr={"merge_commit_sha": "old"}, env=env)
    scheduled = {**env, "GITHUB_EVENT_NAME": "schedule"}
    validate_workflow_context("volt-demo-monitoring", env=scheduled)
    with pytest.raises(ValueError, match="monitoring only"):
        validate_workflow_context("volt-dev-evaluation", env=scheduled)
    with pytest.raises(ValueError, match="from main"):
        validate_workflow_context("volt-demo-monitoring", env={**scheduled, "GITHUB_REF": "refs/heads/feature"})


def test_automatic_workflows_cannot_reach_azure_before_explicit_activation():
    workflows = Path(__file__).resolve().parents[1] / ".github/workflows"
    for filename, job_name in [
        ("agent-pr-gate.yml", "live-evaluation"), ("agent-release.yml", "promote"),
        ("production-watch.yml", "watch"),
    ]:
        workflow = yaml.load((workflows / filename).read_text(), Loader=yaml.BaseLoader)
        job = workflow["jobs"][job_name]
        assert "vars.VOLT_LIVE_GATE_ENABLED == 'true'" in job["if"]
        assert workflow["env"]["VOLT_LIVE_GATE_ENABLED"] == "${{ vars.VOLT_LIVE_GATE_ENABLED }}"
        steps = job["steps"]
        preflight = next(i for i, step in enumerate(steps) if "live_gate_preflight.py" in step.get("run", ""))
        login = next(i for i, step in enumerate(steps) if step.get("uses") == "azure/login@v2")
        assert preflight < login
        if job_name == "watch":
            assert "vars.VOLT_PRODUCTION_WATCH_ENABLED == 'true'" in job["if"]
    gate = yaml.load((workflows / "agent-pr-gate.yml").read_text(), Loader=yaml.BaseLoader)
    assert "paths" not in gate["on"]["pull_request"]


def test_an_environment_name_is_not_an_approval_gate():
    with pytest.raises(ValueError, match="required reviewers"):
        validate_environment({"name": "volt-dev-evaluation", "protection_rules": []})
    valid = {"can_admins_bypass": False, "protection_rules": [
        {"type": "required_reviewers", "reviewers": [{"type": "User", "reviewer": {"id": 123}}],
         "prevent_self_review": True}]}
    validate_environment(valid)
    with pytest.raises(ValueError, match="bypass"):
        validate_environment({**valid, "can_admins_bypass": True})


def test_action_gate_requires_current_rubric_calibration_and_complete_cases():
    calibration = [json.loads(line) for line in CALIBRATION.read_text().splitlines()]
    receipt = {
        "status": "passed", "source_commit": "commit", "package_sha256": "digest",
        "model": "gpt-5.4-mini",
        "rubric_sha256": hashlib.sha256(RUBRIC.read_bytes()).hexdigest(),
        "calibration_sha256": hashlib.sha256(CALIBRATION.read_bytes()).hexdigest(),
        "calibration": [{"id": row["id"], "passed": row["expected_pass"]} for row in calibration],
        "cases": [{"id": "test", "passed": True, "reason": "Advice only.", "evidence": "Contact support.", "response_id": "response"}],
    }
    verify_action_gate(receipt, [{"id": "test"}], "commit", "digest")
    invalid = copy.deepcopy(receipt)
    invalid["calibration"][0]["passed"] = True
    with pytest.raises(ValueError, match="calibration"):
        verify_action_gate(invalid, [{"id": "test"}], "commit", "digest")
    with pytest.raises(ValueError, match="every case"):
        verify_action_gate({**receipt, "cases": []}, [{"id": "test"}], "commit", "digest")
    with pytest.raises(ValueError, match="evidence"):
        verify_action_gate({**receipt, "cases": [{**receipt["cases"][0], "evidence": ""}]},
                           [{"id": "test"}], "commit", "digest")
    with pytest.raises(ValueError, match="reviewed rubric"):
        verify_action_gate({**receipt, "model": "unreviewed-model"}, [{"id": "test"}], "commit", "digest")


def test_validation_rejects_wrong_project_or_unverified_deployment_before_billed_work():
    receipt = {"status": "deployed-hash-verified", "project_endpoint": DEV,
               "memory_enabled": False, "agent_version": "7", "source_commit": "commit",
               "package_sha256": "digest"}
    assert validation_endpoint(receipt, "dev") == DEV
    with pytest.raises(ValueError, match="selected environment"):
        validation_endpoint(receipt, "demo")
    with pytest.raises(ValueError, match="verified package"):
        validation_endpoint({**receipt, "status": "submitting"}, "dev")
    promotion = {**receipt, "status": "package-verified-smoke-pending", "target_project": DEMO}
    assert validation_endpoint(promotion, "demo") == DEMO


def test_candidate_packages_committed_runtime_not_tests_or_environment(monkeypatch, tmp_path):
    files = {
        "agent/src/main.py": b"from evidence_contract import EvidenceContract\n",
        "agent/src/evidence_contract.py": b"class EvidenceContract: pass\n",
        "agent/src/.agent_configs/baseline/instructions.md": b"Read-only support.",
        "agent/src/requirements.txt": b"example==1\n",
        "agent/src/.env": b"PRIVATE_TEST_SENTINEL=not-for-packaging\n",
        "agent/src/tests/test_runtime.py": b"assert True\n",
    }

    def committed_git(*args):
        if args == ("rev-parse", "HEAD"):
            return b"commit\n"
        if args == ("status", "--porcelain"):
            return b""
        if args == ("ls-files", "-z", "--", "agent/src"):
            return ("\0".join(files) + "\0").encode()
        if args[0] == "show":
            revision, path = args[1].split(":", 1)
            assert revision == "commit"
            return files[path]
        raise AssertionError(args)

    monkeypatch.setattr(prepare_candidate, "git", committed_git)
    for folder in ("first", "second"):
        out = tmp_path / folder
        monkeypatch.setattr(sys, "argv", ["prepare_candidate.py", "--expected-commit", "commit", "--out", str(out)])
        prepare_candidate.main()
        with zipfile.ZipFile(out / "agent.zip") as archive:
            assert set(archive.namelist()) == {
                "main.py", "evidence_contract.py", ".agent_configs/baseline/instructions.md", "requirements.txt",
            }
            assert archive.read("evidence_contract.py") == files["agent/src/evidence_contract.py"]
        receipt = json.loads((out / "deployment.json").read_text())
        assert receipt["status"] == "packaged-not-deployed"
        assert receipt["package_sha256"] == hashlib.sha256((out / "agent.zip").read_bytes()).hexdigest()
    assert (tmp_path / "first/agent.zip").read_bytes() == (tmp_path / "second/agent.zip").read_bytes()
