# Evidence-first release: implementation and activation

The v2 runtime, grader, rubric and workflow are **implemented locally, not cloud
validated or activated**. The serving historical DEMO version and its 9/9 result
have not changed. Its immutable ZIP and receipts remain historical evidence.

## What changed

The old repair changed instructions only. The business path always
registers `EvidenceContract` in the real Agent construction, including when
Memory supplies context. It buffers model
output, selects matching current-run tool calls/results, enforces the decision
and renders a constrained response before customer text leaves the Responses
stream. Contradictory, missing or malformed evidence produces an explicitly
logged `unavailable` response. Real tool events remain in the protocol.

The contract recognizes the synthetic workshop identifier forms and fails closed
for ambiguous/multiple identifiers. It is not a general customer-authorization
system. It cites approved references actually supplied by the business result;
IQ retrieval remains a separate inspectable source, not a basis for inventing a
tool decision. Response buffering adds time to first customer text.

DEV Memory now runs outside the contract and cannot bypass its renderer.
Memory-only requests have no business tool evidence and return `unavailable`;
the prior native Memory records are historical, not proof of the new response UX.
The v2 release gate still rejects Memory-enabled packages. No cross-user Memory
guarantee is added.

V1 dataset, grader and recordings remain unchanged. V2 adds exact tool arguments,
returned status consistency and two customer-language escalation cases (11 total).
The code check for
unsupported action phrases is intentionally a regression sentinel, not a semantic
safety classifier. The separate model rubric must also pass its eight positive/
negative calibration examples and every captured case before promotion.

The model rubric is authored but has not yet been calibrated against Azure.
The historical escalation capture passes v1 and fails the new local code check.
`recordings/escalation-finding.json` records that provenance; it is a repository
annotation, not a native Insights finding.

## Explicit activation prerequisites

Do not configure these or run the live workflow without separate approval.

1. Review and merge the workflow implementation onto `main` through the existing
   credential-free CI. This bootstrap merge is not a v2 behavioral release.
2. Confirm GitHub plan/permissions support required environment reviewers and
   branch protection. The preflight currently supports the branch-protection API,
   not ruleset-only configurations; unsupported controls fail closed.
3. Configure `volt-dev-evaluation` and `volt-demo-promotion` environments with
   required reviewers, self-review disabled and administrator bypass disabled.
4. Configure distinct OIDC identities for the exact environment subjects.
   DEV needs candidate deployment and native/model evaluation in the existing DEV
   project. DEMO needs deployment/evaluation in DEMO plus read access to DEV's
   candidate/evaluation evidence. Grant only the verified project-scoped roles
   required by the supported SDK path. Do not grant subscription Contributor.
5. Add environment/repository variables `VOLT_DEV_CLIENT_ID`,
   `VOLT_DEMO_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`.
   Azure uses OIDC; no Azure client secret is needed. Separately configure
   repository secret `VOLT_GATE_READ_TOKEN`, scoped only to this repository with
   read-only **Administration** and **Environments** access. The ordinary Actions
   token is not assumed to be able to inspect protection settings. The control
   token is passed only to the preflight reads, never to the agent or model.
   Credentials are not source files; token creation also requires approval.
6. Require the exact `volt/live-behavior` status on `main`, alongside current CI.
   Set repository variable `VOLT_LIVE_GATE_ENABLED=true` only after approval.
7. Approve a bounded trial: one candidate, eleven fresh cases, one native business
   evaluation, eight calibration prompts and eleven model-rubric judgments.
   Promotion performs another independent eleven-case/native/rubric validation.
   No retries, optimizer jobs, role changes or recurring evaluation are implicit.

All cloud jobs are disabled unless `VOLT_LIVE_GATE_ENABLED=true`. With separately
approved activation, `agent-pr-gate.yml` evaluates same-repository, non-draft PRs
after local checks and a real environment approval. It validates the PR event,
head and target, rather than incorrectly requiring a main-branch event.
It runs for every PR, including workflow/docs changes, so a required status
cannot remain pending merely because a path filter skipped the workflow.
This also means each approved PR run incurs the full bounded evaluation cost.

