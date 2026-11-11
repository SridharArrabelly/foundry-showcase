import sys
from pathlib import Path

import pytest
from azure.ai.agentserver.core import FoundryAgentRequestContext, reset_request_context, set_request_context

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preferences import caller_scope


def scoped(user_id, session_id):
    token = set_request_context(
        FoundryAgentRequestContext(call_id="opaque-test-call", user_id=user_id, session_id=session_id)
    )
    try:
        return caller_scope()
    finally:
        reset_request_context(token)


def test_scope_is_stable_across_sessions_and_separate_for_callers():
    assert scoped("synthetic-caller-a", "one") == scoped("synthetic-caller-a", "two")
    assert scoped("synthetic-caller-a", "one") != scoped("synthetic-caller-b", "one")


def test_missing_authenticated_context_never_uses_shared_memory():
    token = set_request_context(FoundryAgentRequestContext())
    try:
        with pytest.raises(RuntimeError, match="authenticated caller"):
            caller_scope()
    finally:
        reset_request_context(token)
