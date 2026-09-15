#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"admin.html", "article.html", "blog.html", "preventivi.html", "share.html"}
LINKS = [
    ("Home", "/"),
    ("Analisi", "/analisi.html"),
    ("Autore", "/chi-sono.html"),
    ("Libri", "/libri-media.html"),
    ("Metodo", "/metodo.html"),
    ("Press", "/press.html"),
    ("Contatti", "/contatti.html"),
]
TOPIC_PAGES = {
    "medio-oriente.html", "palestina-israele.html", "sanzioni-lawfare.html",
    "energia-rotte.html", "russia-cina-nato.html", "balcani-macedonia.html",
}
HEADER_RE = re.compile(r'(<header\b[^>]*>)(.*?)(</header>)', re.I | re.S)
NAV_RE = re.compile(r'<nav\b[^>]*>.*?</nav>', re.I | re.S)
MOBILE_RE = re.compile(r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bmobile-nav\b[^"\']*["\'])[^>]*>.*?</div>', re.I | re.S)
MENU_SCRIPT_RE = re.compile(r'<script\b[^>]*\bsrc=["\']/?menu\.js(?:\?v=[^"\']*)?["\'][^>]*></script>', re.I | re.S)
A_RE = re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')

def active_label(path: Path, source: str):
    name = path.name
    if name == "index.html": return "Home"
    if name == "analisi.html" or name in TOPIC_PAGES or 'class="report-body"' in source or 'class="report"' in source: return "Analisi"
    if name in {"chi-sono.html", "cosa-faccio.html", "impegno.html"}: return "Autore"
    if name == "libri-media.html": return "Libri"
    if name == "metodo.html": return "Metodo"
    if name == "press.html": return "Press"
    if name == "contatti.html": return "Contatti"
    return None

def menu_html(active=None):
    return '<nav aria-label="Navigazione principale">' + ''.join(
        f'<a href="{href}"' + (' aria-current="page"' if label == active else '') + f'>{label}</a>'
        for label, href in LINKS
    ) + '</nav>'

def mobile_html(active=None):
    return '<div class="mobile-nav" aria-label="Navigazione mobile">' + ''.join(
        f'<a href="{href}"' + (' aria-current="page"' if label == active else '') + f'>{label}</a>'
        for label, href in LINKS
    ) + '</div>'

def signature(source: str):
    h = HEADER_RE.search(source)
    if not h: return None
    n = NAV_RE.search(h.group(2))
    if not n: return None
    return tuple((TAG_RE.sub('', body).strip(), href) for href, body in A_RE.findall(n.group(0)))

def normalize(path: Path):
    source = path.read_text(encoding="utf-8", errors="ignore")
    active = active_label(path, source)
    canonical_nav, canonical_mobile = menu_html(active), mobile_html(active)
    changed = False
    h = HEADER_RE.search(source)
    if h:
        inside = h.group(2)
        if NAV_RE.search(inside):
            new_inside = NAV_RE.sub(canonical_nav, inside, count=1)
        else:
            button = re.search(r'<button\b[^>]*\bclass=["\'][^"\']*\bmenu\b[^"\']*["\'][^>]*>', inside, re.I)
            new_inside = inside[:button.start()] + canonical_nav + inside[button.start():] if button else inside + canonical_nav
        new_header = h.group(1) + new_inside + h.group(3)
        if new_header != h.group(0):
            source = source[:h.start()] + new_header + source[h.end():]
            changed = True
    if MOBILE_RE.search(source):
        new_source = MOBILE_RE.sub(canonical_mobile, source, count=1)
        if new_source != source: source, changed = new_source, True
    elif h:
        h2 = HEADER_RE.search(source)
        source = source[:h2.end()] + canonical_mobile + source[h2.end():]
        changed = True

    canonical_script = '<script src="/menu.js?v=4"></script>'
    if MENU_SCRIPT_RE.search(source):
        new_source = MENU_SCRIPT_RE.sub(canonical_script, source)
        if new_source != source: source, changed = new_source, True
    elif '</body>' in source:
        source = source.replace('</body>', canonical_script + '</body>', 1)
        changed = True

    if changed: path.write_text(source, encoding="utf-8")
    return changed

def main():
    pages = [p for p in sorted(ROOT.glob('*.html')) if p.name not in EXCLUDE]
    before = {}
    for p in pages:
        sig = signature(p.read_text(encoding='utf-8', errors='ignore'))
        before.setdefault(sig, []).append(p.name)
    changed = sum(1 for p in pages if normalize(p))
    after = {}
    for p in pages:
        sig = signature(p.read_text(encoding='utf-8', errors='ignore'))
        after.setdefault(sig, []).append(p.name)
    print(f'Navigation audit: {len(pages)} editorial/public root HTML pages')
    print(f'Desktop menu variants before: {len(before)}')
    for i,(sig,names) in enumerate(sorted(before.items(), key=lambda x: -len(x[1])),1):
        print(f'  before {i}: {len(names)} pages -> {sig}')
        if sig is None: print('    no-header/no-nav:', ', '.join(names))
    print(f'Pages normalized: {changed}')
    print(f'Desktop menu variants after: {len(after)}')
    for i,(sig,names) in enumerate(sorted(after.items(), key=lambda x: -len(x[1])),1):
        print(f'  after {i}: {len(names)} pages -> {sig}')
        if sig is None: print('    no-header/no-nav:', ', '.join(names))

if __name__ == '__main__': main()
