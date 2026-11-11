"""Create a printable presenter manuscript without adding project dependencies."""
from html import escape
from pathlib import Path
import re
import win32com.client

ROOT = Path(__file__).parent
text = (ROOT / "Presenter manuscript.md").read_text(encoding="utf-8")

def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

blocks = []
for block in text.split("\n\n"):
    block = block.strip()
    if not block:
        continue
    if block.startswith("```") and block.endswith("```"):
        command = "\n".join(block.splitlines()[1:-1])
        blocks.append('<p class="cue command">' + escape(command).replace("\n", "<br>") + "</p>")
    elif block.startswith("# "):
        blocks.append("<h1>" + inline(block[2:]) + "</h1>")
    elif block.startswith("## "):
        heading = block[3:]
        cls = "chapter" if heading.startswith("Slide ") or heading.startswith("Appendix ") else ""
        blocks.append(f'<h2 class="{cls}">{inline(heading)}</h2>')
    elif re.match(r"^\d+\. ", block) or block.startswith("- "):
        items = [re.sub(r"^(?:\d+\.|-)\s*", "", s) for s in block.splitlines()]
        blocks.append("<ul>" + "".join("<li>" + inline(s) + "</li>" for s in items) + "</ul>")
    else:
        cls = "cue" if block.startswith("[") else "spoken" if block.startswith("“") else ""
        blocks.append(f'<p class="{cls}">{inline(block).replace(chr(10), "<br>")}</p>')

html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>Volt & Co — Presenter manuscript</title>
<style>
@page { size: A4; margin: 18mm 19mm; }
body { font-family: 'Segoe UI', sans-serif; font-size: 11pt; color: #201b36; line-height: 1.32; }
h1 { font-size: 27pt; color: #5230bc; }
h2 { font-size: 19pt; color: #5230bc; margin-top: 20pt; }
h2.chapter { page-break-before: always; }
p { margin: 0 0 9pt; }
p.cue { color: #005b9f; background-color: #edf5fb; padding: 8pt; font-size: 10pt; }
strong { color: #352263; }
code { font-family: Consolas, monospace; font-size: 9.5pt; }
p.command { font-family: Consolas, monospace; font-size: 9pt; }
li { margin-bottom: 5pt; }
</style></head><body>""" + "\n".join(blocks) + "</body></html>"
path = ROOT / "Presenter manuscript.html"
path.write_text(html, encoding="utf-8")
app = win32com.client.DispatchEx("Word.Application")
app.Visible = False
doc = None
try:
    doc = app.Documents.Open(str(path), ReadOnly=True, AddToRecentFiles=False)
    doc.PageSetup.PaperSize = 7  # A4
    doc.PageSetup.TopMargin = 51
    doc.PageSetup.BottomMargin = 51
    doc.PageSetup.LeftMargin = 54
    doc.PageSetup.RightMargin = 54
    footer = doc.Sections(1).Footers(1).Range
    footer.Text = "VOLT & CO  |  PRESENTER MANUSCRIPT  |  "
    footer.Font.Name = "Segoe UI"
    footer.Font.Size = 9
    footer.Font.Color = 0x65524F
    footer.Collapse(0)
    footer.Fields.Add(footer, 33)  # PAGE
    doc.ExportAsFixedFormat(str(ROOT / "Presenter manuscript.pdf"), 17)
    print("Presenter manuscript.pdf:", doc.ComputeStatistics(2), "pages")
finally:
    if doc is not None:
        doc.Close(False)
    app.Quit()
