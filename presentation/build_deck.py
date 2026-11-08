"""Editable 16:9 presentation, using the workshop's indigo/lilac visual language."""
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
OUT = HERE / "Foundry - From prototype to operated service.pptx"
P = {"ink": "242424", "muted": "626272", "blue": "0408AC", "purple": "4F42FD",
     "lilac": "E6E1FF", "paper": "F7F7FA", "white": "FFFFFF", "dark": "1C1B30",
     "green": "087A54", "red": "B3261E", "line": "D8D5E9"}
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
prs.core_properties.title = "Microsoft Foundry: from prototype to operated service"
prs.core_properties.subject = "Volt and Co | GitHub Copilot SDK | Microsoft Foundry"
prs.core_properties.author = "Sridhar Arrabelly"
prs.core_properties.keywords = "Foundry, GitHub Copilot SDK, agent lifecycle, synthetic demo"
notes_export = []


def rgb(key):
    return RGBColor.from_string(P.get(key, key))


def box(slide, x, y, w, h, fill="white", line=None, rounded=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if line:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    if rounded:
        shape.adjustments[0] = 0.08
    return shape


def text(slide, value, x, y, w, h, size=22, color="ink", bold=False, font="Segoe UI"):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    for i, line in enumerate(value.split("\n")):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.text = line
        para.font.name = font
        para.font.size = Pt(size)
        para.font.bold = bold
        para.font.color.rgb = rgb(color)
        para.space_after = Pt(8)
    return shape


def arrow(slide, x1, y1, x2, y2, color="purple"):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
        Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(2)
    from pptx.oxml.xmlchemy import OxmlElement
    end = OxmlElement("a:tailEnd")
    end.set("type", "triangle")
    shape.line._get_or_add_ln().append(end)


def circle(slide, label, x, y, color="blue"):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(.52), Inches(.52))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    shape.line.fill.background()
    t = text(slide, label, x, y + .045, .52, .4, 18, "white", True)
    from pptx.enum.text import PP_ALIGN
    t.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER


