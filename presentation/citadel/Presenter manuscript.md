# Volt & Co — From useful agent to governed service

## Presenter-only delivery contract

**Rehearsal draft — 11 November 2026.** This is a complete spoken manuscript and stage script, not a claim that the pending integration work has passed. The audience deck is deliberately evergreen. Replace every **REHEARSAL BINDING** with the exact verified URL, command, file, click sequence, run ID and fallback evidence before delivering the live route. No bracketed stage direction is spoken aloud.

The main route is 80 minutes, followed by 10 minutes of Q&A: **22 minutes slides, 52 minutes live or explicitly prepared evidence, 6 minutes transitions**. Evidence inspection counts as demonstration time; the audience must be told whether a job was computed live or completed earlier. Do not start infrastructure, indexing, optimization or Insights jobs during the session.

Read the main script verbatim. Read a branch only when its condition occurs. “Expected observation” is a rehearsal assertion, not an instruction to narrate an outcome that did not happen. Wait for the evidence before reading the corresponding result sentence. A missing result is not a pass.

All people, orders, products, policy documents and recalls are synthetic. DEMO is production-like, not customer production. Tool actions are read-only; neither a refund nor a shipment is executed. Do not display credentials, subscription keys, authorization headers or customer data.

**Browser preparation:** open only the rehearsed, signed-in surfaces for Volt, the hosted agent, Toolbox, Knowledge, APIM, Guardrails, Memory, Evaluations, Optimizer, Traces and GitHub. Put the deck in presenter mode and this manuscript on the presenter display. Turn off notifications. Complete the readiness checklist in the companion document.

**Binding index:** RB01 workspace; RB02 live client and agent; RB03 Toolbox; RB04 IQ and correlation; RB05 APIM; RB06 guardrail enforcement; RB07 memory; RB08 native evaluations; RB09 optimizer; RB10 operational defect and trace; RB11 reviewed regression; RB12 issue/Copilot; RB13 PR/gates; RB14 release; RB15 corrected request and evidence chain. A binding includes a real fallback capture or explicitly says “no capture; concept only.”

**Current readiness update — 18:05, 11 November 2026.** The incident remains the genuine v1 `recommendation` versus `eligible` mismatch. Baseline v1 remains **8 passed, 1 failed, 0 errored of 9**. Corrected candidate **v6 is 9 passed, 0 failed, 0 errored**, same pinned evaluator v1 and unchanged nine cases. Both runs grade captured real responses, not server-side agent reruns. One initial model-service failure was preserved and retried once; **9/9 is not 100% operational availability**.

Issue **#1** and **PR #2, READY FOR REVIEW**, exist at head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`. All existing CI and native business statuses succeeded. The PR is **unmerged**, with **no DEMO release**. Cloud Copilot dispatch failed before starting; the actual fix used local Copilot assistance in an isolated worktree. Candidate v6's native code hash matches packaged ZIP SHA-256 `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996`. Ready-for-review status is not approval or release.

Native harmless-marker guardrail enforcement and the **single-authenticated-caller native Memory lifecycle are verified**. Memory used four separate v5-bound sessions/conversations: remember/read exact native content, new-conversation recall, forget/confirm native deletion, then a fourth conversation with no saved preference. A second genuine authenticated identity is still required for scope/user-binding and cross-user isolation proof.

Session pinning **was correct**: SDK/CLI use `extra_body.agent_session_id`; native `get_session` confirmed v5 and the returned session ID matched. The actual `remember_response_style` tool ran. Preview response `agent_reference` misleadingly reports the endpoint's current v6, where Memory is off. Preserve that discrepancy; do not claim clean version metadata. The live Memory segment must explicitly pin v5; its exact command is forthcoming and must not be guessed.

The remedy was the documented **Foundry User** role for the DEV project's managed identity at Foundry account scope; OpenAI User alone was insufficient. This shared-account DEV/DEMO profile is still not hard production isolation, and Memory/evaluation model traffic is not automatically under the customer APIM token budget. **Never copy private Memory evidence or put native Memory IDs, caller scope or raw session IDs into materials.** No Optimizer run, automatic Insights finding or DEMO release is established.

## Slide 01 — From useful agent to governed service

**Clock 00:00–01:00 · 1 minute slides · Screen: wave cover.**

[Start on the cover. Do not open the terminal.]

“Welcome. Today we are going to follow one customer and one agent all the way from a useful answer to a service we can govern and improve.

“Our customer bought a Volt charger. Their request sounds simple: can I get a replacement? But answering responsibly requires product facts, policy evidence, permitted tools, a clear safety boundary and a way to know whether a change really improved the result.

“Microsoft Foundry is the agent platform in this story. Citadel gives us a governance architecture around it. GitHub Copilot helps us develop and repair the application; it is not the application runtime we are about to inspect.

“We have eighty minutes for the journey and ten for questions. Most of the time will be in the application and the platform, not in slides. Everything customer-facing is synthetic. When we inspect a prepared run, I will say so.

“The organizing picture is two loops.”

[At 01:00, advance to slide 2. If the audience arrives late, do not restart this introduction; recover time from optional inspection depth.]

## Slide 02 — Two loops. One improving service.

**Clock 01:00–04:00 · 3 minutes slides · Screen: the adapted original workshop inner/outer-loop diagram.**

[Point to the left loop, then the right loop. Keep the actual diagram visible throughout.]

“This is the workshop's two-loop picture, adapted to the environments we are using today. The inner loop is where we build and prove the agent. We connect a model, tools and knowledge; run a request; inspect a trace; evaluate behavior; and improve the configuration.

“The outer loop is where we make that learning repeatable. A reviewed candidate passes release checks, reaches the serving environment and is observed in operation. We call that environment DEMO because it is synthetic and production-like, not customer production.

“The important parts are the two bridges. Look at the top bridge. We do not hand over a promising chat transcript and say, ‘ship it.’ We hand over an identifiable candidate and its evidence: code, instructions, tool configuration, knowledge, evaluation results and policy.

“Now look at the bottom bridge. Operational evidence comes back into development. That does not mean every answer the agent produced becomes training data or ground truth. A person reviews what happened and writes the expected behavior before a trace becomes a regression case.

“The center column is the shared contract. Environments can separate identities and permissions while sharing the definition of correct behavior. Our DEV and DEMO projects currently share an account, and the Memory identity's role scope is broader than a project. This profile is not a hard production isolation boundary.

“Here is a useful diagnostic question for your own projects. If someone changes a prompt tomorrow, can you tell which tools and policy were used, which tests passed, and which version is serving? If the answer is no, the missing piece is not necessarily a smarter model. It may be one of these bridges.

“We will travel clockwise. First we make the answer useful, then govern it, examine one narrow memory preference, measure it and inspect optimization. Finally, an observed decision mismatch becomes the evidence for a reviewed regression and a Copilot-assisted repair through the release gate.

“Keep this picture in mind. Each later screen is a close-up of one part of it.”

[Pause for five seconds to let the diagram settle. At 04:00 advance to slide 3. No live demo is needed here. If projection is too small to read the diagram, explain the two bridges rather than attempting to read every label.]

## Slide 03 — One customer. One support journey.

**Clock 04:00–06:00 · 2 minutes slides · Screen: customer case and three-step decision path.**

“Meet our one customer. They have a Volt Charge 65, batch CH-0722, on order VC-10482. They are outside the standard thirty-day return window. They ask whether they can get a replacement and which policy applies.

“The temptation is to jump straight to a confident answer. We are going to resist that. A standard return window, a recall and a warranty or replacement assessment are different things. The model should not collapse them into one yes-or-no refund decision.

“First, business tools establish facts. What product and batch are involved? What does the synthetic recall record say? What is the order status, and what does the eligibility service return?

“Second, Foundry IQ supplies policy evidence. We want an identifiable policy source that we can open, not a plausible paragraph that the model invented.

“Third, the agent explains the responsible next step. For this journey, that means human assessment rather than an automatic refund. We are not moving money, sending replacement stock or changing an order on stage.

“The wider fictional store has catalog and compatibility capabilities as well, but we are not going on five separate tours. The replacement question is our thread through every platform feature.

“Later we will see why getting the facts and the prose right is still not enough. The structured workflow decision must agree with the tool's eligibility result. That will be our operational learning moment.

“Before we run the request, we need to choose who owns the agent's runtime.”

[At 06:00 advance to slide 4. If asked whether these are real customers, answer: “No. The product, order, recall and documents are synthetic fixtures, chosen so the expected behavior can be checked.”]

## Slide 04 — Choose the operating model

**Clock 06:00–08:00 · 2 minutes slides · Screen: prompt-versus-hosted comparison.**

“There are two operating models worth separating. A prompt agent gives you the managed configuration path. You define instructions and capabilities without maintaining custom orchestration code. That is a good starting point when it meets the application's needs.

“A hosted agent gives you control of the application's runtime logic, while Foundry still supplies managed hosting. That is the choice for this demonstration because we want a deterministic decision adapter and the integration path we are inspecting.

“Our runtime is Python Microsoft Agent Framework, exposing the Responses protocol. Protocol choice matters here because the hosted optimization path we intend to demonstrate requires Responses. The older Copilot SDK Invocations implementation is a separate fallback. It must not be presented as an optimizer-compatible substitute.

“Tools, source control and CI are not, on their own, reasons to choose hosted. The real question is whether you need the custom runtime behavior and are prepared to own that code and its dependencies.

