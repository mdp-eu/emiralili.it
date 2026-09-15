#!/usr/bin/env python3
from pathlib import Path
import re, json, html

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-15"
PERSON_ID = "https://emiralili.it/#person"
AUTHOR = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Emir Alili",
    "url": "https://emiralili.it/chi-sono.html",
    "sameAs": [
        "https://www.linkedin.com/in/emiralili/",
        "https://www.instagram.com/emir_alili/",
        "https://www.facebook.com/emir.alili.81/",
        "https://t.me/emiralili",
    ],
}
TOPICS = {
    "medio-oriente": {
        "name": "Medio Oriente",
        "file": "medio-oriente.html",
        "title": "Medio Oriente — Analisi e dossier di Emir Alili",
        "description": "Dossier di Emir Alili su Iran, Siria, Turchia, Golfo, Yemen, Israele, Palestina e rapporti di forza regionali.",
        "intro": "Un archivio tematico sulle trasformazioni del Medio Oriente: sicurezza, energia, alleanze, conflitti, diplomazia e rapporti di forza.",
        "terms": ["iran","israel","israele","palestin","gaza","siria","turki","turch","saud","yemen","houth","hormuz","qatar","emirati","uae","golfo","golan","hamas","unrwa","giordania","libano","hezbollah","mecca"],
    },
    "palestina-israele": {
        "name": "Palestina e Israele",
        "file": "palestina-israele.html",
        "title": "Palestina e Israele — Dossier di Emir Alili",
        "description": "Analisi e dossier di Emir Alili su Palestina, Israele, Gaza, Cisgiordania, diritto internazionale, sicurezza e occupazione.",
        "intro": "Dossier dedicati a Palestina e Israele, con attenzione a diritto, sicurezza, occupazione, società, diplomazia e strutture di potere.",
        "terms": ["israel","israele","palestin","gaza","cisgiord","west bank","unrwa","idf","netanyahu","hamas","settler","insediament","7 ottobre","710"],
    },
    "sanzioni-lawfare": {
        "name": "Sanzioni e lawfare",
        "file": "sanzioni-lawfare.html",
        "title": "Sanzioni e lawfare — Analisi di Emir Alili",
        "description": "Dossier di Emir Alili su OFAC, sanzioni secondarie, liste nere, banche, diritto internazionale e strumenti giuridico-finanziari di potere.",
        "intro": "Un percorso sui dispositivi giuridici, finanziari e amministrativi usati come strumenti di pressione internazionale.",
        "terms": ["sanzion","ofac","lawfare","lista nera","blacklist","fincen","section 311","dollaro","banca","bank","icj","cpi","corte","interpol","terroris","patriot act","swift"],
    },
    "energia-rotte": {
        "name": "Energia, Hormuz e rotte",
        "file": "energia-rotte.html",
        "title": "Energia, Hormuz e rotte — Dossier di Emir Alili",
        "description": "Analisi di Emir Alili su petrolio, gas, Stretto di Hormuz, Bab el-Mandeb, Suez, shipping, raffinerie e sicurezza delle rotte.",
        "intro": "Energia e geografia come strumenti di potere: petrolio, gas, stretti, porti, shipping e corridoi logistici.",
        "terms": ["petrol","gas","energia","hormuz","bab el-mandeb","suez","shipping","petrolier","lng","carburant","raffiner","rotta","corridoio","porto","stretto","diesel","pipeline"],
    },
    "russia-cina-nato": {
        "name": "Russia, Cina e NATO",
        "file": "russia-cina-nato.html",
        "title": "Russia, Cina e NATO — Analisi di Emir Alili",
        "description": "Dossier di Emir Alili su Russia, Cina, NATO, Ucraina, Stati Uniti, riarmo, tecnologia e trasformazione dell'ordine internazionale.",
        "intro": "Analisi dei rapporti di forza tra Russia, Cina, NATO, Stati Uniti ed Europa, dalle guerre alla tecnologia strategica.",
        "terms": ["russia","mosca","ucrain","cina","pechino","nato","pentagono","stati uniti","brics","riarmo","drone","semicondutt","chip","artico","corea del nord","pyongyang"],
    },
    "balcani-macedonia": {
        "name": "Balcani e Macedonia",
        "file": "balcani-macedonia.html",
        "title": "Balcani e Macedonia — Dossier di Emir Alili",
        "description": "Analisi di Emir Alili su Macedonia del Nord, Serbia, Kosovo, Bosnia, Albania, Balcani, diaspora e rapporti regionali.",
        "intro": "Un archivio dedicato ai Balcani e alla Macedonia del Nord: finanza, sicurezza, identità, integrazione europea e rapporti regionali.",
        "terms": ["macedonia","skopje","serbia","serbo","kosovo","bosnia","balcan","albania","bulgaria","grecia","mavrovo","ungheria","eximbank","mladic"],
    },
}
EXCLUDE = {"index.html","analisi.html","chi-sono.html","contatti.html","libri-media.html","metodo.html","impegno.html","cosa-faccio.html","news.html","privacy-cookie.html","admin.html","article.html"}

