"""
Page generators for the Velox Peptides multipage site.

Each generator takes data and returns an HTML string. The caller writes it to disk.
"""
import json
from html import escape
from components import (
    base_layout,
    breadcrumb,
    compound_card,
    category_tile,
    disclaimer_inline,
    trust_strip,
    faq_block,
    faq_schema_ld,
    SITE_URL,
    SITE_NAME,
    CONTACT_EMAIL,
    COMPANY,
    COMPANY_NUMBER,
)


def _price_display(sizes):
    """Return a price string for compound card / meta description."""
    if len(sizes) == 1:
        return f"£{sizes[0]['p']:.2f}"
    prices = [s['p'] for s in sizes]
    return f"from £{min(prices):.2f}"


# ======================================================================== #
# HOMEPAGE
# ======================================================================== #
def gen_homepage(compounds, stacks, categories, featured_slugs):
    title = f"{SITE_NAME} — UK Research Peptides · HPLC-Tested · CoA-Verified"
    description = ("Research-grade peptides for UK laboratories and qualified researchers. "
                   "Every batch third-party HPLC-tested with certificate of analysis. "
                   "48-hour UK dispatch from Northern Ireland via Royal Mail Tracked 48. "
                   "For in vitro research use only.")

    # Build featured list from compounds AND stacks, preserving slug order
    _all_products = {p['slug']: p for p in compounds + stacks}
    featured = [_all_products[slug] for slug in featured_slugs if slug in _all_products]
    total_compound_count = len(compounds) + len(stacks)

    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "url": SITE_URL,
        "name": SITE_NAME,
        "description": "UK research peptide supplier. HPLC-verified, CoA-supplied, Royal Mail Tracked 48 UK dispatch.",
    }

    # ── 1. HERO ───────────────────────────────────────────────────────────────
    hero = f"""<section class="hero">
  <div class="hero-i">
    <div class="hero-content">
      <div class="h-ey">HPLC-Verified &middot; CoA-Supplied &middot; UK Dispatch</div>
      <h1 class="h-h1">HPLC-Verified<br>Research<br><em>Peptides.</em></h1>
      <div class="h-stats-row">
        <div class="h-stat-item">
          <span class="hsi-v">&ge;98%</span>
          <span class="hsi-l">HPLC Purity</span>
        </div>
        <span class="hsi-div" aria-hidden="true"></span>
        <div class="h-stat-item">
          <span class="hsi-v">48h</span>
          <span class="hsi-l">UK Dispatch</span>
        </div>
        <span class="hsi-div" aria-hidden="true"></span>
        <div class="h-stat-item">
          <span class="hsi-v">{total_compound_count}</span>
          <span class="hsi-l">Products</span>
        </div>
      </div>
      <p class="h-sub">
        {len(compounds)} research compounds and {len(stacks)} stacks across cognitive, metabolic,
        healing, growth, and anti-ageing pathways. Every batch third-party HPLC-tested,
        certificate of analysis supplied with every order.
      </p>
      <div class="h-btns">
        <a class="btn-p" href="/compounds/">Browse Compounds</a>
        <a class="btn-o" href="/tools/reconstitution-calculator/">Reconstitution Calculator</a>
      </div>
      <p class="h-compliance"><strong>For in vitro research use only.</strong> Not for human or veterinary consumption.</p>
    </div>
    <div class="hero-panel hp-block">
      <div class="hp-lbl">LATEST BATCH REPORT &mdash; 2026</div>
      <div class="hp-rows">
        <div class="hp-r"><span class="hp-k">Compound</span><span class="hp-v">BPC-157 &middot; Lot 2026-04A</span></div>
        <div class="hp-r"><span class="hp-k">CAS Number</span><span class="hp-v">137525-51-0</span></div>
        <div class="hp-r"><span class="hp-k">HPLC Purity</span><span class="hp-v ok">99.4% &mdash; PASS &#x2713;</span></div>
        <div class="hp-r"><span class="hp-k">Mass Spec</span><span class="hp-v ok">1419.5 g/mol &mdash; CONFIRMED</span></div>
        <div class="hp-r"><span class="hp-k">Appearance</span><span class="hp-v ok">White lyophilised powder &mdash; PASS</span></div>
        <div class="hp-r"><span class="hp-k">Testing Lab</span><span class="hp-v">Eurofins Scientific Ltd</span></div>
      </div>
      <div class="hp-tags">
        <span class="hp-tag">HPLC</span>
        <span class="hp-tag">MASS SPEC</span>
        <span class="hp-tag">LYOPHILISED</span>
        <span class="hp-tag">ISO ACCREDITED</span>
      </div>
    </div>
  </div>
</section>"""

    # ── 3. CATEGORY GRID ──────────────────────────────────────────────────────
    category_grid = f"""<section class="hp-sec hp-sec-cats">
  <div class="sec-i">
    <div class="hp-block">
      <div class="hp-block-hdr">
        <h2 class="sec-t">Browse by research category</h2>
        <p class="sec-sub">Five categories covering the primary pathway clusters studied in preclinical peptide research.</p>
      </div>
      <div class="cat-grid">
        {''.join(category_tile(c) for c in categories)}
      </div>
    </div>
  </div>
</section>"""

    # ── 4. FEATURED COMPOUNDS ─────────────────────────────────────────────────
    featured_section = f"""<section class="hp-sec hp-sec-featured">
  <div class="sec-i">
    <div class="hp-block hp-feat-block">
      <div class="hp-feat-hdr">
        <div class="hp-feat-accent-bar"></div>
        <div class="hp-feat-titles">
          <div class="hp-block-eyebrow">RESEARCH CATALOGUE</div>
          <h2 class="hp-feat-title">FEATURED RESEARCH COMPOUNDS</h2>
          <p class="hp-feat-sub">Popular compounds trusted by researchers worldwide &mdash; every batch HPLC-verified</p>
        </div>
      </div>
      <div class="prod-grid prod-grid-4">
        {''.join(compound_card(c) for c in featured)}
      </div>
      <div class="hp-block-ft">
        <a class="btn-o" href="/compounds/">View all {len(compounds)} compounds &rarr;</a>
      </div>
    </div>
  </div>
</section>"""

    # ── 5. WHY RESEARCHERS TRUST US ───────────────────────────────────────────
    standards_section = """<section class="hp-sec hp-sec-stds">
  <div class="sec-i">
    <div class="hp-block">
      <div class="hp-block-hdr">
        <h2 class="sec-t">Why researchers trust us</h2>
        <p class="sec-sub">Every compound we supply meets the same uncompromising quality standard before it leaves our facility.</p>
      </div>
      <div class="stds-grid">
        <div class="std-card hp-block">
          <div class="std-ic">&#x1F52C;</div>
          <div class="std-t">Independent HPLC Testing</div>
          <p class="std-p">Every batch is tested by an ISO-accredited third-party laboratory. Results are non-negotiable — sub-standard batches are never dispatched.</p>
        </div>
        <div class="std-card hp-block">
          <div class="std-ic">&#x2705;</div>
          <div class="std-t">&ge;98% Purity Standard</div>
          <p class="std-p">We only ship compounds that meet our minimum 98% HPLC purity threshold. Sub-standard batches are rejected and destroyed, no exceptions.</p>
        </div>
        <div class="std-card hp-block">
          <div class="std-ic">&#x1F4C4;</div>
          <div class="std-t">CoA With Every Order</div>
          <p class="std-p">Your certificate of analysis ships with every order. HPLC chromatogram, mass spec confirmation, and full batch data included as standard.</p>
        </div>
        <div class="std-card hp-block">
          <div class="std-ic">&#x1F4E6;</div>
          <div class="std-t">48h UK Dispatch</div>
          <p class="std-p">Orders placed before 2pm are dispatched the same working day via Royal Mail Tracked 48. Discreet, temperature-appropriate packaging throughout.</p>
        </div>
        <div class="std-card hp-block">
          <div class="std-ic">&#x1F3E6;</div>
          <div class="std-t">Secure Bank Transfer</div>
          <p class="std-p">Payments processed via Zempler Bank transfer — no third-party processors, no chargebacks, no card data shared with any external network.</p>
        </div>
      </div>
    </div>
  </div>
</section>"""

    # ── 6. RECONSTITUTION CALCULATOR ─────────────────────────────────────────
    calculator_section = """<section class="hp-sec hp-sec-calc">
  <div class="sec-i">
    <div class="hp-block hp-calc-block">
      <div class="hp-calc-content">
        <div class="hp-calc-text">
          <div class="hp-block-eyebrow">FREE RESEARCH TOOL</div>
          <h2 class="sec-t">Reconstitution Calculator</h2>
          <p class="hp-calc-desc">Calculate the exact volume of bacteriostatic water needed to achieve your target peptide concentration. Supports any vial size, any target concentration — results in seconds.</p>
          <ul class="hp-calc-features">
            <li>&#x2713; Any vial size (2mg, 5mg, 10mg)</li>
            <li>&#x2713; Any target concentration</li>
            <li>&#x2713; Displays per-unit dose volume</li>
            <li>&#x2713; No account or sign-up required</li>
          </ul>
          <a class="btn-p" href="/tools/reconstitution-calculator/">Open Calculator</a>
        </div>
        <div class="hp-calc-preview">
          <div class="hp-calc-demo">
            <div class="hcd-label">EXAMPLE CALCULATION</div>
            <div class="hcd-row"><span class="hcd-k">Vial size</span><span class="hcd-v">5mg BPC-157</span></div>
            <div class="hcd-row"><span class="hcd-k">Target conc.</span><span class="hcd-v">500 mcg/mL</span></div>
            <div class="hcd-row"><span class="hcd-k">BAC water needed</span><span class="hcd-v hcd-result">10.0 mL</span></div>
            <div class="hcd-row"><span class="hcd-k">Doses per vial</span><span class="hcd-v hcd-result">50 doses</span></div>
            <div class="hcd-row"><span class="hcd-k">Volume per dose</span><span class="hcd-v hcd-result">0.20 mL (200 &micro;L)</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    # ── 7. NEWSLETTER ─────────────────────────────────────────────────────────
    newsletter_section = """<section class="hp-sec hp-sec-nl">
  <div class="sec-i">
    <div class="hp-block hp-nl-block">
      <div class="nl-inner">
        <div class="hp-block-eyebrow">RESEARCH BULLETIN</div>
        <h2 class="nl-t">Stay ahead of the research</h2>
        <p class="nl-sub">New compound arrivals, batch release notices, and plain-language research summaries delivered to your inbox. No marketing, no spam.</p>
        <div class="nl-row">
          <input class="nl-inp" type="email" placeholder="your@institution.ac.uk" aria-label="Email address">
          <button class="nl-btn btn-p" type="button">Subscribe</button>
        </div>
        <p class="nl-disc">For researchers only. Unsubscribe at any time. We never share your address.</p>
      </div>
    </div>
  </div>
