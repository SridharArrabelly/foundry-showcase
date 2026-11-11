# Foundry showcase: Volt & Co

## Current: 90-minute Citadel internal enablement

Start with [the integrated showcase guide](showcase/README.md) and
[the complete presenter manuscript](presentation/citadel/Presenter%20manuscript.md).
The new deck, handout and offline evidence viewer are in `presentation/citadel`.
This path uses Agent Framework / Responses, with GitHub Copilot for development.
It preserves the original implementation below; do not run the root `azure.yaml`
when preparing the Citadel showcase.

## Original 50-minute fallback

A 50-minute customer presentation and one coherent demo: build with GitHub
Copilot, run a constrained Copilot SDK agent in Microsoft Foundry, evaluate
behaviour, gate a release and turn reviewed operational evidence into a test.

**Synthetic demo, not a production reference deployment.** Read the explicit
boundaries below before presenting.

**Start here: [delivery map, deployed versions and live links](docs/DELIVERY.md).**

## Deliverables

- `presentation/Foundry - From prototype to operated service.pptx`: 15 main
  slides and 5 hidden Q&A slides. Every slide has talk track, timing,
  transitions, demo cues, fallback and source notes in PowerPoint Presenter View.
- `presentation/Foundry - From prototype to operated service.pdf`: audience handout.
- `presentation/Presenter notes.md`: searchable copy of all embedded notes.
- `presentation/Presenter script.md` / `.html` / `.pdf`: full read-aloud delivery,
  separated stage directions, exact transitions, demo commands and contingency wording.
- `docs/PRESENTER.md`: exact commands and screen sequence.
- `docs/REHEARSAL.md`: access, readiness, costs and contingency checks.
- `scripts/demo.py`: live requests, deterministic evaluation and reviewed feedback.
- `scripts/foundry_eval.py`: native Foundry model-judged coherence on captured outputs.
- `.github/workflows/`: credential-free contract checks and manually triggered,
  OIDC-authenticated candidate deployment / live evaluation.

## Project structure

```text
azure.yaml                         Foundry model and hosted-agent definition
src/github-copilot-invocations/
  main.py                          Copilot SDK + Foundry Invocations adapter
  instructions.md                  Shared agent response contract
  volt/domain.py                   Three read-only tools, explicit baseline defect
  volt/data.json                   Six fictional products and recall fixtures
  volt/evaluation.py               Deterministic business assertions
  pyproject.toml / uv.lock          Dependencies and exact resolution
datasets/core.jsonl                 Seven reviewed known cases
datasets/regression.jsonl           Two reviewed missing-information cases
infra/                             Telemetry + scoped GitHub OIDC identity
scripts/                           Presenter commands and release gate
tests/                             Fast unit and business-contract checks
presentation/                      Editable deck, notes, PDF and generator
evidence/                          Captured results; gitignored, never fabricated
```

The source directory name is retained from the official Microsoft sample so its
provenance is easy to follow. The deployed agent is named `volt-assistant`.
Remote code packaging uses the exported, pinned `requirements.txt`. The
development `pyproject.toml` is excluded from that package to avoid the remote
builder interpreting it as a Poetry project. After changing dependencies, run
`uv export --no-dev --no-hashes --no-emit-project --format requirements-txt --output-file requirements.txt`
from the agent source directory and commit both lockfiles.

## Prerequisites

PowerShell 7, Python 3.13, `uv`, Azure CLI, Azure Developer CLI with the
`microsoft.foundry` extension, and access to a Foundry project/model deployment.
The presenter needs Foundry data-plane access in addition to subscription
management-plane permissions. Viewing traces also requires telemetry read access.

For manual authentication, run `az login` and `azd auth login` yourself in the
intended tenant. Do not copy tokens into source or slides.
For a fresh clone on an authorized machine, run `scripts/configure_existing.ps1`
to reuse the resource IDs in `config/demo-target.json`. It creates only local
azd configuration and does not provision new cloud resources.

```powershell
Set-Location C:\Users\sarrabelly\Documents\GitHub\foundry-showcase\demo
Set-Location src\github-copilot-invocations
uv sync --group dev --python 3.13
.\.venv\Scripts\python.exe -m copilot download-runtime
Set-Location ..\..
python -m unittest discover -s tests -v
```

## Configuration

Local deployment context lives in gitignored `.azure`. The committed manifest
contains variable references, not credentials.

| Variable | Purpose |
|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry project endpoint returned by provisioning |
| `AZURE_AI_PROJECT_ID` | Actual ARM project ID returned by Azure |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Deployment name, not an arbitrary model label |
| `VOLT_VARIANT` | `baseline` (intentional demo defect) or `improved` |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Telemetry connection, kept in azd environment / GitHub secret |
| `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_LOCATION` | Deployment context |

The approved deployment uses Sweden Central and the sample's `gpt-5.4-mini`
GlobalStandard deployment. **GlobalStandard is not a Sweden-only processing
commitment.** Check the deployment type, data path and current terms for any
customer residency requirement.

