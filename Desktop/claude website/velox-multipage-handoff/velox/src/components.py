"""
Shared components for the Velox Peptides multipage site.
Each function returns an HTML string. The generator composes pages from these.
"""
import json
from html import escape


SITE_URL = 'https://veloxpeps.com'
SITE_NAME = 'Velox Peptides'
COMPANY = 'CRP Labs Ltd'
COMPANY_NUMBER = 'NI738125'
CONTACT_EMAIL = 'veloxpeps@gmail.com'
ADDRESS_LOCALITY = 'Holywood'
ADDRESS_REGION = 'Northern Ireland'
ADDRESS_COUNTRY = 'GB'


# ======================================================================== #
# BASE HTML LAYOUT
# ======================================================================== #
def base_layout(*, title, description, path, body, extra_head='', extra_schema_ld=None, page_class='', extra_js=''):
    """
    Wrap page body in the shared HTML skeleton.

    Args:
        title (str): <title> and og:title.
        description (str): meta description and og:description.
        path (str): absolute path from root, e.g. '/compounds/bpc-157/'
        body (str): main content HTML (everything inside <main> or the page body,
                    NOT including <header> or <footer>).
        extra_head (str): additional elements to append to <head>.
        extra_schema_ld (list|None): additional JSON-LD blocks to inject.
        page_class (str): class applied to <body> for page-type styling.
        extra_js (str): additional <script> tags to inject before </body>.
    """
    canonical = SITE_URL + path
    og_image = f'{SITE_URL}/assets/images/og-default.png'
    robots_meta = ''
    if path.startswith(('/cart/', '/checkout/')):
        robots_meta = '<meta name="robots" content="noindex,nofollow">\n  '

    # Sitewide JSON-LD: Organization
    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "legalName": COMPANY,
        "url": SITE_URL,
        "logo": f"{SITE_URL}/assets/images/logo.png",
        "email": CONTACT_EMAIL,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": ADDRESS_LOCALITY,
            "addressRegion": ADDRESS_REGION,
            "addressCountry": ADDRESS_COUNTRY,
        },
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "UK Company Number",
            "value": COMPANY_NUMBER,
        },
        "sameAs": [
            "https://www.instagram.com/veloxpeptides",
        ],
    }
    schema_blocks = [org_schema]
    if extra_schema_ld:
        schema_blocks.extend(extra_schema_ld)
    schema_html = '\n'.join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
        for s in schema_blocks
    )

    og_type = 'article' if path.startswith('/research/') and path != '/research/' else 'website'

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  {robots_meta}<link rel="canonical" href="{canonical}">

  <!-- Open Graph -->
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_GB">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{og_image}">

  <!-- Icons and manifest -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#030407">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;0,900;1,700;1,800;1,900&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/css/core.css">

  <!-- Homepage hash-redirect map (only on /) -->
  {homepage_hash_redirect_script() if path == '/' else ''}

  <!-- JSON-LD -->
  {schema_html}

  {extra_head}
</head>
<body class="{page_class}">

{disclaimer_bar_top()}

{site_header(path)}

<main class="site-main">
{body}
</main>

{site_footer()}

{entry_gate()}

<div class="toast" id="toast"></div>

<script src="/assets/js/core.js"></script>
{extra_js}
</body>
</html>
"""


# ======================================================================== #
# HOMEPAGE HASH REDIRECT — maps legacy #fragments to new URLs
# ======================================================================== #
def homepage_hash_redirect_script():
    mapping = {
        '#catalogue': '/compounds/',
        '#calc': '/tools/reconstitution-calculator/',
        '#peptide-reconstitution-calculator': '/tools/reconstitution-calculator/',
        '#footer': '/about/',
        '#cognitive': '/compounds/cognitive/',
        '#metabolic': '/compounds/metabolic/',
        '#healing': '/compounds/healing-and-repair/',
        '#growth': '/compounds/growth/',
        '#aging': '/compounds/anti-ageing/',
        '#ageing': '/compounds/anti-ageing/',
        '#stacks': '/stacks/',
        '#research': '/research/',
        '#about': '/about/',
        '#faq': '/faq/',
        '#contact': '/contact/',
        '#refund': '/legal/refunds/',
        '#privacy': '/legal/privacy/',
        '#terms': '/legal/terms/',
        '#shipping-policy': '/shipping/',
        '#cookie-policy': '/legal/cookies/',
        '#cart': '/cart/',
        # Individual compound anchors
        '#bpc-157': '/compounds/bpc-157/',
        '#tb-500': '/compounds/tb-500/',
        '#cjc-1295': '/compounds/cjc-1295/',
        '#tesamorelin': '/compounds/tesamorelin/',
        '#dsip': '/compounds/dsip/',
        '#selank': '/compounds/selank/',
        '#semax': '/compounds/semax/',
        '#dihexa': '/compounds/dihexa/',
        '#mots-c': '/compounds/mots-c/',
        '#nad': '/compounds/nad-plus/',
        '#nad-plus': '/compounds/nad-plus/',
        '#retatrutide': '/compounds/retatrutide/',
        '#ghk-cu': '/compounds/ghk-cu/',
        '#glutathione': '/compounds/glutathione/',
        '#melanotan-ii': '/compounds/melanotan-ii/',
    }
    return f"""<script>
