# Volt & Co enablement — source mapping, timing and readiness

**Status:** DEMO v1's nine fresh runtime cases passed; its own native evaluator v1 completed 9 passed / 0 failed / 0 errored. Same ZIP/native hash, DEMO guardrail and a separate fresh App Insights root are verified. Old incident evidence remains native capture/tool sequence + failed evaluation, not an exported App Insights span. Optimizer retained baseline; all 19 audience visuals stay unchanged.
**Authored:** 11 November 2026.  
**Scope:** only new artifacts in this `citadel` folder. No existing deck or source presentation was edited. No commit, push, Azure operation, dependency installation or infrastructure startup was performed.

## Deliverables

| File | Purpose |
|---|---|
| `Volt & Co - Governed and improving agents.pptx` | Editable 19-slide presentation: 17 visible slides, 2 hidden Q&A backups. Full verbatim manuscript is embedded in the PowerPoint notes pane on every slide. |
| `Volt & Co - Audience.pdf` | Native PowerPoint export of the 17 visible slides only; no presenter-only readiness notes or hidden backups. |
| `Presenter manuscript.md` | Complete timed manuscript, exact switch/return cues, expected observations, slow/failure branches, technical/business Q&A, shortened routes and rehearsal checklist. |
| `Presenter manuscript.pdf` | Printable, page-numbered A4 manuscript, rendered by Microsoft Word; 44 pages. |
| `Presenter manuscript.html` | Printable/editable intermediate source for the manuscript PDF. |
| `renders\slide-01.png` … `renders\slide-19.png` | Native PowerPoint render of every slide at 1920 × 1080; includes hidden backups for review. |
| `renders\contact-1.png` … `renders\contact-4.png` | Review contact sheets, not evidence screenshots. |
| `Rehearsal bindings.json` | Structured handoff for the parent to replace each exact runtime/demo binding with verified steps and evidence. |
| `validation.json` | Content/notes/package/native text-height validation results. |
| `Recorded evidence.html` | Self-contained, clearly recorded-only fallback using whitelisted baseline-v1, candidate-v6 and demo-v1 exports plus actual Optimizer outcome. No fetch/CDN/server/analytics, private Memory data or signed download URLs. |
| `build_recorded_evidence.py` | Reproducible offline-viewer source generator; source recordings are read-only. |
| `test_recorded_evidence.py` | Local offline browser validation, including no network requests and injection/URL-redaction checks. |
| `estimate_spoken_words.py` / `spoken-word-estimate.json` | Reproducible visible-slide main-route word estimate and timing risks; not a human rehearsal. |
| `recorded-evidence-manifest.json` | Input hashes, whitelisted-source provenance and output-size record. |
| `recorded-evidence-browser-validation.json` | Offline Edge results; 27 captures, 43 spans, desktop/mobile and injection checks. |

The deck contains no fabricated portal screenshot, benchmark, evaluation count, optimization improvement or release ID. Native editable shapes/text replace the source's unrelated screenshots. The cover wave artwork, masters/themes/layouts, two-loop diagram, Citadel architecture and outer-loop diagram come from the supplied workshop.

## Primary source and slide mapping

Primary source: `C:\Users\sarrabelly\Downloads\Foundry Agent Platform Workshop v1.0.0.pptx` — **198 slides, 35 hidden**. These are this file's numbers, not the older 202-slide deck's numbers.

Supporting reference was supplied at `C:\Users\sarrabelly\OneDrive - Microsoft\00FY27\Microsoft Foundry - What's New and What's Next - Bank Briefing.pptx`; no unverified screenshot or evidence was imported from it. The workshop is the actual visual/master source used here.

