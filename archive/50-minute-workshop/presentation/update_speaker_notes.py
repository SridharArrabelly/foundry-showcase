"""Embed the complete script while preserving every non-notes PPTX part byte-for-byte."""
import hashlib
import html
import json
import os
import posixpath
import re
import zipfile
from pathlib import Path

from lxml import etree

HERE = Path(__file__).parent
MANUSCRIPT = HERE / "Presenter script.md"
DECK = HERE / "Foundry - From prototype to operated service.pptx"
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def plain_notes(value):
    return re.sub(r"^```[^\n]*\n?", "", value, flags=re.MULTILINE).strip()


def target_part(parent, target):
    return target.lstrip("/") if target.startswith("/") else posixpath.normpath(
        posixpath.join(posixpath.dirname(parent), target)
    )


def rels_path(part):
    directory, name = posixpath.split(part)
    return f"{directory}/_rels/{name}.rels"


def compile_notes(source):
    headings = list(re.finditer(r"^## Slide (\d{2}) - (.+)$", source, re.MULTILINE))
    if [int(m[1]) for m in headings] != list(range(1, 21)):
        raise ValueError("The manuscript must contain slides 01 through 20 exactly once, in order")
    notes, titles = [], []
    for i, match in enumerate(headings):
        body = source[match.end():headings[i + 1].start() if i + 1 < len(headings) else len(source)].strip()
        if "[TIME]" not in body or "[DO]" not in body or not re.search(r"\[(?:SAY|IF .+ - SAY)\]", body):
            raise ValueError(f"Slide {i + 1} lacks timing, actions or spoken delivery")
        notes.append(plain_notes(body))
        titles.append(match[2])
    preparation = source.split("## Before the audience arrives", 1)[1].split("## Running order", 1)[0]
    notes[0] += (
        "\n\n[PRE-SHOW SETUP - COMPLETE BEFORE STARTING THE CLOCK]\n"
        "The following setup is included here so the notes are self-contained. "
        "Once ready, return to the welcome at the top of this note.\n\n"
        + plain_notes(preparation)
    )
    return notes, titles, headings


def replace_notes(notes):
    original = DECK.read_bytes()
    before_digest = hashlib.sha256(original).hexdigest()
    replacements = {}
    with zipfile.ZipFile(DECK) as archive:
        original_parts = {name: archive.read(name) for name in archive.namelist()}
        presentation = etree.fromstring(original_parts["ppt/presentation.xml"])
        relationships = {
            r.get("Id"): r.get("Target")
            for r in etree.fromstring(original_parts["ppt/_rels/presentation.xml.rels"])
        }
        slides = presentation.findall("p:sldIdLst/p:sldId", NS)
        if len(slides) != len(notes):
            raise ValueError("Slide count differs from the manuscript; do not silently remap notes")
        for slide, note in zip(slides, notes):
            part = target_part("ppt/presentation.xml", relationships[slide.get(f"{{{NS['r']}}}id")])
            links = etree.fromstring(original_parts[rels_path(part)])
            note_links = [r for r in links if r.get("Type", "").endswith("/notesSlide")]
            if len(note_links) != 1:
                raise ValueError(f"Expected exactly one notes part for {part}")
            note_part = target_part(part, note_links[0].get("Target"))
            root = etree.fromstring(original_parts[note_part])
            bodies = root.xpath(
                ".//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]/p:txBody", namespaces=NS
            )
            if len(bodies) != 1:
                raise ValueError(f"Ambiguous notes body in {note_part}")
            body = bodies[0]
            for child in list(body):
                if child.tag == f"{{{NS['a']}}}p":
                    body.remove(child)
            for line in note.splitlines():
                paragraph = etree.SubElement(body, f"{{{NS['a']}}}p")
                if line:
                    run = etree.SubElement(paragraph, f"{{{NS['a']}}}r")
                    props = etree.SubElement(run, f"{{{NS['a']}}}rPr", lang="en-US", sz="1200")
                    if line.startswith("[") and line.endswith("]"):
                        props.set("b", "1")
                    value = etree.SubElement(run, f"{{{NS['a']}}}t")
                    value.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    value.text = line
            replacements[note_part] = etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone=True)
        temp = DECK.with_suffix(".notes-update.tmp")
        try:
            with zipfile.ZipFile(temp, "w") as updated:
                for info in archive.infolist():
                    updated.writestr(info, replacements.get(info.filename, original_parts[info.filename]))
            with zipfile.ZipFile(temp) as updated:
                if updated.testzip() is not None or set(updated.namelist()) != set(original_parts):
                    raise ValueError("Presentation package validation failed")
                changed = [name for name, value in original_parts.items() if updated.read(name) != value]
                if not set(changed) <= set(replacements):
                    raise ValueError("A non-notes presentation part changed")
            if hashlib.sha256(DECK.read_bytes()).hexdigest() != before_digest:
                raise RuntimeError("The deck changed during the update. Preserve the user edit and rerun.")
        except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, etree.XMLSyntaxError):
            temp.unlink(missing_ok=True)
            raise
    os.replace(temp, DECK)
    return {"notes_parts_updated": len(replacements), "changed_parts": changed,
            "non_notes_parts_unchanged": True, "before_sha256": before_digest,
            "after_sha256": hashlib.sha256(DECK.read_bytes()).hexdigest()}


