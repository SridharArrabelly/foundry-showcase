# Presenter operating guide

The PPTX contains the talk track in the Notes pane, with a timed handoff for each
demo. Use Presenter View. The visible slide remains the customer-friendly
summary; do not put command transcripts on every slide.

## Before the room opens

Open only these surfaces: PowerPoint Presenter View; VS Code on `volt/domain.py`
and the datasets; one terminal in the demo root; Foundry project with agent,
Traces and evaluation result tabs; GitHub Actions. Hide notifications.

```powershell
Set-Location C:\Users\sarrabelly\Documents\GitHub\foundry-showcase\demo
$py = ".\src\github-copilot-invocations\.venv\Scripts\python.exe"
azd ai agent show --output json | ConvertFrom-Json | Select-Object name, version, status, playground_url
# Use the actual version IDs in evidence/rehearsal-index.json, once created.
$versions = Get-Content evidence\rehearsal-index.json | ConvertFrom-Json
$baseline = $versions.baseline_version
$improved = $versions.improved_version
```

Never substitute a guessed version. If no rehearsal index exists, finish
rehearsal before presenting. First invocation may download/start the Copilot
runtime and warm Foundry compute; warm the exact versions in advance.

## Demo 1 | slides 5-6 | 09:00-16:00

Say: "The infrastructure is prepared. Watch the customer request, not setup."

```powershell
python scripts\demo.py ask "Find the cheapest charger for my Volt Book 14 under EUR 50." `
  --version $improved --out evidence\shopping.json
python scripts\demo.py ask "Is my Volt Charge 65 from batch CH-0722 safe to use?" `
  --version $improved --out evidence\recall.json
```

Expected: VC-C65 at EUR 39.90, after the 30W charger is rejected for a 65W
requirement. Recall status is `recalled` for the synthetic CH-0722 record.
Open the captured JSON and show tool inputs/results. Foundry: project > agent >
Traces > completed request. If ingestion is delayed, open the rehearsed trace.

Return to slide 7: "We can explain this one execution. Now let's measure a set."

## Demo 2 | slides 7-9 | 18:00-25:00

Show `datasets/core.jsonl`, then the new missing-batch case in regression.jsonl.
The baseline bug is deliberate; do not stage it as an unexpected production incident.
The correction is in `recall_notices`: missing input must return `needs_batch`.

```powershell
python scripts\check_contract.py --variant baseline  # expected exit 1 / BLOCK
python scripts\check_contract.py --variant improved  # expected exit 0 / PASS
python scripts\demo.py ask "I have a Volt Charge 65. Is it safe?" `
  --version $baseline --out evidence\missing-batch-baseline.json
python scripts\demo.py ask "I have a Volt Charge 65. Is it safe?" `
  --version $improved --out evidence\missing-batch-improved.json
```

Show actual completed `baseline.json` and `candidate.json`. Do not wait for a full
suite live. For a fresh run, use `demo.py evaluate --version ... --dataset ...`.
Open `evidence/foundry-evaluation.json`'s report URL for the native coherence run.
Clarify that coherence is not recall correctness or a safety guarantee.

Return to slide 10: "An improved candidate still needs a release decision."

## Demo 3 | slides 10-11 | 27:00-34:00

GitHub > Actions > Volt quality gate: open a completed `baseline` failure and
`improved` pass. The failure should point to the missing-batch contract.
If available, open the live candidate/release workflow separately. Do not
describe the offline quality job as having invoked a model.

```powershell
Get-Content evidence\release.json
python scripts\demo.py ask "Check Volt Charge 65 batch CH-0926 for a recall." `
  --out evidence\released-request.json
```

Do not display an unfiltered `azd ai agent show` response: it includes configured
environment values, including the telemetry connection string.

The client uses the approved version from `release.json`. This pointer is not a
change to Foundry's default portal routing. Show version, dataset hash and
report hash. Say deployment and full scoring happened during rehearsal.

Return to slide 12: "The release only proves the expectations we wrote down."

## Demo 4 | slides 12-13 | 35:00-47:00

Foundry > agent > Monitor (preview), then Traces. Use a completed captured
missing-batch request with its trace ID. If the Foundry filter is empty, use the
connected Application Insights resource and filter custom spans by `volt.variant`
and the captured operation/trace ID. Do not claim a missing UI integration works.

Review the expected behaviour with the audience before running:

```powershell
python scripts\demo.py feedback --trace evidence\missing-batch-baseline.json `
  --id reviewed-missing-batch --query "I have a Volt Charge 65. Is it safe?" `
  --expected-decision needs_batch `
  --expected-behavior "Ask for the batch code before a recall conclusion; never infer safety from missing evidence." `
  --reviewer "Presenter reviewed with audience" --approve `
  --out evidence\reviewed-case.jsonl
python scripts\demo.py evaluate --version $improved `
  --dataset evidence\reviewed-case.jsonl --out evidence\reviewed-result.json
```

The feedback command refuses to overwrite an existing review. Use a unique
filename on the next rehearsal. Do not include an unreviewed output as truth.
Portal `Traces > select > Add to dataset` is an optional preview path. The
code-first reviewed row is the verified fallback and does not claim that button
was used.

Return to slide 14: "The next release has a stronger contract."

## Shortened path

If 5 minutes late: keep one live shopping request, open completed evaluations,
show completed release evidence, and preserve the missing-batch feedback loop.
Skip fresh native judge runs, preview screens and a cold deployment. Finish at
minute 50 and leave Q&A intact.

## Technical and business Q&A

| Question | Answer |
|---|---|
| Is this the managed Copilot harness prompt-agent option? | No. This is code using the Copilot SDK, packaged as a Foundry hosted agent. |
| Are you running GitHub-hosted inference? | No. BYOK here means our Foundry model with Entra; no GitHub runtime token is embedded. |
| Why not just a prompt agent? | Use one when managed authoring/tool support fits. This story deliberately shows code-owned logic and its release lifecycle. |
| Can the customer-facing runtime run shell commands? | This sample exposes only the three reviewed tools. It is not a general coding assistant. |
| Is missing-batch refusal a platform guardrail? | No. It is a domain tool contract and agent behaviour, not evidence of a content-filter intervention. |
| Do passing scores prove safety? | No. Coverage, calibrated evaluators, least privilege and human review remain necessary. |
| Does Sweden Central guarantee Sweden-only processing? | No. The selected model is GlobalStandard; validate each service, deployment type and data path. |
| What does it cost? | Model calls, hosted compute, telemetry, evaluations and CI all contribute. Measure representative usage and current rates; don't quote savings from one prompt. |
| What is the ROI? | Establish customer handling-time, resolution-quality and escalation baselines, then measure the pilot against them. |
| What should a production rollout add? | Separate environments and deployment identities, reviewed policy thresholds, mandatory release checks, approvals, retention/privacy controls and incident ownership. |
