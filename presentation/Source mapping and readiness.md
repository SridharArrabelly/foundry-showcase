# Volt & Co — delivery map and readiness

The current deck has **23 slides: 21 visible, including four demo checkpoints,
and two hidden Q&A backups**. It is designed for approximately 50 technical
attendees, with 80 minutes of content and 10 minutes of questions.

## The screen-switch map

| Clock | Slides / screen | Action |
|---|---|---|
| 00–13 | 1–6 | Customer, inner/outer loop, runtime choice and Citadel |
| 13–15 | 7–8 | Explain the tools and policy needed for the request |
| 15–27 | **9 → terminal / Foundry / focused code → 10** | **Demo 1:** fresh customer request, Toolbox and IQ |
| 27–30 | 10–12 | Debrief utility; distinguish access, guardrails and memory |
| 30–45 | **13 → APIM / Foundry / verified proofs → 14** | **Demo 2:** govern capabilities |
| 45–47 | 14–15 | Debrief boundaries; define quality and optimization decisions |
| 47–57 | **16 → native evaluation / Optimizer reports → 17** | **Demo 3:** inspect completed runs |
| 57–60 | 17–19 | Debrief measured outcomes; explain the repair/release chain |
| 60–78 | **20 → evidence / GitHub / editor / terminal → 21** | **Demo 4:** actual repair history, exact release and a new request |
| 78–80 | 21 | Four takeaways |
| 80–90 | 21; optional 22–23 | Q&A |

Show the demo card before switching. Say its opening bridge, Alt+Tab to the
prepared application group, and remain there for the full demonstration.
Return to the card and advance once to the numbered return slide. That slide's
notes begin with the debrief. Cards do not automatically run commands or launch
applications.

The time budget includes 25 minutes on concept/return slides, 49 minutes of
demonstration/evidence inspection and six minutes of screen transitions.
Narration overlaps the demonstrations: do not count it a second time.
`spoken-word-estimate.json` is a speech estimate, not a human rehearsal.

## Files and ownership

| File | Purpose |
|---|---|
| `Volt & Co - Governed and improving agents.pptx` | Editable audience deck with the full script embedded in notes |
| `Volt & Co - Audience.pdf` | Visible slides only |
| `Presenter manuscript.md` / `.html` / `.pdf` | One synchronized, fully written presenter script |
| `Recorded evidence.html` | Self-contained offline fallback, visibly labeled recorded |
| `Rehearsal bindings.json` | Actual project/version/run links and four entry/return pairs |
| `build_citadel_deck.py` and rendering helpers | Rebuild tools, not runtime agent code |
| `..\docs\OPERATIONS.md` | Authoritative setup and operational commands |
| `..\.runtime\presentation-renders` | Generated slide/review images; not another source deck |

Do not use the archived 50-minute slides or their old commands as the current
workshop entry point. The user's edited older deck is preserved in
`archive/50-minute-workshop/presentation`, not overwritten.

## Source mapping

Primary source: the user-supplied
`C:\Users\sarrabelly\Downloads\Foundry Agent Platform Workshop v1.0.0.pptx`
(**198 slides, 35 hidden**). The older 202-slide deck has different numbering.
Its visual language, original wave artwork, masters, lifecycle and architecture
diagrams are retained. The source deck itself is not edited.

