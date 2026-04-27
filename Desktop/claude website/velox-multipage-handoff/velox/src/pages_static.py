"""
Generators for static/content pages: research hub, tools, about, contact,
shipping, FAQ, legal, cart, and the checkout flow.
"""
import json
from html import escape
from components import (
    base_layout,
    breadcrumb,
    faq_block,
    faq_schema_ld,
    SITE_URL,
    SITE_NAME,
    COMPANY,
    COMPANY_NUMBER,
    CONTACT_EMAIL,
)


# ======================================================================== #
# RESEARCH LIBRARY HUB — /research/
# ======================================================================== #
def gen_research_hub():
    title = f"Research Library — Peptide Mechanisms and Preclinical Literature Summaries · {SITE_NAME}"
    description = ("Peer-reviewed peptide research summaries covering mechanisms of action, "
                   "preclinical findings, and reconstitution protocols. "
                   "For scientific reference — not medical advice.")

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'Research Library'}])

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Research library</h1>
    <p class="page-lede">
      Plain-language summaries of the peer-reviewed preclinical literature behind each research compound in our catalogue. Articles cover mechanisms of action, study designs, key findings, and the limitations of preclinical data.
    </p>
    <p class="page-compliance">
      <strong>For scientific reference only — not medical advice.</strong>
      All content is derived from peer-reviewed preclinical and in vitro research. Summaries are provided for scientific reference, not medical advice, diagnosis, or treatment. All compounds are for in vitro research use only. Not for human or veterinary consumption.
    </p>
  </div>
</section>

<section class="research-placeholder">
  <div class="sec-i">
    <div class="rp-card">
      <div class="rp-card-eyebrow">— IN DEVELOPMENT</div>
      <h2 class="rp-card-t">Research library — launching May 2026</h2>
      <p>
        The Velox Peptides research library is under active development. Initial articles will cover:
      </p>
      <ul class="rp-list">
        <li><strong>BPC-157: Mechanisms of Action in Preclinical Angiogenesis Research</strong> — rodent studies of vascular tissue response, VEGF interaction, and mucosal protection.</li>
        <li><strong>Retatrutide and Multi-Receptor Metabolic Research</strong> — the triple-agonist pharmacology investigated in GLP-1 / GIP / glucagon pathway studies.</li>
        <li><strong>Peptide Reconstitution — A Technical Guide</strong> — bacteriostatic water, concentration calculations, and handling best practice.</li>
        <li><strong>Understanding HPLC Purity in Research Peptides</strong> — how HPLC testing works, what a certificate of analysis documents, and how to read one.</li>
        <li><strong>Semax and BDNF Pathway Activity in Preclinical Neuroscience</strong> — the Eastern European research tradition and key findings.</li>
        <li><strong>MOTS-c and Mitochondrial Pathway Research</strong> — the mitochondrially-encoded peptide investigated for AMPK activation and metabolic signalling.</li>
      </ul>
      <p>
        Articles will publish on a weekly cadence. To be notified when articles publish, email <a href="mailto:{CONTACT_EMAIL}?subject=Research library notification">{CONTACT_EMAIL}</a>.
      </p>
    </div>
  </div>
</section>

<section class="research-cta">
  <div class="sec-i">
    <div class="cta-card">
      <div>
        <h2 class="cta-t">Browse the compound catalogue</h2>
        <p>Every compound page includes a research overview, specification table, and batch testing summary.</p>
      </div>
      <a class="btn-p" href="/compounds/">View compounds →</a>
    </div>
  </div>
</section>
"""
    return base_layout(
        title=title, description=description, path='/research/',
        body=body, page_class='page-research',
    )


# ======================================================================== #
# RECONSTITUTION CALCULATOR — /tools/reconstitution-calculator/
# ======================================================================== #
def gen_reconstitution_calculator():
    title = f"Peptide Reconstitution Calculator — Dose, Volume, Concentration · {SITE_NAME}"
    description = ("Research peptide reconstitution calculator: enter peptide amount (mg), "
                   "bacteriostatic water volume (ml), and desired dose (mcg) to calculate concentration "
                   "and volume per injection. For in vitro research use only.")

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'label': 'Reconstitution calculator'},
    ])

    body = f"""{bc}
<section class="calc-sec">
  <div class="sec-i">
    <div class="sec-hdr">
      <div class="page-eyebrow">— RESEARCH TOOL</div>
      <h1 class="page-h1">Peptide reconstitution calculator</h1>
      <p class="page-lede">
        Calculate the concentration of a reconstituted research peptide and the volume required to deliver a given quantity for <strong>in vitro research use</strong>. Enter the peptide amount, the volume of bacteriostatic water used for reconstitution, and the quantity required per application.
      </p>
      <p class="page-compliance"><strong>For in vitro research use only.</strong> This calculator is a research tool. It is not medical advice and not for human or veterinary administration.</p>
    </div>

    <div class="calc-grid">
      <div class="calc-form">
        <div class="calc-row">
          <label class="calc-lbl" for="calc-pep">Peptide amount (mg)</label>
          <input class="calc-inp" id="calc-pep" type="number" step="0.1" min="0.1" placeholder="e.g. 10" value="10">
          <div class="calc-hint">Total mg of compound in the vial.</div>
        </div>
        <div class="calc-row">
          <label class="calc-lbl" for="calc-water">Bacteriostatic water (ml)</label>
          <input class="calc-inp" id="calc-water" type="number" step="0.1" min="0.1" placeholder="e.g. 2" value="2">
          <div class="calc-hint">Volume added for reconstitution.</div>
        </div>
        <div class="calc-row">
          <label class="calc-lbl" for="calc-dose">Quantity per application (mcg)</label>
          <input class="calc-inp" id="calc-dose" type="number" step="10" min="1" placeholder="e.g. 250" value="250">
          <div class="calc-hint">Micrograms (µg) required per research application.</div>
        </div>
      </div>

      <div class="calc-results">
        <div class="calc-res-hdr">Calculated values</div>
        <div class="calc-res">
          <div class="calc-res-k">Concentration</div>
          <div class="calc-res-v" id="calc-conc">—</div>
        </div>
        <div class="calc-res">
          <div class="calc-res-k">Volume per application</div>
          <div class="calc-res-v" id="calc-vol">—</div>
        </div>
        <div class="calc-res">
          <div class="calc-res-k">Units per 1 ml insulin syringe</div>
          <div class="calc-res-v" id="calc-units">—</div>
        </div>
        <div class="calc-res">
          <div class="calc-res-k">Total applications per vial</div>
          <div class="calc-res-v" id="calc-apps">—</div>
        </div>
      </div>
    </div>

    <div class="calc-notes">
      <h2 class="sec-t-sm">Notes</h2>
      <ul>
        <li>1 insulin syringe unit = 0.01 ml on a standard 1 ml (100-unit) insulin syringe. The "units" value above is a conversion only — it does not constitute guidance for human administration.</li>
        <li>Bacteriostatic water (0.9% benzyl alcohol) allows a reconstituted peptide to be stored at 2–8°C for up to 28 days.</li>
        <li>For sterile storage without bacteriostatic water, reconstituted peptide should be used within 24 hours.</li>
        <li>This calculator performs arithmetic only. Study design, protocol development, and handling decisions are the responsibility of the researcher.</li>
      </ul>
    </div>
  </div>
