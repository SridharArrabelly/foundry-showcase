"""Rebuild the showcase using the user's original Azure artwork and diagrams."""
import json
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
NOTES = json.loads((HERE / "slide_notes.json").read_text(encoding="utf-8"))
OUT = HERE / "Foundry - From prototype to operated service.pptx"
C = {
    "ink": "161616", "muted": "555B64", "azure": "0078D4", "navy": "2A446F",
    "blue": "005A9E", "pale": "E8F3FC", "white": "FFFFFF", "paper": "F5F4F2",
    "line": "D4DFE9", "green": "087A54", "green_pale": "E7F5EE",
    "red": "AD2927", "red_pale": "FCEDEC", "purple": "4F42FD",
}
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
prs.core_properties.title = "Microsoft Foundry: from prototype to operated service"
prs.core_properties.author = "Sridhar Arrabelly"
prs.core_properties.subject = "Volt & Co | GitHub Copilot SDK | Microsoft Foundry"
guide = []


def color(value):
    return RGBColor.from_string(C.get(value, value))


def shape(slide, kind, x, y, w, h, fill="white", line=None):
    item = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    item.fill.solid()
    item.fill.fore_color.rgb = color(fill)
    if line:
        item.line.color.rgb = color(line)
        item.line.width = Pt(1.2)
    else:
        item.line.fill.background()
    # Avoid theme-dependent shadows in the canvas and Office.
    item._element.spPr.append(OxmlElement("a:effectLst"))
    return item


def rect(slide, x, y, w, h, fill="white", line=None):
    return shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill, line)


def text(slide, value, x, y, w, h, size=22, ink="ink", bold=False, align=None, font="Segoe UI"):
    item = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = item.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    for i, line in enumerate(value.split("\n")):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.space_after = Pt(7)
        p.line_spacing = 1.08
        if align is not None:
            p.alignment = align
        run = p.add_run()
        run.text = line
        # Explicit run formatting is essential: the app renderer does not inherit
        # paragraph-level font size/color as native PowerPoint does.
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color(ink)
    return item


def arrow(slide, x1, y1, x2, y2, ink="azure", width=2):
    item = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
        Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    item.line.color.rgb = color(ink)
    item.line.width = Pt(width)
    tail = OxmlElement("a:tailEnd")
    tail.set("type", "triangle")
    item.line._get_or_add_ln().append(tail)
    return item


def circle(slide, value, x, y, fill="navy", diameter=.58):
    shape(slide, MSO_SHAPE.OVAL, x, y, diameter, diameter, fill)
    text(slide, value, x, y + .09, diameter, .34, 17, "white", True, PP_ALIGN.CENTER)


def image(slide, filename, x, y, w, h):
    path = ASSETS / filename
    with Image.open(path) as im:
        ratio = im.width / im.height
    height = min(h, w / ratio)
    width = height * ratio
    slide.shapes.add_picture(str(path), Inches(x + (w - width) / 2),
                             Inches(y + (h - height) / 2), Inches(width), Inches(height))


def header(title, eyebrow, subtitle=None, hidden=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, 13.333, 7.5, "paper")
    if hidden:
        s._element.set("show", "0")
    text(s, eyebrow, .65, .35, 12, .34, 15, "azure", True)
    text(s, title, .65, .95, 12.05, .95, 32, "ink", True)
    if subtitle:
        text(s, subtitle, .67, 1.95, 12.0, .56, 18, "muted")
    footer(s)
    return s


def footer(s, note="Volt & Co | Synthetic demonstration | Microsoft Foundry"):
    text(s, note, .66, 7.08, 11.6, .22, 10, "muted")
    text(s, f"{len(prs.slides):02}", 12.18, 7.02, .5, .3, 12, "navy", True)


def takeaway(s, value, y=6.28, fill="pale"):
    rect(s, .65, y, 12.0, .58, fill)
    text(s, value, .85, y + .12, 11.6, .36, 18, "navy", True)


def note(s, title, visual, extra=""):
    number = len(prs.slides)
    body = NOTES[number - 1]
    s.notes_slide.notes_text_frame.text = body
    guide.append((number, title, body))


