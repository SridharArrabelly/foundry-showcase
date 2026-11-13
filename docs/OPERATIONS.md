# Volt Citadel internal enablement

This is the operational guide for the current, preview-inclusive 90-minute workshop.
The earlier implementation is retained in Git history, not in this checkout.
Its setup instructions do not apply to the current workshop.
Nothing here is a claim of customer-production readiness.

## What is implemented

The evidence-first revision adds a locally tested business response boundary,
additive v2 evaluation and an opt-in behavioral workflow. It has not been
deployed or cloud-validated. [Release activation and remaining approvals](RELEASE-GATE.md)
are separate from the historical results below.
The follow-up keeps the contract enabled even with Memory, adds a second
customer-language escalation case, and introduces automatic PR/release and
scheduled-check workflows. Their activation flags remain unset; merging code
alone does not authorize or activate Azure work.

- Pinned Citadel Governance Hub parameters for a small, single-region deployment.
- Separate Foundry `volt-dev` and production-like `volt-demo` projects.
- Agent Framework Responses host with an optimizer baseline, a versioned toolbox
  binding, and mandatory APIM model routing through a managed Foundry connection.
  There is no direct-model fallback or runtime Key Vault credential lookup.
- Read-only Volt business API with its own canonical fixtures under `tools/volt`.
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

The instruction-only fix in PR #2 has a complete native v6 evaluation: **9 passed, 0
failed, 0 errored**, using the same evaluator and unchanged nine-case dataset.
One invocation initially failed with a model-service error; its evidence was
preserved and that case retried once. Business grading of completed responses
is not an availability measurement. The native status is attached to the exact
PR commit. After explicit human approval, PR #2 was merged into
`feature/volt-citadel`, and the saved ZIP was promoted unchanged to
`volt-demo` / `volt-support` v1. A fresh native DEMO evaluation also passed all
nine cases. Issue #1 is closed. That historical repair targeted the feature branch;
the workshop was later merged to `main` in PR #3.

Native Memory now passes remember, cross-conversation recall, forget and native
deletion checks for one authenticated caller. A second-identity test remains
pending; do not claim independent per-user authorization from a scope string.
Memory is deliberately disabled in DEMO; its runtime has project-only access
without the broader Memory account roles. DEMO's six business-tool checks, two
IQ source documents and native guardrail marker have been verified.

The approved Optimizer retry completed, but retained the baseline at a
task-adherence score of **0.75**: screening found no accepted improvement.
The requested limit was two candidates, not two completed candidates. None was
applied. The first job failed after upstream model throttling and Citadel
circuit-breaker responses. With approval, the mini deployment was increased
from 10 to 50 capacity units (50 requests/minute and 50,000 tokens/minute).
The pay-per-token SKU and model policy stayed unchanged; each APIM application
contract still limits traffic to 20,000 TPM and 500,000 daily tokens.

The deck has been visually reviewed and the technical journey exercised.
A full human 90-minute timing rehearsal is still required. Cross-user Memory
isolation and automated Insights findings are not claimed. Use the completed
Optimizer run on stage: its measured duration was 18 minutes 23 seconds.

## Start the presentation

Open `presentation\Volt & Co - Governed and improving agents.pptx`
in PowerPoint Presenter View. Use `Presenter manuscript.pdf` for the complete
spoken script and `Source mapping and readiness.md` for preflight checks.
`Recorded evidence.html` is the clearly labeled offline fallback, not a live UI.
The four visible demo cards are slides **7, 12, 15 and 19**, returning to
**8, 13, 16 and 20**. The pre-activation route distinguishes historical cloud
results from local v2 tests. A fresh corrected escalation request in Demo 4
requires a separately approved and verified v2 deployment; never use v1 as its proof.

The default walkthrough uses real, completed issue/PR/evaluation evidence rather
than pretending to create the already-merged fix again. Copilot assistance was
local; cloud coding-agent dispatch was unavailable with the current credential.
The runtime is Microsoft Agent Framework, not the Copilot SDK.

For the live golden request, run from the repository root after setting up the
agent environment below:

```powershell
$env:PYTHONIOENCODING = "utf-8"
$python = ".\agent\src\.venv\Scripts\python.exe"
$source = ".\agent\src"
$out = ".\.runtime\live-" + (Get-Date -Format "yyyyMMdd-HHmmss")
& $python .\scripts\capture_cases.py `
  --project-endpoint "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-demo" `
  --expected-version 1 --dataset "$source\.foundry\datasets\volt-regression.jsonl" `
  --case replacement-recall --fresh --out $out --pause-seconds 0