</section>"""

    # ── 8. COMMUNITY ──────────────────────────────────────────────────────────
    community_section = """<section class="hp-sec hp-sec-comm">
  <div class="sec-i">
    <div class="hp-block hp-comm-block">

      <div class="hp-comm-hdr">
        <h2 class="hp-comm-title">JOIN THE COMMUNITY</h2>
        <p class="hp-comm-sub">Connect with researchers &mdash; get protocol guidance and be first to hear about new releases</p>
      </div>

      <div class="hp-soc-row">

        <a class="hp-soc-card" href="https://discord.gg/veloxpeps" target="_blank" rel="noopener noreferrer">
          <div class="hp-soc-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.004.037.023.073.05.095a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/></svg>
          </div>
          <div class="hp-soc-name">Discord</div>
          <div class="hp-soc-handle">Join the server</div>
        </a>

        <a class="hp-soc-card" href="https://www.instagram.com/veloxpeps" target="_blank" rel="noopener noreferrer">
          <div class="hp-soc-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none"/></svg>
          </div>
          <div class="hp-soc-name">Instagram</div>
          <div class="hp-soc-handle">@biohack.exe</div>
        </a>

        <a class="hp-soc-card" href="https://t.me/veloxpeptides" target="_blank" rel="noopener noreferrer">
          <div class="hp-soc-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.941z"/></svg>
          </div>
          <div class="hp-soc-name">Telegram</div>
          <div class="hp-soc-handle">@veloxpeptides</div>
        </a>

      </div>
    </div>
  </div>