(function(){{
  var r = {json.dumps(mapping)};
  var d = r[window.location.hash];
  if (d) {{ window.location.replace(d); }}
}})();
</script>"""


# ======================================================================== #
# SITE HEADER
# ======================================================================== #
def site_header(current_path: str):
    """Primary navigation. `current_path` determines which nav item is marked active."""
    def active(paths):
        return 'active' if any(current_path.startswith(p) for p in paths) else ''

    return f"""<header class="site-header">
  <nav class="nav" aria-label="Primary">

    <a class="nav-logo" href="/" aria-label="{SITE_NAME}">
      <img class="nav-logo-img" src="/assets/images/veloxpeps2.png" alt="Velox Peptides" width="150" height="auto">
    </a>

    <div class="nav-links">
      <a class="nl {active(['/compounds/'])}" href="/compounds/">Shop</a>
      <a class="nl {active(['/stacks/'])}" href="/stacks/">Stacks</a>
      <a class="nl {active(['/about/', '/about/lab-and-sourcing/', '/about/quality-and-testing/', '/about/coa-library/'])}" href="/about/">About</a>
      <a class="nl {active(['/faq/'])}" href="/faq/">FAQ</a>
      <a class="nl {active(['/contact/'])}" href="/contact/">Contact</a>
    </div>

    <div class="nav-actions">
      <a class="nav-ig" href="https://www.instagram.com/veloxpeps" target="_blank" rel="noopener noreferrer" aria-label="Velox Peptides on Instagram">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
          <circle cx="12" cy="12" r="4"/>
          <circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>
        </svg>
      </a>
      <a class="nav-cart" href="/cart/" aria-label="View cart">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <span class="nav-cart-label">Order</span>
        <span class="nav-cart-count" id="nav-cart-count">0</span>
      </a>
      <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>

  </nav>
  <div class="mob-menu" id="mob-menu" aria-hidden="true">
    <a href="/compounds/" class="mob-nl">Shop</a>
    <a href="/compounds/cognitive/" class="mob-nl mob-nl-sub">— Cognitive</a>
    <a href="/compounds/metabolic/" class="mob-nl mob-nl-sub">— Metabolic</a>
    <a href="/compounds/healing-and-repair/" class="mob-nl mob-nl-sub">— Healing &amp; Repair</a>
    <a href="/compounds/growth/" class="mob-nl mob-nl-sub">— Growth</a>
    <a href="/compounds/anti-ageing/" class="mob-nl mob-nl-sub">— Anti-Ageing</a>
    <a href="/stacks/" class="mob-nl mob-nl-sub">— Stacks</a>
    <a href="/tools/reconstitution-calculator/" class="mob-nl mob-nl-sub">— Reconstitution Calculator</a>
    <a href="/about/" class="mob-nl">About</a>
    <a href="/faq/" class="mob-nl">FAQ</a>
    <a href="/shipping/" class="mob-nl mob-nl-sub">— Shipping</a>
    <a href="/contact/" class="mob-nl">Contact</a>
    <a href="/cart/" class="mob-nl">Order</a>
  </div>
</header>
"""


# ======================================================================== #
# DISCLAIMER BARS
# ======================================================================== #
def disclaimer_bar_top():
    """Teal scrolling announcement banner — sits at the very top of every page."""
    items = [
        'FOR RESEARCH USE ONLY',
        'FREE UK SHIPPING ON ORDERS OVER &pound;100',
        'HPLC VERIFIED',
        'COA ON EVERY ORDER',
        'FOR RESEARCH USE ONLY',
        'FREE UK SHIPPING ON ORDERS OVER &pound;100',
        'HPLC VERIFIED',
        'COA ON EVERY ORDER',
    ]
    sep = '&nbsp;&nbsp;&nbsp;&middot;&nbsp;&nbsp;&nbsp;'
    # Duplicate the track so the seamless loop works
    track_content = sep.join(items) + sep
    return f"""<div class="ann-bar" role="note" aria-label="Site announcements">
  <div class="ann-track-wrap" aria-hidden="true">
    <span class="ann-track">{track_content}</span><span class="ann-track" aria-hidden="true">{track_content}</span>
  </div>
