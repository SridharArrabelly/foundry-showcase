# Rehearsal and contingency checklist

## Access and resources

- Confirm tenant, subscription, Sweden Central project and model deployment.
- Confirm actual agent versions and which one the demo release pointer selects.
- Verify model quota and that the presenter has Foundry data-plane permissions.
- Verify Application Insights connection, trace ingestion and telemetry read access.
- Verify GitHub repository access, Actions availability and OIDC trust on main.
- No cloud credentials in source, screenshots, traces or slide notes.

## Data and expected outputs

- All six products and three batch records are fictional.
- Shopping: VC-C65 / EUR 39.90, not the underpowered VC-C30.
- Known recall: CH-0722 -> recalled. Registered CH-0926 -> no listed recall,
  not a blanket safety guarantee. Unknown CH-9999 -> unknown.
- Missing batch: baseline demonstrates the deliberate negative-lookup defect;
  improved requests the batch. Keep baseline out of the approved release pointer.
- Core and extended regression results refer to the same dataset hashes.
- Human-reviewed feedback includes source invocation, trace ID and reviewer.

## Timing and costs

- Warm both exact hosted versions before presenting.
- Measure one full run of each segment. Use recorded long-running work on stage.
- Allow time for telemetry ingestion; don't poll the portal repeatedly in public.
- Use a small test set and bounded runs. Judge invocations also consume tokens.
- The telemetry workspace uses 30-day retention and a 1 GB daily ingestion cap.
  A cap is not an immediate exact budget stop. Review Azure costs after rehearsal.
- Stop local helpers and avoid idle paid resources after the event.

## Fallback evidence

- Capture live shopping, recall and missing-batch responses as JSON.
- Save baseline/candidate reports, dataset hashes, version IDs and timestamps.
- Save the native Foundry evaluation URL and completed status if available.
- Capture GitHub BLOCK/PASS logs and release-manifest evidence.
- Save a screen capture of the actual Foundry/App Insights trace, or use the
  recorded JSON's trace ID and tool results. Never fabricate a portal screenshot.
- Keep the slide PDF and presenter notes available offline.
- Label every fallback as recorded. Offline unit tests are not live-model results.

## Customer-specific confirmation

- Audience mix and desired technical depth.
- Sector-appropriate terminology and whether retail is an acceptable neutral sample.
- Permission to show previews, tenant/project identifiers and synthetic recordings.
- Residency, model deployment-type and network requirements.
- Acceptable telemetry content, retention, access and external tool boundaries.
- Pilot business outcome, release owner, operational owner and success criteria.
- No NDA roadmap content is included in this package.

## Day-of

Open the deck in Presenter View, close unrelated windows, silence notifications,
confirm readable zoom, and reset the terminal to the demo root. Keep a second
copy of completed evidence ready. At minute 43, start the closing regression
segment even if earlier material ran long. At minute 50, open Q&A.