def extract(pattern, s, flags=re.I|re.S):
    m = re.search(pattern, s, flags)
    return html.unescape(m.group(1).strip()) if m else ""

def article_meta(path):
    s = path.read_text(encoding="utf-8")
    if 'class="report-body"' not in s or 'class="report"' not in s:
        return None
    title = extract(r'<h1[^>]*>(.*?)</h1>', s)
    kicker = extract(r'<p class="kicker"[^>]*>(.*?)</p>', s)
    desc = extract(r'<meta name="description" content="([^"]*)"', s)
    canonical = extract(r'<link rel="canonical" href="([^"]+)"', s) or f"https://emiralili.it/{path.name}"
    image = extract(r'<meta property="og:image" content="([^"]+)"', s)
    published = extract(r'<meta property="article:published_time" content="([^"]+)"', s)
    modified = extract(r'<meta property="article:modified_time" content="([^"]+)"', s)
    combined = " ".join([path.stem, title, kicker, desc]).lower()
    topic_keys=[]
    for key,cfg in TOPICS.items():
        if any(term in combined for term in cfg["terms"]):
            topic_keys.append(key)
    return {"path": path, "html": s, "title": title, "kicker": kicker, "desc": desc, "canonical": canonical, "image": image, "published": published, "modified": modified, "topics": topic_keys}

def topic_box(keys):
    if not keys:
        return ""
    links = "".join(f'<a href="/{TOPICS[k]["file"]}">{html.escape(TOPICS[k]["name"])}</a>' for k in keys[:3])
    return '<nav class="topic-context" aria-label="Percorsi tematici"><span>Percorsi tematici</span><div>'+links+'</div></nav>'

AUTHOR_BOX = '''<aside class="author-entity-box" aria-label="Informazioni sull'autore">
<img src="/assets/img/Emir primo piano.jpg" alt="Emir Alili, autore e analista geopolitico" width="640" height="640" loading="lazy">
<div><p class="author-kicker">Autore</p><h2>Emir Alili</h2>
<p>Autore e analista geopolitico. Su emiralili.it pubblica dossier documentati su rapporti di forza, Medio Oriente, sanzioni, energia, sicurezza internazionale e Balcani.</p>
<div class="author-links"><a href="/chi-sono.html">Profilo autore</a><a href="/libri-media.html">Libri e media</a><a href="/contatti.html">Canali ufficiali</a></div></div>
</aside>'''