def write_html(source, titles):
    nav = "".join(
        f'<a href="#slide-{i:02}">{i:02} · {html.escape(title)}</a>'
        for i, title in enumerate(titles, 1)
    )
    output = ["""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Foundry | Full presenter script</title>
<style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;color:#161616;background:#f5f4f2;font:18px/1.65 'Segoe UI',sans-serif}
header{background:#2a446f;color:white;padding:25px 32px}header h1{font-size:30px;margin:0}header p{margin:8px 0 0}
nav{position:fixed;top:145px;bottom:0;left:0;width:270px;overflow:auto;padding:20px;font-size:14px}
nav a{display:block;color:#005a9e;text-decoration:none;padding:7px 4px}nav a:hover{text-decoration:underline}
main{max-width:1130px;margin-left:290px;padding:24px 42px 80px}h1{font-size:32px}h2{font-size:28px;line-height:1.3;color:#2a446f;margin:44px 0 20px}
h3{font-size:14px;letter-spacing:.04em;margin:0 0 12px;color:#005a9e}
.stage{background:white;border-left:5px solid #d4dfe9;padding:18px 24px;margin:18px 0;break-inside:avoid}
.say{border-color:#0078d4}.say p{font-size:20px}.conditional{background:#fff8e9;border-color:#c28721}.action{background:#e8f3fc}.time{background:#2a446f;color:white}.time h3{color:white}
p{margin:0 0 14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5;font:14px/1.5 Consolas,monospace;background:#eef0f4;padding:18px;border-radius:4px}
table{width:100%;border-collapse:collapse;font-size:15px;margin:18px 0}th,td{text-align:left;vertical-align:top;padding:9px;border-bottom:1px solid #d4dfe9}
a{color:#005a9e}section{scroll-margin-top:20px}
@media(max-width:900px){nav{position:static;width:auto;max-height:220px}main{margin:0;padding:20px}header{padding:20px}}
@page{size:A4;margin:16mm 15mm}
@media print{nav,header{display:none}main{margin:0;padding:0;max-width:none}body{font-size:11pt;line-height:1.35;background:white}.say p{font-size:11.5pt;line-height:1.4}p{margin:0 0 7px}.stage{break-inside:auto;padding:8px 12px;margin:10px 0}.time{background:white!important;color:#161616!important}.time h3{color:#2a446f!important}section{break-before:page}h2{font-size:20pt;margin:12px 0}h3{margin:0 0 7px}pre{font:9pt/1.3 Consolas,monospace;padding:10px}a{color:inherit;text-decoration:none}}
</style><header><h1>Microsoft Foundry · Full presenter script</h1>
<p>Read SAY aloud. Follow DO and COMMAND silently. Conditional wording replaces—not adds to—the normal path.</p></header>""",
        "<nav>" + nav + "</nav><main>"]
    lines = source.splitlines()
    i, stage_open, section_open = 0, False, False

    def close_stage():
        nonlocal stage_open
        if stage_open:
            output.append("</div>")
            stage_open = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("## Slide "):
            close_stage()
            if section_open:
                output.append("</section>")
            number = re.match(r"## Slide (\d{2})", line)[1]
            output.append(f'<section id="slide-{number}"><h2>{html.escape(line[3:])}</h2>')
            section_open = True
        elif line.startswith("#"):
            close_stage()
            level = min(len(line) - len(line.lstrip("#")), 3)
            output.append(f"<h{level}>{html.escape(line[level:].strip())}</h{level}>")
        elif line.startswith("[") and line.endswith("]"):
            close_stage()
            label = line[1:-1]
            if label == "TIME":
                kind = "time"
            elif label.startswith(("IF ", "WHILE WAITING")):
                kind = "conditional"
            elif "SAY" in label:
                kind = "say"
            else:
                kind = "action"
            output.append(f'<div class="stage {kind}"><h3>{html.escape(label)}</h3>')
            stage_open = True
        elif line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            output.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [part.strip() for part in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
                    tag = "th" if not rows else "td"
                    rows.append("<tr>" + "".join(f"<{tag}>{html.escape(cell)}</{tag}>" for cell in cells) + "</tr>")
                i += 1
            output.append("<table>" + "".join(rows) + "</table>")
            i -= 1
        elif line.startswith("https://"):
            output.append(f'<p><a href="{html.escape(line, quote=True)}">{html.escape(line)}</a></p>')
        elif line.strip():
            paragraph = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("[", "#", "```", "|", "https://")):
                i += 1
                paragraph.append(lines[i])
            value = " ".join(paragraph)
            if value.startswith("https://") and " " not in value:
                output.append(f'<p><a href="{html.escape(value, quote=True)}">{html.escape(value)}</a></p>')
            else:
                output.append("<p>" + html.escape(value) + "</p>")
        i += 1
    close_stage()
    if section_open:
        output.append("</section>")
    output.append("</main></html>")
    (HERE / "Presenter script.html").write_text("\n".join(output), encoding="utf-8")


