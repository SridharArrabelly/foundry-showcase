"""The evidence contract must be registered whether or not Memory is enabled."""

import sys
from pathlib import Path

from agent_framework import AgentMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import create_support_agent
from evidence_contract import EvidenceContract


class _FakeMemory(AgentMiddleware):
    async def process(self, context, call_next):
        await call_next()


def _middleware(agent):
    # Agent Framework keeps the registered middleware on the agent; tolerate either attribute name.
    for name in ("middleware", "_middleware", "agent_middleware"):
        value = getattr(agent, name, None)
        if value is not None:
            return list(value)
    raise AssertionError("Could not read registered middleware from the Agent instance.")


def test_contract_registered_without_memory():
    agent = create_support_agent(client=None, tools=[], instructions="x")
    assert any(isinstance(m, EvidenceContract) for m in _middleware(agent))


def test_contract_still_registered_with_memory():
    memory = _FakeMemory()
    agent = create_support_agent(client=None, tools=[], instructions="x", memory=memory)
    registered = _middleware(agent)
    assert any(isinstance(m, EvidenceContract) for m in registered)
    assert memory in registered
