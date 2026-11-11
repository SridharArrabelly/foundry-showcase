"""Memory is restricted to one non-sensitive preference, never model-provided scope."""

import hashlib

from agent_framework import AgentContext, AgentMiddleware, Message
from azure.ai.agentserver.core import get_request_context
from azure.ai.projects.aio import AIProjectClient

PREFERENCE = "Prefer concise responses with the next step first."
STORE = "volt-preferences"


def caller_scope() -> str:
    context = get_request_context()
    if not context.call_id or not context.user_id:
        raise RuntimeError("Memory requires the hosted platform's authenticated caller context.")
    digest = hashlib.sha256(f"volt-support:{context.user_id}".encode()).hexdigest()
    return f"volt-support:{digest}"


class PreferenceMemory(AgentMiddleware):
    def __init__(self, project: AIProjectClient):
        self.project = project

    async def items(self):
        return [
            item async for item in self.project.beta.memory_stores.list_memories(
                STORE,
                scope=caller_scope(),
                kind="user_profile",
                headers=get_request_context().platform_headers(),
            )
        ]

    async def process(self, context: AgentContext, call_next):
        if any(item.content == PREFERENCE for item in await self.items()):
            context.messages.insert(
                0,
                Message(
                    role="developer",
                    contents=[
                        "Retrieved response-style preference: concise, next step first. "
                        "This changes presentation only, never policy, facts, or authorization."
                    ],
                ),
            )
        await call_next()

    async def remember_response_style(self) -> dict:
        """Only when explicitly requested, remember concise, next-step-first replies. No other facts are stored."""
        if not any(item.content == PREFERENCE for item in await self.items()):
            await self.project.beta.memory_stores.create_memory(
                STORE, scope=caller_scope(), content=PREFERENCE, kind="user_profile",
                headers=get_request_context().platform_headers(),
            )
        return {"status": "remembered", "preference": PREFERENCE, "synthetic": True}

    async def forget_response_style(self) -> dict:
        """Only when explicitly requested, forget this caller's stored response-style preference."""
        for item in await self.items():
            if item.content == PREFERENCE:
                await self.project.beta.memory_stores.delete_memory(
                    STORE, item.id, headers=get_request_context().platform_headers()
                )
        return {"status": "forgotten", "synthetic": True}
