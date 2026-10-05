# AI for Psy

Responsive static homepage. Separate Russian `/ru/` and English `/en/` routes; root defaults to Russian. Approved copy is preserved in `copy-approved.json`, extracted from the referenced conversation.

## Develop

Run `python3 build.py` after updating the content or template. Serve `dist/` with any static web server. Styling and interaction files live in `dist/style.css` and `dist/app.js`; these are source files and should remain tracked.

Desktop displays all four cards. Below 761px cards become native keyboard-accessible accordions, initially collapsed, with one open at a time.

## Pending integration

The original approved mockup image was not available in the conversation export. The illustration is a provisional SVG composition with laptop, vase, and a text-free mug carrying a green globe. Replace with the approved asset when available. It is not the exact TA-Next Academy logo.

Contact destinations were not supplied. Service buttons open a localized selection dialog and permit copying the chosen service; connect the actual contact destination before a public launch.

Both approved language versions retain their exact paragraph copy; headings use sentence case visually. The Russian brand is localized to avoid mixing languages. No analytics, cookies, forms, or customer data storage are included.

## Revision to supplied mockup

Brand is now `AIforPsy` in both languages, without a symbol. Hero uses a generated photoreal workspace with globe-only mug; native UI text is overlaid separately. Four compact pastel cards show brief previews and equal-bottom Read More buttons. Full approved service copy lives in localized dialog templates. Mobile cards remain collapsed accordions.

Hero asset: `dist/hero-workspace.png`, generated with built-in image_gen. Prompt: premium photorealistic therapist workspace, 2:1; left ivory negative space; right pale oak desk, silver laptop, beige vase with olive branches, cream mug with small green globe only, notebook, upholstered chair, soft sunlight, ivory/sage/taupe palette; no people, typography, branding or watermark.

## Readability and hero revision

Removed the foreground vase and its branches with built-in image_gen, preserving background greenery and other objects. Current asset is `dist/hero-workspace-v3.png`. Edit prompt: remove only the foreground beige vase and all its olive branches; reconstruct the tabletop/window naturally; preserve background greenery, laptop, chair, globe mug, notebook, lighting and composition.

Removed the values strip. Russian service question now uses «может»; English is “How Can AI Help You?”. Supporting copy and controls increased at least 20% while all h1 sizes are unchanged. Service body and lead: 12px to 15px desktop; mobile 13px to 16px. Approved full service paragraphs remain intact in dialog templates.
