# Contributor instructions

This is the current Volt & Co Foundry/Citadel workshop. Read `README.md` and
`docs/OPERATIONS.md` before changing the implementation. For Foundry agent work,
load the `microsoft-foundry` skill and its applicable workflow.

- Use `feature/<short-description>` branches.
- The runtime is Agent Framework / Responses in `agent/src`; Copilot assists development.
- `tools/volt` owns current synthetic business fixtures. Do not import historical code.
- All customer data is synthetic and tools remain read-only.
- Preserve evaluation expectations, case coverage and exact-artifact provenance.
- Never label recorded evidence as live or infer execution from fluent prose.
- Memory is DEV-only. Do not claim cross-user isolation without two genuine identities.
- Keep secrets and private Memory records out of source, slides and recordings.
- Run the focused commands in the root README; CI is `.github/workflows/citadel-quality.yml`.
- Do not provision, redeploy, optimize, merge or change Azure resources merely to clean up files.
- The verified release artifact and receipts in `.runtime` are historical evidence.
  Do not rebuild them and claim the hashes are unchanged.
- The earlier 50-minute workshop is retained in Git history, not in this checkout.
  Keep local recovery copies and private environment state out of Git.
