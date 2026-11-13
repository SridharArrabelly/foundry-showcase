import json
from pathlib import Path
import re
import zipfile

from lxml import etree
from pptx import Presentation
import win32com.client

ROOT = Path(__file__).parent
deck_path = ROOT / "Volt & Co - Governed and improving agents.pptx"
deck = Presentation(deck_path)
assert len(deck.slides) == 24
assert sum(s._element.get("show") != "0" for s in deck.slides) == 22
assert all(s.has_notes_slide and len(s.notes_slide.notes_text_frame.text) > 350 for s in deck.slides)

slide_texts = []
for n, slide in enumerate(deck.slides, 1):
    text = "\n".join(s.text for s in slide.shapes if s.has_text_frame)
    slide_texts.append(text)
    assert not re.search(r"xxxx|lorem|ipsum|speaker name|financial|northstar|nova|library assistant|classified|private preview", text, re.I), (n, text)
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for run in p.runs:
                    assert run.font.name, (n, shape.shape_id, run.text)
                    assert run.font.size is not None, (n, shape.shape_id, run.text)
                    assert run.font.color.type is not None, (n, shape.shape_id, run.text)

for entry, back in [(7, 8), (12, 13), (15, 16), (19, 20)]:
    assert f"RETURN TO SLIDE {back:02}" in slide_texts[entry - 1]
    assert "[SWITCH OUT" in deck.slides[entry - 1].notes_slide.notes_text_frame.text
    assert f"slide {back}" in deck.slides[entry - 1].notes_slide.notes_text_frame.text
    assert "BACK FROM DEMO" in slide_texts[back - 1]

with zipfile.ZipFile(deck_path) as z:
    slide_parts = [p for p in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", p)]
    note_parts = [p for p in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", p)]
    assert len(slide_parts) == len(note_parts) == 24
    for part in slide_parts + note_parts:
        etree.fromstring(z.read(part))
    assert not any(p.startswith("ppt/media/") and p.endswith((".mp3", ".wav", ".mp4", ".wmv")) for p in z.namelist())

app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(str(deck_path), True, False, False)
overflow = []
try:
    for slide in pres.Slides:
        for shape in slide.Shapes:
            if shape.HasTextFrame and shape.TextFrame2.HasText:
                tr = shape.TextFrame2.TextRange
                available = shape.Height - shape.TextFrame2.MarginTop - shape.TextFrame2.MarginBottom
                if tr.BoundHeight > available + 3:
                    overflow.append({
                        "slide": slide.SlideIndex,
                        "shape": shape.Id,
                        "text": tr.Text,
                        "bound_height_pt": round(tr.BoundHeight, 2),
                        "available_height_pt": round(available, 2),
                    })
finally:
    pres.Close()

report = {
    "slides": 24,
    "visible": 22,
    "hidden": [23, 24],
    "notes": "Full manuscript embedded in every slide",
    "source_slide_27": "excluded",
    "unused_source_audio": "removed",
    "textual_checks": "passed",
    "native_text_height_warnings": overflow,
}
(ROOT / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
