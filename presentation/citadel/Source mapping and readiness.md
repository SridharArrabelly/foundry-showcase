# Volt & Co enablement — source mapping, timing and readiness

**Status:** PR #2 READY FOR REVIEW, all existing CI/native business statuses successful, unmerged and no DEMO release. Baseline v1 8/9 and candidate v6 9/9 remain verified. Native single-caller Memory lifecycle passed on correctly pinned v5; cross-user isolation, exact live command and clean preview version metadata remain unresolved. All audience visuals stay unchanged.  
**Authored:** 11 November 2026.  
**Scope:** only new artifacts in this `citadel` folder. No existing deck or source presentation was edited. No commit, push, Azure operation, dependency installation or infrastructure startup was performed.

## Deliverables

| File | Purpose |
|---|---|
| `Volt & Co - Governed and improving agents.pptx` | Editable 19-slide presentation: 17 visible slides, 2 hidden Q&A backups. Full verbatim manuscript is embedded in the PowerPoint notes pane on every slide. |
| `Volt & Co - Audience.pdf` | Native PowerPoint export of the 17 visible slides only; no presenter-only readiness notes or hidden backups. |
| `Presenter manuscript.md` | Complete timed manuscript, exact switch/return cues, expected observations, slow/failure branches, technical/business Q&A, shortened routes and rehearsal checklist. |
| `Presenter manuscript.pdf` | Printable, page-numbered A4 manuscript, rendered by Microsoft Word; 40 pages. |
| `Presenter manuscript.html` | Printable/editable intermediate source for the manuscript PDF. |
| `renders\slide-01.png` … `renders\slide-19.png` | Native PowerPoint render of every slide at 1920 × 1080; includes hidden backups for review. |
| `renders\contact-1.png` … `renders\contact-4.png` | Review contact sheets, not evidence screenshots. |
| `Rehearsal bindings.json` | Structured handoff for the parent to replace each exact runtime/demo binding with verified steps and evidence. |
| `validation.json` | Content/notes/package/native text-height validation results. |

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
| 16 | Follow one fix from trace to customer | NEW | Native editable evidence chain, unchanged. Notes now distinguish verified v6 candidate evidence from the still-unfilled DEMO promotion/serving link. |
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
| 63–76 | 15 | Issue, local Copilot, review-ready PR, candidate and release boundary | 1 | 12 | 0 |
| 76–80 | 16–17 | Corrected candidate evidence, unfilled release link and close | 3 | 1 | 0 |
| **Content subtotal** | | | **22** | **52** | **6** |
| 80–90 | 17, optional 18–19 | Technical and business Q&A | | | |

The manuscript includes approximately 13,500 words **including** stage directions, readiness holds, optional branches, Q&A and appendices. Those sections are not all read in the main route. The time allocation intentionally reserves demonstration time for real observation, navigation and response latency.

**Hard cutoffs:** do not launch optimizer/Insights jobs on stage; at 72:00 show ready-for-review status and successful existing checks, while keeping merge/DEMO release unfilled. Finish candidate inspection by 77:00 and start Q&A at 80:00. Memory may run live only after its forthcoming exact command explicitly pins v5; otherwise use an approved redacted summary.

## Readiness snapshot used for authoring

This table preserves the parent's supplied state, not an independent Azure verification. No cloud actions were taken by the presentation author.