</section>"""

    body = '\n'.join([
        hero,
        featured_section,
        category_grid,
        newsletter_section,
        standards_section,
        community_section,
    ])

    return base_layout(
        title=title,
        description=description,
        path='/',
        body=body,
        extra_schema_ld=[website_schema],
        page_class='page-home',
    )


# ======================================================================== #
# CATALOGUE ROOT — /compounds/
# ======================================================================== #
def gen_catalogue_root(compounds, stacks, categories):
    title = f"Research Compound Catalogue — {SITE_NAME}"
    description = (f"{len(compounds)} research peptide compounds across cognitive, metabolic, "
                   "healing, growth, and anti-ageing categories. HPLC-verified, CoA-supplied, "
                   "UK dispatch. For in vitro research use only.")

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'label': 'Compounds'},
    ])

    intro = f"""<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Research compound catalogue</h1>
    <p class="page-lede">
      The complete Velox Peptides research compound catalogue. {len(compounds)} individual compounds plus {len(stacks)} multi-compound research stacks, every one supplied with a batch certificate of analysis, every one HPLC-tested prior to dispatch.
    </p>
    <p class="page-compliance"><strong>For in vitro research use only.</strong> Not for human or veterinary consumption.</p>
  </div>
</section>"""

    category_section = f"""<section class="cat-grid-sec">
  <div class="sec-i">
    <div class="sec-hdr"><h2 class="sec-t">Browse by research category</h2></div>
    <div class="cat-grid">
      {''.join(category_tile(c) for c in categories)}
    </div>
  </div>
</section>"""

    # All compounds grouped by category
    compound_groups = []
    for cat in categories:
        cat_compounds = [c for c in compounds if c['category'] == cat['key']]
        if not cat_compounds:
            continue
        compound_groups.append(f"""<section class="cat-group" id="{cat['slug']}">
  <div class="sec-i">
    <div class="sec-hdr">
      <h2 class="sec-t">{escape(cat['label'])} research peptides</h2>
      <a class="sec-link" href="/compounds/{cat['slug']}/">View {escape(cat['label'].lower())} hub →</a>
    </div>
    <div class="prod-grid">
      {''.join(compound_card(c) for c in cat_compounds)}
    </div>
  </div>
</section>""")

    stacks_link = f"""<section class="cta-sec">
  <div class="sec-i">
    <div class="cta-card">
      <div>
        <div class="cta-eyebrow">— MULTI-COMPOUND BUNDLES</div>
        <h2 class="cta-t">Research stacks</h2>
        <p>{len(stacks)} curated multi-compound bundles grouping compounds commonly studied together in preclinical research.</p>
      </div>
      <a class="btn-p" href="/stacks/">View research stacks →</a>
    </div>
  </div>
</section>"""

    # CollectionPage schema
    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Research Compound Catalogue",
        "url": f"{SITE_URL}/compounds/",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "url": SITE_URL + c['url'],
                    "name": c['fullName'],
                }
                for i, c in enumerate(compounds)
            ],
        },
    }

    body = '\n'.join([bc, intro, category_section, *compound_groups, stacks_link])
    return base_layout(
        title=title,
        description=description,
        path='/compounds/',
        body=body,
        extra_schema_ld=[collection_schema],
        page_class='page-catalogue',
    )


# ======================================================================== #
# CATEGORY HUB — /compounds/{category_slug}/
# ======================================================================== #
def gen_category_hub(category, compounds, stacks):
    cat_compounds = [c for c in compounds if c['category'] == category['key']]
    cat_stacks = [s for s in stacks if category['key'] in s.get('categoryTags', [])]

    label = category['label']
    title = f"{label} Research Peptides — {', '.join(c['name'] for c in cat_compounds[:4])}"
    if len(title) > 70:
        title = f"{label} Research Peptides — {SITE_NAME}"
    description = (f"{label.lower().capitalize()}-focused research peptides studied for the pathway "
                   f"activity described in the peer-reviewed preclinical literature. "
                   f"HPLC-verified, CoA-supplied, UK dispatch. For in vitro research use only.")

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/compounds/', 'label': 'Compounds'},
        {'label': label},
    ])

    # Category-specific intro copy
    intro_copy = _category_intro_copy(category['key'])

    intro = f"""<section class="page-intro">
  <div class="sec-i">
    <div class="page-eyebrow">— CATEGORY · {len(cat_compounds)} COMPOUNDS</div>
    <h1 class="page-h1">{escape(label)} research peptides</h1>
    {intro_copy}
    <p class="page-compliance"><strong>For in vitro research use only.</strong> Compounds in this category are not for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition.</p>
  </div>
</section>"""

    compounds_section = f"""<section class="cat-compounds">
  <div class="sec-i">
    <h2 class="sec-t">Compounds in {escape(label.lower())} research</h2>
    <div class="prod-grid">
      {''.join(compound_card(c) for c in cat_compounds)}
    </div>
  </div>
</section>"""

    stacks_section = ''
    if cat_stacks:
        stacks_section = f"""<section class="cat-stacks">
  <div class="sec-i">
    <h2 class="sec-t">Stacks containing {escape(label.lower())} compounds</h2>
    <div class="stack-grid">
      {''.join(_stack_card_mini(s) for s in cat_stacks)}
    </div>
  </div>
