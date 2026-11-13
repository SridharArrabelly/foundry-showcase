# Review of PR #4 and the fixes in this package

Reviewed: `main` at 62c60f3 (merge of PR #4, "evidence-first workshop and opt-in behavioral release gate").

## Local integration status

The supplied ZIP matches the original `feature/gate-and-contract-fixes` commit.
The newer standalone runbook's demo cards (8, 13, 16, 20) were checked against
the supplied 26-slide presentation. Original files are preserved under ignored
`.runtime/incoming/cowork-review-20261113`; the rights-managed deck remains
protected and local, not published to GitHub or substituted for the current deck.

Subsequent fixes repair test discovery, exercise enforcement with Memory context,
bind preflight to real PR/main/scheduled events, add explicit cloud activation
guards and shared concurrency, and use the exact evaluated source during release.
The red-team target adapter is implemented and tested locally; full SDK installation
is blocked by package-feed/TLS failures. No cloud scan or activation has occurred.
The proposal below is historical rationale, not authorization or execution evidence.

The user subsequently supplied a General/public copy of the 26-slide deck.
That approved copy is now the current repository presentation; the protected
originals remain local. The current presenter guide, audience PDF and demo
entry/return links were synchronized when adopting it.

## What PR #4 got right (keep it)

| Recommendation | Status in PR #4 |
|---|---|
| C1 Enforce the decision in code | **Done.** `evidence_contract.py` derives `decision` from this run's tool result, validates arguments against the request and fails closed to `unavailable`. Good tests. |
| C3 Fix promotion branch/check names | **Done.** `promote_demo.py` now defaults to `main` and the real `contracts` check. |
| C4 Grade against what the tool returned | **Done.** `business_contract_v2.py` checks arguments, returned status, read-only boundary and citations. |
| C5 Rubric evaluator + escalation case | **Done (authored).** `action_truthfulness.json` with 8 calibration examples. Not yet calibrated in Azure. |
| C6 Real Bridge 2 finding | **Done (recorded).** `recordings/escalation-finding.json` ties the real DEMO "I'm escalating" claim to its response ID and trace. |
| I11 Memory to backup | **Done.** |

## Why it still "doesn't feel right" — six problems

1. **Nothing new has actually run.** v2 runtime, v2 grader, rubric and the workflow are all "implemented locally, cloud validation pending". So the deck and notes are full of caveats and the audience hears what is *not* done. **Fix: run the activation once (below) before you build anything else.** One real failing run and one real passing run turn every caveat into a screenshot.
2. **The gate is not a gate.** `behavioral-release.yml` is `workflow_dispatch` only: someone types a PR number and SHA. "Nothing reaches production without passing the gate" is not true if the gate is optional. **Fixed here:** `agent-pr-gate.yml` runs on every same-repo PR that touches agent/tools/evaluations, behind a required-reviewer environment, and posts a required status `volt/live-behavior`. `agent-release.yml` promotes on merge to `main` after a second approval, pulling the *same* evaluated ZIP from the gate run.
3. **The contract can be switched off.** In `main.py`, `middleware = [EvidenceContract()] if memory is None else [memory]` — enabling Memory silently removes the contract. **Fixed here:** the contract is always registered; Memory runs outside it. Side effect: Memory-only requests (remember my style) now render through the contract; Memory is backup-only, so that is acceptable.
4. **The model no longer writes the answer.** `ANSWERS` templates replace all model prose, and Foundry IQ retrieval no longer reaches the customer (citations come only from tool references). An SE will ask "so what is the LLM for?". **Do not undo it — teach it.** Slide: *"Code owns the decision. The model owns understanding the request."* After hardening, the model's remaining job is tool choice and argument extraction, which is exactly what the evaluation targets. Say it explicitly, and name the trade-off (no streaming, templated tone). Optional next step: let the model write a short explanation that the action-truthfulness rubric must pass, while code keeps decision, citations and the no-action sentence.
5. **Test prompts coach the agent.** The v2 `escalation-request` case says "do not pretend to create a ticket or handoff" — it tells the agent the answer. Real customers do not. **Fixed here:** rewritten in customer language, plus a second implicit escalation case (11 cases total).
6. **Case files expire in 7 days.** "A case file you can reopen" needs longer retention. **Fixed here:** 90 days in the new workflows.

Also still missing from the lifecycle: red-teaming (I1) and scheduled production evaluation (I2). **Added here:** `scripts/run_red_team.py` (needs one adapter function wired to your existing invocation code) and `production-watch.yml` (weekly re-score of DEMO; a failure opens a `production-finding` issue — that is where Bridge 2 starts).

## Files in this package

| File | Action |
|---|---|
| `agent/src/main.py` | Replace. Contract always on. |
| `agent/src/tests/test_contract_always_on.py` | Add. If `Agent(client=None)` is rejected by your Agent Framework version, pass a stub chat client. |
| `.github/workflows/agent-pr-gate.yml` | Add. Automatic PR gate. |
| `.github/workflows/agent-release.yml` | Add. Promote-on-merge with approval. |
| `.github/workflows/production-watch.yml` | Add. Scheduled DEMO evaluation; failure opens an issue. |
| `.github/workflows/behavioral-release.yml` | Keep as the manual break-glass path, or delete once the two above work. |
| `agent/src/.foundry/datasets/volt-regression-v2.jsonl` | Replace. Customer-language escalation cases (11 cases). |
| `scripts/run_red_team.py` | Add. Wire `invoke_agent()` to the helper in `capture_cases.py`. |
| `docs/DEMO-RUNBOOK.md` | Add. Click-by-click script for the four demos. |

Two things to check when you apply them:
- `scripts/live_gate_preflight.py` was written for `workflow_dispatch` "from reviewed main". On a `pull_request` event `GITHUB_REF` is `refs/pull/<n>/merge`; relax that one check if it fails. On `pull_request` the workflow file comes from the PR, so keep the required reviewer on `volt-dev-evaluation` — that approval is the control that stops unreviewed code getting credentials.
- Update `docs/RELEASE-GATE.md` retention text (7 → 90 days) and branch protection to require `volt/live-behavior`.

## Activation — do this once, before the deck (≈ half a day)

1. Merge this package via a normal PR (credential-free CI only).
2. Create environments `volt-dev-evaluation`, `volt-demo-promotion`, `volt-demo-monitoring` with required reviewers; OIDC identities per `docs/RELEASE-GATE.md` step 4; variables `VOLT_DEV_CLIENT_ID`, `VOLT_DEMO_CLIENT_ID`, `VOLT_DEMO_MONITOR_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `VOLT_DEMO_PROJECT_ENDPOINT`, `VOLT_DEMO_AGENT_VERSION`, `VOLT_DEMO_EVAL_ID`; secret `VOLT_GATE_READ_TOKEN`.
3. **Failing run (for Demo 3's "the gate says no" moment):** open a PR titled *"Remove the evidence contract to restore streaming"* that drops `EvidenceContract()` from `create_support_agent`. It is a plausible latency change. The gate should fail on `replacement-recall` / `escalation-request` (model-written decision or action claim). Do not merge it; keep the run URL and PR comment.
4. **Passing run (for Demo 3):** open the PR with the v2 runtime (`evidence_contract.py` + this `main.py`) → gate passes → merge → approve promotion → DEMO verified. Record the ZIP hash, both run URLs and the PR comment.
5. Run `run_red_team.py` once against DEV; keep the scorecard.
6. Run `production-watch.yml` once manually; keep the result.
7. Re-take screenshots for the backup slides; then rehearse with the timer.
