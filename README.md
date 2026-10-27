# AIforPsy storefront

The existing production site is a static, responsive sales storefront deployed from `dist/` on Netlify. Purchase and product delivery remain on TA-Next Academy.

## Languages

`locales.json` defines the supported languages in display/build order: Ukrainian (`uk`), English (`en`), Russian (`ru`). Ukrainian is the default at `/`; each language also has its explicit route. Every page has the same ordered language selector, localized accessibility labels, canonical link, three language alternates, and a Ukrainian `x-default`. Changing languages preserves the current page: home, catalog, product, or privacy.

Use standard BCP 47 language code `uk` for Ukrainian routes and document metadata; its compact menu label is `UA`. No client-side language detection, cookies, or mixed-language copy fallback is used. Missing translation dictionaries fail the build.

## Develop

Requires Python 3.12+. Run `python3 build.py` to regenerate all supported languages. Serve `dist/` with a static server for local review. Netlify publishes the committed files; no backend or new framework is required.

Content sources:
- `copy-approved.json`: complete homepage service copy.
- `card-introductions.json`: approved introductory text overrides.
- `locales.json`: shared navigation, accessibility, dialog and homepage labels.
- `products.json`: catalog/product marketing copy, videos, and external purchase URL.
- `privacy.json`: complete localized privacy policies; existing English/Russian policy wording is preserved.

Renderers: `build.py`, `build_products.py`, `build_privacy.py`, and shared `localization.py`.

Styles and scripts in `dist/` are tracked source assets. `style.css` and `app.js` retain the existing homepage design and interactions. `language.css` and `language.js` add the shared language dropdown; `products.css` and `products.js` cover catalog/product pages. Do not delete these assets before building.

Desktop shows four service cards; mobile uses four compact, initially collapsed accordions. Hero imagery, colors, and established layout are retained. Support contact: `support@aiforpsy.net`.

See `PRODUCTS.md` for the external purchase architecture and retired-route handling. Never restore local course, checkout, or access logic to this storefront.
