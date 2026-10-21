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
