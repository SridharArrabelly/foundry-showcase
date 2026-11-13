"""Build the current workshop from the unchanged user-supplied reference deck."""
from copy import deepcopy
from pathlib import Path
import re
import zipfile

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import parse_xml
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = Path(__file__).parent
SOURCE = Path(r"C:\Users\sarrabelly\OneDrive - Microsoft\00FY27\AI Roadshow FY27\Foundry Agent Platform Workshop v1.0.0.pptx")
OUTPUT = ROOT / "Volt & Co - Governed and improving agents.pptx"
PURPLE, AZURE, INK = "5230BC", "0078D4", "201B36"
VIOLET, PALE, TEAL, WHITE, MUTED = "EDE7FE", "F5F7FC", "087D87", "FFFFFF", "4F5265"
FONT = "Segoe UI"


def inch(v):
    return Inches(v)


def add_text(slide, text, x, y, w, h, size=20, color=INK, bold=False,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    shape = slide.shapes.add_textbox(inch(x), inch(y), inch(w), inch(h))
    tf = shape.text_frame
    tf.clear()
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = valign
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(5)
        p.line_spacing = 1.08
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(color)
    return shape


def rect(slide, x, y, w, h, fill=WHITE, line=None, radius=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        inch(x), inch(y), inch(w), inch(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line:
        shape.line.color.rgb = RGBColor.from_string(line)
        shape.line.width = Pt(1.3)
    else:
        shape.line.fill.background()
    if radius:
        shape.adjustments[0] = 0.06
    return shape


def line(slide, x1, y1, x2, y2, color=PURPLE, width=2.2, arrow=False):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, inch(x1), inch(y1), inch(x2), inch(y2))
    shape.line.color.rgb = RGBColor.from_string(color)
    shape.line.width = Pt(width)
    if arrow:
        tail = OxmlElement("a:tailEnd")
        tail.set("type", "triangle")
        tail.set("w", "sm")
        tail.set("len", "sm")
        shape.line._get_or_add_ln().append(tail)
    return shape


def circle(slide, text, x, y, diameter=.44, fill=PURPLE, size=15):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, inch(x), inch(y), inch(diameter), inch(diameter))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(fill)
    s.line.fill.background()
    add_text(slide, text, x, y + .02, diameter, diameter - .02, size, WHITE, True,
             PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)


def chip(slide, text, x, y, w, fill=VIOLET, color=PURPLE, size=12):
    rect(slide, x, y, w, .34, fill, radius=True)
    add_text(slide, text, x + .08, y + .055, w - .16, .23, size, color, True)


def footer(slide, n, chapter, preview=None):
    add_text(slide, f"VOLT & CO  /  {chapter.upper()}", .5, 7.08, 10.8, .22, 10.5, MUTED)
    number = add_text(slide, f"{n:02}", 12.35, 7.04, .48, .25, 12, PURPLE, True, PP_ALIGN.RIGHT)
    number.name = "Workshop slide number"
    if preview:
        chip(slide, preview, 10.0, .28, 2.82, size=10.5)


def title(slide, text, subtitle="", n=None, chapter="", preview=None):
    add_text(slide, text, .5, .52, 12.3, .72, 34, INK, True)
    if subtitle:
        add_text(slide, subtitle, .5, 1.3, 12.2, .5, 16, PURPLE)
    if n:
        footer(slide, n, chapter, preview)


def clear(slide):
    for shape in list(slide.shapes):
        slide.shapes._spTree.remove(shape._element)
    for tag in ["p:timing", "p:transition"]:
        for el in list(slide._element.findall(tag, slide._element.nsmap)):
            slide._element.remove(el)


def get(slide, sid):
    return next(s for s in slide.shapes if s.shape_id == sid)


def remove(slide, *ids):
    for s in list(slide.shapes):
        if s.shape_id in ids:
            slide.shapes._spTree.remove(s._element)


def replace(slide, sid, text, size=None, color=None, bold=None):
    s = get(slide, sid)
    old = next((r for p in s.text_frame.paragraphs for r in p.runs if r.text.strip()), None)
    rpr = deepcopy(old._r.rPr) if old is not None and old._r.rPr is not None else None
    s.text_frame.clear()
    for i, part in enumerate(text.split("\n")):
        p = s.text_frame.paragraphs[0] if i == 0 else s.text_frame.add_paragraph()
        r = p.add_run()
        r.text = part
        if rpr is not None:
            r._r.insert(0, deepcopy(rpr))
        r.font.name = FONT
        if size is not None:
            r.font.size = Pt(size)
        elif r.font.size is None:
            r.font.size = Pt(16)
        if color is not None:
            r.font.color.rgb = RGBColor.from_string(color)
        elif r.font.color.type is None:
            r.font.color.rgb = RGBColor.from_string(INK)
        if bold is not None:
            r.font.bold = bold
    return s


def restyle_source(slide):
    """Keep source colors and hierarchy, explicitly name fonts on every run."""
    def walk(shapes):
        for shape in shapes:
            if hasattr(shape, "shapes"):
                walk(shape.shapes)
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = FONT
    walk(slide.shapes)


def notes(slide, manuscript):
    ns = slide.notes_slide
    tree = ns._element.find("p:cSld/p:spTree", ns._element.nsmap)
    for child in list(tree):
        if etree.QName(child).localname not in ["nvGrpSpPr", "grpSpPr"]:
            tree.remove(child)
    sp = parse_xml(
        b'<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        b'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        b'<p:nvSpPr><p:cNvPr id="2" name="Presenter manuscript"/><p:cNvSpPr/>'
        b'<p:nvPr><p:ph type="body" idx="13"/></p:nvPr></p:nvSpPr><p:spPr/>'
        b'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')
    tree.append(sp)
    tf = ns.notes_text_frame
    tf.text = manuscript
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor.from_string(INK)


def prune_slide(slide):
    # Removed screenshots/audio must not remain as unused package attachments.
    for node in list(slide._element.iter()):
        if etree.QName(node).localname in ["hlinkClick", "hlinkMouseOver"]:
            node.getparent().remove(node)
    used = set()
    for node in slide._element.iter():
        for k, v in node.attrib.items():
            if k.startswith("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"):
                used.add(v)
    for rid, rel in list(slide.part.rels.items()):
        if rid not in used and rel.reltype.rsplit("/", 1)[-1] not in ["slideLayout", "notesSlide"]:
            slide.part.drop_rel(rid)
    for rid, rel in list(slide.notes_slide.part.rels.items()):
        if rel.reltype.rsplit("/", 1)[-1] not in ["notesMaster", "slide"]:
            slide.notes_slide.part.drop_rel(rid)



STAGES = ["BUILD", "PROVE", "RELEASE", "OPERATE", "IMPROVE"]
TITLES = [
    "Can we defend this release?", "One agent. Two loops. Four demonstrations.",
    "Two loops. One improving service.", "One customer. One accountable answer.",
    "The harness runs the loop. We own the contract.", "Where Citadel and Foundry meet",
    "Demo 1 · Build and inspect", "A useful answer is only the beginning.",
    "Three ways to judge the same behavior", "Name the boundary. Show its evidence.",
    "Optimization is an experiment, not a promise.", "Demo 2 · Prove the contract",
    "Bridge 1 · Candidate + evidence + approval", "A case file you can reopen",
    "Demo 3 · Inspect the release gate", "The release passed. The contract missed something.",
    "Observe the request, not just the aggregate.", "Bridge 2 · A finding becomes a test",
    "Demo 4 · Turn the finding into a repair", "The architecture decisions we can explain",
    "Your next POC: one decision, one evidence chain.", "Useful. Defensible. Improving.",
    "Memory is a separate, narrow experiment.", "Identity follows responsibility.",
]


def tracker(slide, current):
    for index, stage in enumerate(STAGES):
        x = .5 + index * 2.48
        chip(slide, stage, x, 6.69, 2.25,
             PURPLE if stage == current else PALE,
             WHITE if stage == current else MUTED, 11)


def cards(slide, number, subtitle, entries, stage=None, status=None):
    clear(slide)
    title(slide, TITLES[number - 1], subtitle, number, stage or "The workshop", status)
    if number in (9, 14, 20, 21, 22):
        if number == 22:
            rect(slide, .5, 2.05, 12.33, 4.42, INK, radius=True)
        for index, (heading, text) in enumerate(entries):
            y = 2.2 + index * 1.4
            color = (PURPLE, AZURE, TEAL)[index]
            if number != 22:
                rect(slide, .5, y, 12.33, 1.16, VIOLET if index == 0 else PALE, radius=True)
            circle(slide, str(index + 1), .78, y + .24, .52, color, 18)
            add_text(slide, heading, 1.6, y + .2, 3.2, .9, 24,
                     WHITE if number == 22 else color, True)
            add_text(slide, text, 5.0, y + .19, 7.45, .8, 21,
                     WHITE if number == 22 else INK)
        if stage:
            tracker(slide, stage)
        return
    width = (12.33 - .35 * (len(entries) - 1)) / len(entries)
    for index, (heading, text) in enumerate(entries):
        x = .5 + index * (width + .35)
        rect(slide, x, 2.25, width, 3.78, VIOLET if index == 0 else WHITE,
             PURPLE if index != 2 else TEAL, True)
        circle(slide, str(index + 1), x + .24, 2.52, .43, PURPLE)
        add_text(slide, heading, x + .25, 3.19, width - .5, .95, 25, INK, True)
        add_text(slide, text, x + .25, 4.27, width - .5, 1.42, 19, MUTED)
    if stage:
        tracker(slide, stage)


def demo(slide, number, which, question, mode, steps, back, stage):
    clear(slide)
    chip(slide, f"DEMO {which} · LEAVE THE SLIDES", .5, .5, 5, PURPLE, WHITE, 14)
    add_text(slide, TITLES[number - 1].split(" · ", 1)[1], .5, 1.18, 12.0, .8, 39, INK, True)
    add_text(slide, mode, .5, 2.08, 12.0, .42, 14, PURPLE, True)
    rect(slide, .5, 2.85, 5.7, 2.75, INK, radius=True)
    add_text(slide, question, .85, 3.45, 5.0, 1.7, 31, WHITE, True)
    for index, (head, detail) in enumerate(steps):
        y = 2.83 + index * .98
        circle(slide, str(index + 1), 6.72, y + .02, .44, PURPLE, 15)
        add_text(slide, head, 7.4, y, 5, .43, 22, INK, True)
        add_text(slide, detail, 7.4, y + .46, 5, .45, 17, MUTED)
    rect(slide, .5, 5.99, 12.33, .57, TEAL, radius=True)
    add_text(slide, f"RETURN TO SLIDE {back:02} · Debrief before the next question",
             .78, 6.13, 11.8, .33, 18, WHITE, True)
    tracker(slide, stage)
    footer(slide, number, f"Demo {which}")


def make_deck():
    prs = Presentation(SOURCE)
    selected = {i: prs.slides[i - 1] for i in [1, 15, 6, 159]}
    layout = selected[159].slide_layout
    content = {}
    for n in range(1, 25):
        content[n] = selected[{1: 1, 3: 15, 6: 6}[n]] if n in (1, 3, 6) else prs.slides.add_slide(layout)
    ids = {prs.part.related_part(item.rId): item for item in prs.slides._sldIdLst}
    keep = {slide.part for slide in content.values()}
    for item in list(prs.slides._sldIdLst):
        if prs.part.related_part(item.rId) not in keep:
            prs.part.drop_rel(item.rId)
        prs.slides._sldIdLst.remove(item)
    for n, slide in content.items():
        prs.slides._sldIdLst.append(ids[slide.part])
        slide._element.set("show", "0" if n > 22 else "1")
        restyle_source(slide)
        for tag in ("p:timing", "p:transition"):
            for element in list(slide._element.findall(tag, slide._element.nsmap)):
                slide._element.remove(element)
    s = content[1]
    clear(s)
    add_text(s, "VOLT & CO / MICROSOFT FOUNDRY + CITADEL", .5, 1.6, 11, .45, 17, PURPLE, True)
    add_text(s, "Can we defend\nthis release?", .5, 2.42, 11.6, 1.8, 48, INK, True)
    add_text(s, "One customer. Two loops. Evidence at every handoff.", .5, 4.55, 11.5, .6, 24, PURPLE)
    add_text(s, "80 minutes of content + 10 minutes Q&A", .5, 5.2, 10, .4, 17, MUTED)
    s = content[2]
    clear(s)
    title(s, TITLES[1], "Follow the lifecycle—not a catalogue of features.", 2, "Run of show")
    agenda = [("00–10", "WHY + THE SYSTEM", "A trust question; two loops and two bridges"),
              ("10–25", "DEMO 1 · BUILD", "Hosted agent, Toolbox, IQ, gateway and trace"),
              ("25–40", "DEMO 2 · PROVE", "Business evidence, judges, controls and optimization"),
              ("40–50", "DEMO 3 · RELEASE", "Candidate, case file and approval boundary"),
              ("50–70", "OPERATE → DEMO 4 · IMPROVE", "A real escaped claim becomes a regression"),
              ("70–90", "DECISIONS + NEXT POC + Q&A", "Ten minutes reserved for your questions")]
    for i, (clock, head, detail) in enumerate(agenda):
        y = 2.05 + i * .72
        chip(s, clock, .5, y, 1.45, PURPLE, WHITE, 13)
        add_text(s, head, 2.2, y - .02, 4.2, .4, 18, INK, True)
        add_text(s, detail, 6.55, y, 6.0, .55, 17, MUTED)
    s = selected[15]
    replace(s, 2, "Two loops. One improving service.", 32, INK, True)
    replace(s, 4, "Build and prove in DEV. Release and learn in production-like DEMO.", 16, PURPLE)
    replacements = {
        7: "BRIDGE 1 · HANDOFF",
        8: "DEV   →   CANDIDATE + EVIDENCE   →   DEMO",
        9: "Code · tools · knowledge · tests · policy",
        14: "INNER LOOP · BUILD & PROVE",
        18: "Connect tools + policy.",
        22: "Inspect one execution.",
        26: "Test correctness + safety.",
        30: "Compare held-out cases.",
        38: "Same tests",
        45: "OUTER LOOP · RELEASE & LEARN",
        49: "Gate the exact candidate.",
        53: "Verify the serving version.",
        57: "Watch requests + failures.",
        60: "Learn & improve",
        61: "Review the next test case.",
        64: "BRIDGE 2 · FEEDBACK",
        65: "DEMO   →   HUMAN REVIEW   →   DEV",
        66: "Reviewed traces become new regression tests.",
    }
    for sid, txt in replacements.items():
        replace(s, sid, txt)
    for sid in [7, 64]:
        replace(s, sid, get(s, sid).text, 12, bold=True)
    for sid, y, h, size in [
        (8, 1.96, .31, 17), (9, 2.28, .26, 15),
        (65, 5.86, .32, 17), (66, 6.2, .28, 15),
        (14, 2.78, .3, 15), (45, 2.78, .3, 15),
    ]:
        shape = replace(s, sid, get(s, sid).text, size)
        shape.top, shape.height = inch(y), inch(h)
    for headings, bodies in [
        ([17, 21, 25, 29], [18, 22, 26, 30]),
        ([48, 52, 56, 60], [49, 53, 57, 61]),
    ]:
        for i, (head, body) in enumerate(zip(headings, bodies)):
            heading = replace(s, head, get(s, head).text, 17, bold=True)
            supporting = replace(s, body, get(s, body).text, 15)
            heading.top, heading.height = inch(3.2 + i * .58), inch(.29)
            supporting.top, supporting.height = inch(3.5 + i * .58), inch(.26)
    for i, sid in enumerate([34, 35, 36]):
        shape = replace(s, sid, get(s, sid).text, 14, bold=True)
        shape.top, shape.height = inch(3.5 + i * .26), inch(.25)
    for i, sid in enumerate([37, 38, 39, 40]):
        shape = replace(s, sid, get(s, sid).text, 15)
        shape.top, shape.height = inch(4.39 + i * .29), inch(.27)
    replace(s, 67, "Source workshop lifecycle diagram · adapted for synthetic DEV / DEMO", 10, MUTED)
    # Keep the source artwork and both bridges; enlarge the shortened text for projection.
    footer(s, 3, "The lifecycle")

    s = selected[6]
    replace(s, 6, "Where Citadel and Foundry meet", 32, AZURE, True)
    replace(s, 9, "Architecture context  ·  Identity  ·  Owner  ·  Telemetry")
    replace(s, 11, "LAYER 2 · AGENT OPERATIONS\nBuild → Host → Evaluate → Improve")
    replace(s, 15, "Volt agent")
    replace(s, 17, "Policy")
    replace(s, 24, "A2A", 11)
    replace(s, 31, "GOVERNED\nCAPABILITIES", 10.6)
    replace(s, 32, "Approved model")
    replace(s, 33, "Volt MCP tools")
    replace(s, 34, "A2A · context")
    replace(s, 36, "LAYER 4 · SECURITY FOUNDATION · SEPARATE ENABLEMENT")
    get(s, 36).width = inch(10.2)
    replace(s, 37, "MICROSOFT DEFENDER\nArchitecture context—not enabled by this diagram")
    remove(s, 46)
    add_text(s, "Focus today: governed model/tool access + agent operations. Other layers are architecture context.",
             .65, 1.21, 12.0, .4, 15, PURPLE)
    footer(s, 6, "Architecture reference")


    cards(content[4], 4, "VC-10482 · Volt Charge 65 · CH-0722 · synthetic data",
          [("Business facts", "Order, exact batch and replacement eligibility."),
           ("Policy evidence", "An identifiable replacement policy and recall notice."),
           ("Responsible answer", "Assessment advice—not a ticket, refund or shipment.")], "BUILD")
    cards(content[5], 5, "Start with the managed path; choose hosted when application-owned logic matters.",
          [("Managed harness", "The platform owns orchestration and supported execution."),
           ("Our hosted choice", "Agent Framework + Responses. Code enforces the business contract."),
           ("Copilot's role", "Development assistant. The same review and release gate applies.")], "BUILD")
    demo(content[7], 7, 1, "Can we explain how this answer was produced?",
         "15–25 MIN · FRESH REQUEST + IDENTIFIED TRACE",
         [("Ask", "Terminal · pinned released version"),
          ("Follow", "Foundry · tools, IQ and actual spans"),
          ("Inspect", "Two code regions, not a repository tour")], 8, "BUILD")
    cards(content[8], 8, "BACK FROM DEMO 1 · Configuration is not execution evidence.",
          [("Useful", "The request reaches facts and policy."),
           ("Inspectable", "The response identifies the executed path."),
           ("Still unproven", "Did the answer preserve the business meaning?")], "PROVE")
    cards(content[9], 9, "One metric cannot answer every quality question.",
          [("Code", "Expected outcome + request-bound tool results + schema and references."),
           ("Model rubric", "Does the prose claim an action that never happened?"),
           ("Human", "Review expectations, ambiguous wording and real incidents.")], "PROVE")
    cards(content[10], 10, "Keep access, content safety and business correctness distinct.",
          [("Verified evidence", "Routed utility and a recorded input-marker content_filter block."),
           ("Local v2 contract", "Tool-derived decision and constrained no-action wording before streaming."),
           ("Separate activation", "Tool-boundary policy and bounded red-team scan need approval and proof.")], "PROVE")
    cards(content[11], 11, "Completed prior experiment · preview · no candidate applied",
          [("Bounded search", "Instruction-only; separate training and validation sets."),
           ("Actual outcome", "Baseline 0.75 retained. No accepted improvement."),
           ("Review decision", "Job success alone proves neither a quality gain nor release readiness.")], "PROVE")
    demo(content[12], 12, 2, "What does a passing test actually establish?",
         "31–40 MIN · NATIVE V1 HISTORY + LOCAL V2 CONTRACT",
         [("Compare", "Historical 8/9 → 9/9 was a prompt repair"),
          ("Challenge", "Expected outcome AND observed evidence"),
          ("Enforce", "Local Responses tests; cloud v2 pending")], 13, "PROVE")
    cards(content[13], 13, "BACK FROM DEMO 2 · Bridge 1 carries an identifiable candidate.",
          [("Package once", "Commit + instructions + dependencies + ZIP digest."),
           ("Evaluate", "Fresh pinned responses; native business and calibrated action gates."),
           ("Approve", "Protected environment; same artifact; independent DEMO verification.")], "RELEASE")
    cards(content[14], 14, "The badge is the verdict. The case file explains it.",
          [("Identity", "Versioned source, package, agent, Toolbox, dataset and grader."),
           ("Behavior", "Case outcomes, rubric reasons and failure evidence."),
           ("Release", "Approval + promotion receipt + serving hash + fresh post-run.")], "RELEASE")
    demo(content[15], 15, 3, "Could another engineer defend this release?",
         "43–50 MIN · IMPLEMENTED WORKFLOW; CLOUD ACTIVATION PENDING",
         [("Open", "Workflow and explicit activation controls"),
          ("Inspect", "Actual historical case file—not v2 proof"),
          ("Decide", "No live pass or approval is invented")], 16, "RELEASE")
    s = content[16]
    clear(s)
    title(s, TITLES[15], "BACK FROM DEMO 3 · Recorded released DEMO v1", 16, "Operate")
    rect(s, .5, 2.1, 3.0, 3.9, PURPLE, radius=True)
    add_text(s, "9 / 9", .8, 2.7, 2.4, .9, 54, WHITE, True)
    add_text(s, "Historical business\ncases passed", .8, 4.05, 2.4, 1.3, 24, WHITE)
    add_text(s, "“I'm escalating this\nto human support.”", 4.1, 2.4, 8.3, 1.55, 36, INK, True)
    add_text(s, "There is no handoff tool.\nThe answer claims more than the tools performed.",
             4.1, 4.45, 8.2, 1.15, 24, TEAL, True)
    tracker(s, "OPERATE")
    cards(content[17], 17, "The escaped claim has a matching saved response ID and a 43-span trace.",
          [("Actual observation", "Released DEMO response + correlated App Insights export."),
           ("Missing criterion", "V1 checked decisions, tools and references, but missed action claims."),
           ("Future monitor", "Sampled continuous evaluation is not yet configured.")], "OPERATE")
    cards(content[18], 18, "Operation supplies evidence. A reviewer supplies the expectation.",
          [("Inspect", "Keep the original answer, tool evidence and version identity."),
           ("Annotate", "No handoff occurred. Advice is not execution."),
           ("Regress", "Add the escalation case and action rubric; show the old capture fail.")], "IMPROVE")
    demo(content[19], 19, 4, "What did operation teach us to test?",
         "60–70 MIN · REAL RECORDED FINDING + LOCAL FAIL/FIX/PASS",
         [("Find", "Same response, trace and reviewed expectation"),
          ("Repair", "Copilot-assisted diff + real host-stream test"),
          ("Return", "Cloud proof awaits approval")], 20, "IMPROVE")
    cards(content[20], 20, "BACK FROM DEMO 4 · One reason for each architectural choice.",
          [("Application", "Hosted Responses; request-bound decision renderer; read-only business API."),
           ("Platform", "Toolbox + IQ; governed model and tool routes; scoped identity."),
           ("Lifecycle", "Versioned tests, case file, release gate and feedback.")], "IMPROVE")
    cards(content[21], 21, "A customer-ready next step is a scoped experiment, not a platform shopping list.",
          [("One decision", "Choose a business outcome and an accountable owner."),
           ("One contract", "Define supported actions, expected results and failure boundaries."),
           ("One proof chain", "Agree release criteria, representative cases and an operational feedback path.")])
    cards(content[22], 22, "10 MINUTES FOR QUESTIONS",
          [("Own the contract", "The harness runs the loop; our application enforces business meaning."),
           ("Open the evidence", "A green badge is a verdict. The case file explains it."),
           ("Learn from operation", "Reviewed findings become tests before they become fixes.")])
    cards(content[23], 23, "Q&A backup · Memory preview · DEV only",
          [("Proved", "One caller: remember, recall across conversations, forget and verify deletion."),
           ("Not authority", "Synthetic response style only. No policy, permissions or business facts."),
           ("Still unverified", "Cross-user isolation needs a second genuine authenticated identity.")])
    cards(content[24], 24, "Q&A backup · shared account is not a hard production isolation boundary",
          [("Caller + runtime", "Entra-authenticated entry; runtime reaches versioned capabilities."),
           ("DEV + DEMO", "Different contracts and projects. DEMO Memory remains off."),
           ("Release identity", "Scoped OIDC roles and real approvals still require separate activation.")])
    script = (ROOT / "Presenter manuscript.md").read_text(encoding="utf-8")
    sections = re.findall(r"(?ms)^## Slide (\d{2})[^\n]*\n(.*?)(?=^## Slide \d{2}|^## Appendix|\Z)", script)
    by_num = {int(n): text.strip() for n, text in sections}
    assert set(by_num) == set(range(1, 25))
    for n, slide in content.items():
        for shape in slide.shapes:
            if shape.name == "Workshop slide number":
                shape.text_frame.paragraphs[0].runs[0].text = f"{n:02}"
        notes(slide, by_num[n])
        prune_slide(slide)
    used = {s.slide_layout.part for s in prs.slides}
    for master in prs.slide_masters:
        for item in list(master._element.sldLayoutIdLst):
            if master.part.related_part(item.rId) not in used:
                master.part.drop_rel(item.rId)
                master._element.sldLayoutIdLst.remove(item)
    prs.core_properties.title = "Volt & Co — Can we defend this release?"
    prs.core_properties.subject = "Evidence-first revision · cloud activation pending"
    prs.core_properties.author = "Microsoft · Volt & Co enablement"
    prs.save(OUTPUT)
    print(f"{OUTPUT}\n24 slides: 22 visible and 2 hidden backups. Cloud-dependent v2 proof is explicitly pending.")


if __name__ == "__main__":
    make_deck()
