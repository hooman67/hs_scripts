#!/usr/bin/env python3
"""Build the local KDP candidate-SKU review gallery.

The gallery deliberately shows accepted and rejected assets together so that
folder labels are never mistaken for visually verified image roles.
"""

from __future__ import annotations

import html
import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "research" / "dataset" / "data"
OUTPUT = ROOT / "research" / "dataset" / "artifacts" / "candidate_gallery.html"
S3_ROOT = "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website"


@dataclass(frozen=True)
class Product:
    name: str
    sku: str
    verdict: str
    rationale: str
    folder: Path
    s3_prefix: str
    labels: dict[str, tuple[str, str]]


def _pair(
    name: str,
    sku: str,
    verdict: str,
    rationale: str,
    folder_name: str,
    labels: dict[str, tuple[str, str]],
) -> Product:
    return Product(
        name,
        sku,
        verdict,
        rationale,
        DATA / "pairs" / folder_name,
        f"{S3_ROOT}/3_pairs/{folder_name}/",
        labels,
    )


def _focus(
    name: str,
    sku: str,
    verdict: str,
    rationale: str,
    folder_name: str,
    labels: dict[str, tuple[str, str]],
) -> Product:
    return Product(
        name,
        sku,
        verdict,
        rationale,
        DATA / "focus_skus" / folder_name,
        f"{S3_ROOT}/focus_skus/{folder_name}/",
        labels,
    )


