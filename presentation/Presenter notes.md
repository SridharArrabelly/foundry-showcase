# Slide-by-slide presenter notes

Visual rebuild: original Azure artwork and workshop diagrams, with explicit run formatting for canvas readability.


## Slide 1: Microsoft Foundry: from prototype to operated service

TIME: Holding slide; welcome included in 00:00-02:00

TALK TRACK
Welcome. This is a practical story, not a feature tour. We will follow a single assistant from useful behaviour to a reviewable release and back into development. The slides supply the mental model; the demo supplies the evidence.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
The first distinction is between an impressive answer and an operated service.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slides 9 and 12; current Microsoft Foundry product name.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Original Azure title artwork from the Bank Briefing. Black text on the original light field. Explicit run-level font size and color.


## Slide 2: One customer request. A complete operating story.

TIME: 00:00-02:00

TALK TRACK
A prototype may answer impressively while using the wrong tool, skipping a policy, or being impossible to reproduce. We are not claiming building agents is trivial. We are saying that building is only part of the responsibility. Foundry connects development and operations; our engineering policies make the connection enforceable.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Let's give that responsibility a concrete customer and a small set of checkable facts.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Adapted from workshop slide 9; avoid unsupported reliability or performance claims.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Flow layout and outcome-first wording adapted from Bank Briefing slide 4; replaces disconnected generic cards.


## Slide 3: Meet Volt & Co

TIME: 02:00-04:00

TALK TRACK
Volt and Co is the same sample use case as the workshop. We deliberately narrowed it to three read-only tools. The fixture has a 30W charger at EUR 19.90, a 65W charger at EUR 39.90, and a 100W charger at EUR 59.90. Volt Book 14 requires 65W. These numbers are fictional and mechanically checkable. Later, the same customer's recall enquiry will expose a missing-information case.

ON SCREEN / DEMO CUE
Point to Find, Check and Support. Do not introduce the other workshop skills.

TRANSITION OUT
We will follow these three capabilities around two loops.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slide 6 and notes. New synthetic fixture: volt/data.json; no claim that these prices came from the original deck.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Data-row layout follows Bank Briefing slides 3 and 8. Prices/specifications are the deployed synthetic fixtures—not original workshop results.


## Slide 4: One continuous system: inner and outer loop

TIME: 04:00-07:00

TALK TRACK
The workshop's inner loop is build/connect, run/debug/trace, evaluate/guard and improve in DEV. The outer loop is gate/release, readiness, operation and reviewed feedback. The forward bridge carries source revision, configuration, dataset and results. The return bridge carries evidence plus a reviewed expectation. A production trace is not a correct answer by definition. For this compact demo, DEV is local and the serving target is a Foundry demo project; production would separate environments and identities more fully.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Before the first request, here is exactly where GitHub and Foundry each participate.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slides 12-14 and speaker notes. https://learn.microsoft.com/azure/foundry/agents/concepts/development-lifecycle

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Actual diagram from workshop slide 12. Implementation filenames were shortened in the image for legibility.

UPDATED PRESENTER CUE
Treat the full diagram as the reference lifecycle. This live demo does not implement every box: DEV is local; the hosted serving environment is a demo project. Do not claim production isolation, Agent 365, a managed Toolbox or automated red teaming.


## Slide 5: Build in GitHub. Run and improve in Foundry.

TIME: 07:00-09:00

TALK TRACK
There are two distinct uses of Copilot: the developer assistant and the SDK harness inside our business agent. This is a hosted agent, not a managed Copilot-harness prompt agent. The model is deployed in Foundry and authenticated with Entra; no GitHub token is embedded. The runtime exposes only three reviewed business tools. The demo does not connect a managed Foundry Toolbox or APIM gateway; those remain an extension path rather than a claim about this implementation. Our custom application spans complement Foundry-host telemetry.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Let's prove the useful path first. I will not spend your time provisioning infrastructure live.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slides 6 and 30. Official Microsoft Copilot SDK Invocations sample; github/copilot-sdk BYOK documentation.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Enlarged BUILD and HOST sections from the original workshop slide 23 architecture graphic.

UPDATED PRESENTER CUE
The graphic is the broader platform reference, not a claim that every shown integration is configured. Point specifically to Copilot SDK, hosted runtime, models, evaluation and tracing.


## Slide 6: Watch the answer—and the path that produced it

TIME: 09:00-16:00

TALK TRACK
The 30W charger is cheapest, but it does not meet the device's 65W requirement. The 65W model is the cheapest compatible in-budget choice. Open the structured result, not just the prose. Catalog and compatibility do not guarantee that a specific batch is safe. Then run the known recall enquiry from the source deck.

