# Google local search setup

The website stays on GitHub Pages. Google Sites is a separate website builder and is not needed to appear in Google Search or Maps.

## Already in the code
- Unique page titles, descriptions, HTTPS canonical URLs and social sharing metadata.
- Indexable static HTML, clear service headings and Western Spring and surrounding areas copy.
- Connected business, service, website and page JSON-LD identities on both pages.
- Accurate phone and service area information, optimized responsive images and meaningful alt text.
- XML sitemap at https://bennystreeservices.com/sitemap.xml and robots.txt.
- Mobile call and SMS links, visible content without JavaScript, and native expandable answers.

The business schema describes the confirmed service area. No street address, map pin, opening hours, ratings or license number are invented. Google’s LocalBusiness rich-result requirements include an address, so this service-area markup should not be described as guaranteeing a rich result.

## When the owner is ready
1. HTTPS is configured and verified as of October 21, 2026. GitHub issued a certificate covering bennystreeservices.com and www.bennystreeservices.com, HTTPS enforcement is on, and www redirects to the canonical apex domain. Existing Cloudflare DNS-only CNAME records were already correct and were retained. The certificate request was restarted by removing and re-saving the same domain in GitHub Pages settings. Keep this existing hosting configuration.
2. Create or claim the real Google Business Profile at https://business.google.com/. Use the exact public business name and phone shown here. If customers are not served at the business address, configure a service-area business and hide the address according to Google’s rules. Select the closest accurate tree-service category and only real service areas. The owner must complete Google’s required verification.
3. Add https://bennystreeservices.com/ as the website, confirmed services, actual hours if provided, the supplied logo and original project photos. Keep these details consistent with the website.
4. Supply the verified public Google Maps / Business Profile URL. Add it to the business node’s `sameAs` array on BOTH HTML pages, then add a visible, accurately labeled profile link. Add a review link only after obtaining the actual review URL. Do not use guessed listing IDs or fabricated review stars.
5. Add the domain in https://search.google.com/search-console/. Domain properties need the exact Google-issued DNS TXT verification value; URL-prefix properties can use the exact Google-issued HTML file or meta verification tag. No placeholder verification token has been published. Add the token only when issued, and use the requested verification method.
6. Submit https://bennystreeservices.com/sitemap.xml in Search Console after HTTPS works. Inspect the homepage and contact URL. Review indexing and mobile Core Web Vitals as real usage data becomes available.
7. Ask actual customers for honest reviews and add new real project photos over time. Keep profile information current.

Code can make the business understandable and the site usable. Rankings also depend on relevance, distance and prominence; no ranking position is guaranteed.

Official guidance:
- https://support.google.com/business/answer/7091
- https://support.google.com/business/answer/9157481
- https://developers.google.com/search/docs/appearance/structured-data/local-business
- https://developers.google.com/search/docs/monitor-debug/search-console-start

## Spanish search pages

Spanish versions live at `/es/` and `/es/contact.html`. Both language versions include reciprocal `hreflang` annotations, self-referencing canonical URLs, localized page metadata and page-language structured data. Both Spanish URLs are in the sitemap. These pages translate the website; they do not assert that staff speak a particular language. The business name, service area and primary/secondary phone numbers remain consistent.

## Google reviews integration status (October 28, 2026)

Public searches did not establish a listing matching the supplied primary phone number, (708) 296-8946. Similar business names in other locations are not sufficient verification. No third-party listing was connected.

The homepage review block is designed for the space immediately after About / Why choose Benny’s and before the FAQ. It offers two distinct actions: read Google reviews and leave a Google review. Contact has a compact version. Activation is controlled by `config/google-reviews.json`, initially unverified with no URLs. `scripts/build_reviews.py` leaves the public page unchanged until both exact links have been verified. After activation, rebuild Spanish pages with `python scripts/build_spanish.py`.

Get the actual review-form URL from the owner’s Google Business Profile: Read Reviews, then Get more reviews, then Copy. Also supply the public Google Maps profile link, so visitors can view the listing and its reviews. Verify the listing identity against the phone number and owner-provided details before switching the configuration on.

Official instructions: https://support.google.com/business/answer/16816815?hl=en

The existing branded QR still opens https://bennystreeservices.com/. It is now on the Contact page with download links. It does not open a Google review form and should not be labeled as a review QR. A separate review QR can be generated only after obtaining the correct review-form URL.
