"""Render Google review links only after the real listing has been verified.

1. Fill config/google-reviews.json with the exact profile and review-form URLs.
2. Set verified=true only after checking the business identity.
3. Run python scripts/build_reviews.py, then python scripts/build_spanish.py.

For a clearly labeled, non-public layout preview:
  python scripts/build_reviews.py --preview _reviews-preview.html
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- GOOGLE_REVIEWS_START -->'
END = '<!-- GOOGLE_REVIEWS_END -->'
ALLOWED_HOSTS = {'google.com', 'www.google.com', 'maps.google.com', 'maps.app.goo.gl', 'g.page', 'g.co'}


def verified_links(config):
    if config.get('verified') is not True:
        return None
    links = []
    for key in ('profile_url', 'write_review_url'):
        value = config.get(key)
        if not isinstance(value, str):
            raise ValueError('A verified configuration needs both Google URLs.')
        url = urlsplit(value)
        if url.scheme != 'https' or url.hostname not in ALLOWED_HOSTS or url.username or url.password or url.path in ('', '/'):
            raise ValueError('Use the exact HTTPS Google listing or review link, not a search or home page.')
        if url.hostname in {'google.com', 'www.google.com'} and not url.path.startswith(('/maps', '/local', '/search')):
            raise ValueError('Use a Google business listing URL.')
        if url.path == '/search':
            raise ValueError('A generic search does not identify a verified Google listing.')
        links.append(value)
    return tuple(links)


def actions(links):
    if links is None:
        return '<div class="review-actions"><span class="button review-preview-button" aria-disabled="true">Read Google reviews</span><span class="text-link" aria-disabled="true">Leave a Google review</span></div>'
    profile, review = map(lambda url: escape(url, quote=True), links)
    return f'<div class="review-actions"><a class="button" href="{profile}">Read Google reviews</a><a class="text-link" href="{review}">Leave a Google review</a></div>'


def review_section(links, preview=False):
    if links is None and not preview:
        return ''
    note = '<p class="review-preview-note">Design preview only. The verified Google listing and review link are still needed. Buttons are inactive in this preview.</p>' if preview else ''
    return f'''<section class="section wrap reviews-section" id="reviews" aria-labelledby="reviews-heading">
  {note}<div class="reviews-layout"><div class="reviews-heading"><p class="eyebrow">CUSTOMER EXPERIENCES</p><h2 id="reviews-heading">A word from our customers.</h2></div><div class="reviews-copy"><p class="reviews-label">Reviews on Google</p><p>Read what customers share on Google. If we’ve worked on your trees, we’d appreciate hearing about your experience.</p>{actions(links)}</div></div>
</section>'''


def contact_section(links):
    if links is None:
        return ''
    return f'''<section class="wrap contact-reviews" aria-labelledby="contact-reviews-heading"><h2 id="contact-reviews-heading">Worked with Benny’s?</h2><p>Your feedback helps neighbors find a local tree service.</p>{actions(links)}</section>'''


def replace_section(source, section):
    if START not in source or END not in source:
        raise ValueError('Missing Google review placement markers.')
    return re.sub(re.escape(START) + r'.*?' + re.escape(END), START + '\n' + section + '\n' + END, source, count=1, flags=re.S)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    config = json.loads((ROOT / 'config/google-reviews.json').read_text(encoding='utf-8-sig'))
    links = verified_links(config)
    if args.preview:
        source = (ROOT / 'index.html').read_text(encoding='utf-8')
        args.preview.write_text(replace_section(source, review_section(None, preview=True)), encoding='utf-8')
        print('Saved labeled layout preview:', args.preview)
        return
    for name, section in [('index.html', review_section(links)), ('contact.html', contact_section(links))]:
        page = ROOT / name
        source = replace_section(page.read_text(encoding='utf-8'), section)
        if links:
            match = re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
            data = json.loads(match[1])
            business = data['@graph'][0]
            business['sameAs'] = list(dict.fromkeys(business.get('sameAs', []) + [links[0]]))
            source = source[:match.start(1)] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n' + source[match.end(1):]
        page.write_text(source, encoding='utf-8')
    print('Google reviews:', 'verified links published in source' if links else 'not configured; no public placeholders or inactive buttons added')


if __name__ == '__main__':
    main()