`agent-release.yml` resolves the exact merged PR for a main push, downloads
its successful gate artifact, and uses the evaluated head's dataset and grader
for promotion. Both stages still require human approval before Azure login.
The manual `behavioral-release.yml` remains available from reviewed `main`.
All four cloud workflows share one concurrency group and never cancel a live run.
Choose one promotion route per candidate. Do not approve both a manual promotion
and the automatic release for the same PR; concurrency serializes work but is
not a deployment deduplication mechanism.

To include promotion in one run, approve DEV first, wait for the real behavioral
status, merge the exact PR, then approve the queued DEMO environment job. If the
head changes, start a new approved run; never relabel old results.

## Evidence and gate behavior

`prepare_candidate.py` packages the exact clean commit once. `--deploy` uploads
it to the existing DEV agent using the supported code-upload SDK route and
compares the native code hash. It reuses the established DEV v6 configuration
with Memory disabled; it does not provision infrastructure. New candidate
versions can affect DEV's endpoint-current version, so do not run mid-workshop.

`validate_live_release.py --execute` registers a separate v2 code evaluator,
captures version-bound responses, runs native grading, calibrates the model judge
and scores action truthfulness. A partial failure keeps partial receipts but
does not create a passing summary.

`promote_demo.py` now defaults to `main` and the real `contracts` check. It
selects the newest run of each check, so an earlier green rerun cannot hide a
later failure. V2 additionally requires native case-level results and calibrated
model verdicts for the **same response IDs**. Promotion uploads the evaluated
ZIP without rebuilding. `verify_demo_release.py` checks independent DEMO results.

The Actions artifact is the case file: candidate ZIP/hash/source receipt, native
evaluator registration, captured responses, native case results, rubric and
calibration verdicts, and promotion/post-release receipts. Workflows request 90-day
retention, subject to repository/organization policy; export the reviewed sanitized
subset before expiration. These responses
are synthetic but should still be treated as operational evidence.

Historical command reproduction needs explicit `--contract-version v1`,
`--base-branch feature/volt-citadel`, `--required-check contracts` and
`--required-check tool-contract`. Do not rerun an already completed promotion.

## Optional scans and scheduled checks

The preview red-team script now invokes the real version-pinned agent through
the same helper as business captures. It preserves target response IDs and rejects
failed or mismatched responses and missing scorecards. It uses isolated PEP 723
dependencies, not the hosted agent's runtime environment:

```powershell
uv run --python 3.13 --script .\scripts\run_red_team.py --check-sdk
# Only after separate usage approval; replace the version with a verified DEV version.
uv run --python 3.13 --script .\scripts\run_red_team.py --execute `
  --expected-version <DEV-version> --objectives 1 --max-target-calls 20 `
  --out .\.runtime\redteam-<unique-run>
```

Default scope: four content-risk categories, one objective per category, baseline
plus EASY/Jailbreak strategies, at most 20 target calls and a 30-minute scan timeout.
Objective generation, transformation and grading incur additional usage; the
target-call limit is not a spending cap. Completion is not a zero-attack-success
claim. This is not a business-rule evaluation. Source:
[official Microsoft red-team SDK guide](https://learn.microsoft.com/azure/foundry/how-to/develop/run-scans-ai-red-teaming-agent).

Local adapter tests pass. Full SDK installation is currently blocked by a
missing wheel on the configured mirror and TLS handshake failures on the public
package host. No SDK scan, scorecard or native calibration is claimed.

`production-watch.yml` additionally requires `VOLT_PRODUCTION_WATCH_ENABLED=true`,
the protected `volt-demo-monitoring` environment, a separately scoped OIDC identity
and verified DEMO endpoint/version/evaluation variables. It replays the fixed
synthetic v1 dataset against the explicitly pinned version; it does not sample
real traffic, prove the endpoint-current version, or detect all action claims.
Only capture/scoring failures open an issue; authentication/setup failures remain
workflow failures, not invented production incidents. The issue has no dependency
on a label that may not exist. Activation and recurring costs need separate approval.

## Remaining approvals and evidence

- Actual v2 DEV deployment, native grader registration and model calibration.
- GitHub branch/environment controls and OIDC role assignments.
- Failed/green workflow runs and verified v2 DEMO promotion.
- Any bounded red-team run, native Insights, portal annotation or tool-boundary
  guardrail beyond the previously verified input marker.
- Any recurring or sampled continuous-evaluation configuration.

Until these are completed, slides must say **implemented / cloud validation
pending**, never “the new gate passed” or “the revised code is serving.”
