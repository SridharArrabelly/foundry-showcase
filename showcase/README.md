# Volt Citadel internal enablement

This is the separate, preview-inclusive 90-minute showcase under construction.
The original agent and presentation at the repository root are retained as a fallback.
Nothing in this directory is a claim of customer-production readiness.

## What is implemented

- Pinned Citadel Governance Hub parameters for a small, single-region deployment.
- Separate Foundry `volt-dev` and production-like `volt-demo` projects.
- Agent Framework Responses host with an optimizer baseline, a versioned toolbox
  binding, and mandatory APIM model routing through a managed Foundry connection.
  There is no direct-model fallback or runtime Key Vault credential lookup.
- Read-only Volt business API reusing the original catalog and recall functions.
- Synthetic replacement policy and recall documents, plus real IQ bootstrap code.
- Native Foundry business-contract evaluator and restricted memory-store setup.

The model gateway, IQ retrieval and six business-tool cases through the complete
Foundry Toolbox / APIM / Functions path have been exercised against Azure.
The first hosted customer journey executed all four tools and returned policy
citations. A native business evaluation of nine captured v1 responses completed
with **8 passed, 1 failed, 0 errored**. The failing replacement answer sounded
correct but used `decision: recommendation` while the eligibility tool returned
`eligible`. This is a genuine observed contract defect, not a seeded safety error.
Fresh model responses can vary; the recording preserves the original incident.
The harmless guardrail marker produced a native HTTP 400 `content_filter`.

The focused fix in PR #2 has a complete native v6 evaluation: **9 passed, 0
failed, 0 errored**, using the same evaluator and unchanged nine-case dataset.
One invocation initially failed with a model-service error; its evidence was
preserved and that case retried once. Business grading of completed responses
is not an availability measurement. The native status is attached to the exact
PR commit; the PR is ready for human review, not merged or promoted to DEMO.

Native Memory now passes remember, cross-conversation recall, forget and native
deletion checks for one authenticated caller. A second-identity test remains
pending; do not claim independent per-user authorization from a scope string.
Optimizer, DEMO promotion and the full release rehearsal remain unfinished.
The replacement presentation has been built and visually reviewed, but its
remaining live-demo bindings are still being completed.

## Environment and costs

The approved subscription is `40b687ca-31b5-4374-bea2-4c178369b9c0`, tenant
`b1cd5b73-a77b-4002-a5a6-1599e4c4ee37`, resource group `rg-volt-citadel`,
region Sweden Central. The three model deployments use Data Zone Standard;
the account location alone is not a Sweden-only processing guarantee.

APIM Developer has no production SLA. Hub/search base resources were estimated
at approximately USD 12-18/day at public retail pricing, excluding metered
hosting, inference, memory, evaluation, optimization, tax and other usage.
This estimate is not a spending cap. Resources continue billing until removed.

The user approved authenticated public access for the **new** Foundry account.
`scripts\Set-DemoNetwork.ps1` applies this explicit overlay and disables key-based
Foundry authentication. The pinned upstream template otherwise hard-codes
`networkAcls.defaultAction = Deny`, even when public networking is enabled.
Reapply the approved overlay after any hub redeployment. Do not apply it to the
original account or treat this demo as an entirely private-network implementation.

## Reproducible foundations

Prerequisites: authenticated Azure CLI and Azure Developer CLI, PowerShell,
Python 3.13, uv, Bicep, and the Foundry azd extensions. Use the existing signed-in
tenant; the scripts do not log in or change the subscription automatically.

From the repository root:

```powershell
.\showcase\scripts\Get-CitadelSource.ps1
az bicep build-params --file .\showcase\infra\hub.bicepparam --outfile .\.runtime\volt-hub.parameters.json

Push-Location .\showcase\tools
uv sync --python 3.13
uv run python -m pytest -q
uv export --no-dev --no-hashes --no-emit-project --format requirements-txt --output-file requirements.txt
uv run python ..\scripts\package_tools.py
Pop-Location

Push-Location .\showcase\volt-support\src\agent-framework-agent-basic-responses
uv sync --python 3.13
uv run python -m pytest -q
uv run python -m pytest ..\..\..\evaluators -q
Pop-Location
```

The function ZIP includes only authored API files and the existing canonical
`volt` domain package; no local environment or credentials are packaged.
The hosted agent uses a pinned `requirements.txt` export for the remote builder.
`bootstrap_toolbox.py` uses the SDK's `allowed_tools` field, which the CLI's
connection-add command does not expose, to curate the three support operations
and one IQ retrieval tool. The REST backend retains the original catalog and
compatibility operations, but they are not exposed by this support toolbox.
Toolbox curation is not a substitute for backend authorization. Toolbox callers
authenticate with Entra; the APIM and Function hops use centrally managed scoped
credentials. This synthetic API does not implement real customer order ownership.

