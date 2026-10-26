# AIforPsy product storefront

The existing AIforPsy repository is a static bilingual sales storefront deployed on Netlify. Payments, customer access, lessons, and materials belong to TA-Next Academy.

## Build

Use Python 3.12+ and run `python3 build.py`. Netlify publishes committed `dist/`; no build dependency, API, or account system is required. Existing homepage, privacy pages, shared styles, header, and footer are preserved.

`products.json` is the catalog and sales-content configuration. Only `status: published` items appear in the catalog. AI Secretary remains draft.

## Public routes (both /ru and /en)

- `/save-time/`: existing product catalog.
- `/products/personal-ai-operations-director/`: existing sales page, including hero, description, benefits, explainer video, testimonials, and purchase CTAs.

The previous hub, setup paths, payment status pages, private preview generator, download handlers, and access function have been removed. Netlify redirects retired product URLs to the same-language sales page; they do not grant access or start a purchase. There are no paid files in the public deployment.

## External purchase destination

Set **one** `externalPurchaseUrl` on `products[0]` to the exact, verified HTTPS mirror-product URL on `ta-next.com` (or `www.ta-next.com`). The configured destination is the exact mirror-product URL supplied by the owner, including its `share_version` parameter. Both purchase CTAs render as ordinary links to TA-Next Academy; only the existing `lang` query parameter follows the current page language. If the URL is cleared to `null`, CTAs stay visible but disabled and the existing not-yet-available notice is shown. No production path is guessed.

After setting the URL, rebuild and verify both language pages, both CTAs, and the destination. No payment keys, checkout session, webhook, entitlement, database, or AIforPsy success/cancel flow should be introduced. Purchase and delivery remain entirely on TA-Next Academy.

## Public videos and content

`explainerYouTubeUrl` and `testimonialYouTubeUrl` retain their existing behavior and placeholders. `testimonialMode` accepts `link` or `embed`. Approved RU/EN sales copy and product-includes data remain unchanged. No translation or extra section has been introduced.