| New | Title | Workshop source | Treatment |
|---:|---|---:|---|
| 1 | From useful agent to governed service | 1 | Original wave cover and Foundry branding retained through its original layout/master; new editable title and event copy. Removed inherited audio/icon objects. |
| 2 | Two loops. One improving service. | 15 | **Actual source diagram retained**, including both bridges, two loops and center contract. Removed Factory-specific artifact labels; adapted PROD to synthetic DEMO. |
| 3 | One customer. One support journey. | 9 | Source scenario and visual hierarchy narrowed to Charge 65 / CH-0722 / VC-10482; editable facts → policy → human-assessment diagram. |
| 4 | Choose the operating model | 33, originally hidden | Unhidden and simplified to four decision rows; source purple comparison language; hosted runtime choice explicit. |
| 5 | Our code. Foundry's runtime. | 31 | Source responsibility split adapted to editable paired panels; Copilot development vs Agent Framework runtime explicit. |
| 6 | Where Citadel and Foundry meet | 6 | **Actual layered source diagram retained**. Volt labels adapted; A2A/security/management layers presented as architecture context, not enabled proof. |
| 7 | Give the agent governed capabilities | 47 | Removed financial screenshots and skills. Source tools → Toolbox → version concept becomes an editable capability-route diagram. |
| 8 | Ground the answer in policy | 141 | Source sources → knowledge base → agent composition rebuilt as editable diagram, restricted to implemented Azure AI Search/text+semantic extractive retrieval. No vector/federated-source claim. |
| 9 | One gateway. Explicit access contracts. | 57 | Financial operations removed. Editable model/tool routing diagram with actual Volt topology, not a portal screenshot. |
| 10 | Enforce the right boundary | 128 | Source intervention-flow design adapted to distinguish authorization, content controls and business logic. Only a verified boundary may be claimed during the demo. |
| 11 | Remember preferences, not authority | 115 | Scope concept simplified to caller A across conversations and genuine caller B. Automatic prompt-agent scope assumptions removed. |
| 12 | Evidence before confidence | 83 | Trust-by-demo versus trust-by-evidence reframed as coherence versus structured business decision + observed tool + required citation. No invented metric. |
| 13 | Optimize configuration. Review the change. | 98, informed by 101 | Source flow and evaluate/apply/release separation adapted. Factory commands and finance content removed. |
| 14 | Operation teaches DEV what to test | 185 | Source trace flywheel adapted to the genuine `recommendation` versus `eligible` mismatch; human review remains central. No artificial safety defect or automatic Insights claim. |
| 15 | A PR carries code and behavioral evidence | 159 | **Actual source DEV → gate → serving-environment diagram retained**. Corrected artifact/rebuild language and production-like DEMO label. |
| 16 | Follow one fix from trace to customer | NEW | Native chain unchanged; notes bind fresh DEMO 9/9, same artifact and separate fresh-root observability, without inventing the old incident span. |
| 17 | Useful. Governed. Measurable. Improving. | 198 | Six source takeaways reduced to four, in a clean editable close/Q&A layout. |
| 18 | Memory: a store is not an authorization system | 113, hidden backup | Scoped-store concept adapted to the narrow actual preference store. Hidden in slideshow and excluded from audience PDF. |
| 19 | Separate platform and team responsibilities | 163, hidden backup | Account/project responsibility concept adapted to named DEV/DEMO projects. Hidden in slideshow and excluded from audience PDF. |

**Explicit exclusions:** source 27 and its restricted/private-preview material; library/Nova/finance scenarios; unrelated screenshots; Factory-specific workflows; broad feature agenda; unverified enablement of Defender, Agent 365 or Purview. All inherited slide notes have been replaced, including the hidden backups.

## Exact run of show

S = slides; D = live or explicitly prepared demonstration/evidence; T = screen transitions. Prepared jobs are identified as prepared in the spoken script.

| Clock | Slides | Chapter | S | D | T |
|---|---|---|---:|---:|---:|
| 00–04 | 1–2 | Cover and two loops | 4 | 0 | 0 |
| 04–08 | 3–4 | Customer and agent choice | 4 | 0 | 0 |
| 08–13 | 5–6 | Responsibilities and Citadel | 4 | 0 | 1 |
| 13–27 | 7–8 | Business tools, IQ and customer proof | 1 | 12 | 1 |
| 27–39 | 9–10 | APIM and supported guardrails | 2 | 9 | 1 |
| 39–45 | 11 | Memory continuity and boundaries | 1 | 4 | 1 |
| 45–57 | 12–13 | Native evaluation and optimizer | 2 | 9 | 1 |
| 57–63 | 14 | Operational defect, trace and reviewed case | 0 | 5 | 1 |
| 63–76 | 15 | Issue, local Copilot, merged PR, operator gate and exact-ZIP promotion | 1 | 12 | 0 |
| 76–80 | 16–17 | Fresh DEMO result, separate observability proof and close | 3 | 1 | 0 |
| **Content subtotal** | | | **22** | **52** | **6** |
| 80–90 | 17, optional 18–19 | Technical and business Q&A | | | |

The full manuscript includes stage directions, commands, conditional branches, backups, Q&A and appendices that are not read in the main route. Count the spoken route separately.

**Spoken-only estimate:** **5,769 words** on visible slides 1–17, excluding code, stage directions, headings, fallback branches, backups and Q&A. At 120–140 words/minute, that is **48.1–41.2 minutes** of scripted speech (**44.4 minutes at 130**). After the booked six transition minutes, the 80-minute content budget leaves **25.9–32.8 minutes** for non-narrated interaction and waits. Much speech happens during the 52 demonstration/evidence minutes; do not add all 52 again as silent time.

**Overrun risks:** the opening 13-minute block needs about **13.0 minutes at 130 wpm** including its booked transition, or **14.0 at 120**, before extra clicking or pauses. Slide 1's one-minute cover and slide 6's architecture/transition slot are locally tight; slide 6 is about **44 seconds over its slot at 130 wpm** if its booked transition is fully non-narrated. The two-minute fresh-request close on slide 16 is also latency-sensitive: preserve the 30-second fallback cutoff. Trim or rehearse these areas rather than taking Q&A time. This is a word-based estimate, **not a completed human 90-minute rehearsal**. Numbers/IDs read aloud and unscripted comments add time.