def node(s, x, y, w, title, body, fill="white"):
    rect(s, x, y, w, 1.75, fill, "line")
    text(s, title, x + .17, y + .17, w - .34, .42, 21, "navy", True)
    text(s, body, x + .17, y + .71, w - .34, .85, 17, "ink")


def step_row(s, items, y=3.0):
    width = 12.0 / len(items)
    for i, (head, detail) in enumerate(items):
        x = .65 + i * width
        circle(s, str(i + 1), x + .12, y)
        if i < len(items) - 1:
            arrow(s, x + .78, y + .28, x + width - .1, y + .28, "line")
        text(s, head, x + .1, y + .83, width - .28, .56, 21, "navy", True)
        text(s, detail, x + .1, y + 1.55, width - .3, 1.0, 18)


def demo_label(s, number, time):
    rect(s, .65, 2.64, 1.8, .45, "navy")
    text(s, f"LIVE DEMO {number}", .8, 2.73, 1.48, .25, 13, "white", True)
    text(s, time, 2.7, 2.72, 4.2, .3, 15, "muted")


# 01: Original Bank Briefing artwork, not a recreated gradient.
s = prs.slides.add_slide(prs.slide_layouts[6])
s.shapes.add_picture(str(ASSETS / "azure-cover.png"), 0, 0, prs.slide_width, prs.slide_height)
text(s, "Microsoft Foundry", .65, 2.05, 6.35, .68, 34, "ink", True)
text(s, "From prototype\nto operated service", .65, 2.95, 6.35, 1.45, 37, "ink", True)
text(s, "Build with GitHub Copilot.\nRun, evaluate and improve in Foundry.", .68, 4.78, 6.0, .92, 22, "navy")
text(s, "Sridhar Arrabelly", .68, 6.14, 5.2, .38, 19, "ink", True)
text(s, "Customer deep dive + live demo  |  50 minutes + Q&A", .68, 6.65, 7.2, .33, 14)
note(s, "Microsoft Foundry: from prototype to operated service",
     "Original Azure title artwork from the Bank Briefing. Black text on the original light field. Explicit run-level font size and color.")

# 02: A connected sequence, using the Bank Briefing's operating-system framing.
s = header("One customer request. A complete operating story.",
           "The story", "Build quickly. Prove deliberately. Learn after release.")
step_row(s, [
    ("Build", "Copilot + code\nA useful assistant"),
    ("Connect", "Business tools\nCheckable facts"),
    ("Prove", "Cases + traces\nMeasured behaviour"),
    ("Release", "Version + evidence\nAn explicit gate"),
    ("Improve", "Observed failure\nA reviewed new test"),
], y=2.95)
takeaway(s, "The strength is in the connections—not the number of features we can show.")
note(s, "One customer request. A complete operating story.",
     "Flow layout and outcome-first wording adapted from Bank Briefing slide 4; replaces disconnected generic cards.")

# 03: Customer request + actual fictional products, not decorative feature boxes.
s = header("Meet Volt & Co", "One use case throughout",
           "A fictional electronics assistant that recommends the cheapest product that works.")
rect(s, .65, 2.78, 4.1, 2.78, "pale")
text(s, "“A charger for my\nVolt Book 14.\nUnder EUR 50.”", .93, 3.08, 3.5, 1.85, 28, "navy", True)
text(s, "The device requires 65W.", .93, 5.08, 3.5, .36, 17)
products = [
    ("Volt Charge 30", "30W", "EUR 19.90", "Underpowered", "red"),
    ("Volt Charge 65", "65W", "EUR 39.90", "Compatible + in budget", "green"),
    ("Volt Charge 100", "100W", "EUR 59.90", "Above budget", "muted"),
]
for i, (name, watts, price, outcome, ink) in enumerate(products):
    y = 2.86 + i * .98
    rect(s, 5.18, y, 7.47, .83, "white")
    text(s, name, 5.4, y + .12, 2.4, .35, 20, "ink", True)
    text(s, f"{watts}  |  {price}", 7.95, y + .12, 2.35, .35, 18, "muted")
    text(s, outcome, 10.25, y + .12, 2.2, .5, 16, ink, True)
takeaway(s, "Then the same customer asks about a recall. Missing evidence becomes the next test.")
note(s, "Meet Volt & Co",
     "Data-row layout follows Bank Briefing slides 3 and 8. Prices/specifications are the deployed synthetic fixtures—not original workshop results.")