ON SCREEN / DEMO CUE
Transition 09:00-10:00. In the demo directory: python scripts/demo.py ask "Find the cheapest charger for my Volt Book 14 under EUR 50." --out evidence/shopping.json. Then ask "Is my Volt Charge 65 from batch CH-0722 safe to use?". Foundry portal: project > agent > Traces; open a completed request. Tool evidence is in the captured JSON even if portal ingestion is delayed.

TRANSITION OUT
Switch to the prepared demo surface now.

RETURN FROM DEMO
We have explained one execution. Now ask whether it holds across a representative set.

IF TIME OR TECHNOLOGY FAILS
Use the captured shopping and recall JSON plus the telemetry view from rehearsal. Say when it was recorded. Do not wait more than 30 seconds for an ingested trace.

SOURCE / CLAIM BOUNDARY
Executable commands are in docs/PRESENTER.md and scripts/demo.py. Do not present an offline tool test as a live model evaluation.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Editable request-to-tool sequence. This is a diagram, not a fabricated portal screenshot. Exact commands remain in the speaker notes.


## Slide 7: From a convincing answer to measurable evidence

TIME: 16:00-17:00

TALK TRACK
The dataset is part of the product contract, not an afterthought. We include shopping, insufficient budget, incompatibility, known recalls, unknown batches and refusal of fabricated invoices. We compare candidates on identical reviewed cases and retain failures. We do not invent an accuracy or cost-improvement percentage. A synthetic set is useful for a demonstration, but a production evaluation needs customer-specific distribution and expert labels.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Different questions need different kinds of checks.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slide 84; datasets/core.jsonl.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Chart uses the actual baseline and candidate reports (7/9 versus 9/9). It does not import results from other agents.

UPDATED PRESENTER CUE
Do not translate this into a percentage accuracy claim. The model-judged coherence scorecard is a separate measurement.


## Slide 8: Three checks. Three different jobs.

TIME: 17:00-18:00

TALK TRACK
We use deterministic assertions where the fixtures give an objective answer. A native Foundry coherence evaluation scores the captured live responses; it does not replay the agent and it does not certify recall correctness. The human reviewer defines what missing information should cause the agent to do. In production, add calibrated semantic and safety evaluators suited to the risk profile. Check availability per evaluator rather than calling the whole catalog GA.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Now look at a baseline and a deliberately narrow correction.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slide 86. https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Text hierarchy and status-lane layout adapted from Bank Briefing slide 8; evaluator logic from workshop slide 86.


## Slide 9: Change the contract—not just the wording

TIME: 18:00-25:00

TALK TRACK
The intentional baseline defect is in the recall tool: no batch was mistaken for a negative recall lookup. This is not a claim that the model happened to fail today. We show the defect and its consequence explicitly. The improved version returns needs_batch. The agent then asks for the missing fact. The core suite and the extended regression suite are distinct; a passing core suite never implied it covered the missing-batch case.

ON SCREEN / DEMO CUE
Show volt/domain.py recall_notices and its baseline/improved branch. Open the actual baseline and improved report files. Run: python scripts/check_contract.py --variant baseline (expected exit 1), then --variant improved. Run the focused live missing-batch query against the saved version. Open the native Foundry evaluation URL from evidence/foundry-evaluation.json.

TRANSITION OUT
Switch to the prepared demo surface now.

RETURN FROM DEMO
The candidate is improved on this reviewed contract. It still needs a controlled release decision.

IF TIME OR TECHNOLOGY FAILS
Use completed live reports. The offline contract command proves the business-code correction only; label it as such. Skip a fresh full model evaluation if it exceeds the budget.

SOURCE / CLAIM BOUNDARY
Executable commands are in docs/PRESENTER.md and scripts/demo.py. Do not present an offline tool test as a live model evaluation.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Readable before/after visualization of the actual tool defect and fix. Exact code and results are in the demo; this slide is not a terminal screenshot.


## Slide 10: How a candidate becomes an operated service

TIME: 25:00-27:00

TALK TRACK
A model score is not a release system. Our workflow determines which checks run and whether execution continues. The repository's credential-free quality workflow runs unit and tool-contract tests. Live evaluation evidence is separate and must not be relabelled as CI's offline output. The release script accepts only a passing live scorecard for the evaluated version and creates a release manifest. Production should add environment approvals and separate deployment identities; a private repository's branch-protection availability depends on the GitHub plan.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
I will show actual completed checks, not wait for a cold deployment.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slides 14, 162 and 178. Microsoft hosted-agent CI/CD quickstart.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Actual outer-loop bridge diagram from workshop slide 162. Its DEV/PROD labels describe the reference production pattern.