**Hard cutoffs:** no new Optimizer job, capacity change, merge or promotion on stage. Use verified reports or the recorded-only offline viewer; Q&A starts at 80:00. The Memory command is bound from README, but human timing/display rehearsal and second-authenticated-user testing are still undone.

## Readiness snapshot used for authoring

This table preserves the parent's supplied state, not an independent Azure verification. No cloud actions were taken by the presentation author.

| Area | Known at authoring | Still required before live delivery |
|---|---|---|
| Environment | Shared account; DEV Memory role is account-scoped, but DEMO runtime has project-only Foundry User, no Memory account roles and Memory off | Do not upgrade this profile into a blanket hard-production-isolation claim |
| Hosted runtime | DEV v1 baseline, DEV v6 candidate and fresh DEMO v1 captures verified; same ZIP/native hash | Native grades captures, not agent reruns; preserve DEV invocation-retry disclosure and Memory metadata warning |
| Model gateway | Managed connected-model route through APIM returned `VOLT_GATEWAY_OK` | Correlated agent execution through the route, not just standalone probe |
| APIM controls | Developer SKU; per-use-case products/subscriptions; model allowlist; 20k TPM / 500k daily token quota | Demonstrated allowed/denied access contract, redacted policy view and real status/correlation |
| Model capacity | User-approved mini capacity 10→50; readback 50 RPM / 50,000 TPM; same DataZoneStandard/model version/RAI policy | APIM remains 20k TPM / 500k daily; backend capacity is not the application token contract or a cost/SLA guarantee |
| Business backend | Functions with private storage and managed identity; five read-only operations; Toolbox v2 curates three business operations plus one IQ; all four executed in the hosted protocol output | Preserve actual version/response/trace association for presentation |
| Credential boundaries | Toolbox→APIM subscription credential; APIM→Function function-scoped key in Key Vault | Redacted execution proof; never claim all hops keyless |
| MCP | Native APIM business MCP verified through Toolbox v2; six direct-tool cases passed; hosted order/recall/eligibility invocations now verified | Rehearse evidence navigation; successful tool execution does not imply a correct structured decision |
| IQ | IQ actually executed in the hosted run; natural-language explanation and policy citations are right | Exact source-passage and citation navigation for the presentation |
| Memory | **Single-caller lifecycle PASSED** in four separate v5-bound sessions/conversations: native content, persistence, deletion, post-delete absence | Exact v5 command is bound; second genuine authenticated identity still needed for cross-user isolation; no raw IDs/scope in materials |
| Evaluator | Baseline v1 **8/9**; candidate v6 **9 passed, 0 failed, 0 errored**, each row passed; same pinned evaluator v1 and unchanged nine cases | Completed-response business grading, not server-side agent reruns or 100% operational availability; preserved initial failure and one retry must be disclosed |
| Guardrail | Native harmless-marker **HTTP 400 / content_filter** verified at input stage; local probe proof recorded | Rehearse version/attachment navigation and recheck new deployments; no universal-safety claim |
| Optimizer | Initial native failure; one authorized retry **succeeded / candidate_screening_stalled**, baseline/best task-adherence 0.75, completed candidates 0, nothing applied | Max 2 is a budget, not two completed candidates; no accepted improvement; code repair is separate |
| Operations | Baseline mismatch preserved and repaired via reviewed local-assisted PR | No automatic Insights finding is established |
| Release | PR #2 merged as 04a2197 into feature/volt-citadel, main untouched; same ZIP promoted; nine fresh DEMO cases and its own native 9/9 run passed | Human rehearsal and production guarantees remain distinct from this synthetic proof |
| DEMO components | Separate contracts/connections/Toolbox v1; six business-tool cases and IQ retrieval of two actual source documents passed | Do not call these a completed nine-case agent evaluation |
| Observability | Fresh golden DEMO request has verified App Insights root operation and exact correlation fields | Old incident correlation ID was not found in exported App Insights; no automatic Insights monitor/finding is verified |

### Verified Toolbox preflight update

The implementation owner supplied this additional verification after the first independent visual review. Six actual direct-Toolbox cases passed: recalled CH-0722; missing batch → `needs_batch`; unknown batch → `unknown`; order VC-10482 → delivered; recall replacement → eligible for human assessment; missing order → `needs_order`. The curated set is **exactly three business operations plus one IQ tool** in **Toolbox v2**.

The exact command and evidence path are recorded in the manuscript's preflight appendix and `Rehearsal bindings.json`. Run from the demo repository root; the existing evidence is `.\.runtime\volt-tool-retrieval.json`. SDK/CLI preparation required the actual azd-managed `FOUNDRY_PROJECT_ENDPOINT`. This is preflight, not a feature-catalogue segment.

Direct Toolbox preflight, DEV/DEMO native grading, pinned Memory, Optimizer outcome and fresh-root telemetry are separate evidence. Cross-user Memory isolation and human timing rehearsal remain undone. Memory/promotion commands can be filled from inspected local documentation/static arguments; no Azure/Git action is needed to bind them.

### Verified hosted execution and selected incident