</section>"""

    # Category-level FAQ
    cat_faqs = _category_faqs(category['key'], cat_compounds)
    faq_section = faq_block(cat_faqs, heading=f"Frequently asked — {label.lower()} research")

    # Collection + FAQ schema
    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{label} Research Peptides",
        "url": f"{SITE_URL}/compounds/{category['slug']}/",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": SITE_URL + c['url'], "name": c['fullName']}
                for i, c in enumerate(cat_compounds)
            ],
        },
    }
    schemas = [collection_schema]
    if cat_faqs:
        schemas.append(faq_schema_ld(cat_faqs))

    body = '\n'.join([bc, intro, compounds_section, stacks_section, faq_section])
    return base_layout(
        title=title,
        description=description,
        path=f"/compounds/{category['slug']}/",
        body=body,
        extra_schema_ld=schemas,
        page_class='page-category',
    )


def _category_intro_copy(cat_key: str) -> str:
    copy = {
        'cognitive': """<p class="page-lede">Cognitive research peptides are studied in the preclinical literature for their effects on neuroplasticity, neurotransmitter signalling, and the structural proteins that govern how brain cells form and maintain connections.</p>
<p>The compounds in this category include <strong>Semax</strong> and <strong>Selank</strong>, both extensively researched in Eastern European neuroscience institutions; <strong>DSIP</strong>, a neuropeptide isolated from deep-sleep states; and <strong>Dihexa</strong>, an angiotensin IV-derived oligopeptide investigated for its interaction with the HGF/c-Met synaptic signalling axis. Research models across this category typically examine BDNF expression, GABAergic and serotonergic modulation, dendritic spine density, and task-based cognitive performance in rodents.</p>""",
        'metabolic': """<p class="page-lede">Metabolic research peptides are studied for their roles in regulating energy balance, insulin response, glucose metabolism, and mitochondrial signalling across preclinical and in vitro models.</p>
<p>This category includes <strong>Retatrutide</strong>, a next-generation triple-receptor agonist simultaneously engaging GLP-1, GIP, and glucagon pathways; <strong>Mots-C</strong>, a mitochondrially-encoded peptide investigated for AMPK activation; and <strong>NAD+</strong>, the foundational coenzyme at the centre of sirtuin enzyme activity and cellular energy metabolism. Research across this category examines receptor-mediated signalling, metabolic gene expression, and the interactions between nutrient-sensing pathways.</p>""",
        'healing': """<p class="page-lede">Healing and repair research peptides are studied in preclinical tissue-response models for their roles in angiogenesis, cellular migration, wound tissue closure, and structural protein regulation.</p>
<p>This category contains <strong>BPC-157</strong>, among the most extensively studied repair-focused compounds in rodent research, and <strong>TB-500</strong>, a synthetic analogue of thymosin beta-4 studied for its actin-regulating effects in cellular migration. Both are also investigated alongside each other in tissue-repair research protocols.</p>""",
        'growth': """<p class="page-lede">Growth hormone-releasing hormone (GHRH) analogues studied in preclinical and clinical research for their effects on GH secretion, IGF-1 pathway activity, and downstream metabolic signalling.</p>
<p>This category includes <strong>CJC-1295 (no DAC)</strong>, a GRF(1-29) analogue that produces a shorter, more physiologically pulsatile GH-release pattern, and <strong>Tesamorelin</strong>, one of the most clinically researched GHRH analogues, studied for both GH/IGF-1 pathway effects and visceral fat distribution in specific patient populations.</p>""",
        'aging': """<p class="page-lede">Anti-ageing research peptides and reagents studied in preclinical models for their roles in cellular antioxidant defence, collagen and elastin synthesis, and the sirtuin enzyme pathway.</p>
<p>This category includes <strong>GHK-Cu</strong>, a naturally occurring copper tripeptide extensively researched in dermatological cellular models; <strong>L-Glutathione (Reduced)</strong>, the foundational intracellular antioxidant involved in mitochondrial redox balance; and <strong>Melanotan II</strong>, a synthetic alpha-MSH analogue binding across multiple melanocortin receptor subtypes.</p>""",
    }
    return copy.get(cat_key, '<p class="page-lede">Research compounds in this category.</p>')


def _category_faqs(cat_key: str, compounds: list) -> list:
    compound_names = ', '.join(c['name'] for c in compounds)
    common = [
        {
            'q': f'What compounds does Velox Peptides supply for {cat_key} research?',
            'a': f'Velox Peptides supplies {len(compounds)} research compounds in this category: {compound_names}. All are HPLC-verified and supplied with a batch certificate of analysis.',
        },
        {
            'q': 'Are these peptides for human use?',
            'a': 'No. All compounds supplied by Velox Peptides are strictly for in vitro research use by qualified researchers. They are not medicinal products and are not for human or veterinary consumption.',
        },
        {
            'q': 'How are research peptides supplied?',
            'a': 'Research compounds are supplied as lyophilised (freeze-dried) powders in sterile vials for reconstitution with bacteriostatic water prior to research use. See our <a href="/tools/reconstitution-calculator/">reconstitution calculator</a> for concentration and volume calculations.',
        },
        {
            'q': 'Is a certificate of analysis supplied?',
            'a': 'Yes. A batch-specific certificate of analysis documenting HPLC purity, mass spectrometry confirmation, and appearance is supplied with every order. Previous batch CoAs are available in our <a href="/about/coa-library/">CoA library</a>.',
        },
    ]
    return common


def _stack_card_mini(s):
    """Compact stack card used on category hubs and /stacks/."""
    size      = s['sizes'][0]
    price     = size['p']
    orig      = size.get('origPrice')
    save_pct  = size.get('savePct')

    if orig is not None and save_pct is not None:
        price_html = f"""<div class="sc-price-block">
      <span class="sc-was">&pound;{orig:.2f}</span>
      <span class="sc-price">&pound;{price:.2f}</span>
      <span class="sc-badge">SAVE {save_pct}%</span>
    </div>"""
    else:
        price_html = f'<span class="sc-price">&pound;{price:.2f}</span>'

    # Component pills for the card
    pills_html = ''
    pills = s.get('componentPills', [])
    if pills:
        pill_items = ''.join(
            f'<span class="sc-card-pill"><span class="sc-cp-name">{escape(p["name"])}</span>'
            f'<span class="sc-cp-size">{escape(p["size"])}</span>'
            f'<span class="sc-cp-price">&pound;{p["price"]:.2f}</span></span>'
            for p in pills
        )
        pills_html = f'<div class="sc-card-pills">{pill_items}</div>'

    return f"""<article class="stack-card">
  <a class="stack-card-link" href="{s['url']}">
    <div class="stack-card-eyebrow">— STACK · {len(pills)} COMPOUNDS</div>
    <h3 class="stack-card-name">{escape(s['name'])}</h3>
    <div class="stack-card-full">{escape(s['fullName'])}</div>
    {pills_html}
    <p class="stack-card-desc">{escape(s['shortDesc'])}</p>
    <div class="stack-card-ft">
      {price_html}
      <span class="stack-card-action">View stack →</span>
    </div>
  </a>
