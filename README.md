# Volt & Co | Microsoft Foundry workshop

One customer journey, from a useful hosted agent to a governed, measurable service.
Designed for a **90-minute internal technical session: 80 minutes plus 10 minutes Q&A**.

## Start here

- **Present:** [editable deck](presentation/Volt%20%26%20Co%20-%20Governed%20and%20improving%20agents.pptx) and [full presenter manuscript](presentation/Presenter%20manuscript.md).
- **Run:** [setup, live commands and operational boundaries](docs/OPERATIONS.md).
- **Rehearse:** [source mapping and readiness](presentation/Source%20mapping%20and%20readiness.md).
- **Recover:** [offline recorded evidence](presentation/Recorded%20evidence.html). Always label it as recorded, never live.

## One project, four demonstrations

| Demonstration | Question | Main surfaces |
|---|---|---|
| 1. Make the answer useful | Can the agent justify a replacement assessment? | Hosted request, Toolbox, Foundry IQ |
| 2. Govern the capabilities | Which boundaries act, and what may persist? | Citadel/APIM, guardrails, narrow DEV Memory |
| 3. Measure before improving | Did the change actually improve behavior? | Native evaluations and the completed Optimizer experiment |
| 4. Close the loop | Can evidence become a reviewed fix and verified release? | Trace, GitHub issue/PR, code, release evidence, fresh DEMO request |

Use the deck's demo entry/return cues. New requests are live; completed evaluations,
the Optimizer job and the already-merged PR are inspected as historical evidence.

## Repository map

```text
agent/                 Hosted-agent project and azd definition
  src/                 Agent Framework runtime, instructions and runtime tests
tools/                 Read-only Functions API and its synthetic Volt domain
evaluations/           Native business grader and release-gate tests
knowledge/             Synthetic policy documents for IQ
infra/                 Citadel, gateway, identity and guardrail definitions
scripts/               Setup, probes, capture, evaluation and release commands
recordings/            Redacted records of actual completed runs
presentation/          Current slides, full script, audience PDF and offline viewer
docs/                  Current operational guide
archive/               Earlier 50-minute workshop; not the current entry point
.runtime/              Ignored local receipts, packages, renders and vendor checkout
```

`foundry-showcase` is the Git root. There is no separate `demo` project wrapper or
top-level `deliverables` source tree. Generated ZIPs belong under `.runtime/delivery`;
they are distributions, not a second editable copy of the project.

## Local checks

From this directory, using the existing environments:

```powershell
& .\tools\.venv\Scripts\python.exe -m pytest .\tools\tests -q
& .\agent\src\.venv\Scripts\python.exe -m pytest .\agent\src\tests .\evaluations -q
```

On a fresh clone, use `uv sync --locked --python 3.13` in `tools` and `agent/src`
first. Do not copy virtual environments between machines. See the operational
guide for Azure prerequisites; these local checks require no cloud credentials.

## What the evidence establishes

The original hosted business baseline was **8/9**, the reviewed DEV candidate
**9/9**, and fresh DEMO responses passed their own **9/9** native evaluation.
The tested agent ZIP was promoted unchanged. The source reorganization does not
redeploy or change that verified package.

The Optimizer retained its baseline; no improved candidate was accepted or applied.
Memory was verified for one authenticated DEV caller and remains off in DEMO.
The tools do not create tickets, issue refunds or ship replacements. Nine synthetic
business checks are not a production-readiness or availability guarantee.

Everything customer-facing is synthetic. Important previews are explicitly labeled.
The shared-account profile is not hard production isolation; APIM Developer has no
production SLA. Base Azure resources continue billing. A full timed presenter
rehearsal is still required.
