from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/siria-carburanti-proteste-central.png"
OUTPUT = ROOT / "assets/social/siria-carburanti-proteste-instagram.jpg"
PREVIEW = ROOT / "assets/social/siria-carburanti-proteste-preview-390.jpg"
W, H = 1080, 1350
BG, GOLD, RED, WHITE, MUTED = "#091720", "#d6b16b", "#c91f2d", "#ffffff", "#d6dde2"
BOX, BORDER = "#071219", "#52616d"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=False): return ImageFont.truetype(FB if bold else FR, size)
def fit(draw, text, width, start, minimum, bold=True):
    for size in range(start, minimum - 1, -1):
        f = font(size, bold)
        if draw.textbbox((0, 0), text, font=f)[2] <= width: return f
    return font(minimum, bold)

im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
d.rectangle((42, 30, 1038, 1320), outline=GOLD, width=3); d.rectangle((56, 44, 1024, 50), fill=RED)
d.text((56, 75), "SIRIA · CARBURANTI · PROTESTE · POTERE", font=font(25, True), fill=GOLD)
title1 = "LA PACE PROMESSA FINISCE"; title2 = "ALLA POMPA DI BENZINA"
d.text((56, 118), title1, font=fit(d, title1, 968, 46, 29), fill=WHITE)
d.text((56, 170), title2, font=fit(d, title2, 968, 46, 29), fill=WHITE)
sub = "Il diesel sale del 40%. La protesta cambia il conto politico."
d.text((56, 226), sub, font=fit(d, sub, 968, 29, 19, False), fill=MUTED)
src = Image.open(SOURCE).convert("RGB"); frame = (56, 280, 1024, 815); fw, fh = frame[2]-frame[0], frame[3]-frame[1]
ratio = max(fw/src.width, fh/src.height); scaled = src.resize((round(src.width*ratio), round(src.height*ratio)), Image.Resampling.LANCZOS)
left = (scaled.width-fw)//2; top = (scaled.height-fh)//2; crop = scaled.crop((left, top, left+fw, top+fh))
mask = Image.new("L", (fw, fh), 0); ImageDraw.Draw(mask).rounded_rectangle((0,0,fw,fh), radius=16, fill=255)
im.paste(crop, (56,280), mask); d.rounded_rectangle(frame, radius=16, outline=BORDER, width=3)
d.rectangle((78,751,1002,803), fill=BOX); caption = "RICOSTRUZIONE EDITORIALE · NON RAFFIGURA UN EVENTO SPECIFICO"
d.text((92,762), caption, font=fit(d, caption, 890, 22, 14), fill=WHITE)
d.rectangle((56,835,1024,935), fill=BOX, outline="#32414b", width=2); d.text((82,847), "IL MECCANISMO", font=font(20,True), fill=GOLD)
d.text((82,880), "CARBURANTE PIÙ CARO. TRASPORTI PIÙ CARI.", font=fit(d, "CARBURANTE PIÙ CARO. TRASPORTI PIÙ CARI.", 916, 21, 15), fill=WHITE)
d.text((82,905), "IL COSTO DELLA TRANSIZIONE SCENDE SULLA STRADA.", font=fit(d, "IL COSTO DELLA TRANSIZIONE SCENDE SULLA STRADA.", 916, 21, 15), fill=WHITE)
d.text((56,955), "EMIR ALILI", font=font(42,True), fill=WHITE); d.line((318,985,1024,985), fill=GOLD, width=2)
d.text((382,1009), "SEGUIMI SUI CANALI UFFICIALI", font=font(20,True), fill=GOLD)
d.rounded_rectangle((56,1037,1024,1189), radius=12, fill=BOX, outline=GOLD, width=2)
items=[("WA","WHATSAPP","Emir Alili","#23c763"),("IG","INSTAGRAM","@emir_alili","#e64b8e"),("f","FACEBOOK","Emir Alili","#4385e8"),("TG","TELEGRAM","@emiralili","#35a9e8"),("TT","TIKTOK","@em.al.25","#f05576"),("YT","YOUTUBE","@Emir-Alili","#ef3038"),("WEB","SITO WEB","emiralili.it","#4aa7ff")]
colw=968/len(items)
for i,(icon,label,handle,color) in enumerate(items):
    x0=56+i*colw
    if i: d.line((x0,1057,x0,1172), fill=GOLD, width=1)
    cx=x0+colw/2; d.ellipse((cx-20,1048,cx+20,1088), fill=color)
    fi=fit(d,icon,34,14,10); bb=d.textbbox((0,0),icon,font=fi); d.text((cx-(bb[2]-bb[0])/2,1058),icon,font=fi,fill=WHITE)
    fl=fit(d,label,colw-8,13,9); bb=d.textbbox((0,0),label,font=fl); d.text((cx-(bb[2]-bb[0])/2,1101),label,font=fl,fill=color)
    fhnd=fit(d,handle,colw-8,14,9); bb=d.textbbox((0,0),handle,font=fhnd); d.text((cx-(bb[2]-bb[0])/2,1132),handle,font=fhnd,fill=WHITE)
d.rectangle((56,1207,1024,1301), fill=RED); cta="LEGGI IL DOSSIER SU WWW.EMIRALILI.IT"; fc=fit(d,cta,900,30,23); bb=d.textbbox((0,0),cta,font=fc)
d.text(((W-(bb[2]-bb[0]))/2,1238),cta,font=fc,fill=WHITE)
im.save(OUTPUT,quality=94,subsampling=0,optimize=True); im.resize((390,488),Image.Resampling.LANCZOS).save(PREVIEW,quality=92)
print(OUTPUT); print(PREVIEW)
