from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).parent
renders = root.parent / ".runtime" / "presentation-renders"
images = sorted(renders.glob("slide-*.png"))
font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
for start in range(0, len(images), 6):
    group = images[start:start + 6]
    sheet = Image.new("RGB", (1440, ((len(group) + 1) // 2) * 440), "#e8e8ed")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(group):
        x, y = (i % 2) * 720, (i // 2) * 440
        image = Image.open(path).convert("RGB")
        image.thumbnail((704, 396))
        sheet.paste(image, (x + 8, y + 34))
        draw.text((x + 12, y + 4), path.stem + (" · hidden backup" if int(path.stem[-2:]) > 17 else ""), font=font, fill="#201b36")
    sheet.save(renders / f"contact-{start // 6 + 1}.png")
print("Contact sheets written")