| Area | Known at authoring | Still required before live delivery |
|---|---|---|
| Environment | `rg-volt-citadel`, Sweden Central; DEV/DEMO projects share account `fdy-volt-citadel-261111`; Memory account-MI role scope is broader than project | This profile is **not hard production isolation**; review actual identities/roles for a production design |
| Hosted runtime | Historical v1 baseline and v6 candidate code/package identity verified; Memory v5 pin independently confirmed by native get_session and matching returned session identity | Preview response agent_reference misleadingly shows endpoint-current v6 for a v5 session; preserve warning, not a clean metadata claim |
| Model gateway | Managed connected-model route through APIM returned `VOLT_GATEWAY_OK` | Correlated agent execution through the route, not just standalone probe |
| APIM controls | Developer SKU; per-use-case products/subscriptions; model allowlist; 20k TPM / 500k daily token quota | Demonstrated allowed/denied access contract, redacted policy view and real status/correlation |
| Business backend | Functions with private storage and managed identity; five read-only operations; Toolbox v2 curates three business operations plus one IQ; all four executed in the hosted protocol output | Preserve actual version/response/trace association for presentation |
| Credential boundaries | Toolbox→APIM subscription credential; APIM→Function function-scoped key in Key Vault | Redacted execution proof; never claim all hops keyless |
| MCP | Native APIM business MCP verified through Toolbox v2; six direct-tool cases passed; hosted order/recall/eligibility invocations now verified | Rehearse evidence navigation; successful tool execution does not imply a correct structured decision |
| IQ | IQ actually executed in the hosted run; natural-language explanation and policy citations are right | Exact source-passage and citation navigation for the presentation |
| Memory | **Single-caller lifecycle PASSED** in four separate v5-bound sessions/conversations: native content, persistence, deletion, post-delete absence | Second genuine authenticated identity needed for cross-user scope binding/isolation; exact live v5 command forthcoming; no raw IDs/scope in materials |
| Evaluator | Baseline v1 **8/9**; candidate v6 **9 passed, 0 failed, 0 errored**, each row passed; same pinned evaluator v1 and unchanged nine cases | Completed-response business grading, not server-side agent reruns or 100% operational availability; preserved initial failure and one retry must be disclosed |
| Guardrail | Native harmless-marker **HTTP 400 / content_filter** verified at input stage; local probe proof recorded | Rehearse version/attachment navigation and recheck new deployments; no universal-safety claim |
| Optimizer | **No run yet** | Use conceptual branch only until an actual job exists; local-assisted code fix is not an optimizer result |
| Operations | Baseline mismatch preserved; issue #1, ready-for-review PR #2 and corrected v6 captures exist | Approval and release remain; no verified automatic Insights finding |
| Release | PR #2 **READY FOR REVIEW**, head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`; all existing CI/native business statuses success | Still **UNMERGED**, **no DEMO release**; approval and serving proof remain |

### Verified Toolbox preflight update

The implementation owner supplied this additional verification after the first independent visual review. Six actual direct-Toolbox cases passed: recalled CH-0722; missing batch → `needs_batch`; unknown batch → `unknown`; order VC-10482 → delivered; recall replacement → eligible for human assessment; missing order → `needs_order`. The curated set is **exactly three business operations plus one IQ tool** in **Toolbox v2**.

The exact command and evidence path are recorded in the manuscript's preflight appendix and `Rehearsal bindings.json`. Run from the demo repository root; the existing evidence is `.\.runtime\volt-tool-retrieval.json`. SDK/CLI preparation required the actual azd-managed `FOUNDRY_PROJECT_ENDPOINT`. This is preflight, not a feature-catalogue segment.

Direct Toolbox preflight, hosted baseline, candidate grading and single-caller Memory lifecycle are separate evidence. Cross-user Memory isolation, the exact live v5 command, an Optimizer run and DEMO release remain unverified/unbound. The PR is ready for review, not merged. The presentation author did not invoke Azure.

### Verified hosted execution and selected incident

The implementation owner supplied the following verified run. These facts are recorded in slide 7's PowerPoint notes, the manuscript and `Rehearsal bindings.json`; no cloud invocation was performed by the presentation author.

| Field | Verified value |
|---|---|
| Agent | `volt-support`, version **1** |
| Protocol | Responses **2.0.0** |
| Toolbox | **2** |
| Actual protocol executions | **order, recall, eligibility, IQ** — all four ran |
| Response | `caresp_02ddb9a77175f58700lAjFhWXx30P0Frxo1oLxhgKwmjshXgd7` |
| Trace | `8be3ccdd0e7b0bdcac285dcbbcdf4ef4` |
| Client elapsed | **25.372 seconds**, one observation only; not an SLA, percentile or benchmark |
| Prose and policy citations | Correct |
| Model's structured output | `decision=recommendation` |
| Actual eligibility tool result | `eligible` |

**Portal URL:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/build?version=1

**Verified CLI, from `showcase\volt-support`:**

`azd ai agent invoke volt-support --new-conversation --version 1 "For the synthetic Volt demo: my order is VC-10482 and my Volt Charge 65 batch is CH-0722. It is past the normal 30-day return window. Can I still be assessed for a replacement? Check my order, recall status and replacement eligibility, and cite the policy. Do not actually change my order."`

**Selected incident:** this remains the historical v1 failure. Corrected v6 captures pass the business case and PR #2 is ready for review with successful existing statuses. Keep versions distinct; neither status success nor readiness for review implies merge or DEMO release.

**Current story update:** audience slides remain unchanged. Notes connect the baseline failure to the local-assisted fix, ready-for-review PR and v6 9/9 business result. The single-caller Memory lifecycle is a distinct v5-pinned proof. The final DEMO release link remains unfilled.

### Completed native baseline — new hosted 8/9