</section>
"""
    extra_js = '<script src="/assets/js/calculator.js"></script>'
    return base_layout(
        title=title, description=description,
        path='/tools/reconstitution-calculator/',
        body=body, extra_js=extra_js, page_class='page-calculator',
    )


# ======================================================================== #
# ABOUT — /about/
# ======================================================================== #
def gen_about_index():
    title = f"About {SITE_NAME} — UK Research Peptide Supplier"
    description = (f"{SITE_NAME} is a UK research peptide supplier based in Northern Ireland. "
                   "HPLC-verified compounds, certificate of analysis on every order, "
                   "48-hour dispatch. For in vitro research use only.")

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'About'}])

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">About {SITE_NAME}</h1>
    <p class="page-lede">{SITE_NAME} is a United Kingdom research reagent supplier operating as {COMPANY} (Company No. {COMPANY_NUMBER}). We supply HPLC-verified research peptides to laboratory and qualified research customers across the UK, dispatched from Northern Ireland by Royal Mail Tracked 48.</p>
  </div>
</section>

<section class="about-section">
  <div class="sec-i">
    <h2 class="sec-t">What we supply</h2>
    <p>Research-grade peptide compounds for in vitro scientific research, together with reconstitution supplies (bacteriostatic water) required for laboratory use. Every compound is sold strictly as a research reagent and is not a medicinal product within the meaning of the Human Medicines Regulations 2012.</p>

    <h2 class="sec-t">How we test</h2>
    <p>Every batch is third-party HPLC-tested prior to dispatch. Certificates of analysis document HPLC purity, mass spectrometry confirmation of molecular weight, and appearance. A batch CoA is included with every order; historical batch CoAs are archived in our <a href="/about/coa-library/">CoA library</a>.</p>

    <h2 class="sec-t">How we dispatch</h2>
    <p>Orders are dispatched within 48 hours of cleared bank transfer payment, Monday to Friday. Standard UK delivery is via Royal Mail Tracked 48 — 2-4 working days. Full details are in our <a href="/shipping/">shipping information</a>.</p>

    <h2 class="sec-t">How to order</h2>
    <p>Payment is by UK bank transfer to our Zempler Bank business account. Full bank details are provided at checkout. Your order is processed on receipt of cleared payment, and dispatch confirmation is sent by email.</p>

    <h2 class="sec-t">Contact</h2>
    <p>For pre-purchase enquiries, batch CoA requests, or research protocol queries, contact <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
  </div>
</section>

<section class="about-compliance">
  <div class="sec-i">
    <div class="ab-comp-card">
      <div class="ab-comp-eyebrow">— COMPLIANCE STATEMENT</div>
      <p>{SITE_NAME} supplies research reagents for <em>in vitro</em> use by qualified researchers. No product sold by {SITE_NAME} is a medicinal product within the meaning of the Human Medicines Regulations 2012. No product has been evaluated by the MHRA or FDA. No product is intended for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition. See our <a href="/legal/research-use-policy/">Research Use Policy</a>.</p>
    </div>
  </div>
</section>
"""
    return base_layout(
        title=title, description=description, path='/about/',
        body=body, page_class='page-about',
    )


# ======================================================================== #
# CONTACT — /contact/
# ======================================================================== #
def gen_contact():
    title = f"Contact — {SITE_NAME}"
    description = "Contact Velox Peptides for research enquiries, batch CoA requests, or order support. UK research peptide supplier based in Northern Ireland."

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'Contact'}])

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Contact</h1>
    <p class="page-lede">For research enquiries, pre-purchase questions, batch certificate of analysis requests, and order support.</p>
  </div>
</section>

<section class="contact-section">
  <div class="sec-i">
    <div class="contact-grid">
      <div>
        <h2 class="sec-t">Email</h2>
        <p><a class="contact-email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
        <p>Replies typically within one working day, Monday to Friday.</p>

        <h2 class="sec-t">What to include</h2>
        <p>For <strong>pre-purchase enquiries</strong> — your compound of interest, size, and any specific batch CoA questions.</p>
        <p>For <strong>existing orders</strong> — your order reference number and the nature of the enquiry.</p>
        <p>For <strong>research protocol questions</strong> — we cannot provide protocol advice, but we can confirm compound specifications, batch characteristics, and handling recommendations.</p>

        <h2 class="sec-t">Company details</h2>
        <address class="contact-address">
          {COMPANY}<br>
          Company number: {COMPANY_NUMBER}<br>
          Registered in Northern Ireland
        </address>
      </div>
      <div>
        <div class="contact-panel">
          <div class="contact-panel-hdr">What we cannot help with</div>
          <ul>
            <li>Human or veterinary dosing advice — we do not supply products for this purpose</li>
            <li>Medical questions of any kind — consult a qualified healthcare professional</li>
            <li>Pre-purchase sample supply</li>
            <li>Research protocol design or experimental consultation</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    return base_layout(
        title=title, description=description, path='/contact/',
        body=body, page_class='page-contact',
    )