“GitHub Copilot will appear later as our development assistant. It can help write a regression and repair the adapter. That does not make it the serving harness.

“There are also other managed-harness experiences in preview. They are useful context, but they are not another implementation track today. We will not turn this into a survey of every agent option.

“Notice the cost row. Hosting adds active compute to model and tool usage. We have not measured a total cost advantage for this application, so I am not going to promise one. The choice should follow control, compatibility and operating requirements.

“Let us make that ownership split concrete.”

[At 08:00 advance to slide 5. Keep questions about alternate SDKs for Q&A unless they block understanding of the chosen runtime.]

## Slide 05 — Our code. Foundry's runtime.

**Clock 08:00–10:00 · 2 minutes slides · Screen: responsibility split.**

“Hosted is the control path, not the unmanaged path. On the left are our responsibilities: the agent logic, orchestration, framework dependencies, request handling and configuration. If our application's final decision contradicts its authoritative tool evidence, we have to investigate and repair that decision path. Managed hosting cannot repair the business meaning for us.

“On the right is the platform: managed deployment and endpoints, scaling and agent identity, and the lifecycle surfaces for tracing, evaluation and operation.

“The deployed agent can be tested and inspected in Foundry, but we do not edit the hosted Python implementation in the prompt-agent editor. We change code in source control and deploy a candidate.

“Responses is the contract at the hosted boundary. The runtime can reach capabilities through the project and Toolbox, and our application must still supply the correct configuration and authorization context.

“Here is the distinction to remember when Copilot appears. Copilot is helping the developer work on code. Agent Framework is running the customer request. If we confuse those two roles, we will misunderstand both the lifecycle and the evidence.

“Similarly, a managed identity does not mean every downstream hop is keyless. We will call out the actual access contracts at the gateway rather than generalize from one identity badge.

“Now we can put the agent into the broader Citadel picture.”

[At 10:00 advance to slide 6.]

## Slide 06 — Where Citadel and Foundry meet

**Clock 10:00–13:00 · 2 minutes slides + 1 minute transition · Screen: original Citadel architecture, then prepared workspace.**

“This is the supplied Citadel architecture. We have kept the original layered picture because the relationships matter more than a list of products.

“Layer two is agent operations: build, host, evaluate and improve. That is where our Volt agent, its tools, context and evaluations live.

“Layer one is the Governance Hub. In our selected routes, API Management sits between the agent-facing connection and the approved model or business tools. It gives us an explicit place to apply access and consumption controls.

“The diagram also shows broader management and security integrations. Those are architecture context. Deploying a gateway does not automatically enable Defender, Agent 365, Purview or every other layer. We only claim a control after inspecting its actual configuration and behavior.

“There are also service paths not shown as a single universal gateway hop. We must not assume that IQ internals, memory processing, evaluation models or optimizer-service traffic all traverse our model gateway and inherit its quotas.

“Our account has separate DEV and DEMO projects, but those are not hard production isolation in this profile. The effective account-managed-identity role scope used for Memory is broader than project scope. Memory and evaluation model traffic are not automatically under the customer's APIM token budget.

“The selected resource group is in Sweden Central, but resource location is not a Sweden-only processing guarantee. The deployed model uses a data-zone SKU. We need to discuss processing geography and retention separately from the map pin.

“The Foundry endpoint is public and Entra-authenticated in the approved configuration. Key Vault and backend storage remain private. This is not an all-private-network demonstration.

“With those boundaries clear, let us leave the diagram and inspect the prepared application.”

[At 12:00 switch from slides to the signed-in workspace. **REHEARSAL BINDING RB01:** exact workspace, file names and click sequence showing instructions, deterministic business contract and pinned tool configuration. Show at most three views; never improvise a repository tour. No terminal command is authorized by this script.]

“I am showing a prepared workspace, not generating a complete application in front of you. These are the instructions, the business contract and the capability bindings. The purpose is to establish what is versioned before we inspect runtime behavior.”

[Expected observation: Agent Framework and Responses are identifiable in the deployed implementation, not just in a plan. At 12:45 return to slides and advance to slide 7. At 13:00 start its chapter.]

**If workspace access is slow:** “The code view is not the proof of the customer outcome. I will move to the rehearsed agent view, and we will return to code when there is a specific defect to fix.”

**If the replacement runtime is not ready:** “The intended runtime path is not available in this environment. I can explain the architecture, but I will not substitute the older Invocations agent and imply that it proves the same integration.” Follow the concept-only route or the explicitly labelled compatible recorded run in RB02.

## Slide 07 — Give the agent governed capabilities

**Clock 13:00–21:00 · 30 seconds slides + 7 minutes demonstration + 30 seconds transitions.**

[Keep slide 7 visible until 13:30.]

“The Toolbox is how we package the capabilities the agent may use. For this request, the useful business operations are recall, order status and return or warranty eligibility. These are read-only operations, not a license to mutate an order. We pin the curated capability set to the agent version. The diagram is conceptual; the actual evidence is in the next screens.”

[13:30–13:45: open the recorded agent portal or the prepared CLI. **REHEARSAL BINDING RB02 — hosted execution verified by the implementation owner:** `volt-support` version 1, Responses 2.0.0, Toolbox 2. Rehearse sign-in and the presentation navigation; do not assume an unverified custom client UI. The 30-second switch threshold remains a presenter pacing rule, not a latency promise.]

[Verified portal URL: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/build?version=1]

[Verified CLI command, from `showcase\volt-support`: `azd ai agent invoke volt-support --new-conversation --version 1 "For the synthetic Volt demo: my order is VC-10482 and my Volt Charge 65 batch is CH-0722. It is past the normal 30-day return window. Can I still be assessed for a replacement? Check my order, recall status and replacement eligibility, and cite the policy. Do not actually change my order."` The presentation author recorded but did not execute this command.]