def slide(title, eyebrow, subtitle=None, dark=False, hidden=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb("dark" if dark else "paper")
    if hidden:
        s._element.set("show", "0")
    text(s, eyebrow.upper(), .55, .35, 12.1, .32, 12, "lilac" if dark else "blue", True)
    text(s, title, .55, .93, 12.0, 1.15, 34, "white" if dark else "ink")
    if subtitle:
        text(s, subtitle, .57, 2.02, 12.0, .62, 18, "lilac" if dark else "blue")
    n = len(prs.slides)
    text(s, "MICROSOFT FOUNDRY  |  VOLT & CO  |  SYNTHETIC DEMO", .55, 7.07, 10.8, .2, 9,
         "lilac" if dark else "muted")
    text(s, f"{n:02}", 12.18, 7.02, .55, .28, 12, "lilac" if dark else "blue", True)
    return s


def card(s, x, y, w, h, title, body, number=None, fill="white", accent="blue"):
    box(s, x, y, w, h, fill, "line", True)
    if number:
        circle(s, number, x + .22, y + .24, accent)
        tx, tw = x + .9, w - 1.12
    else:
        tx, tw = x + .25, w - .5
    text(s, title, tx, y + .26, tw, .75, 23, accent, True)
    text(s, body, x + .25, y + 1.15, w - .5, h - 1.35, 19, "ink")


def band(s, value, y=6.14, color="blue"):
    box(s, .55, y, 12.2, .65, color, rounded=True)
    text(s, value, .8, y + .13, 11.7, .43, 20, "white", True)


def notes(s, time, talk, show="", transition="", back="", fallback="", source=""):
    body = (
        f"TIME: {time}\n\nTALK TRACK\n{talk}\n\n"
        f"ON SCREEN / DEMO CUE\n{show or 'Stay on this slide.'}\n\n"
        f"TRANSITION OUT\n{transition}\n\nRETURN FROM DEMO\n{back or 'Not applicable.'}\n\n"
        f"IF TIME OR TECHNOLOGY FAILS\n{fallback or 'Keep the main message and move on.'}\n\n"
        f"SOURCE / CLAIM BOUNDARY\n{source}\n\n"
        "PRESENTER REMINDER: All Volt and Co records are synthetic. Show recorded evidence as recorded, "
        "and live invocations as live. The demo has local DEV and a hosted demo target in one Foundry project; "
        "it is not a production-isolation reference deployment."
    )
    s.notes_slide.notes_text_frame.text = body
    notes_export.append((len(prs.slides), s.shapes[1].text if len(s.shapes) > 1 else "", body))


s = slide("From prototype\nto operated service", "Microsoft Foundry | Customer deep dive", dark=True)
text(s, "Build with GitHub Copilot.\nRun, evaluate and improve with Foundry.", .6, 3.0, 7.1, 1.4, 28, "white")
for i, (head, detail) in enumerate([("BUILD", "One useful agent"), ("PROVE", "Evidence before release"), ("IMPROVE", "Learn from operations")]):
    y = 2.85 + i * 1.05
    circle(s, str(i + 1), 9.0, y, "purple")
    text(s, head, 9.75, y, 2.7, .4, 19, "white", True)
    text(s, detail, 9.75, y + .43, 2.8, .45, 15, "lilac")
text(s, "Sridhar Arrabelly  |  50 minutes + Q&A", .6, 6.35, 10, .45, 17, "lilac")
notes(s, "Holding slide; welcome included in 00:00-02:00", "Welcome. This is a practical story, not a feature tour. We will follow a single assistant from useful behaviour to a reviewable release and back into development. The slides supply the mental model; the demo supplies the evidence.", transition="The first distinction is between an impressive answer and an operated service.", source="Workshop slides 9 and 12; current Microsoft Foundry product name.")

s = slide("A convincing answer is only the beginning", "The business problem", "The harder question: can we explain, release and keep improving it?")
card(s, .55, 2.95, 3.9, 2.65, "Useful", "It solves a real customer task.\nNot just a fluent response.", "1")
card(s, 4.72, 2.95, 3.9, 2.65, "Provable", "We can inspect behaviour\nand measure regressions.", "2")
card(s, 8.88, 2.95, 3.9, 2.65, "Operable", "Every release has evidence.\nOperations teaches DEV.", "3")
band(s, "Our question today: what evidence earns the next release?")
notes(s, "00:00-02:00", "A prototype may answer impressively while using the wrong tool, skipping a policy, or being impossible to reproduce. We are not claiming building agents is trivial. We are saying that building is only part of the responsibility. Foundry connects development and operations; our engineering policies make the connection enforceable.", transition="Let's give that responsibility a concrete customer and a small set of checkable facts.", source="Adapted from workshop slide 9; avoid unsupported reliability or performance claims.")

s = slide("Meet Volt & Co", "One use case throughout", "A fictional electronics assistant that recommends the cheapest product that works.")
box(s, .55, 2.85, 4.15, 3.15, "dark", rounded=True)
text(s, '"A charger for my\nVolt Book 14.\nUnder EUR 50."', .85, 3.18, 3.5, 1.65, 27, "white")
text(s, "Six synthetic products.\nNo purchases. No customer data.", .85, 5.3, 3.5, .65, 15, "lilac")
for i, (title, body) in enumerate([
    ("Find", "Catalog facts and prices"),
    ("Check", "Device compatibility"),
    ("Support", "Batch-specific recall status"),
]):
    y = 2.85 + i * 1.02
    circle(s, str(i + 1), 5.1, y + .1)
    text(s, title, 5.86, y + .06, 2.0, .42, 23, "blue", True)
    text(s, body, 8.0, y + .1, 4.3, .65, 20)
band(s, "Boundary: missing evidence is not permission to claim certainty.")
notes(s, "02:00-04:00", "Volt and Co is the same sample use case as the workshop. We deliberately narrowed it to three read-only tools. The fixture has a 30W charger at EUR 19.90, a 65W charger at EUR 39.90, and a 100W charger at EUR 59.90. Volt Book 14 requires 65W. These numbers are fictional and mechanically checkable. Later, the same customer's recall enquiry will expose a missing-information case.", show="Point to Find, Check and Support. Do not introduce the other workshop skills.", transition="We will follow these three capabilities around two loops.", source="Workshop slide 6 and notes. New synthetic fixture: volt/data.json; no claim that these prices came from the original deck.")

s = slide("Two loops. Two evidence bridges.", "The lifecycle", "The inner loop proves a candidate. The outer loop releases and learns.")
card(s, .55, 2.85, 5.05, 2.6, "INNER LOOP | DEV", "Build + connect\nRun + trace\nEvaluate + improve", fill="white")
card(s, 7.7, 2.85, 5.05, 2.6, "OUTER LOOP | SERVING", "Gate + release\nObserve + investigate\nReview + feed back", fill="white", accent="purple")
arrow(s, 5.75, 3.38, 7.55, 3.38)
text(s, "candidate\n+ evidence", 5.9, 3.65, 1.6, .95, 15, "blue")
box(s, .55, 5.75, 12.2, .72, "lilac", rounded=True)
text(s, "Observed interaction  >  human review  >  new regression case  >  next candidate", .85, 5.92, 11.6, .45, 20, "blue", True)
notes(s, "04:00-07:00", "The workshop's inner loop is build/connect, run/debug/trace, evaluate/guard and improve in DEV. The outer loop is gate/release, readiness, operation and reviewed feedback. The forward bridge carries source revision, configuration, dataset and results. The return bridge carries evidence plus a reviewed expectation. A production trace is not a correct answer by definition. For this compact demo, DEV is local and the serving target is a Foundry demo project; production would separate environments and identities more fully.", transition="Before the first request, here is exactly where GitHub and Foundry each participate.", source="Workshop slides 12-14 and speaker notes. https://learn.microsoft.com/azure/foundry/agents/concepts/development-lifecycle")

s = slide("Build with GitHub. Operate in Foundry.", "Architecture | one runtime, not two agents", "GitHub Copilot develops the code. The Copilot SDK is the application's runtime harness.")
card(s, .55, 2.85, 3.65, 2.65, "GitHub", "Code + Copilot\nTests + pull requests\nActions + evidence", "1")
card(s, 4.83, 2.85, 3.65, 2.65, "Copilot SDK", "Constrained harness\nThree read-only tools\nFoundry model via Entra", "2")
card(s, 9.1, 2.85, 3.65, 2.65, "Foundry", "Hosted agent + endpoint\nEvaluation + traces\nOperational review", "3")
arrow(s, 4.25, 4.05, 4.72, 4.05)
arrow(s, 8.54, 4.05, 9.0, 4.05)
band(s, "We own the business logic. Foundry manages the hosting around it.")
notes(s, "07:00-09:00", "There are two distinct uses of Copilot: the developer assistant and the SDK harness inside our business agent. This is a hosted agent, not a managed Copilot-harness prompt agent. The model is deployed in Foundry and authenticated with Entra; no GitHub token is embedded. The runtime exposes only three reviewed business tools. The demo does not connect a managed Foundry Toolbox or APIM gateway; those remain an extension path rather than a claim about this implementation. Our custom application spans complement Foundry-host telemetry.", transition="Let's prove the useful path first. I will not spend your time provisioning infrastructure live.", source="Workshop slides 6 and 30. Official Microsoft Copilot SDK Invocations sample; github/copilot-sdk BYOK documentation.")


def demo_slide(number, title, query, checks, timing, talk, show, back, fallback):
    s = slide(title, f"Live demo {number} | {timing}", dark=True)
    box(s, .6, 2.65, 7.2, 2.4, "white", rounded=True)
    text(s, query, .95, 3.0, 6.5, 1.7, 27, "blue")
    for i, check in enumerate(checks):
        circle(s, str(i + 1), 8.35, 2.83 + i * .92, "purple")
        text(s, check, 9.12, 2.91 + i * .92, 3.35, .76, 19, "white")
    text(s, "Live execution where ready. Recorded evidence is labelled and versioned.", .65, 6.25, 11.8, .5, 17, "lilac")
    notes(s, timing, talk, show=show, transition="Switch to the prepared demo surface now.", back=back, fallback=fallback, source="Executable commands are in docs/PRESENTER.md and scripts/demo.py. Do not present an offline tool test as a live model evaluation.")
    return s


demo_slide("01", "A useful answer, with an inspectable path",
    "Find the cheapest charger for my\nVolt Book 14 under EUR 50.",
    ["Check the recommendation", "Inspect the tool evidence", "Follow the request trace"], "09:00-16:00",
    "The 30W charger is cheapest, but it does not meet the device's 65W requirement. The 65W model is the cheapest compatible in-budget choice. Open the structured result, not just the prose. Catalog and compatibility do not guarantee that a specific batch is safe. Then run the known recall enquiry from the source deck.",
    "Transition 09:00-10:00. In the demo directory: python scripts/demo.py ask \"Find the cheapest charger for my Volt Book 14 under EUR 50.\" --out evidence/shopping.json. Then ask \"Is my Volt Charge 65 from batch CH-0722 safe to use?\". Foundry portal: project > agent > Traces; open a completed request. Tool evidence is in the captured JSON even if portal ingestion is delayed.",
    "We have explained one execution. Now ask whether it holds across a representative set.",
    "Use the captured shopping and recall JSON plus the telemetry view from rehearsal. Say when it was recorded. Do not wait more than 30 seconds for an ingested trace.")

s = slide("A good demo is not a quality baseline", "Prove the behaviour", "Use the same reviewed cases to compare candidates.")
card(s, .55, 2.9, 5.8, 2.65, "Trust by demo", '"It looked right when I tried it."\nOne execution, unknown coverage.', fill="white", accent="red")
card(s, 6.95, 2.9, 5.8, 2.65, "Trust by evidence", "Named cases. Expected behaviour.\nResults tied to the exact candidate.", fill="white", accent="green")
band(s, "A green score on a small dataset is evidence, not a guarantee.")
notes(s, "16:00-17:00", "The dataset is part of the product contract, not an afterthought. We include shopping, insufficient budget, incompatibility, known recalls, unknown batches and refusal of fabricated invoices. We compare candidates on identical reviewed cases and retain failures. We do not invent an accuracy or cost-improvement percentage. A synthetic set is useful for a demonstration, but a production evaluation needs customer-specific distribution and expert labels.", transition="Different questions need different kinds of checks.", source="Workshop slide 84; datasets/core.jsonl.")

s = slide("Three checks, three different jobs", "Evaluation design", "Do not ask one magic score to do everything.")
card(s, .55, 2.85, 3.9, 2.95, "Deterministic", "Correct product and batch\nRequired tool evidence\nMissing-input contract", "1")
card(s, 4.72, 2.85, 3.9, 2.95, "Model-judged", "Native Foundry scorecard\nResponse coherence\nA signal, not domain truth", "2")
card(s, 8.88, 2.85, 3.9, 2.95, "Human review", "Expected behaviour\nAmbiguous risk decisions\nRelease acceptance", "3")
band(s, "Useful + correct enough for the agreed cases + reviewable.")
notes(s, "17:00-18:00", "We use deterministic assertions where the fixtures give an objective answer. A native Foundry coherence evaluation scores the captured live responses; it does not replay the agent and it does not certify recall correctness. The human reviewer defines what missing information should cause the agent to do. In production, add calibrated semantic and safety evaluators suited to the risk profile. Check availability per evaluator rather than calling the whole catalog GA.", transition="Now look at a baseline and a deliberately narrow correction.", source="Workshop slide 86. https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets")

demo_slide("02", "Change one thing. Measure what changed.",
    "Baseline  >  evidence  >  correction\n\nSame questions. Same assertions.",
    ["Open a failing case", "Inspect the code change", "Compare the candidate"], "18:00-25:00",
    "The intentional baseline defect is in the recall tool: no batch was mistaken for a negative recall lookup. This is not a claim that the model happened to fail today. We show the defect and its consequence explicitly. The improved version returns needs_batch. The agent then asks for the missing fact. The core suite and the extended regression suite are distinct; a passing core suite never implied it covered the missing-batch case.",
    "Show volt/domain.py recall_notices and its baseline/improved branch. Open the actual baseline and improved report files. Run: python scripts/check_contract.py --variant baseline (expected exit 1), then --variant improved. Run the focused live missing-batch query against the saved version. Open the native Foundry evaluation URL from evidence/foundry-evaluation.json.",
    "The candidate is improved on this reviewed contract. It still needs a controlled release decision.",
    "Use completed live reports. The offline contract command proves the business-code correction only; label it as such. Skip a fresh full model evaluation if it exceeds the budget.")

s = slide("Release the evidence, not just the prompt", "The outer loop", "A passing check is meaningful only when the release path enforces it.")
for x, n, title, body in [
    (.55, "1", "Verify", "Code tests\nReviewed cases\nCandidate identity"),
    (4.72, "2", "Decide", "Required criteria\nHuman acceptance\nRecorded evidence"),
    (8.88, "3", "Release", "Pinned version\nKnown configuration\nRollback reference"),
]:
    card(s, x, 2.85, 3.9, 2.85, title, body, n)
band(s, "Foundry supplies capabilities. We configure the release policy.")
notes(s, "25:00-27:00", "A model score is not a release system. Our workflow determines which checks run and whether execution continues. The repository's credential-free quality workflow runs unit and tool-contract tests. Live evaluation evidence is separate and must not be relabelled as CI's offline output. The release script accepts only a passing live scorecard for the evaluated version and creates a release manifest. Production should add environment approvals and separate deployment identities; a private repository's branch-protection availability depends on the GitHub plan.", transition="I will show actual completed checks, not wait for a cold deployment.", source="Workshop slides 14, 162 and 178. Microsoft hosted-agent CI/CD quickstart.")

demo_slide("03", "A release we can explain",
    "Source revision + agent version\n+ dataset hash + scorecard",
    ["Show BLOCK and PASS", "Inspect the release record", "Invoke the pinned version"], "27:00-34:00",
    "The blocked workflow is intentionally run with the baseline business contract; it is a real GitHub Actions failure, not a screenshot of a fabricated pipeline. The improved run passes that contract. Keep offline CI and live model evaluation distinct. Open the recorded live candidate scorecard, the version and the release manifest. Invoke that exact deployed version. Say clearly that deployment happened during rehearsal.",
    "Transition 27:00-28:00. GitHub repository > Actions > Volt quality gate: open the baseline and improved runs. Open evidence/release.json. Run python scripts/demo.py ask \"Check Volt Charge 65 batch CH-0926 for a recall.\" --version <recorded improved version>. Use the recorded version from the manifest, not an invented number.",
    "A release only proves the expectations we wrote down. Operations brings us the next question.",
    "Use captured Actions logs and the release manifest if GitHub or Azure is slow. Never say a full production governance pipeline is enforced if required checks/environment controls have not been configured.")

s = slide("Operations teaches development what to test", "The return bridge", "An observation becomes a regression case only after review.")
steps = [("Observe", "An ambiguous recall enquiry"),
         ("Review", "Decide the expected behaviour"),
         ("Add a test", "Keep trace provenance"),
         ("Improve", "Prove the next candidate")]
for i, (head, body) in enumerate(steps):
    x = .55 + i * 3.12
    card(s, x, 2.95, 2.85, 2.6, head, body, str(i + 1))
band(s, "Observed output is evidence. It is not automatically a label.")
notes(s, "34:00-35:00", "Our production-like traffic is synthetic. We intentionally include an enquiry that omits the batch number. We inspect the actual captured result and its tool path, then review what the response should have done. The feedback command requires explicit approval and records the reviewer, source invocation, trace ID and content hash. It refuses to overwrite an existing review file. This is an application workflow, not an automatic Foundry correction.", transition="Let's carry one observed interaction back into the test set.", source="Workshop slides 14, 189 and 193. Trace-to-dataset conversion is preview; this package also includes an explicit code-first reviewed-row path.")

demo_slide("04", "Close the loop",
    "I have a Volt Charge 65.\nIs it safe?",
    ["Inspect the missing fact", "Approve one regression row", "Recheck the corrected version"], "35:00-47:00",
    "Missing information is not a negative result. Show the recorded baseline trace and the returned no_recall status despite the absent batch. Review the correct contract: ask for the batch, do not assert safety. Export one reviewed case. Return to DEV and show the fix. Run it against the earlier and corrected versions or use the completed reports if time is short. Do not patch the serving agent directly from an operational screen.",
    "35:00-42:00: Foundry Monitor/Traces or Application Insights; open the seeded missing-batch request. Run the feedback command in docs/PRESENTER.md with a human reviewer. 42:00-43:00: return to DEV. 43:00-47:00: show the focused regression FAIL/PASS and full core+regression evidence. Foundry's native Add to dataset path is optional preview, not required for the code-first loop.",
    "The next release has a stronger contract because operations supplied a new case.",
    "Preserve this segment if running late: skip fresh batch evaluation or optional preview screens, but show observation, review, test and corrected evidence. Use the same captured request, not another agent's screenshots.")

s = slide("Four things to take away", "One continuous lifecycle", dark=True)
for i, (title, detail) in enumerate([
    ("Build for a customer task", "One use case makes the architecture meaningful."),
    ("Prove behaviour, not just wording", "Inspect the path and compare reviewed cases."),
    ("Make release policy explicit", "A score matters when a gate uses it."),
    ("Turn observations into tests", "Human-reviewed feedback strengthens the next release."),
]):
    y = 2.5 + i * .91
    circle(s, str(i + 1), .65, y, "purple")
    text(s, title, 1.45, y - .02, 10.6, .43, 24, "white", True)
    text(s, detail, 1.45, y + .45, 10.6, .4, 17, "lilac")
notes(s, "47:00-49:00; 49:00-50:00 buffer", "We built with GitHub Copilot, ran a Copilot SDK harness in Foundry, inspected tool evidence, measured behaviour, showed a reviewable release and returned an observation to development. The differentiator is the connection across these activities. For a customer pilot, choose one outcome, agree its failure boundaries and define who owns the release decision. Do not promise this small demonstration is a production-ready solution.", transition="Let's use the remaining time on the decisions that matter for your environment.", source="Selective synthesis of workshop slides 12 and 202; unused memory/IQ/optimizer claims removed.")

s = slide("Your questions. Your operating model.", "Q&A | 50:00-60:00", "The right next step is a bounded pilot with an agreed evidence contract.")
card(s, .55, 3.0, 3.9, 2.55, "Outcome", "What customer task\nmust improve?")
card(s, 4.72, 3.0, 3.9, 2.55, "Boundary", "What must never\nhappen?")
card(s, 8.88, 3.0, 3.9, 2.55, "Ownership", "Who can approve\nand operate a release?")
notes(s, "50:00-60:00", "Use the hidden appendix only when a question earns it. Technical questions: hosted versus prompt, SDK versus development assistant, identity, network boundaries, model cost, evaluation coverage. Business questions: handling time, resolution quality, escalation quality and total operating cost. ROI needs a customer baseline. No generic claim that all data remains in Sweden: the selected model uses GlobalStandard, and processing geography follows that deployment type and connected services.", transition="Close on the customer's next measurable decision, not a catalogue of features.", source="Architecture reference deck: outcome-first and ownership framing.")

s = slide("What is live here, and what is not", "Appendix | implementation boundaries", hidden=True)
card(s, .55, 2.8, 5.85, 3.55, "Implemented", "Copilot SDK + Foundry model\nHosted Invocations endpoint\nThree read-only business tools\nApp Insights application spans\nCode and model-judged evaluations")
card(s, 6.9, 2.8, 5.85, 3.55, "Not claimed", "Managed Foundry Toolbox / APIM\nAutonomous self-correction\nCustomer production isolation\nFull safety certification\nMeasured cost or ROI improvement", accent="purple")
notes(s, "Q&A backup only", "Use this slide to keep the promise precise. The tool surface is packaged and allowlisted in code. The managed Toolbox and APIM story is an extension, not a hidden prerequisite. Native semantic scoring evaluates captured outputs. The demo is deliberately narrow; the production architecture needs stronger environment isolation, identities and governance based on customer requirements.", transition="Return to the relevant live artifact rather than expanding into another feature tour.", source="Implementation inspection and workshop scope reduction.")

s = slide("Availability is capability-specific", "Appendix | status checked 8 November 2026", hidden=True)
card(s, .55, 2.8, 5.85, 3.5, "GA core", "Foundry hosted agents\nPrompt/hosted agent tracing\nCore evaluations*\nManaged Toolbox*\nModel guardrails", accent="green")
card(s, 6.9, 2.8, 5.85, 3.5, "Preview boundaries", "Monitor and recurring evaluations\nTrace-to-dataset conversion\nInsights; skills\nAgent guardrails / intervention\nAgent Optimizer: limited preview", accent="purple")
text(s, "* Individual tools, evaluators and networking paths can differ. Recheck before delivery.", .6, 6.55, 12, .36, 14, "muted")
notes(s, "Q&A backup only", "The GA matrix describes named experiences. Do not turn the platform's GA milestone into a blanket promise. The Copilot SDK and specific package/API versions have their own lifecycle; pin and verify them independently. Avoid live dependencies on optimizer and Insights. The implementation uses native model-judged coherence, whose evaluator requirements should be checked in the selected region.", source="https://learn.microsoft.com/azure/foundry/concepts/general-availability\nhttps://learn.microsoft.com/azure/foundry/observability/concepts/trace-agent-concept", transition="Tie the answer to the customer's required capability and region.")

s = slide("Who owns what?", "Appendix | responsibility and security", hidden=True)
card(s, .55, 2.8, 3.9, 3.15, "Application team", "Instructions + tools\nDomain correctness\nTests + release criteria\nCustomer experience")
card(s, 4.72, 2.8, 3.9, 3.15, "Platform", "Hosting + endpoints\nIdentity integration\nTrace infrastructure\nEvaluation services")
card(s, 8.88, 2.8, 3.9, 3.15, "Shared decisions", "Least privilege\nData + trace retention\nNetwork boundaries\nIncident ownership")
band(s, "Managed hosting does not make the application correct or risk-free.", y=6.3)
notes(s, "Q&A backup only", "This is a responsibility map, not a compliance certification. Agent identities need explicit access to downstream services. An Azure management-plane Owner role did not, by itself, supply the data-plane access needed during setup; Foundry User is scoped separately. Trace content can contain sensitive data. This demo uses only synthetic data and a 30-day telemetry retention configuration. GlobalStandard model deployment does not promise Sweden-only processing.", source="Workshop slide 30 and official Foundry identity/tracing guidance.", transition="Bring the discussion back to a concrete customer requirement.")

s = slide("When the network is not on our side", "Appendix | shortened path", hidden=True)
for i, (title, body) in enumerate([
    ("Keep", "The same use case\nThe evidence bridges\nThe feedback-to-test moment"),
    ("Use", "Captured live JSON\nCompleted evaluation runs\nSaved release evidence"),
    ("Say", "This is a rehearsal capture.\nHere is its version and date.\nThis is the result we observed."),
]):
    card(s, .55 + i * 4.17, 2.85, 3.9, 2.9, title, body, str(i + 1))
band(s, "Skip waiting. Do not replace evidence with invented numbers.")
notes(s, "Presenter backup; not part of the 50-minute path", "If five minutes behind, replace fresh batch runs with completed results and omit preview-only screens. If Azure is unavailable, show captured results with recorded timestamp, version, tool evidence and trace ID. If no live evidence was captured successfully, say the cloud step is unverified and use only the offline domain test as a limited code demonstration. Do not imply it is a substitute for the live Foundry journey.", transition="Return to the four takeaways.", source="docs/REHEARSAL.md")

s = slide("Sources and useful boundaries", "Appendix | official references", hidden=True)
text(s, "Primary story: Foundry Agent Platform Workshop v1.0.0\nSlides 6, 9, 12-14, 30, 84, 86, 162, 189 and 193.", .65, 2.65, 12, 1.0, 21, "blue", True)
text(s, "Microsoft Learn: hosted agents, lifecycle, tracing, evaluations and GA matrix\nMicrosoft Foundry samples: Copilot SDK / Invocations\nGitHub Copilot SDK: BYOK, tool declarations and runtime configuration\nAll links and exact package versions are in the repository.", .65, 3.95, 12, 1.65, 20)
band(s, "No NDA roadmap. No unmeasured security, residency, cost or performance claims.")
notes(s, "Backup only", "The primary deck and its notes supplied the narrative. Finance and public-library screenshots were not reused as Volt evidence. The reference architecture supplied outcome-first and ownership framing. The OTP briefing's NDA roadmap pages were excluded. The unreadable enterprise operating-system deck was not used. All visuals here are editable diagrams, not fabricated portal screenshots.", source="\n".join([
    "https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents",
    "https://learn.microsoft.com/azure/foundry/concepts/general-availability",
    "https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets",
    "https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup",
    "https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot",
    "https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md",
]), transition="Return to Q&A.")

HERE.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
guide = ["# Slide-by-slide presenter notes\n", "Notes are also embedded in PowerPoint's Notes pane and Presenter View.\n"]
for number, title, body in notes_export:
    guide += [f"\n## Slide {number}: {title}\n", body + "\n"]
(HERE / "Presenter notes.md").write_text("\n".join(guide), encoding="utf-8")
print(f"Created {OUT} ({len(prs.slides)} slides, {sum(s._element.get('show') == '0' for s in prs.slides)} hidden)")
