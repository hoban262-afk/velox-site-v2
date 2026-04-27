# Velox Peptides — Multipage SEO Restructure (Handoff to Claude Code)

## Role
You are a senior front-end engineer executing a pre-specified plan. You are NOT re-planning. The architecture, sitemap, URL structure, copy register, schema strategy, and generator approach have been fixed and agreed. Your job is to finish executing. Push back only if you find a technical blocker in the code — not if you disagree with the plan.

## Project context

**Site:** Velox Peptides (CRP Labs Ltd, Co. No. NI738125), UK research peptide supplier, Holywood, Northern Ireland.
**Domain:** veloxpeps.com, deployed via Vercel from GitHub.
**Current state:** Single HTML file (`veloxpeps_deploy_last_tonight.html`, ~4,200 lines, 449KB) doing everything via SPA `showPage()` routing. Needs restructuring into a multipage site for SEO.
**Catalogue:** 14 individual compounds + 11 stacks + 1 supply (bacteriostatic water) = 26 products across 5 research categories (cognitive, metabolic, healing-and-repair, growth, anti-ageing).

**Hard constraints (non-negotiable):**
1. **MHRA compliance.** No therapeutic, medical, or human-use claims anywhere. "For in vitro research use only. Not for human consumption." enforced sitewide.
2. **Scientific register.** No "Best seller," no "Sale" badges, no "Add to Cart." CTA is "Add to order." No lifestyle / wellness language.
3. **Brand system preserved pixel-for-pixel.** Background `#030407`, accent `#01D3A0`, existing typography and "Our Style" visual language (teal grid overlays, concentric ring SVGs, 800-weight headlines with outline-text key words, teal eyebrow labels, pill/badge tags).
4. **Plain multipage HTML, no build step.** No Astro, no Next.js, no npm. Static HTML files deployed straight from GitHub to Vercel. Claude IS the build tool — the `src/generate.py` script produces all files from `src/data/*.json`.
5. **Flow preservation.** Entry gate (cookie-based overlay), Royal Mail Tracked 48 UK-only delivery, Zempler Bank bank-transfer payment must all continue to work.
6. **Dashboards deferred.** Admin and affiliate dashboards are CUT from the new build. Do not carry them over.

## Decisions already made — do not revisit

- Foundation: plain multipage HTML, no build step, generator in Python produces all HTML from `src/data/*.json`
- URL structure: `/compounds/{slug}/`, `/compounds/{category}/`, `/stacks/{slug}/`, `/supplies/bacteriostatic-water/`, `/research/`, `/tools/reconstitution-calculator/`, `/about/`, `/contact/`, `/shipping/`, `/faq/`, `/legal/*/`, `/cart/`, `/checkout/{step}/`
- Retatrutide Pen is a SIZE VARIANT on the Retatrutide page, NOT a separate URL
- CJC-1295 (no DAC) uses slug `cjc-1295` (DAC status is a variant, not the URL)
- NAD+ slug is `nad-plus` (hyphenated)
- Anti-ageing slug uses UK spelling
- Stacks get their own URLs under `/stacks/`
- BPC-157 + TB-500 bundle (id=3 in source) moves from `healing` category to `/stacks/bpc157-tb500-bundle/`
- Payment is Zempler Bank bank transfer. NO Stripe, NO Wallid, NO high-risk card processor. Bank transfer only.
- Delivery: Royal Mail Tracked 48 ONLY, UK ONLY, £4.99 flat (free £80+)
- CTA is "Add to order" everywhere (NOT "Add to Cart", NOT "Request for Research")
- Entry gate is a cookie-gated overlay (`vp_entry`, 30-day expiry), NOT a URL redirect
- Admin + affiliate pages are CUT
- Research articles: template only for Phase 1, copy comes later
- Schema: generic `Product` + `Article` + `Organization` + `BreadcrumbList` + `FAQPage` + `CollectionPage`. **Absolutely NO `MedicalDrug`, `Drug`, `MedicalTherapy`, `MedicalScholarlyArticle`, `Review`, or `AggregateRating` schema anywhere.** These trigger Google's medical YMYL treatment and MHRA risk.

