from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/riyadh-patto-mecca-background.png"
OUTPUT = ROOT / "assets/social/riyadh-patto-mecca-prova.jpg"
PREVIEW = ROOT / "assets/social/riyadh-patto-mecca-prova-preview-390.jpg"
W, H = 1080, 1350
GOLD, IVORY, RED = "#d6b16b", "#f4efe4", "#b5222b"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)

def fit(draw, text, width, start, minimum, bold=True):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold)
        if draw.textbbox((0, 0), text, font=f)[2] <= width:
            return f
    return font(minimum, bold)

src = Image.open(SOURCE).convert("RGB")
ratio = max(W / src.width, H / src.height)
src = src.resize((round(src.width * ratio), round(src.height * ratio)), Image.Resampling.LANCZOS)
left, top = (src.width - W) // 2, (src.height - H) // 2
im = src.crop((left, top, left + W, top + H))
im = ImageEnhance.Contrast(im).enhance(1.06)
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(0, 650):
    alpha = round(205 * (1 - y / 760))
    od.rectangle((0, y, W, y + 1), fill=(3, 7, 10, max(0, alpha)))
for y in range(1080, H):
    alpha = round(85 + 145 * ((y - 1080) / (H - 1080)))
    od.rectangle((0, y, W, y + 1), fill=(3, 7, 10, min(230, alpha)))
im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(im)
d.rectangle((34, 30, 1046, 1320), outline=GOLD, width=3)
d.rectangle((50, 46, 1030, 52), fill=RED)
d.text((62, 78), "ARABIA SAUDITA · YEMEN · SICUREZZA", font=font(24, True), fill=GOLD)
lines = ["IL PATTO", "ALLA PROVA", "DI RIYADH"]
y = 128
for i, line in enumerate(lines):
    f = fit(d, line, 940, 82, 54, True)
    d.text((62, y), line, font=f, fill=GOLD if i == 2 else IVORY, stroke_width=1, stroke_fill="#06090b")
    y += 91
d.line((62, 1168, 1018, 1168), fill=GOLD, width=2)
d.text((62, 1192), "EMIR ALILI", font=font(36, True), fill=IVORY)
cta = "LEGGI IL DOSSIER COMPLETO SU WWW.EMIRALILI.IT"
d.text((62, 1260), cta, font=fit(d, cta, 956, 25, 18, True), fill=GOLD)
im.save(OUTPUT, quality=95, subsampling=0, optimize=True)
im.resize((390, 488), Image.Resampling.LANCZOS).save(PREVIEW, quality=92, optimize=True)
print(OUTPUT)