| Current | Title / purpose | Source slide |
|---:|---|---|
| 1 | From useful agent to governed service | 1 |
| 2 | Two loops. One improving service. | 15; original diagram |
| 3 | One customer. One support journey. | 9 |
| 4 | Choose the operating model | 33; originally hidden |
| 5 | Our code. Foundry's runtime. | 31 |
| 6 | Where Citadel and Foundry meet | 6; original layered diagram |
| 7 | Give the agent governed capabilities | 47 |
| 8 | Ground the answer in policy | 141 |
| 9 | Demo 1 — Make the answer useful | New screen-switch checkpoint |
| 10 | One gateway. Explicit access contracts. | 57; return from Demo 1 |
| 11 | Enforce the right boundary | 128 |
| 12 | Remember preferences, not authority | 115; second-identity test explicitly unverified |
| 13 | Demo 2 — Govern the capabilities | New screen-switch checkpoint |
| 14 | Evidence before confidence | 83; return from Demo 2 |
| 15 | Optimize configuration. Review the change. | 98, informed by 101 |
| 16 | Demo 3 — Measure before improving | New screen-switch checkpoint |
| 17 | Operation teaches DEV what to test | 185; return from Demo 3 |
| 18 | A PR carries code and behavioral evidence | 159; original outer-loop diagram |
| 19 | Follow one fix from trace to customer | Authored evidence chain |
| 20 | Demo 4 — Close the loop | New screen-switch checkpoint |
| 21 | Useful. Governed. Measurable. Improving. | 198; return from Demo 4 |
| 22 | Memory authorization | 113; hidden backup |
| 23 | Account/project responsibilities | 163; hidden backup |

Unrelated finance scenarios, screenshots, the broad feature agenda, source slide
27's restricted material and unsupported blanket security claims are excluded.
No native portal screenshot or successful result was fabricated.

## Rehearsal checklist

- Open the current deck in Presenter View; test readability from the back of the room.
  Use large terminal/editor text and browser zoom. Close unrelated tabs and notifications.
- Pre-open the **DEMO** agent and Toolbox v1 for Demo 1. DEV's Toolbox is v2;
  do not interchange their configuration evidence.
- Verify Azure/GitHub access and the exact native report links in the bindings.
  Do not project connection headers, keys or private Memory records.
- Prepare both fresh-request commands from the script. Each uses a new output
  directory, `--fresh`, DEMO v1 and one replacement-recall case.
- At 30 seconds without a result, announce the recorded fallback and move on.
  Never replace a pending request with recorded output without saying so.
- Keep the original incident capture distinct from current DEMO behavior.
  Its exported App Insights span is unverified; the separate golden DEMO trace has 43 spans.
- Inspect already-completed native evaluations and Optimizer. Do not start a job,
  merge the existing PR again, change capacity or redeploy on stage.
- Memory's main route uses redacted prior proof. A live four-conversation branch
  requires its own timing/redaction rehearsal. A second authenticated user is still
  needed before making cross-user isolation claims.
- The restricted-consumer APIM denial drill has no verified capture. Explain that
  boundary conceptually unless real evidence is obtained separately.
- If an answer says “I'm escalating,” state that no ticket/handoff was executed.
- Rehearse all four entry/return pairs and reserve Q&A from 80:00. If behind,
  skip deeper policy/latency inspection, not the distinction between live and recorded.

## What remains true

Native business evidence is DEV **8/9 → 9/9** and an independent fresh DEMO
**9/9**. It grades captured real responses, not server-side agent reruns or
availability. The saved code ZIP and native deployed hash match.
Optimizer retained a 0.75 task-adherence baseline with no accepted candidate;
that metric is not the business-contract score.

The actual fix used local Copilot assistance. The gate is operator-run, not
GitHub-enforced branch protection. No automatic Insights monitor, rollback
drill, universal safety, production SLA, cost saving or customer-order ownership
authorization is claimed.

This is a shared-account, synthetic profile. DataZoneStandard is not Sweden-only
processing; APIM Developer has no production SLA; selected gateway quotas do not
cover every service-internal call. Base resources remain billable. A full human
90-minute rehearsal is still outstanding.

## Rebuild locally

These are local document operations, not Azure operations. The presentation
builders use the existing Python presentation environment, PowerPoint and Word.

```powershell
python .\presentation\build_citadel_deck.py
& .\presentation\render_native.ps1
python .\presentation\make_contact_sheets.py
python .\presentation\render_manuscript.py
python .\presentation\validate_artifacts.py
python .\presentation\estimate_spoken_words.py
python .\presentation\build_recorded_evidence.py
python .\presentation\test_recorded_evidence.py
```