# ======================================================================== #
# SHIPPING — /shipping/
# ======================================================================== #
def gen_shipping():
    title = f"Shipping and Delivery — {SITE_NAME}"
    description = "Velox Peptides shipping and delivery. Royal Mail Tracked 48, UK only, 48-hour dispatch from Northern Ireland. For in vitro research use only."

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'Shipping'}])

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Shipping and delivery</h1>
    <p class="page-lede">All Velox Peptides orders dispatch from Northern Ireland via Royal Mail Tracked 48, to UK addresses only.</p>
  </div>
</section>

<section class="policy-section">
  <div class="sec-i">
    <div class="policy-grid">
      <div class="policy-card">
        <h2 class="sec-t">Delivery method</h2>
        <p><strong>Royal Mail Tracked 48.</strong> All UK orders ship via this method as standard. A tracking number is supplied by email at dispatch.</p>
        <p>Tracked 48 is Royal Mail's 2-4 working day tracked service. Delivery is attempted by your local Royal Mail delivery office; if you are not in, a card is left and the parcel returned to the local office for collection or redelivery.</p>
      </div>
      <div class="policy-card">
        <h2 class="sec-t">Dispatch time</h2>
        <p>Orders are dispatched within <strong>48 hours of cleared bank transfer payment</strong> (Monday to Friday, excluding UK public holidays).</p>
        <p>Orders received at the weekend or on a public holiday dispatch on the next working day once payment has cleared.</p>
      </div>
      <div class="policy-card">
        <h2 class="sec-t">Delivery area</h2>
        <p><strong>United Kingdom only</strong> — including England, Scotland, Wales, Northern Ireland, Channel Islands, and the Isle of Man.</p>
        <p>We do not currently dispatch outside the UK. International orders entered in error will be refunded.</p>
      </div>
      <div class="policy-card">
        <h2 class="sec-t">Shipping cost</h2>
        <p>Royal Mail Tracked 48: <strong>£4.99</strong> flat rate for orders under £80. Free shipping on orders £80 or over.</p>
      </div>
      <div class="policy-card">
        <h2 class="sec-t">Packaging</h2>
        <p>Orders ship in plain outer packaging with no external branding. Inner packaging identifies Velox Peptides on the invoice and certificate of analysis documentation.</p>
      </div>
      <div class="policy-card">
        <h2 class="sec-t">If your order does not arrive</h2>
        <p>Tracked 48 parcels are normally delivered within 2-4 working days of dispatch. If your parcel is not received within 10 working days of the dispatch confirmation email, contact <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> with your order reference and tracking number.</p>
      </div>
    </div>
  </div>
</section>
"""
    return base_layout(title=title, description=description, path='/shipping/', body=body, page_class='page-shipping')


# ======================================================================== #
# FAQ — /faq/
# ======================================================================== #
def gen_faq():
    title = f"FAQ — {SITE_NAME}"
    description = "Frequently asked questions about Velox Peptides research compounds, HPLC testing, certificates of analysis, UK delivery, and payment by bank transfer."

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'FAQ'}])

    faqs = [
        {
            'q': 'Are your research peptides legal to buy in the UK?',
            'a': 'Yes. All peptides sold by Velox Peptides are supplied strictly for in vitro scientific research purposes only. They are not licensed medicines and are not for human consumption. Their sale and purchase for research purposes is lawful in the UK.'
        },
        {
            'q': 'What purity standard are Velox Peptides compounds?',
            'a': 'All compounds are HPLC-tested to a minimum purity of 98%, with most compounds tested at 99% or higher. The exact batch-verified purity is shown on each compound page and on the certificate of analysis supplied with every order.'
        },
        {
            'q': 'Is a certificate of analysis supplied?',
            'a': 'Yes. Every order includes a batch-specific certificate of analysis documenting HPLC purity, mass spectrometry molecular weight confirmation, and physical appearance. Previous batch CoAs are archived in the <a href="/about/coa-library/">CoA library</a>.'
        },
        {
            'q': 'How quickly will my UK order be dispatched?',
            'a': 'Orders are dispatched within 48 hours of cleared bank transfer payment being received, Monday to Friday. Standard delivery is 2-4 working days via Royal Mail Tracked 48.'
        },
        {
            'q': 'How do I pay for research peptides?',
            'a': 'Payment is by UK bank transfer to our Zempler Bank business account. Full bank details are supplied at checkout. Your order is processed on receipt of cleared payment; dispatch confirmation follows by email.'
        },
        {
            'q': 'Do you ship outside the United Kingdom?',
            'a': 'No. Velox Peptides currently ships to UK addresses only (including Channel Islands and Isle of Man). International orders entered in error will be refunded.'
        },
        {
            'q': 'Can I order on behalf of a company or laboratory?',
            'a': 'Yes. If you require a VAT invoice made out to a company or research institution, include the company name and billing details at checkout or email <a href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a> after ordering.'
        },
        {
            'q': 'How should I store research peptides after delivery?',
            'a': 'Lyophilised peptides are stable at 2–8°C when kept desiccated and protected from light. After reconstitution with bacteriostatic water (0.9% BnOH), solutions are stable at 2–8°C for up to 28 days. See the individual compound page for compound-specific storage notes.'
        },
        {
            'q': 'Can I cancel or return an order?',
            'a': 'Orders that have not yet dispatched can be cancelled for a full refund by emailing <a href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a>. Once dispatched, research compounds are non-returnable for handling and chain-of-custody reasons. Full refund and returns details are in our <a href="/legal/refunds/">refunds policy</a>.'
        },
        {
            'q': 'Are you evaluated by the MHRA?',
            'a': 'No. Velox Peptides supplies research reagents for in vitro scientific research only. Our products are not medicinal products within the meaning of the Human Medicines Regulations 2012, and they have not been evaluated by the MHRA or FDA. They are not intended for human or veterinary consumption, diagnosis, treatment, cure, or prevention of any condition. See our <a href="/legal/mhra-statement/">MHRA statement</a>.'
        },
    ]

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Frequently asked questions</h1>
    <p class="page-lede">Answers to common questions about Velox Peptides research compounds, testing, delivery, and payment.</p>
  </div>
</section>
<section class="faq-page-sec">
  <div class="sec-i">
    {faq_block(faqs, heading="General questions")}
  </div>
</section>
"""
    return base_layout(
        title=title, description=description, path='/faq/',
        body=body, extra_schema_ld=[faq_schema_ld(faqs)],
        page_class='page-faq',
    )


