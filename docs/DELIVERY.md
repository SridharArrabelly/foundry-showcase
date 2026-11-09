# Delivery map

## Open first

1. `presentation/Foundry - From prototype to operated service.pptx`
2. `presentation/Presenter script.html`
3. `presentation/Recorded demo evidence.html`

The deck has **15 visible slides plus 5 hidden Q&A backups**. The Notes pane
contains talk track, timing, transitions to and from demos, fallback and source
boundaries. The PDF intentionally exports only the 15 visible slides.

The speaker notes now contain a complete delivery script, not topic reminders:
read-aloud wording, separate screen actions, exact commands, loading commentary,
success/failure branches and the sentence to transition to the next slide.
The same manuscript is available as `Presenter script.md`, a navigable HTML
reader, and a print-ready `Presenter script.pdf`.

The visual revision restores the original Bank Briefing Azure cover art and
workshop diagrams (inner/outer loops, release bridge, platform and improvement
loop), with high-contrast text and explicit font formatting for the app canvas.
The source-derived diagrams are images; new text and diagrams remain editable.

## Actual rehearsal, 8 November 2026

| Artifact | Recorded result |
|---|---|
| Hosted baseline | `volt-assistant:2`, 7/9 cases pass; both missing-batch cases fail |
| Hosted improved candidate | `volt-assistant:4`, 9/9 cases pass |
| GitHub OIDC release | Successful deploy, live evaluation and release artifact |
| Native Foundry scoring | Completed coherence evaluation on captured outputs |
| Telemetry | Invocation and child tool spans observed in Application Insights |
| Feedback loop | Baseline invocation converted to an explicitly approved demo test; corrected agent passes |

These are small synthetic-case results, not accuracy benchmarks, statistical
claims, safety certification or customer ROI measurements. Demo approval flags
do not replace presenter/domain-expert sign-off.

## Live links

- [Private repository](https://github.com/SridharArrabelly/foundry-showcase)
- [Foundry agent version 4](https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-github-copilot-invocations-dev-38f60a75,,cog-pa36s3dwoftlo,foundry-showcase/build/agents/volt-assistant/build?version=4)
- [Successful live release workflow](https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42460045951)
- [Intentionally blocked contract run](https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42459859840)
- [Passing quality run](https://github.com/SridharArrabelly/foundry-showcase/actions/runs/42459993922)
- [Native candidate coherence scorecard](https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-github-copilot-invocations-dev-38f60a75,,cog-pa36s3dwoftlo,foundry-showcase/build/evaluations/eval_eeaa3f5f3d204576b729e2c151e096d2/run/evalrun_07901120534340d0a5106b48c48e9dd6)

The older failed deployment and first failed OIDC attempt remain as truthful
history; they are not the deliberate business-contract failure to show on stage.

## Resources left provisioned

Foundry project `foundry-showcase` in Sweden Central, its model deployment and
hosted agent versions; Application Insights and Log Analytics; and a
main-branch-scoped GitHub OIDC identity. The runtime uses a Foundry-hosted model,
not GitHub-hosted inference. Charges can continue while resources are retained.

No separate customer production environment was created. DEV is local and the
serving target is a demo project. The release pointer controls this demo's
client version, not the Foundry portal's default routing. Managed Toolbox,
APIM, memory, IQs, optimizer and multi-agent orchestration are outside this build.

The complete ZIP includes synthetic recorded evidence but excludes `.azure`,
`.env`, `.venv`, `.runtime` and Git internals. The repository excludes raw
rehearsal evidence; use the ZIP or download the linked Actions artifact.
