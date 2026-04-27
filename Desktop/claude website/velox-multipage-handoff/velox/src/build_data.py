"""
Transforms raw product data from the source HTML into the structured
compounds.json + stacks.json files used by the site generator.

Key transformations applied:
  - Slug generation for URLs
  - Category slug mapping (cognitive, metabolic, healing-and-repair, growth, anti-ageing)
  - Merge Retatrutide + Retatrutide Pen into one compound with 4 sizes
  - Move BPC-157 + TB500 bundle from 'healing' to 'stacks' (it IS a stack)
  - Strip all sale/badge/Best seller text per copy register rules
  - Generate shortDesc (first 2 sentences of desc, used for meta descriptions)
  - Generate per-compound FAQ seeds (research-use focused, schema-safe)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent

# ----------------------------- CATEGORY MAP ----------------------------- #
CATEGORY_MAP = {
    'cognitive':  {'slug': 'cognitive',            'label': 'Cognitive',              'shortDesc': 'Compounds studied for effects on BDNF expression, neurotransmitter signalling, and synaptic plasticity in preclinical research.'},
    'metabolic':  {'slug': 'metabolic',            'label': 'Metabolic',              'shortDesc': 'Compounds studied for effects on GLP-1, GIP, glucagon, AMPK, and mitochondrial signalling pathways in preclinical research.'},
    'healing':    {'slug': 'healing-and-repair',   'label': 'Healing & Repair',       'shortDesc': 'Compounds studied for roles in tissue response, angiogenesis, cellular migration, and structural repair pathways in preclinical research.'},
    'growth':     {'slug': 'growth',               'label': 'Growth',                 'shortDesc': 'Growth hormone-releasing hormone analogues studied for GH and IGF-1 pathway activity in preclinical research.'},
    'aging':      {'slug': 'anti-ageing',          'label': 'Anti-Ageing',            'shortDesc': 'Compounds studied for roles in cellular antioxidant activity, collagen synthesis, and sirtuin pathway function in preclinical research.'},
    'supplies':   {'slug': 'supplies',             'label': 'Supplies',               'shortDesc': 'Reconstitution reagents and research consumables.'},
    'stacks':     {'slug': 'stacks',               'label': 'Stacks',                 'shortDesc': 'Multi-compound research bundles.'},
}

# --------------------------- SLUG OVERRIDES ----------------------------- #
SLUG_OVERRIDES = {
    1: 'bacteriostatic-water',   # from "Bac Water"
    2: 'bpc-157',
    15: 'tb-500',
    4: 'cjc-1295',               # strip "wo DAC" — it's a variant description, not the slug
    14: 'tesamorelin',
    5: 'dsip',
    12: 'selank',
    13: 'semax',
    23: 'dihexa',
    9: 'mots-c',
    10: 'nad-plus',              # hyphenate the +
    11: 'retatrutide',
    6: 'ghk-cu',
    7: 'glutathione',
    8: 'melanotan-ii',

    # Stacks
    3: 'bpc157-tb500-bundle',
    101: 'cognitive',
    102: 'cognitive-and-sleep',
    112: 'advanced-cognitive',
    103: 'gh-peptide',
    104: 'anti-ageing',
    105: 'metabolic',
    106: 'skin-and-aesthetic',
    107: 'ultimate-repair',
    108: 'repair-and-metabolic',
    109: 'gh-and-metabolic',
}

# Compounds referenced by each stack (for linking). Slugs only.
STACK_COMPONENTS = {
    3:   ['bpc-157', 'tb-500'],
    101: ['semax', 'selank'],
    102: ['semax', 'selank', 'dsip'],
    112: ['semax', 'selank', 'dihexa'],
    103: ['cjc-1295', 'tesamorelin'],
    104: ['ghk-cu', 'glutathione', 'nad-plus'],
    105: ['mots-c', 'nad-plus', 'retatrutide'],
    106: ['melanotan-ii', 'ghk-cu', 'glutathione'],
    107: ['bpc-157', 'tb-500', 'ghk-cu'],
    108: ['retatrutide', 'bpc-157', 'tb-500'],
    109: ['retatrutide', 'tesamorelin'],
}

# Which category does each stack relate to? (for "Related stacks" on category hubs)
STACK_CATEGORY_TAGS = {
    3:   ['healing'],
    101: ['cognitive'],
    102: ['cognitive'],
    112: ['cognitive'],
    103: ['growth'],
    104: ['aging'],
    105: ['metabolic'],
    106: ['aging'],
    107: ['healing'],
    108: ['healing', 'metabolic'],
    109: ['growth', 'metabolic'],
}

# --------------------- MOLECULAR WEIGHT (manual lookup) ------------------ #
# Where known. Leave blank if unsure; we don't invent values.
MOLECULAR_WEIGHTS = {
    'bpc-157':       '1419.5 g/mol',
    'tb-500':        '4963.4 g/mol',
    'cjc-1295':      '3367.8 g/mol',
    'tesamorelin':   '5195.8 g/mol',
    'dsip':          '848.9 g/mol',
    'selank':        '751.9 g/mol',
    'semax':         '813.9 g/mol',
    'dihexa':        '308.4 g/mol',
    'mots-c':        '2174.5 g/mol',
    'nad-plus':      '663.4 g/mol',
    'retatrutide':   '4731.3 g/mol',
    'ghk-cu':        '402.9 g/mol',
    'glutathione':   '307.3 g/mol',
    'melanotan-ii':  '1024.2 g/mol',
}

# --------------------- SEQUENCES (manual lookup) ------------------------- #
SEQUENCES = {
    'bpc-157':       'GEPPPGKPADDAGLV',
    'tb-500':        'Ac-SDKPDMAEIEKFDKSKLKKTETQEKNPLPSKETIEQEKQAGES-OH (frag)',
    'cjc-1295':      'HAIBU-Y-D-Ala-DFA-LRKVLGQLSARKLLQDIMSR-NH2 (no DAC)',
    'tesamorelin':   'trans-3-hexenoyl-YADAIFTNSYRKVLGQLSARKLLQDIMSR-NH2',
    'dsip':          'WAGGDASGE',
    'selank':        'TKPRPGP',
    'semax':         'MEHFPGP',
    'dihexa':        'N-hexanoic-Tyr-Ile-(6)-aminohexanoic',
    'mots-c':        'MRWQEMGYIFYPRKLR',
    'retatrutide':   'Modified 39-aa peptide — triple agonist',
    'ghk-cu':        'Gly-His-Lys · Cu²⁺',
    'glutathione':   'γ-L-glutamyl-L-cysteinyl-glycine',
    'melanotan-ii':  'Ac-Nle-c(Asp-His-D-Phe-Arg-Trp-Lys)-NH₂',
}


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r'[\+]', '-plus', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


def first_sentences(text: str, n: int = 2) -> str:
    sents = re.split(r'(?<=[.!?])\s+', text)
    return ' '.join(sents[:n])


def clean_sale_language(text: str) -> str:
    """Remove any residual consumer-commerce phrasing from descriptions."""
    # Existing descriptions are already well-written in scientific register.
    # This is a defensive pass.
    bad_phrases = [r'\bbest\s+seller\b', r'\bon\s+sale\b', r'\bnew\s+arrival\b']
    for p in bad_phrases:
        text = re.sub(p, '', text, flags=re.IGNORECASE)
    return text


def build_faq(compound: dict) -> list:
    """Generate 3 research-use-focused FAQ entries. Schema-safe — no dosing."""
    name = compound['name']
    purity = compound.get('purity')
    cas = compound.get('cas')
    faqs = []
    # Q1: purity
    if purity:
        faqs.append({
            'q': f'What purity is Velox Peptides {name}?',
            'a': f'{name} is supplied at {purity}% HPLC-verified purity. A certificate of analysis is provided with every order. Every batch is third-party tested before dispatch.'
        })
    # Q2: reconstitution (generic, safe)
    if compound['category'] != 'supplies':
        faqs.append({
            'q': f'How is {name} supplied and reconstituted for research use?',
            'a': f'{name} is supplied as a lyophilised powder in sterile single-use vials. For in vitro research use, reconstitution is performed with bacteriostatic water. See the <a href="/tools/reconstitution-calculator/">reconstitution calculator</a> for volume calculations based on required concentration.'
        })
    # Q3: research context
    faqs.append({
        'q': f'What is {name} used for in preclinical research?',
        'a': f'{name} is studied in the peer-reviewed literature across the pathways described in the research overview above. Velox Peptides supplies {name} strictly as a research reagent for in vitro use by qualified researchers. It is not a medicinal product and is not for human or veterinary consumption.'
    })
    # Q4: CAS (factual anchor, good for rich results)
    if cas:
        faqs.append({
            'q': f'What is the CAS number for {name}?',
            'a': f'The CAS registry number for {name} is {cas}. This identifier is listed on every batch certificate of analysis supplied with orders.'
        })
    return faqs


# ============================ MAIN BUILD ================================ #
def main():
    raw_path = ROOT / 'data' / 'products_raw.json'
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    compounds = []
    stacks = []
    supplies = []

    # Handle Retatrutide Pen merge into Retatrutide
    reta_pen = next(p for p in raw if p['id'] == 116)
    reta = next(p for p in raw if p['id'] == 11)
    # Merge pen size into retatrutide's sizes
    for sz in reta_pen['sizes']:
        reta['sizes'].append({**sz, 'note': 'Pre-loaded pen format — no reconstitution required.'})
    # Remove Pen from processing
    raw = [p for p in raw if p['id'] != 116]

    for p in raw:
        pid = p['id']
        slug = SLUG_OVERRIDES.get(pid, slugify(p['name']))
        cat_slug = CATEGORY_MAP[p['cat']]['slug']
        cat_label = CATEGORY_MAP[p['cat']]['label']
        desc = clean_sale_language(p['desc'])

        record = {
            'id': pid,
            'slug': slug,
            'name': p['name'],
            'fullName': p['full'],
            'category': p['cat'],
            'categoryLabel': cat_label,
            'categorySlug': cat_slug,
            'cas': p.get('cas'),
            'formula': p.get('formula'),
            'molecularWeight': MOLECULAR_WEIGHTS.get(slug),
            'sequence': SEQUENCES.get(slug),
            'purity': p.get('purity'),
            'sizes': p['sizes'],
            'description': desc,
            'shortDesc': first_sentences(desc, 2),
            # Price display: current price = sale price if sale, else regular
            'origPriceRange': p.get('orig'),
            'isRecentlyAdded': p.get('badge') == 'New',
        }
        # Add FAQ
        record['faq'] = build_faq(record)

        # Route to the right list
        if p['cat'] == 'stacks' or pid == 3:
            # id=3 is the BPC/TB500 bundle — belongs with stacks
            record['url'] = f'/stacks/{slug}/'
            record['components'] = STACK_COMPONENTS.get(pid, [])
            record['categoryTags'] = STACK_CATEGORY_TAGS.get(pid, [])
            stacks.append(record)
        elif p['cat'] == 'supplies':
            record['url'] = f'/supplies/{slug}/'
            supplies.append(record)
        else:
            record['url'] = f'/compounds/{slug}/'
            compounds.append(record)

    # Write output JSON files
    (ROOT / 'data').mkdir(exist_ok=True)
    with open(ROOT / 'data' / 'compounds.json', 'w', encoding='utf-8') as f:
        json.dump(compounds, f, indent=2, ensure_ascii=False)
    with open(ROOT / 'data' / 'stacks.json', 'w', encoding='utf-8') as f:
        json.dump(stacks, f, indent=2, ensure_ascii=False)
    with open(ROOT / 'data' / 'supplies.json', 'w', encoding='utf-8') as f:
        json.dump(supplies, f, indent=2, ensure_ascii=False)

    # Categories file
    cats = []
    for cat_key, meta in CATEGORY_MAP.items():
        if cat_key == 'supplies':
            continue
        cats.append({
            'key': cat_key,
            'slug': meta['slug'],
            'label': meta['label'],
            'shortDesc': meta['shortDesc'],
            'compoundCount': sum(1 for c in compounds if c['category'] == cat_key),
        })
    with open(ROOT / 'data' / 'categories.json', 'w', encoding='utf-8') as f:
        json.dump(cats, f, indent=2, ensure_ascii=False)

    print(f"Compounds: {len(compounds)}")
    print(f"Stacks: {len(stacks)}")
    print(f"Supplies: {len(supplies)}")
    print(f"Categories: {len(cats)}")

    # Sanity print
    print("\nCompound URLs:")
    for c in compounds:
        print(f"  {c['url']:<42} {c['name']}")
    print("\nStack URLs:")
    for s in stacks:
        print(f"  {s['url']:<42} {s['name']}")


if __name__ == '__main__':
    main()