def main():
    source = MANUSCRIPT.read_text(encoding="utf-8")
    notes, titles, headings = compile_notes(source)
    audit = replace_notes(notes)
    (HERE / "slide_notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "Presenter notes.md").write_text(source, encoding="utf-8")
    write_html(source, titles)
    counts = []
    for i, heading in enumerate(headings):
        body = source[heading.end():headings[i + 1].start() if i + 1 < len(headings) else len(source)]
        blocks = re.findall(r"^\[([^\n]+)\]\s*\n(.*?)(?=^\[|\Z)", body, flags=re.MULTILINE | re.DOTALL)
        spoken = " ".join(text for label, text in blocks
                          if label in ("SAY", "TRANSITION - SAY", "RETURN TO SLIDES - SAY", "CLOSING - SAY"))
        counts.append({"slide": i + 1, "spoken_words": len(re.findall(r"\b[\w'-]+\b", spoken))})
    audit["spoken_word_counts"] = counts
    (HERE / "notes-update-check.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"notes_parts_updated": audit["notes_parts_updated"],
                      "non_notes_parts_unchanged": audit["non_notes_parts_unchanged"],
                      "main_path_spoken_words": sum(item["spoken_words"] for item in counts[:14]),
                      "per_slide": counts}, indent=2))


if __name__ == "__main__":
    main()