The implementation owner supplied the following verified run. These facts are recorded in slide 7's PowerPoint notes, the manuscript and `Rehearsal bindings.json`; no cloud invocation was performed by the presentation author.

| Field | Verified value |
|---|---|
| Agent | `volt-support`, version **1** |
| Protocol | Responses **2.0.0** |
| Toolbox | **2** |
| Actual protocol executions | **order, recall, eligibility, IQ** — all four ran |
| Response | `caresp_02ddb9a77175f58700lAjFhWXx30P0Frxo1oLxhgKwmjshXgd7` |
| Reported correlation ID | `8be3ccdd0e7b0bdcac285dcbbcdf4ef4` — **not found in exported App Insights; no verified span claim** |
| Client elapsed | **25.372 seconds**, one observation only; not an SLA, percentile or benchmark |
| Prose and policy citations | Correct |
| Model's structured output | `decision=recommendation` |
| Actual eligibility tool result | `eligible` |

**Portal URL:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/build?version=1

**Verified CLI, from `showcase\volt-support`:**

`azd ai agent invoke volt-support --new-conversation --version 1 "For the synthetic Volt demo: my order is VC-10482 and my Volt Charge 65 batch is CH-0722. It is past the normal 30-day return window. Can I still be assessed for a replacement? Check my order, recall status and replacement eligibility, and cite the policy. Do not actually change my order."`

**Selected incident:** the verified evidence is the historical native response/tool sequence and failed native evaluation. The old correlation ID has no verified exported App Insights span. The separate reviewed code repair passed DEV and fresh DEMO native evaluations; it was not Optimizer-generated.

**Current story update:** audience slides remain unchanged. Optimizer produced no accepted improvement, so its baseline stayed. Separately, the reviewed code repair reached DEMO unchanged and passed nine fresh cases/native grading. A fresh golden DEMO root proves current observability, not the old incident span. The offline viewer is recorded text evidence, not a portal screenshot.

### Completed native baseline — new hosted 8/9

Native Foundry baseline **COMPLETED**, business_contract **v1**: **8 passed, 1 failed, 0 errored of 9**. Failed item **1** is **replacement-recall**. This remains the **new hosted v1 baseline**, not the historical local 7/9. The corrected v6 result is recorded separately below.

**Report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_28da2cdf28224eb799a9a2e3d9f8672e

**Evaluation ID:** `eval_5a3774acf4f347e1bd35ae30375d0f2d`. **Run ID:** `evalrun_28da2cdf28224eb799a9a2e3d9f8672e`.

**Evidence semantics:** the native run evaluates captured **real hosted responses** and **observed successful tool calls**. It is not coherence scoring and is **not a server-side rerun of the agent**. Replay artifact: `showcase\recordings\baseline-v1.json`, commit **78b54e4**. Opening or re-scoring that saved baseline does not prove that a new candidate ran correctly.

### Verified candidate v6, merged PR and same-ZIP promotion

- **Issue:** https://github.com/SridharArrabelly/foundry-showcase/issues/1
- **MERGED PR:** https://github.com/SridharArrabelly/foundry-showcase/pull/2
- **Merge:** `04a2197` into `feature/volt-citadel`; **main untouched**
- **Existing status checks:** all existing CI and native business status success
- **PR head:** `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`
- **Candidate:** v6, native code hash matches packaged ZIP SHA-256 `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996`
- **Native result:** **COMPLETED, 9 passed, 0 failed, 0 errored**, each of nine rows verified passed
- **Comparison contract:** same pinned evaluator v1 and unchanged nine-case dataset as the v1 8/9 baseline
- **Candidate report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_d6967759ba834c51b26a39296474ff0f

**Operational disclosure:** one initial model-service failed invocation was preserved and retried once. **9/9 is business grading of completed real v6 responses, not 100% operational availability.** Zero grading errors does not erase the invocation failure. Native evaluation grades captures rather than rerunning the agent server-side. No separate holdout result or full release-gate pass is implied.

**Recorded natural-language limitation:** the actual DEMO golden answer says “Next step: I’m escalating this to human support.” Preserve it verbatim. No ticket/handoff tool exists and no ticket or handoff was created; the backend is read-only. Slides 7 and 16 now explicitly cue: **“That wording is advisory; no ticket or handoff was created. Our nine-case metric validates decision/tool/reference, not every natural-language action claim.”** The newer live rehearsal's more cautious wording does not erase the earlier limitation. No new issue, deployment or audience-slide edit is part of this clarification.

Issue #1 is **CLOSED as completed**, with a DEMO-report comment. PR #2 merged as 04a2197 and merged-branch CI **43065816204 succeeded**: https://github.com/SridharArrabelly/foundry-showcase/actions/runs/43065816204 . This is separate from historical foundation CI.

**Actual development path:** cloud Copilot dispatch **failed before start** because the current gh credential was not an OAuth token. The user approved gh CLI as **SridharArrabelly**. The fix actually used **local Copilot assistance in an isolated worktree**. Do not claim cloud coding-agent execution, invent a cloud job, or present the local patch as optimizer-generated.

