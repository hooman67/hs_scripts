from __future__ import annotations

import collections
import csv
import hashlib
import html
import itertools
import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

import analyze
import device_stats as devices

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "single-page"
PREFIX = "analysis/hp-lifestyle-statistics-all-devices-20261106"
CDN = f"https://foundry-aws-corp.adobe.io/asset/{analyze.BUCKET}/{PREFIX}"
BASE = "Original no-person parquet"
ADDED = "Added original printer references (people visible)"
FIELDS = (
    "scene", "type_open_set", "type_closed_set", "lighting_open_set",
    "lighting_closed_set", "background", "composition", "camera", "entities",
)

# These are printer-specific relationships, not the focal laptop/monitor's support.
BASE_PRINTERS = {
    57: ("Secondary / background", "Desk / worktable", ["Not established"], "Printer on right side of the blue desk."),
    161: ("Secondary / background", "Not established", ["Not established"], "Printer in blurred background; its supporting furniture is not established."),
    174: ("Primary / foreground", "Desk / worktable", ["Wood"], "Black printer on light wooden desk."),
    281: ("Secondary / background", "Crate", ["Plastic"], "Black printer on a black plastic crate in the background."),
    364: ("Primary / foreground", "Desk / worktable", ["Wood"], "White-and-blue printer on light wood desk."),
    365: ("Secondary / background", "Cabinet / console", ["Not established"], "Background printer on cabinet against brick wall."),
    366: ("Primary / foreground", "Shelf / storage unit", ["Not established"], "Printer on white shelving unit; toner boxes below."),
    367: ("Primary / foreground", "Cabinet / console", ["Not established"], "White-and-grey printer on white cabinet."),
    368: ("Primary / foreground", "Cabinet / console", ["Not established"], "Ink-tank printer on light grey cabinet with black legs."),
    370: ("Primary / foreground", "Cabinet / console", ["Not established"], "Ink-tank printer on light grey cabinet."),
    371: ("Primary / foreground", "Cabinet / console", ["Not established"], "Open inkjet/scanner on white cabinet."),
    433: ("Primary / foreground", "Cabinet / console", ["Wood"], "Printer on light wood cabinet with glass doors."),
    442: ("Primary / foreground", "Desk / worktable", ["Wood"], "White-and-mint printer on light wood desk."),
    447: ("Secondary / background", "Desk / worktable", ["Not established"], "Black printer on secondary desk in background left."),
}

PRIMARY_SUPPORTS = {
    "style_261": ("Table", ["Wood"], "Printer on broad wooden worktable."),
    "style_279": ("Cabinet", ["Wood"], "Printer on wooden cabinet beneath window."),
    "style_281": ("Cabinet", ["Wood"], "Printer on wooden console."),
    "style_282": ("Desk", ["Wood"], "Printer on wooden desk."),
    "style_296": ("Desk", ["Not established"], "Printer on light-colored desk; material not established."),
    "style_297": ("Handheld (person)", ["Not established"], "Focal laptop held by standing person; printer separately on desk."),
    "style_298": ("Desk", ["Not established"], "Focal monitor/workstation on white desk; printer support not visible."),
    "style_299": ("Desk", ["Not established"], "Focal workstation and printer on shared desktop."),
    "style_302": ("Desk", ["Not established"], "Focal laptop on shared desktop."),
    "style_337": ("Integrated machine structure", ["Metal"], "Integrated metal gantry and workbed; full chassis not visible."),
    "style_342": ("Table", ["Wood"], "Focal laptop on wood table; printer on separate console."),
}

