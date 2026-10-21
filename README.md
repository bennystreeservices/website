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

Business details were supplied by the owner: Bedford Park and surrounding Chicagoland; tree removal, trimming and pruning, stump removal; family-operated; licensed and insured; free estimates. No hours, street address, email, emergency availability, or additional services were provided.

Preview with `python -m http.server 8000`, then visit http://localhost:8000.

## Mobile and Google setup

The mobile contact bar reserves its height, including device safe areas. Both pages use a viewport-height layout so short pages keep the footer at the bottom. Phone and text actions work without JavaScript. Native `details` elements provide keyboard-accessible answers.

See `GOOGLE-SETUP.md` for the remaining Google Business Profile and Search Console steps. Real profile URLs and verification tokens must come from the owner’s Google account. No Google account has been created or connected by this code change.

Responsive checks covered both pages at 320, 360, 390, 430, 700, 768, 1024 and 1440 CSS pixels. At each width the document fit the viewport, the phone/SMS targets matched, the footer did not leave a gap, and the mobile contact bar appeared only at its intended breakpoint.