PRODUCTS = [
    _pair(
        "K-Express Single Serve — Black",
        "5000358267",
        "PRIMARY POC CANDIDATE",
        "Two genuine exact-SKU kitchen/studio lifestyle baselines and two usable clean product references. "
        "Simple silhouette makes this a strong first fidelity test; no delivered human-interaction baseline.",
        "K-Express-Single-Serve-Coffee-Maker__Black",
        {
            "life_H__K-Express_Alt_7.jpg": ("verified-life", "Genuine exact-SKU lifestyle; no overlay"),
            "life_H__K-Express_Alt_8.jpg": ("verified-life", "Genuine exact-SKU kitchen lifestyle; cup under spout"),
            "life_H__K-Express_Alt_2.jpg": ("exclude", "Feature/infographic with text; not a blind-test real"),
            "ref__K-Express-Single-Serve-Coffee-Maker_en_general.jpg": ("verified-ref", "Clean three-quarter reference"),
            "ref__K-Express-Single-Serve-Coffee-Maker_5000358267.jpg": ("verified-ref", "Clean frontal reference"),
            "ref__K-Express_Alt_4.jpg": ("exclude", "Feature callout with text; supplemental only"),
        },
    ),
    _pair(
        "Keurig Mini Mate Plus — Warm Stone",
        "5000390177",
        "PRIMARY HUMAN-INTERACTION CANDIDATE",
        "One clean exact-SKU reference and one strong official human-interaction lifestyle image. "
        "The colorful lineup is multi-variant and can inform style but is not an exact-SKU blind baseline.",
        "Keurig-Mini-Mate-Plus__Warm_Stone",
        {
            "ref__Keurig-Mini-Mate-Plus_5000390177.jpg": ("verified-ref", "Clean exact-SKU reference"),
            "life_H__3000x3000_warm_stone_library.jpg": ("verified-life", "Official exact-SKU human-interaction lifestyle"),
            "life_A__drinklineup-mbplus.jpg": ("proxy", "Official multi-color lineup; variant-ambiguous proxy"),
            "life_H__Alt3_Warm_Stone.jpg": ("exclude", "Feature callout with text"),
            "life_H__Alt4_Warm_Stone.jpg": ("exclude", "Feature callout with text"),
        },
    ),
    _pair(
        "K-2550 Plumbed — Default",
        "5000380341",
        "SECONDARY INTERACTION STRESS TEST",
        "Two references and four contextual office/product-in-use images, including hand interaction. "
        "Useful for interaction testing but a commercial brewer, so less aligned to the consumer ticket goal.",
        "Keurig-K-2550-Plumbed-Coffee-Maker__Default",
        {
            "ref__Keurig-K-2550-Plumbed-Coffee-Maker_en_general.jpg": ("verified-ref", "Clean exact-product reference"),
            "ref__2025_K2550_BOI_Alt_1-Plumbed.jpg": ("exclude", "Packshot with promotional badge"),
            "life_H__kq7zxviszrcagx7buyfd.jpg": ("verified-life", "Contextual product-in-use baseline"),
            "life_H__lwxbjkds7ro8ekceonbv.jpg": ("verified-life", "Office/product station baseline"),
            "life_H__rf3qs9jnarnbvqh95yfb_1.jpg": ("verified-life", "Human interaction baseline"),
            "life_H__svysauan8d81gkwvvdjk.jpg": ("verified-life", "Human/button interaction baseline"),
            "life_H__2025_K2550_BOI_Alt_Images_Alt_4-Plumbed.jpg": ("exclude", "Promotional feature composite"),
            "life_H__2025_K2550_BOI_Alt_Images_Alt_7-Pourover.jpg": ("exclude", "Text/composite and mixed product scope"),
        },
    ),
    _focus(
        "K-Supreme Gen 2 — Black",
        "5000393168",
        "TICKET SKU — GENERATION CANDIDATE",
        "Two clean exact-SKU references and three exact-SKU studio lifestyle compositions. "
        "Good for product/style validation; weak real-world and human-interaction baselines.",
        "02_K-Supreme-Gen2_Black_5000393168",
        {
            "reference/00_Keurig-K-Supreme-Gen2_5000393168.jpg": ("verified-ref", "Clean exact-SKU reference"),
            "reference/01_Keurig-K-Supreme-Gen2_5000393168_alt1.jpg": ("verified-ref", "Clean exact-SKU alternate reference"),
            "lifestyle_studio/10_Hero_Silo_or_Lifestyle.jpg": ("verified-life", "Exact-SKU studio lifestyle"),
            "lifestyle_studio/11_Hero_Silo_or_Lifestyle_3.jpg": ("verified-life", "Shared black/gray studio composition"),
            "lifestyle_studio/13_Hero_Silo_or_Lifestyle_5.jpg": ("verified-life", "Exact-SKU studio lifestyle with cup"),
            "lifestyle_no_brewer/12_Hero_Silo_or_Lifestyle_4.jpg": ("exclude", "Human shown but brewer absent"),
        },
    ),
    _focus(
        "K-Duo Gen 2 — Moonlight Gray",
        "5000396548",
        "TICKET SKU — HARD FIDELITY STRESS TEST",
        "One clean exact-SKU product reference plus supplemental callout views. There is no genuine public "
        "exact-color lifestyle image or video in the scrape. Its dual brewer/carafe geometry makes it the harder test.",
        "01_K-Duo-Gen2_MoonlightGray_5000396548",
        {
            "reference/00_K-Duo-hot-and-iced-Single-Serve-Carafe-Coffee-Maker-Gen2_5000396548.jpg": (
                "verified-ref",
                "Clean exact-SKU hero reference",
            ),
            "reference/03_K-Duo-hot-and-iced-Single-Serve-Carafe-Coffee-Maker-Gen2_5000378536_alt3.jpg": (
                "proxy",
                "Exact-color product view with feature callout",
            ),
            "reference/04_K-Duo-hot-and-iced-Single-Serve-Carafe-Coffee-Maker-Gen2_5000378536_alt4.jpg": (
                "proxy",
                "Exact-color product view with feature callout",
            ),
        },
    ),
    _pair(
        "K-Slim Single Serve — White",
        "5000388718",
        "ALTERNATE — NOT FIRST CHOICE",
        "Three references but only one genuine contextual lifestyle image; two pair-labeled lifestyle files are infographics.",
        "K-Slim-Single-Serve-Coffee-Maker__White",
        {
            "life_H__k-slim-alt2-white.jpg": ("verified-life", "Genuine exact-SKU kitchen lifestyle"),
            "life_H__12656_K-Slim_MultiStream_Toolkit_Lite_Assets_Retailer_Multistream_Technology_Whi.jpg": (
                "exclude",
                "Infographic",
            ),
            "life_H__K-Slim-Single-Serve-Coffee-Maker_white_alt_2.jpg": ("exclude", "Feature image with text"),
        },
    ),
    _pair(
        "K-Cafe Barista Bar — Black",
        "5000389310",
        "REJECT AS REAL-LIFESTYLE BASELINE",
        "Three usable product references, but both pair-labeled lifestyle files are feature infographics rather than scenes.",
        "K-Cafe-Barista-Bar__Black",
        {
            "life_H__K-Cafe-Barista-Bar_5000374606_alt_13.jpg": ("exclude", "Infographic"),
            "life_H__K-Cafe-Barista-Bar_5000374606_alt_6.jpg": ("exclude", "Feature close-up with text"),
        },
    ),
]