## What already exists in this repo

**`src/data/products_raw.json`** — extracted from source HTML, 27 raw product records

**`src/build_data.py`** — transforms raw products into:
- `src/data/compounds.json` (14 compounds, enriched with slug, categorySlug, molecular weight, sequence, FAQ, shortDesc)
- `src/data/stacks.json` (11 stacks including BPC+TB bundle, with components and categoryTags arrays for cross-linking)
- `src/data/supplies.json` (1 supply: bacteriostatic water)
- `src/data/categories.json` (5 categories with compoundCount)

**`src/assets/css/core.css`** — 84KB of CSS extracted from the source HTML. This is the brand system. Preserve it. Extend minimally for the new page types. Add extensions to the end of this file, do not modify the existing rules.

**`src/components.py`** — fully built shared components:
- `base_layout(title, description, path, body, extra_head, extra_schema_ld, page_class, extra_js)` — wraps body in HTML skeleton with `<head>`, header, footer, disclaimer bar, entry gate, JSON-LD
- `site_header(current_path)` — nav with compound/stack/research/about/contact links, active-state highlighting, mobile hamburger menu
- `site_footer()` — 4-column footer with compliance block above it
- `disclaimer_bar_top()` — scrolling marquee
- `disclaimer_inline(compound_name)` — inline below H1s
- `entry_gate()` — cookie-gated overlay
- `breadcrumb(trail)` — renders visual breadcrumb + BreadcrumbList JSON-LD simultaneously
- `trust_strip()` — 5 pillars
- `compound_card(c)` — the card used on category hubs and related strips
- `category_tile(cat)` — homepage/catalogue-root tiles
- `faq_block(faqs, heading)` + `faq_schema_ld(faqs)` — collapsible FAQ + schema

**`src/pages_products.py`** — product-family page generators already built:
- `gen_homepage(compounds, stacks, categories, featured_slugs)`
- `gen_catalogue_root(compounds, stacks, categories)` — `/compounds/`
- `gen_category_hub(category, compounds, stacks)` — `/compounds/{slug}/`
- `gen_compound_page(compound, all_compounds, all_stacks)` — `/compounds/{compound-slug}/`
- `gen_stacks_root(stacks)` — `/stacks/`
- `gen_stack_page(stack, all_compounds)` — `/stacks/{slug}/`
- `gen_supply_page(supply)` — `/supplies/{slug}/`
- Helper `_stack_card_mini(s)` for compact stack cards

**`src/pages_static.py`** — static-page generators already built:
- `gen_research_hub()` — `/research/` (placeholder hub; articles come later)
- `gen_reconstitution_calculator()` — `/tools/reconstitution-calculator/`
- `gen_about_index()` — `/about/`
- `gen_contact()` — `/contact/`
- `gen_shipping()` — `/shipping/`
- `gen_faq()` — `/faq/` with 10 FAQ entries + FAQPage schema
- `gen_legal_research_use()`, `gen_legal_mhra()`, `gen_legal_terms()`, `gen_legal_privacy()`, `gen_legal_cookies()`, `gen_legal_refunds()` — all 6 legal pages
- `gen_cart()` — `/cart/`
- `gen_checkout_shipping()` — `/checkout/shipping/`
- `gen_checkout_payment()` — `/checkout/payment/`
- `gen_checkout_confirmation()` — `/checkout/confirmation/`

## What's left to do (your job)

