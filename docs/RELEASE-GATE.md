# Evidence-first release: implementation and activation

The v2 runtime, grader, rubric and workflow are **implemented locally, not cloud
validated or activated**. The serving historical DEMO version and its 9/9 result
have not changed. Its immutable ZIP and receipts remain historical evidence.

## What changed

The old repair changed instructions only. The new Memory-disabled business path
registers `EvidenceContract` in the real Agent construction. It buffers model
output, selects matching current-run tool calls/results, enforces the decision
and renders a constrained response before customer text leaves the Responses
stream. Contradictory, missing or malformed evidence produces an explicitly
logged `unavailable` response. Real tool events remain in the protocol.

The contract recognizes the synthetic workshop identifier forms and fails closed
for ambiguous/multiple identifiers. It is not a general customer-authorization
system. It cites approved references actually supplied by the business result;
IQ retrieval remains a separate inspectable source, not a basis for inventing a
tool decision. Response buffering adds time to first customer text.

DEV Memory is a separate exercise that retains its existing middleware; it does
not use the business-only renderer. The v2 release gate rejects Memory-enabled
packages. No cross-user Memory guarantee is added.

V1 dataset, grader and recordings remain unchanged. V2 adds exact tool arguments,
returned status consistency and an escalation-request case. The code check for
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
7. Approve a bounded trial: one candidate, ten fresh cases, one native business
   evaluation, eight calibration prompts and ten model-rubric judgments.
   Promotion performs another independent ten-case/native/rubric validation.
   No retries, optimizer jobs, role changes or recurring evaluation are implicit.

The manual workflow takes a same-repository PR number, exact 40-character head
SHA and optional promotion flag. It runs only from reviewed `main`, validates
the head again before Azure login, serializes live runs, and requires environment
approval. Fork PRs and draft PRs are rejected. This is intentionally opt-in,
not automatic execution of every PR's code with deployment credentials.

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
calibration verdicts, and promotion/post-release receipts. Artifacts have seven-day
retention; export the reviewed sanitized subset before expiration. These responses
are synthetic but should still be treated as operational evidence.

Historical command reproduction needs explicit `--contract-version v1`,
`--base-branch feature/volt-citadel`, `--required-check contracts` and
`--required-check tool-contract`. Do not rerun an already completed promotion.

## Remaining approvals and evidence

- Actual v2 DEV deployment, native grader registration and model calibration.
- GitHub branch/environment controls and OIDC role assignments.
- Failed/green workflow runs and verified v2 DEMO promotion.
- Any bounded red-team run, native Insights, portal annotation or tool-boundary
  guardrail beyond the previously verified input marker.
- Any recurring or sampled continuous-evaluation configuration.

Until these are completed, slides must say **implemented / cloud validation
pending**, never “the new gate passed” or “the revised code is serving.”