def normalize_jsonld(s, topics):
    def repl(m):
        raw=m.group(1)
        try:
            data=json.loads(raw)
        except Exception:
            return m.group(0)
        targets=[]
        if isinstance(data, dict) and data.get("@type")=="NewsArticle":
            targets=[data]
        elif isinstance(data, dict) and isinstance(data.get("@graph"), list):
            targets=[x for x in data["@graph"] if isinstance(x,dict) and x.get("@type")=="NewsArticle"]
        if not targets:
            return m.group(0)
        for obj in targets:
            obj["author"]=AUTHOR
            pub=obj.get("publisher")
            if not isinstance(pub,dict):
                pub={}
            pub.update({"@type":"Organization","name":"Emir Alili","url":"https://emiralili.it/","logo":{"@type":"ImageObject","url":"https://emiralili.it/assets/brand/emir-alili-logo.png","width":512,"height":512}})
            obj["publisher"]=pub
            if topics:
                obj["about"]=[{"@type":"Thing","name":TOPICS[k]["name"],"url":"https://emiralili.it/"+TOPICS[k]["file"]} for k in topics[:3]]
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(",",":"))+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, s, flags=re.S|re.I)

def enhance_article(item):
    s=item["html"]
    s=re.sub(r'<meta name="author" content="[^"]*">','<meta name="author" content="Emir Alili">',s,flags=re.I)
    s=normalize_jsonld(s,item["topics"])
    if 'href="/authority.css' not in s and 'href="authority.css' not in s:
        s=s.replace('</head>','<link rel="stylesheet" href="/authority.css?v=1"></head>',1)
    s=re.sub(r'<nav class="topic-context".*?</nav>','',s,flags=re.S)
    s=re.sub(r'<aside class="author-entity-box".*?</aside>','',s,flags=re.S)
    s=s.replace('</article>',topic_box(item["topics"])+AUTHOR_BOX+'</article>',1)
    if 'src="/menu.js' not in s and 'src="menu.js' not in s:
        s=s.replace('</body>','<script src="/menu.js?v=2"></script></body>',1)
    item["path"].write_text(s,encoding="utf-8")

def card(a):
    tag=html.escape(a["kicker"] or "Dossier")
    title=html.escape(a["title"])
    desc=html.escape((a["desc"] or "")[:240])
    href=html.escape(a["path"].name)
    time=(a["published"] or a["modified"] or "")[:10]
    img=(f'<img src="{html.escape(a["image"])}" alt="Copertina del dossier {title}" loading="lazy">' if a["image"] else "")
    return f'<a class="geo-card authority-card" href="/{href}">{img}<span>{tag}</span><time datetime="{time}">{time}</time><h3>{title}</h3><p>{desc}</p><b>Leggi il dossier →</b></a>'

def pillar_page(key, articles):
    cfg=TOPICS[key]
    ordered=sorted(articles,key=lambda a:a["published"] or a["modified"] or "",reverse=True)
    cards="\n".join(card(a) for a in ordered)
    itemlist=[{"@type":"ListItem","position":i+1,"url":a["canonical"],"name":a["title"]} for i,a in enumerate(ordered)]
    data={"@context":"https://schema.org","@type":"CollectionPage","@id":f'https://emiralili.it/{cfg["file"]}#page',"url":f'https://emiralili.it/{cfg["file"]}',"name":cfg["name"],"description":cfg["description"],"inLanguage":"it-IT","author":AUTHOR,"about":{"@type":"Thing","name":cfg["name"]},"mainEntity":{"@type":"ItemList","itemListElement":itemlist}}
    return f'''<!doctype html><html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(cfg["title"])}</title><meta name="description" content="{html.escape(cfg["description"])}">
<meta name="author" content="Emir Alili"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="https://emiralili.it/{cfg["file"]}"><meta property="og:type" content="website"><meta property="og:site_name" content="Emir Alili"><meta property="og:title" content="{html.escape(cfg["title"])}"><meta property="og:description" content="{html.escape(cfg["description"])}"><meta property="og:url" content="https://emiralili.it/{cfg["file"]}">
<link rel="icon" href="/favicon.ico"><link rel="manifest" href="/manifest.json"><link rel="stylesheet" href="/editorial.css?v=5"><link rel="stylesheet" href="/authority.css?v=1">
<script type="application/ld+json">{json.dumps(data,ensure_ascii=False,separators=(",",":"))}</script></head><body class="hub-page authority-hub">
<header><a class="logo" href="/"><span>EA</span><b>Emir Alili</b></a><nav><a href="/">Home</a><a href="/chi-sono.html">Chi sono</a><a href="/analisi.html">Geopolitica</a><a href="/libri-media.html">Libri</a><a href="/contatti.html">Contatti</a></nav><button class="menu" aria-label="Apri menu" aria-expanded="false"><i></i><i></i></button></header>
<div class="mobile-nav"><a href="/">Home</a><a href="/chi-sono.html">Chi sono</a><a href="/analisi.html">Geopolitica</a><a href="/libri-media.html">Libri</a><a href="/contatti.html">Contatti</a></div>
<main><section class="hub-hero authority-hero"><p class="kicker">Percorso tematico · Emir Alili</p><h1>{html.escape(cfg["name"])}</h1><p>{html.escape(cfg["intro"])}</p><div class="authority-byline"><a href="/chi-sono.html">A cura di Emir Alili — profilo autore ↗</a></div></section>
<section class="authority-related"><p class="section-tag">Dossier collegati</p><h2>{len(ordered)} analisi nel percorso</h2><div class="geo-grid authority-grid">{cards}</div></section>{AUTHOR_BOX}</main>
<footer><p>© 2026 Emir Alili</p><a href="/analisi.html">Tutte le analisi ↑</a></footer><script src="/menu.js?v=2"></script></body></html>'''