Native Foundry baseline **COMPLETED**, business_contract **v1**: **8 passed, 1 failed, 0 errored of 9**. Failed item **1** is **replacement-recall**. This remains the **new hosted v1 baseline**, not the historical local 7/9. The corrected v6 result is recorded separately below.

**Report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_28da2cdf28224eb799a9a2e3d9f8672e

**Evaluation ID:** `eval_5a3774acf4f347e1bd35ae30375d0f2d`. **Run ID:** `evalrun_28da2cdf28224eb799a9a2e3d9f8672e`.

**Evidence semantics:** the native run evaluates captured **real hosted responses** and **observed successful tool calls**. It is not coherence scoring and is **not a server-side rerun of the agent**. Replay artifact: `showcase\recordings\baseline-v1.json`, commit **78b54e4**. Opening or re-scoring that saved baseline does not prove that a new candidate ran correctly.

### Verified candidate v6, issue and ready-for-review PR

- **Issue:** https://github.com/SridharArrabelly/foundry-showcase/issues/1
- **READY-FOR-REVIEW PR:** https://github.com/SridharArrabelly/foundry-showcase/pull/2
- **Existing status checks:** all existing CI and native business status success
- **PR head:** `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`
- **Candidate:** v6, native code hash matches packaged ZIP SHA-256 `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996`
- **Native result:** **COMPLETED, 9 passed, 0 failed, 0 errored**, each of nine rows verified passed
- **Comparison contract:** same pinned evaluator v1 and unchanged nine-case dataset as the v1 8/9 baseline
- **Candidate report:** https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_d6967759ba834c51b26a39296474ff0f

**Operational disclosure:** one initial model-service failed invocation was preserved and retried once. **9/9 is business grading of completed real v6 responses, not 100% operational availability.** Zero grading errors does not erase the invocation failure. Native evaluation grades captures rather than rerunning the agent server-side. No separate holdout result or full release-gate pass is implied.

**Actual development path:** cloud Copilot dispatch **failed before start** because the current gh credential was not an OAuth token. The user approved gh CLI as **SridharArrabelly**. The fix actually used **local Copilot assistance in an isolated worktree**. Do not claim cloud coding-agent execution, invent a cloud job, or present the local patch as optimizer-generated.

**Release state at 18:05:** PR #2 is **READY FOR REVIEW**, all existing CI/native business statuses succeeded, and it remains **UNMERGED** with **no DEMO release**. This presentation task does not change PR state, merge or deploy. Ready for review is not approval; serving identity and post-release customer proof remain separate.

### Verified single-caller Memory lifecycle and remaining limits

The native Memory lifecycle **PASSED for one authenticated caller**, using **four separate sessions/conversations**:

1. Remember a native item and read its exact stored content.
2. Recall the preference from a new session/conversation.
3. Forget the native item and confirm native deletion.
4. A fourth new session/conversation reports no saved preference.

Private evidence locator only: `.runtime\memory-proof-v5-pinned\summary.json`, plus four JSON step records. These private files are **not copied or read by the presentation author**. Native Memory item IDs, caller scope and raw session ID values are **not included in presentation materials**. Use only an approved redacted summary/view; never project or package raw evidence.

**Corrected transport conclusion:** session pinning **was correct**. SDK and CLI pass `extra_body.agent_session_id`; native `get_session` confirmed **v5**, and the returned session identity matched. The actual `remember_response_style` tool executed. Preview response `agent_reference` misleadingly reports endpoint-current **v6** even for the v5-bound session. The probe preserves both and warns. Do not retain the earlier “v5 actually served v6” diagnosis, and do not claim clean version metadata.

**Live binding:** current endpoint **v6 has Memory disabled**. The live Memory segment must explicitly pin **v5**. Its exact command is forthcoming; do not guess or silently invoke the current endpoint. The v6 business candidate must not be presented as having demonstrated Memory.

**Root remedy:** the documented **Foundry User** role for the **DEV project's managed identity at Foundry account scope** was required. **OpenAI User alone was insufficient.** This remains broader than project scope and is **not a hard DEV/DEMO production isolation boundary**.

**Unproved boundary:** scope text/user-ID binding and cross-user isolation still require a **second genuine authenticated identity**. Four conversations for one caller do not establish that. **Memory/evaluation model traffic is not automatically under the customer's APIM token budget.**

### Verified harmless-marker guardrail

`probe_guardrail.py` produced **HTTP 400**, error **content_filter**, type `content_safety_error`, at the **input** stage. The local proof is `.\.runtime\volt-guardrail-proof.json` from the demo repository root. Request ID: `088298eff265d56cd2438f8dbd2dcbb2`; `native_filter_observed=true`. The presentation author inspected the saved local proof and the script's arguments, without running Azure operations.