def _image_files(folder: Path) -> list[Path]:
    return sorted(p for p in folder.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})


def build() -> None:
    cards: list[str] = []
    for product in PRODUCTS:
        images: list[str] = []
        for path in _image_files(product.folder):
            rel_key = path.relative_to(product.folder).as_posix()
            status, note = product.labels.get(rel_key, ("exclude", "Not manually accepted for POC input/baseline"))
            rel_src = Path(os.path.relpath(path, OUTPUT.parent)).as_posix()
            s3_uri = product.s3_prefix + rel_key
            images.append(
                f"""
                <figure class="asset {status}">
                  <a href="{html.escape(rel_src)}" target="_blank"><img loading="lazy" src="{html.escape(rel_src)}"></a>
                  <figcaption>
                    <span class="pill">{html.escape(status)}</span>
                    <strong>{html.escape(note)}</strong>
                    <code>{html.escape(rel_key)}</code>
                    <code>{html.escape(s3_uri)}</code>
                  </figcaption>
                </figure>
                """
            )
        cards.append(
            f"""
            <section class="product">
              <header><div><h2>{html.escape(product.name)}</h2><p>SKU {html.escape(product.sku)}</p></div>
              <span class="verdict">{html.escape(product.verdict)}</span></header>
              <p class="rationale">{html.escape(product.rationale)}</p>
              <div class="grid">{''.join(images)}</div>
            </section>
            """
        )

    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KDP candidate SKU review</title>
<style>
:root{{--bg:#101216;--panel:#1a1e24;--line:#343b45;--text:#edf1f6;--muted:#aab4c0;--blue:#75c6ff}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 system-ui,sans-serif}}
main{{max-width:1800px;margin:auto;padding:28px}} h1{{margin:0 0 8px;font-size:32px}} h2{{margin:0;font-size:23px}}
.intro,.rationale{{color:var(--muted);max-width:1100px}} .legend{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 28px}}
.legend span,.pill,.verdict{{border:1px solid var(--line);border-radius:999px;padding:4px 9px;font-size:12px;font-weight:700}}
.product{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;margin:0 0 26px}}
.product header{{display:flex;justify-content:space-between;gap:18px;align-items:start}} .product header p{{margin:4px 0;color:var(--muted)}}
.verdict{{color:#ffd27b;border-color:#8d6d35}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
.asset{{margin:0;border:2px solid var(--line);background:#111419;border-radius:10px;overflow:hidden}} .asset img{{width:100%;height:260px;object-fit:contain;background:#fff;display:block}}
.asset figcaption{{padding:11px;display:grid;gap:7px}} .asset strong{{font-size:13px}} code{{display:block;color:#a9b6c5;font-size:10px;overflow-wrap:anywhere}}
.verified-ref{{border-color:#4fa7ff}} .verified-life{{border-color:#51cc88}} .proxy{{border-color:#d4a34c}} .exclude{{border-color:#6b7078;opacity:.72}}
.verified-ref .pill{{color:#75c6ff}} .verified-life .pill{{color:#75e7a5}} .proxy .pill{{color:#ffd27b}} .exclude .pill{{color:#aab0b8}}
</style></head><body><main>
<h1>KDP scraped-data candidate review</h1>
<p class="intro">As of 2026-10-07. Visual verification layer for the KDP lifestyle-hero POC. Pair/folder labels are discovery metadata; the colored review label below is the manually checked role. Click any image for its full local resolution.</p>
<div class="legend"><span style="color:#75c6ff">verified-ref</span><span style="color:#75e7a5">verified-life</span><span style="color:#ffd27b">proxy</span><span>exclude</span></div>
{''.join(cards)}
</main></body></html>"""
    OUTPUT.write_text(document, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    build()