INVENTORY_ADDITIONS = {
    "style_261": {"Printed papers / documents": ["printed activity sheets"], "Pens / stationery": ["child holding drawing pen"]},
    "style_279": {"Printed papers / documents": ["printed activity sheets"]},
    "style_281": {"Artwork / picture / poster": ["photo collage", "photo display stand"]},
    "style_282": {"Artwork / picture / poster": ["photo collage and hanging ornaments", "photo prints"], "Printed papers / documents": ["photo prints"]},
    "style_296": {},
    "style_297": {},
    "style_298": {},
    "style_299": {"Water bottle": ["desk lamp and water bottle"]},
    "style_302": {"Water bottle": ["headphones and travel bottle"]},
    "style_337": {"Printer": ["industrial flatbed printing equipment"], "Printed substrate / workpiece": ["patterned sheet"], "Tools / industrial equipment": ["metal gantry", "industrial flatbed printing equipment"]},
    "style_342": {},
}


def load():
    source = json.loads((ROOT / "source.json").read_text())
    baseline = json.loads((ROOT / "output/rows.json").read_text())
    references = json.loads((ROOT / "printer-reconciliation.json").read_text())
    captions = json.loads((ROOT / "additional-printers/visual_captions.json").read_text())
    missing = {r["reference"]: r for r in references if not r["existing_match"]}
    assert len(source) == len(baseline) == 458
    assert len(references) == 15 and len(missing) == len(captions) == 11
    assert {c["reference"] for c in captions} == set(missing)
    rows = []
    raw_rows = []
    caption_export = []
    for raw, reviewed in zip(source, baseline):
        assert json.loads(raw["target_caption"]) == reviewed["scap"]
        row = dict(reviewed, cohort=BASE, caption_provenance="Existing Qwen SCAP in source parquet")
        if row["source_row"] in BASE_PRINTERS:
            role, support, materials, evidence = BASE_PRINTERS[row["source_row"]]
            row["printer_observation"] = {
                "role": role, "kind": "Desktop printer", "support": support,
                "materials": materials, "support_evidence": evidence,
                "front_orientation": "Not independently coded",
                "paper_access": "Not independently coded",
                "uncertainty": "Caption-derived evidence; not a fresh visual caption.",
            }
        rows.append(row)
        raw_rows.append(dict(raw, cohort=BASE, caption_provenance=row["caption_provenance"]))
    for offset, caption in enumerate(captions):
        ref = missing[caption["reference"]]
        scap = caption["scap"]
        assert set(scap) == set(FIELDS) and caption["human_presence"] is True
        raw = dict(ref["source_match"])
        raw.update(
            target_caption=json.dumps(scap, ensure_ascii=False),
            caption=json.dumps(scap, ensure_ascii=False),
            image_type="real", cohort=ADDED,
            caption_provenance="Fresh assistant visual inspection of original photograph",
        )
        row = analyze.extract(raw, 458 + offset)
        support, materials, evidence = PRIMARY_SUPPORTS[caption["reference"]]
        row.update(
            product_category=caption["primary_category"],
            environment=caption["environment"], environment_basis="Assistant visual inspection",
            cohort=ADDED, caption_provenance=raw["caption_provenance"],
            reference=caption["reference"], printer_observation=caption["printer_observation"],
            human_claims=["Physical person/people visible in original reference photograph."],
            depicted_humans=[],
            flags=["Original reference contains people; not a no-person image."],
            support={
                "immediate": support, "underlying": analyze.UNKNOWN,
                "evidence": evidence, "basis": "Assistant visual inspection",
                "materials": materials, "all_support_materials": materials,
            },
        )
        for family, labels in INVENTORY_ADDITIONS[caption["reference"]].items():
            row["objects"].setdefault(family, []).extend(labels)
        if "Printer" not in row["device_presence"]:
            row["device_presence"].append("Printer")
        rows.append(row)
        raw_rows.append(raw)
        caption_export.append(dict(
            caption, image_hash=ref["identity"], target_image=raw["target_image"],
            original_product_name=raw.get("product_name"),
            cohort=ADDED, caption_provenance=raw["caption_provenance"],
        ))
    assert len(rows) == 469
    assert len({r["image_hash"].removesuffix("_no_humans") for r in rows}) == 469
    assert sum("printer_observation" in r for r in rows) == 25
    assert {r["source_row"] for r in baseline if "Printer" in r["objects"]} == set(BASE_PRINTERS)
    for r in rows:
        assert ("Printer" in r["objects"]) == ("printer_observation" in r)
    devices.annotate(rows)
    return rows, raw_rows, caption_export


