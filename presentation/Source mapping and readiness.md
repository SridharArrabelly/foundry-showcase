# Current presentation: source mapping and readiness

## One current deck

Open **Can we defend this release - Foundry SE Showcase.pptx**.
It has **26 slides: 24 visible and hidden backups 25–26**. This is the adopted
user-supplied deck, not the retired 24-slide presentation. The older deck is
available in Git history; its filename is no longer an active entry point.

The user supplied a General/public copy on 13 November 2026. Before preparation,
the file was a readable Open XML package and native PowerPoint reported rights
management disabled. The original approved copy has SHA-256
`52f893b09ec0039c27f46fc51d9ab7ec608dbca4cabfaa0823f610a4692ff07b`.
The protected earlier copies remain in ignored local storage; their labels were
not removed by the agent.

The design and order are retained. The preparation script corrects claims that
would imply unperformed cloud work, adds explicit demo-return cues, hides the
two backups, and synchronizes delivery clocks and the presenter guide.
It does not rebuild or overwrite any historical agent release artifact.

## Delivery order

| Clock | Chapter | Current slides |
|---|---|---|
| 00–05 | Why and agenda | 1–3 |
| 05–10 | Two loops, two bridges | 4 |
| 10–25 | Inner loop: Build | 5–7 → **8 / Demo 1 → 9** |
| 25–40 | Inner loop: Prove | 9–12 → **13 / Demo 2 → 14** |
| 40–50 | Bridge 1: candidate, evidence, approval | 14–15 → **16 / Demo 3 → 17** |
| 50–60 | Operate, finding and feedback | 17–19 |
| 60–70 | Bridge 2: finding, test and repair | **20 / Demo 4 → 21** |
| 70–80 | Architecture, takeaways, customer POC | 21–23 |
| 80–90 | Q&A | 24; backups 25–26 only if useful |

Demo 1 starts at 17:00, Demo 2 at 32:00, Demo 3 at 42:00 and Demo 4 at 60:00.
Their slots include transitions. Return to the demo card and advance once to
the named debrief slide. `docs/DEMO-RUNBOOK.md` has the detailed command sequence;
`Presenter manuscript.md`/PDF contain matching speaker notes and operating cues.
They are not a claim of a completed human rehearsal or a verbatim 80-minute speech.

## Original workshop references

The earlier 198-slide Foundry workshop supplied the lifecycle vocabulary and
the review's references: 84 (evaluators), 171 (case file), 174 (PR gate),
181 (continuous evaluation), 189 (trace-to-dataset), 192 (architecture),
195 (POC) and 198 (takeaways). Those are source-reference numbers, not the
current 26-slide deck's numbers.

That user-supplied local workshop had 35 hidden slides and 105 nonempty note
sections, SHA-256 `e3e4c79391b114f14968bb990812b757a3c200a13079f7e03ef4109bcbb2ec47`.
The linked online version was not independently inspected. Restricted AKS/A-B
material and private release dates are not part of this presentation.

## Evidence readiness

| Capability | What can be shown now | Still pending |
|---|---|---|
| Historical release | DEV 8/9 → 9/9; separate DEMO 9/9; identical original ZIP | Never relabel the instructions-only repair as code enforcement |
| Runtime contract | Local Agent/Responses-host proof, including Memory context | Revised cloud deployment and serving-version verification |
| V2 evaluation | Eleven cases, original nine expectations retained, two escalation cases | Native v2 execution and action-rubric calibration |
| Escaped action claim | Recorded DEMO answer, matching 43-span trace and reviewed annotation | Not a native Insights finding |
| Release workflow | Code, local rejection checks and historical v1 case file | Actual protections/OIDC, live gate results and v2 promotion |
| Red teaming | Version-pinned adapter and local tests | SDK installation is blocked; no scan/scorecard exists |
| Scheduled checks | Explicitly disabled workflow for pinned synthetic v1 cases | Activation, recurring-cost approval and real results |
| Insights | Capability explanation only | No monitor configured |
| Memory | Historical one-caller DEV proof, backup only | Cross-user isolation and revised Memory-enabled response UX |

The source deck's aspirational live route is not an execution receipt. Use the
local/recorded routes embedded in the current notes until approved cloud runs
produce new evidence. Red teaming is separate from the PR business/rubric gate.
Calibration resides inside `action-judgments.json`; promotion and DEMO results
belong to the release artifact, not every PR artifact.

## Preparation and rehearsal

From the repository root:

```powershell
python .\presentation\build_citadel_deck.py
& .\presentation\render_native.ps1
python .\presentation\make_contact_sheets.py
python .\presentation\render_manuscript.py
python .\presentation\validate_artifacts.py
python .\presentation\estimate_spoken_words.py
```

The builder prepares the current 26-slide file in place by default. To import a
new approved copy, provide `--source <path>`; it will not silently restore the
old 24-slide deck. The audience PDF excludes the two hidden backups.
Rendered review images stay under ignored `.runtime/presentation-renders`.

Rehearse with the actual projector, large terminal/editor text and the four
entry/return pairs. Keep a 30-second fallback cutoff for fresh requests.
Identify a fallback as a different recorded execution when appropriate.
Do not use a presentation as authorization to deploy, approve a gate or change
permissions. Preserve the final ten minutes for Q&A.
