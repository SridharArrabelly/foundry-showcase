"""Adapt the user-supplied workshop without changing it or the existing deck."""
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
SOURCE = Path(r"C:\Users\sarrabelly\Downloads\Foundry Agent Platform Workshop v1.0.0.pptx")
OUTPUT = ROOT / "Volt & Co - Governed and improving agents.pptx"
PURPLE, AZURE, INK = "5230BC", "0078D4", "201B36"
VIOLET, PALE, TEAL, WHITE, MUTED = "EDE7FE", "F5F7FC", "087D87", "FFFFFF", "4F5265"
FONT = "Segoe UI"
SLIDE_SOURCES = [1, 15, 9, 33, 31, 6, 47, 141, 57, 128, 115, 83, 98, 185, 159, None, 198, 113, 163]


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
    add_text(slide, f"{n:02}", 12.35, 7.04, .48, .25, 12, PURPLE, True, PP_ALIGN.RIGHT)
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


def make_deck():
    prs = Presentation(SOURCE)
    selected = {i: prs.slides[i - 1] for i in SLIDE_SOURCES if i is not None}
    keep = {s.part for s in selected.values()}
    for sid in list(prs.slides._sldIdLst):
        if prs.part.related_part(sid.rId) not in keep:
            prs.part.drop_rel(sid.rId)
            prs.slides._sldIdLst.remove(sid)
    # Structural changes first: keep original master/layout/theme relationships.
    new = prs.slides.add_slide(selected[159].slide_layout)
    selected[None] = new
    ids_by_part = {prs.part.related_part(i.rId): i for i in prs.slides._sldIdLst}
    for i in list(prs.slides._sldIdLst):
        prs.slides._sldIdLst.remove(i)
    for n in SLIDE_SOURCES:
        prs.slides._sldIdLst.append(ids_by_part[selected[n].part])
    for i, slide in enumerate(prs.slides):
        slide._element.set("show", "0" if i >= 17 else "1")
        restyle_source(slide)
        for tag in ["p:timing", "p:transition"]:
            for el in list(slide._element.findall(tag, slide._element.nsmap)):
                slide._element.remove(el)

    s = selected[1]
    clear(s)
    add_text(s, "VOLT & CO  /  INTERNAL ENABLEMENT", .5, 1.8, 11, .38, 17, PURPLE, True)
    add_text(s, "From useful agent\nto governed service", .5, 2.45, 11.6, 1.55, 43, INK, True)
    add_text(s, "Microsoft Foundry + Citadel", .5, 4.22, 9, .45, 23, PURPLE)
    add_text(s, "One customer journey. Two learning loops.", .5, 4.82, 9, .4, 18, INK)
    add_text(s, "80 minutes of content  +  10 minutes of Q&A", .5, 5.3, 9, .35, 14, MUTED)

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
    footer(s, 2, "The lifecycle")

    s = selected[9]
    clear(s)
    title(s, "One customer. One support journey.",
          "Volt Charge 65  /  batch CH-0722  /  order VC-10482", 3, "The customer")
    rect(s, .5, 2.0, 4.0, 4.62, INK, radius=True)
    chip(s, "SYNTHETIC CUSTOMER CASE", .78, 2.28, 3.42, PURPLE, WHITE, 12)
    add_text(s, "“Can I get a\nreplacement?”", .8, 2.98, 3.42, 1.35, 32, WHITE, True)
    add_text(s, "Outside the standard\n30-day return window.", .8, 4.62, 3.35, .9, 22, WHITE)
    add_text(s, "A recall and a return window\nare not the same decision.", .8, 5.75, 3.3, .65, 16, "D8D0F5")
    steps = [
        ("1", "Establish the facts", "Recall, order and eligibility tools", PURPLE),
        ("2", "Ground the policy", "Foundry IQ returns a source citation", AZURE),
        ("3", "Choose a responsible next step", "Human assessment—not an automatic refund", TEAL),
    ]
    for y, (num, head, body, col) in zip([2.35, 3.85, 5.35], steps):
        circle(s, num, 4.95, y, .52, col, 17)
        add_text(s, head, 5.73, y - .02, 6.85, .55, 25, INK, True)
        add_text(s, body, 5.73, y + .67, 6.85, .5, 18, MUTED)
    line(s, 5.21, 2.95, 5.21, 3.64, "CEC5EC", 2)
    line(s, 5.21, 4.45, 5.21, 5.13, "CEC5EC", 2)

    s = selected[33]
    clear(s)
    title(s, "Choose the operating model",
          "Use the managed path unless the application needs custom runtime control.", 4, "Agent choices")
    rect(s, .5, 2.0, 12.33, .72, PURPLE)
    add_text(s, "The decision", .72, 2.17, 2.65, .34, 20, WHITE, True)
    add_text(s, "Prompt agent", 3.62, 2.17, 3.9, .34, 20, WHITE, True)
    add_text(s, "Hosted agent", 8.3, 2.17, 4.1, .34, 20, WHITE, True)
    rows = [
        ("Authoring", "Instructions and configuration", "Framework or custom code"),
        ("Runtime responsibility", "Managed orchestration", "Your logic; managed hosting"),
        ("Choose it when…", "The managed path is enough", "You need deterministic logic"),
        ("Cost shape", "Model and tool usage", "Usage + active compute"),
    ]
    for i, (a, b, c) in enumerate(rows):
        y = 2.72 + i * .72
        rect(s, .5, y, 12.33, .72, WHITE if i % 2 else VIOLET)
        add_text(s, a, .72, y + .17, 2.7, .45, 17, INK, True)
        add_text(s, b, 3.62, y + .17, 4.2, .45, 18)
        add_text(s, c, 8.3, y + .17, 4.2, .45, 18)
    rect(s, .5, 6.0, 12.33, .7, INK, radius=True)
    add_text(s, "VOLT'S CHOICE", .72, 6.22, 2.2, .3, 13, "C8BAFF", True)
    add_text(s, "Agent Framework + Responses  →  deterministic decisions and lifecycle integration",
             3.05, 6.19, 9.5, .4, 18, WHITE)

    s = selected[31]
    clear(s)
    title(s, "Our code. Foundry's runtime.",
          "Hosted is the control path—not the unmanaged path.", 5, "Hosted responsibilities")
    # Source slide 31's paired responsibility panels, retained as editable shapes.
    rect(s, .5, 2.02, 5.96, 3.9, VIOLET, PURPLE, True)
    rect(s, 6.85, 2.02, 5.98, 3.9, "E8F4FD", AZURE, True)
    chip(s, "YOU OWN", .78, 2.29, 1.8, PURPLE, WHITE)
    chip(s, "FOUNDRY PROVIDES", 7.13, 2.29, 2.8, AZURE, WHITE)
    for y, txt in [(3.01, "Agent logic + orchestration"), (3.77, "Framework + dependencies"), (4.53, "Responses request handling"), (5.29, "Configuration + sizing")]:
        add_text(s, txt, .82, y, 5.28, .5, 23, INK, True)
    for y, txt in [(3.01, "Managed hosting + endpoint"), (3.77, "Scaling + agent identity"), (4.53, "Tracing + evaluations"), (5.29, "Operate + monitor")]:
        add_text(s, txt, 7.17, y, 5.28, .5, 23, INK, True)
    add_text(s, "GitHub Copilot helps us develop the application.", .55, 6.22, 7.55, .4, 20, PURPLE, True)
    add_text(s, "It is not the deployed runtime.", 8.12, 6.22, 4.5, .4, 20, INK)

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

    s = selected[47]
    clear(s)
    title(s, "Give the agent governed capabilities",
          "Tools → a curated Toolbox → a pinned agent version", 7, "Tools and evidence")
    chip(s, "CONCEPTUAL ROUTE · NOT A PORTAL SCREENSHOT", .5, 1.9, 6.15, size=11)
    rect(s, .5, 2.78, 3.15, 2.85, VIOLET, PURPLE, True)
    add_text(s, "Read-only\nbusiness tools", .8, 3.08, 2.6, 1.0, 27, PURPLE, True)
    add_text(s, "Recall\nOrder status\nEligibility", .8, 4.18, 2.65, 1.2, 19)
    line(s, 3.68, 4.17, 4.38, 4.17, PURPLE, 3, True)
    rect(s, 4.48, 2.78, 4.35, 2.85, WHITE, PURPLE, True)
    chip(s, "FOUNDRY TOOLBOX", 4.76, 3.06, 3.8, PURPLE, WHITE, 14)
    add_text(s, "Curate tools.\nPin the version.\nKeep access explicit.", 4.8, 3.85, 3.75, 1.5, 23, INK, True)
    line(s, 8.88, 4.17, 9.58, 4.17, PURPLE, 3, True)
    rect(s, 9.7, 2.78, 3.13, 2.85, INK, radius=True)
    add_text(s, "Volt agent", 10.0, 3.15, 2.5, .55, 27, WHITE, True)
    add_text(s, "Agent Framework\nResponses protocol", 10.0, 4.04, 2.5, .9, 20, WHITE)
    add_text(s, "One answer we can inspect—not an unrestricted tool catalog.",
             .55, 6.1, 12.1, .6, 24, PURPLE, True)

    s = selected[141]
    clear(s)
    title(s, "Ground the answer in policy",
          "Foundry IQ connects source evidence to the customer response.", 8, "Knowledge", "IQ portal experience · preview")
    # Source slide 141's source → knowledge base → agent composition, narrowed to Search.
    heads = [("1", "Sources", .5, 3.55, PURPLE), ("2", "Knowledge base", 4.88, 3.55, AZURE), ("3", "Agent + citation", 9.26, 3.57, TEAL)]
    for num, head, x, w, col in heads:
        rect(s, x, 2.25, w, 3.82, WHITE, col, True)
        circle(s, num, x + .26, 2.53, .44, col)
        add_text(s, head, x + .85, 2.52, w - 1.05, .6, 23, col, True)
    # Native document symbols rather than unrelated source screenshots.
    for y in [3.47, 4.49]:
        rect(s, .8, y, .48, .65, VIOLET, PURPLE)
        line(s, .9, y + .19, 1.17, y + .19, PURPLE, 1)
        line(s, .9, y + .34, 1.17, y + .34, PURPLE, 1)
    add_text(s, "Replacement policy", 1.46, 3.49, 2.28, .65, 19, INK, True)
    add_text(s, "Synthetic recall notice", 1.46, 4.51, 2.28, .72, 19, INK, True)
    add_text(s, "Azure AI Search", .81, 5.45, 2.9, .35, 16, PURPLE, True)
    add_text(s, "volt-support-\nknowledge", 5.18, 3.5, 2.92, .85, 23, INK, True)
    add_text(s, "Text + semantic\nextractive retrieval", 5.18, 4.67, 2.92, .85, 20, MUTED)
    add_text(s, "Retrieve evidence.\nKeep the source.\nExplain next steps.", 9.56, 3.48, 2.94, 1.65, 23, INK, True)
    add_text(s, "A citation is inspectable.", 9.56, 5.46, 2.95, .4, 16, TEAL, True)
    line(s, 4.09, 4.25, 4.72, 4.25, PURPLE, 2.6, True)
    line(s, 8.47, 4.25, 9.1, 4.25, PURPLE, 2.6, True)
    add_text(s, "Policy knowledge complements business tools. It does not replace them.", .5, 6.35, 12.2, .5, 22, PURPLE, True)

    s = selected[57]
    clear(s)
    title(s, "One gateway. Explicit access contracts.",
          "Citadel's Governance Hub governs the calls routed through it.", 9, "APIM")
    rect(s, .5, 2.25, 2.95, 3.7, INK, radius=True)
    add_text(s, "Volt agent", .8, 2.57, 2.35, .6, 28, WHITE, True)
    add_text(s, "Connected model", .8, 3.65, 2.35, .8, 20, WHITE)
    add_text(s, "Toolbox → MCP", .8, 4.86, 2.35, .8, 20, WHITE)
    rect(s, 4.22, 2.25, 4.35, 3.7, VIOLET, PURPLE, True)
    chip(s, "API MANAGEMENT", 4.52, 2.56, 3.75, PURPLE, WHITE, 16)
    add_text(s, "Access by use case\nApproved model route\nToken quotas", 4.54, 3.45, 3.65, 1.65, 24, INK, True)
    add_text(s, "Trace the boundary that acted.", 4.54, 5.45, 3.65, .35, 15, PURPLE)
    line(s, 3.48, 4.05, 4.04, 4.05, PURPLE, 3, True)
    line(s, 8.63, 3.4, 9.37, 3.4, AZURE, 3, True)
    line(s, 8.63, 4.88, 9.37, 4.88, TEAL, 3, True)
    rect(s, 9.51, 2.65, 3.32, 1.45, "E8F4FD", AZURE, True)
    add_text(s, "Approved model", 9.79, 2.91, 2.77, .5, 23, AZURE, True)
    add_text(s, "gpt-5.4-mini route", 9.79, 3.48, 2.77, .35, 16)
    rect(s, 9.51, 4.37, 3.32, 1.58, "E6F3F3", TEAL, True)
    add_text(s, "Volt business API", 9.79, 4.62, 2.77, .5, 23, TEAL, True)
    add_text(s, "Functions + private storage", 9.79, 5.21, 2.77, .7, 17)
    add_text(s, "An access contract is not customer order-ownership authorization.",
             .5, 6.35, 12.3, .5, 23, INK, True)

    s = selected[128]
    clear(s)
    title(s, "Enforce the right boundary",
          "Authorization ≠ content guardrails ≠ business eligibility", 10, "Governance", "Agent guardrails · preview")
    stages = [
        ("1", "Input", "Inspect content\nat supported\nboundaries.", PURPLE),
        ("2", "Reason", "Plan from\ninstructions\nand context.", PURPLE),
        ("3", "Tool access", "Check the\nconsumer's\naccess contract.", AZURE),
        ("4", "Business rule", "Apply eligibility\nand safety\nrules.", TEAL),
        ("5", "Response", "Inspect the\noutcome and\nits evidence.", PURPLE),
    ]
    for i, (num, head, body, col) in enumerate(stages):
        x = .5 + i * 2.5
        rect(s, x, 2.5, 2.31, 3.0, WHITE, col, True)
        circle(s, num, x + .23, 2.78, .43, col)
        add_text(s, head, x + .23, 3.48, 1.87, .7, 22, col, True)
        add_text(s, body, x + .23, 4.2, 1.87, 1.05, 17)
        if i < 4:
            line(s, x + 2.33, 3.94, x + 2.47, 3.94, PURPLE, 2, True)
    rect(s, .5, 5.94, 12.33, .72, VIOLET, radius=True)
    add_text(s, "Prove permitted utility and the specific block—not just a refusal.",
             .76, 6.12, 11.8, .43, 21, PURPLE, True)

    s = selected[115]
    clear(s)
    title(s, "Remember preferences, not authority",
          "The same caller can return. The facts still come from authoritative systems.", 11, "Memory", "Memory Store · preview")
    rect(s, 4.83, 2.28, 3.68, 3.76, VIOLET, PURPLE, True)
    chip(s, "VOLT-PREFERENCES", 5.12, 2.56, 3.1, PURPLE, WHITE, 13)
    add_text(s, "“Concise answers.\nNext step first.”", 5.14, 3.36, 3.06, 1.0, 26, INK, True)
    add_text(s, "User profile only\n7-day retention\nExplicit forget", 5.14, 4.75, 3.05, 1.2, 19, PURPLE)
    for y, label, sub, writing in [
        (2.6, "Caller A · session 1", "Write the preference", True),
        (4.58, "Caller A · session 2", "Return the saved preference", False),
    ]:
        circle(s, "A", .63, y, .55, AZURE, 19)
        add_text(s, label, 1.42, y, 2.87, .56, 22, INK, True)
        add_text(s, sub, 1.42, y + .72, 2.87, .75, 17, MUTED)
        start, end = (4.12, 4.65) if writing else (4.65, 4.12)
        line(s, start, y + .3, end, y + .3, AZURE, 2.5, True)
    circle(s, "B", 9.12, 2.63, .55, TEAL, 19)
    add_text(s, "Caller B", 9.91, 2.63, 2.4, .55, 23, INK, True)
    add_text(s, "Separate authenticated\nscope—not a new chat\nfor Caller A.", 9.13, 3.66, 3.12, 1.35, 22)
    chip(s, "NO SHARED PREFERENCE", 9.13, 5.39, 3.36, "E6F3F3", TEAL, 12)
    add_text(s, "Keep policy, permissions and customer facts out of preference memory.",
             .5, 6.33, 12.15, .55, 21, PURPLE, True)

    s = selected[83]
    clear(s)
    title(s, "Evidence before confidence",
          "A fluent answer can still make the wrong business decision.", 12, "Evaluation", "Custom evaluators · preview")
    rect(s, .5, 2.12, 3.75, 3.9, INK, radius=True)
    add_text(s, "“It sounds right.”", .8, 2.49, 3.15, 1.05, 30, WHITE, True)
    add_text(s, "Coherence", .8, 3.79, 3.15, .55, 25, "D5C9FF", True)
    add_text(s, "Useful quality evidence.\nNot recall correctness.", .8, 4.6, 3.15, .9, 20, WHITE)
    line(s, 4.3, 4.12, 4.99, 4.12, PURPLE, 3, True)
    rect(s, 5.13, 2.12, 7.7, 3.9, WHITE, PURPLE, True)
    chip(s, "BUSINESS CONTRACT", 5.45, 2.43, 3.78, PURPLE, WHITE, 14)
    add_text(s, "Structured decision", 5.47, 3.27, 6.98, .5, 26, INK, True)
    add_text(s, "+ observed tool evidence", 5.47, 4.04, 6.98, .5, 26, AZURE, True)
    add_text(s, "+ policy citation when required", 5.47, 4.81, 6.98, .5, 26, TEAL, True)
    add_text(s, "Compare exact versions on reviewed cases. Keep tuning data separate from holdouts.",
             .5, 6.35, 12.3, .5, 22, PURPLE, True)

    s = selected[98]
    clear(s)
    title(s, "Optimize configuration. Review the change.",
          "The best score starts a review—it does not authorize a release.", 13, "Agent Optimizer", "Agent Optimizer · limited preview")
    flow = [
        ("1", "Define", "Objective +\ntuning cases"),
        ("2", "Generate", "Configuration\ncandidates"),
        ("3", "Compare", "Baseline +\nheld-out cases"),
        ("4", "Review", "Source diff +\ncost / latency"),
        ("5", "Gate", "Approved for\nrelease"),
    ]
    for i, (n, h, b) in enumerate(flow):
        x = .5 + 2.5 * i
        fill = PURPLE if i == 3 else WHITE
        fg = WHITE if i == 3 else INK
        rect(s, x, 2.49, 2.31, 3.0, fill, PURPLE, True)
        circle(s, n, x + .25, 2.78, .43, AZURE if i == 3 else PURPLE)
        add_text(s, h, x + .25, 3.5, 1.82, .64, 23, fg, True)
        add_text(s, b, x + .25, 4.35, 1.82, .9, 18, fg)
        if i < 4:
            line(s, x + 2.34, 3.94, x + 2.46, 3.94, PURPLE, 2, True)
    add_text(s, "A code defect needs a code fix. An optimizer candidate can also be rejected.",
             .5, 6.1, 12.2, .65, 24, PURPLE, True)

    s = selected[185]
    clear(s)
    title(s, "Operation teaches DEV what to test",
          "Tool result: eligible. Agent decision: recommendation.", 14, "The trace flywheel")
    chip(s, "OBSERVED BUSINESS-CONTRACT MISMATCH", .5, 1.98, 5.2, size=12)
    flow = [
        ("1", "Trace", "What happened?"),
        ("2", "Select", "Relevant evidence"),
        ("3", "Inspect", "Find the decision"),
        ("4", "Propose", "A regression case"),
        ("5", "Review", "Expected behavior"),
        ("6", "Improve", "Test the fix"),
    ]
    for i, (n, h, b) in enumerate(flow):
        x = .5 + i * 2.08
        fill, fg = (PURPLE, WHITE) if i == 4 else (WHITE, INK)
        rect(s, x, 2.83, 1.93, 2.65, fill, PURPLE, True)
        circle(s, n, x + .22, 3.09, .42, AZURE if i == 4 else PURPLE)
        add_text(s, h, x + .22, 3.79, 1.49, .6, 22, fg, True)
        add_text(s, b, x + .22, 4.57, 1.49, .65, 17, fg)
    line(s, 11.85, 5.68, 11.85, 6.08, TEAL, 2)
    line(s, 11.85, 6.08, 1.46, 6.08, TEAL, 2, True)
    add_text(s, "A trace is evidence. A person supplies the reviewed expectation.",
             .5, 6.4, 12.25, .48, 22, PURPLE, True)

    s = selected[159]
    replace(s, 2, "A PR carries code and behavioral evidence", 32, INK, True)
    replace(s, 4, "One reviewed candidate. Separate environments. A verifiable serving version.", 16, PURPLE)
    replace(s, 13, "SYNTHETIC TRAFFIC")
    replace(s, 14, "DEMO")
    replace(s, 15, "Production-like requests, real usage.")
    replace(s, 16, "Verify what is actually serving.")
    replace(s, 23, "Candidate")
    replace(s, 24, "Exact\ncandidate", 16)
    replace(s, 30, "Required\nchecks pass", 16)
    replace(s, 36, "Approved\nversion", 16)
    for sid in [24, 30, 36]:
        for paragraph in get(s, sid).text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
    for sid in [23, 29, 35]:
        replace(s, sid, get(s, sid).text, 18, bold=True)
    replace(s, 40, "Reviewed traces → new regression tests.", 18)
    get(s, 40).height = inch(.38)
    replace(s, 42, "A passing PR is not the finish line. Verify the serving version and the customer outcome.", 19, WHITE, True)
    replace(s, 43, "DEMO is a synthetic environment—not customer production.", 12, WHITE)
    footer(s, 15, "The release gate")

    s = new
    clear(s)
    title(s, "Follow one fix from trace to customer",
          "Every link should identify the same change—not merely the latest version.", 16, "The evidence chain")
    nodes = [
        (0.5, 2.35, "01", "Trace", "Observed decision"),
        (4.88, 2.35, "02", "Reviewed case", "Expected: eligible"),
        (9.26, 2.35, "03", "Issue + PR", "Reproduction + diff"),
        (9.26, 4.62, "04", "Candidate", "Commit + artifact"),
        (4.88, 4.62, "05", "Gate", "Exact run + verdict"),
        (.5, 4.62, "06", "Serving version", "Corrected customer result"),
    ]
    for x, y, n, head, sub in nodes:
        col = TEAL if n == "06" else PURPLE
        rect(s, x, y, 3.55, 1.7, WHITE, col, True)
        circle(s, n, x + .25, y + .26, .46, col, 13)
        add_text(s, head, x + .92, y + .27, 2.38, .72, 23, col, True)
        add_text(s, sub, x + .26, y + 1.16, 3.03, .4, 16)
    line(s, 4.09, 3.19, 4.72, 3.19, PURPLE, 2.8, True)
    line(s, 8.47, 3.19, 9.1, 3.19, PURPLE, 2.8, True)
    line(s, 11.03, 4.1, 11.03, 4.48, PURPLE, 2.8, True)
    line(s, 9.1, 5.47, 8.47, 5.47, PURPLE, 2.8, True)
    line(s, 4.72, 5.47, 4.09, 5.47, TEAL, 2.8, True)
    add_text(s, "Version identity + behavioral evidence + human judgment", .5, 6.62, 12.1, .35, 20, PURPLE, True)

    s = selected[198]
    clear(s)
    title(s, "Useful. Governed. Measurable. Improving.",
          "Four ideas to take back to your next agent.", 17, "Takeaways + Q&A")
    takeaways = [
        (.5, 2.15, "1", "Useful", "Tools establish facts.\nIQ supplies policy evidence.", PURPLE),
        (6.86, 2.15, "2", "Governed", "Explicit access and boundaries.\nMemory stays deliberately narrow.", AZURE),
        (.5, 4.28, "3", "Measurable", "Correctness is a contract.\nQuality is more than fluency.", TEAL),
        (6.86, 4.28, "4", "Improving", "Reviewed traces become tests.\nGated changes reach customers.", PURPLE),
    ]
    for x, y, n, h, b, c in takeaways:
        circle(s, n, x + .05, y + .04, .6, c, 21)
        add_text(s, h, x + .94, y, 5.02, .63, 30, c, True)
        add_text(s, b, x + .94, y + .83, 4.96, .97, 21)
    rect(s, .5, 6.48, 12.33, .43, INK, radius=True)
    add_text(s, "10 MINUTES FOR YOUR QUESTIONS", .74, 6.57, 11.82, .24, 13, WHITE, True, PP_ALIGN.CENTER)

    s = selected[113]
    clear(s)
    title(s, "Memory: a store is not an authorization system",
          "Q&A backup · one store, explicitly derived scopes, narrow retention", 18, "Hidden backup", "Memory Store · preview")
    rect(s, .5, 2.1, 7.6, 4.15, VIOLET, PURPLE, True)
    chip(s, "VOLT-PREFERENCES", .8, 2.4, 3.4, PURPLE, WHITE, 14)
    for y, h, b in [(3.2, "Caller A scope", "Fixed synthetic response-style preference"),
                     (4.64, "Caller B scope", "Independent preference state")]:
        rect(s, .8, y, 7.0, 1.14, WHITE, PURPLE, True)
        add_text(s, h, 1.05, y + .16, 6.45, .35, 20, PURPLE, True)
        add_text(s, b, 1.05, y + .66, 6.45, .32, 16)
    add_text(s, "Scope follows the\nauthenticated caller.", 8.65, 2.65, 4.13, 1.05, 25, INK, True)
    add_text(s, "7-day TTL\nUser profile only\nForget + verify deletion", 8.65, 4.24, 4.0, 1.5, 23, PURPLE)
    add_text(s, "New conversation ≠ new identity. Runtime isolation needs two authenticated identities.",
             .5, 6.55, 12.3, .42, 20, INK, True)

    s = selected[163]
    clear(s)
    title(s, "Separate platform and team responsibilities",
          "Q&A backup · account scope and project scope solve different problems", 19, "Hidden backup")
    rect(s, .5, 2.08, 12.33, 4.48, "E8F4FD", AZURE, True)
    chip(s, "FOUNDRY ACCOUNT", .82, 2.39, 3.23, AZURE, WHITE, 15)
    add_text(s, "fdy-volt-citadel-261111", 4.41, 2.4, 7.8, .4, 23, AZURE, True)
    add_text(s, "Model deployment, shared infrastructure and account-level responsibilities",
             .84, 3.07, 11.6, .48, 21)
    for x, head, body in [(1.0, "volt-dev", "Build, test and compare candidates"), (6.94, "volt-demo", "Serve synthetic customer traffic")]:
        rect(s, x, 3.94, 5.39, 1.98, WHITE, PURPLE, True)
        add_text(s, head, x + .27, 4.22, 4.85, .51, 27, PURPLE, True)
        add_text(s, body, x + .27, 4.99, 4.85, .66, 21)
    add_text(s, "Different project names are not, by themselves, proof of permission isolation.",
             .5, 6.71, 12.3, .3, 18, INK, True)

    script = (ROOT / "Presenter manuscript.md").read_text(encoding="utf-8")
    sections = re.findall(r"(?ms)^## Slide (\d{2})[^\n]*\n(.*?)(?=^## Slide \d{2}|^## Appendix|\Z)", script)
    by_num = {int(n): text.strip() for n, text in sections}
    assert set(by_num) == set(range(1, 20)), by_num.keys()
    for n, slide in enumerate(prs.slides, 1):
        notes(slide, by_num[n])
        prune_slide(slide)
    used_layouts = {slide.slide_layout.part for slide in prs.slides}
    for master in prs.slide_masters:
        for layout_id in list(master._element.sldLayoutIdLst):
            if master.part.related_part(layout_id.rId) not in used_layouts:
                master.part.drop_rel(layout_id.rId)
                master._element.sldLayoutIdLst.remove(layout_id)
    prs.core_properties.title = "Volt & Co — From useful agent to governed service"
    prs.core_properties.subject = "90-minute internal developer enablement · Microsoft Foundry + Citadel"
    prs.core_properties.author = "Microsoft · Volt & Co enablement"
    prs.core_properties.keywords = "Foundry, Citadel, Volt, internal enablement, rehearsal draft"
    prs.core_properties.comments = "Adapted from the user-supplied workshop. Presenter bindings require rehearsal verification."
    prs.save(OUTPUT)
    with zipfile.ZipFile(OUTPUT) as z:
        slides = [p for p in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", p)]
        assert len(slides) == 19, slides
        for path in slides:
            xml = z.read(path).decode()
            assert not any(t in xml.lower() for t in ["northstar", "financial-report", "nova", "private preview", "classified"])
    print(OUTPUT)
    print("19 slides: 17 visible; 2 hidden Q&A backups. Original source visuals retained on 1, 2, 6, 15.")


if __name__ == "__main__":
    make_deck()