</div>"""


def disclaimer_inline(compound_name: str = 'This compound'):
    """Inline compliance block shown below compound H1s."""
    return f"""<div class="disc-inline">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F5C842" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
  <span>For <strong>in vitro research use only</strong>. {compound_name} is not for human or veterinary consumption, diagnosis, treatment, or prevention of any condition.</span>
</div>"""


# ======================================================================== #
# BREADCRUMB
# ======================================================================== #
def breadcrumb(trail: list):
    """
    trail = [{'href': '/', 'label': 'Home'}, {'label': 'Current page'}]
    The last item should NOT have an href (it's the current page).
    """
    items_html = []
    for i, item in enumerate(trail):
        is_last = (i == len(trail) - 1)
        sep = '' if i == 0 else '<span class="bc-sep" aria-hidden="true">›</span>'
        if is_last or 'href' not in item:
            items_html.append(f'{sep}<span class="bc-current" aria-current="page">{escape(item["label"])}</span>')
        else:
            items_html.append(f'{sep}<a class="bc-link" href="{item["href"]}">{escape(item["label"])}</a>')

    # BreadcrumbList JSON-LD
    ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item['label'],
                **({"item": SITE_URL + item['href']} if 'href' in item else {}),
            }
            for i, item in enumerate(trail)
        ],
    }
    return (f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(items_html)}</nav>\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')


# ======================================================================== #
# TRUST STRIP — 5 pillars
# ======================================================================== #
def trust_strip():
    return """<section class="trust" aria-label="Trust indicators">
  <div class="trust-i">
    <div class="ti"><div class="ti-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><div><div class="ti-ttl">HPLC Tested</div><div class="ti-sub">Every batch</div></div></div>
    <div class="ti"><div class="ti-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div><div><div class="ti-ttl">CoA Supplied</div><div class="ti-sub">Every order</div></div></div>
    <div class="ti"><div class="ti-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg></div><div><div class="ti-ttl">48h UK Dispatch</div><div class="ti-sub">Royal Mail Tracked 48</div></div></div>
    <div class="ti"><div class="ti-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div><div><div class="ti-ttl">Pay by Bank</div><div class="ti-sub">Zempler bank transfer</div></div></div>
    <div class="ti"><div class="ti-ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div><div><div class="ti-ttl">≥98% Purity</div><div class="ti-sub">Batch-released standard</div></div></div>
  </div>
</section>"""


# ======================================================================== #
# COMPOUND CARD (used on category hubs and elsewhere)
# ======================================================================== #
def compound_card(c):
    """Render a compound as a card — consistent across category hubs, homepage featured, related strips."""
    sizes = c['sizes']

    # Find the lead size (lowest price) and collect its discount metadata
    if len(sizes) == 1:
        lead = sizes[0]
        from_prefix = ''
    else:
        lead = min(sizes, key=lambda s: s['p'])
        from_prefix = 'From '

    badge     = lead.get('badge')       # 'save' | 'best_price' | None
    was_price = lead.get('wasPrice')    # own old price (Part 1)
    rrp       = lead.get('rrp')         # competitor RRP (Part 2)
    save_pct  = lead.get('savePct')     # integer % for SAVE badge

    # Build price footer HTML
    if badge == 'save' and was_price is not None:
        price_html = f"""<div class="cc-price-block">
      <span class="cc-was">&pound;{was_price:.2f}</span>
      <span class="cc-price">{from_prefix}&pound;{lead['p']:.2f}</span>
      <span class="cc-badge cc-badge-save">SAVE {save_pct}%</span>
    </div>"""
    elif badge == 'best_price' and rrp is not None:
        price_html = f"""<div class="cc-price-block">
      <span class="cc-was">&pound;{rrp:.2f}</span>
      <span class="cc-price">{from_prefix}&pound;{lead['p']:.2f}</span>
      <span class="cc-badge cc-badge-best">BEST PRICE</span>
    </div>"""
    else:
        price_html = f'<span class="cc-price">{from_prefix}&pound;{lead["p"]:.2f}</span>'

    purity_str = f"{c['purity']}% HPLC" if c.get('purity') else ''
    cas_str = f"CAS {c['cas']}" if c.get('cas') else ''
    meta_parts = [p for p in [purity_str, cas_str] if p]
    meta_line = ' · '.join(meta_parts)

    recently = '<span class="cc-tag cc-tag-new">NEW</span>' if c.get('isRecentlyAdded') else ''

    return f"""<article class="cc {c.get('cl', '')}">
  <a class="cc-img-link" href="{c['url']}" tabindex="-1" aria-hidden="true">
    <div class="cc-img-wrap">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#01D3A0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      <span class="cc-img-name">{escape(c['name'])}</span>
    </div>
  </a>
  <div class="cc-body">
    <div class="cc-hdr">
      <div class="cc-cat">{escape(c['categoryLabel'])}</div>
      {recently}
    </div>
    <a class="cc-name-link" href="{c['url']}">
      <h3 class="cc-name">{escape(c['name'])}</h3>
    </a>
    <div class="cc-full">{escape(c['fullName'])}</div>
    {f'<div class="cc-meta">{escape(meta_line)}</div>' if meta_line else ''}
    <p class="cc-desc">{escape(c['shortDesc'])}</p>
    <div class="cc-ft">
      {price_html}
    </div>
  </div>
</article>"""


# ======================================================================== #
# CATEGORY TILE (homepage + /compounds/ root)
# ======================================================================== #
def category_tile(cat):
    return f"""<a class="cat-tile" href="/compounds/{cat['slug']}/">
  <div class="cat-tile-hdr">
    <span class="cat-tile-eyebrow">— CATEGORY</span>
    <span class="cat-tile-count">{cat['compoundCount']} compounds</span>
  </div>
  <h3 class="cat-tile-name">{escape(cat['label'])}</h3>
  <p class="cat-tile-desc">{escape(cat['shortDesc'])}</p>
  <span class="cat-tile-action">Browse {escape(cat['label'].lower())} →</span>
</a>"""


# ======================================================================== #
# SITE FOOTER
# ======================================================================== #
def site_footer():
    return f"""<div class="compliance-block" role="note" aria-label="Compliance notice">
  <div class="cb-i">
    <strong>Compliance statement.</strong>
    Velox Peptides supplies research reagents for <em>in vitro</em> use by qualified researchers. Every compound is sold strictly as a research reagent. No product is a medicinal product within the meaning of the Human Medicines Regulations 2012. No product has been evaluated by the MHRA or FDA. No product is intended for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition. Any use outside lawful scientific research is outside the scope of sale. See our <a href="/legal/research-use-policy/">Research Use Policy</a> and <a href="/legal/mhra-statement/">MHRA Statement</a>.
  </div>
</div>

<footer class="site-footer" id="footer">
  <div class="ft-i">
    <div class="ft-top">
      <div class="ft-brand">
        <div class="ft-logo-wordmark">Velox Peptides</div>
        <p class="ft-tag">UK research peptide supplier. HPLC-verified, CoA on every order, dispatched from Northern Ireland via Royal Mail Tracked 48.</p>
        <address class="ft-address">
          {COMPANY}<br>
          Company no. {COMPANY_NUMBER}<br>
          {ADDRESS_LOCALITY}, {ADDRESS_REGION}, United Kingdom<br>
          <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
        </address>
      </div>
      <div class="ft-cols">
        <div class="ft-col">
          <div class="ft-col-h">Compounds</div>
          <a href="/compounds/">All compounds</a>
          <a href="/compounds/cognitive/">Cognitive</a>
          <a href="/compounds/metabolic/">Metabolic</a>
          <a href="/compounds/healing-and-repair/">Healing &amp; Repair</a>
          <a href="/compounds/growth/">Growth</a>
          <a href="/compounds/anti-ageing/">Anti-Ageing</a>
          <a href="/stacks/">Stacks</a>
          <a href="/supplies/bacteriostatic-water/">Bacteriostatic Water</a>
        </div>
        <div class="ft-col">
          <div class="ft-col-h">Resources</div>
          <a href="/research/">Research Library</a>
          <a href="/tools/reconstitution-calculator/">Reconstitution Calculator</a>
          <a href="/about/">About Velox</a>
          <a href="/about/quality-and-testing/">Quality &amp; Testing</a>
          <a href="/about/coa-library/">CoA Library</a>
          <a href="/faq/">FAQ</a>
        </div>
        <div class="ft-col">
          <div class="ft-col-h">Order &amp; Delivery</div>
          <a href="/cart/">Current order</a>
          <a href="/shipping/">Shipping &amp; Delivery</a>
          <a href="/legal/refunds/">Refunds &amp; Returns</a>
          <a href="/contact/">Contact</a>
        </div>
        <div class="ft-col">
          <div class="ft-col-h">Legal</div>
          <a href="/legal/research-use-policy/">Research Use Policy</a>
          <a href="/legal/mhra-statement/">MHRA Statement</a>
          <a href="/legal/terms/">Terms &amp; Conditions</a>
          <a href="/legal/privacy/">Privacy Policy</a>
          <a href="/legal/cookies/">Cookie Policy</a>
        </div>
      </div>
    </div>
    <div class="ft-bot">
      <div class="ft-cr">&copy; 2026 {COMPANY}. All rights reserved.</div>
      <div class="ft-disc">For in vitro research use only. Not for human or veterinary consumption.</div>
    </div>
  </div>
</footer>"""


# ======================================================================== #
# ENTRY GATE — cookie-gated overlay, first visit only
# ======================================================================== #
def entry_gate():
    return """<div class="entry-gate" id="entry-gate" role="dialog" aria-modal="true" aria-labelledby="eg-av-title">
  <div class="eg-i">

    <div class="eg-logo-wrap">
      <img class="eg-logo-img" src="/assets/images/veloxpeps2.png" alt="Velox Peptides" width="190">
    </div>

    <div class="eg-eyebrow">AGE VERIFICATION</div>
    <h2 id="eg-av-title" class="eg-av-title">Confirm your eligibility</h2>
    <p class="eg-sub">This website is restricted to qualified researchers aged 21 or over. All products are for in vitro research use only.</p>

    <div class="eg-checks">
      <label class="eg-check-row">
        <input type="checkbox" class="eg-cb" checked>
        <span class="eg-check-box" aria-hidden="true"></span>
        <span class="eg-check-label">I am 21 years of age or older</span>
      </label>
      <label class="eg-check-row">
        <input type="checkbox" class="eg-cb" checked>
        <span class="eg-check-box" aria-hidden="true"></span>
        <span class="eg-check-label">I am a qualified researcher, scientist, or laboratory professional</span>
      </label>
      <label class="eg-check-row">
        <input type="checkbox" class="eg-cb" checked>
        <span class="eg-check-box" aria-hidden="true"></span>
        <span class="eg-check-label">All products will be used for lawful in vitro research only &mdash; not for human consumption</span>
      </label>
      <label class="eg-check-row">
        <input type="checkbox" class="eg-cb" checked>
        <span class="eg-check-box" aria-hidden="true"></span>
        <span class="eg-check-label">I accept the <a href="/legal/terms/" target="_blank" rel="noopener">Terms &amp; Conditions</a> and <a href="/legal/research-use-policy/" target="_blank" rel="noopener">Research Use Disclaimer</a></span>
      </label>
    </div>

    <div class="eg-disclaimer">
      All products sold for research use only. Not for human consumption. Not evaluated by the MHRA or FDA.
    </div>

    <div class="eg-actions">
      <button class="eg-btn eg-btn-p" id="eg-accept">I CONFIRM &mdash; ENTER SITE</button>
      <a class="eg-exit-link" href="https://www.gov.uk" rel="noopener">Exit</a>
    </div>

  </div>
</div>"""


# ======================================================================== #
# FAQ BLOCK (compound pages, category hubs, /faq/)
# ======================================================================== #
def faq_block(faqs: list, heading: str = 'Frequently Asked Research-Use Questions'):
    if not faqs:
        return ''
    items_html = []
    for faq in faqs:
        # Note: faq['a'] is raw HTML (may contain <a> tags). Do not escape.
        q = escape(faq['q'])
        a = faq['a']
        items_html.append(f"""
<details class="faq-item">
  <summary class="faq-q">{q}</summary>
  <div class="faq-a">{a}</div>
</details>""")
    return f"""<section class="faq-sec" aria-labelledby="faq-heading">
  <h2 id="faq-heading" class="sec-t">{escape(heading)}</h2>
  <div class="faq-list">
    {''.join(items_html)}
  </div>
</section>"""


def faq_schema_ld(faqs: list):
    """Generate FAQPage JSON-LD. Strip HTML from answers for the schema text."""
    import re as _re
    def strip_html(s):
        return _re.sub(r'<[^>]+>', '', s)
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f['q'],
                "acceptedAnswer": {"@type": "Answer", "text": strip_html(f['a'])},
            }
            for f in faqs
        ],
    }