**Final release proof:** the same saved ZIP SHA `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996` reached **volt-demo / volt-support v1** without rebuild; native hash verified. **All nine fresh runtime cases passed**, and DEMO's own native evaluator v1 completed **9 passed, 0 failed, 0 errored**. Export `showcase\recordings\demo-v1.json`. The actual `.runtime\volt-demo-release.json` receipt is now **runtime-verified**, finalized by `verify_demo_release.py` after checking live completed DEMO evaluation, target code hash/configuration and pinned grader.

**DEMO report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-demo/build/evaluations/eval_a0c23c81fa62456fabd5f05a11453cec/run/evalrun_c61cce9dc8774d528841ca069d992255

**DEMO endpoint:** `https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-demo/agents/volt-support/endpoint/protocols/openai/responses?api-version=v1`. Native DEMO guardrail separately returned **HTTP 400 / content_filter**; evidence `.runtime\volt-demo-guardrail-proof.json`.

**Fresh golden DEMO App Insights proof:** response `caresp_03f2cedafe9a81ff00ml4CEH7VZPqFrxR1SFFHpglDzRb3u45a`; root operation `7f4619cba4075a99c6d1b077dad68f69`; UTC `2026-11-11T17:19:09.3446407Z`; duration **23.4094s**, one observation, not an SLA; project volt-demo, version 1. Evidence `.runtime\volt-demo-golden-trace.json`. Use `customDimensions['azure.ai.agentserver.response_id']`, `customDimensions['gen_ai.agent.version']`, `customDimensions['microsoft.foundry.project.id']`. `gen_ai.agent.id` is a principal GUID, not name:version. This is separate from the old incident and is not an automatic Insights finding.

**Operator-run gate:** `showcase\scripts\promote_demo.py` checks merged exact PR, GitHub CI, native case counts and expectations, grader hash and source hash, then uploads the same ZIP. This demonstrated gate is **not GitHub branch-protection or environment enforcement**. Release uses the documented SDK/CLI multipart code route; `azd --from-package` lacks the necessary code-zip metadata here. Inspect the script/recorded evidence; do not rerun deployment for the presentation.

**Receipt finalizer—operator documentation/contingency only:** from demo root, `.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\verify_demo_release.py --receipt .\.runtime\volt-demo-release.json --runtime-evaluation .\showcase\volt-support\src\agent-framework-agent-basic-responses\.foundry\results\demo-v1\evaluation.json`. Static flags and the matching evaluation receipt were checked read-only. This command queries Azure and writes the receipt; it does not rerun the agent. Do not execute it just to stage an already completed verification or edit status manually. Neither script is GitHub-enforced protection.

**Fresh single-case live route is now rehearsed:** use the exact `showcase\README.md` “Start the presentation” command, copied into slide 16 notes and `fresh_demo_single_case` in the bindings. Keep `PYTHONIOENCODING=utf-8`, a new timestamped `.runtime\live-...` output, the DEMO project, `--expected-version 1`, `--case replacement-recall`, `--fresh` and `--pause-seconds 0`. The observed rehearsal returned eligible with all policy citations. `--fresh` refuses cached output/replay: a fixed cached directory is not a live demonstration. This one request remains separate from the nine-case release gate and from the prior golden request's 43-span trace.

**DEMO bindings:** separate contracts, connections and Toolbox **v1**. Connection names are `volt-demo-models-LLM`, `volt-demo-business-tools`, `volt-demo-policy-knowledge`; names must be distinct across projects due to account connection-ownership collisions, while Toolbox labels remain stable. Six business-tool cases and IQ retrieval of two actual source documents passed. Those component checks are distinct from the now-completed fresh nine-case agent run and DEMO native 9/9 result.

**DEMO identity:** native agent runtime has **project-only Foundry User**, **no Memory account roles**, and **Memory OFF**. DEV v5's single-caller Memory demonstration remains distinct.

### Final native Optimizer outcome — baseline retained

The user approved instruction-only search with a **maximum of two candidates**, unchanged model/tool permissions, separate training/validation examples and **no automatic application**.

Initial native job `opt_69c51eb68b4a43bc8c9d21b748f190c0` **FAILED during candidate evaluation**. APIM gateway evidence showed actual upstream model **429s**, followed by Citadel circuit-breaker **503s**. This was not merely a local DNS/watcher failure. The mini deployment read **10 RPM / 10,000 TPM**, below the **20,000-TPM application contract**.

User-approved capacity increase **10→50** read back **50 RPM / 50,000 TPM**, unchanged DataZoneStandard, model version and RAI policy. APIM stayed **20k TPM / 500k daily**. The user authorized **ONE retry**.

Retry **opt_bcc5008122ae4a88ab10bfa428ecf616**:

| Field | Verified result |
|---|---|
| Native job status | `succeeded` |
| Termination | `candidate_screening_stalled` |
| Baseline task-adherence | **0.75** |
| Best task-adherence | **0.75** |
| Candidate budget | **max 2**, not two completed candidates |
| Completed candidate count | **0** |
| Returned result | **Only baseline** |
| Accepted optimized candidate / improvement | **None** |
| Applied candidate | **NONE** |