# ======================================================================== #
# LEGAL PAGES — each generator returns HTML
# ======================================================================== #
def _legal_base(slug, heading, description, body_md):
    path = f'/legal/{slug}/'
    title = f"{heading} — {SITE_NAME}"
    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': heading}])
    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">{escape(heading)}</h1>
  </div>
</section>
<section class="legal-sec">
  <div class="legal-i">
{body_md}
  </div>
</section>
"""
    return base_layout(title=title, description=description, path=path, body=body, page_class='page-legal')


def gen_legal_research_use():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>1. Purpose of this policy</h2>
<p>This Research Use Policy defines the terms under which Velox Peptides (operated by {COMPANY}, Company No. {COMPANY_NUMBER}) supplies research reagents to customers. By placing an order, you agree to the terms of this policy in addition to our <a href="/legal/terms/">Terms and Conditions</a>.</p>

<h2>2. Status of the products supplied</h2>
<p>All research compounds supplied by Velox Peptides are sold strictly as research reagents intended for <strong>in vitro scientific research</strong>. No product supplied by Velox Peptides is:</p>
<ul>
  <li>A medicinal product within the meaning of the Human Medicines Regulations 2012;</li>
  <li>A veterinary medicinal product;</li>
  <li>A cosmetic product, food product, or food supplement;</li>
  <li>Evaluated, licensed, or approved by the Medicines and Healthcare products Regulatory Agency (MHRA), the Food and Drug Administration (FDA), or any comparable regulatory body.</li>
</ul>

<h2>3. Permitted use</h2>
<p>Customers may use products supplied by Velox Peptides only for the following purposes:</p>
<ul>
  <li>In vitro scientific research conducted in a laboratory setting by qualified researchers;</li>
  <li>Analytical reference and calibration;</li>
  <li>Educational demonstration in an appropriate laboratory training context.</li>
</ul>

<h2>4. Prohibited use</h2>
<p>Products supplied by Velox Peptides must not be:</p>
<ul>
  <li>Administered to humans or non-human animals for any purpose;</li>
  <li>Used to diagnose, treat, cure, mitigate, or prevent any disease or medical condition;</li>
  <li>Added to food, beverages, or consumer products of any kind;</li>
  <li>Re-sold or distributed to any party who does not accept the terms of this policy;</li>
  <li>Used in any way that violates United Kingdom law or the law of the jurisdiction in which the customer operates.</li>
</ul>

<h2>5. Customer responsibilities</h2>
<p>By placing an order, the customer represents and warrants that:</p>
<ul>
  <li>They are aged 18 or over;</li>
  <li>They are a qualified researcher or otherwise authorised to handle research reagents under applicable UK law;</li>
  <li>They will use the products purchased exclusively for the permitted purposes described in Section 3;</li>
  <li>They will not use the products for any of the prohibited purposes described in Section 4;</li>
  <li>They will store, handle, and dispose of the products in accordance with standard laboratory practice.</li>
</ul>

<h2>6. No medical or therapeutic claims</h2>
<p>Velox Peptides makes no claims — express or implied — regarding the suitability of any product for the diagnosis, treatment, cure, mitigation, or prevention of any disease or medical condition in humans or animals. All descriptive content on this website is derived from peer-reviewed preclinical research literature and is provided for scientific reference only. It is not medical advice and must not be relied upon as such.</p>

<h2>7. Regulatory position</h2>
<p>The sale of research reagents for in vitro scientific research is lawful in the United Kingdom. Products supplied by Velox Peptides fall outside the regulatory scope of the Human Medicines Regulations 2012 because they are not supplied or offered for use as medicinal products. Any re-purposing of these products for medicinal use is unauthorised, outside the scope of sale, and undertaken entirely at the customer's own risk and responsibility.</p>

<h2>8. Changes to this policy</h2>
<p>Velox Peptides may update this policy from time to time. The effective date at the top of this page reflects the date of the most recent update. Continued use of the website constitutes acceptance of the current policy.</p>

<h2>9. Contact</h2>
<p>Questions about this policy: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
"""
    return _legal_base('research-use-policy', 'Research Use Policy',
                       f"{SITE_NAME} Research Use Policy — defines in vitro research-only terms of supply and prohibited uses. All products are research reagents only, not medicinal products.",
                       body_md)


def gen_legal_mhra():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>Statement regarding the Medicines and Healthcare products Regulatory Agency (MHRA)</h2>

<p><strong>{SITE_NAME}</strong> (operated by {COMPANY}, Company No. {COMPANY_NUMBER}) supplies research reagents for in vitro scientific research only.</p>

<p>No product sold by Velox Peptides is a medicinal product within the meaning of the Human Medicines Regulations 2012. No product sold by Velox Peptides has been evaluated by the MHRA. No product sold by Velox Peptides is licensed, registered, or authorised for human or veterinary medical use.</p>

<p>Velox Peptides makes no therapeutic, medical, or health claims regarding any product it supplies. All descriptive content on this website is derived from the peer-reviewed preclinical research literature and is provided for scientific reference only.</p>

<p>The sale of research reagents for in vitro scientific research is lawful in the United Kingdom. Products supplied for this purpose fall outside the regulatory scope of the Human Medicines Regulations 2012.</p>

<p>Any use of Velox Peptides products outside the scope of lawful in vitro scientific research is outside the scope of sale and is the sole responsibility of the end user.</p>

<p>For the avoidance of doubt:</p>
<ul>
  <li>No Velox Peptides product is intended for human consumption.</li>
  <li>No Velox Peptides product is intended for veterinary use.</li>
  <li>No Velox Peptides product should be used to diagnose, treat, cure, mitigate, or prevent any disease.</li>
  <li>No Velox Peptides product is a food, food supplement, cosmetic, or consumer product.</li>
