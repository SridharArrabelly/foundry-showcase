# Volt support hosted agent

The customer runtime uses Microsoft Agent Framework and the Foundry Responses
hosting protocol. GitHub Copilot is the development assistant, not a coding
harness exposed to customers.

The agent binds to the separately provisioned Citadel DEV project. **Do not run
`azd provision` in this folder to create another Foundry account.** Infrastructure
is managed by `..\infra`; use `azd deploy volt-support` after its prerequisites
and environment bindings have been verified.

Model inference uses the managed Foundry connection `volt-models-LLM`, which
routes through the Citadel APIM access contract. The model reference is always
`<connection>/<deployment>`; there is no direct-model fallback. Foundry resolves
the gateway credentials, so the agent does not need network access to Key Vault
or a subscription key in its environment.

## Required environment

| Name | Meaning |
|---|---|
| `AZURE_AI_PROJECT_ENDPOINT` | Selected project endpoint for local development; the platform injects `FOUNDRY_PROJECT_ENDPOINT` when hosted. |
| `AZURE_AI_PROJECT_ID` | Azure-resolved project resource ID used by azd. |
| `VOLT_MODEL_CONNECTION` | `volt-models-LLM` in DEV. |
| `TOOLBOX_ENDPOINT` | Exact versioned MCP endpoint in the same project. |
| `VOLT_MEMORY_ENABLED` | `false` locally and for isolated quality/optimization runs; enable for authenticated memory exercises. |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Telemetry binding, held only in ignored local/deployment configuration. |

The guardrail's Azure-resolved full ARM ID is bound explicitly in `azure.yaml`
under `policies[].raiPolicyName`. This azd definition uses camelCase; the
published agent uses `rai_config.rai_policy_name`. Do not assume arbitrary
manifest fields expand `${...}` like environment-variable bindings do.

On a fresh clone, use `..\scripts\bootstrap_agent.py --project-id <Azure-resolved-ID>
--model-deployment gpt-5.4-mini` with the runtime's Python environment. It uses
supported local-template adoption in isolated temporary staging and transfers
azd-generated state back here. It does not hand-author reserved `FOUNDRY_*`
variables, change the global project selection, or provision another account.
Existing compatible bindings are retained. The currently installed CLI requires
its managed `FOUNDRY_PROJECT_ENDPOINT` binding; setting only the legacy
`AZURE_AI_PROJECT_ENDPOINT` is insufficient for deployment.

Memory scope comes from the hosted platform's request context, never a tool
argument or free-form user ID. Only a fixed synthetic response-style preference
can be stored. Missing authenticated context fails closed when memory is enabled.

The authoritative optimizer baseline is `.agent_configs\baseline` beside
`main.py`. Load it with `load_config()`; instruction changes are reviewed like code.
The deployment uses a locked `requirements.txt` export because the remote builder
must not reinterpret `pyproject.toml` as a Poetry project.

See [the operational guide](../docs/OPERATIONS.md) for deployment scope, progress, costs,
policy constraints, provenance, and local validation commands.