</article>"""


# ======================================================================== #
# COMPOUND PAGE — /compounds/{slug}/
# ======================================================================== #
def gen_compound_page(compound, all_compounds, all_stacks):
    c = compound
    title = f"{c['name']} — {c['fullName']}"
    if c.get('cas'):
        title += f" · CAS {c['cas']}"
    title += f" · {SITE_NAME}"
    description = (f"{c['name']} ({c['fullName']}) for in vitro research use. "
                   f"HPLC-verified{' ' + str(c['purity']) + '%' if c.get('purity') else ''} purity, batch CoA supplied, "
                   f"UK dispatch from £{min(s['p'] for s in c['sizes']):.2f}. "
                   f"{'CAS ' + c['cas'] + '. ' if c.get('cas') else ''}Not for human consumption.")[:310]

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/compounds/', 'label': 'Compounds'},
        {'href': f"/compounds/{c['categorySlug']}/", 'label': c['categoryLabel']},
        {'label': c['name']},
    ])

    # Hero
    spec_items = [
        ('CAS Number', c.get('cas') or '—'),
        ('Molecular Formula', c.get('formula') or '—'),
        ('HPLC Purity', f"{c['purity']}% (batch-verified)" if c.get('purity') else '—'),
        ('Form', 'Lyophilised powder'),
        ('Storage', '2–8°C, desiccated, protected from light'),
        ('Classification', 'Research reagent — in vitro use only'),
    ]
    spec_html = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in spec_items)

    # Order panel — size options + acknowledgement + Add to Order
    size_opts = ''
    for i, sz in enumerate(c['sizes']):
        checked = 'checked' if i == 0 else ''
        note = f'<span class="cp-size-note">{escape(sz["note"])}</span>' if sz.get('note') else ''

        # Build price display for this size
        badge    = sz.get('badge')
        was_p    = sz.get('wasPrice')
        rrp_p    = sz.get('rrp')
        save_pct = sz.get('savePct')

        if badge == 'save' and was_p is not None:
            price_display = f"""<span class="cp-size-price-wrap">
    <span class="cp-size-was">&pound;{was_p:.2f}</span>
    <span class="cp-size-p">&pound;{sz['p']:.2f}</span>
    <span class="cp-size-badge cp-badge-save">SAVE {save_pct}%</span>
  </span>"""
        elif badge == 'best_price' and rrp_p is not None:
            price_display = f"""<span class="cp-size-price-wrap">
    <span class="cp-size-was">&pound;{rrp_p:.2f}</span>
    <span class="cp-size-p">&pound;{sz['p']:.2f}</span>
    <span class="cp-size-badge cp-badge-best">BEST PRICE</span>
  </span>"""
        else:
            price_display = f'<span class="cp-size-p">&pound;{sz["p"]:.2f}</span>'

        size_opts += f"""<label class="cp-size-opt">
  <input type="radio" name="size" value="{escape(sz['l'])}" data-price="{sz['p']}" {checked}>
  <span class="cp-size-l">{escape(sz['l'])}</span>
  {price_display}
  {note}
</label>"""

    hero = f"""<section class="cp-hero">

  <div class="cp-img-col">
    <div class="cp-img-placeholder" aria-label="Product image — {escape(c['name'])}">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#01D3A0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      <span class="cp-img-label">{escape(c['name'])}</span>
      <span class="cp-img-sub">PRODUCT IMAGE</span>
    </div>
    <div class="cp-img-badges">
      <span class="cp-badge">HPLC VERIFIED</span>
      <span class="cp-badge">COA SUPPLIED</span>
      <span class="cp-badge cp-badge-purity">&ge;{c.get('purity', 98)}% PURITY</span>
    </div>
  </div>

  <div class="cp-hero-main">
    <div class="cp-eyebrow">— {escape(c['categoryLabel'])}</div>
    <h1 class="cp-h1">{escape(c['name'])} <em>{escape(c['fullName'])}</em></h1>
    {disclaimer_inline(c['name'])}
    <p class="cp-lede">{escape(c['shortDesc'])}</p>
    <dl class="cp-spec">{spec_html}</dl>
  </div>

  <aside class="cp-order" aria-label="Order panel">
    <div class="cp-order-hdr">Order for research</div>
    <form class="cp-order-form" data-compound="{escape(c['slug'])}" data-name="{escape(c['name'])}" data-full="{escape(c['fullName'])}" data-url="{escape(c['url'])}" id="order-form">
      <div class="cp-size-label">Vial size</div>
      <div class="cp-sizes">{size_opts}</div>

      <label class="cp-ack">
        <input type="checkbox" name="ack" id="ack" required>
        <span>I confirm this is for <strong>in vitro research use only</strong> and not for human or veterinary consumption.</span>
      </label>

      <button type="submit" class="cp-order-btn" id="add-to-order-btn">Add to order</button>

      <ul class="cp-order-meta">
        <li><span class="cpom-ic">&#x2713;</span> Batch CoA supplied with every order</li>
        <li><span class="cpom-ic">&#x2713;</span> Royal Mail Tracked 48 &middot; UK dispatch</li>
        <li><span class="cpom-ic">&#x2713;</span> Dispatched within 48 hours</li>
        <li><span class="cpom-ic">&#x2713;</span> Pay by Zempler bank transfer</li>
      </ul>
    </form>
  </aside>

