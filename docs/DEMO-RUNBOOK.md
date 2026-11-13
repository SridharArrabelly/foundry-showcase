# Demo runbook — "Can we defend this release?"

Four demos, one agent (`volt-support`), one customer request. Every demo answers one
question and ends on one sentence. Prepared tabs are listed per demo; open them before
the session in this order. Terminal and editor at 22–26 pt. Notifications off.

**Golden request (used in every demo):** order `VC-10482`, Volt Charge 65 batch
`CH-0722`, past the 30-day window, customer asks for a replacement.

**Rule for every live call:** 30-second cutoff. If it misses, say "here is the same
request recorded yesterday" and open the recorded tab. Never present a recording as live.

---

## Demo 1 — Build and trace (inner loop) · 8 min · after slide 9

**Question:** Can we explain how this answer was produced?

Tabs: Foundry portal (DEV project → Agents → `volt-support`), Foundry Toolbox view,
VS Code on `agent/src/evidence_contract.py`, terminal in repo root, Foundry Tracing.

1. **Portal, Create agent dialog (30 s).** Show the "Use the Microsoft Copilot harness"
   option, then cancel. Say: *"If Volt only needed Q&A with tools, I'd tick this and be done."*
2. **Agent `volt-support` (1 min).** Hosted agent, Agent Framework, version pinned.
   Say: *"We own the harness because a business rule has to be enforced in code. You'll see which one."*
3. **Toolbox (1 min).** Three read-only business tools + one Foundry IQ retrieval tool,
   curated with `allowed_tools`. Point out: no ticket, refund or shipment tool exists.
4. **Gateway (30 s).** Every model call goes through the Citadel APIM gateway:
   Entra token check, model allow-list, 20k TPM / 500k daily token contract.
5. **Live request (2 min).**
   ```powershell
   & .\agent\src\.venv\Scripts\python.exe .\scripts\capture_cases.py `
     --project-endpoint "https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev" `
     --expected-version <DEV version> --dataset ".\agent\src\.foundry\datasets\volt-regression-v2.jsonl" `
     --case replacement-recall --fresh --out .\.runtime\live-demo1 --pause-seconds 0
   ```
   Read out: `decision: eligible`, citation `VOLT-REPLACEMENT-2026-11`, and the sentence
   "No ticket, handoff, refund, shipment or order change has been performed."
6. **Trace (2 min).** Open the response in Tracing: agent span → tool calls
   (`getReturnWarrantyEligibility` with `VC-10482`/`CH-0722`) → gateway → result.
7. **Code (1 min).** `evidence_contract.py`, `supported_response()`: `decision=body["status"]`.
   Say: *"The model chose the tool and extracted the order and batch. Code wrote the decision."*

**Close:** *"Every answer has a trace, and the decision comes from the tool, not the model."*

Fallback: `presentation/Recorded evidence.html` → golden DEMO trace (43 spans).

---

## Demo 2 — Prove it (inner loop) · 8 min · after slide 13

**Question:** What does "passing" actually establish?

Tabs: Foundry Evaluations (DEV, baseline run 8/9), the failing row, VS Code tests,
terminal, red-team scorecard, guardrail probe output, Optimizer run.

1. **Baseline 8/9 (2 min).** Open the native evaluation. Open the failed row:
   answer sounds right; `decision: recommendation`, tool returned `eligible`.
   Say: *"Fluent and wrong. A human reviewer would have passed it."*
2. **Three kinds of evaluator (1 min).** Code grader (`business_contract_v2.py`: did the
   decision equal what the tool returned?), model rubric (`action_truthfulness.json`:
   did it claim an action it can't perform?), human review (the annotation in Demo 4).
3. **Fix in code, tested in seconds (2 min).**
   ```powershell
   & .\agent\src\.venv\Scripts\python.exe -m pytest .\agent\src\tests .\evaluations -q
   ```
4. **Red team (1 min).** Open the scorecard from `run_red_team.py`: attack success rate by
   risk category and strategy. Say what it covers and what it doesn't (content risks, not business logic).
5. **Guardrail (1 min).** `scripts/probe_guardrail.py`: blocklisted marker → HTTP 400 `content_filter`.
6. **Optimizer (1 min).** Completed run: baseline retained at 0.75, no better candidate.
   Say: *"The optimizer found nothing better. That is evidence too — we didn't ship a change for its own sake."*

**Close:** *"Passing means: right tool, right arguments, decision equals the tool, no invented actions, and the attacks we tried failed."*

---

## Demo 3 — The gate (Bridge 1) · 8 min · after slide 16

**Question:** Can we defend this exact artifact?

Pre-staged before the session (a gate run takes up to 45 min):
- PR A — *"Remove the evidence contract to restore streaming"* — gate **failed**.
- PR B — the v2 runtime — gate **passed**, merged; release run **waiting for approval**
  (or already promoted; then show its record).

1. **PR A (2 min).** Checks tab: `volt/live-behavior` ✕. Open the PR comment and the
   failing case. Say: *"A reasonable latency change. The gate said no, with the case to prove it."*
2. **PR B (2 min).** Required status ✓, comment with summary, environment approval history
   (who approved DEV credentials and when).
3. **Case file (2 min).** Download the artifact: candidate ZIP + SHA-256, native evaluation,
   rubric verdicts and calibration, response IDs. Say: *"Ninety days from now an auditor can reopen this."*
4. **Release (2 min).** `Agent release to DEMO` run → approve `volt-demo-promotion` live
   (or show the approval) → promotion receipt: same ZIP hash as the evaluated one → DEMO verification.

**Close:** *"Nothing reaches DEMO without passing the gate, and what we ship is byte-for-byte what we tested."*

---

## Demo 4 — Production teaches development (Bridge 2) · 10 min · after slide 20

**Question:** What did production teach us to test next?

Tabs: recorded DEMO v1 response + trace, `recordings/escalation-finding.json`,
production-watch run, GitHub issue, dataset diff, PR B (or a Copilot-drafted PR), gate run.

1. **The finding (2 min).** DEMO v1 told a customer *"I'm escalating this to human support"*.
   There is no hand-off tool. It scored **1.0** on the v1 business evaluator.
   Open the trace: no hand-off call exists. Say: *"A test that only reads the decision would have passed it. It did."*
2. **Triage → test case (2 min).** Show the annotation and the two new dataset rows
   (customer language, no coaching).
3. **Prove the test bites (2 min).** Run the regression test that replays the real response:
   ```powershell
   & .\agent\src\.venv\Scripts\python.exe -m pytest .\evaluations -q -k "post_release_finding"
   ```
   v1 grader: pass. v2 grader: fail. *"Now the gate can see it."*
4. **The loop closes (3 min).** Production watch → issue → PR (optionally drafted by the
   Copilot coding agent from the issue) → the same gate → promotion. Show PR B's run as the
   result. Say: *"AI-written or human-written, the change faces the same gate."*
5. **What runs every week (1 min).** `production-watch.yml`: scheduled re-score of DEMO;
   a failure opens a `production-finding` issue.

**Close:** *"Every production finding becomes a test before it becomes a fix."*
