from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/trump-dazi-russia-background.png"
OUTPUT = ROOT / "assets/social/trump-dazi-russia-dogana-globale.jpg"
PREVIEW = ROOT / "assets/social/trump-dazi-russia-dogana-globale-preview-390.jpg"
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
im = ImageEnhance.Contrast(im).enhance(1.05)

# Readability gradients while retaining a single full-page cinematic scene.
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(0, 650):
    alpha = round(205 * (1 - y / 760))
    od.rectangle((0, y, W, y + 1), fill=(4, 9, 12, max(0, alpha)))
for y in range(1060, H):
    alpha = round(75 + 155 * ((y - 1060) / (H - 1060)))
    od.rectangle((0, y, W, y + 1), fill=(4, 9, 12, min(230, alpha)))
im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(im)

d.rectangle((34, 30, 1046, 1320), outline=GOLD, width=3)
d.rectangle((50, 46, 1030, 52), fill=RED)
d.text((62, 78), "STATI UNITI · RUSSIA · ENERGIA · SANZIONI", font=font(24, True), fill=GOLD)

lines = ["IL DOLLARO DIVENTA", "UNA DOGANA", "GLOBALE"]
y = 128
for i, line in enumerate(lines):
    f = fit(d, line, 940, 72 if i != 2 else 80, 48, True)
    d.text((62, y), line, font=f, fill=IVORY if i < 2 else GOLD, stroke_width=1, stroke_fill="#06090b")
    y += 84

# Minimal signature/footer hierarchy, no panels or infographics.
d.line((62, 1168, 1018, 1168), fill=GOLD, width=2)
d.text((62, 1192), "EMIR ALILI", font=font(36, True), fill=IVORY)
cta = "LEGGI IL DOSSIER COMPLETO SU WWW.EMIRALILI.IT"
fc = fit(d, cta, 956, 25, 18, True)
d.text((62, 1260), cta, font=fc, fill=GOLD)

im.save(OUTPUT, quality=95, subsampling=0, optimize=True)
im.resize((390, 488), Image.Resampling.LANCZOS).save(PREVIEW, quality=92, optimize=True)
print(OUTPUT)
print(PREVIEW)
