#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-15"

NOINDEX = {
    "admin.html": "noindex,nofollow",
    "preventivi.html": "noindex,nofollow",
    "blog.html": "noindex,follow",
    "share.html": "noindex,follow",
}

CORE_URLS = [
    ("https://emiralili.it/", "1.0"),
    ("https://emiralili.it/analisi.html", "0.9"),
    ("https://emiralili.it/chi-sono.html", "0.9"),
    ("https://emiralili.it/libri-media.html", "0.8"),
    ("https://emiralili.it/metodo.html", "0.8"),
    ("https://emiralili.it/press.html", "0.9"),
    ("https://emiralili.it/contatti.html", "0.7"),
    ("https://emiralili.it/medio-oriente.html", "0.9"),
    ("https://emiralili.it/palestina-israele.html", "0.9"),
    ("https://emiralili.it/sanzioni-lawfare.html", "0.9"),
    ("https://emiralili.it/energia-rotte.html", "0.9"),
    ("https://emiralili.it/russia-cina-nato.html", "0.9"),
    ("https://emiralili.it/balcani-macedonia.html", "0.9"),
]

def set_noindex(filename, directive):
    path = ROOT / filename
    if not path.exists(): return False
    s = path.read_text(encoding="utf-8", errors="ignore")
    meta = f'<meta name="robots" content="{directive}">'
    if re.search(r'<meta\s+name=["\']robots["\'][^>]*>', s, re.I):
        ns = re.sub(r'<meta\s+name=["\']robots["\'][^>]*>', meta, s, count=1, flags=re.I)
    elif '</head>' in s:
        ns = s.replace('</head>', meta + '</head>', 1)
    else:
        return False
    if ns != s:
        path.write_text(ns, encoding="utf-8")
        return True
    return False

def ensure_sitemap():
    path = ROOT / 'sitemap.xml'
    if not path.exists(): return 0
    s = path.read_text(encoding='utf-8')
    added=[]
    for url, priority in CORE_URLS:
        if f'<loc>{url}</loc>' in s: continue
        added.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>')
    if added:
        block='\n' + '\n'.join(added) + '\n'
        s=s.replace('</urlset>', block + '</urlset>')
        path.write_text(s, encoding='utf-8')
    return len(added)

def main():
    changed=[]
    for filename,directive in NOINDEX.items():
        if set_noindex(filename,directive): changed.append(filename)
    added=ensure_sitemap()
    print('SEO hygiene: noindex updated:', ', '.join(changed) if changed else 'none')
    print('SEO hygiene: core sitemap URLs added:', added)

if __name__ == '__main__': main()
