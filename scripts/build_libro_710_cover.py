from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/social/libro-710-avvertimenti-instagram.jpg"
PREVIEW = ROOT / "assets/social/libro-710-avvertimenti-preview-390.jpg"
BOOK = ROOT / "assets/img/copertina-710.jpeg"
STRIP = ROOT / "assets/social/social-channels-strip.png"

W, H = 1080, 1350
BG, GOLD, RED, WHITE, MUTED = "#06151c", "#d7aa55", "#d7192d", "#f4f2ec", "#c8d0d3"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size): return ImageFont.truetype(path, size)

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle((44, 34, W-44, H-34), outline=GOLD, width=3)
d.rectangle((88, 72, W-88, 80), fill=RED)
d.text((88, 103), "ISRAELE · 7 OTTOBRE · LIBRO", fill=GOLD, font=font(FONT_B, 27))
d.text((88, 145), "IL LIBRO AVEVA", fill=WHITE, font=font(FONT_B, 62))
d.text((88, 208), "VISTO IL METODO", fill=WHITE, font=font(FONT_B, 62))
d.text((88, 284), "Nuovi avvertimenti incrinano la versione della sorpresa totale", fill=MUTED, font=font(FONT_R, 24))

# Central editorial still life: the real book cover, lifted from the site asset.
d.rounded_rectangle((87, 332, 993, 832), radius=18, fill="#0c222b", outline="#788b95", width=3)
book = Image.open(BOOK).convert("RGB")
book.thumbnail((300, 455), Image.Resampling.LANCZOS)
shadow = Image.new("RGBA", (book.width+50, book.height+50), (0,0,0,0))
ImageDraw.Draw(shadow).rounded_rectangle((24,24,book.width+24,book.height+24), radius=8, fill=(0,0,0,180))
shadow = shadow.filter(ImageFilter.GaussianBlur(12))
im.paste(shadow.convert("RGB"), (142, 353))
im.paste(book, (156, 346))

# Documentary timeline, deliberately graphical: no invented photograph.
d.line((525, 410, 525, 728), fill=GOLD, width=4)
events = [(430,"15 SET", "PRIMO ALLARME"),(535,"23 SET", "TELEFONATA ATTRIBUITA A MBZ"),(650,"7 OTT", "ATTACCO DI HAMAS")]
for y, date, label in events:
    d.ellipse((510,y-10,530,y+10), fill=RED, outline=WHITE, width=2)
    d.text((552,y-20), date, fill=GOLD, font=font(FONT_B, 23))
    d.text((552,y+12), label, fill=WHITE, font=font(FONT_B, 18))
d.rectangle((110, 778, 970, 820), fill="#07131a")
d.text((134, 786), "7/10 — L'INIZIO DELLA FINE DEL TRUMAN SHOW", fill=WHITE, font=font(FONT_B, 22))

d.rectangle((88, 854, 992, 936), outline=GOLD, width=2)
d.text((108, 869), "IL MECCANISMO", fill=GOLD, font=font(FONT_B, 21))
d.text((108, 899), "IL PRETESTO SPIEGA L'USO. NON PROVA LA REGIA.", fill=WHITE, font=font(FONT_B, 24))
d.text((88, 955), "EMIR ALILI", fill=WHITE, font=font(FONT_B, 45))
d.line((322, 983, 992, 983), fill=GOLD, width=2)

strip = Image.open(STRIP).convert("RGB")
strip = strip.resize((904, 196), Image.Resampling.LANCZOS)
im.paste(strip, (88, 1000))
d.rectangle((88, 1215, 992, 1288), fill=RED)
cta = "LEGGI IL DOSSIER SU WWW.EMIRALILI.IT"
b = d.textbbox((0,0), cta, font=font(FONT_B, 30))
d.text(((W-(b[2]-b[0]))/2, 1233), cta, fill=WHITE, font=font(FONT_B, 30))

OUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUT, quality=94, subsampling=0)
im.resize((390, 488), Image.Resampling.LANCZOS).save(PREVIEW, quality=92)
print(OUT)
print(PREVIEW)