</ul>

<p>If you have questions about the regulatory status of a specific product, contact <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
"""
    return _legal_base('mhra-statement', 'MHRA Statement',
                       f"{SITE_NAME} MHRA statement. All products supplied are research reagents for in vitro use only and are not medicinal products.",
                       body_md)


def gen_legal_terms():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>1. Parties</h2>
<p>These Terms and Conditions govern the supply of research reagents by Velox Peptides, a trading name of {COMPANY} (Company No. {COMPANY_NUMBER}), registered in Northern Ireland, United Kingdom ("we", "us", "our"). The person placing an order ("you", "customer") accepts these terms by placing an order.</p>

<h2>2. Products</h2>
<p>All products supplied are research reagents for in vitro scientific research only. See our <a href="/legal/research-use-policy/">Research Use Policy</a> and <a href="/legal/mhra-statement/">MHRA Statement</a>.</p>

<h2>3. Orders and acceptance</h2>
<p>An order placed through this website is an offer to purchase the products described. We accept your offer when we confirm dispatch by email. We may decline any order at our discretion, including where we have reason to believe the order is for prohibited use or for an underage customer.</p>

<h2>4. Prices</h2>
<p>Prices are shown in Great British Pounds (GBP) and include applicable taxes unless stated otherwise. Prices may change at any time; the price shown at the time of order is the price payable.</p>

<h2>5. Payment</h2>
<p>Payment is by UK bank transfer to our Zempler Bank business account. Bank details are supplied at checkout. Your order is processed on receipt of cleared payment. If payment is not received within 7 days of order, the order is cancelled.</p>

<h2>6. Delivery</h2>
<p>Products are dispatched via Royal Mail Tracked 48 to UK addresses only. Dispatch occurs within 48 hours of cleared payment (Monday to Friday). See <a href="/shipping/">Shipping and Delivery</a>.</p>

<h2>7. Risk and title</h2>
<p>Risk of loss or damage passes to you on delivery to the address specified at checkout. Title to the products passes on receipt of cleared payment in full.</p>

<h2>8. Cancellation and returns</h2>
<p>Orders not yet dispatched may be cancelled by emailing <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> for a full refund. Once dispatched, research compounds are non-returnable for handling and chain-of-custody reasons. See <a href="/legal/refunds/">Refunds Policy</a>.</p>

<h2>9. Warranty</h2>
<p>We warrant that each batch of product supplied meets the HPLC purity specification documented in the accompanying certificate of analysis. We give no other warranties, express or implied, regarding the products, and specifically no warranty of fitness for any human or veterinary purpose.</p>

<h2>10. Limitation of liability</h2>
<p>Our total liability arising out of or in connection with any order is limited to the price paid for that order. We are not liable for any indirect, consequential, or special loss. Nothing in these terms limits liability for death or personal injury caused by our negligence, fraud, or any other liability that cannot be limited by UK law.</p>

<h2>11. Prohibited uses and indemnity</h2>
<p>You agree to use the products only for the purposes permitted by our Research Use Policy. You indemnify us against all loss, claims, and liability arising from any use outside those permitted purposes.</p>

<h2>12. Governing law and jurisdiction</h2>
<p>These terms are governed by the law of Northern Ireland. The courts of Northern Ireland have exclusive jurisdiction over any dispute arising out of or in connection with these terms.</p>

<h2>13. Contact</h2>
<p>Questions about these terms: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
"""
    return _legal_base('terms', 'Terms and Conditions',
                       f"Terms and Conditions for {SITE_NAME} research peptide orders. UK bank transfer payment, Royal Mail Tracked 48 delivery, research reagent supply only.",
                       body_md)


def gen_legal_privacy():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>1. Who we are</h2>
<p>This website is operated by Velox Peptides, a trading name of {COMPANY} (Company No. {COMPANY_NUMBER}), Northern Ireland, UK. We are the data controller for the personal data we collect about you.</p>

<h2>2. What we collect</h2>
<p>When you place an order, we collect: your name, email address, phone number (optional), delivery address, billing address (if different), and your order history. We do not collect payment card details — payment is by bank transfer and your bank processes the transfer information.</p>
<p>When you browse the website, we receive standard web traffic data: IP address, browser type, pages visited, referrer URL, timestamps.</p>

<h2>3. Why we collect it</h2>
<ul>
  <li><strong>Order fulfilment</strong> — to process your order, dispatch it, and communicate about delivery.</li>
  <li><strong>Customer support</strong> — to answer enquiries and support existing orders.</li>
  <li><strong>Legal compliance</strong> — to comply with UK tax, accounting, and consumer law obligations.</li>
  <li><strong>Security</strong> — to protect the website from abuse and fraud.</li>
</ul>

<h2>4. Legal basis</h2>
<p>We process your personal data on the following bases under UK GDPR: (a) performance of a contract to fulfil your order; (b) legal obligation for tax and accounting records; (c) legitimate interest for fraud prevention and website security.</p>

<h2>5. How long we keep it</h2>
<p>Order records are kept for 7 years to comply with UK tax and accounting obligations. Enquiry emails are kept for 2 years unless you request deletion earlier. Web traffic logs are kept for 30 days.</p>

<h2>6. Who we share it with</h2>
<p>We share your data only with: (a) Royal Mail, to dispatch your order; (b) our accountants and banking providers, for financial record-keeping; (c) law enforcement or regulatory authorities if legally required. We do not sell or rent your personal data to any third party for marketing purposes.</p>

<h2>7. Your rights under UK GDPR</h2>
<ul>
  <li>Request access to the personal data we hold about you;</li>
  <li>Request correction of inaccurate data;</li>
  <li>Request deletion of your data, subject to legal retention requirements;</li>
  <li>Object to processing for legitimate interest purposes;</li>
  <li>Request restriction of processing;</li>
  <li>Request portability of your data.</li>
</ul>
<p>To exercise any of these rights, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>

<h2>8. Cookies</h2>
<p>See our <a href="/legal/cookies/">Cookie Policy</a> for details on the cookies this website uses.</p>