# 04: The original two-loop artwork, preserving its actual diagram.
s = header("One continuous system: inner and outer loop", "The lifecycle",
           "Reference lifecycle: two loops, connected by versioned and reviewed evidence.")
image(s, "two-loops.png", .57, 2.53, 12.19, 4.27)
note(s, "One continuous system: inner and outer loop",
     "Actual diagram from workshop slide 12. Implementation filenames were shortened in the image for legibility.",
     "Treat the full diagram as the reference lifecycle. This live demo does not implement every box: DEV is local; the hosted serving environment is a demo project. Do not claim production isolation, Agent 365, a managed Toolbox or automated red teaming.")

# 05: Reuse the real Foundry architecture graphic with a focused demo-path rail.
s = header("Build in GitHub. Run and improve in Foundry.", "Architecture",
           "Copilot for development. Copilot SDK for runtime. Foundry for hosting and lifecycle.")
image(s, "build-and-host.png", .65, 2.68, 12.0, 3.28)
rect(s, .65, 6.24, 12.0, .59, "pale")
for x, label in [(1.0, "Inspect every run"), (5.0, "Score before release"), (9.0, "Learn from traffic")]:
    text(s, label, x, 6.37, 3.45, .35, 19, "navy", True)
note(s, "Build in GitHub. Run and improve in Foundry.",
     "Enlarged BUILD and HOST sections from the original workshop slide 23 architecture graphic.",
     "The graphic is the broader platform reference, not a claim that every shown integration is configured. Point specifically to Copilot SDK, hosted runtime, models, evaluation and tracing.")

# 06: Trace diagram for the live shopping request.
s = header("Watch the answer—and the path that produced it", "Live demo 1",
           "One request, three business checks, inspectable evidence.")
demo_label(s, "01", "09:00-16:00 | live request + trace")
node(s, .65, 3.58, 2.6, "Customer", "Volt Book 14\nBudget: EUR 50", "pale")
node(s, 3.8, 3.58, 2.6, "Catalog", "30W at EUR 19.90\n65W at EUR 39.90")
node(s, 6.95, 3.58, 2.6, "Compatibility", "Reject 30W\nConfirm 65W")
node(s, 10.1, 3.58, 2.55, "Answer", "Volt Charge 65\nEUR 39.90", "green_pale")
for x in [3.3, 6.45, 9.6]:
    arrow(s, x, 4.43, x + .38, 4.43)
rect(s, 3.8, 5.65, 8.85, .55, "pale")
text(s, "The trace links the request, tool arguments, returned facts and response.", 4.0, 5.78, 8.43, .34, 17, "navy")
text(s, "Next: explaining one execution is not the same as proving consistent behaviour.",
     .72, 6.52, 11.9, .38, 17, "navy", True)
note(s, "Watch the answer—and the path that produced it",
     "Editable request-to-tool sequence. This is a diagram, not a fabricated portal screenshot. Exact commands remain in the speaker notes.")

# 07: Actual nine-case comparison, visually encoded without claiming benchmark accuracy.
s = header("From a convincing answer to measurable evidence", "Evaluate",
           "Recorded rehearsal: the same nine synthetic cases, compared across two versions.")
for row, (label, passed, badge, fill) in enumerate([
    ("Baseline · version 2", 7, "BLOCK", "red"),
    ("Corrected · version 4", 9, "PASS", "green"),
]):
    y = 2.98 + row * 1.4
    text(s, label, .72, y + .09, 3.3, .5, 24, "navy", True)
    for i in range(9):
        rect(s, 4.4 + i * .58, y, .43, .64, "green" if i < passed else "red_pale")
        text(s, "+" if i < passed else "-", 4.4 + i * .58, y + .15, .43, .3,
             16, "white" if i < passed else "red", True, PP_ALIGN.CENTER)
    text(s, f"{passed}/9", 10.0, y - .02, 1.25, .6, 32, fill, True)
    text(s, badge, 11.45, y + .13, 1.1, .4, 17, fill, True)