[Version-metadata caution: this is the historical v1 invocation. The Memory investigation confirmed correct v5 session pinning through `extra_body.agent_session_id`: native `get_session` and matching returned session identity confirmed v5. The preview response's `agent_reference` nevertheless reported endpoint-current v6. Use authoritative session evidence and preserve the metadata warning; do not describe this as proven routing to the wrong version.]

[Observed evidence: response `caresp_02ddb9a77175f58700lAjFhWXx30P0Frxo1oLxhgKwmjshXgd7`; trace `8be3ccdd0e7b0bdcac285dcbbcdf4ef4`. All four tools executed. Client elapsed was 25.372 seconds for this one observation—not an SLA, percentile or benchmark. Retain the implementation owner's actual output; no capture file path is invented here.]

“Here is the synthetic customer request I am sending: ‘For the synthetic Volt demo: my order is VC-10482 and my Volt Charge 65 batch is CH-0722. It is past the normal thirty-day return window. Can I still be assessed for a replacement? Check my order, recall status and replacement eligibility, and cite the policy. Do not actually change my order.’

“While it runs, notice what I am not asking the model to invent. We have a concrete product, batch and order. The business tools should supply their facts, and the policy source should explain the next step.”

[13:45–16:15: submit once. Read the actual response. Open the structured result only after it exists. Do not resubmit repeatedly. Expected observation: the result reflects actual recall/order/eligibility tool evidence, cites policy where required and proposes human assessment rather than asserting that a refund or replacement shipment has happened.]

[For the recorded version-1 response, do not call the workflow correct. Its prose/citations are right but `decision=recommendation` conflicts with tool result `eligible`. Say: “Successful execution and convincing prose are not the same as a passing business contract.” This remains the v1 failure. The later v6 candidate passes the contract and PR #2 is ready for review, with existing CI/native status success; it is unmerged and not released to DEMO.]

“Let us separate the wording from the evidence. The response is the customer-facing explanation. The tool records are where we check the facts. I want to see which operation ran, what arguments it received and what it actually returned. A nicely worded answer alone would not prove that the correct tool was used.

“For the recall operation, compare the product and batch with our request. For the order operation, compare the order identifier. For eligibility, distinguish the standard return window from the separate assessment path. We are not concluding that a request is authorized merely because the user typed an order number.”

[16:15–18:30: switch to Foundry Toolbox. **REHEARSAL BINDING RB03:** Toolbox v2 is verified through the native APIM business MCP path, with exactly three business operations plus one IQ tool. The backend has five read-only operations; the curated business subset is recall, order status and eligibility. The hosted response and trace recorded above now provide actual execution evidence for all four tools, beyond the earlier six-case direct-tool preflight. Rehearse the portal navigation. Do not turn preflight into a feature-catalogue segment or equate four executed tools with workflow correctness.]

“Now we can inspect the configuration behind that answer. This is the specific Toolbox version used by the agent, not an unrelated current version. We can see the business-tool connection and the curated operations.

“The backend can support more operations than we choose to expose in this journey. That distinction is important. A Toolbox is a reusable contract, not a requirement to give every agent every tool.

“The APIM MCP endpoint translates selected business API operations into discoverable tool calls. The connection's per-use-case access contract is part of the route. We do not display its credential here.”

[18:30–20:45: return to the request evidence and follow one business-tool invocation. Expected observation: arguments and results correlate with the same request and version. If the UI does not expose a field, use only the verified redacted trace view in RB03.]

“This is the connection between configuration and execution. A tool being listed is configuration evidence. A correlated invocation is execution evidence. We want both.

“The model supplies reasoning. Our business systems supply facts. The Toolbox makes the permitted capabilities reusable. But we still need the policy that explains why those facts lead to a particular next step.”

[20:45–21:00: return to slides; advance to slide 8.]

**If loading exceeds 30 seconds:** “This request is taking longer than the rehearsed threshold. Rather than create duplicate traffic, I will inspect the captured run of the same version. This is a prepared result, not a live response.” Open only RB02's verified capture with its timestamp/version.

**If a tool fails or the result is wrong:** “We have a failed or incomplete execution, not a successful answer. We can still inspect the boundary that failed. I will not fill in the missing result from the scenario.” Show the real error, then the labelled fallback if one exists.

**If no end-to-end capture exists:** “The integration has not produced this proof yet. The architecture explains the intended path; it does not demonstrate that the path worked.” Continue conceptually without claiming customer success.

## Slide 08 — Ground the answer in policy

**Clock 21:00–27:00 · 30 seconds slides + 5 minutes demonstration + 30 seconds transitions.**

“This is the source workshop's source-to-knowledge-to-agent pattern, narrowed to what we are actually using. Our knowledge base is backed by Azure AI Search and text plus semantic extractive retrieval. I am not describing a vector or hybrid implementation that we have not built.

“The policy source complements the business tools. A recall lookup supplies a fact; a policy citation makes the explanation inspectable.”

[21:30–21:45: switch to Knowledge. **REHEARSAL BINDING RB04:** exact navigation to `volt-support-knowledge`, verified source list, retrieval response, citation link and request correlation. Expected source references include `VOLT-REPLACEMENT-2026-11` and `SYNTHETIC-RECALL-001`. Use the actual returned IDs/links, not an invented browser URL.]

“Here is the knowledge base and here are the synthetic documents behind it. I want to open the replacement policy and the recall notice, not just point at a search service being present.

“Now compare the source reference returned by retrieval with the citation in the customer response. The important property is traceability. We can ask whether the passage actually supports the statement, whether the source is the intended one and whether the business result was interpreted correctly.

“A citation is not a magic truth stamp. It can be irrelevant, stale or misread. The human reviewer and the evaluator still need to compare the claim with its evidence.”

[22:30–24:30: open the returned policy passage; compare it with the original request's decision. Do not read the entire document. Point to the standard-window language and the assessment path only if they are present in the retrieved text.]

“For this case, do not confuse ‘outside the standard return window’ with ‘there can be no further assessment.’ We are looking for the policy-supported next step, not a model-created exception and not an automatic refund.

“Notice also the division of responsibility. Search retrieval does not authenticate ownership of order VC-10482. That needs a separate customer authorization design before a real deployment. Our synthetic environment does not implement that real-world ownership check.”

[24:30–26:45: inspect one correlated request trace connecting retrieval and business facts. Use the actual capture if it completed before the session and say so.]

“This trace brings the pieces together. We can see the request, the selected capability and the retrieved evidence in the same execution story. Where telemetry does not include a field, we should say that it is absent rather than infer it.

“Adding retrieval and tools adds work, and often latency, to a simple model call. We have not established a universal latency or cost number. The engineering question is whether the evidence is worth that cost for this decision, and whether we can measure the actual path.

“We now have a useful answer. The next question is whether the agent can reach only the capabilities it is supposed to reach.”

[26:45–27:00: return to slides; advance to slide 9.]

**If Knowledge or citation navigation is slow:** “The portal view is loading. I will use the saved retrieval response from this exact run and identify its source reference. This is prepared evidence, not a new retrieval.” Show the approved capture.

**If the cited document is absent or does not support the answer:** “The citation does not support the claim we need. That is a grounding failure, even if the answer sounds plausible.” Do not silently substitute another document or a generic source screenshot.

## Slide 09 — One gateway. Explicit access contracts.

**Clock 27:00–32:00 · 1 minute slides + 4 minutes demonstration.**

“The Governance Hub gives us a place to apply the access contract for routed traffic. There are two important routes here: the connected-model route and Toolbox access to the MCP business tools.

“For the model path, the configured route is `volt-models-LLM` to the approved `gpt-5.4-mini` deployment through APIM. The gateway also has a model allowlist and token controls. Twenty thousand tokens per minute and five hundred thousand daily tokens are token quotas, not a dollar cap.

“For the business route, the Toolbox connection uses a managed per-use-case subscription credential. APIM reaches the Function through a function-scoped key held in Key Vault. Backend storage uses managed identity. So no, not every hop is keyless.

“An APIM consumer contract is also not real customer order-ownership authorization. That is a different control.”

[28:00: switch to the APIM and request-evidence views. **REHEARSAL BINDING RB05:** redacted product/subscription contract, model-policy location, permitted request, restricted-consumer request, expected status and gateway correlation. Bind actual commands or controls; do not type guessed HTTP calls or reveal keys.]

“First, let us inspect an allowed request. The useful path should still succeed. Governance that blocks everything is not a useful product.

“Now we will use the separately prepared restricted demonstration consumer for an operation it has not been granted. We expect an authorization rejection at the named APIM control, not a polite refusal generated by the model.”

[28:30–30:15: run or open the permitted and denied evidence. Expected observation: the allowed operation succeeds; the restricted operation is rejected with a real gateway status/control record. Only say “APIM rejected it” after that record is visible.]

“The evidence tells us where the decision happened. We can connect the response to the access contract and the boundary that enforced it. If we only saw the agent say ‘I cannot do that,’ we would not know whether authorization had been enforced at all.

“The model route and business-tool route also have different contracts. Do not assume one subscription, one policy or one budget magically covers every service-internal call.”

[30:15–31:45: inspect the redacted policy and route identity. If the latest gateway probe is shown, identify `VOLT_GATEWAY_OK` as a gateway-route probe, not proof of the entire customer workflow.]

“A successful model gateway probe establishes that route. It does not establish that the agent used the route in every call, that the tool contract works, or that every internal platform operation shares the quota.

“API Management Developer SKU is also a demonstration choice, not a production availability design. Its baseline cost and the costs of Search, hosting and model usage need separate consideration.”

[At 31:45 return to the deck; at 32:00 show slide 10. The switch is included in this evidence-inspection block.]

**If the denial does not occur:** “The restricted call was not rejected as expected. That is a failed access-control demonstration. We will not describe it as protected until the actual contract and enforcement are corrected.” Use the verified capture only if it exists and is explicitly labelled.

**If the policy pane will expose a secret:** “We will use the redacted evidence view. Credential material is not needed to understand or prove this control.”

## Slide 10 — Enforce the right boundary

**Clock 32:00–39:00 · 1 minute slides + 5 minutes demonstration + 1 minute transitions.**

“Keep three questions separate. Authorization asks whether this consumer may use the capability. Content guardrails inspect supported content boundaries. Business rules decide what the facts and policy permit.

“This diagram is a reasoning aid, not a claim that every possible intervention point is active in our deployment. We will prove the particular agent boundary we configured and retain the evidence of that block.

“The demonstration fixture is deliberately harmless: a unique blocklist marker. It is designed to make the enforcement path observable. It is not a jailbreak-resistance benchmark and it does not demonstrate universal safety.”

[33:00–33:30: switch to Guardrails and the recorded proof. **REHEARSAL BINDING RB06 — verified:** the harmless `VOLT_DEMO_BLOCK_MARKER_261111` probe returned HTTP **400**, error code **content_filter**, type `content_safety_error`, at the **input** stage. The local proof is `.\.runtime\volt-guardrail-proof.json` from the demo repository root; request ID `088298eff265d56cd2438f8dbd2dcbb2`; `native_filter_observed` is true. This is platform enforcement, not a model's refusal text.]

[Rehearsal invocation matching `probe_guardrail.py`'s actual arguments, from the demo repository root: `.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\probe_guardrail.py --project-endpoint https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev --agent volt-support --out .\.runtime\volt-guardrail-proof.json`. The presentation author did not run it. The probe targets the named agent without a version argument: record the resolved serving version when rerunning; do not assume a new memory-enabled deployment inherits this proof.]

“Here is the policy attachment on the version we are testing. Now I will send the harmless marker through the supported boundary. We expect a platform enforcement result that we can distinguish from the model choosing to refuse.”

[33:30–35:00: inspect the prepared proof, explicitly identifying it as captured before the session, or run the rehearsed probe once. Open `http_status=400` and `error.code=content_filter`. Inspect the input-stage message and request ID, rather than displaying only a short refusal sentence.]

“This is the specific evidence we need: the supported boundary acted on the configured fixture. The block is attributable to a control, rather than inferred from the final prose.

“Now let us send the legitimate Volt request again. Safety cannot mean that all useful traffic is stopped. We want allowed utility and the specific block in the same evidence set.”

[35:00–36:30: execute the allowed control; compare actual outcomes. If tool-input or tool-output moderation is not verified, do not demonstrate or claim it.]

“There is a limit to what this test proves. It demonstrates this configured block at this boundary. It does not prove that every harmful request is detected, that every tool is covered, or that the application cannot violate a business rule.

“That is why the business contract remains separate. An allowed, well-grounded request can still end with the wrong structured workflow decision. The guardrail cannot make `recommendation` agree with an eligibility result of `eligible`. Content enforcement is not a replacement for business correctness checks.”

[36:30–38:30: inspect the correlated evidence, then reset the client to the normal synthetic request. Avoid opening a broad safety catalog.]

“The practical takeaway is to name the boundary in your test. ‘The agent was safe’ is too vague. ‘This configured control rejected this fixture while the permitted request still succeeded’ is narrower, inspectable and useful.

“We have controlled what the agent may do. Now we need to control what it carries from one conversation to the next.”

[38:30–39:00: return to the deck and advance to slide 11.]

**If the marker is not blocked:** “The policy exists, but this request did not demonstrate enforcement at the agent boundary. We have found a gap between configuration and runtime behavior.” Stop the safety claim; do not force the model to refuse with additional prompt instructions.

**If the event takes too long:** “I will switch to the verified capture of the same policy and version. This is a prepared enforcement result.” If none exists, say: “We can explain the boundary design, but we do not yet have runtime proof.”

## Slide 11 — Remember preferences, not authority

**Clock 39:00–45:00 · 1 minute slides + 4 minutes demonstration + 1 minute transitions.**

“Memory is useful when it preserves appropriate continuity. Our deliberately narrow preference is: concise answers, with the next step first.

“The store is `volt-preferences`, with a seven-day TTL and user profile enabled. Chat summaries and procedural memory are off. We are not storing order facts, identity details, recall status, policy or permissions.

“We have verified the lifecycle for one authenticated caller, using an explicit scope. The intended binding is to the caller, but we still need a second genuine authenticated identity to prove cross-user separation. Four conversations for one caller are not four identities.”

[40:00–40:30: **RB07 single-caller lifecycle PASSED.** Use an approved redacted summary of the verified four-session run, or the live sequence only after its exact command is supplied and rehearsed. Private evidence locator: `.runtime\memory-proof-v5-pinned\summary.json`, plus four step records. Do not copy or project those raw files. Native Memory item IDs, caller scope and raw session IDs must remain redacted in every displayed/exported artifact. The current endpoint is v6 with Memory disabled; this segment must explicitly pin v5. The exact live command is forthcoming—do not guess one.]

“For this chapter, the verified Memory run uses a v5-bound session. The current endpoint's v6 has Memory off. I will distinguish this pinned Memory proof from the v6 business-evaluation candidate.”

“The four-session run completed before this session. I will describe its verified observations, using only redacted material, rather than imply that an unbound live command has just run. In the first session, the authenticated caller saved the synthetic response-style preference and its exact native content was read back.”

[40:30–41:15: session/conversation 1 — the native remember operation creates the item, and its exact stored content is read back. The actual `remember_response_style` tool executed. Display only the approved synthetic preference text and the verified result; redact native item identity and caller scope. Do not invent the stored string or show raw private JSON.]

“We checked the actual native stored content, not just whether the assistant promised to remember it. The item is deliberately narrow; product facts and policy still come from authoritative systems.”

[41:15–42:00: session/conversation 2 — a separate new session and conversation for the same authenticated caller recalls the saved preference. The retrieval was verified. Show a redacted result, not the scope or native identifiers; answer style alone is not the proof.]

“This is a new conversation with the same authenticated caller. The retrieval evidence demonstrates continuity. Concise wording by itself would not.”

[42:00–43:00: session/conversation 3 — forget the actual native item and confirm native deletion. The operator uses its native identity privately; the presentation must not display or copy the ID. Retain the distinction between an acknowledgment and verified deletion.]

“Now the native item is forgotten and deletion is confirmed. This is stronger evidence than a response that merely says ‘I forgot.’ TTL is a retention backstop, not a substitute for explicit deletion.”

[43:00–44:00: session/conversation 4 — a fourth separate session/conversation reports no saved preference. This completes the verified single-caller content/persistence/deletion lifecycle. It is not a test of another user's isolation.]

“A fourth new conversation now reports no saved preference. We have verified content, continuity and deletion for one authenticated caller. We have not proved cross-user isolation; that needs a second genuine identity and a verified scope-to-user binding.

[44:00–44:30: explain the version warning without revealing session identifiers. SDK/CLI use `extra_body.agent_session_id`; native `get_session` confirmed v5 and the returned session identity matched. The actual `remember_response_style` tool ran. Keep the conflicting preview `agent_reference` warning visible; no raw identifier values belong in this material.]

“The version metadata needs care. Native session lookup confirmed v5, the returned session identity matched, and the Memory tool actually ran. SDK and CLI passed the session binding correctly. The preview response's agent reference still showed the current endpoint v6. That field is misleading here; we preserve both observations and warn rather than call the metadata clean.

“The required permission was Foundry User for the DEV project's managed identity at account scope. OpenAI User alone was not enough. That account-level scope is not a hard DEV/DEMO production boundary.

“This capability is persisted context, not model training or an authorization system. A remembered preference must never override the recall record, the policy or the consumer's permissions. Its model traffic, and evaluation model traffic, are not automatically under our customer APIM token budget.

“That felt more helpful. The next question is how to measure whether the agent actually is better.”

[44:30–45:00: return to the deck; advance to slide 12.]

**If the exact live command is still missing:** “The single-caller run is verified, but the live v5-pinned command has not yet been bound for this presentation. I will use a redacted verification summary, not an unpinned invocation against the current v6 endpoint.”

**If a new live attempt fails:** “This new attempt did not reproduce the verified lifecycle. We will preserve its failure and distinguish it from the prepared four-session proof.” Do not infer persistence from short wording.

**If asked about caller B:** “We have proved the lifecycle for one authenticated caller, not cross-user isolation. The second genuine identity and scope/user binding test remain pending.” Never replace that test with a manually typed user ID or another conversation.

**If deletion is delayed or fails:** “The forget request has not yet produced a verified absence. I will not claim deletion until the read-back confirms it.” Record the unresolved check and move on at 44:30.

## Slide 12 — Evidence before confidence

**Clock 45:00–51:00 · 1 minute slides + 4 minutes 30 seconds demonstration + 30 seconds transitions.**

[RB08 — completed native baseline: business_contract v1 scored **8 passed, 1 failed, 0 errored of 9**. Failed item **1**, `replacement-recall`, is the observed `recommendation` versus `eligible` mismatch. Evaluation ID `eval_5a3774acf4f347e1bd35ae30375d0f2d`; run ID `evalrun_28da2cdf28224eb799a9a2e3d9f8672e`. This is a native evaluation of captured real hosted responses and observed successful tool calls, not coherence and not a server-side rerun of the agent.]

“A coherent answer can still make the wrong business decision. That is why we separate judged quality from the business contract.

“For Volt, the contract checks the structured decision and the observed tool evidence, with a policy citation when the case requires one. The report's evaluator is business_contract version one.

“We now have a completed native baseline: eight cases passed, one failed and none errored. These are captured real hosted responses, including the successful tool calls we observed. Foundry is grading that evidence; it is not invoking the agent again behind the scenes.

“This is the new hosted eight-of-nine baseline, not the older local seven-of-nine result. We will compare it with the actual v6 candidate, which now passes all nine business cases. First, let us inspect the original failure.”

[46:00–46:15: open the actual native report: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_28da2cdf28224eb799a9a2e3d9f8672e . Verify Completed status and the business_contract v1 totals. Open failed item 1, `replacement-recall`. The saved baseline replay is `showcase\recordings\baseline-v1.json`, commit `78b54e4`; it is captured evidence, not a new invocation.]

“This is the completed run and this is the failed replacement-recall item. We can inspect it in the native report.

“The eligibility tool returned eligible. The model's structured decision says recommendation. The customer-facing text and citations are right, but the workflow contract is not. That is why this item failed even though all four tools executed successfully.”

[46:15–48:15: inspect failed item 1 and its captured tool/decision evidence, then one passing recall case from the same report. Read actual case labels and verdicts; do not substitute a coherence metric. Show that the replay source is the captured hosted baseline. Do not claim that opening the report reran the agent.]

“An aggregate can hide an important failure. Eight passing cases do not cancel this workflow mismatch. We need a clear release consequence for a protected business-contract failure.

“A coherence judge might like the prose. That would be a different measure, not a way to turn this failed business decision into a pass.”

[48:15–50:45: open the completed candidate v6 report: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_d6967759ba834c51b26a39296474ff0f . Confirm **9 passed, 0 failed, 0 errored**, each of the nine rows passed, same pinned evaluator v1 and unchanged nine-case dataset. This grades the captured real v6 responses. No separate holdout or server-side rerun is implied.]

“Now the actual comparison: v1 passed eight of nine; candidate v6 passes all nine completed-response business cases, using the same evaluator version and unchanged nine-case dataset. We are grading real v6 captures, not re-scoring the old baseline and not asking Foundry to rerun the agent server-side.

“There is an important reliability qualification. One initial model-service invocation failed. That failure was preserved, and the request was retried once. The nine completed responses then passed business grading. Nine of nine is not a claim of one hundred percent operational availability, and zero evaluation errors does not erase the invocation failure.

“The candidate's native code hash matches the packaged ZIP. We will connect that artifact identity to the PR shortly. Passing this business comparison is evidence for review, not permission to merge or promote.

“Memory can contaminate a test if a prior conversation leaks into the next case, so evaluation needs isolated or reset state.

“A reviewed dataset is still a sample. Passing it is evidence, not a proof of every future request. Generated cases can help, but domain review supplies the expected behavior.

“Now we can use this contract to judge optimization instead of treating a higher score as an automatic release.”

[50:45–51:00: return to the deck; advance to slide 13.]

**If a new run is queued:** “The new run has not completed. I will inspect our completed hosted baseline and identify it. I will not replace the new result with local CI numbers or imply that the baseline is the corrected candidate.”

**If the native report cannot load:** “The report is unavailable in this view. I will open the saved real baseline capture and keep its identity visible. The completed native result is eight passed, one failed and zero errored, but this local replay is not a new evaluation or agent execution.” Use `baseline-v1.json`; do not manufacture a portal screenshot.

**If business and quality verdicts disagree:** “That disagreement is useful. A fluent response can fail the business contract. Our release rule must respect the business constraint rather than average it away.”

## Slide 13 — Optimize configuration. Review the change.

**Clock 51:00–57:00 · 1 minute slides + 4 minutes 30 seconds demonstration + 30 seconds transitions.**

[CURRENT STATUS — no Optimizer run exists yet. The workflow below remains conceptual until RB09 is bound. Say: “We have not run Agent Optimizer in this environment. I will explain its review workflow, then use our actual code-fixed candidate comparison to illustrate what evidence a candidate needs. That candidate was locally Copilot-assisted, not optimizer-generated.” Do not read the completed-job sentences or display a manual change as an optimizer result. The later live-job sequence is reserved for a future verified run.]

“Agent Optimizer searches for configuration candidates against an objective. In this journey, useful objectives include clear next steps, appropriate clarification and policy evidence. The optimizer is not a substitute for fixing broken business code.

“There are three decisions after a candidate looks promising: evaluate it, review and apply the configuration change, and release it through the gate. Those are separate decisions.

“The best score starts review. It does not authorize deployment. A candidate may improve a tuning score while harming a holdout case, cost, latency or another quality measure. Keeping the baseline is a valid outcome.”

[52:00–52:15: switch to a completed native optimizer job. **REHEARSAL BINDING RB09:** verified access, Responses agent version, completed job ID, objective, tuning dataset, candidate configuration diff, baseline comparison, held-out evaluation and measured resource/latency evidence if available. Do not launch an optimizer job on stage.]

“This job completed before the session. We are inspecting its actual result, not waiting for a search to finish live.

“First, identify the objective and the candidates. Then identify the exact change the service proposed. We should be able to read a configuration diff rather than just admire a score.”

[52:15–54:15: open the proposed instructions/configuration change; read the actual diff. Do not narrate an improvement that is absent.]

“The useful review question is: why might this change help our customer, and what might it break? If it makes the next step clearer, does it still ask for a missing batch? If it changes tool behavior, does it still retrieve the authoritative evidence?

“Now we move away from the tuning set. These are the held-out cases. The candidate must satisfy the protected business contract, not merely the objective used during search.”

[54:15–56:45: inspect holdout outcomes, source-control representation and any measured trade-off. Name the actual candidate verdict.]

“Optimization also consumes resources. It may call the model and tools many times. That is why our tools are read-only or sandboxed, the environment is DEV, and memory is isolated. The service's internal traffic is not automatically covered by our selected gateway quota.

“If this candidate is not acceptable, we retain the baseline. If it is acceptable, we record the source change and still pass the release checks. We have not shown that optimization repairs a deterministic adapter bug or guarantees lower cost.

“Evaluation tests the questions we knew to ask. Operation exposes the questions we missed.”

[56:45–57:00: return to the deck; advance to slide 14.]

**If no native optimizer job completed:** “Optimizer access or execution has not produced a completed job in this environment. I can explain the review process, but I will not label a manually edited prompt as an optimizer result.” Show the conceptual flow only, then use the saved time for real evaluation evidence.

**If the job failed or produced no acceptable candidate:** “The outcome is to keep the baseline. That is the control working: a search result is not a release obligation.”

**If the portal is slow:** “I will use the captured result for this job ID. It was computed before the session and remains prepared evidence.”

## Slide 14 — Operation teaches DEV what to test

**Clock 57:00–63:00 · 5 minutes demonstration + 1 minute transitions.**

[SELECTED INCIDENT — historical v1 mismatch: correct prose/citations, model `decision=recommendation`, eligibility tool `eligible`. Response `caresp_02ddb9a77175f58700lAjFhWXx30P0Frxo1oLxhgKwmjshXgd7`; trace `8be3ccdd0e7b0bdcac285dcbbcdf4ef4`; failed native item 1 `replacement-recall`; baseline replay `showcase\recordings\baseline-v1.json`, commit `78b54e4`. Issue #1 and ready-for-review PR #2 exist; v6 captured responses pass all nine business cases and all existing CI/native statuses succeeded. No merge or DEMO release occurred. Preserve the baseline failure; do not call it current v6 behavior or an automatic Insights finding.]

[57:00–57:30: show the trace-flywheel slide during the transition; do not give another feature lecture.]

“Now the return bridge. This is the real mismatch we just saw in the native report. The tools ran, the prose and citations are right, but the structured decision disagrees with the eligibility evidence. We did not plant a safety defect to make this chapter interesting.”

[Switch to the recorded response/trace and baseline replay. **RB10 is bound to the real incident above.** Open the same `replacement-recall` request and `baseline-v1.json`, not an unrelated current conversation. Rehearse the trace-view navigation using the actual trace ID. No automatic Insights finding has been verified: use trace evidence and call it trace evidence.]

“This is the request and this is the version that handled it. We will start with the recorded tool result and structured decision, not an AI-written incident summary.

“There is no verified automatic Insights finding for this incident. The trace and the failed native evaluation item are our evidence. A hand-authored issue is not an automatic Insight.”

[57:30–59:00: inspect the captured request, order/recall/eligibility/IQ tool executions, the actual `eligible` tool result and the model's `recommendation` decision. Keep the v1 response/trace identity visible. Use only fields present in the recorded output.]

“The customer did provide the order and batch. The eligibility tool returned eligible, meaning eligible for human assessment in this synthetic flow, not an instruction to issue a refund.

“The model emitted recommendation in the structured decision. A downstream workflow reading that field does not get the same outcome as the correct natural-language explanation. That is the contract mismatch we need to repair.”

[59:00–60:15: replay the captured real baseline and correlate it with failed item 1 in the native report. State that this is a saved execution, not a new server-side agent run. An optional live repeat uses the exact slide-7 request, but cannot replace the original evidence if the model produces a different decision.]

“This replay preserves the failure even if another live answer varies. It is not a fabricated result. It is the actual hosted output the native evaluator scored.

“We know what disagreed. We should not invent the root cause from the transcript alone. The code review must find how the final decision is derived and how the authoritative tool result should constrain it.”

[60:15–62:30: inspect the baseline failed-case expectation and its link to issue #1 / ready-for-review PR #2. **RB11:** retain `replacement-recall`, observed tool evidence, expected `eligible` and baseline `recommendation`. Inspect the actual regression rather than inventing a file path or declaring approval complete. Passing statuses and readiness for review are not merge or release.]

“A trace is evidence, not a label. The native case identifies the mismatch; a person still reviews the regression and its business expectation. For this request, the structured decision must preserve the eligible assessment outcome supported by the tool.

“We must not solve it by hard-coding every response to eligible. Preserve the other eight baseline cases, including missing and unknown information, and preserve the no-mutation boundary.

“The regression needs the input, the expected decision and the provenance of the observed tool results. That is more useful than a screenshot of prose that already looks correct.

“This gives the development assistant a scoped problem: repair the mismatch, preserve surrounding behavior and show the evidence. The local Copilot-assisted PR is ready for review, with existing CI and native business status success. Next we inspect that evidence. It is still unmerged, and DEMO release has not happened.”

[62:30–63:00: return to the deck; advance to slide 15.]

**If Insights has no real finding:** “There is no generated Insights finding for this case. We will use the actual trace and observed decision directly.” Do not call the manual analysis an Insight.

**If a live repeat does not reproduce:** “This new answer differs from the captured failure. That is not proof of a repair. We will use the identified v1 replay and the completed native report to inspect the actual incident.” Never edit a new answer to recreate the failure.

**If the trace view is delayed:** “The trace view has not loaded within our cutoff. We can still inspect the real v1 protocol capture and its native evaluation item. We are replaying evidence, not claiming a new trace or an automatic Insight.”

## Slide 15 — A PR carries code and behavioral evidence

**Clock 63:00–76:00 · 1 minute slides + 12 minutes demonstration.**

[VERIFIED CANDIDATE / RELEASE HOLD — issue https://github.com/SridharArrabelly/foundry-showcase/issues/1 ; READY-FOR-REVIEW PR https://github.com/SridharArrabelly/foundry-showcase/pull/2 ; head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`. All existing CI and native business statuses succeeded. Actual fix: local Copilot assistance in an isolated worktree; cloud dispatch failed before starting because the gh credential was not OAuth. Candidate v6: 9 passed / 0 failed / 0 errored, every row passed. PR remains UNMERGED; no DEMO release. This presentation task must not change PR state, merge or deploy.]

“The outer loop starts with an identifiable candidate and ends with an identifiable serving version. The PR carries more than code. It carries the reproduction, the reviewed expectation and the evidence needed to judge the change.

“DEV and DEMO are separate projects in this shared-account demo, not a hard production isolation boundary. The effective account-managed-identity scope for Memory is broader than project scope. A production release design needs its actual identities and permissions reviewed, not just two project names.

“We have a local Copilot-assisted repair, a PR ready for review and successful existing CI and native business statuses. We do not yet have a merge or DEMO release. The final serving-version link is still open.”

[64:00–65:15: open issue #1, then ready-for-review PR #2. **RB12 is bound to the existing records.** Inspect the actual issue, head SHA, review state and successful existing status checks. Do not create duplicates or change PR state. Ready for review is not approved, merged or released.]

“This issue is our record of the real replacement-recall mismatch. We can connect it to the captured response, the failed native item and the candidate PR.

“One important detail about how the fix was made: the cloud Copilot dispatch failed before it started because the available gh credential was not an OAuth token. The user approved gh CLI under SridharArrabelly, but that did not satisfy the cloud dispatch contract. The actual repair used local Copilot assistance in an isolated worktree.

“So I am not going to show a cloud coding-agent run that never happened. We will inspect the actual local-assisted patch. The acceptance criterion is still the business contract, not the assistant's explanation.”

[65:15–67:30: inspect the prepared local-assisted diff at PR head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`. State that the work was completed before this inspection. Show a local-session record only if it exists; do not invent a transcript, exact original prompt or cloud job. Limit editor time to the decision derivation and relevant regression.]

“Let us inspect the patch, not just the assistant's explanation. Where is the final structured decision derived? How does it use the observed eligibility result? Does it preserve missing, unknown, recalled and non-recalled cases rather than hard-coding a favorable answer?

“We inspect how the regression relates to the original failure and how the normal cases are preserved. The verified native comparison uses the unchanged nine-case dataset; a green check on unrelated behavior would not prove this repair.”

[67:30–69:30: inspect candidate provenance. The native v6 code hash matches packaged ZIP SHA-256 `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996`. Bind the exact artifact-view navigation rather than guessing a ZIP path. The full digest is recorded here and in the bindings. Keep the candidate version, PR head and packaged artifact association distinct from a promotion record.]

“This is the PR head, and this is the candidate artifact identity. The native v6 code hash matches the packaged ZIP. That is stronger evidence than a label saying ‘latest.’

“Now we inspect the native business result for that candidate. Other PR checks and human approval still answer separate questions. We do not call this the whole release gate merely because the business evaluation passed.”

[69:30–72:00: open candidate report https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_d6967759ba834c51b26a39296474ff0f . Confirm Completed, v6 captures, **9 passed / 0 failed / 0 errored**, each row passed, same pinned evaluator v1 and unchanged nine-case dataset. Retain the v1 8/9 report as the baseline, not a substituted metric.]

“The candidate passes all nine completed-response business cases, compared with eight in the v1 baseline. These are real captured v6 responses. Native evaluation grades them; it does not rerun the agent server-side.

“We also preserved an initial model-service failed invocation and retried it once. That operational failure is not erased by nine passing completed responses. Nine of nine does not mean one hundred percent availability, and zero grading errors is not a statement that every invocation succeeded.

“The evidence should identify the source commit, the built artifact or image where applicable, the agent version, the pinned Toolbox, the knowledge revision or snapshot, and the dataset and evaluator versions. Some systems expose these differently; the release record must still make the association explicit.”

[72:00–74:30: return to the PR's actual READY-FOR-REVIEW state and successful existing CI/native business statuses. **RB14 remains unfulfilled: unmerged, no DEMO release.** Do not substitute green checks, readiness for review or a candidate deployment for approval and serving evidence.]

“This is where the verified delivery story currently stops: the PR is ready for review, existing CI and native business statuses have succeeded, and the candidate business comparison passes. It is not merged and nothing has been released to DEMO.

“The remaining release work is real work: human review, all required checks, approval, promotion of the reviewed artifact, and verification of the actual serving version. We do not skip it to make the diagram look complete.”

[74:30–75:45: inspect the existing chain: baseline trace/report, issue #1, ready-for-review PR #2, successful statuses, head SHA, v6 native code/package hash and candidate report. Identify the unfilled promotion/serving link. Do not manufacture a live DEMO close.]

“For the eventual release, the artifact must match what was reviewed. A rebuild requires its own provenance and validation. We will also need an identifiable rollback target, not simply a remembered version name.

“The Memory investigation also taught us to distinguish authoritative session evidence from preview response metadata. Its v5 session pin was correct, but the response's agent reference reported endpoint-current v6. We keep that warning visible. For this candidate we have verified code-hash evidence; an eventual DEMO release still needs its own serving proof.”

[75:45–76:00: return to slides; advance to slide 16.]

**If asked to show the cloud job:** “There is no executed cloud coding-agent job to show. Dispatch failed before start. The fix used local Copilot assistance in an isolated worktree, and this is its actual PR diff.”

**If Copilot produces an incorrect patch:** “The proposed change does not meet the reviewed contract. We reject it. A development assistant is not an approval authority.” Use the already reviewed fallback only if one exists.

**If a gate fails:** “This candidate is not releasable. The gate has stopped it. We can inspect the failure or use the previously approved candidate, but we do not override the evidence to finish a demo.”

**If the release succeeds but the serving version does not match:** “Deployment completion and serving identity disagree. We have not proved promotion. We will not present the customer result as this candidate until that identity is resolved.”

**If asked whether the fix is released:** “No. The PR is ready for review and existing checks passed, but it is unmerged and there has been no DEMO release.” Keep the final serving link open.

## Slide 16 — Follow one fix from trace to customer

**Clock 76:00–78:00 · 1 minute demonstration + 1 minute slides.**

[RELEASE HOLD — RB15 is not complete. Candidate v6's real captures passed business grading, and PR #2 is ready for review, but no merge, DEMO release or post-promotion customer request is verified. Inspect candidate evidence and leave the release link open. The separate Memory v5 pin is verified, but preview version metadata remains misleading.]

[76:00: show slide 16 briefly, then open the actual replacement-recall row in the v6 candidate report. It is prepared evidence from real completed v6 responses, not a new invocation or DEMO serving proof. Keep the agent version and run identity visible.]

“This is the same business case in the corrected v6 candidate capture: order VC-10482 and batch CH-0722. The prose was already right in the baseline. The candidate now passes the structured business contract as well.”

[76:05–76:55: inspect the actual v6 row's passing verdict and recorded eligibility/decision evidence. The expected eligible outcome remains human assessment, not an automatic refund or shipment. Explicitly identify this as candidate capture evidence. The initial model-service failure and one retry remain disclosed; the report grades completed responses.]

“The completed candidate response passes this business case. That is useful progress, but the final serving-version link is still open: no DEMO promotion has occurred.”

[At 77:00 return to slide 16. Do not turn the conceptual serving-version node into a completed-delivery claim.]

“Follow the chain as far as the evidence takes us. The baseline trace showed the mismatch. The issue and ready-for-review PR connect it to the local-assisted fix. Existing CI and native business checks passed, and v6 has verified code/package identity. Approval, merge, DEMO release and serving proof still remain.

“Every link should refer to the same change. A pile of green screenshots from unrelated versions is not this chain.

“This is how operation teaches development—and how we distinguish a promising, tested candidate from a released customer service.”

[At 78:00 advance to slide 17.]

**If the candidate report is slow:** “The candidate report is taking longer to load. We have its verified completed result and artifact identity, but I will not substitute the v1 baseline as if it were the corrected capture or claim a DEMO request happened.” Use an actual v6 capture only if its display path is bound.

**If the displayed evidence has a different identity:** “This is not the verified v6 run. We must resolve the identity before claiming this result.” Finish with the conceptual takeaways and keep the release link open.

## Slide 17 — Useful. Governed. Measurable. Improving.

**Clock 78:00–80:00 · 2 minutes slides. Then 80:00–90:00 Q&A.**

“Four ideas to take back to your next agent.

“First, useful. Give the agent authoritative capabilities, not just a larger prompt. Our tools established business facts, and IQ supplied policy evidence we could inspect.

“Second, governed. Name the access contract and the boundary. Authorization, content controls and business rules solve different problems. Memory should preserve appropriate continuity, not become a hidden policy or permission store.

“Third, measurable. Correctness is a contract. Fluency and coherence are valuable, but they do not prove recall correctness. Evaluate identifiable candidates against reviewed cases, and inspect failures at case level.

“Fourth, improving. Operational evidence returns to development through human review. Copilot can help implement a narrow repair. The PR, evaluation gate and serving-version check keep that repair connected to the customer outcome.

“The point of the two loops is not to slow developers down. It is to preserve what we learn, make changes reviewable and avoid starting from a convincing demo every time.

“We did not just build an agent. We built a way to know what it did, control what it may do and improve it without losing the evidence.

“We have ten minutes for questions. Which boundary in your own application would you want to prove first: knowledge, tools, memory, evaluation or release?”

[Keep slide 17 visible for Q&A. Use hidden slides 18–19 only when the question benefits from their diagrams. Do not automatically advance into hidden backups. If any planned proof remained incomplete, replace the closing “we built” sentence with: “This is the operating model we are building toward; the incomplete proofs we named remain release blockers.”]

## Slide 18 — Hidden backup: memory scope

**Q&A only · not included in the 80-minute route or the audience PDF.**

[Open this hidden slide only for a memory/isolation question. Return to slide 17 afterward.]

“A Memory Store is a service container for persisted context. Scope partitions access to the items we retrieve, but the application must derive and use that scope correctly.

“The store is configured for one narrow synthetic preference, seven-day TTL and user profile only. We verified content, persistence and deletion for one authenticated caller across four separate sessions and conversations. Scope-to-user binding and cross-user isolation still require a second genuine authenticated identity.

“The native v5 session pin was correct. SDK and CLI use extra_body agent_session_id, native get_session confirmed v5, the returned session identity matched, and remember_response_style ran. The preview response's agent_reference nevertheless reported current endpoint v6, which has Memory off. We preserve the discrepancy rather than claim clean version metadata.

“The documented remedy was Foundry User for the DEV project's managed identity at account scope; OpenAI User alone was insufficient. That broader scope and the shared DEV/DEMO account are still not hard production isolation.

“Two conversations for caller A can demonstrate continuity. They cannot demonstrate caller isolation. That requires another authenticated caller, B, and an observed absence of A's preference.

“The same distinction applies to forgetting. A successful delete response is useful, but a read-back establishes that the item is no longer returned. Retention and deletion should be tested separately.

“This is not model training and not a system of record for recall, policy, identity or authorization. The memory preview also has network constraints; this session is not an entirely private-network design.”

[Current answer: “The single-caller native lifecycle passed, including content read-back, cross-conversation recall, deletion and no preference in a fourth conversation. Cross-user isolation has not been proved. A live segment must pin v5 using the forthcoming exact command; v6 has Memory off. Preview agent_reference metadata remains misleading.” Never display native Memory IDs, caller scope or raw private JSON.]

## Slide 19 — Hidden backup: account and project responsibilities

**Q&A only · not included in the 80-minute route or the audience PDF.**

[Open this hidden slide only for environment, identity or ownership questions. Return to slide 17 afterward.]

“The account and project scopes separate different responsibilities. The account is where model deployments and shared infrastructure are managed. Projects hold the agent-facing resources and runtime context used by teams.

“Our selected account is `fdy-volt-citadel-261111`, with `volt-dev` and `volt-demo` projects in the approved tenant. The resource group is `rg-volt-citadel` in Sweden Central.

“That structure helps us organize responsibilities, but this actual profile is not hard production isolation: DEV and DEMO share the account and the effective managed-identity role scope for Memory is broader than project scope. The intended production boundary needs its own identity, role and release design.

“Memory and evaluation model traffic are not automatically under the customer's APIM token budget. Project organization and a customer gateway policy do not imply a common budget boundary for every service-internal call.

“The public Foundry endpoint is Entra-authenticated in the approved design. Backend storage and Key Vault remain private. A data-zone model deployment is not a promise of Sweden-only processing.

“In a real customer system we would additionally need customer identity and order-ownership authorization, appropriate logging and retention, operational support and a production availability design. We should not confuse a synthetic enablement environment with a complete production compliance posture.”

## Appendix A — Complete Q&A answer bank

**Why hosted rather than prompt?**

“We chose hosted for custom deterministic runtime logic and this integration path. Prompt agents are a good managed option when their orchestration meets the need. Tools, CI and source control do not independently require hosted. The trade-off is owning application code and dependencies in addition to the usage and hosting costs.”

**Is Copilot the agent runtime?**

“No. GitHub Copilot is the development assistant in this route. The new customer runtime is Python Microsoft Agent Framework using Responses. The older Copilot SDK Invocations agent is a fallback implementation, not proof of hosted optimizer compatibility.”

**Did the cloud coding agent make this fix?**

“No. Cloud dispatch failed before starting because the gh credential was not an OAuth token. The user approved gh CLI as SridharArrabelly, and the actual fix used local Copilot assistance in an isolated worktree. Issue 1 and ready-for-review PR 2 are the records; there is no executed cloud coding-agent job to show.”

**Does 9/9 mean every invocation succeeded?**

“No. Candidate v6's nine completed real responses passed business grading. One initial model-service failed invocation was preserved and retried once. The result is not one hundred percent operational availability, and zero evaluation errors does not erase the invocation failure. Native evaluation grades captures rather than rerunning the agent server-side.”

**Does Citadel make the solution compliant?**

“No. Citadel supplies an implementable governance architecture. Compliance depends on the actual controls, data, identities, network posture, retention, operating procedures and organizational requirements. A gateway deployment does not automatically turn on Defender, Agent 365, Purview or every layer in the blueprint.”

**Is every hop keyless?**

“No. The backend uses managed identity for private storage. APIM reaches the Function with a function-scoped key held in Key Vault. Toolbox uses a managed per-use-case subscription credential to APIM. We need to describe and rotate those credentials according to their real contracts rather than call the entire chain keyless.”

**Can a user read someone else's order?**

“This synthetic demonstration does not implement real customer order-ownership authorization. An authenticated platform caller and an APIM consumer contract are not enough to establish that a real customer owns a particular order. That is a production requirement we would implement and test before using real customer data.”

**Does the gateway impose a dollar budget on all AI usage?**

“No. The configured twenty-thousand-token-per-minute and five-hundred-thousand-daily-token limits are token controls on the routed path, not a monetary cap across the platform. Memory and evaluation model traffic are not automatically under the customer's APIM token budget. Other service processing and idle infrastructure can also incur costs.”

**What does it cost, and how fast is it?**

“We have not published a validated cost-per-case or latency benchmark for this deliverable. The relevant cost includes APIM Developer, Search, hosted compute, Functions, storage, telemetry and model usage, including evaluation and optimization. Latency can include retrieval, multiple tool calls, model work and cold or queued execution. We would measure the representative path with versioned workload assumptions rather than promise a generic saving.”

**Is all processing in Sweden?**

“The selected resource group is in Sweden Central. The model uses a data-zone deployment SKU, so that location does not establish Sweden-only processing. We need to inspect the specific model, service and telemetry data-handling commitments separately.”

**Does IQ use vector search in this demo?**

“No. The implemented path is Azure AI Search with text and semantic extractive retrieval. We show the source-to-knowledge-to-agent architecture without claiming vector or hybrid retrieval or additional federated sources.”

**Can we replace the human with an automatic refund?**

“That would be a different risk and authorization design. Today's tools are read-only and the next step is human assessment. Moving money or changing an order needs explicit transaction authority, customer ownership checks, idempotency, appropriate approvals and its own evaluation and audit evidence.”

**Can guardrails prevent every unsafe action?**

“No. A successful blocklist fixture proves that configured boundary for that input. It does not establish universal jailbreak resistance or coverage of every tool. Content controls complement authorization, deterministic business rules, least privilege and human approval.”

**Does memory train the model, and can it store policy?**

“Here memory is persisted context retrieved for future requests, not training. We deliberately exclude policy, product facts, customer identity and permissions. Those remain authoritative elsewhere. We test retention, deletion and identity separation rather than trusting a convenient chat experience.”

**Why not release the optimizer's highest-scoring candidate?**

“Because its objective and tuning set are not the complete release contract. We need held-out business cases, safety and access checks, source review and measured trade-offs. A higher score can hide a regression. The baseline remains an acceptable decision if no candidate clears the gate.”

**How do we know the evaluator is right?**

“We review the expected business outcomes and test the evaluator itself against known pass and fail cases. Tool evidence and structured decisions make the contract more inspectable than fluency alone. Evaluator versioning, dataset review and case-level disagreement remain important; no aggregate removes the need for domain judgment.”

**Why not let production traces automatically become labels?**

“A trace tells us what happened, not what should have happened. It can contain an incorrect answer, irrelevant data or sensitive content. We select safe evidence, review the expected behavior and only then promote it into a regression case.”

**Is the defect real?**

“Yes. The captured v1 response had correct prose and citations but the wrong structured decision. Its native baseline was eight of nine. The local-assisted fix is in ready-for-review PR 2 and v6 passed all nine completed-response business cases on the same evaluator and dataset. It is still unmerged, with no DEMO release.”

**What happens if the pipeline fails during the session?**

“We keep the failure visible and do not release that candidate. If there is a previously approved run of the same repair, we label it as prepared and inspect its identity. Otherwise the release proof is incomplete. Finishing the story is not a reason to bypass a gate.”

## Appendix B — Shortened delivery paths

**If five minutes behind at 45:00:** keep native business evaluation and the customer-to-release chain. Recover three minutes by showing only the optimizer objective, actual candidate diff and final held-out verdict; omit the deep trade-off inspection. Recover two minutes by omitting the optional second-consumer gateway drill if it has not happened, or shorten the monitoring overview to the one relevant trace. Say: “I am compressing the inspection depth, not changing the standard of proof.”

**If ten minutes behind:** compress Memory to a redacted summary of the verified single-caller lifecycle and its limits: second-identity proof pending, explicit live v5 command forthcoming, misleading preview metadata. Use the existing local-assisted PR diff rather than reenacting generation or cloud dispatch. Preserve governance proof, native case evidence, the ready-for-review PR and the unfilled DEMO release link. Keep Q&A at minute 80; never project raw Memory evidence.

**If a whole integration is unavailable:** do not spend the recovered time narrating a fictional live proof. Say: “This capability remains a design walkthrough in this environment; the runtime proof is not available.” Move to verified evidence in the next chapter. The audience should leave knowing what was demonstrated and what was not.

**If only sixty minutes are available for content:** use slides 1–6 in ten minutes; customer tools and IQ in twelve; gateway and guardrail in eight; memory in four using prepared evidence; evaluation and optimizer in eight; trace, reviewed fix and release in fourteen; customer proof and four takeaways in four. Keep a separate ten-minute Q&A. Do not provision, wait on optimizer jobs or expand the code tour.

## Appendix C — Final rehearsal checklist

1. Replace RB01–RB15 with exact verified navigation, commands, IDs and fallback captures. No unresolved binding is silently treated as ready.
2. Verify the served runtime is Agent Framework + Responses, and keep the older Invocations fallback explicitly separate.
3. Warm the intended endpoint once; test the actual presentation network, screen scaling and signed-in identities.
4. Retain the verified Toolbox v2 preflight evidence described below; separately verify the hosted agent's correlated invocation and model route.
5. Verify the IQ references and passages. Do not infer grounding from service existence.
6. Prove allowed and denied APIM outcomes with redacted credential-safe evidence.
7. Prove the configured guardrail at the actual agent boundary and then prove permitted utility.
8. Use the verified four-session single-caller Memory summary. Bind the forthcoming exact live command with explicit v5 pinning; endpoint v6 has Memory off. Redact native item/session identifiers and caller scope. Cross-user isolation still needs a second genuine authenticated identity.
9. Open both native reports: baseline v1 8/9 and candidate v6 9/9, same pinned evaluator v1 and unchanged nine-case dataset. Disclose the preserved initial model-service failure and one retry. These grade completed real captures, not agent reruns or availability.
10. No Optimizer run exists yet. Use the conceptual branch unless a future actual job and its evidence are bound; never label the local-assisted fix an optimizer result.
11. Preserve the actual v1 mismatch, trace and `showcase\recordings\baseline-v1.json` at commit `78b54e4`. Review the replacement-recall regression; preserve the other baseline cases. Do not introduce a safety defect.
12. Open issue #1 and READY-FOR-REVIEW PR #2 at head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`. Existing CI/native business statuses succeeded. State local Copilot assistance and failed cloud dispatch; approval, merge and DEMO release remain separate.
13. Ensure fallback captures contain real timestamps and versions and are labelled prepared. No synthetic portal screenshot is evidence.
14. Check cost and quota headroom, current preview access and permissions. Do not expose secrets or broaden permissions on stage.
15. Rehearse twice against a reset environment. At 72:00 show the actual PR review state and explicitly leave the DEMO promotion link open; do not manufacture a release fallback.
16. The independent all-slide review and focused re-reviews, including slides 14 and 16, passed. This update changes presenter-only content; preserve every audience image.

**Verified Toolbox preflight — presenter preparation only, not a live feature catalogue.** The implementation owner has verified native APIM business MCP end-to-end through Foundry Toolbox v2. The curated Toolbox is exactly three business operations plus one IQ tool. Six direct-tool cases passed: recalled CH-0722; missing batch → `needs_batch`; unknown batch → `unknown`; order VC-10482 → delivered; recall replacement → eligible for human assessment; missing order → `needs_order`. These are real Toolbox preflight results, not native agent evaluation scores or proof of the hosted customer journey.

From the **demo repository root**, the durable verification command is:

`.\showcase\volt-support\src\agent-framework-agent-basic-responses\.venv\Scripts\python.exe .\showcase\scripts\probe_toolbox.py --project-endpoint https://fdy-volt-citadel-261111.services.ai.azure.com/api/projects/volt-dev --version 2 --out .\.runtime\volt-tool-retrieval.json`

The implementation owner's saved evidence is `.\.runtime\volt-tool-retrieval.json`, relative to that same demo root. The command is recorded here for rehearsal; the presentation author did not run it or operate Azure. SDK/CLI setup required the actual azd-managed `FOUNDRY_PROJECT_ENDPOINT` binding. That setup detail belongs in preflight, not on an audience slide.

Baseline execution, native v6 candidate grading and single-caller Memory lifecycle are separate proofs. Direct-tool preflight alone establishes none of them. The PR is ready for review, unmerged and not released to DEMO. An Optimizer run, cross-user Memory isolation and the exact live v5 command remain unbound.

**Verified hosted execution and selected incident.** The implementation owner verified `volt-support` version 1, Responses 2.0.0, Toolbox 2. Protocol output shows all four tools actually executed: order, recall, eligibility and IQ. Response ID: `caresp_02ddb9a77175f58700lAjFhWXx30P0Frxo1oLxhgKwmjshXgd7`. Trace ID: `8be3ccdd0e7b0bdcac285dcbbcdf4ef4`. Observed client elapsed: **25.372 seconds for one request**, not an SLA or performance benchmark. The exact portal URL and invocation command are embedded in slide 7's notes and `Rehearsal bindings.json`.

The baseline answer's prose and citations are right, but its model decision is `recommendation` while the eligibility tool returned `eligible`. This remains the historical incident and native v1 failure. The later v6 capture passes this business case; do not portray the baseline failure as unchanged v6 behavior or infer DEMO release from the candidate result.

**Completed native baseline:** business_contract v1 — **8 passed, 1 failed, 0 errored of 9**. Failed item 1 is `replacement-recall`. This new hosted **8/9** baseline is not the old local **7/9**. It grades captured real hosted responses and observed successful tool calls, not coherence and not a server-side rerun. Replay artifact: `showcase\recordings\baseline-v1.json`, commit `78b54e4`.

Native report: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_28da2cdf28224eb799a9a2e3d9f8672e

**Completed candidate v6:** **9 passed, 0 failed, 0 errored**, each of nine rows verified passed. Same pinned evaluator v1; unchanged nine-case dataset. One initial model-service failed invocation was preserved and retried once. This is business grading of completed real responses, **not 100% operational availability**, and native evaluation does not rerun the agent server-side.

Candidate report: https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,fdy-volt-citadel-261111,volt-dev/build/evaluations/eval_5a3774acf4f347e1bd35ae30375d0f2d/run/evalrun_d6967759ba834c51b26a39296474ff0f

Candidate provenance: PR head `1d01eaae455ac0b2aa39da0f5a57d5543017a5e2`; native v6 code hash matches packaged ZIP SHA-256 `ac015b257905e6dbd92f04bc49d6f86c8eb757f22557433c7c2ad47a83508996`. Issue https://github.com/SridharArrabelly/foundry-showcase/issues/1 ; READY-FOR-REVIEW PR https://github.com/SridharArrabelly/foundry-showcase/pull/2 . All existing CI/native business statuses succeeded; PR is unmerged, with no DEMO release. Cloud dispatch failed before start; actual fix used local Copilot in an isolated worktree, with user-approved gh CLI identity SridharArrabelly.

**Verified guardrail:** `probe_guardrail.py` produced HTTP 400, code `content_filter`, type `content_safety_error`, input stage. The recorded local evidence is `.\.runtime\volt-guardrail-proof.json`; request ID `088298eff265d56cd2438f8dbd2dcbb2`; `native_filter_observed=true`. The exact rehearsal command and the named-agent/version caveat are in slide 10's notes. This proves the configured harmless-marker block, not universal safety.

**Memory single-caller lifecycle PASSED:** four distinct sessions/conversations verified native remember, exact stored-content read-back, new-conversation recall, forget by native item identity, native deletion and a fourth conversation reporting no saved preference. Private evidence locator: `.runtime\memory-proof-v5-pinned\summary.json` plus four step records. These files are **not copied into the materials**. Redact native Memory IDs, caller scope and raw session IDs everywhere; no actual values are recorded here.

**Pinning correction:** SDK/CLI correctly use `extra_body.agent_session_id`. Native `get_session` confirmed v5 and the returned session identity matched; `remember_response_style` actually executed. Preview response `agent_reference` misleadingly reports endpoint-current v6 even for the v5-bound session. The probe preserves both and warns. This is not a confirmed routing failure or clean version metadata. Current endpoint v6 has Memory off; the live Memory segment **must pin v5**, and the exact command is forthcoming.

**Permission and isolation limits:** the documented Foundry User role for the DEV project's managed identity was required at Foundry account scope; OpenAI User alone was insufficient. A second genuine authenticated identity is still required to prove scope/user-ID binding and cross-user isolation. The shared-account DEV/DEMO profile remains **not a hard production isolation boundary**. Memory/evaluation model traffic is not automatically under the customer APIM token budget.

Foundation commit `3d72b88` is pushed on `feature/volt-citadel`; historical CI passed at https://github.com/SridharArrabelly/foundry-showcase/actions/runs/43028286638. Keep that separate from the current ready-for-review PR and v6 comparison. Automatic Insights findings, an Optimizer run, approval, merge and DEMO release remain unverified. The presentation author has not operated Azure, read/copied private Memory proof files, changed PR status or performed Git operations.

## Appendix D — Source framing and references

The supplied workshop is the primary narrative and design source: two environments/two loops/two bridges (15); hosted as the control path (31); governed capabilities (47, 57); supported intervention boundaries (128); trust by evidence rather than a lucky run (83); evaluate/apply/release as separate decisions (98, 101); human-reviewed trace flywheel (185); gated outer loop (159); and evidence-led takeaways (198). All original finance, Nova, library and Factory narration has been replaced. The complete source-slide mapping and readiness snapshot are in `Source mapping and readiness.md`.

Official references for presenter preparation, not claims that the current runtime implements every documented feature:

- https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent
- https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox
- https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq
- https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-memory
- https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-guardrails
- https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-overview
- https://learn.microsoft.com/azure/foundry/concepts/evaluation-evaluators/custom-evaluators
- https://learn.microsoft.com/azure/foundry/how-to/develop/cloud-evaluation
- https://github.com/Azure-Samples/foundry-citadel-platform
- https://github.com/Azure-Samples/ai-hub-gateway-solution-accelerator