UPDATED PRESENTER CUE
The caption explicitly distinguishes the deployed demo from production isolation. Do not claim that a passing local score changes the portal's default routing.


## Slide 11: A release we can explain

TIME: 27:00-34:00

TALK TRACK
The blocked workflow is intentionally run with the baseline business contract; it is a real GitHub Actions failure, not a screenshot of a fabricated pipeline. The improved run passes that contract. Keep offline CI and live model evaluation distinct. Open the recorded live candidate scorecard, the version and the release manifest. Invoke that exact deployed version. Say clearly that deployment happened during rehearsal.

ON SCREEN / DEMO CUE
Transition 27:00-28:00. GitHub repository > Actions > Volt quality gate: open the baseline and improved runs. Open evidence/release.json. Run python scripts/demo.py ask "Check Volt Charge 65 batch CH-0926 for a recall." --version <recorded improved version>. Use the recorded version from the manifest, not an invented number.

TRANSITION OUT
Switch to the prepared demo surface now.

RETURN FROM DEMO
A release only proves the expectations we wrote down. Operations brings us the next question.

IF TIME OR TECHNOLOGY FAILS
Use captured Actions logs and the release manifest if GitHub or Azure is slow. Never say a full production governance pipeline is enforced if required checks/environment controls have not been configured.

SOURCE / CLAIM BOUNDARY
Executable commands are in docs/PRESENTER.md and scripts/demo.py. Do not present an offline tool test as a live model evaluation.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Document-flow layout from the Bank Briefing's worked scenario. Uses the real version 4 release and live workflow, not generic success badges.


## Slide 12: Operations teaches development what to test

TIME: 34:00-35:00

TALK TRACK
Our production-like traffic is synthetic. We intentionally include an enquiry that omits the batch number. We inspect the actual captured result and its tool path, then review what the response should have done. The feedback command requires explicit approval and records the reviewer, source invocation, trace ID and content hash. It refuses to overwrite an existing review file. This is an application workflow, not an automatic Foundry correction.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Let's carry one observed interaction back into the test set.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slides 14, 189 and 193. Trace-to-dataset conversion is preview; this package also includes an explicit code-first reviewed-row path.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Original lifecycle illustration from workshop slide 67.

UPDATED PRESENTER CUE
The diagram describes the broader platform loop; Insights and Agent Optimizer are not live dependencies in this implementation. Our actual path is capture, review, add a test, fix and re-evaluate.


## Slide 13: Close the loop with one new test

TIME: 35:00-47:00

TALK TRACK
Missing information is not a negative result. Show the recorded baseline trace and the returned no_recall status despite the absent batch. Review the correct contract: ask for the batch, do not assert safety. Export one reviewed case. Return to DEV and show the fix. Run it against the earlier and corrected versions or use the completed reports if time is short. Do not patch the serving agent directly from an operational screen.

ON SCREEN / DEMO CUE
35:00-42:00: Foundry Monitor/Traces or Application Insights; open the seeded missing-batch request. Run the feedback command in docs/PRESENTER.md with a human reviewer. 42:00-43:00: return to DEV. 43:00-47:00: show the focused regression FAIL/PASS and full core+regression evidence. Foundry's native Add to dataset path is optional preview, not required for the code-first loop.

TRANSITION OUT
Switch to the prepared demo surface now.

RETURN FROM DEMO
The next release has a stronger contract because operations supplied a new case.

IF TIME OR TECHNOLOGY FAILS
Preserve this segment if running late: skip fresh batch evaluation or optional preview screens, but show observation, review, test and corrected evidence. Use the same captured request, not another agent's screenshots.

SOURCE / CLAIM BOUNDARY
Executable commands are in docs/PRESENTER.md and scripts/demo.py. Do not present an offline tool test as a live model evaluation.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Editable feedback-loop diagram anchored in the captured missing-batch case.


## Slide 14: One system. Four things to remember.

TIME: 47:00-49:00; 49:00-50:00 buffer

TALK TRACK
We built with GitHub Copilot, ran a Copilot SDK harness in Foundry, inspected tool evidence, measured behaviour, showed a reviewable release and returned an observation to development. The differentiator is the connection across these activities. For a customer pilot, choose one outcome, agree its failure boundaries and define who owns the release decision. Do not promise this small demonstration is a production-ready solution.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Let's use the remaining time on the decisions that matter for your environment.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Selective synthesis of workshop slides 12 and 202; unused memory/IQ/optimizer claims removed.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Reuses the original Bank Briefing Azure artwork. Large black text stays on the light side of the composition.


