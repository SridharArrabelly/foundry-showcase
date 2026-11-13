# Evidence-first workshop: source map and readiness

## What this revision delivers

**24 slides: 22 visible, two hidden backups.** One 90-minute story, four substantial
demonstrations, explicit return cues and full spoken notes. Memory moves to backup.

The current pre-activation version is honest about local v2 code versus historical
cloud proof. It must not be presented as a completed v2 live release until the
separately approved cloud workflow, model calibration and promotion have succeeded.

| Clock | Chapter | Screen-switch instruction |
|---|---|---|
| 00–10 | Why, agenda and lifecycle | Slides 1–3 |
| 10–25 | Build and inspect | Slides 4–6 → **7 / Demo 1 → 8** |
| 25–40 | Prove | Slides 8–11 → **12 / Demo 2 → 13** |
| 40–50 | Bridge 1 | Slides 13–14 → **15 / Demo 3 → 16** |
| 50–60 | Operate and the escaped finding | Slides 16–18 |
| 60–70 | Bridge 2 | **19 / Demo 4 → 20** |
| 70–80 | Architecture and POC | Slides 20–22 |
| 80–90 | Q&A | Slide 22; backups 23–24 only if useful |

Show the entry card, say its bridge, then leave the slides. Return once at the
named target and speak the debrief. The cards do not execute commands.

## Verified reviewer reference

