from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/hormuz-blacklist-56-central.jpg"
OUTPUT = ROOT / "assets/social/hormuz-lista-nera-fuoco-instagram.jpg"

W, H = 1080, 1350
BG = "#091720"
RED = "#c91f2d"
GOLD = "#d6b16b"
WHITE = "#ffffff"
MUTED = "#d6dde2"
BORDER = "#52616d"
BOX = "#071219"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def fit_text(draw, text, max_width, start_size, min_size, bold=True):
    for size in range(start_size, min_size - 1, -1):
        f = font(size, bold)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
    return font(min_size, bold)


canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
draw.rectangle((56, 44, 1024, 50), fill=RED)

draw.text((56, 75), "HORMUZ · SHIPPING · LAWFARE", font=font(30, True), fill=GOLD)

headline = ["LA LISTA NERA", "DIVENTA FUOCO"]
headline_font = font(66, True)
draw.text((56, 114), headline[0], font=headline_font, fill=WHITE)
draw.text((56, 184), headline[1], font=headline_font, fill=WHITE)

subtitle = "Cinquantasei navi, poi i missili sulle petroliere"
draw.text((56, 292), subtitle, font=fit_text(draw, subtitle, 968, 34, 26, False), fill=MUTED)

src = Image.open(SOURCE).convert("RGB")
frame = (56, 350, 1024, 950)
fw, fh = frame[2] - frame[0], frame[3] - frame[1]
ratio = max(fw / src.width, fh / src.height)
scaled = src.resize((round(src.width * ratio), round(src.height * ratio)), Image.Resampling.LANCZOS)
left = (scaled.width - fw) // 2
top = (scaled.height - fh) // 2
crop = scaled.crop((left, top, left + fw, top + fh))
mask = Image.new("L", (fw, fh), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, fw, fh), radius=16, fill=255)
canvas.paste(crop, (56, 350), mask)
draw.rounded_rectangle(frame, radius=16, outline=BORDER, width=3)

caption_box = (76, 868, 1004, 936)
overlay = Image.new("RGBA", (caption_box[2] - caption_box[0], caption_box[3] - caption_box[1]), (4, 14, 20, 210))
canvas.paste(overlay.convert("RGB"), (caption_box[0], caption_box[1]))
draw.text((88, 882), "LNG, LPG, GREGGIO E PRODOTTI RAFFINATI", font=font(24, True), fill=WHITE)

draw.rectangle((56, 990, 1024, 1102), fill=BOX, outline="#32414b", width=2)
draw.text((82, 1005), "IL MECCANISMO", font=font(20, True), fill=GOLD)
mechanism = "WASHINGTON BLOCCA. TEHERAN INTERDICE. GLI ARMATORI PAGANO."
draw.text((82, 1039), mechanism, font=fit_text(draw, mechanism, 916, 27, 21, True), fill=WHITE)

draw.text((56, 1140), "EMIR ALILI", font=font(44, True), fill=WHITE)
draw.rectangle((56, 1230, 1024, 1305), fill=RED)
cta = "LEGGI IL DOSSIER SU WWW.EMIRALILI.IT"
cta_font = fit_text(draw, cta, 900, 30, 24, True)
bbox = draw.textbbox((0, 0), cta, font=cta_font)
draw.text((540 - (bbox[2] - bbox[0]) / 2, 1249), cta, font=cta_font, fill=WHITE)

canvas.save(OUTPUT, quality=94, optimize=True, progressive=True)
print(OUTPUT)