**Report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/optimization/opt_bcc5008122ae4a88ab10bfa428ecf616

**Portable prepared source:** `showcase\recordings\optimizer.json`; optional full local result `.runtime\volt-optimizer-retry-result.txt`. The offline generator now reads only committed/sanitized recording exports, never `.runtime`. `memory.json` is available but remains unused because this viewer has no Memory panel. Initial job report: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/optimization/opt_69c51eb68b4a43bc8c9d21b748f190c0

Verified portal labels: **Optimization outcome: No improvement**, Succeeded, Candidates 0, baseline/best 0.75, elapsed **18m23s**, Total tokens **207.6K**, baseline-only/stall-limit warnings. **Do not click Deploy best candidate**: it would deploy the retained baseline, not an accepted improved candidate. Use the completed run rather than waiting eighteen minutes on stage.

Reported tokens: agent **143,266**, evaluation **49,373**, optimization **14,979**. Agent average **20.682s across 20 calls**. These are run counters, **not an SLA, cost guarantee or assurance that all usage is under the customer APIM budget**.

The portal baseline table's **11.1s / 4.6K tokens** is a different aggregation from the job-wide 20.682s across 20 calls. Do not mix them or claim a before/after latency improvement.

**Interpretation:** succeeded describes job status, not quality improvement. Preserve termination/warnings, zero completed candidates, baseline-only output and nothing applied. Retain the Optimizer baseline. The reviewed business-contract code fix is separate; its 8/9→9/9 scores are not this 0.75 task-adherence metric. The Optimizer job retry is also distinct from the invocation retry disclosed in the business captures.

### Verified single-caller Memory lifecycle and remaining limits

The native Memory lifecycle **PASSED for one authenticated caller**, using **four separate sessions/conversations**:

1. Remember a native item and read its exact stored content.
2. Recall the preference from a new session/conversation.
3. Forget the native item and confirm native deletion.
4. A fourth new session/conversation reports no saved preference.

Private evidence locator only: `.runtime\memory-proof-v5-pinned\summary.json`, plus four JSON step records. These private files are **not copied or read by the presentation author**. Native Memory item IDs, caller scope and raw session ID values are **not included in presentation materials**. Use only an approved redacted summary/view; never project or package raw evidence.

**Corrected transport conclusion:** session pinning **was correct**. SDK and CLI pass `extra_body.agent_session_id`; native `get_session` confirmed **v5**, and the returned session identity matched. The actual `remember_response_style` tool executed. Preview response `agent_reference` misleadingly reports endpoint-current **v6** even for the v5-bound session. The probe preserves both and warns. Do not retain the earlier “v5 actually served v6” diagnosis, and do not claim clean version metadata.

**Live binding filled from README:** from demo root, `.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\probe_memory.py --project-endpoint https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev --expected-version 5 --out .\.runtime\memory-rehearsal`. Do not invoke it during artifact preparation. Human rehearsal/redaction is still required; DEV v6 and DEMO v1 have Memory off.

**Root remedy:** the documented **Foundry User** role for the **DEV project's managed identity at Foundry account scope** was required. **OpenAI User alone was insufficient.** This remains broader than project scope and is **not a hard DEV/DEMO production isolation boundary**.

**Unproved boundary:** scope text/user-ID binding and cross-user isolation still require a **second genuine authenticated identity**. Four conversations for one caller do not establish that. **Memory/evaluation model traffic is not automatically under the customer's APIM token budget.**

**Forget scope:** only the native Memory item was deleted. Historical conversations and telemetry were not erased. The offline viewer intentionally omits private Memory evidence.

### Verified harmless-marker guardrail

`probe_guardrail.py` produced **HTTP 400**, error **content_filter**, type `content_safety_error`, at the **input** stage. The local proof is `.\.runtime\volt-guardrail-proof.json` from the demo repository root. Request ID: `088298eff265d56cd2438f8dbd2dcbb2`; `native_filter_observed=true`. The presentation author inspected the saved local proof and the script's arguments, without running Azure operations.

Rehearsal invocation matching the actual script, from the demo repository root:

`.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\probe_guardrail.py --project-endpoint https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev --agent volt-support --out .\.runtime\volt-guardrail-proof.json`

The probe resolves the named agent and has no version argument. Record the actual resolved version on a rerun; recheck a new deployment rather than assuming it inherits the proof. This is native marker enforcement, not a model refusal and not proof of every boundary or attack.

**Foundation evidence, not release proof:** commit `3d72b88` and passed CI at https://github.com/SridharArrabelly/foundry-showcase/actions/runs/43028286638 remain historical foundation evidence. Keep them separate from actual corrective PR #2 and candidate v6's native report. They do not prove human approval or DEMO promotion.

### Non-negotiable accuracy boundaries

