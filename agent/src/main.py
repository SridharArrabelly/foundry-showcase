# Copyright (c) Microsoft. All rights reserved.

import asyncio
from contextlib import AsyncExitStack

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import FoundryToolbox, ResponsesHostServer
from azure.ai.agentserver.optimization import load_config
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

from preferences import PreferenceMemory
from evidence_contract import EvidenceContract
from response_contract import SupportResponse
from settings import Settings


def create_support_agent(client, tools, instructions, memory=None):
    """The business evidence contract is never optional.

    Previously, enabling Memory *replaced* the EvidenceContract middleware, so a
    Memory-enabled build could emit model-written decisions. Memory now runs
    outside the contract: it may shape context, but the customer-facing decision
    is always rendered from this run's tool evidence.
    """
    middleware = [EvidenceContract()] if memory is None else [memory, EvidenceContract()]
    return Agent(
        client=client, name="VoltSupport", instructions=instructions,
        tools=tools, middleware=middleware,
        default_options={"store": False, "response_format": SupportResponse},
    )


async def main():
    load_dotenv()
    settings = Settings.from_environment()
    config = load_config()
    if not config.model or "/" in config.model:
        raise ValueError("Optimizer model selection must use a deployment within the approved gateway.")
    async with AsyncExitStack() as stack:
        credential = await stack.enter_async_context(DefaultAzureCredential())
        project = await stack.enter_async_context(
            AIProjectClient(endpoint=settings.project_endpoint, credential=credential)
        )
        client = FoundryChatClient(
            project_endpoint=settings.project_endpoint,
            model=f"{settings.model_connection}/{config.model}",
            credential=credential,
        )
        toolbox = FoundryToolbox(credential, url=settings.toolbox_endpoint)
        tools = [toolbox]
        memory = None
        if settings.memory_enabled:
            memory = PreferenceMemory(project)
            tools.extend([memory.remember_response_style, memory.forget_response_style])
        agent = create_support_agent(client, tools, config.compose_instructions(), memory)
        await ResponsesHostServer(agent).run_async()

if __name__ == "__main__":
    asyncio.run(main())
