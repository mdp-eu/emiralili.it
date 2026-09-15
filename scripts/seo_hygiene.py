#!/usr/bin/env python3
from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-16"

NOINDEX = {
    "admin.html": "noindex,nofollow",
    "preventivi.html": "noindex,nofollow",
    "blog.html": "noindex,follow",
    "share.html": "noindex,follow",
    "article.html": "noindex,follow",
    "libri-media.html": "noindex,follow",
    "metodo.html": "noindex,follow",
    "press.html": "noindex,follow",
    "cosa-faccio.html": "noindex,follow",
    "impegno.html": "noindex,follow",
}

EXCLUDE_FROM_SITEMAP = set(NOINDEX) | {"404.html"}
TOPIC_PAGES = {
    "medio-oriente.html", "palestina-israele.html", "sanzioni-lawfare.html",
    "energia-rotte.html", "russia-cina-nato.html", "balcani-macedonia.html",
}

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

def canonical_for(path, source):
    if path.name == "index.html":
        return "https://emiralili.it/"
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', source, re.I)
    if not m:
        m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', source, re.I)
    if m and m.group(1).startswith("https://emiralili.it/"):
        return m.group(1).split('#')[0]
    return f"https://emiralili.it/{path.name}"

def lastmod_for(source):
    for key in ("dateModified", "datePublished"):
        m = re.search(rf'["\']{key}["\']\s*:\s*["\'](\d{{4}}-\d{{2}}-\d{{2}})', source)
        if m: return m.group(1)
    m = re.search(r'<time[^>]+datetime=["\'](\d{4}-\d{2}-\d{2})', source, re.I)
    return m.group(1) if m else TODAY

def priority_for(name):
    if name == "index.html": return "1.0"
    if name in {"analisi.html", "chi-sono.html"} or name in TOPIC_PAGES: return "0.9"
    if name == "contatti.html": return "0.6"
    if name == "privacy-cookie.html": return "0.3"
    return "0.8"

def rebuild_sitemap():
    entries = []
    seen = set()
    for path in sorted(ROOT.glob("*.html")):
        if path.name in EXCLUDE_FROM_SITEMAP:
            continue
        source = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', source, re.I):
            continue
        url = canonical_for(path, source)
        if url in seen:
            continue
        seen.add(url)
        entries.append((url, lastmod_for(source), priority_for(path.name)))
    entries.sort(key=lambda x: (0 if x[0] == "https://emiralili.it/" else 1, x[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, priority in entries:
        lines.append(f'  <url><loc>{escape(url)}</loc><lastmod>{lastmod}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>')
    lines.append('</urlset>')
    content = '\n'.join(lines) + '\n'
    path = ROOT / 'sitemap.xml'
    old = path.read_text(encoding='utf-8') if path.exists() else ''
    if content != old:
        path.write_text(content, encoding='utf-8')
        return len(entries), True
    return len(entries), False

def main():
    changed=[]
    for filename,directive in NOINDEX.items():
        if set_noindex(filename,directive): changed.append(filename)
    count, sitemap_changed = rebuild_sitemap()
    print('SEO hygiene: noindex updated:', ', '.join(changed) if changed else 'none')
    print('SEO hygiene: sitemap URLs:', count)
    print('SEO hygiene: sitemap rebuilt:', sitemap_changed)

if __name__ == '__main__': main()