### 1. Main generator (`src/generate.py`)
Write this. It must:
- Load all JSON files from `src/data/`
- Import every `gen_*` function from `pages_products.py` and `pages_static.py`
- Call each generator with the right data
- Write each HTML string to the correct path under `output/` using the URL-to-path convention: `/compounds/bpc-157/` → `output/compounds/bpc-157/index.html`, `/` → `output/index.html`
- Copy `src/assets/` → `output/assets/` verbatim
- Pick a sensible `featured_slugs` list for the homepage (suggest: `['bpc-157', 'retatrutide', 'tb-500', 'semax', 'mots-c', 'nad-plus']`)
- Generate `output/sitemap.xml` listing all indexable URLs (skip `/cart/*`, `/checkout/*`)
- Generate `output/robots.txt` (blocks `/cart/`, `/checkout/`, `/coa/`, `/admin/`; references sitemap)
- Generate `output/vercel.json` with `trailingSlash: true`, `cleanUrls: true`, plus defensive 301 redirects (`/index.html` → `/`, `/anti-aging/*` → `/anti-ageing/*`, `/products/*` → `/compounds/*`, `/shop/` → `/compounds/`, `/peptides/*` → `/compounds/*`)
- Generate `output/site.webmanifest` (display: browser, theme_color #030407)
- Print a summary of what was generated

### 2. Client-side JS files (`src/assets/js/`)

These are referenced by generated pages but don't exist yet. Build them all:

**`core.js`** — loaded on every page. Must handle:
- Entry gate: check cookie `vp_entry`; if absent show `#entry-gate` overlay; on `#eg-accept` click, set cookie with `Path=/; Max-Age=2592000` and hide overlay
- Mobile nav: `#hamburger` click toggles `#mob-menu` visibility, also toggles `aria-expanded`
- Cart count update: read `localStorage.getItem('vp_cart')` (JSON array), sum item counts, update `#nav-cart-count`
- Toast helper: global `window.toast(msg)` function that shows `#toast` element for 3 seconds
- Re-render cart count on `storage` events (cart updated in another tab)

**`compound.js`** — loaded on compound, stack, supply pages. Must handle:
- Size selector: radio-button `input[name="size"]` changes update the displayed price
- Ack checkbox + "Add to order" button: on submit, require ack checked, read selected size, read the form `data-*` attributes (`data-compound`, `data-name`, `data-full`, `data-url`), push `{slug, name, url, size, price, qty: 1}` to `localStorage.vp_cart` array (merge with existing or increment qty), show toast "Added to order", update cart count
- Prevent default form submission

**`cart.js`** — loaded on `/cart/`. Must handle:
- Read `localStorage.vp_cart`
- If empty: hide `#cart-summary`, show `#cart-empty`
- If items: render each into `#cart-items` as a row with name link, size, £price, qty +/- buttons, remove button
- Recompute subtotal, shipping (£4.99, free if subtotal ≥ £80), total; update `#cart-subtotal`, `#cart-shipping`, `#cart-total`
- Wire up qty + remove buttons (write back to localStorage, re-render)
- Link `#cart-proceed` goes to `/checkout/shipping/`

**`checkout.js`** — loaded on all 3 `/checkout/*/` pages. Detect page by presence of `#shipping-form`, `#payment-form`, or `#confirm-summary`. Must handle:
- All pages: render cart summary into `#co-cart-items` (compact list)
- Shipping page: on submit, validate required fields + ack checkbox, save to `sessionStorage.vp_checkout` as JSON, redirect to `/checkout/payment/`
- Payment page: read `sessionStorage.vp_checkout` and display delivery address in `#co-deliver-to`; on submit, validate terms checkbox, generate order reference `VP-{YYYYMMDD}-{4 random chars}`, save ref + totals to sessionStorage, redirect to `/checkout/confirmation/`
- Confirmation page: display order ref in `#confirm-ref` and `#confirm-ref-2`, display total in `#confirm-amount`, populate `#bank-sort` and `#bank-acc` with placeholder values (`XX-XX-XX` and `XXXXXXXX` — these are deliberate placeholders to be replaced with real Zempler details post-deploy), render order summary into `#confirm-summary`, CLEAR `localStorage.vp_cart` on page load (order is placed, cart empties)
- "Billing same as delivery" checkbox on payment page toggles visibility of `#bill-fields`

**`calculator.js`** — loaded on `/tools/reconstitution-calculator/`. Must handle:
- Read `#calc-pep` (mg), `#calc-water` (ml), `#calc-dose` (mcg) on input
- Compute: concentration = `(pep * 1000) / water` mcg/ml; volume = `dose / concentration` ml; units = `volume * 100`; applications = `(pep * 1000) / dose`
- Display rounded values in `#calc-conc` (e.g. `5,000 mcg/ml`), `#calc-vol` (`0.05 ml`), `#calc-units` (`5 units`), `#calc-apps` (`40 applications`)
- Run once on load, then on every input event

### 3. CSS extensions (`src/assets/css/core.css`)

Append to end of existing file. Add styles for the new classes used by generated pages. Many of these already exist in `core.css` (extracted from the source). Check before re-declaring. Mobile breakpoints: 44–48px tap targets, 16px form inputs (prevents iOS zoom).

New classes likely needed:
- Compound page: `.cp-hero`, `.cp-hero-main`, `.cp-eyebrow`, `.cp-h1`, `.cp-lede`, `.cp-spec`, `.cp-order`, `.cp-size-opt`, `.cp-ack`, `.cp-order-btn`, `.cp-order-meta`, `.cp-section`, `.cp-spec-table`, `.cp-compliance`, `.cp-source-note`
- Category hub + catalogue: `.page-intro`, `.page-h1`, `.page-lede`, `.page-compliance`, `.page-eyebrow`, `.cat-grid`, `.cat-tile`, `.prod-grid`, `.cc` (compound card) and children, `.cat-group`
- Stack: `.stack-grid`, `.stack-card` and children, `.stack-comps`, `.stack-comp` and children
- Breadcrumb: `.breadcrumb`, `.bc-link`, `.bc-sep`, `.bc-current`
- Disclaimer: `.disc-inline`, `.compliance-block`, `.h-compliance`
- Checkout: `.co-steps`, `.co-step`, `.co-grid`, `.co-form-col`, `.co-form`, `.f-grid-2`, `.f-row`, `.f-full`, `.f-lbl`, `.f-inp`, `.ship-opts`, `.ship-opt`, `.co-ack`, `.co-err`, `.co-submit`, `.co-back`, `.co-summary` and children, `.pay-method`, `.confirm-card`, `.confirm-ref`, `.confirm-bank` and children
- Cart: `.cart-sec`, `.cart-grid`, `.cart-items-col`, `.cart-item`, `.cart-summary` and children, `.cart-empty`
- Calculator: `.calc-sec`, `.calc-grid`, `.calc-form`, `.calc-row`, `.calc-lbl`, `.calc-inp`, `.calc-hint`, `.calc-results`, `.calc-res`, `.calc-notes`
- Legal: `.legal-sec`, `.legal-i`, `.legal-effective`
- FAQ: `.faq-sec`, `.faq-list`, `.faq-item`, `.faq-q`, `.faq-a`
- Site header: `.site-header`, `.nav-logo`, `.nav-links`, `.nav-actions`, `.nav-cart`, `.nav-cart-count`, `.hamburger`, `.mob-menu`, `.mob-nl`, `.mob-nl-sub`
- Entry gate: `.entry-gate`, `.eg-i`, `.eg-top`, `.eg-eyebrow`, `.eg-title`, `.eg-body`, `.eg-actions`, `.eg-btn`, `.eg-foot`
- Footer: `.site-footer`, `.ft-i`, `.ft-top`, `.ft-brand`, `.ft-cols`, `.ft-col`, `.ft-bot`, `.compliance-block`
- Accessibility helper: `.visually-hidden`
- Toast: `.toast`, `.toast.show`

### 4. Favicon + manifest assets
Generate placeholder `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` using the VP teal-ring logo (simple: circle stroke #01D3A0, "VP" text centered, #030407 background). Put them in `src/assets/` and have the generator copy to `output/`. Placeholder `og-default.png` (1200×630) also.

### 5. Run the generator, verify, package

- Run `python3 src/generate.py`
- Verify every file in `output/` exists at the expected path
- Spot-check 3 files for correctness: `output/index.html`, `output/compounds/bpc-157/index.html`, `output/cart/index.html`
- Validate at least one JSON-LD block by running `python3 -c "import json; ..."` on its contents
- The `output/` directory is the deployable artifact — this is what gets pushed to GitHub and served by Vercel.

## Execution order

Do these in order. Finish each before starting the next:
1. Read all existing files in `src/` to understand what's already built (start with `components.py`, `pages_products.py`, `pages_static.py`, `build_data.py`)
2. Write `src/assets/js/core.js`, `compound.js`, `cart.js`, `checkout.js`, `calculator.js`
3. Append CSS extensions to `src/assets/css/core.css` for the new classes
4. Create favicon + manifest placeholder assets
5. Write `src/generate.py`
6. Run `python3 src/build_data.py` (regenerates JSON) then `python3 src/generate.py`
7. Debug any errors. Fix at the source, re-run.

## Verification checklist (run before declaring done)

- [ ] 50+ HTML files produced in `output/`
- [ ] Every compound page has `Product` JSON-LD with GBP offers and CAS identifier (where compound has a CAS)
- [ ] Every indexable page has a unique `<title>`, `<meta description>`, canonical link
- [ ] `/cart/` and all `/checkout/*/` pages have `<meta name="robots" content="noindex,nofollow">`
- [ ] NO page contains the strings "Best seller", "Add to Cart", "Shop Now", "Buy Now", "Discrete packaging", "MedicalDrug", "MedicalTherapy", "AggregateRating"
- [ ] Every page contains "For in vitro research use only"
- [ ] `sitemap.xml` lists only indexable URLs, no `/cart` or `/checkout`
- [ ] `robots.txt` present with sitemap reference
- [ ] `vercel.json` has `trailingSlash: true`
- [ ] Entry gate cookie sets with `Path=/` (check in `core.js`)
- [ ] Homepage has the hash-redirect script (legacy `#bpc-157` etc. → new URLs)

## Things to push back on if you encounter them

- If a generator function references a field that doesn't exist in the JSON — fix the JSON shape in `build_data.py`, regenerate, then re-run the generator. Don't silently default the field.
- If CSS collides between pages — namespace the class (prefix with `.cp-`, `.cat-`, `.co-` etc.), don't !important your way out.
- If you find a "Best seller" or other banned phrase surviving in the source data or a generator — grep the codebase and fix all instances, not just the one you noticed.
- If a compound is missing a `cas` or `formula` — render `—` in the display, not "undefined" or "null".

## Things you should NOT do

- Do not invent molecular weights, sequences, or CAS numbers. The manual lookups in `build_data.py` are the source of truth. If a value is missing, leave it missing.
- Do not restore any admin, affiliate, owner-dashboard, or login code. Those pages are cut.
- Do not add `MedicalDrug` or any `schema.org/Medical*` type. Ever.
- Do not add customer reviews, ratings, testimonials, or `AggregateRating` schema.
- Do not write human-use language in any copy. If a generator has copy that sounds like dosing advice, flag it and rewrite in preclinical-research register.
- Do not add a build step. No `package.json`, no `node_modules`, no webpack/vite/astro/next. Output is plain HTML + CSS + JS.
- Do not change URLs from the list already defined. `/compounds/cjc-1295/`, `/compounds/nad-plus/`, `/compounds/anti-ageing/` (UK spelling) — these are fixed.

Start now.