def stats(rows):
    n = len(rows)
    counts = analyze.prevalence([list(r["objects"]) for r in rows], n)
    global_objects = {e["value"]: e["n"] / n for e in counts}
    groups = []
    definitions = analyze.groupings(rows)
    family_lookup = {}
    environment_definitions = []
    for family in devices.FAMILIES:
        members = [r for r in rows if family in r["device_observations"]]
        if not members:
            continue
        name = f"{family} / all environments"
        definitions.append(("Device presence", name, members))
        family_lookup[("Device presence", name)] = family
        for env in sorted({r["environment"] for r in members}):
            name = f"{family} present / {env}"
            environment_definitions.append(("Device presence x environment", name,
                                            [r for r in members if r["environment"] == env]))
            family_lookup[("Device presence x environment", name)] = family
    definitions.extend(environment_definitions)
    for i, (kind, name, members) in enumerate(definitions):
        if kind == "All rows":
            name = f"All {n} analyzed images"
        group = analyze.group_stats(members, global_objects)
        if (kind, name) in family_lookup:
            family = family_lookup[(kind, name)]
            group.update(devices.group_counts(members, family), device_family=family)
        group.update(
            id=f"profile-{i}", kind=kind, name=name,
            dataset_pct=round(100 * len(members) / n, 2),
            cohorts=analyze.scalar_counts(members, "cohort"),
            fields=analyze.field_patterns(members),
        )
        for info in group["fields"].values():
            info.pop("examples")
        groups.append(group)
    return groups


def esc(value):
    return html.escape(str(value), quote=True)


def counted(entries):
    return "<br>".join(
        f'{esc(e["value"])}: <b>{e["n"]}/{e["denominator"]}</b> ({e["pct"]:.1f}%)'
        for e in entries
    ) or '<span class="muted">No normalized match / no repeated phrase.</span>'


