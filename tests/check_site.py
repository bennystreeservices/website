"""Validate all four static pages, language metadata and local link targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ['index.html', 'contact.html', 'es/index.html', 'es/contact.html']

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.alternates = {}
        self.canonical = None
        self.language = None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate id: ' + a['id']
            self.ids.add(a['id'])
        if tag == 'html': self.language = a['lang']
        if tag in ['a', 'link'] and a.get('href'): self.refs.append(a['href'])
        if tag in ['img', 'script'] and a.get('src'): self.refs.append(a['src'])
        if tag == 'img':
            assert a.get('alt') and a.get('width') and a.get('height')
            for source in a.get('srcset', '').split(','):
                if source.strip(): self.refs.append(source.strip().split()[0])
        if tag == 'link' and a.get('rel') == 'alternate': self.alternates[a['hreflang']] = a['href']
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']

pages = {file: Page((ROOT / file).read_text(encoding='utf-8')) for file in FILES}
for file, page in pages.items():
    source = (ROOT / file).read_text(encoding='utf-8')
    assert '\u2014' not in source
    lang = 'es' if file.startswith('es/') else 'en'
    assert page.language == lang
    assert set(page.alternates) == {'en', 'es', 'x-default'}
    assert page.canonical == page.alternates[lang]
    assert page.alternates == pages[('' if lang == 'es' else 'es/') + Path(file).name].alternates
    data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)[1])
    assert data['@graph'][0]['telephone'] == '+17082968946'
    assert data['@graph'][-1]['inLanguage'].startswith(lang)
    for ref in page.refs:
        u = urlsplit(ref)
        if u.scheme in ['tel', 'sms']:
            assert u.path in ['+17082968946', '+17086925590']
            continue
        if u.scheme and u.hostname != 'bennystreeservices.com': continue
        target = ROOT / unquote(u.path.lstrip('/')) if u.scheme or u.path.startswith('/') else ROOT / Path(file).parent / unquote(u.path)
        if not u.path: target = ROOT / file
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), (file, ref)
        if u.fragment:
            relative = target.resolve().relative_to(ROOT).as_posix()
            if relative in pages: assert u.fragment in pages[relative].ids, (file, ref)
    print('PASS:', file, 'language metadata, local links, assets, contact numbers and JSON-LD')
assert (ROOT / 'CNAME').read_text().strip() == 'bennystreeservices.com'