</section>"""

    # Research overview (uses existing description)
    overview = f"""<section class="cp-section" id="overview">
  <h2 class="sec-t">Research overview</h2>
  <p>{escape(c['description'])}</p>
  <p class="cp-source-note">Summary paraphrased from the peer-reviewed preclinical literature. Full citations will be available in the <a href="/research/">research library</a>. For in vitro research use only.</p>
</section>"""

    # Full specs table
    formula = c.get('formula') or '—'
    mw = c.get('molecularWeight') or '—'
    seq = c.get('sequence') or '—'
    specs_table = f"""<section class="cp-section" id="specifications">
  <h2 class="sec-t">Compound specifications</h2>
  <div class="cp-table-wrap">
    <table class="cp-spec-table">
      <tbody>
        <tr><th scope="row">Common name</th><td>{escape(c['name'])}</td></tr>
        <tr><th scope="row">Full name</th><td>{escape(c['fullName'])}</td></tr>
        <tr><th scope="row">CAS number</th><td>{escape(c.get('cas') or '—')}</td></tr>
        <tr><th scope="row">Molecular formula</th><td>{escape(formula)}</td></tr>
        <tr><th scope="row">Molecular weight</th><td>{escape(mw)}</td></tr>
        <tr><th scope="row">Sequence</th><td class="mono">{escape(seq)}</td></tr>
        <tr><th scope="row">HPLC purity</th><td>{c['purity']}% (batch-verified)</td></tr>
        <tr><th scope="row">Appearance</th><td>White to off-white lyophilised powder</td></tr>
        <tr><th scope="row">Solubility</th><td>Bacteriostatic water, sterile saline</td></tr>
        <tr><th scope="row">Storage (lyophilised)</th><td>2–8°C, protected from light</td></tr>
        <tr><th scope="row">Storage (reconstituted)</th><td>2–8°C, up to 28 days</td></tr>
        <tr><th scope="row">Supplied as</th><td>{', '.join(escape(s['l']) for s in c['sizes'])}</td></tr>
      </tbody>
    </table>
  </div>
</section>"""

    # CoA section
    coa_section = f"""<section class="cp-section" id="coa">
  <h2 class="sec-t">Batch testing and certificate of analysis</h2>
  <p>Every batch of {escape(c['name'])} is third-party HPLC-tested prior to dispatch. A batch-specific certificate of analysis documenting HPLC purity, mass spectrometry confirmation, and appearance is supplied with every order.</p>
  <p>Previous batch CoAs are archived in the <a href="/about/coa-library/">CoA library</a>. For batch-specific CoA requests prior to purchase, contact <a href="mailto:{CONTACT_EMAIL}?subject=CoA request - {escape(c['name'])}">{CONTACT_EMAIL}</a>.</p>
</section>"""

    # Related compounds (same category, exclude self)
    related = [x for x in all_compounds if x['category'] == c['category'] and x['slug'] != c['slug']][:3]
    related_html = ''
    if related:
        related_html = f"""<section class="cp-section" id="related-compounds">
  <h2 class="sec-t">Related compounds</h2>
  <div class="prod-grid">{''.join(compound_card(r) for r in related)}</div>
</section>"""

    # Related stacks (stacks that contain this compound)
    related_stacks = [s for s in all_stacks if c['slug'] in s.get('components', [])]
    stacks_html = ''
    if related_stacks:
        stacks_html = f"""<section class="cp-section" id="related-stacks">
  <h2 class="sec-t">Stacks containing {escape(c['name'])}</h2>
  <div class="stack-grid">{''.join(_stack_card_mini(s) for s in related_stacks[:3])}</div>
</section>"""

    # FAQ
    faq_section = faq_block(c['faq'])

    # Compliance block
    compliance = f"""<section class="cp-compliance">
  <h2 class="visually-hidden">Compliance notice</h2>
  <p><strong>For in vitro research use only.</strong> {escape(c['name'])} is supplied solely as a research reagent for qualified professionals conducting in vitro or animal-model studies. It is not a medicinal product within the meaning of the Human Medicines Regulations 2012. It has not been evaluated by the MHRA or FDA. It is not intended for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition. Any use outside lawful scientific research is outside the scope of sale.</p>
