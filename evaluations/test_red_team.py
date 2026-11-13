import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_red_team import invoke_agent, read_scorecard


def target_clients(**changes):
    session = SimpleNamespace(agent_session_id="session", version_indicator=SimpleNamespace(agent_version="7"))
    data = {"agent_session_id": "session", "agent_reference": {"name": "volt-support", "version": "7"},
            "status": "completed", **changes}
    result = Mock(output_text=json.dumps({"answer": "No action has been performed."}))
    result.model_dump.return_value = data
    project, client = Mock(), Mock()
    project.agents.create_session.return_value = session
    client.conversations.create.return_value = SimpleNamespace(id="conversation")
    client.responses.create.return_value = result
    return project, client


def test_red_team_adapter_invokes_the_version_bound_agent_and_returns_actual_text():
    project, client = target_clients()
    answer, data = invoke_agent(project, client, "7", "Synthetic probe.")
    assert answer == "No action has been performed."
    assert data["agent_reference"]["version"] == "7"
    client.responses.create.assert_called_once_with(
        input="Synthetic probe.", conversation={"id": "conversation"},
        extra_body={"agent_session_id": "session"},
    )


@pytest.mark.parametrize("changes", [
    {"agent_session_id": "other"},
    {"agent_reference": {"name": "volt-support", "version": "8"}},
    {"status": "failed"},
])
def test_red_team_adapter_rejects_wrong_lineage_or_failed_responses(changes):
    with pytest.raises(RuntimeError):
        invoke_agent(*target_clients(**changes), "7", "Synthetic probe.")


def test_red_team_scorecard_cannot_be_a_null_success(tmp_path):
    path = tmp_path / "scorecard.json"
    path.write_text('{"redteaming_scorecard": null}')
    with pytest.raises(ValueError, match="complete"):
        read_scorecard(path)
    result = {"risk_category_summary": [{"overall_asr": 0.1}]}
    path.write_text(json.dumps({"redteaming_scorecard": result}))
    assert read_scorecard(path) == result