<h2>9. Complaints</h2>
<p>If you have a complaint about how we handle your personal data, you may contact the UK Information Commissioner's Office (ICO) at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>

<h2>10. Changes</h2>
<p>We may update this policy from time to time. The effective date at the top of this page reflects the date of the most recent update.</p>
"""
    return _legal_base('privacy', 'Privacy Policy',
                       f"{SITE_NAME} Privacy Policy. What we collect, why, how long we keep it, and your rights under UK GDPR.",
                       body_md)


def gen_legal_cookies():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>What cookies are</h2>
<p>Cookies are small text files stored by your browser when you visit a website. They allow the website to remember information about your visit, such as your preferences.</p>

<h2>The cookies we use</h2>

<h3>Strictly necessary cookies</h3>
<ul>
  <li><code>vp_entry</code> — records that you have acknowledged our research-use entry notice. Set for 30 days from acceptance. Without this cookie you would see the acknowledgement overlay on every page.</li>
  <li><code>vp_cart</code> — stores the contents of your current order so you can continue shopping across pages. Cleared when you complete or empty your order. Held in your browser's local storage.</li>
  <li><code>vp_checkout</code> — stores delivery address details entered during checkout, so they persist between the address and payment steps. Cleared when you complete your order. Held in your browser's session storage.</li>
</ul>

<h3>Analytics cookies</h3>
<p>We may deploy a privacy-respecting analytics provider (such as Plausible or Fathom) to measure aggregate website usage. These providers do not use tracking cookies and do not identify individual users.</p>

<h3>Third-party cookies</h3>
<p>We do not currently deploy third-party advertising, tracking, or social media cookies on this website.</p>

<h2>Managing cookies</h2>
<p>You can clear cookies from your browser at any time. Clearing the <code>vp_entry</code> cookie will re-display the research-use acknowledgement overlay on your next visit. Clearing your browser storage will empty your current order.</p>

<h2>Contact</h2>
<p>Questions about cookies: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
"""
    return _legal_base('cookies', 'Cookie Policy',
                       f"{SITE_NAME} Cookie Policy. Describes the strictly necessary cookies used for the research-use acknowledgement and order flow.",
                       body_md)


def gen_legal_refunds():
    body_md = f"""<p class="legal-effective">Last updated: 23 April 2026</p>

<h2>1. Orders not yet dispatched</h2>
<p>If your order has not yet been dispatched, we will cancel it and issue a full refund to the bank account from which payment was received. Email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> with your order reference as soon as possible. Refunds are processed within 3 working days of cancellation confirmation.</p>

<h2>2. Orders that have been dispatched</h2>
<p>Once dispatched, research compounds are non-returnable for handling, storage-condition, and chain-of-custody reasons. We cannot verify that a compound returned to us has been stored correctly since dispatch, and we cannot restock it safely.</p>
<p>We will, however, take responsibility for any of the following:</p>
<ul>
  <li><strong>Damage in transit.</strong> Vials broken or leaking on arrival — photograph the packaging and the vial immediately on receipt and email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. We will replace or refund at our discretion.</li>
  <li><strong>Wrong product dispatched.</strong> If we have sent the wrong compound or size, we will arrange a return and resend the correct product at no cost to you, or refund in full.</li>
  <li><strong>Product fails the batch CoA specification.</strong> If independent testing shows the product does not meet the HPLC purity stated on the supplied certificate of analysis, we will refund or replace. Testing must be conducted by a reputable third-party HPLC laboratory, and we may request the full test report.</li>
</ul>

<h2>3. Refund method</h2>
<p>Refunds are issued by UK bank transfer to the bank account from which payment was received. We do not issue cash refunds or store credit.</p>

<h2>4. Non-delivery</h2>
<p>If your tracked parcel has not arrived within 10 working days of dispatch confirmation, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. We will investigate with Royal Mail and, depending on the investigation outcome, either reissue the order or refund in full.</p>

<h2>5. Consumer rights</h2>
<p>This policy does not affect any statutory rights you may have under the Consumer Rights Act 2015 for products supplied as consumer items. However, products supplied by Velox Peptides are research reagents supplied to research customers, and the statutory distance-selling right of withdrawal under the Consumer Contracts Regulations 2013 does not apply to orders placed on behalf of a research institution or business.</p>

<h2>6. Contact</h2>
<p>For refund and return queries: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
"""
    return _legal_base('refunds', 'Refunds and Returns',
                       f"{SITE_NAME} refunds and returns policy. Pre-dispatch cancellation, damage in transit, wrong product, and batch-CoA failure.",
                       body_md)


# ======================================================================== #
# CART — /cart/
# ======================================================================== #
def gen_cart():
    title = f"Current Order — {SITE_NAME}"
    description = "Review your current research order before checkout."

    bc = breadcrumb([{'href': '/', 'label': 'Home'}, {'label': 'Current order'}])

    body = f"""{bc}
<section class="page-intro">
  <div class="sec-i">
    <h1 class="page-h1">Your order</h1>
    <p class="page-lede">Review your current research order. Payment is processed by UK bank transfer after you place the order.</p>
  </div>
</section>

<section class="cart-sec">
  <div class="sec-i">
    <div class="cart-grid">
      <div class="cart-items-col">
        <div id="cart-items"></div>
        <div class="cart-empty" id="cart-empty" style="display:none;">
          <div class="cart-empty-ic">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          </div>
          <h2>Your order is empty</h2>
          <p>Add compounds from the catalogue to build your order.</p>
          <a class="btn-p" href="/compounds/">Browse compounds</a>
        </div>
      </div>
      <aside class="cart-summary" id="cart-summary">
        <div class="cart-sum-hdr">Order summary</div>
        <div class="cart-sum-row"><span>Subtotal</span><span id="cart-subtotal">£0.00</span></div>
        <div class="cart-sum-row"><span>Shipping</span><span id="cart-shipping">£4.99</span></div>
        <div class="cart-sum-row cart-sum-total"><span>Total</span><span id="cart-total">£4.99</span></div>
        <div class="cart-sum-note">Free shipping on orders £80+</div>
        <a class="btn-p cart-proceed" href="/checkout/shipping/" id="cart-proceed">Proceed to delivery</a>
        <a class="btn-o cart-continue" href="/compounds/">Continue browsing</a>
        <div class="cart-sum-pay">
          <div class="cart-sum-pay-hdr">Payment method</div>
          <p>UK bank transfer to Zempler Bank business account. Bank details supplied at checkout. Order processed on cleared payment.</p>
        </div>
      </aside>
    </div>
  </div>
</section>
"""
    extra_js = '<script src="/assets/js/cart.js"></script>'
    return base_layout(
        title=title, description=description, path='/cart/',
        body=body, extra_js=extra_js, page_class='page-cart',
    )


