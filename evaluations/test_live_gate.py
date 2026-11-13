import copy
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from promote_demo import REPO, validate_pr_checks
from live_gate_preflight import validate_environment
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