Rehearsal invocation matching the actual script, from the demo repository root:

`.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\probe_guardrail.py --project-endpoint https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev --agent volt-support --out .\.runtime\volt-guardrail-proof.json`

The probe resolves the named agent and has no version argument. Record the actual resolved version on a rerun; recheck a new deployment rather than assuming it inherits the proof. This is native marker enforcement, not a model refusal and not proof of every boundary or attack.

**Foundation evidence, not release proof:** commit `3d72b88` and passed CI at https://github.com/SridharArrabelly/foundry-showcase/actions/runs/43028286638 remain historical foundation evidence. Keep them separate from actual corrective PR #2 and candidate v6's native report. They do not prove human approval or DEMO promotion.

### Non-negotiable accuracy boundaries

- The old **7/9 → 9/9** numbers were local/CI checks; old portal metrics were coherence only. The new native captured-response comparison is **v1 8/9 → v6 9/9**, same evaluator v1 and unchanged nine cases.
- Candidate 9/9 grades completed responses, not availability: an initial model-service failure was preserved and retried once. No DEMO promotion or merge is implied.
- Cloud dispatch failed before start; actual fix used local Copilot assistance in an isolated worktree. PR #2 is now verified ready for review with successful existing statuses, but not merged or released.
- Memory content/persistence/deletion are verified for one caller; cross-user isolation is not. Current endpoint v6 has Memory off, so live Memory must pin v5 using the forthcoming command.
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

All exact controls, paths and commands remain deliberately unguessed. Fill `Rehearsal bindings.json` and replace the corresponding block in the Markdown manuscript. Then rerun the builder so the PowerPoint notes match the document.

| Binding | Slide(s) | Needed evidence |
|---|---:|---|
| RB01 | 6 | Workspace/file navigation proving chosen implementation and versioned configuration |
| RB02 | 7 | Historical baseline retained; session pinning itself verified. Distinguish authoritative get_session evidence from misleading preview agent_reference metadata |
| RB03 | 7 | Toolbox v2 and all four hosted tool executions verified in the recorded response/trace; rehearse configuration/evidence navigation |
| RB04 | 8 | IQ invocation and correct citations verified; exact source-passage/citation navigation remains to bind |
| RB05 | 9 | Allowed/restricted consumer proof, redacted policies, gateway status and correlation |
| RB06 | 10 | Native input enforcement verified: HTTP 400 / content_filter. Proof and rehearsal command bound; recheck resolved version/new deployments |
| RB07 | 11, 18 | Single-caller native lifecycle passed in four v5 sessions; exact live pin command and second-authenticated-user isolation test remain pending; redact IDs/scope |
| RB08 | 12 | Verified v1 8/9 and v6 9/9 reports; same evaluator/dataset; initial failure and one retry disclosed; no availability claim |
| RB09 | 13 | Completed native optimizer run, actual diff, tuning/holdout separation and verdict |
| RB10 | 14 | Real mismatch selected and tied to actual trace, captured replay and native failed item 1; no automatic Insights finding |
| RB11 | 14 | Expected `eligible` assessment outcome from the native case; exact regression schema/path and reviewer approval remain to bind |
| RB12 | 15 | Issue #1 and READY-FOR-REVIEW PR #2, successful existing CI/native statuses and local Copilot assistance bound; no merge/DEMO release |
| RB13 | 15 | Exact PR head, v6 native code/package hash and completed 9/9 business grading bound; full release approval not implied |
| RB14 | 15 | Approval/promotion identity, artifact provenance, deployment/serving identity, rollback and completed fallback |
| RB15 | 16 | Candidate captures pass, but approved DEMO serving version and post-promotion request are still unverified |

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

## Rebuild and verification

Run only inside this artifact folder / from the repository root. These scripts do not operate Azure or edit source decks.

```powershell
python 'demo\presentation\citadel\build_citadel_deck.py'
& 'demo\presentation\citadel\render_native.ps1'
python 'demo\presentation\citadel\make_contact_sheets.py'
python 'demo\presentation\citadel\render_manuscript.py'
python 'demo\presentation\citadel\validate_artifacts.py'
```

Existing tooling used: python-pptx, Pillow, lxml, pywin32, native PowerPoint, native Word and Poppler. No new dependency was installed. Native Office documents opened by the render scripts are closed; the PowerPoint application is not quit because the user's other presentations may be open.

The presentation builder reuses the supplied source and creates a fresh output in this folder. It intentionally replaces all selected-slide notes and prunes removed screenshots/audio relationships. It asserts exactly 19 packaged slides and rejects inherited finance/Nova/restricted-preview slide text.