The reviewer refers to the [linked online workshop](https://onedrive.cloud.microsoft/:p:/a@3wd7z4b6/S/cQqcmS2qKIDnQbWAX3_QQjI_EgUC2eDOq6LllEwyqTs4S8z6zA?isSPOFile=1).
The user supplied a fresh local copy after browser access stalled. Its content
is readable and the review's principal slide references match this copy.
The online file itself has not been independently inspected.

The current local source is
`C:\Users\sarrabelly\OneDrive - Microsoft\00FY27\AI Roadshow FY27\Foundry Agent Platform Workshop v1.0.0.pptx`
(198 slides, 35 hidden, 105 with nonempty speaker notes).
SHA-256: `e3e4c79391b114f14968bb990812b757a3c200a13079f7e03ef4109bcbb2ec47`.
It differs from the earlier Downloads copy; the reused slide XML for 1, 6, 15
and 159 is unchanged. The builder now reads this current source and keeps its
original cover theme, two-loop diagram
(local slide 15) and Citadel diagram (local slide 6). Other slides use the same
editable visual language. Neither the local source nor the shared online file is modified.

The source references below describe selected concepts, not wholesale slide
imports. References checked include 84 (evaluator types), 171 (case file),
174 (PR gate), 181 (continuous evaluation), 189 (trace-to-dataset), 192
(architecture) and 195/198 (POC and takeaways). Source slide 13's actual title
is "Why agent engineering feels decoupled"; "two loops, two bridges" is the
reviewer's description, not its literal title.

| Output | Purpose | Source treatment |
|---:|---|---|
| 1 | Can we defend this release? | Original cover theme; trust question from review/AgentOps narrative |
| 2 | Loop-based timed agenda | Newly authored; not the source's full feature agenda |
| 3 | Two loops and bridges | Local source 15's actual diagram |
| 4 | Volt customer contract | Same synthetic order/batch and non-mutation boundary |
| 5 | Harness and runtime ownership | Clean comparison; no restricted AKS card or parity claim |
| 6 | Citadel and Foundry | Local source 6's architecture; contextual layers explicitly distinguished |
| 7–8 | Demo 1 and debrief | New checkpoint; tracing appears in the inner loop |
| 9 | Code/model/human evaluation | Concept informed by reviewer reference 84 |
| 10 | Control boundaries | Supported proof versus pending tool-boundary/safety work |
| 11 | Honest optimization outcome | One completed no-improvement experiment, not a feature tour |
| 12–13 | Demo 2 and Bridge 1 | New checkpoint; historical prompt repair distinct from new code enforcement |
| 14–15 | Case file and Demo 3 | Concepts from reviewer references 171/174; actual custom workflow, not an unverified AgentOps installation |
| 16–17 | Released finding and observability | Actual DEMO claim and matching recorded trace; continuous monitoring pending |
| 18–19 | Bridge 2 and Demo 4 | Actual annotation/regression path; not a fictional native Insights result |
| 20 | Selected architecture | One reason per layer; inspired by reviewer reference 192 |
| 21–22 | Customer POC and takeaways | Adapted close inspired by 195/198; three memorable lines |
| 23–24 | Memory and identity | Hidden Q&A backups; no cross-user-isolation claim |

Restricted AKS/A-B experiment content and private release dates are excluded.
No portal screenshot, successful pipeline or score is fabricated.

## Evidence readiness

| Capability | Current evidence | Remaining condition |
|---|---|---|
| Historical hosted release | DEV 8/9 → 9/9 and separate DEMO 9/9; same ZIP/native hash | Keep v1 identities and instruction-only repair description |
| Genuine outer-loop finding | Recorded DEMO “I'm escalating” claim; same response ID in trace; local v1-pass/v2-fail regression | Optional fresh incident capture has to establish its own correlation |
| Runtime enforcement | Real local Agent tool loop and Responses HTTP stream tests | New DEV/DEMO deployment and cloud behavior verification |
| Evaluation v2 | Original nine expectations retained, additive escalation case, tool-result consistency tests | Native registration/evaluation and semantic judge calibration |
| Model rubric | Versioned rubric and eight positive/negative calibration examples | Approved model calls; authored examples alone are not calibrated proof |
| Automated release | Opt-in workflow, current check names, exact commit and response lineage, protection preflight | Configure actual OIDC roles/reviewers/branch protection and exercise failing/passing runs |
| Guardrails | Recorded native input-marker block and permitted utility | Tool-boundary route support and bounded red-team run separately approved |
| Continuous evaluation / Insights | Architecture and intended operating role only | No recurring job or native monitor configured |
| Memory | Historical one-caller DEV lifecycle proof | Backup only; Memory off in DEMO; no second-identity proof |

Use `docs/RELEASE-GATE.md` for exact activation conditions. The new workflow is
not enabled by adding YAML, and an environment name is not an approval control.
Do not rerun or overwrite historical packages, recordings or receipts.

## Presenter readiness

The spoken-route estimate excludes commands, stage directions, fallback branches,
backups and Q&A. Demonstration narration overlaps interaction. Do not add all
demo minutes again as silent time or treat an estimate as a completed rehearsal.

Rehearse the four entry/return pairs with the actual projector and browser zoom.
Use 22–26-point terminal/editor text. Put these notes on a private display.
Prepare only the relevant tabs and close notifications.

Keep the 30-second fallback cutoff for a fresh call. State whether the fallback
is a different recorded request. A pending/error response is not a pass.
Use the local routes for Demos 2–4 until cloud proof exists. After activation,
update the version bindings and notes from actual receipts before presenting.

If behind, shorten the Optimizer counters and broad trace navigation, then use
part of the architecture/POC block as recovery. Preserve the actual finding,
contract boundary and ten-minute Q&A.

## Build and verification

The source builder and manuscript remain synchronized; the final deck embeds
every section's notes. `Volt & Co - Audience.pdf` excludes hidden backups.
Rendered review images belong under `.runtime/presentation-renders`.

```powershell
python .\presentation\build_citadel_deck.py
& .\presentation\render_native.ps1
python .\presentation\make_contact_sheets.py
python .\presentation\render_manuscript.py
python .\presentation\validate_artifacts.py
python .\presentation\estimate_spoken_words.py
python .\presentation\test_recorded_evidence.py
```

The recorded viewer still shows unchanged historical evidence. The new finding
annotation is `recordings/escalation-finding.json`; local regression results
must not be relabeled as new native cloud scores.
