# Benny's Tree Service

Two static pages hosted on GitHub Pages from `main`, repository root.
The `CNAME` file preserves bennystreeservices.com. No build step or paid services.

## Editing
- `index.html`: services, project photographs, and business introduction.
- `contact.html`: telephone and SMS contact details.
- `styles.css`: shared responsive design.
- `script.js`: updates the copyright year; contact links work without JavaScript.
- `assets/originals/`: unmodified supplied artwork and photographs.
- `assets/`: optimized WebP versions in two sizes, plus `share-1200x630.jpg` (link preview image), `apple-touch-icon.png` and `favicon-48.png`, all generated from `assets/originals/logo.png`.

Add gallery photographs by copying an existing `figure` in `.gallery`, updating its image sources, dimensions, descriptive alt text, and accurate caption. Preserve original files and export optimized WebP sizes. Do not describe an image as finished work unless that is confirmed.

Business details were supplied by the owner: Western Spring and surrounding areas; tree removal, trimming and pruning, stump removal; family-operated; licensed and insured; free estimates. No hours, street address, email, emergency availability, or additional services were provided.

Preview with `python -m http.server 8000`, then visit http://localhost:8000.

## Mobile and Google setup

The mobile contact bar reserves its height, including device safe areas. Both pages use a viewport-height layout so short pages keep the footer at the bottom. Phone and text actions work without JavaScript. Native `details` elements provide keyboard-accessible answers.

See `GOOGLE-SETUP.md` for the remaining Google Business Profile and Search Console steps. Real profile URLs and verification tokens must come from the owner’s Google account. No Google account has been created or connected by this code change.

Responsive checks covered both pages at 320, 360, 390, 430, 700, 768, 1024 and 1440 CSS pixels. At each width the document fit the viewport, the phone/SMS targets matched, the footer did not leave a gap, and the mobile contact bar appeared only at its intended breakpoint.

## English and Spanish

- English: `index.html`, `contact.html`.
- Spanish: `es/index.html`, `es/contact.html`, with their own canonical URLs and reciprocal language metadata.
- Edit English copy normally, then update the matching entries in `translations/es.json` and run `python scripts/build_spanish.py`. The generator fails if visible copy is missing a Spanish translation, so both versions stay in sync. Brand names and phone numbers stay the same.
- A header link switches languages and works without JavaScript. The script remembers an explicit choice when browser storage is available. An English page offers a dismissible Spanish suggestion when Spanish is the browser's first preferred language. It never reads keyboard settings and never auto-translates based solely on browser language.
- Dismissal lasts for the current browser tab session. The language switch remains available after dismissal. No translation widget, external translation service, or added tracking is used.
- Run `node --test tests/language.test.cjs` and `python tests/check_site.py` after changes. Commit generated Spanish pages so GitHub Pages needs no build step.

Bilingual browser checks covered all four pages at 320, 360, 390, 430, 700, 768, 1024 and 1440 CSS pixels, with no horizontal overflow. Language switching, Spanish navigation and saved preference redirects were also verified in the browser.

## Reviews and QR placement

The branded website QR is live on the Contact page at `#qr-code`, with PNG and SVG downloads. Every footer links to that section. Its copy explains that it opens the same website, so mobile visitors do not need to scan their own screen. Both English and Spanish versions are generated and validated.

The Google review layout is reserved between About / Why choose Benny’s and the homepage FAQ, with a smaller pair of links on Contact. No review buttons, scores, counts or quotations are published until the exact Google links are verified.

Configure `config/google-reviews.json` with the verified public profile URL and the Google-issued review-form URL, then set `verified` to `true`. Run:

```text
python scripts/build_reviews.py
python scripts/build_spanish.py
python tests/check_site.py
python tests/test_reviews.py
```

The first command inserts real links into the reserved HTML positions and adds the profile to the business schema. The Spanish builder localizes the same component. No external widget, API key or paid service is required. Customers view the current reviews on Google and can open the Google review form directly.

To preview the proposed placement before configuring a listing, run `python scripts/build_reviews.py --preview _reviews-preview.html` and open that page on the local server. It is explicitly labeled as a design preview. Do not commit or deploy the preview file.