def table(headers, rows, caption=None):
    head = "".join(f"<th scope='col'>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    title = f"<caption>{esc(caption)}</caption>" if caption else ""
    return f"<div class='table-wrap'><table>{title}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def comparisons(rows, getter, label, predicate=lambda r: True):
    cohorts = ([r for r in rows if r["cohort"] == BASE and predicate(r)],
               [r for r in rows if r["cohort"] == ADDED and predicate(r)],
               [r for r in rows if predicate(r)])
    counters = [collections.Counter(v for r in cohort for v in set(getter(r))) for cohort in cohorts]
    names = sorted(counters[2], key=lambda k: (-counters[2][k], k))
    cells = []
    for name in names:
        values = [f"{c[name]}/{len(cohort)} ({100*c[name]/len(cohort):.1f}%)" if cohort else "0/0 (n/a)"
                  for c, cohort in zip(counters, cohorts)]
        cells.append([esc(name), *values])
    return table([label, f"Original n={len(cohorts[0])}", f"Added n={len(cohorts[1])}", f"Combined n={len(cohorts[2])}"], cells)


def printer_groups(rows):
    printers = [r for r in rows if "printer_observation" in r]
    desktop = [r for r in printers if r["printer_observation"]["kind"] == "Desktop printer"]
    groups = []
    for env in sorted({r["environment"] for r in printers}):
        members = [r for r in printers if r["environment"] == env]
        groups.append((
            env, len(members),
            analyze.prevalence([[r["printer_observation"]["support"]] for r in members], len(members)),
            analyze.prevalence([list(r["objects"]) for r in members], len(members)),
        ))
    return printers, desktop, groups


def device_section(rows, groups, family, number):
    members = [r for r in rows if family in r["device_observations"]]
    group = next(g for g in groups if g["kind"] == "Device presence" and g["device_family"] == family)
    environment_groups = [g for g in groups if g["kind"] == "Device presence x environment" and g["device_family"] == family]
    predicate = lambda r: family in r["device_observations"]
    parts = [
        f'<section class="device-section" id="{devices.anchor(family)}">',
        f'<h3>1.{number}. {esc(devices.TITLES[family])} &mdash; {len(members)} scenes</h3>',
        f'<p><strong>{len(members)}/469 ({100*len(members)/469:.1f}%)</strong> of analyzed images contain this device family. '
        f'Original {cohort_n(group, BASE)}; added {cohort_n(group, ADDED)}. {esc(group["strength"])}.</p>',
    ]
    if family == "Printer":
        parts.append("<p>All 25 printer-containing scenes are included: 24 desktop-printer scenes and one industrial scene. "
                     "Integrated industrial machine structure is a separate support category, not a desktop placement recommendation.</p>")
    parts.append("<h4>Device role</h4>")
    parts.append(comparisons(rows, lambda r: [r["device_observations"][family]["role"]], "Role in scene", predicate))
    parts.append("<h4>Environments</h4>")
    parts.append(comparisons(rows, lambda r: [r["environment"]], "Environment", predicate))
    parts.append("<h4>Device-specific immediate support</h4>")
    parts.append(comparisons(rows, lambda r: devices.values(r, family, "immediate"), "Immediate support", predicate))
    parts.append("<h4>Underlying support</h4>")
    parts.append(comparisons(rows, lambda r: devices.values(r, family, "underlying"), "Underlying support", predicate))
    parts.append("<h4>Immediate support materials</h4>")
    parts.append(comparisons(rows, lambda r: devices.values(r, family, "materials"), "Material", predicate))
    parts.append("<h4>Surrounding objects &amp; other devices</h4>")
    parts.append(comparisons(rows, lambda r: devices.surroundings(r, family), "Contextual entity family", predicate))
    parts.append("<h4>Environment &times; support &times; materials &times; surroundings</h4>")
    parts.append(table(
        ["Environment", "Images (original + added)", "Device-specific supports", "Support materials", "Surrounding objects / other devices", "All nine SCAP fields"],
        [[esc(g["name"].split(" present / ", 1)[1]), f'{g["n"]} ({cohort_n(g, BASE)} + {cohort_n(g, ADDED)})',
          counted(g["supports"]), counted(g["support_materials"]), counted(g["surrounding_objects"]),
          f'<a href="#{g["id"]}">Patterns for this device/environment (n={g["n"]})</a>'] for g in environment_groups],
    ))
    parts.append("<h4>Support evidence coverage</h4>")
    parts.append(table(["Evidence basis", "Images"], [
        [esc(e["value"]), f'{e["n"]}/{e["denominator"]} ({e["pct"]:.1f}%)'] for e in group["support_evidence"]
    ]))
    parts.append("<h4>SCAP patterns across all scenes containing this device</h4>")
    parts.append(pattern_table(group["fields"]))
    parts.append("</section>")
    return "\n".join(parts)


def render(rows, groups):
    main = groups[0]
    sections = []
    sections.append("""<header><p class="eyebrow">HP LIFESTYLE DATA ANALYSIS</p>
<h1>Product, environment &amp; SCAP statistics</h1>
<p>One scrollable page. Aggregate statistics only: no gallery, sample pages or pagination.</p></header>
<div class="cards"><div><b>469</b>analyzed image identities</div><div><b>458 + 11</b>original rows + added references</div>
<div><b>9 device families</b>the same breakdown for each</div><div><b>9 fields</b>SCAP patterns for every group</div></div>
<aside><strong>Important cohort distinction:</strong> the 458 original rows are from the no-person parquet.
The 11 added original printer photographs visibly contain people and were freshly captioned by assistant visual inspection.
They are a printer-targeted supplement, not a random sample. Combined percentages therefore describe this collection,
not HP's product or environment distribution. The original parquet and its captions are unchanged.</aside>""")
    sections.append("""<nav aria-label="Contents"><a href="#devices">1. Every device family</a>
<a href="#overview">2. Products &amp; environments</a><a href="#supports">3. Supporting surfaces</a>
<a href="#objects">4. Surrounding objects</a><a href="#associations">5. Product/environment associations</a>
<a href="#patterns">6. SCAP patterns for every group</a><a href="#method">7. Method &amp; downloads</a></nav>""")
    sections.append("""<section id="devices"><h2>1. The same breakdown for every device family</h2>
<p>Each device has its own role, environment, support, material, surrounding-object and nine-field SCAP statistics,
including every observed device/environment combination. Primary and secondary appearances are included.
One image can therefore contribute to several device sections.</p>
<p>Supports belong to the device being counted, not automatically to the scene's focal product.
Reviewed focal-product placements are preserved; other devices require an explicit device-specific caption relationship.
Unknown relationships remain unknown. Multiple explicit placements within one device family are multi-label image-presence counts.
Surrounding-object tables exclude that device's own entity family; SCAP tables describe the whole scene.</p>""")
    sections.append("<nav aria-label='Device families'>" + "".join(
        f'<a href="#{devices.anchor(f)}">{esc(devices.TITLES[f])} ({sum(f in r["device_observations"] for r in rows)})</a>'
        for f in devices.FAMILIES
    ) + "</nav>")
    for number, family in enumerate(devices.FAMILIES, 1):
        sections.append(device_section(rows, groups, family, number))
    sections.append("</section><section id='overview'><h2>2. Products &amp; environments</h2><h3>Primary product focus (exclusive)</h3>")
    sections.append(comparisons(rows, lambda r: [r["product_category"]], "Primary product category"))
    sections.append("<h3>Device presence (multiple devices may occur in one image)</h3>")
    sections.append(comparisons(rows, lambda r: r["device_presence"], "Device family"))
    sections.append("<h3>Environment (one assigned environment per image)</h3>")
    sections.append(comparisons(rows, lambda r: [r["environment"]], "Environment"))
    sections.append("<h3>Source product-name coverage</h3>")
    sections.append(comparisons(rows, lambda r: ["Unnamed" if r["product_name"] == "(unnamed)" else "Named source code"], "Metadata coverage"))
    sections.append("<p>Source product names are unverified catalog codes, not inferred retail SKUs. A named code in a scene with a background printer can refer to a computer, not the printer.</p>")
    sections.append(comparisons(rows, lambda r: [r["product_name"]], "Exact source product code"))
    sections.append("</section><section id='supports'><h2>3. Supporting surfaces</h2><p>These overall tables refer to the <strong>primary product</strong>. For any individual device, including secondary devices, use its dedicated section above. Immediate and underlying supports are separate; nearby furniture is not automatically supporting furniture.</p>")
    sections.append(comparisons(rows, lambda r: [r["support"]["immediate"]], "Immediate support"))
    sections.append("<h3>Underlying support (when a separate layer is established)</h3>")
    sections.append(comparisons(rows, lambda r: [r["support"]["underlying"]], "Underlying support"))
    sections.append("<h3>Immediate support material (multi-label)</h3>")
    sections.append(comparisons(rows, lambda r: r["support"]["materials"], "Material"))
    sections.append("</section><section id='objects'><h2>4. Surrounding objects &amp; room elements</h2><p>Per-image presence, not number of object instances. Device and support families are included for context. Percentages can sum above 100%.</p>")
    sections.append(comparisons(rows, lambda r: list(r["objects"]), "Entity family"))
    sections.append("<h3>Top 30 co-occurring contextual-object pairs</h3><p>Pairs exclude primary device families, generic desks/tables and windows. Counts are association, not causation or generation instructions.</p>")
    sections.append(table(["Pair", "Images / 469", "Percent"], [[esc(e["value"]), f'{e["n"]}/469', f'{e["pct"]:.1f}%'] for e in main["object_pairs"][:30]]))
    sections.append("</section><section id='associations'><h2>5. Product &times; environment associations</h2><p>Every observed primary-category/environment combination is listed. Percentages within a cell use that row's group size. All normalized support, material and object families are shown; the five most frequent repeated co-object pairs are shown per group.</p>")
    associations = [g for g in groups if g["kind"] == "Product category x environment"]
    sections.append(table(
        ["Primary product / environment", "Images (original + added)", "Immediate support", "Material", "Objects / room elements", "Repeated co-object pairs (top five)"],
        [[f'<a href="#{g["id"]}">{esc(g["name"])}</a>', f'{g["n"]} ({cohort_n(g, BASE)} + {cohort_n(g, ADDED)})<br>{esc(g["strength"])}',
          counted(g["supports"]), counted(g["support_materials"]), counted(g["objects"]),
          counted([e for e in g["object_pairs"] if e["n"] >= 2][:5])] for g in associations]))
    sections.append("</section><section id='patterns'><h2>6. SCAP patterns for every product &amp; environment group</h2>")
    sections.append("""<p>Every profile below is on this page. Each contains all nine SCAP fields, normalized pattern counts,
and up to six repeated 2-4-word phrases. Phrase counts describe caption wording, not additional visual facts.
<strong>n=1 is a single observation, not a recurring pattern; n=2-4 is sparse and descriptive only.</strong>
Larger groups can still contain related shots of the same scene. Added visual captions and original Qwen captions have different authoring styles.</p>""")
    for kind, members in itertools.groupby(groups, key=lambda g: g["kind"]):
        members = list(members)
        sections.append(f"<h3>{esc(kind)} ({len(members)} profiles)</h3>")
        sections.append("<p class='profile-index'>" + " | ".join(f'<a href="#{g["id"]}">{esc(g["name"])} ({g["n"]})</a>' for g in members) + "</p>")
        for g in members:
            sections.append(f'<article id="{g["id"]}"><h4>{esc(g["name"])} &mdash; n={g["n"]}</h4>'
                            f'<p class="muted">{esc(g["strength"])}. Original {cohort_n(g, BASE)}; added {cohort_n(g, ADDED)}. '
                            f'{g["dataset_pct"]:.2f}% of the 469-image collection.</p>')
            if g["kind"] != "Product category x environment":
                support_heading = "Device-specific supports" if "device_family" in g else "Primary product supports"
                object_counts = g.get("surrounding_objects", g["objects"])
                sections.append(table(["Environments", support_heading, "Materials", "Objects / room elements"], [
                    [counted(g["environments"]), counted(g["supports"]), counted(g["support_materials"]), counted(object_counts)]
                ]))
            sections.append(pattern_table(g["fields"]))
            sections.append("</article>")
    sections.append("</section><section id='method'><h2>7. Method, limitations &amp; downloads</h2>")
    sections.append(f"""<p><strong>Original source:</strong> <code>{esc(analyze.SOURCE)}</code>. All 458 rows are retained:
432 train and 26 validation; 160 <code>lifestyle_hp_brand</code> and 298 <code>lifestyle</code>.
There are 457 augmented images and one real image according to source metadata. The baseline has 215 unnamed product records.</p>
<p><strong>Printer supplement:</strong> 11 unmatched original identities out of 15 reference photographs.
The four already represented identities were not added again. All 11 additions contain physical people.
The source originals were visually inspected and freshly captioned by the assistant; no new Qwen, GPT or Gemini batch-caption run is claimed.
The industrial-machine identification uses the source catalog and is kept separate from desktop printers.</p>
<p><strong>Counting:</strong> image-presence counts use each image once per category.
Primary focus and environment are exclusive assignments; device, object, material and field tags are multi-label.
Tables show their denominators. Source scene variants remain distinct image identities, including similar office photographs;
469 unique identities do not mean 469 independent scenes. No product-model identity is inferred from appearance.</p>
<p><strong>Evidence:</strong> the original 458-row analysis is caption-derived with reviewed heuristic normalization,
not an independent visual assessment of every baseline image. Every device family now has a device-specific support audit:
reviewed focal placements, explicit device-entity placements, or supporting furniture that explicitly names the device.
Another product's desk is never used merely because it occurs in the same scene. Printer placements retain the earlier reviewed coding.
Two baseline captions directly claim physical-person presence (a lap and a distant person); these are caption warnings, not newly verified visual findings.
Screen/poster depictions are not counted as physical people. Unknown support/material remains unknown.</p>
<p><strong>SCAP coverage:</strong> all nine fields are nonempty in all 469 records.
Field tags are rule-based and non-exhaustive; an absent tag means no normalized match, not visual absence.
Repeated phrases require at least two images and can reflect template wording. Exact field values are retained in downloads.</p>
<p><strong>For product-shot generation:</strong> use product-specific support and environment associations as descriptive guidance,
not engineering specifications. This analysis supplies no measured clearances, validated physical dimensions, or tested generation success rates.
People visible in added references are not recommendations to introduce people into a no-person output.</p>
<p class="downloads"><a href="additional_printer_captions.json">11 new structured captions (JSON)</a>
<a href="additional_printer_captions.csv">11 new captions (CSV)</a>
<a href="combined_captioned.parquet">469-image captioned parquet</a>
<a href="rows.json">469-image extraction audit (JSON)</a>
<a href="device_placement_audit.csv">All device-specific placement evidence (CSV)</a>
<a href="statistics.json">Complete aggregate statistics (JSON)</a>
<a href="association_counts.csv">Association counts (CSV)</a>
<a href="scap_pattern_counts.csv">SCAP pattern counts (CSV)</a></p>
<p class="muted">Downloads are supporting data, not separate report/sample pages. All report statistics and group profiles are above.
No source photograph or source parquet has been overwritten.</p></section>""")
    body = "\n".join(sections)
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HP Lifestyle - Consolidated Statistics</title>
<style>
*{box-sizing:border-box}html{scroll-behavior:auto}body{font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;color:#17283a;background:#f4f7fb;margin:0}
main{max-width:1600px;margin:auto;background:white;padding:28px 34px 70px}
h1{font-size:34px;line-height:1.2;margin:8px 0 12px}h2{font-size:26px;margin-top:45px;padding-bottom:8px;border-bottom:3px solid #1264a3}
h3{font-size:21px;margin-top:30px}h4{font-size:19px;margin:0 0 8px}a{color:#075e9b}p{max-width:1200px}
.eyebrow{font-size:12px;letter-spacing:2px;color:#1264a3;font-weight:700}.muted{color:#53677b}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:24px 0}.cards div{padding:16px;background:#eaf3fb;border:1px solid #d5e5f3;border-radius:8px}.cards b{display:block;font-size:30px;color:#075e9b}
aside{padding:18px;border-left:5px solid #bc7b09;background:#fff7e2}nav{display:flex;flex-wrap:wrap;gap:12px 24px;padding:20px 0}
.table-wrap{overflow-x:auto;margin:14px 0 24px}table{width:100%;border-collapse:collapse;font-size:13px;table-layout:auto}
th{background:#e8f0f8;text-align:left;white-space:normal}th,td{border:1px solid #d8e1eb;padding:10px 12px;vertical-align:top}
td:first-child{min-width:135px}tbody tr:nth-child(even){background:#f8fafc}td{overflow-wrap:anywhere}caption{text-align:left;font-weight:bold;padding:10px}
article{padding:22px 0;border-top:1px solid #b9c9d8;scroll-margin-top:12px}.profile-index{font-size:13px;line-height:1.9}
.device-section{padding:15px 0 25px;border-top:2px solid #b9c9d8;scroll-margin-top:12px}.device-section h4{margin-top:24px}
.downloads{display:flex;flex-wrap:wrap;gap:12px 24px}code{overflow-wrap:anywhere;font-size:12px}
@media(max-width:700px){main{padding:18px 12px}.cards{grid-template-columns:repeat(2,1fr)}h1{font-size:27px}th,td{padding:8px;font-size:12px}}
</style></head><body><main>""" + body + "</main></body></html>"


def cohort_n(group, cohort):
    return next((e["n"] for e in group["cohorts"] if e["value"] == cohort), 0)


def pattern_table(fields):
    return table(["SCAP field", "Nonempty records", "Normalized patterns (image presence)", "Repeated caption phrases"],
                 [[esc(field), f'{fields[field]["present"]}/{fields[field]["denominator"]}',
                   counted(fields[field]["patterns"]), counted(fields[field]["repeated_phrases"])] for field in FIELDS])


def write_csv(path, headers, rows):
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def build():
    OUT.mkdir(exist_ok=True)
    rows, raw, captions = load()
    groups = stats(rows)
    printer_rows, desktop, _ = printer_groups(rows)
    document = render(rows, groups)
    (OUT / "index.html").write_text(document)
    for name, value in (
        ("rows.json", rows), ("statistics.json", groups),
        ("additional_printer_captions.json", captions),
        ("printer_reconciliation.json", json.loads((ROOT / "printer-reconciliation.json").read_text())),
    ):
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2))
    pq.write_table(pa.Table.from_pylist(raw), OUT / "combined_captioned.parquet", compression="zstd")
    write_csv(OUT / "additional_printer_captions.csv",
              ["reference", "image_hash", "target_image", "cohort", "caption_provenance", "human_presence", *FIELDS, "printer_observation"],
              [[c[k] for k in ("reference", "image_hash", "target_image", "cohort", "caption_provenance", "human_presence")]
               + [json.dumps(c["scap"][f], ensure_ascii=False) if isinstance(c["scap"][f], (dict, list)) else c["scap"][f] for f in FIELDS]
               + [json.dumps(c["printer_observation"])] for c in captions])
    write_csv(OUT / "device_placement_audit.csv",
              ["source_row", "image_hash", "cohort", "device_family", "role", "immediate_support", "underlying_support", "materials", "basis", "evidence"],
              [[r["source_row"], r["image_hash"], r["cohort"], family, info["role"],
                p["immediate"], p["underlying"], "; ".join(p["materials"]), p["basis"], p["evidence"]]
               for r in rows for family, info in r["device_observations"].items() for p in info["placements"]])
    association_records = []
    pattern_records = []
    for g in groups:
        for dimension in ("products", "environments", "product_names", "supports", "underlying_supports", "support_materials", "objects", "object_pairs", "device_presence"):
            association_records.extend([g["kind"], g["name"], dimension, e["value"], e["n"], e["denominator"], e["pct"]] for e in g[dimension])
        for dimension in ("surrounding_objects", "roles", "support_evidence"):
            association_records.extend([g["kind"], g["name"], dimension, e["value"], e["n"], e["denominator"], e["pct"]] for e in g.get(dimension, []))
        for field, info in g["fields"].items():
            for kind in ("patterns", "repeated_phrases"):
                pattern_records.extend([g["kind"], g["name"], field, kind, e["value"], e["n"], e["denominator"], e["pct"]] for e in info[kind])
    write_csv(OUT / "association_counts.csv", ["group_kind", "group", "dimension", "value", "n", "denominator", "pct"], association_records)
    write_csv(OUT / "scap_pattern_counts.csv", ["group_kind", "group", "field", "pattern_kind", "value", "n", "denominator", "pct"], pattern_records)
    metadata = {
        "identities": len(rows), "baseline": 458, "added": len(captions),
        "printer_containing": len(printer_rows), "desktop_printer_containing": len(desktop),
        "industrial_printer_containing": len(printer_rows) - len(desktop),
        "profiles": len(groups), "scap_fields_per_profile": 9,
        "device_families": {f: sum(f in r["device_observations"] for r in rows) for f in devices.FAMILIES},
        "source_parquet_sha256": hashlib.sha256((ROOT / "source.parquet").read_bytes()).hexdigest(),
        "url": f"{CDN}/index.html",
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    build()