- The old **7/9 → 9/9** numbers were local/CI checks; old portal metrics were coherence only. The new native captured-response comparison is **v1 8/9 → v6 9/9**, same evaluator v1 and unchanged nine cases.
- DEV and DEMO 9/9 are separate captured-response business results, not availability guarantees. DEV's preserved invocation failure/retry remains disclosed; DEMO has nine fresh cases and its own run.
- Cloud dispatch failed before start; actual fix used local Copilot assistance. PR #2 merged into feature/volt-citadel, not main, and the same ZIP reached DEMO.
- The promotion gate is operator-run, not a claim of GitHub branch-protection or environment enforcement.
- Optimizer ended succeeded/candidate_screening_stalled with only baseline, 0.75/0.75, completed count 0, max-two budget and nothing applied. Do not claim quality improvement, two completed candidates or an optimizer-generated business fix.
- Memory content/persistence/deletion are verified for one caller; cross-user isolation is not. The bound README command pins DEV v5; DEV v6 and DEMO v1 have Memory off.
- Native session evidence confirms v5 despite misleading preview agent_reference v6. Preserve both facts; never call the version metadata clean.
- No private native Memory IDs, caller scope or raw session IDs may appear in presentation artifacts. Private evidence is referenced, not copied.
- The native baseline grades captured real responses and successful tool calls. It does not rerun the agent server-side; unchanged replay data cannot establish a new candidate's behavior.
- A registered evaluator, created memory store, deployed guardrail policy or “active” hosted deployment is not runtime proof.
- The model deployment is data-zone, not Sweden-only processing. Public Entra-authenticated Foundry is approved; this is not all-private networking.
- No real customer order-ownership authorization exists in the demonstration. APIM consumer permission is not customer ownership.
- Token quotas are not dollar caps. Service-internal IQ/memory/evaluation/optimizer traffic is not automatically governed by the selected model gateway.
- Account-MI scope for Memory is broader than project, and this shared-account DEV/DEMO profile is not hard production isolation. Memory/evaluation model traffic is not automatically under the customer APIM token budget.
- APIM Developer, Search and hosted compute may incur idle costs. No measured latency, cost reduction or optimizer improvement is invented.
- No refund or shipment is executed. “Human assessment” is the appropriate next step in this synthetic journey.
- The selected incident is the genuine structured-decision mismatch, not a seeded missing-batch defect. A trace becomes a regression only after review; no automatic Insights finding is inferred.
- A prepared result is labelled prepared, with its run/version identity. No manually edited prompt is called an optimizer result; no manually authored issue is called an Insight.

## Binding handoff to the parent

Verified technical facts, paths and commands are now bound in `Rehearsal bindings.json` and the manuscript. Human screen navigation/timing and the explicitly optional restricted-consumer drill remain rehearsal decisions, not guessed working controls. After any further edits, rebuild notes and manuscript together.

| Binding | Slide(s) | Needed evidence |
|---|---:|---|
| RB01 | 6 | Runtime main.py, response_contract.py and settings.py paths bound; rehearse screen navigation |
| RB02 | 7 | Historical baseline retained; session pinning itself verified. Distinguish authoritative get_session evidence from misleading preview agent_reference metadata |
| RB03 | 7 | Toolbox v2 and all four hosted tool executions verified in the recorded response/trace; rehearse configuration/evidence navigation |
| RB04 | 8 | IQ invocation/reference/title evidence bound to native captures and offline viewer; live Knowledge-pane navigation optional |
| RB05 | 9 | Allowed/restricted consumer proof, redacted policies, gateway status and correlation |
| RB06 | 10 | Native input enforcement verified: HTTP 400 / content_filter. Proof and rehearsal command bound; recheck resolved version/new deployments |
| RB07 | 11, 18 | Single-caller native lifecycle passed; exact v5 pin command bound; second genuine identity and human redaction/timing rehearsal remain |
| RB08 | 12 | Verified DEV baseline/candidate and independent fresh DEMO 9/9 reports; invocation retry disclosed; exact native portal DOM labels recorded |
| RB09 | 13 | Actual native retry/report bound: succeeded plus stalled screening, baseline 0.75 only, completed candidates 0, max-two budget, nothing applied |
| RB10 | 14 | Real mismatch evidenced by native response/tool sequence and failed evaluation; old exported App Insights span unverified; offline replay ready |
| RB11 | 14 | volt-regression.jsonl replacement-recall row and business_contract.py paths bound; expected eligible; only code-view timing remains |
| RB12 | 15 | Merged PR #2, merge 04a2197 into feature/volt-citadel, main untouched; actual local Copilot assistance |
| RB13 | 15 | Reviewed head, saved ZIP/native v6 hash and DEV 9/9 bound; separate completed DEMO 9/9 also bound |
| RB14 | 15 | Operator promotion and verify_demo_release.py command/input bound; actual receipt runtime-verified; no stage rerun or GitHub-enforced-protection claim |
| RB15 | 16 | Exact fresh single-case CLI successfully rehearsed; UTF-8/new timestamp/--fresh/v1; separate nine-case gate and prior golden trace |

## Final binding classification

