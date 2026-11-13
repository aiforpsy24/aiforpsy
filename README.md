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

## Services direction

The fourth homepage direction opens `/{lang}/services/` directly. Mobile keeps its compact accordion and the Read More link opens the same catalog. It no longer opens the generic project/support dialog. `services.json` and `build_services.py` generate the shared catalog and localized service pages. The existing header/footer and other directions are unchanged.

The photoshoot self-service link goes directly to MARKEVITA. Assisted checkout and booking are still disabled while their isolated TA-Next test workflow is prepared; no live payment is enabled by this storefront update.

### Course-creation event referral

`course-event.json` keeps the permanent catalog card separate from its destination.
Replace only `eventUrl` when the owner supplies a new TA-Next event URL; keep the
card copy and artwork. The build does not expire past events. Verify the destination's
published languages before updating `publishedLanguages` (currently EN/RU only).
The UK homepage and root page remain unchanged; no UK event catalog is generated.

`dist/assets/create-course.webp` is a language-neutral 16:9 derivative of the linked
event's laptop artwork, made with the built-in image generator. Editing instruction:
“Preserve the horizontal laptop and 3×3 course grid; remove all words, numbers,
prices and badges, including book text; seamlessly extend the warm backgrounds.
No text, logos or currency symbols.” This avoids embedded Russian copy on the EN card.
