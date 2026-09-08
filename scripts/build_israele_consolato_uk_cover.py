from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/israele-consolato-uk-central.png"
OUTPUT = ROOT / "assets/social/israele-consolato-uk-instagram.jpg"
PREVIEW = ROOT / "assets/social/israele-consolato-uk-preview-390.jpg"

W, H = 1080, 1350
BG, GOLD, RED, WHITE, MUTED = "#091720", "#d6b16b", "#c91f2d", "#ffffff", "#d6dde2"
BOX, BORDER = "#071219", "#52616d"
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


im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((42, 30, 1038, 1320), outline=GOLD, width=3)
d.rectangle((56, 44, 1024, 50), fill=RED)
d.text((56, 75), "ISRAELE · REGNO UNITO · CISGIORDANIA", font=font(26, True), fill=GOLD)
d.text((56, 120), "LONDRA CHIUDE IL MERCATO", font=font(48, True), fill=WHITE)
d.text((56, 178), "ISRAELE CHIUDE IL CONSOLATO", font=font(48, True), fill=WHITE)
d.text((56, 292), "La ritorsione sposta il costo sui palestinesi", font=fit(d, "La ritorsione sposta il costo sui palestinesi", 968, 32, 24, False), fill=MUTED)

src = Image.open(SOURCE).convert("RGB")
frame = (56, 350, 1024, 850)
fw, fh = frame[2] - frame[0], frame[3] - frame[1]
ratio = max(fw / src.width, fh / src.height)
scaled = src.resize((round(src.width * ratio), round(src.height * ratio)), Image.Resampling.LANCZOS)
crop = scaled.crop(((scaled.width - fw)//2, (scaled.height - fh)//2, (scaled.width + fw)//2, (scaled.height + fh)//2))
mask = Image.new("L", (fw, fh), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, fw, fh), radius=16, fill=255)
im.paste(crop, (56, 350), mask)
d.rounded_rectangle(frame, radius=16, outline=BORDER, width=3)
d.rectangle((78, 786, 1002, 838), fill="#071219")
d.text((92, 797), "MERCI BLOCCATE, CANALE DIPLOMATICO RECISO", font=fit(d, "MERCI BLOCCATE, CANALE DIPLOMATICO RECISO", 890, 25, 19), fill=WHITE)

d.rectangle((56, 870, 1024, 970), fill=BOX, outline="#32414b", width=2)
d.text((82, 882), "IL MECCANISMO", font=font(20, True), fill=GOLD)
mechanism = "IL DIVIETO COLPISCE GLI INSEDIAMENTI. LA RITORSIONE COLPISCE IL CANALE PALESTINESE."
d.text((82, 915), mechanism, font=fit(d, mechanism, 916, 22, 16), fill=WHITE)

d.text((56, 990), "EMIR ALILI", font=font(42, True), fill=WHITE)
d.line((318, 1020, 1024, 1020), fill=GOLD, width=2)
d.text((382, 1044), "SEGUIMI SUI CANALI UFFICIALI", font=font(20, True), fill=GOLD)

d.rounded_rectangle((56, 1072, 1024, 1224), radius=12, fill=BOX, outline=GOLD, width=2)
items = [
    ("WA", "WHATSAPP", "Emir Alili", "#23c763"),
    ("IG", "INSTAGRAM", "@emir_alili", "#e64b8e"),
    ("f", "FACEBOOK", "Emir Alili", "#4385e8"),
    ("TG", "TELEGRAM", "@emiralili", "#35a9e8"),
    ("TT", "TIKTOK", "@em.al.25", "#f05576"),
    ("YT", "YOUTUBE", "@Emir-Alili", "#ef3038"),
    ("WEB", "SITO WEB", "emiralili.it", "#4aa7ff"),
]
colw = 968 / len(items)
for i, (icon, label, handle, color) in enumerate(items):
    x0 = 56 + i * colw
    if i:
        d.line((x0, 1092, x0, 1207), fill=GOLD, width=1)
    cx = x0 + colw/2
    d.ellipse((cx-20, 1083, cx+20, 1123), fill=color)
    fi = fit(d, icon, 34, 14, 10)
    bb = d.textbbox((0,0), icon, font=fi)
    d.text((cx-(bb[2]-bb[0])/2, 1093), icon, font=fi, fill=WHITE)
    fl = fit(d, label, colw-8, 13, 9)
    bb = d.textbbox((0,0), label, font=fl)
    d.text((cx-(bb[2]-bb[0])/2, 1136), label, font=fl, fill=color)
    fhnd = fit(d, handle, colw-8, 14, 9)
    bb = d.textbbox((0,0), handle, font=fhnd)
    d.text((cx-(bb[2]-bb[0])/2, 1167), handle, font=fhnd, fill=WHITE)

d.rectangle((56, 1242, 1024, 1306), fill=RED)
cta = "LEGGI IL DOSSIER SU WWW.EMIRALILI.IT"
fc = fit(d, cta, 900, 30, 23)
bb = d.textbbox((0,0), cta, font=fc)
d.text(((W-(bb[2]-bb[0]))/2, 1258), cta, font=fc, fill=WHITE)

im.save(OUTPUT, quality=94, subsampling=0, optimize=True)
im.resize((390, 488), Image.Resampling.LANCZOS).save(PREVIEW, quality=92)
print(OUTPUT)
print(PREVIEW)