## Slide 15: Thank you / Q&A

TIME: 50:00-60:00

TALK TRACK
Use the hidden appendix only when a question earns it. Technical questions: hosted versus prompt, SDK versus development assistant, identity, network boundaries, model cost, evaluation coverage. Business questions: handling time, resolution quality, escalation quality and total operating cost. ROI needs a customer baseline. No generic claim that all data remains in Sweden: the selected model uses GlobalStandard, and processing geography follows that deployment type and connected services.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Close on the customer's next measurable decision, not a catalogue of features.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Architecture reference deck: outcome-first and ownership framing.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Original Bank Briefing closing-slide visual language and artwork.


## Slide 16: What is implemented—and what is not

TIME: Q&A backup only

TALK TRACK
Use this slide to keep the promise precise. The tool surface is packaged and allowlisted in code. The managed Toolbox and APIM story is an extension, not a hidden prerequisite. Native semantic scoring evaluates captured outputs. The demo is deliberately narrow; the production architecture needs stronger environment isolation, identities and governance based on customer requirements.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Return to the relevant live artifact rather than expanding into another feature tour.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Implementation inspection and workshop scope reduction.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Bank Briefing's two-column editorial treatment; no repetitive rounded cards.


## Slide 17: Availability is capability-specific

TIME: Q&A backup only

TALK TRACK
The GA matrix describes named experiences. Do not turn the platform's GA milestone into a blanket promise. The Copilot SDK and specific package/API versions have their own lifecycle; pin and verify them independently. Avoid live dependencies on optimizer and Insights. The implementation uses native model-judged coherence, whose evaluator requirements should be checked in the selected region.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Tie the answer to the customer's required capability and region.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
https://learn.microsoft.com/azure/foundry/concepts/general-availability
https://learn.microsoft.com/azure/foundry/observability/concepts/trace-agent-concept

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Status-table design follows the Bank Briefing, but uses the current checked status—not its historical September status claims.


## Slide 18: The broader agent platform

TIME: Q&A backup only

TALK TRACK
This is a responsibility map, not a compliance certification. Agent identities need explicit access to downstream services. An Azure management-plane Owner role did not, by itself, supply the data-plane access needed during setup; Foundry User is scoped separately. Trace content can contain sensitive data. This demo uses only synthetic data and a 30-day telemetry retention configuration. GlobalStandard model deployment does not promise Sweden-only processing.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Bring the discussion back to a concrete customer requirement.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
Workshop slide 30 and official Foundry identity/tracing guidance.

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Enlarged original platform graphic from workshop slide 22. Broader capabilities are explicitly labelled as a reference; the ownership discussion remains in the notes.


## Slide 19: When a live step takes too long

TIME: Presenter backup; not part of the 50-minute path

TALK TRACK
If five minutes behind, replace fresh batch runs with completed results and omit preview-only screens. If Azure is unavailable, show captured results with recorded timestamp, version, tool evidence and trace ID. If no live evidence was captured successfully, say the cloud step is unverified and use only the offline domain test as a limited code demonstration. Do not imply it is a substitute for the live Foundry journey.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Return to the four takeaways.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
docs/REHEARSAL.md

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Shortened-path timeline matches the main narrative; readable black text on light backgrounds.


## Slide 20: Sources and useful boundaries

TIME: Backup only

TALK TRACK
The primary deck and its notes supplied the narrative. Finance and public-library screenshots were not reused as Volt evidence. The reference architecture supplied outcome-first and ownership framing. The OTP briefing's NDA roadmap pages were excluded. The unreadable enterprise operating-system deck was not used. All visuals here are editable diagrams, not fabricated portal screenshots.

ON SCREEN / DEMO CUE
Stay on this slide.

TRANSITION OUT
Return to Q&A.

RETURN FROM DEMO
Not applicable.

IF TIME OR TECHNOLOGY FAILS
Keep the main message and move on.

SOURCE / CLAIM BOUNDARY
https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents
https://learn.microsoft.com/azure/foundry/concepts/general-availability
https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets
https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup
https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot
https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md

PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; it is not a production-isolation reference deployment.

VISUAL REBUILD
Visual provenance is recorded in presentation/assets/PROVENANCE.md. Complex original diagrams are high-resolution images; all surrounding text and new diagrams remain editable.