# ======================================================================== #
# CHECKOUT — SHIPPING STEP
# ======================================================================== #
def gen_checkout_shipping():
    title = f"Delivery Details — Checkout — {SITE_NAME}"
    description = "Enter your UK delivery address. Royal Mail Tracked 48, UK only."

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/cart/', 'label': 'Order'},
        {'label': 'Delivery'},
    ])

    body = f"""{bc}
<section class="checkout-steps" aria-label="Checkout progress">
  <div class="sec-i">
    <ol class="co-steps">
      <li class="co-step co-step-active">1. Delivery</li>
      <li class="co-step">2. Payment</li>
      <li class="co-step">3. Confirmation</li>
    </ol>
  </div>
</section>

<section class="checkout-sec">
  <div class="sec-i">
    <div class="co-grid">
      <div class="co-form-col">
        <h1 class="page-h1">Delivery details</h1>
        <p class="page-lede">Royal Mail Tracked 48, UK addresses only. Dispatch within 48 hours of cleared payment.</p>

        <form id="shipping-form" class="co-form" novalidate>
          <h2 class="sec-t">Contact</h2>
          <div class="f-grid-2">
            <div class="f-row"><label class="f-lbl" for="sh-fname">First name *</label><input class="f-inp" id="sh-fname" name="fname" required></div>
            <div class="f-row"><label class="f-lbl" for="sh-lname">Last name *</label><input class="f-inp" id="sh-lname" name="lname" required></div>
            <div class="f-row f-full"><label class="f-lbl" for="sh-email">Email address *</label><input class="f-inp" id="sh-email" name="email" type="email" required></div>
            <div class="f-row f-full"><label class="f-lbl" for="sh-phone">Phone number (optional)</label><input class="f-inp" id="sh-phone" name="phone" type="tel" placeholder="+44 ..."></div>
          </div>

          <h2 class="sec-t">Delivery address</h2>
          <div class="f-grid-2">
            <div class="f-row f-full"><label class="f-lbl" for="sh-addr1">Address line 1 *</label><input class="f-inp" id="sh-addr1" name="addr1" required></div>
            <div class="f-row f-full"><label class="f-lbl" for="sh-addr2">Address line 2</label><input class="f-inp" id="sh-addr2" name="addr2"></div>
            <div class="f-row"><label class="f-lbl" for="sh-city">City *</label><input class="f-inp" id="sh-city" name="city" required></div>
            <div class="f-row"><label class="f-lbl" for="sh-post">Postcode *</label><input class="f-inp" id="sh-post" name="postcode" required></div>
            <div class="f-row f-full"><label class="f-lbl" for="sh-country">Country</label><input class="f-inp" id="sh-country" name="country" value="United Kingdom" readonly></div>
          </div>

          <h2 class="sec-t">Delivery method</h2>
          <div class="ship-opts">
            <label class="ship-opt">
              <input type="radio" name="shipping" value="tracked48" checked>
              <div class="ship-opt-main">
                <div class="ship-opt-name">Royal Mail Tracked 48</div>
                <div class="ship-opt-sub">2–4 working days, tracked. UK only.</div>
              </div>
              <div class="ship-opt-price" id="ship-price">£4.99</div>
            </label>
          </div>

          <label class="co-ack">
            <input type="checkbox" name="ack" required>
            <span>I confirm this order is for <strong>in vitro research use only</strong> and I have read the <a href="/legal/research-use-policy/" target="_blank">Research Use Policy</a>.</span>
          </label>

          <div class="co-err" id="co-err"></div>

          <button type="submit" class="btn-p co-submit">Continue to payment →</button>
          <a href="/cart/" class="co-back">← Back to order</a>
        </form>
      </div>

      <aside class="co-summary">
        <div class="co-sum-hdr">Order summary</div>
        <div id="co-cart-items"></div>
        <div class="co-sum-rows">
          <div class="co-sum-row"><span>Subtotal</span><span id="co-subtotal">£0.00</span></div>
          <div class="co-sum-row"><span>Shipping</span><span id="co-shipping">£4.99</span></div>
          <div class="co-sum-row co-sum-total"><span>Total</span><span id="co-total">£4.99</span></div>
        </div>
      </aside>
    </div>
  </div>
</section>
"""
    extra_js = '<script src="/assets/js/checkout.js"></script>'
    return base_layout(
        title=title, description=description, path='/checkout/shipping/',
        body=body, extra_js=extra_js, page_class='page-checkout',
    )


