#!/usr/bin/env python3
"""
Velox Peptides static site generator.
Run from the src/ directory: python3 generate.py
Output written to ../output/
"""
import json
import os
import shutil
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
DATA_DIR = os.path.join(SRC_DIR, 'data')

sys.path.insert(0, SRC_DIR)

from components import SITE_URL, SITE_NAME, COMPANY
from pages_products import (
    gen_homepage, gen_catalogue_root, gen_category_hub,
    gen_compound_page, gen_stacks_root, gen_stack_page, gen_supply_page,
)
from pages_static import (
    gen_research_hub, gen_reconstitution_calculator, gen_about_index,
    gen_contact, gen_shipping, gen_faq,
    gen_legal_research_use, gen_legal_mhra, gen_legal_terms,
    gen_legal_privacy, gen_legal_cookies, gen_legal_refunds,
    gen_cart, gen_checkout_shipping, gen_checkout_payment, gen_checkout_confirmation,
)

FEATURED_SLUGS = ['bpc157-tb500-mix', 'retatrutide', 'tesamorelin', 'nad-plus', 'semax', 'selank', 'mots-c', 'ghk-cu']


def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), encoding='utf-8') as f:
        return json.load(f)


def write_page(path, html):
    """Write HTML for path (e.g. '/compounds/bpc-157/') to output dir."""
    clean = path.strip('/')
    dir_path = os.path.join(OUTPUT_DIR, *clean.split('/')) if clean else OUTPUT_DIR
    os.makedirs(dir_path, exist_ok=True)
    out_file = os.path.join(dir_path, 'index.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    return out_file


def main():
    compounds  = load_json('compounds.json')
    stacks     = load_json('stacks.json')
    supplies   = load_json('supplies.json')
    categories = load_json('categories.json')
    nav_cats   = [c for c in categories if c['key'] != 'stacks']

    if os.path.exists(OUTPUT_DIR):
        # Remove all contents except .git (preserve deployment repo if present)
        for entry in os.listdir(OUTPUT_DIR):
            if entry == '.git':
                continue
            full = os.path.join(OUTPUT_DIR, entry)
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)
    else:
        os.makedirs(OUTPUT_DIR)

    pages = []

    def wp(path, html):
        write_page(path, html)
        pages.append(path)
        print(f'  {path}')

    print('Generating pages...')

    wp('/', gen_homepage(compounds, stacks, nav_cats, FEATURED_SLUGS))
    wp('/compounds/', gen_catalogue_root(compounds, stacks, nav_cats))

    for cat in nav_cats:
        wp(f"/compounds/{cat['slug']}/", gen_category_hub(cat, compounds, stacks))

    for c in compounds:
        wp(c['url'], gen_compound_page(c, compounds, stacks))

    wp('/stacks/', gen_stacks_root(stacks))
    for s in stacks:
        wp(s['url'], gen_stack_page(s, compounds))

    for s in supplies:
        wp(s['url'], gen_supply_page(s))

    wp('/research/', gen_research_hub())
    wp('/tools/reconstitution-calculator/', gen_reconstitution_calculator())
    wp('/about/', gen_about_index())
    wp('/contact/', gen_contact())
    wp('/shipping/', gen_shipping())
    wp('/faq/', gen_faq())

    wp('/legal/research-use-policy/', gen_legal_research_use())
    wp('/legal/mhra-statement/', gen_legal_mhra())
    wp('/legal/terms/', gen_legal_terms())
    wp('/legal/privacy/', gen_legal_privacy())
    wp('/legal/cookies/', gen_legal_cookies())
    wp('/legal/refunds/', gen_legal_refunds())

    wp('/cart/', gen_cart())
    wp('/checkout/shipping/', gen_checkout_shipping())
    wp('/checkout/payment/', gen_checkout_payment())
    wp('/checkout/confirmation/', gen_checkout_confirmation())

    # ── Assets ────────────────────────────────────────────────────────────────
    print('\nCopying assets...')
    src_assets = os.path.join(SRC_DIR, 'assets')
    dst_assets = os.path.join(OUTPUT_DIR, 'assets')
    shutil.copytree(src_assets, dst_assets)
    # Remove build-time temp file from output
    tmp = os.path.join(dst_assets, '_extensions.css')
    if os.path.exists(tmp):
        os.remove(tmp)
    print('  assets/ copied')

    # ── favicon.svg ───────────────────────────────────────────────────────────
    favicon_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="8" fill="#030407"/>'
        '<circle cx="16" cy="16" r="10" fill="none" stroke="#01D3A0" stroke-width="2.5"/>'
        '<text x="16" y="21" text-anchor="middle" font-family="Space Grotesk,sans-serif"'
        ' font-weight="700" font-size="12" fill="#01D3A0">V</text>'
        '</svg>'
    )
    with open(os.path.join(OUTPUT_DIR, 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(favicon_svg)

    # ── sitemap.xml ───────────────────────────────────────────────────────────
    sitemap_paths = [p for p in pages if not p.startswith(('/cart', '/checkout'))]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in sitemap_paths:
        sitemap += f'  <url><loc>{SITE_URL}{p}</loc></url>\n'
    sitemap += '</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)

    # ── robots.txt ────────────────────────────────────────────────────────────
    robots = (
        'User-agent: *\n'
        'Disallow: /cart/\n'
        'Disallow: /checkout/\n'
        'Disallow: /coa/\n'
        'Disallow: /admin/\n'
        f'Sitemap: {SITE_URL}/sitemap.xml\n'
    )
    with open(os.path.join(OUTPUT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots)

    # ── vercel.json ───────────────────────────────────────────────────────────
    vercel_cfg = {
        "trailingSlash": True,
        "cleanUrls": True,
        "redirects": [
            {"source": "/shop", "destination": "/compounds/", "permanent": True},
            {"source": "/shop/(.*)", "destination": "/compounds/$1", "permanent": True},
            {"source": "/product/(.*)", "destination": "/compounds/$1", "permanent": True},
            {"source": "/products/(.*)", "destination": "/compounds/$1", "permanent": True},
        ],
        "headers": [
            {
                "source": "/assets/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ]
            }
        ]
    }
    with open(os.path.join(ROOT_DIR, 'vercel.json'), 'w', encoding='utf-8') as f:
        json.dump(vercel_cfg, f, indent=2)

    # ── site.webmanifest ──────────────────────────────────────────────────────
    manifest = {
        "name": SITE_NAME,
        "short_name": "Velox",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#030407",
        "theme_color": "#01D3A0",
        "icons": [
            {"src": "/assets/images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ]
    }
    with open(os.path.join(OUTPUT_DIR, 'site.webmanifest'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f'\nDone. {len(pages)} pages written to {OUTPUT_DIR}')
    print(f'       sitemap.xml ({len(sitemap_paths)} URLs), robots.txt, vercel.json, site.webmanifest, favicon.svg')


if __name__ == '__main__':
    main()