text(s, "The two failed cases both omitted the batch code.", .75, 5.74, 11.7, .45, 22, "ink", True)
takeaway(s, "Small synthetic-case results—not a population accuracy estimate or safety certification.")
note(s, "From a convincing answer to measurable evidence",
     "Chart uses the actual baseline and candidate reports (7/9 versus 9/9). It does not import results from other agents.",
     "Do not translate this into a percentage accuracy claim. The model-judged coherence scorecard is a separate measurement.")

# 08: Clean editorial lanes following the Bank Briefing text treatments.
s = header("Three checks. Three different jobs.", "Define what good means",
           "Use deterministic checks, model judges and human review together.")
for i, (head, sub, rows) in enumerate([
    ("Code-based", "Objective business assertions", ["Correct product and batch", "Required tool evidence", "Missing-input contract"]),
    ("Model-based", "Native Foundry scorecard", ["Coherence of captured answers", "A semantic quality signal", "Not domain correctness"]),
    ("Human", "Expected behaviour and acceptance", ["Ambiguous or risky cases", "Validate the labels", "Approve the release policy"]),
]):
    x = .65 + i * 4.12
    rect(s, x, 2.87, 3.75, .66, "navy")
    text(s, head, x + .18, 3.02, 3.37, .4, 23, "white", True)
    text(s, sub, x + .04, 3.83, 3.66, .72, 20, "blue", True)
    text(s, "\n".join(rows), x + .04, 4.78, 3.64, 1.17, 18)
takeaway(s, "No single score can establish usefulness, correctness and safety for every case.")
note(s, "Three checks. Three different jobs.",
     "Text hierarchy and status-lane layout adapted from Bank Briefing slide 8; evaluator logic from workshop slide 86.")

# 09: Before/after code contract, not another dark title card.
s = header("Change the contract—not just the wording", "Live demo 2",
           "“I have a Volt Charge 65. Is it safe?”")
demo_label(s, "02", "18:00-25:00 | baseline, correction, comparison")
for x, head, value, detail, fill, ink in [
    (.65, "BEFORE", "batch = null\nstatus = no_recall", "Missing evidence was treated\nas a negative lookup.", "red_pale", "red"),
    (7.15, "AFTER", "batch = null\nstatus = needs_batch", "Ask for the batch before\nmaking a recall conclusion.", "green_pale", "green"),
]:
    rect(s, x, 3.5, 5.5, 2.18, fill)
    text(s, head, x + .24, 3.7, 5.0, .34, 15, ink, True)
    text(s, value, x + .24, 4.22, 5.0, 1.1, 23, "ink", font="Cascadia Code")
    text(s, detail, x + .06, 5.87, 5.4, .8, 20, ink, True)
arrow(s, 6.3, 4.52, 6.99, 4.52, "navy", 3)
note(s, "Change the contract—not just the wording",
     "Readable before/after visualization of the actual tool defect and fix. Exact code and results are in the demo; this slide is not a terminal screenshot.")

# 10: Original release diagram, prominently labelled as the production reference.
s = header("How a candidate becomes an operated service", "The outer loop",
           "Reference pattern: rebuild, gate and promote—then learn from operation.")
image(s, "release-bridge.png", .6, 2.63, 12.12, 3.85)
text(s, "Our demo: local DEV + a hosted DEMO target. The approved client pins the evaluated version.",
     .72, 6.58, 11.95, .38, 16, "blue", True)
note(s, "How a candidate becomes an operated service",
     "Actual outer-loop bridge diagram from workshop slide 162. Its DEV/PROD labels describe the reference production pattern.",
     "The caption explicitly distinguishes the deployed demo from production isolation. Do not claim that a passing local score changes the portal's default routing.")

# 11: Real release evidence as a document flow.
s = header("A release we can explain", "Live demo 3",
           "Show the actual Actions run and the evidence attached to the candidate.")
demo_label(s, "03", "27:00-34:00 | gate + deployed version")
step_row(s, [
    ("Source", "Git revision\nConfiguration"),
    ("Evidence", "Dataset hashes\nCase results"),
    ("Decision", "9/9 criteria pass\nExplicit acceptance"),
    ("Serving", "volt-assistant:4\nPinned demo client"),
], y=3.42)
takeaway(s, "Deployment and long-running scoring were completed in rehearsal—not silently simulated.")
note(s, "A release we can explain",
     "Document-flow layout from the Bank Briefing's worked scenario. Uses the real version 4 release and live workflow, not generic success badges.")