</section>"""

    # Product schema (no MedicalDrug — stays as generic Product)
    offers = [{
        "@type": "Offer",
        "url": SITE_URL + c['url'],
        "priceCurrency": "GBP",
        "price": f"{s['p']:.2f}",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "sku": f"VP-{c['slug'].upper()}-{s['l'].replace(' ', '')}",
    } for s in c['sizes']]

    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": c['fullName'],
        "alternateName": c['name'],
        "description": c['shortDesc'],
        "brand": {"@type": "Brand", "name": SITE_NAME},
        "sku": f"VP-{c['slug'].upper()}",
        "image": f"{SITE_URL}/assets/images/compounds/{c['slug']}.png",
        "url": SITE_URL + c['url'],
        "audience": {"@type": "Audience", "audienceType": "Research professionals"},
        "offers": offers[0] if len(offers) == 1 else offers,
    }
    if c.get('cas'):
        product_schema["identifier"] = {
            "@type": "PropertyValue",
            "propertyID": "CAS",
            "value": c['cas'],
        }

    schemas = [product_schema]
    if c.get('faq'):
        schemas.append(faq_schema_ld(c['faq']))

    body = '\n'.join([bc, hero, overview, specs_table, coa_section, related_html, stacks_html, faq_section, compliance])

    extra_js = '<script src="/assets/js/compound.js"></script>'
    return base_layout(
        title=title,
        description=description,
        path=c['url'],
        body=body,
        extra_schema_ld=schemas,
        page_class='page-compound',
        extra_js=extra_js,
    )


# ======================================================================== #
# STACK ROOT — /stacks/
# ======================================================================== #
def gen_stacks_root(stacks):
    title = f"Research Stacks — Multi-Compound Bundles — {SITE_NAME}"
    description = (f"{len(stacks)} curated multi-compound research stacks grouping peptides commonly "
                   "studied together. HPLC-verified, CoA-supplied, UK dispatch. For in vitro research use only.")

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'Stacks'}])

    intro = f"""<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Research stacks</h1>
    <p class="page-lede">
      Multi-compound bundles grouping {len(stacks)} combinations of compounds commonly studied together in preclinical research. Each stack supplies individual lyophilised vials for each component compound.
    </p>
    <p class="page-compliance"><strong>For in vitro research use only.</strong> Not for human or veterinary consumption.</p>
  </div>
</section>"""

    grid = f"""<section class="stack-grid-sec">
  <div class="sec-i">
    <div class="stack-grid">
      {''.join(_stack_card_mini(s) for s in stacks)}
    </div>
  </div>
</section>"""

    body = '\n'.join([bc, intro, grid])

    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Research Stacks",
        "url": f"{SITE_URL}/stacks/",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": SITE_URL + s['url'], "name": s['fullName']}
                for i, s in enumerate(stacks)
            ],
        },
    }

    return base_layout(
        title=title,
        description=description,
        path='/stacks/',
        body=body,
        extra_schema_ld=[collection_schema],
        page_class='page-stacks-root',
    )


# ======================================================================== #
# STACK PAGE — /stacks/{slug}/
# ======================================================================== #
def gen_stack_page(stack, all_compounds):
    s = stack
    title = f"{s['name']} — {s['fullName']} · {SITE_NAME}"
    description = (f"{s['name']} research stack: {s['fullName']}. "
                   f"HPLC-verified, CoA-supplied, UK dispatch £{s['sizes'][0]['p']:.2f}. "
                   "For in vitro research use only.")[:310]

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/stacks/', 'label': 'Stacks'},
        {'label': s['name']},
    ])

    # Components with full data
    components = [next((c for c in all_compounds if c['slug'] == slug), None) for slug in s.get('components', [])]
    components = [c for c in components if c]

    # Size option (stacks usually have one size)
    size      = s['sizes'][0]
    orig_p    = size.get('origPrice')
    save_pct  = size.get('savePct')

    if orig_p is not None and save_pct is not None:
        stack_price_display = f"""<span class="cp-size-price-wrap">
    <span class="cp-size-was">&pound;{orig_p:.2f}</span>
    <span class="cp-size-p">&pound;{size['p']:.2f}</span>
    <span class="cp-size-badge cp-badge-save">SAVE {save_pct}%</span>
  </span>"""
        stack_saving_line = f'<p class="cp-stack-saving">Save {save_pct}% vs buying individually &mdash; bundle discount applied</p>'
    else:
        stack_price_display = f'<span class="cp-size-p">&pound;{size["p"]:.2f}</span>'
        stack_saving_line = ''

    # "What's in this stack" pill section for the order panel
    pills = s.get('componentPills', [])
    if pills:
        pill_items = '\n      '.join(
            f'<div class="csp-pill">'
            f'<span class="csp-name">{escape(p["name"])}</span>'
            f'<span class="csp-dot" aria-hidden="true">·</span>'
            f'<span class="csp-size">{escape(p["size"])}</span>'
            f'<span class="csp-dot" aria-hidden="true">·</span>'
            f'<span class="csp-price">&pound;{p["price"]:.2f}</span>'
            f'</div>'
            for p in pills
        )
        contents_section = f"""<div class="cp-stack-contents">
      <div class="cp-stack-contents-lbl">WHAT'S IN THIS STACK</div>
      <div class="cp-stack-pills">
      {pill_items}
      </div>
    </div>"""
    else:
        contents_section = ''

    hero = f"""<section class="cp-hero">
  <div class="cp-hero-main">
    <div class="cp-eyebrow">— STACK · {len(components)} COMPOUNDS</div>
    <h1 class="cp-h1">{escape(s['name'])} <em>{escape(s['fullName'])}</em></h1>
    {disclaimer_inline(s['name'])}
    <p class="cp-lede">{escape(s['shortDesc'])}</p>
  </div>

  <aside class="cp-order" aria-label="Order panel">
    <div class="cp-order-hdr">Order for research</div>
    <form class="cp-order-form" data-compound="{escape(s['slug'])}" data-name="{escape(s['name'])}" data-full="{escape(s['fullName'])}" data-url="{escape(s['url'])}" id="order-form">
      {contents_section}
      <div class="cp-size-label">Stack price</div>
      <div class="cp-sizes">
        <label class="cp-size-opt">
          <input type="radio" name="size" value="{escape(size['l'])}" data-price="{size['p']}" checked>
          <span class="cp-size-l">{escape(size['l'])}</span>
          {stack_price_display}
        </label>
      </div>
      {stack_saving_line}
      <label class="cp-ack">
        <input type="checkbox" name="ack" id="ack" required>
        <span>I confirm this is for <strong>in vitro research use only</strong> and not for human or veterinary consumption.</span>
      </label>
      <button type="submit" class="cp-order-btn" id="add-to-order-btn">Add to order</button>
      <ul class="cp-order-meta">
        <li><span class="cpom-ic">✓</span> Batch CoAs for each compound</li>
        <li><span class="cpom-ic">✓</span> Royal Mail Tracked 48 · UK dispatch</li>
        <li><span class="cpom-ic">✓</span> Dispatched within 48 hours</li>
        <li><span class="cpom-ic">✓</span> Pay by Zempler bank transfer</li>
      </ul>
    </form>
  </aside>