The published read-only API uses GET operations. Recall lookup puts the required
product identifier in the resource path and the optional batch in the query.
This avoids two observed native REST-to-MCP mapping problems: a single JSON
argument was forwarded as a raw scalar, and a required query placeholder plus
an optional query produced two `?` delimiters. The original POST handler remains
available for compatibility; it is not the published MCP transport.
`probe_toolbox.py` checks actual domain outcomes, because an HTTP 400 backend
response can still arrive inside an MCP result with `isError: false`.

Foundry custom-evaluator registration requires the explicit
`Foundry-Features: Evaluations=V1Preview` request header in this SDK/API path.
`scripts\bootstrap_foundry.py` supplies it. The same grader is tested locally.
Fluent prose without the correct structured decision and observed tool call
does not pass the business metric.

Memory stores retain only synthetic response-style preferences for seven days.
Conversation summaries and procedural memory are disabled. Scope partitioning
is application logic, not an independent RBAC boundary. End-user identity
provenance and isolation require additional verification before production.

Memory also has a model-authorization dependency. The runtime and caller use
project-scoped roles, while the project's managed identity needs model access on
the Foundry account. This cost-controlled DEV/DEMO profile shares that account;
it is not a hard production isolation boundary. Native Memory/model-service
traffic is not covered by the customer agent's APIM token budget. Review separate
accounts and narrower role requirements before applying this profile to production.

The Memory proof pins native sessions to v5, where Memory is enabled. The current
endpoint is v6, where it is disabled. A preview metadata discrepancy was observed:
the returned session ID and native session readback identify v5, but the response's
`agent_reference.version` reports v6. `probe_memory.py` preserves both, warns
explicitly and verifies the native item and deletion independently. The business
capture gate remains stricter and rejects a response-version mismatch.

## Replaying the verified evidence

`recordings\baseline-v1.json` and `recordings\candidate-v6.json` are labeled
recordings of real hosted calls, not live demonstrations or future guarantees.
The candidate export also records the failed invocation separately.

From the repository root, using the existing agent virtual environment:

```powershell
$python = ".\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe"
$endpoint = "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev"
$root = ".\showcase\volt-support\src\agent-framework-agent-basic-responses"

& $python .\showcase\scripts\probe_memory.py `
  --project-endpoint $endpoint --expected-version 5 `
  --out .\.runtime\memory-rehearsal

& $python .\showcase\scripts\capture_cases.py `
  --project-endpoint $endpoint --expected-version 6 `
  --dataset "$root\.foundry\datasets\volt-regression.jsonl" `
  --out "$root\.foundry\results\rehearsal-v6" --pause-seconds 60

& $python .\showcase\scripts\evaluate_captures.py `
  --project-endpoint $endpoint `
  --captures "$root\.foundry\results\rehearsal-v6\captured.jsonl" `
  --dataset "$root\.foundry\datasets\volt-regression.jsonl" `
  --label "Rehearsal v6" `
  --out "$root\.foundry\results\rehearsal-v6\evaluation.json" `
  --eval-id eval_5a3774acf4f347e1bd35ae30375d0f2d --require-all-pass
```

These commands incur usage. Run evaluation only after capture succeeds. Cached
matching responses are reused; incomplete or altered datasets fail the gate.
Existing evaluation receipts prevent accidental resubmission. Use new explicitly
named output directories for a fresh rehearsal, rather than deleting evidence.
Current source commit/package lineage is in the PR and native evaluation metadata;
pass `--deployment-receipt` when validating a newly packaged candidate.

## Provenance

The hub source is pinned in `infra\citadel-source.json`; it is restored under the
ignored `.runtime` directory rather than copied into the deliverable.
`Get-CitadelSource.ps1` applies reviewed patches: the Foundry compatibility
fragment is required even when optional PII redaction is off, and disabled LLM
diagnostics must not dereference or emit message-capture settings.
The source restore fails if neither the original nor already-patched hunk matches.
LLM diagnostic content capture is disabled without setting unsupported `messages`
values. The subscription's `StorageAccount_PublicNetwork_Modify` policy enforces
private storage. The workload keeps that control and uses a dedicated Functions
integration subnet plus blob/queue/table private endpoints. Shared keys and public
blob access remain disabled; no policy exemption or bypass tag is applied.
The Responses host was scaffolded with the official
`microsoft-foundry/foundry-samples` Agent Framework Responses sample and adapted
using Microsoft's hosted-toolbox and optimizer patterns.