# 12: Original continuous-improvement illustration.
s = header("Operations teaches development what to test", "Observe, evaluate, improve",
           "The next learning cycle starts with evidence from a real interaction.")
image(s, "observe-improve.png", .6, 2.65, 12.12, 3.75)
text(s, "In this session: a synthetic hosted-agent request becomes a reviewed regression case.",
     .72, 6.58, 11.95, .36, 17, "blue", True)
note(s, "Operations teaches development what to test",
     "Original lifecycle illustration from workshop slide 67.",
     "The diagram describes the broader platform loop; Insights and Agent Optimizer are not live dependencies in this implementation. Our actual path is capture, review, add a test, fix and re-evaluate.")

# 13: Loop closure with an actual request and artefacts.
s = header("Close the loop with one new test", "Live demo 4",
           "Observed output is evidence. It is not automatically a correct label.")
demo_label(s, "04", "35:00-47:00 | trace to reviewed case to corrected candidate")
node(s, .65, 3.56, 3.4, "Observe", "No batch supplied.\nBaseline returned no_recall.", "red_pale")
node(s, 4.97, 3.56, 3.4, "Review", "Expected: ask for the batch.\nKeep the source trace ID.", "pale")
node(s, 9.27, 3.56, 3.38, "Prove", "Run the new regression.\nCorrected version passes.", "green_pale")
arrow(s, 4.15, 4.43, 4.8, 4.43)
arrow(s, 8.47, 4.43, 9.1, 4.43)
arrow(s, 10.97, 5.7, 2.35, 5.7, "navy")
text(s, "Return to DEV with a stronger contract—not a direct patch to the serving prompt.",
     1.22, 6.06, 10.9, .7, 21, "navy", True, PP_ALIGN.CENTER)
note(s, "Close the loop with one new test",
     "Editable feedback-loop diagram anchored in the captured missing-batch case.")

# 14: Four takeaways, paired with the original Azure artwork.
s = prs.slides.add_slide(prs.slide_layouts[6])
s.shapes.add_picture(str(ASSETS / "azure-cover.png"), 0, 0, prs.slide_width, prs.slide_height)
text(s, "One system. Four things to remember.", .65, 1.92, 7.0, 1.05, 32, "ink", True)
for i, value in enumerate([
    "Start with a customer outcome.",
    "Prove the path, not just the prose.",
    "Make the release decision explicit.",
    "Turn observations into reviewed tests.",
]):
    y = 3.26 + i * .7
    circle(s, str(i + 1), .68, y, diameter=.47)
    text(s, value, 1.42, y + .04, 6.35, .57, 22, "ink", True)
note(s, "One system. Four things to remember.",
     "Reuses the original Bank Briefing Azure artwork. Large black text stays on the light side of the composition.")

# 15: Reference-style closing, not a third set of identical cards.
s = prs.slides.add_slide(prs.slide_layouts[6])
s.shapes.add_picture(str(ASSETS / "azure-cover.png"), 0, 0, prs.slide_width, prs.slide_height)
text(s, "Thank you", .65, 2.12, 6.6, .7, 38, "ink", True)
text(s, "Which customer journey would you\nput through this loop?", .65, 3.24, 6.5, 1.2, 28, "navy")
text(s, "Outcome  ·  Boundaries  ·  Ownership", .68, 4.94, 6.4, .52, 21, "ink", True)
text(s, "Sridhar Arrabelly\nQ&A | 50:00-60:00", .68, 6.03, 6.0, .75, 18)
note(s, "Thank you / Q&A", "Original Bank Briefing closing-slide visual language and artwork.")

# 16-20: Hidden Q&A references.
s = header("What is implemented—and what is not", "Appendix | implementation boundaries", hidden=True)
for x, head, rows, ink in [
    (.65, "Implemented", ["Copilot SDK + Foundry model", "Hosted Invocations endpoint", "Three read-only domain tools", "Traces + evaluations + release evidence"], "blue"),
    (7.05, "Not claimed", ["Managed Toolbox or APIM", "Customer production isolation", "Autonomous self-correction", "Safety certification or measured ROI"], "muted"),
]:
    text(s, head, x, 2.74, 5.55, .55, 25, ink, True)
    for i, row in enumerate(rows):
        rect(s, x, 3.56 + i * .65, 5.55, .53, "white")
        text(s, row, x + .16, 3.66 + i * .65, 5.22, .38, 19)
