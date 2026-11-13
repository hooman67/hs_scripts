#!/usr/bin/env python3
"""Build the static, IMS-authenticated KDP generation comparison gallery."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"


def card(kind, src, title, note):
    return (f'<figure class="{kind}"><a href="{escape(src)}"><img src="{escape(src)}" '
            f'loading="lazy" alt="{escape(title)}"></a><figcaption><b>{escape(title)}</b>'
            f'<span>{escape(note)}</span></figcaption></figure>')


def grid(cards, cols="three"):
    return f'<div class="grid {cols}">' + "".join(cards) + "</div>"


def prompt(stem, label):
    body = (PROMPTS / f"{stem}.txt").read_text().strip()
    return f'<details><summary>Full prompt · {escape(label)}</summary><pre>{escape(body)}</pre></details>'


def outputs(rows):
    cards = [card("generated", f"../outputs/{name}", title, note) for name, _, title, note in rows]
    return '<h3>Generated outputs</h3>' + grid(cards) + "".join(prompt(stem, title) for _, stem, title, _ in rows)


KEXP = [
    ("k_express_lifestyle_sunburst_high_v1.png", "k_express_lifestyle", "Generated 1 · kitchen morning", "Two clean exact-SKU inputs · no human"),
    ("k_express_human_press_sunburst_high_v2.png", "k_express_human_press", "Generated 2 · first button-press attempt", "User-flagged: hand looks AI-generated; retained as a failure-analysis example"),
    ("k_express_window_breakfast_sunburst_high_v3.png", "k_express_window_breakfast", "Generated 3 · apartment breakfast", "Two clean exact-SKU inputs · wider scene"),
    ("k_express_precise_press_sunburst_high_v4.png", "k_express_precise_press", "Generated 4 · relaxed button press", "New anatomy/contact variation · visually stronger hand"),
    ("k_express_place_mug_sunburst_high_v5.png", "k_express_place_mug", "Generated 5 · placing mug", "New interaction type · strongest hand/contact result in this batch"),
    ("k_express_close_handle_sunburst_high_v6.png", "k_express_close_handle", "Generated 6 · top-close gesture", "Plausible hand pose; exact handle mechanism remains unverified"),
    ("k_express_wide_candid_sunburst_high_v7.png", "k_express_wide_candid", "Generated 7 · wider candid scene", "Human-present environmental variation"),
]

MINI_WARM = [
    ("mini_mate_human_press_sunburst_high_v1.png", "mini_mate_human_press", "Generated 1 · button press", "One clean Warm Stone input · interaction stress case"),
    ("mini_mate_small_space_sunburst_high_v2.png", "mini_mate_small_space", "Generated 2 · small-space kitchen", "One clean Warm Stone input · no human"),
    ("mini_mate_warm_stone_red_pink_studio_sunburst_high_v1.png", "mini_mate_warm_stone_red_pink_studio", "Generated 3 · red/pink studio", "Text-only scene match · no lifestyle image supplied"),
    ("mini_mate_warm_stone_human_place_mug_sunburst_high_v1.png", "mini_mate_warm_stone_human_place_mug", "Generated 4 · placing mug", "One clean Warm Stone input · convincing grip/contact"),
    ("mini_mate_warm_stone_cool_evening_sunburst_high_v1.png", "mini_mate_warm_stone_cool_evening", "Generated 5 · cool evening", "Distinct environment; unwanted coffee stream is a visible prompt-compliance miss"),
]

MINI_BLACK = [
    ("mini_mate_matte_black_botanical_sunroom_sunburst_high_v1.png", "mini_mate_matte_black_botanical_sunroom", "Generated 6 · botanical sunroom", "Only the genuine clean Matte Black reference was supplied"),
    ("mini_mate_matte_black_lavender_pop_studio_sunburst_high_v2.png", "mini_mate_matte_black_lavender_pop_studio", "Generated 7 · lavender pop studio", "Text-only composition match · no lifestyle image supplied"),
    ("mini_mate_matte_black_yellow_blue_tabletop_sunburst_high_v3.png", "mini_mate_matte_black_yellow_blue_tabletop", "Generated 8 · yellow/cobalt tabletop", "Text-only composition match · no lifestyle image supplied"),
    ("mini_mate_matte_black_lavender_human_place_mug_sunburst_high_v4.png", "mini_mate_matte_black_lavender_human_place_mug", "Generated 9 · lavender mug placement", "Genuine clean black reference only · natural hand/contact variation"),
    ("mini_mate_matte_black_yellow_blue_human_press_sunburst_high_v5.png", "mini_mate_matte_black_yellow_blue_human_press", "Generated 10 · yellow/cobalt button press", "Genuine clean black reference only · fingertip contacts existing top control"),
]

KSUP = [
    ("k_supreme_gen2_kitchen_sunburst_high_v1.png", "k_supreme_gen2_kitchen", "Generated 1 · residential kitchen", "Two clean exact-SKU inputs · no human"),
    ("k_supreme_gen2_red_pink_seamless_sunburst_high_v2.png", "k_supreme_gen2_red_pink_seamless", "Generated 2 · red/pink seamless studio", "Text-only scene match · no lifestyle image supplied"),
    ("k_supreme_gen2_red_pink_editorial_sunburst_high_v3.png", "k_supreme_gen2_red_pink_editorial", "Generated 3 · red/pink editorial set", "Second text-only scene match · no lifestyle image supplied"),
    ("k_supreme_gen2_human_press_sunburst_high_v4.png", "k_supreme_gen2_human_press", "Generated 4 · human button press", "Natural contact; exact blue-ring control layout needs C-Tech review"),
    ("k_supreme_gen2_cool_office_sunburst_high_v5.png", "k_supreme_gen2_cool_office", "Generated 5 · cool office", "Materially different environment and lighting"),
]

ke_refs = [
    card("input", "../../../3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_5000358267.jpg", "Input 1 · exact-SKU identity reference", "Frontal product view with blue mug"),
    card("input", "../../../3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_en_general.jpg", "Input 2 · exact-SKU identity reference", "Three-quarter product view with reservoir and controls"),
]
ke_real = [
    card("real", "../../../3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/life_H__K-Express_Alt_7.jpg", "Real comparison 1 · exact-SKU", "Official kitchen composition; held out from generation"),
    card("real", "../../../3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/life_H__K-Express_Alt_8.jpg", "Real comparison 2 · exact-SKU", "Official kitchen composition; held out from generation"),
]

warm_ref = card("input", "../../../3_pairs/Keurig-Mini-Mate-Plus__Warm_Stone/ref__Keurig-Mini-Mate-Plus_5000390177.jpg", "Input · Warm Stone exact-SKU identity reference", "Used for all five Warm Stone lifestyle generations")
black_ref = card("input", "../../../3_pairs/Keurig-Mini-Mate-Plus__Matte_Black/ref__Keurig-Mini-Mate-Plus_en_general.jpg", "Input · genuine Matte Black exact-SKU reference", "Real clean reference for SKU 5000390176; used for all five Matte Black generations")
warm_real = card("real", "../../../3_pairs/Keurig-Mini-Mate-Plus__Warm_Stone/life_H__3000x3000_warm_stone_library.jpg", "Real comparison · Warm Stone exact-SKU", "Official human-present scene; held out from generation")
mini_proxy = card("proxy", "../../../3_pairs/Keurig-Mini-Mate-Plus__Warm_Stone/life_A__drinklineup-mbplus.jpg", "Real comparison · cross-color proxy", "Black product-family composition; not exact Warm Stone ground truth")
black_inspired_1 = card("inspired", "../../../3_pairs/Keurig-Mini-Mate-Plus__Matte_Black/life_H__matteblack-afterhero.jpg", "Real comparison 1 · Matte Black prompt inspiration", "Observed to describe the lavender composition; pixels were not supplied to any displayed generation")
black_inspired_2 = card("inspired", "../../../3_pairs/Keurig-Mini-Mate-Plus__Matte_Black/life_H__matteblackpoolside.jpg", "Real comparison 2 · Matte Black prompt inspiration", "Observed to describe the yellow/cobalt composition; pixels were not supplied to any displayed generation")

ks_refs = [
    card("input", "../../../focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/00_Keurig-K-Supreme-Gen2_5000393168.jpg", "Input 1 · exact-SKU identity reference", "Frontal hot-beverage packshot"),
    card("input", "../../../focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/01_Keurig-K-Supreme-Gen2_5000393168_alt1.jpg", "Input 2 · exact-SKU identity reference", "Frontal packshot with hot and iced beverage context"),
]
ks_real = [
    card("inspired", "../../../focus_skus/02_K-Supreme-Gen2_Black_5000393168/lifestyle_studio/10_Hero_Silo_or_Lifestyle.jpg", "Real comparison 1 · prompt inspiration", "Observed to describe the red/pink scene; pixels were not supplied to the model"),
    card("inspired", "../../../focus_skus/02_K-Supreme-Gen2_Black_5000393168/lifestyle_studio/11_Hero_Silo_or_Lifestyle_3.jpg", "Real comparison 2 · prompt inspiration", "Observed to describe the red/pink scene; product is absent"),
    card("inspired", "../../../focus_skus/02_K-Supreme-Gen2_Black_5000393168/lifestyle_studio/13_Hero_Silo_or_Lifestyle_5.jpg", "Real comparison 3 · prompt inspiration", "Observed to describe the red/pink scene; pixels were not supplied to the model"),
]

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KDP GPT Image 2.5 Sunburst POC comparison</title><link rel="stylesheet" href="./style.css"></head><body>
<div id="ims"></div><div id="loading" class="loading-screen">Loading…</div><div id="content" class="hidden"><main>
<header><p class="eyebrow">FOUNDRY 4.0 · KDP ENGINEERING VALIDATION · 2026-10-07</p><h1>Keurig lifestyle generation POC</h1><p class="sub">GPT Image 2.5 Sunburst · image edits · quality high · 22 landscape lifestyle generations</p><div class="stats"><span>3 product families</span><span>22 generated assets</span><span>8 exact-SKU real lifestyle comparisons</span><span>All displayed generations use clean product references only</span></div></header>
<section class="notice"><strong>How to read this page</strong><p>Blue = clean product input. Green = generated lifestyle. Purple = real held-out comparison. Pink = real image observed only to write a text scene prompt. Yellow = cross-color proxy. Every generation includes its full prompt.</p></section>
<nav class="jump"><a href="#k-express">K-Express Black</a><a href="#mini-mate">Mini Mate Plus</a><a href="#k-supreme">K-Supreme Gen 2 Black</a><a href="#method">Method</a></nav>
<section class="sku" id="k-express"><div class="sku-head"><div><p class="eyebrow">HUMAN-INTERACTION EXPANSION</p><h2>K-Express Black</h2><p>SKU 5000358267 · multiple interaction types retained for failure analysis and selection</p></div><span class="badge">7 generations</span></div><h3>Clean model inputs</h3>{grid(ke_refs, "two")}{outputs(KEXP)}<h3>Real scraped lifestyle comparisons</h3>{grid(ke_real, "two")}</section>
<section class="sku" id="mini-mate"><div class="sku-head"><div><p class="eyebrow">ENVIRONMENT AND INTERACTION EXPANSION</p><h2>Mini Mate Plus · Warm Stone and Matte Black</h2><p>Warm Stone SKU 5000390177 · Matte Black SKU 5000390176</p></div><span class="badge">10 generations</span></div><h3>Clean Warm Stone model input</h3>{grid([warm_ref], "one")}{outputs(MINI_WARM)}<h3>Warm Stone real comparisons</h3>{grid([warm_real, mini_proxy], "two")}<h3>Clean Matte Black model input</h3>{grid([black_ref], "one")}{outputs(MINI_BLACK)}<h3>Matte Black real lifestyle comparisons · prompt inspiration only</h3><p class="section-note">These exact-SKU images were observed when writing the lavender and yellow/cobalt prompts. Their pixels were never sent to any displayed generation, but they are not pristine holdouts for the scene-match outputs.</p>{grid([black_inspired_1, black_inspired_2], "two")}</section>
<section class="sku" id="k-supreme"><div class="sku-head"><div><p class="eyebrow">TICKET SKU · RED/PINK SCENE MATCH</p><h2>K-Supreme Gen 2 Black</h2><p>SKU 5000393168 · two clean references · two text-only red/pink scene matches</p></div><span class="badge">5 generations</span></div><h3>Clean model inputs</h3>{grid(ks_refs, "two")}{outputs(KSUP)}<h3>Real scraped studio comparisons · prompt inspiration only</h3><p class="section-note">These images were observed when writing the red/pink prompts. Their pixels were never sent to the model, but they are not pristine holdouts for the scene-match outputs.</p>{grid(ks_real)}</section>
<section class="method" id="method"><h2>Method and limits</h2><ul><li>Every displayed generation used only clean product identity references. No scraped lifestyle pixels were supplied to these runs.</li><li>Red/pink K-Supreme and lavender/yellow Matte Black outputs are text-prompt scene matches. The real images informed the prompts, so they are not pristine blind-test holdouts for those scenes.</li><li>Visual review supports realism and high-level identity. Exact controls, labels, geometry, contact, and SKU correctness remain for C-Tech review.</li><li>This is a purposive internal engineering set, not a blinded evaluation or production-rights determination.</li></ul></section>
</main></div><script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script><script src="./imsauth.js"></script><script src="./data.js"></script><script src="./main.js"></script><script>document.addEventListener("DOMContentLoaded",()=>initializeIMS());</script></body></html>'''

(ROOT / "gallery" / "index.html").write_text(html)
print(ROOT / "gallery" / "index.html")
