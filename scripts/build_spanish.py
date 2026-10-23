"""Build static Spanish pages from the current English pages and translations/es.json.

Run from any directory: python scripts/build_spanish.py
New visible English copy must have a translation before this build can pass.
"""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = json.loads((ROOT / 'translations/es.json').read_text(encoding='utf-8-sig'))
BRAND_TEXT = {'BENNY’S', 'TREE SERVICE', 'Benny’s Tree Service', 'Benny’s Tree Service.', '©'}

class SpanishPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.in_script = False
        self.in_prompt = False

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')

    def handle_comment(self, data):
        self.output.append('<!--' + data + '-->')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        # Spanish pages do not need a suggestion to switch to Spanish.
        if tag == 'aside' and a.get('class') == 'language-prompt':
            self.in_prompt = True
        if self.in_prompt:
            return
        if tag == 'script':
            self.in_script = True
        if tag == 'html':
            a['lang'] = 'es'
        for key in ('alt', 'aria-label', 'content'):
            if key in a:
                a[key] = TRANSLATIONS.get(a[key], a[key])
        if a.get('class') == 'language-switch':
            a.update(href='../' + a['href'].split('/')[-1], lang='en', hreflang='en',
                     **{'data-language-choice': 'en', 'aria-label': 'View this page in English'})
        for key in ('href', 'src'):
            value = a.get(key, '')
            if value.startswith(('assets/', 'styles.css', 'script.js')):
                a[key] = '../' + value
        if 'srcset' in a:
            a['srcset'] = a['srcset'].replace('assets/', '../assets/')
        if tag == 'meta' and a.get('property') == 'og:locale':
            a['content'] = 'es_US'
        self.output.append('<' + tag + ''.join(' ' + key + ('' if value is None else '="' + escape(value, quote=True) + '"') for key, value in a.items()) + '>')

    def handle_endtag(self, tag):
        if self.in_prompt:
            if tag == 'aside':
                self.in_prompt = False
            return
        self.output.append('</' + tag + '>')
        if tag == 'script':
            self.in_script = False

    def handle_data(self, data):
        if self.in_prompt:
            return
        if self.in_script:
            self.output.append(data)
            return
        text = data.strip()
        if text == 'Español':
            translated = 'English'
        elif text in TRANSLATIONS:
            translated = TRANSLATIONS[text]
        elif not text or text in BRAND_TEXT or not re.search(r'[A-Za-z]', text):
            translated = text
        else:
            raise ValueError('Missing Spanish translation: ' + repr(text))
        self.output.append(escape(data.replace(text, translated, 1) if text else data, quote=False))


def translate_values(value):
    if isinstance(value, dict):
        return {key: translate_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [translate_values(item) for item in value]
    if isinstance(value, str):
        return TRANSLATIONS.get(value, value)
    return value

for name in ('index.html', 'contact.html'):
    source = (ROOT / name).read_text(encoding='utf-8')
    parser = SpanishPage()
    parser.feed(source)
    output = ''.join(parser.output)
    en_url = 'https://bennystreeservices.com/' + ('' if name == 'index.html' else name)
    es_url = 'https://bennystreeservices.com/es/' + ('' if name == 'index.html' else name)
    output = output.replace('rel="canonical" href="' + en_url + '"', 'rel="canonical" href="' + es_url + '"')
    output = output.replace('property="og:url" content="' + en_url + '"', 'property="og:url" content="' + es_url + '"')
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', output, re.S)
    schema = translate_values(json.loads(match[1]))
    page = schema['@graph'][-1]
    page.update({'@id': es_url + '#webpage', 'url': es_url, 'inLanguage': 'es'})
    output = output[:match.start(1)] + '\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n' + output[match.end(1):]
    (ROOT / 'es' / name).write_text(output, encoding='utf-8')
    print('Built es/' + name)
