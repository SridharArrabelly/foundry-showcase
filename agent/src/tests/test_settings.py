import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from settings import Settings


@pytest.fixture
def configured(monkeypatch):
    values = {
        "AZURE_AI_PROJECT_ENDPOINT": "https://volt.services.ai.azure.com/api/projects/dev",
        "VOLT_MODEL_CONNECTION": "volt-models-LLM",
        "TOOLBOX_ENDPOINT": "https://volt.services.ai.azure.com/api/projects/dev/toolboxes/volt/versions/1/mcp?api-version=v1",
    }
    monkeypatch.delenv("FOUNDRY_PROJECT_ENDPOINT", raising=False)
    for name, value in values.items():
        monkeypatch.setenv(name, value)
    return values


def test_missing_gateway_cannot_fall_back_to_direct_model(configured, monkeypatch):
    monkeypatch.delenv("VOLT_MODEL_CONNECTION")
    with pytest.raises(ValueError, match="VOLT_MODEL_CONNECTION"):
        Settings.from_environment()


def test_rejects_direct_model_and_embedded_secrets(configured, monkeypatch):
    monkeypatch.setenv("VOLT_MODEL_CONNECTION", "https://model.openai.azure.com")
    with pytest.raises(ValueError, match="managed gateway"):
        Settings.from_environment()
    monkeypatch.setenv("TOOLBOX_ENDPOINT", "https://user:secret@volt.services.ai.azure.com")
    with pytest.raises(ValueError, match="embedded credentials"):
        Settings.from_environment()


def test_rejects_unpinned_or_cross_project_toolbox(configured, monkeypatch):
    for endpoint in (
        configured["TOOLBOX_ENDPOINT"].replace("/versions/1", ""),
        configured["TOOLBOX_ENDPOINT"].replace("/projects/dev", "/projects/another"),
    ):
        monkeypatch.setenv("TOOLBOX_ENDPOINT", endpoint)
        with pytest.raises(ValueError, match="Pin a toolbox"):
            Settings.from_environment()
