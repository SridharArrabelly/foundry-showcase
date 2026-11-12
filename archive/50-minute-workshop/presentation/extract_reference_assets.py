"""Extract only approved visual assets; never copy roadmap or customer-result slides."""
import json
from pathlib import Path

from PIL import Image
from pptx import Presentation
import win32com.client

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
ASSETS.mkdir(exist_ok=True)
BANK = Path(r"C:\Users\sarrabelly\OneDrive - Microsoft\00FY27") / "Microsoft Foundry - What's New and What's Next - Bank Briefing.pptx"
WORKSHOP = Path(r"C:\Users\sarrabelly\OneDrive - Microsoft\00FY27\AI Roadshow FY27\Foundry Agent Platform Workshop v1.0.0.pptx")
CURRENT = HERE / "Foundry - From prototype to operated service.pptx"
NOTES = HERE / "slide_notes.json"
if not NOTES.exists():
    deck = Presentation(CURRENT)
    NOTES.write_text(json.dumps(
        [slide.notes_slide.notes_text_frame.text for slide in deck.slides],
        ensure_ascii=False, indent=2,
    ), encoding="utf-8")

app = win32com.client.DispatchEx("PowerPoint.Application")
bank = app.Presentations.Open(str(BANK), True, False, False)
try:
    cover = bank.Slides(1)
    for i in range(cover.Shapes.Count, 0, -1):
        cover.Shapes(i).Delete()
    cover.Export(str(ASSETS / "azure-cover.png"), "PNG", 2560, 1440)
finally:
    bank.Close()

workshop = app.Presentations.Open(str(WORKSHOP), True, False, False)
try:
    for number, name, crop in [
        (12, "two-loops", (0.03, 0.245, 0.97, 0.88)),
        (162, "release-bridge", (0.03, 0.245, 0.97, 0.80)),
        (67, "observe-improve", (0.03, 0.285, 0.97, 0.86)),
        (23, "foundry-platform", (0.345, 0.085, 0.982, 0.96)),
        (22, "agent-platform", (0.025, 0.255, 0.975, 0.96)),
    ]:
        slide = workshop.Slides(number)
        if number == 23:
            for i in range(slide.Shapes.Count, 0, -1):
                item = slide.Shapes(i)
                if item.HasTextFrame and item.TextFrame.HasText:
                    if item.TextFrame.TextRange.Text.strip() == "Build AI apps and agents that scale":
                        item.Delete()
        if number == 22:
            for item in slide.Shapes:
                if item.HasTextFrame and item.TextFrame.HasText:
                    value = item.TextFrame.TextRange.Text
                    if "14k models:" in value:
                        item.TextFrame.TextRange.Text = value.replace("14k models:", "Models:")
        if number == 12:
            for shape in slide.Shapes:
                if shape.HasTextFrame and shape.TextFrame.HasText:
                    value = shape.TextFrame.TextRange.Text
                    if value.startswith("Git commit + usecase.yaml"):
                        shape.TextFrame.TextRange.Text = "Versioned candidate + approved configuration + dataset + evaluation results"
                    if value.startswith("Production anomalies & blocked attacks"):
                        shape.TextFrame.TextRange.Text = "Operational observations become reviewed cases and policy updates for the next DEV cycle."
        path = ASSETS / f"{name}.png"
        slide.Export(str(path), "PNG", 3840, 2160)
        image = Image.open(path)
        w, h = image.size
        image.crop(tuple(round(v * d) for v, d in zip(crop, (w, h, w, h)))).save(path)
        if number == 23:
            with Image.open(path) as platform:
                w, h = platform.size
                platform.crop((round(.02 * w), round(.12 * h), round(.98 * w), round(.437 * h))).save(
                    ASSETS / "build-and-host.png"
                )
finally:
    workshop.Close()

(ASSETS / "PROVENANCE.md").write_text(
    "# Visual provenance\n\n"
    "- azure-cover.png: original Bank Briefing title layout artwork, rendered without slide text.\n"
    "- two-loops.png: workshop slide 12 diagram; long implementation filenames shortened to generic evidence labels.\n"
    "- release-bridge.png: workshop slide 162 diagram, used as a labelled production reference pattern.\n"
    "- observe-improve.png: workshop slide 67 lifecycle illustration.\n"
    "- foundry-platform.png: workshop slide 23 architecture graphic; original slide title removed before cropping.\n"
    "- build-and-host.png: enlarged BUILD and HOST sections from the same workshop slide 23 graphic.\n"
    "- agent-platform.png: workshop slide 22 platform graphic (appendix).\n\n"
    "These are source-derived visual assets, not screenshots of the deployed Volt agent. "
    "No finance/library results, NDA roadmap pages, or customer data were copied. "
    "Original files were opened read-only and were not saved or changed.\n",
    encoding="utf-8",
)
print(f"Extracted original artwork and preserved notes in {ASSETS}")
