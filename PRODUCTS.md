# AIforPsy products extension

Extends the existing production repository, static bilingual generator and Netlify deployment. Requires Python 3.12+ for local generation. No new framework or account required.

## Build

`python3 build.py` regenerates the homepage and all public product routes. Existing privacy pages and assets remain in dist. Netlify publishes committed dist; no build dependency was introduced.

`products.json` is the catalog and product data layer. `render_card` is the shared card renderer. Only `status: published` items appear. AI Secretary remains draft. Video URLs are null until supplied; only validated YouTube embed IDs are accepted. `testimonialMode` accepts link or embed.

## Routes (both /ru and /en)

- /save-time/: catalog
- /products/personal-ai-operations-director/: sales page
- /products/personal-ai-operations-director/hub/: access boundary in production
- /products/personal-ai-operations-director/hub/quick-start/: protected setup path
- /products/personal-ai-operations-director/hub/full-automation/: protected setup path
- /products/personal-ai-operations-director/success/ and /cancel/: status routes, never unlock access

## Paid materials and local review

No paid instructions, prompts or ZIP assets are included in the public dist or repository. The complete private preview lives in the owner's local product-work directory. To regenerate locally place private-content.json and personal_ai_operations_director_skill_v2.zip in the parent of this checkout and run `python3 build_products.py --preview`. Serve preview-dist on loopback only. Never publish preview-dist. No localStorage, URL query or client flag grants production access.

Current production access pages explain access requirements. The server function product-access returns 403 for access and 503 for checkout; no active checkout or verified-user path exists yet. These are explicit integration boundaries, not a completed payment/access system.

## Next integration phase

Set approved price and Stripe price ID. Implement checkout server-side. Verify webhook signatures and deduplicate events; grant per-product entitlement only after verified payment. Verify a signed customer session on every hub and download request, then serve content from private storage with non-cacheable responses. Never serve paid content from public dist. A success URL alone must not grant access. Keep Resend/domain secrets out of source.

Set explainerYouTubeUrl, quickStartYouTubeUrl, fullAutomationYouTubeUrl and testimonialYouTubeUrl when ready. UI layout remains the same.