# ======================================================================== #
# CHECKOUT — PAYMENT STEP
# ======================================================================== #
def gen_checkout_payment():
    title = f"Payment — Bank Transfer Details — Checkout — {SITE_NAME}"
    description = "Bank transfer payment to Zempler Bank business account. Order processed on cleared payment."

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/cart/', 'label': 'Order'},
        {'label': 'Payment'},
    ])

    body = f"""{bc}
<section class="checkout-steps">
  <div class="sec-i">
    <ol class="co-steps">
      <li class="co-step co-step-done">✓ Delivery</li>
      <li class="co-step co-step-active">2. Payment</li>
      <li class="co-step">3. Confirmation</li>
    </ol>
  </div>
</section>

<section class="checkout-sec">
  <div class="sec-i">
    <div class="co-grid">
      <div class="co-form-col">
        <h1 class="page-h1">Payment</h1>
        <p class="page-lede">Payment is by UK bank transfer to our Zempler Bank business account. Place your order to generate your order reference, then transfer using that reference.</p>

        <div class="pay-method">
          <div class="pay-method-hdr">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
            <span>UK Bank Transfer — Zempler Bank</span>
          </div>
          <p>After you place this order, you will receive:</p>
          <ul>
            <li>Your unique order reference number</li>
            <li>Full bank transfer details (account name, sort code, account number)</li>
            <li>The total amount to transfer</li>
          </ul>
          <p>Your order is processed once payment clears (typically within 1–2 hours for Faster Payments, or the next working day for other transfers). You will receive a dispatch confirmation email when your parcel ships.</p>
        </div>

        <form id="payment-form" class="co-form">
          <h2 class="sec-t">Billing address</h2>
          <label class="f-checkbox">
            <input type="checkbox" id="bill-same" checked>
            <span>Billing address is the same as delivery address</span>
          </label>
          <div id="bill-fields" style="display:none;">
            <div class="f-grid-2">
              <div class="f-row f-full"><label class="f-lbl" for="bill-addr1">Address line 1</label><input class="f-inp" id="bill-addr1" name="bill_addr1"></div>
              <div class="f-row"><label class="f-lbl" for="bill-city">City</label><input class="f-inp" id="bill-city" name="bill_city"></div>
              <div class="f-row"><label class="f-lbl" for="bill-post">Postcode</label><input class="f-inp" id="bill-post" name="bill_postcode"></div>
            </div>
          </div>

          <label class="co-ack">
            <input type="checkbox" name="terms" required>
            <span>I have read and accept the <a href="/legal/terms/" target="_blank">Terms &amp; Conditions</a> and <a href="/legal/research-use-policy/" target="_blank">Research Use Policy</a>.</span>
          </label>

          <div class="co-err" id="co-err"></div>

          <button type="submit" class="btn-p co-submit">Place order →</button>
          <a href="/checkout/shipping/" class="co-back">← Back to delivery</a>
        </form>
      </div>

      <aside class="co-summary">
        <div class="co-sum-hdr">Order summary</div>
        <div id="co-cart-items"></div>
        <div class="co-sum-rows">
          <div class="co-sum-row"><span>Subtotal</span><span id="co-subtotal">£0.00</span></div>
          <div class="co-sum-row"><span>Shipping</span><span id="co-shipping">£4.99</span></div>
          <div class="co-sum-row co-sum-total"><span>Total</span><span id="co-total">£4.99</span></div>
        </div>
        <div class="co-deliver-to" id="co-deliver-to"></div>
      </aside>
    </div>
  </div>
</section>
"""
    extra_js = '<script src="/assets/js/checkout.js"></script>'
    return base_layout(
        title=title, description=description, path='/checkout/payment/',
        body=body, extra_js=extra_js, page_class='page-checkout',
    )


# ======================================================================== #
# CHECKOUT — CONFIRMATION
# ======================================================================== #
def gen_checkout_confirmation():
    title = f"Order Confirmation — Bank Transfer Details — {SITE_NAME}"
    description = "Order received. Bank transfer details for completing payment."

    bc = breadcrumb([
        {'href': '/', 'label': 'Home'},
        {'href': '/cart/', 'label': 'Order'},
        {'label': 'Confirmation'},
    ])

    body = f"""{bc}
<section class="checkout-steps">
  <div class="sec-i">
    <ol class="co-steps">
      <li class="co-step co-step-done">✓ Delivery</li>
      <li class="co-step co-step-done">✓ Payment</li>
      <li class="co-step co-step-active">3. Confirmation</li>
    </ol>
  </div>
</section>

<section class="confirm-sec">
  <div class="sec-i">
    <div class="confirm-card">
      <div class="confirm-ic">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <h1 class="confirm-t">Order received</h1>
      <p class="confirm-sub">Complete your bank transfer to finalise the order. Dispatch confirmation will follow by email once payment clears.</p>

      <div class="confirm-ref">
        <div class="confirm-ref-lbl">Order reference</div>
        <div class="confirm-ref-v" id="confirm-ref">VP-…</div>
        <div class="confirm-ref-note">Use this as your payment reference.</div>
      </div>

      <div class="confirm-bank">
        <div class="confirm-bank-hdr">Bank transfer details</div>
        <dl class="confirm-bank-dl">
          <div><dt>Account name</dt><dd>{COMPANY}</dd></div>
          <div><dt>Bank</dt><dd>Zempler Bank</dd></div>
          <div><dt>Sort code</dt><dd id="bank-sort">XX-XX-XX</dd></div>
          <div><dt>Account number</dt><dd id="bank-acc">XXXXXXXX</dd></div>
          <div><dt>Amount</dt><dd id="confirm-amount">£0.00</dd></div>
          <div><dt>Reference</dt><dd id="confirm-ref-2">VP-…</dd></div>
        </dl>
        <p class="confirm-bank-note">
          <strong>Important.</strong> Use your order reference as the payment reference so we can match your transfer to your order. Faster Payments typically clear within 1–2 hours; other transfers may take up to 1 working day.
        </p>
      </div>

      <div class="confirm-next">
        <h2 class="sec-t">What happens next</h2>
        <ol class="confirm-next-list">
          <li>You'll receive an order confirmation email with these bank details repeated.</li>
          <li>Complete the bank transfer using your order reference.</li>
          <li>Once payment clears, we dispatch your order within 48 hours (working days).</li>
          <li>You'll receive a dispatch confirmation email with your Royal Mail tracking number.</li>
          <li>Your order arrives within 2–4 working days via Royal Mail Tracked 48.</li>
        </ol>
      </div>

      <div class="confirm-summary" id="confirm-summary"></div>

      <div class="confirm-cta">
        <a class="btn-p" href="/compounds/">Continue browsing</a>
        <a class="btn-o" href="mailto:{CONTACT_EMAIL}?subject=Order query">Contact us about this order</a>
      </div>
    </div>
  </div>
</section>
"""
    extra_js = '<script src="/assets/js/checkout.js"></script>'
    return base_layout(
        title=title, description=description, path='/checkout/confirmation/',
        body=body, extra_js=extra_js, page_class='page-confirmation',
    )