**Filled from verified facts or local read-only sources:** the three recording exports and native report links/counts; answer/decision/citation/tool fields; portable Optimizer outcome; merged PR and artifact/receipt paths; promotion and finalizer commands; actual runtime-verified receipt; rehearsed fresh single-case DEMO command with UTF-8/new timestamp/--fresh/v1; DEMO guardrail/prior root correlation; Memory v5 command; runtime/dataset/evaluator paths. Required technical bindings are supplied; no further technical placeholder needs user input.

**Still needs human input or verification:** (1) a real 90-minute timing/network/display rehearsal, including safe redaction of the live Memory segment; (2) a second genuinely authenticated identity and scope/user-binding isolation test; (3) a restricted-consumer APIM denial capture if that optional negative-access drill is retained—permitted calls alone do not prove denial. Otherwise use the clearly labelled conceptual branch for that drill.

**Not claimed, not missing screenshots to invent:** automated Insights monitoring/findings are **not configured**; no accepted/applied Optimizer candidate, baseline-incident App Insights span, rollback drill, production compliance or SLA is claimed. Portal screenshots timed out twice; the native DEV 9/9 page was verified by DOM. The offline viewer is recorded output, not simulated live portal rendering.

The fresh golden DEMO export `showcase\recordings\demo-trace.json` contains **43 verified correlated spans**. The offline viewer includes only whitelisted names/durations/recorded success and the verified root summary; no raw customDimensions or application/principal IDs are embedded.

Every binding needs either a verified fallback capture or an explicit concept-only branch. The manuscript already supplies the spoken wording for both. Do not remove the fallback wording merely because the portal worked once.

## Visual QA and independent review

Native PowerPoint render completed for all 19 slides. The first pass found crowded Toolbox text, overflow in the five-stage boundary flow, a wrapping memory warning and cramped architecture/footer copy. These were corrected and re-rendered. A further native text-bounds pass identified several source/narrow-box height issues, which were also corrected.

**Independent all-slide review completed:** the reviewer inspected all 19 native images and found no blocking overlap or clipping. Four focused corrections were requested and applied: slide 2 now has shorter, larger loop/bridge/contract text; slide 15 has shorter, larger gate captions and feedback text; slide 6 no longer has an unexplained A2A asterisk; slide 11 shows write into memory and retrieval back to the caller. No additional agent was spawned.

**All independent visual reviews passed**, including the later incident edits on slides 14 and 16. This update changes only notes, manuscript and readiness/bindings. Native-render hash comparison confirms **all 19 audience/backup images are identical**; validation reports no text-height warnings. No audience wording or geometry changed. The original full-review priorities are retained below for rehearsal context:

- **2:** readability of the preserved original inner/outer-loop diagram and its two bridges.
- **6:** source Citadel diagram; contextual layers must not look like a blanket enablement claim.
- **7–11:** diagram labels, line wrapping and separation between nodes, bodies and captions.
- **15:** original outer-loop diagram; candidate/DEMO text and long bottom banner.
- **16:** new six-link evidence chain and arrow direction.
- **18–19:** backup-only state and correct exclusion from the audience PDF.

No low-contrast or overflow issue is knowingly deferred after the local fix-and-render cycle. The dense source diagrams on 2 and 6 remain intentionally information-rich; test projector readability during the parent's independent review.

The offline HTML is about 45 KB, self-contained and marked **RECORDED EVIDENCE — NOT LIVE**. Local headless Edge validation passed with zero page network requests/console errors, all case comparisons, 43 span rows, light/dark themes, responsive layouts and script/DOM-injection fixtures. The small-screen decision fields were stacked after visual inspection to avoid splitting “recommendation.” Review captures: `renders\recorded-evidence-desktop.png` and `renders\recorded-evidence-mobile.png`. These are viewer screenshots, not invented portal evidence.

The independent reviewer passed both viewer captures. The portability update preserves the existing layout and omits the optional Memory panel; generator inputs are entirely under `showcase\recordings`, including sanitized `optimizer.json`.

## Rebuild and verification

Run only inside this artifact folder / from the repository root. These scripts do not operate Azure or edit source decks.

```powershell
python 'demo\presentation\citadel\build_citadel_deck.py'
& 'demo\presentation\citadel\render_native.ps1'
python 'demo\presentation\citadel\make_contact_sheets.py'
python 'demo\presentation\citadel\render_manuscript.py'
python 'demo\presentation\citadel\validate_artifacts.py'
python 'demo\presentation\citadel\build_recorded_evidence.py'
python 'demo\presentation\citadel\test_recorded_evidence.py'
python 'demo\presentation\citadel\estimate_spoken_words.py'
```

Existing tooling used: python-pptx, Pillow, lxml, pywin32, native PowerPoint, native Word and Poppler. No new dependency was installed. Native Office documents opened by the render scripts are closed; the PowerPoint application is not quit because the user's other presentations may be open.

The presentation builder reuses the supplied source and creates a fresh output in this folder. It intentionally replaces all selected-slide notes and prunes removed screenshots/audio relationships. It asserts exactly 19 packaged slides and rejects inherited finance/Nova/restricted-preview slide text.