</section>"""

    overview = f"""<section class="cp-section" id="overview">
  <h2 class="sec-t">Research overview</h2>
  <p>{escape(s['description'])}</p>
</section>"""

    # Components breakdown — each linked to its compound page
    comp_rows = []
    for c in components:
        comp_rows.append(f"""<article class="stack-comp">
  <div class="stack-comp-h">
    <h3 class="stack-comp-name"><a href="{c['url']}">{escape(c['name'])}</a></h3>
    <div class="stack-comp-full">{escape(c['fullName'])}</div>
  </div>
  <p class="stack-comp-desc">{escape(c['shortDesc'])}</p>
  <div class="stack-comp-meta">
    {f"<span>CAS {escape(c['cas'])}</span>" if c.get('cas') else ''}
    <span>{c['purity']}% HPLC</span>
    <a class="stack-comp-link" href="{c['url']}">View {escape(c['name'])} →</a>
  </div>
</article>""")

    components_section = f"""<section class="cp-section" id="components">
  <h2 class="sec-t">Compounds in this stack</h2>
  <div class="stack-comps">{''.join(comp_rows)}</div>
</section>"""

    compliance = f"""<section class="cp-compliance">
  <h2 class="visually-hidden">Compliance notice</h2>
  <p><strong>For in vitro research use only.</strong> This stack is supplied solely as research reagents for qualified professionals conducting in vitro or animal-model studies. No compound in this stack is a medicinal product. None has been evaluated by the MHRA or FDA. None is intended for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition.</p>
</section>"""

    # Product schema
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": s['fullName'],
        "alternateName": s['name'],
        "description": s['shortDesc'],
        "brand": {"@type": "Brand", "name": SITE_NAME},
        "sku": f"VP-STACK-{s['slug'].upper()}",
        "url": SITE_URL + s['url'],
        "audience": {"@type": "Audience", "audienceType": "Research professionals"},
        "offers": {
            "@type": "Offer",
            "url": SITE_URL + s['url'],
            "priceCurrency": "GBP",
            "price": f"{size['p']:.2f}",
            "availability": "https://schema.org/InStock",
        },
    }

    body = '\n'.join([bc, hero, overview, components_section, compliance])
    extra_js = '<script src="/assets/js/compound.js"></script>'

    return base_layout(
        title=title,
        description=description,
        path=s['url'],
        body=body,
        extra_schema_ld=[product_schema],
        page_class='page-stack',
        extra_js=extra_js,
    )


# ======================================================================== #
# SUPPLY PAGE — /supplies/{slug}/
# ======================================================================== #
def gen_supply_page(supply):
    c = supply
    title = f"{c['name']} — {c['fullName']} · {SITE_NAME}"
    description = f"{c['fullName']} for peptide reconstitution. UK dispatch. For in vitro research use only."

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/compounds/', 'label': 'Compounds'},
        {'label': c['name']},
    ])

    # Size opts
    size_opts = ''
    for i, sz in enumerate(c['sizes']):
        checked = 'checked' if i == 0 else ''
        size_opts += f"""<label class="cp-size-opt">
  <input type="radio" name="size" value="{escape(sz['l'])}" data-price="{sz['p']}" {checked}>
  <span class="cp-size-l">{escape(sz['l'])}</span>
  <span class="cp-size-p">&pound;{sz['p']:.2f}</span>
</label>"""

    hero = f"""<section class="cp-hero">
  <div class="cp-hero-main">
    <div class="cp-eyebrow">— RESEARCH SUPPLIES</div>
    <h1 class="cp-h1">{escape(c['name'])} <em>{escape(c['fullName'])}</em></h1>
    <p class="cp-lede">{escape(c['shortDesc'])}</p>
  </div>
  <aside class="cp-order" aria-label="Order panel">
    <div class="cp-order-hdr">Order for research</div>
    <form class="cp-order-form" data-compound="{escape(c['slug'])}" data-name="{escape(c['name'])}" data-full="{escape(c['fullName'])}" data-url="{escape(c['url'])}" id="order-form">
      <div class="cp-size-label">Volume</div>
      <div class="cp-sizes">{size_opts}</div>
      <button type="submit" class="cp-order-btn" id="add-to-order-btn">Add to order</button>
      <ul class="cp-order-meta">
        <li><span class="cpom-ic">✓</span> USP-grade sterile water</li>
        <li><span class="cpom-ic">✓</span> Royal Mail Tracked 48 · UK dispatch</li>
      </ul>
    </form>
  </aside>
</section>"""

    body_main = f"""<section class="cp-section">
  <h2 class="sec-t">About {escape(c['name'])}</h2>
  <p>{escape(c['description'])}</p>
</section>"""

    body = '\n'.join([bc, hero, body_main])
    extra_js = '<script src="/assets/js/compound.js"></script>'

    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": c['fullName'],
        "alternateName": c['name'],
        "description": c['shortDesc'],
        "brand": {"@type": "Brand", "name": SITE_NAME},
        "sku": f"VP-{c['slug'].upper()}",
        "url": SITE_URL + c['url'],
        "offers": [{
            "@type": "Offer",
            "url": SITE_URL + c['url'],
            "priceCurrency": "GBP",
            "price": f"{s['p']:.2f}",
            "availability": "https://schema.org/InStock",
        } for s in c['sizes']],
    }

    return base_layout(
        title=title, description=description, path=c['url'],
        body=body, extra_schema_ld=[product_schema],
        page_class='page-supply', extra_js=extra_js,
    )