takeaway(s, "A compact demo is valuable when its claims and boundaries are precise.")
note(s, "What is implemented—and what is not", "Bank Briefing's two-column editorial treatment; no repetitive rounded cards.")

s = header("Availability is capability-specific", "Appendix | checked 8 November 2026",
           "Portal, API, evaluator and region readiness can differ.", hidden=True)
availability = [
    ("Hosted agents; prompt/hosted tracing", "GA core", "green"),
    ("Core evaluations; managed Toolbox", "GA core*", "green"),
    ("Monitor; Insights; trace-to-dataset", "Preview", "blue"),
    ("Agent guardrails and intervention", "Preview", "blue"),
    ("Agent Optimizer", "Limited preview", "blue"),
]
for i, (feature, status, ink) in enumerate(availability):
    y = 2.75 + i * .62
    rect(s, .65, y, 12, .53, "white")
    text(s, feature, .85, y + .1, 8.6, .35, 20)
    text(s, status, 9.7, y + .1, 2.75, .35, 19, ink, True)
text(s, "* Check individual tools and evaluators. Reconfirm current availability before customer commitments.",
     .72, 6.25, 11.9, .68, 16, "muted")
note(s, "Availability is capability-specific", "Status-table design follows the Bank Briefing, but uses the current checked status—not its historical September status claims.")

s = header("The broader agent platform", "Appendix | platform reference", hidden=True)
image(s, "agent-platform.png", .65, 1.96, 12.0, 4.9)
note(s, "The broader agent platform", "Enlarged original platform graphic from workshop slide 22. Broader capabilities are explicitly labelled as a reference; the ownership discussion remains in the notes.")

s = header("When a live step takes too long", "Appendix | shortened path",
           "Keep the evidence bridges. Cut the waiting, not the story.", hidden=True)
step_row(s, [
    ("Keep live", "One useful request\nOne focused correction"),
    ("Use captures", "Actual version + timestamp\nCompleted scorecards"),
    ("Preserve", "Trace → reviewed test\nThe return to DEV"),
], y=3.08)
takeaway(s, "Say “recorded rehearsal evidence”—never present a fixture as a live model result.")
note(s, "When a live step takes too long", "Shortened-path timeline matches the main narrative; readable black text on light backgrounds.")

s = header("Sources and useful boundaries", "Appendix | provenance",
           "The story, graphics and live evidence each have an explicit source.", hidden=True)
sources = [
    ("Workshop", "Volt & Co, inner/outer-loop diagrams, platform architecture and lifecycle."),
    ("Bank Briefing", "Original Azure artwork, light layouts, typography hierarchy and editorial style."),
    ("This project", "Actual version 2 / version 4 results, traces, GitHub workflow and release record."),
    ("Official documentation", "Current product, SDK, API and preview/GA boundaries; links in the notes."),
]
for i, (title, body) in enumerate(sources):
    y = 2.73 + i * .82
    text(s, title, .73, y, 2.75, .5, 21, "blue", True)
    text(s, body, 3.62, y, 8.85, .67, 19)
takeaway(s, "No NDA roadmap pages. No other agent's screenshots presented as Volt results.")
note(s, "Sources and useful boundaries",
     "Visual provenance is recorded in presentation/assets/PROVENANCE.md. Complex original diagrams are high-resolution images; all surrounding text and new diagrams remain editable.")

for number, page in enumerate(prs.slides, 1):
    for item in page.shapes:
        if item.has_text_frame:
            for paragraph in item.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.text and (run.font.size is None or run.font.color.type is None):
                        raise ValueError(f"Slide {number}: explicit run size/color required for canvas rendering")
prs.save(OUT)
lines = ["# Slide-by-slide presenter notes\n",
         "Visual rebuild: original Azure artwork and workshop diagrams, with explicit run formatting for canvas readability.\n"]
for number, title, body in guide:
    lines += [f"\n## Slide {number}: {title}\n", body + "\n"]
(HERE / "Presenter notes.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Rebuilt {OUT}: {len(prs.slides)} slides, 5 hidden, original artwork + diagrams.")