No `GITHUB_TOKEN` is required by the runtime. Inference uses the Foundry model
through Entra. The SDK refreshes the provider token through a callback. Only
three allowlisted domain tools are enabled; coding, shell and filesystem tools
are not exposed to the customer-facing agent.

## Local and hosted execution

```powershell
azd ai agent run volt-assistant --no-client --port 8098
# In a second terminal:
python scripts\demo.py ask "Find the cheapest charger for my Volt Book 14 under EUR 50." `
  --local-url http://127.0.0.1:8098 --out evidence\local-shopping.json
```

Local execution still calls an Azure model and incurs inference charges. It is
not offline. The offline checks are only `unittest` and `check_contract.py`.

Deployment must target an environment you selected. Do not run provision against
an arbitrary default subscription:

```powershell
azd deploy volt-assistant --no-prompt
azd ai agent show --output json | ConvertFrom-Json | Select-Object name, version, status, playground_url
python scripts\demo.py ask "Is my Volt Charge 65 from batch CH-0722 safe to use?" `
  --version <actual-version> --out evidence\recall.json
```

## Evaluation and release

```powershell
python scripts\demo.py evaluate --version <actual-improved-version> `
  --dataset datasets\core.jsonl --dataset datasets\regression.jsonl `
  --out evidence\candidate.json
python scripts\release.py --version <same-version> --report evidence\candidate.json
```

The gate requires all nine reviewed deterministic cases to pass. It checks
dataset hashes and candidate identity. It writes the demo client's release
pointer; it does **not** change the Foundry portal's default endpoint routing.
`demo.py ask` without `--version` uses that approved pointer, never an implicit
latest version. Explicit candidate requests use `--version`.

Native Foundry scoring:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = azd env get-value FOUNDRY_PROJECT_ENDPOINT
$env:AZURE_AI_MODEL_DEPLOYMENT_NAME = azd env get-value AZURE_AI_MODEL_DEPLOYMENT_NAME
.\src\github-copilot-invocations\.venv\Scripts\python.exe scripts\foundry_eval.py `
  --report evidence\candidate.json
```

This evaluates **captured live responses** for coherence using a built-in model
judge. It does not replay the agent or prove domain correctness. The deterministic
and semantic reports are intentionally separate.

## Explicit boundaries

- DEV is local; the hosted target is a **demo** project, not customer production.
  Production requires separate deployment environments/identities and policy.
- The tool implementation is packaged with the agent. **Managed Foundry Toolbox,
  APIM, memory, IQs, optimizer and multi-agent orchestration are not implemented.**
- `baseline` deliberately maps a missing batch to `no_recall`. Only use it to
  demonstrate the regression. Keep the approved serving pointer on `improved`.
- The package uses small synthetic test sets, not statistically representative
  accuracy measurements or safety certification.
- Monitor, Insights and trace-to-dataset experiences may be preview. Consult
  the status appendix and current official docs before presenting.
- GitHub PR checks prove the offline business contract. The separate live release
  workflow invokes the actual agent. Neither is silently substituted for the other.
- No benchmark, cost saving, ROI, security guarantee or data-residency guarantee
  is claimed. Token usage is evidence, not a complete cost estimate.

## Provenance

Based on Microsoft's [Copilot SDK Invocations sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot).
The presentation adapts the user's workshop lifecycle and Volt & Co story.
No NDA roadmap slides or other agents' results are included.

Official references:
[Hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents),
[GA matrix](https://learn.microsoft.com/azure/foundry/concepts/general-availability),
[Tracing](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup),
[Dataset evaluation](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets),
[CI/CD](https://learn.microsoft.com/azure/foundry/agents/quickstarts/set-up-cicd-hosted-agent),
[Copilot SDK BYOK](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md).

## Cleanup

To regenerate the presentation, install `presentation/requirements.txt`, run
`python presentation/build_deck.py`, then run `scripts/render_slides.ps1` on
Windows with PowerPoint installed. The PDF intentionally contains the 15 visible
slides; the five Q&A backups remain hidden in the editable deck.

The revised design uses the original Azure artwork from the Bank Briefing and
high-resolution workshop lifecycle/platform diagrams. Their provenance is in
`presentation/assets/PROVENANCE.md`. Source diagrams are images; surrounding
text, new process diagrams and the result comparison remain editable. Speaker
notes are authored in `presentation/Presenter script.md`. Run
`python presentation/update_speaker_notes.py` to embed them, update
`slide_notes.json` for future deck rebuilds, and regenerate the readable script.
This notes-only update verifies that every non-notes PowerPoint part is unchanged.
The printable script PDF is a print export of the HTML; it is separate from
the unchanged audience slide handout.

All text runs have explicit size and colour so the app canvas does not lose
inherited paragraph formatting. `build_deck.py` checks this before saving.
The supplied assets make rebuilding independent of the original decks;
`extract_reference_assets.py` is only needed to refresh them from those files.

Stop local processes you started. Delete resources only after reviewing the exact
resource group and confirming it contains only this demo. Telemetry and the
workflow identity are deployed by separate Bicep templates; `azd down` is not a
promise to remove those extensions. Do not delete the subscription or broad
workspace directories. Remove the GitHub OIDC trust when retiring the demo.