```

`--fresh` refuses cached output and recorded-response reuse. Expect an `eligible`
decision, human assessment rather than an executed replacement, and genuine policy
citations. A one-case walkthrough is not the nine-case release gate.

There is no ticket creation or human-handoff integration. Some recorded prose
uses wording such as "I'm escalating"; that is an unsupported action claim,
not evidence that an escalation was executed. This is the real feedback incident.
The historical nine-case metric checks
the decision, required tool evidence and reference, not every natural-language
action claim. The matching DEMO response/trace, repository annotation and additive
regression are documented in `recordings/escalation-finding.json`.

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
.\scripts\Get-CitadelSource.ps1
az bicep build-params --file .\infra\hub.bicepparam --outfile .\.runtime\volt-hub.parameters.json

Push-Location .\tools
uv sync --locked --python 3.13
uv run python -m pytest -q
Pop-Location

Push-Location .\agent\src
uv sync --locked --python 3.13
uv run python -m pytest -q
uv run python -m pytest ..\..\evaluations -q
Pop-Location
```

Packaging is a separate operator action, not part of a check or rehearsal.
Do not rebuild the historical release ZIP or overwrite its receipts.
For a future approved tool release, `scripts/package_tools.py` includes only
the current API files and `tools/volt`; it does not deploy.

The function ZIP includes only authored API files and the canonical
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
it is not a hard production isolation boundary. Native Memory, IQ reasoning,
evaluation and optimization model traffic is not automatically covered by the
customer agent's APIM token budget. Review separate
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
$python = ".\agent\src\.venv\Scripts\python.exe"
$endpoint = "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev"
$root = ".\agent\src"

& $python .\scripts\probe_memory.py `
  --project-endpoint $endpoint --expected-version 5 `
  --out .\.runtime\memory-rehearsal

& $python .\scripts\capture_cases.py `
  --project-endpoint $endpoint --expected-version 6 `
  --dataset "$root\.foundry\datasets\volt-regression.jsonl" `
  --out "$root\.foundry\results\rehearsal-v6" --pause-seconds 60

& $python .\scripts\evaluate_captures.py `
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

## Governed promotion and observability

`scripts\Deploy-AccessContracts.ps1 -Environment DEMO` prepares the separate
DEMO products, subscriptions and connections. Connection names must be distinct
across projects in this shared account: `volt-demo-models-LLM`,
`volt-demo-business-tools`, and `volt-demo-policy-knowledge`. The toolbox retains
the same four public tool labels. Do not reprovision these resources on stage.

`scripts\promote_demo.py` defaults to a read-only preview. With explicit operator
approval and `--execute`, it requires the exact merged PR, successful GitHub
checks, the pinned native grader, all expected case results and the verified
package hash. It uploads the saved ZIP rather than rebuilding the source. Its
output deliberately remains `package-verified-smoke-pending` until
`scripts\verify_demo_release.py --receipt <promotion.json> --runtime-evaluation
<evaluation.json>` validates the separate native DEMO results and finalizes it as
`runtime-verified`. This is an operator-run gate, not a claim
that GitHub branch protection or environment approvals were configured.

The current azd extension's `--from-package` path did not preserve the required
`code-zip` artifact metadata. Promotion therefore uses the supported SDK code
upload for existing agents and the same new-agent multipart route used by azd.
The deployment receipt remains in `.runtime`; do not commit credentials or
environment state when preparing another release.

`scripts\trace_capture.py --capture <case.json> --out <trace.json>` queries only
the time window and operation linked to a captured response. The verified DEMO
golden response has 43 exported spans in `recordings\demo-trace.json`.
Its AgentServer root lasted 23.409 seconds in one observation, not an SLA.
The original defective response is preserved as native response/tool evidence;
its recorded request identifier was not found as an exported App Insights trace.
Do not substitute the fresh DEMO trace and label it as that earlier incident.

`scripts\prepare_optimizer.py` creates the current supported request schema
without submitting a job. Its four training and four validation prompts are
separate from the unchanged nine-case business regression suite. Review the
selected agent version and baseline instructions before another experiment.
The completed run targets the original DEV v1; the checked-in prompt now contains
the reviewed fix. Task-adherence scores are not interchangeable with business
contract scores. Do not click **Deploy best candidate** on the completed
no-improvement run: the retained result is the baseline, not a better candidate.

The native Memory forget operation removes the matching Memory item, not
historical conversations or telemetry. Known completed test sessions were stopped
or already inactive; APIM, Search and other base resources continue billing.
Any teardown needs explicit resource-owner approval and must not affect the
original fallback resource group.

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