def update_analisi():
    p=ROOT/"analisi.html"
    if not p.exists(): return
    s=p.read_text(encoding="utf-8")
    block='''<!-- TOPIC-HUBS:START --><section class="topic-hub-strip" aria-labelledby="topic-hubs-title"><div><p class="section-tag">Percorsi tematici</p><h2 id="topic-hubs-title">Segui un tema.</h2><p>Sei archivi ragionati collegano i dossier per area e aiutano a seguire nel tempo gli stessi rapporti di forza.</p></div><nav aria-label="Percorsi tematici principali">''' + ''.join(f'<a href="/{cfg["file"]}"><strong>{html.escape(cfg["name"])}</strong><span>Apri il percorso →</span></a>' for cfg in TOPICS.values()) + '''</nav></section><!-- TOPIC-HUBS:END -->'''
    if '<!-- TOPIC-HUBS:START -->' in s:
        s=re.sub(r'<!-- TOPIC-HUBS:START -->.*?<!-- TOPIC-HUBS:END -->',block,s,flags=re.S)
    else:
        s=s.replace('<section class="archive-browser"',block+'<section class="archive-browser"',1)
    if 'href="/authority.css' not in s:
        s=s.replace('</head>','<link rel="stylesheet" href="/authority.css?v=1"></head>',1)
    if 'src="/menu.js' not in s and 'src="menu.js' not in s:
        s=s.replace('</body>','<script src="/menu.js?v=2"></script></body>',1)
    p.write_text(s,encoding="utf-8")

def update_sitemap():
    p=ROOT/"sitemap.xml"
    if not p.exists(): return
    s=p.read_text(encoding="utf-8")
    for cfg in TOPICS.values():
        loc=f'https://emiralili.it/{cfg["file"]}'
        if loc not in s:
            row=f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n'
            s=s.replace('</urlset>',row+'</urlset>')
    p.write_text(s,encoding="utf-8")

def main():
    articles=[]
    for p in ROOT.glob("*.html"):
        if p.name in EXCLUDE: continue
        item=article_meta(p)
        if item: articles.append(item)
    for a in articles: enhance_article(a)
    for key,cfg in TOPICS.items():
        (ROOT/cfg["file"]).write_text(pillar_page(key,[a for a in articles if key in a["topics"]]),encoding="utf-8")
    update_analisi(); update_sitemap()
    print(f"Enhanced {len(articles)} dossier pages")
    for key,cfg in TOPICS.items(): print(cfg["name"],sum(key in a["topics"] for a in articles))

if __name__=="__main__": main()
