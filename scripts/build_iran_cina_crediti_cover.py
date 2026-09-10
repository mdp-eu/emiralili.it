from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/social/iran-cina-crediti-central.png"
OUTPUT = ROOT / "assets/social/iran-cina-petrolio-crediti-instagram.jpg"
PREVIEW = ROOT / "assets/social/iran-cina-petrolio-crediti-preview-390.jpg"
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
d.text((56, 75), "IRAN · CINA · PETROLIO · SANZIONI", font=font(25, True), fill=GOLD)
title="IL PETROLIO DIVENTA CREDITO CINESE"; d.text((56, 120), title, font=fit(d,title,968,44,34), fill=WHITE)
sub="Reuters ricostruisce il circuito che evita il dollaro"; d.text((56, 190), sub, font=fit(d,sub,968,30,21,False), fill=MUTED)
src = Image.open(SOURCE).convert("RGB"); frame = (56, 260, 1024, 810); fw, fh = frame[2]-frame[0], frame[3]-frame[1]
ratio = max(fw/src.width, fh/src.height); scaled = src.resize((round(src.width*ratio), round(src.height*ratio)), Image.Resampling.LANCZOS)
left = (scaled.width-fw)//2; top = (scaled.height-fh)//2; crop = scaled.crop((left, top, left+fw, top+fh))
mask = Image.new("L", (fw, fh), 0); ImageDraw.Draw(mask).rounded_rectangle((0,0,fw,fh), radius=16, fill=255)
im.paste(crop, (56,260), mask); d.rounded_rectangle(frame, radius=16, outline=BORDER, width=3)
d.rectangle((78,746,1002,798), fill=BOX); caption="CHUXIN: IL DENARO PUÒ ESISTERE SOLO IN CONTABILITÀ"; d.text((92,757), caption, font=fit(d,caption,890,24,16), fill=WHITE)
d.rectangle((56,830,1024,930), fill=BOX, outline="#32414b", width=2); d.text((82,842), "IL MECCANISMO", font=font(20,True), fill=GOLD)
mechanism = "IL GREGGIO CREA CREDITI IN CINA. I CREDITI PAGANO MERCI E CANTIERI."; d.text((82,875), mechanism, font=fit(d,mechanism,916,22,15), fill=WHITE)
d.text((56,950), "EMIR ALILI", font=font(42,True), fill=WHITE); d.line((318,980,1024,980), fill=GOLD, width=2)
d.text((382,1004), "SEGUIMI SUI CANALI UFFICIALI", font=font(20,True), fill=GOLD)
d.rounded_rectangle((56,1032,1024,1184), radius=12, fill=BOX, outline=GOLD, width=2)
items=[("WA","WHATSAPP","Emir Alili","#23c763"),("IG","INSTAGRAM","@emir_alili","#e64b8e"),("f","FACEBOOK","Emir Alili","#4385e8"),("TG","TELEGRAM","@emiralili","#35a9e8"),("TT","TIKTOK","@em.al.25","#f05576"),("YT","YOUTUBE","@Emir-Alili","#ef3038"),("WEB","SITO WEB","emiralili.it","#4aa7ff")]
colw=968/len(items)
for i,(icon,label,handle,color) in enumerate(items):
    x0=56+i*colw
    if i: d.line((x0,1052,x0,1167), fill=GOLD, width=1)
    cx=x0+colw/2; d.ellipse((cx-20,1043,cx+20,1083), fill=color)
    fi=fit(d,icon,34,14,10); bb=d.textbbox((0,0),icon,font=fi); d.text((cx-(bb[2]-bb[0])/2,1053),icon,font=fi,fill=WHITE)
    fl=fit(d,label,colw-8,13,9); bb=d.textbbox((0,0),label,font=fl); d.text((cx-(bb[2]-bb[0])/2,1096),label,font=fl,fill=color)
    fhnd=fit(d,handle,colw-8,14,9); bb=d.textbbox((0,0),handle,font=fhnd); d.text((cx-(bb[2]-bb[0])/2,1127),handle,font=fhnd,fill=WHITE)
d.rectangle((56,1202,1024,1296), fill=RED); cta="LEGGI IL DOSSIER SU WWW.EMIRALILI.IT"; fc=fit(d,cta,900,30,23); bb=d.textbbox((0,0),cta,font=fc)
d.text(((W-(bb[2]-bb[0]))/2,1233),cta,font=fc,fill=WHITE)
im.save(OUTPUT,quality=94,subsampling=0,optimize=True); im.resize((390,488),Image.Resampling.LANCZOS).save(PREVIEW,quality=92)
print(OUTPUT); print(PREVIEW)
