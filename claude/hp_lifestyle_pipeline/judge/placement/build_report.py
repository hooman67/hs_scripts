#!/usr/bin/env python3
"""Build the local, upload-ready natural-placement judge report.

The builder performs no model calls and no uploads. It snapshots completed result
directories, copies the exact evaluated image bytes into the planned gallery
layout, and publishes sanitized audit files with hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLACEMENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PLACEMENT_DIR.parents[1]
DEFAULT_RUN_DIR = PLACEMENT_DIR / "runs" / "pilot_v1c"
DEFAULT_SPLIT = PLACEMENT_DIR / "data" / "split.json"
DEFAULT_ASSETS = PLACEMENT_DIR / "data" / "assets.json"
DEFAULT_ANNOTATIONS = PLACEMENT_DIR / "data" / "annotation_inventory.json"
DEFAULT_OUTPUT = PLACEMENT_DIR / "report" / "gallery"
PREFERRED_AUTH_SOURCE = Path(
    "/home/colligo/hs_scripts/claude/temp_work/lifestyle_gallery/imsauth.js"
)
FALLBACK_AUTH_SOURCE = (
    PROJECT_DIR
    / "eval_sets"
    / "hp_lifestyle_prompt_digital_twin_eval_v1"
    / "gallery"
    / "imsauth.js"
)
PLANNED_S3_PREFIX = "eval_sets/hp_natural_placement_judge_v1_20261104/gallery"
BUILDER_ID = "hp-natural-placement-report-v1"

SENSITIVE_JSON_KEYS = {
    "access_token",
    "api_key",
    "authorization",
    "aws_access_key_id",
    "aws_secret_access_key",
    "aws_session_token",
    "bearer_token",
    "client_secret",
    "credential",
    "credentials",
    "id_token",
    "password",
    "refresh_token",
    "secret",
    "token",
}


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>HP natural-placement judge · pilot evidence</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <div id="ims"></div>
  <div id="loading" class="loading">Loading placement-judge report…</div>
  <main id="content" class="hidden">
    <header>
      <p class="eyebrow">HP lifestyle pipeline</p>
      <h1>Natural-placement judge · pilot evidence</h1>
      <p class="lede">Image-level judge outputs shown with every runtime input and available human evidence.</p>
      <div class="warning"><strong>Provisional evidence only.</strong> Verdict thresholds are not human-calibrated. This report makes no claim of overall human accuracy, false-positive rate, deployment reliability, or equivalence between missing annotations and passes.</div>
      <div class="anchor-warning"><strong>Examples are development data.</strong> The fixed visual rubric examples below are development demonstrations or researcher-interpreted reference photographs. Held-out targets and held-out labels are never used as examples.</div>
      <p id="evaluationLink" class="raw-links"></p>
    </header>
    <section id="researchSummary" class="visual-rubric"></section>
    <details class="visual-rubric"><summary>Visual rubric examples · fixed model inputs</summary><p id="anchorStatus" class="meta"></p><div id="visualAnchors" class="anchor-grid"></div></details>
    <section class="controls" aria-label="Report filters">
      <label>Split <select id="splitFilter"><option value="all">All</option></select></label>
      <label>Type <select id="typeFilter"><option value="all">All</option></select></label>
      <label>Verdict <select id="verdictFilter"><option value="all">All</option></select></label>
      <label class="search">Search <input id="searchFilter" type="search" placeholder="Case, evidence, annotation…"></label>
    </section>
    <p id="status" class="status"></p>
    <section id="gallery" class="gallery"></section>
  </main>
  <script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>
  <script src="./imsauth.js"></script>
  <script src="./app.js"></script>
  <script>document.addEventListener("DOMContentLoaded", () => initializeIMS());</script>
</body>
</html>
"""


STYLE_CSS = """:root{--ink:#17212b;--muted:#62707f;--line:#d9e0e7;--paper:#f4f6f8;--card:#fff;--blue:#1473e6;--amber:#a85f00;--red:#b42318;--green:#16794b}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.48 Arial,sans-serif}.hidden{display:none!important}.loading{padding:42px;text-align:center}main{max-width:1500px;margin:auto;padding:28px}header,.controls,.case,.visual-rubric{background:var(--card);border:1px solid var(--line);border-radius:12px}header{padding:24px;margin-bottom:16px}.eyebrow{text-transform:uppercase;letter-spacing:.12em;color:var(--blue);font-weight:700}.lede{font-size:18px;color:var(--muted)}.warning,.anchor-warning{padding:14px 16px;border-left:5px solid var(--amber);background:#fff7e6;border-radius:4px;margin-top:10px}.anchor-warning{border-color:var(--blue);background:#eef6ff}.visual-rubric{padding:16px;margin-bottom:16px}.anchor-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:12px}.anchor-card{border:1px solid var(--line);border-radius:9px;overflow:hidden;background:#fff}.anchor-card img{display:block;width:100%;aspect-ratio:4/3;object-fit:contain;background:#dde2e7}.anchor-card .body{padding:12px}.controls{display:flex;gap:14px;flex-wrap:wrap;align-items:end;padding:14px;margin-bottom:12px}.controls label{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted);font-weight:700}.controls select,.controls input{min-width:160px;padding:8px;border:1px solid #b8c2cc;border-radius:6px;background:#fff;color:var(--ink)}.controls .search{flex:1}.controls .search input{width:100%}.status{color:var(--muted);margin:12px 2px}.gallery{display:grid;gap:18px}.case{padding:20px}.case-head{display:flex;justify-content:space-between;gap:14px;align-items:start}.case h2{margin:0 0 5px;font-size:20px}.meta{color:var(--muted)}.badges{display:flex;gap:6px;flex-wrap:wrap}.badge{display:inline-block;border-radius:16px;padding:3px 9px;background:#edf3f8;font-size:12px;font-weight:700}.verdict-pass{background:#e2f5e9;color:var(--green)}.verdict-review{background:#fff1d6;color:#8a4b00}.verdict-fail,.verdict-unavailable{background:#fde8e7;color:var(--red)}.images{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:16px 0}.image-panel{margin:0;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:#eef1f4}.image-panel img{display:block;width:100%;aspect-ratio:4/3;object-fit:contain;background:#dde2e7}.image-panel figcaption{padding:8px 10px;background:#fff}.scoreline{display:flex;gap:12px;flex-wrap:wrap;padding:11px;background:#f6f9fc;border:1px solid var(--line);border-radius:8px}.scoreline strong{font-size:18px}.component-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin-top:12px}.component{border:1px solid var(--line);border-radius:8px;padding:12px}.component h4{margin:0 0 6px}.component p{margin:6px 0}.component .evidence{font-size:14px}.component .consequence{color:var(--muted);font-size:13px}details{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-top:10px;background:#fff}summary{cursor:pointer;font-weight:700}.annotation-warning{color:#8a4b00}.annotation{border-top:1px solid var(--line);padding-top:8px;margin-top:8px}.exact{white-space:pre-wrap;background:#f7f8fa;padding:10px;border-radius:6px}.raw-links{display:flex;gap:10px;flex-wrap:wrap}.raw-links a{color:var(--blue)}.empty{padding:34px;background:#fff;border:1px solid var(--line);border-radius:10px;text-align:center;color:var(--muted)}.error{color:var(--red)}.ims-span{margin-right:8px}.ims-button{margin:5px;padding:5px 9px}@media(max-width:800px){main{padding:12px}.images{grid-template-columns:1fr}.case-head{display:block}.badges{margin-top:8px}}
"""


APP_JS = r"""const $=id=>document.getElementById(id);
const esc=value=>String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const human=value=>String(value??"").replaceAll("_"," ").replace(/\b\w/g,c=>c.toUpperCase());
let REPORT=null;
function addOptions(id,values){for(const value of [...new Set(values)].sort()){const option=document.createElement("option");option.value=value;option.textContent=human(value);$(id).appendChild(option)}}
function imagePanel(asset,label){return `<figure class="image-panel"><img loading="lazy" src="./${esc(asset.relative_path)}" alt="${esc(label)}"><figcaption><strong>${esc(label)}</strong><br><span class="meta">${asset.width}×${asset.height} · SHA-256 ${esc(asset.sha256.slice(0,12))}…</span></figcaption></figure>`}
function renderResearchSummary(){const r=REPORT.review_summary;if(!r){$("researchSummary").hidden=true;return}$("researchSummary").innerHTML=`<h2>${esc(r.title)}</h2><p><strong>${esc(r.conclusion)}</strong></p><ul>${r.findings.map(x=>`<li>${esc(x)}</li>`).join("")}</ul><h3>Score components</h3><table><thead><tr><th>Component</th><th>Weight</th></tr></thead><tbody>${r.weights.map(x=>`<tr><td>${esc(x.component)}</td><td>${esc(x.weight)}</td></tr>`).join("")}</tbody></table><p>${esc(r.scoring_note)}</p><p>${esc(r.limitations)}</p><p><a href="./SUMMARY.md">Full findings and reproduction</a> · <a href="./system_prompt.md">System prompt</a> · <a href="./judgments.json">All target judgments JSON</a></p>`}
function renderAnchors(){const anchors=REPORT.visual_rubric_examples||{examples:[]};$("anchorStatus").textContent=anchors.status||"No fixed visual rubric examples were available at build time.";$("visualAnchors").innerHTML=anchors.examples.length?anchors.examples.map(anchor=>`<article class="anchor-card"><img loading="lazy" src="./${esc(anchor.asset.relative_path)}" alt="Visual rubric example ${esc(anchor.asset_id)}"><div class="body"><div class="badges"><span class="badge">${esc(human(anchor.kind))}</span><span class="badge">not a target row</span></div><h3>${esc(anchor.asset_id)}</h3><p>${esc(anchor.guidance)}</p><details><summary>Provenance</summary><ul><li>Source field: ${esc(anchor.provenance.source_field)}</li><li>Source report: ${esc(anchor.provenance.source_report)}</li><li>Source S3 object: ${esc(anchor.asset.source_s3_url)}</li><li>SHA-256: ${esc(anchor.asset.sha256)}</li><li>Fixed-anchor set SHA-256: ${esc(anchors.definition_sha256)}</li></ul></details></div></article>`).join(""):`<p class="empty">No fixed visual rubric examples were present in the included development requests. None were invented.</p>`;if(REPORT.evaluation_summary){$("evaluationLink").innerHTML=`<a href="./${esc(REPORT.evaluation_summary.relative_path)}" target="_blank" rel="noopener">Sanitized evaluation summary JSON</a> · SHA-256 ${esc(REPORT.evaluation_summary.published_sha256.slice(0,12))}…`}else{$("evaluationLink").textContent=""}}
function components(judgment){if(!judgment)return "";const observation=judgment.observation||{};return `<div class="component-grid">${Object.entries(observation.components||{}).map(([name,c])=>`<article class="component"><h4>${esc(human(name))}</h4><div class="badges"><span class="badge">score ${esc(judgment.component_scores?.[name]??"unscored")}</span><span class="badge">${esc(c.visibility)}</span><span class="badge">severity ${esc(c.severity??"n/a")}</span><span class="badge">${esc(c.confidence)} confidence</span></div><p class="evidence">${esc(c.evidence)}</p><p class="consequence">${esc(c.consequence)}</p>${c.issue_codes?.length?`<p><strong>Issues:</strong> ${esc(c.issue_codes.join(", "))}</p>`:""}</article>`).join("")}</div>`}
function annotationDetails(row){const a=row.human_evidence;const records=a.records||[];return `<details><summary>Human annotation evidence · ${records.length} record${records.length===1?"":"s"}</summary><p class="annotation-warning"><strong>Attribution warning:</strong> ${esc(a.attribution_warning)}</p>${records.length?records.map(record=>`<article class="annotation"><p><strong>${esc(record.reviewer_name||record.reviewer_ldap||"Unknown reviewer")}</strong> · ${esc(record.reviewer_ldap||"")} · ${esc(record.submitted_at||"time unavailable")}</p><p class="exact">${record.comment_present?esc(record.comment_exact):"<em>Empty comment in source. This is not a pass.</em>"}</p>${record.ratings?.length?`<details><summary>Exact structured ratings</summary><ul>${record.ratings.map(r=>`<li>${esc(r.question_text)}: <strong>${esc(r.answer_label)}</strong> <span class="meta">(${esc(r.placement_label_applicability)}; ${esc(r.attribution?.kind)})</span></li>`).join("")}</ul></details>`:""}${record.comment_segments?.length?`<details><summary>Recorded comment attribution segments</summary><ul>${record.comment_segments.map(s=>`<li>“${esc(s.exact_quote)}” · ${esc(s.category)} · target ${esc((s.target_variant_labels||[]).join(", "))} (${esc(s.target_basis)})</li>`).join("")}</ul></details>`:""}</article>`).join(""):"<p><em>No human annotation record exists for this source row. Absence is not a pass.</em></p>"}</details>`}
function rawLinks(row){return `<details><summary>Raw audit files and model-input provenance</summary><p class="raw-links">${row.raw_files.map(file=>`<a href="./${esc(file.relative_path)}" target="_blank" rel="noopener">${esc(file.label)}</a>`).join("")}</p><ul><li>Requested model: ${esc(row.model.requested||"unavailable")}</li><li>Returned model: ${esc(row.model.returned||"unavailable")}</li><li>Image detail: ${esc(row.model.image_detail||"unavailable")}</li><li>System prompt SHA-256: ${esc(row.model.system_prompt_sha256||"unavailable")}</li><li>Observation schema SHA-256: ${esc(row.model.schema_sha256||"unavailable")}</li><li>Scoring policy SHA-256: ${esc(row.model.scoring_sha256||"unavailable")}</li></ul></details>`}
function caseCard(row){const j=row.judgment;const verdict=j?.verdict||"unavailable";const score=j?.natural_placement_score??"unavailable";const coverage=j?.coverage==null?"unavailable":`${Math.round(j.coverage*100)}%`;const summary=j?.observation?.summary||row.error?.message||"No completed judgment is available; no score or verdict is inferred.";return `<article class="case"><div class="case-head"><div><h2>${esc(row.id)}</h2><div class="meta">Source row ${row.row} · ${esc(row.variant.toUpperCase())} · ${esc(row.product_type)} · ${esc(row.image_stage)}</div></div><div class="badges"><span class="badge">${esc(row.split)}</span><span class="badge">${esc(row.product_type)}</span><span class="badge verdict-${esc(verdict)}">${esc(verdict)}</span></div></div><div class="images">${imagePanel(row.twin_asset,"Original digital twin (model input)")}${imagePanel(row.generated_asset,"Generated scene (evaluated image)")}</div><div class="scoreline"><span><strong>${esc(score)}</strong><br>placement score</span><span><strong>${esc(coverage)}</strong><br>visible coverage</span><span><strong>${esc(j?.confidence||"unavailable")}</strong><br>confidence</span><span><strong>${esc(verdict)}</strong><br>verdict</span></div><p>${esc(summary)}</p>${j?components(j):`<p class="error">No judgment payload: ${esc(row.error?.type||"result unavailable")}</p>`}<details><summary>Original scene prompt and scalar model inputs</summary><p class="exact">${esc(row.original_prompt)}</p><ul><li>Product type: ${esc(row.product_type)}</li><li>Image stage: ${esc(row.image_stage)}</li><li>Generated-image SHA-256: ${esc(row.generated_asset.sha256)}</li><li>Twin-image SHA-256: ${esc(row.twin_asset.sha256)}</li></ul></details>${annotationDetails(row)}${rawLinks(row)}</article>`}
function render(){const split=$("splitFilter").value,type=$("typeFilter").value,verdict=$("verdictFilter").value,q=$("searchFilter").value.toLowerCase();const rows=REPORT.rows.filter(row=>(split==="all"||row.split===split)&&(type==="all"||row.product_type===type)&&(verdict==="all"||(row.judgment?.verdict||"unavailable")===verdict)&&(!q||JSON.stringify(row).toLowerCase().includes(q)));$("status").textContent=`${rows.length} of ${REPORT.rows.length} completed or attempted evaluations shown. ${REPORT.run_state_message}`;$("gallery").innerHTML=rows.length?rows.map(caseCard).join(""):`<div class="empty">No result rows match the current filters. ${esc(REPORT.run_state_message)}</div>`}
async function loadReport(){try{const response=await fetch("./data.json",{cache:"no-store"});if(!response.ok)throw new Error(`HTTP ${response.status}`);REPORT=await response.json();renderResearchSummary();renderAnchors();addOptions("splitFilter",REPORT.rows.map(r=>r.split));addOptions("typeFilter",REPORT.rows.map(r=>r.product_type));addOptions("verdictFilter",REPORT.rows.map(r=>r.judgment?.verdict||"unavailable"));for(const id of ["splitFilter","typeFilter","verdictFilter"]){$(id).onchange=render}$("searchFilter").oninput=render;render()}catch(error){$("status").innerHTML=`<span class="error">Could not load report data: ${esc(error.message)}</span>`}}
function onAuthReady(){if(window.__placementReportStarted)return;window.__placementReportStarted=true;loadReport()}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-summary", type=Path)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--annotations", type=Path, default=DEFAULT_ANNOTATIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--auth-source", type=Path, default=PREFERRED_AUTH_SOURCE)
    parser.add_argument("--planned-s3-prefix", default=PLANNED_S3_PREFIX)
    parser.add_argument(
        "--include-splits",
        default="development",
        help="Comma-separated frozen splits to publish; defaults to development only.",
    )
    parser.add_argument(
        "--evaluation-summary",
        type=Path,
        help="Optional evaluation JSON to sanitize, hash, and link without interpreting metrics.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def publication_path(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(PROJECT_DIR).as_posix()
    except ValueError:
        home = Path("/home/colligo")
        try:
            return f"<HOME>/{resolved.relative_to(home).as_posix()}"
        except ValueError:
            return f"<LOCAL_PATH>/{resolved.name}"


def sanitize_json(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            normalized = str(key).lower()
            if normalized in SENSITIVE_JSON_KEYS or normalized == "auth_mode":
                continue
            clean[key] = sanitize_json(item, replacements)
        return clean
    if isinstance(value, list):
        return [sanitize_json(item, replacements) for item in value]
    if isinstance(value, str):
        clean = value
        for source, replacement in sorted(replacements.items(), key=lambda pair: -len(pair[0])):
            clean = clean.replace(source, replacement)
        clean = clean.replace(os.fspath(PROJECT_DIR), "<PROJECT_ROOT>")
        clean = clean.replace("/home/colligo/.claude", "<USER_CONFIG>")
        clean = clean.replace("/home/colligo", "<HOME>")
        return clean
    return value


def copy_verified_asset(
    asset: dict[str, Any],
    gallery_dir: Path,
    planned_s3_prefix: str,
    *,
    relative_path: Path | None = None,
    role: str,
) -> dict[str, Any]:
    source = Path(asset["local_path"])
    if not source.is_file():
        raise FileNotFoundError(f"Missing local image asset: {source}")
    source_hash = sha256_file(source)
    if source_hash != asset["sha256"]:
        raise ValueError(f"Source asset hash mismatch for {source}")
    relative = relative_path or (
        Path("assets") / f"row_{int(asset['row']):02d}" / source.name
    )
    destination = gallery_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copy2(source, destination)
    if sha256_file(destination) != source_hash:
        raise ValueError(f"Copied asset hash mismatch for {destination}")
    return {
        "asset_id": asset["id"],
        "role": role,
        "relative_path": relative.as_posix(),
        "planned_s3_key": f"{planned_s3_prefix.rstrip('/')}/{relative.as_posix()}",
        "source_s3_url": asset["s3_url"],
        "sha256": source_hash,
        "width": asset["width"],
        "height": asset["height"],
        "bytes": asset["bytes"],
    }


def publish_raw_files(
    case_dir: Path,
    case_id: str,
    gallery_dir: Path,
    replacements: dict[str, str],
) -> list[dict[str, Any]]:
    published = []
    candidates = (
        ("request.json", "sanitized request JSON"),
        ("result.json", "sanitized result JSON"),
        ("response.json", "sanitized raw model response JSON"),
        ("observation_schema.json", "observation schema JSON"),
        ("system_prompt.md", "system prompt"),
    )
    for filename, label in candidates:
        source = case_dir / filename
        if not source.is_file():
            continue
        relative = Path("raw") / case_id / filename
        destination = gallery_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        source_hash = sha256_file(source)
        if source.suffix == ".json":
            value = sanitize_json(load_json(source), replacements)
            destination.write_text(
                json.dumps(value, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            sanitized = True
        else:
            shutil.copyfile(source, destination)
            sanitized = False
        published.append(
            {
                "label": label,
                "relative_path": relative.as_posix(),
                "source_sha256": source_hash,
                "published_sha256": sha256_file(destination),
                "sanitized": sanitized,
            }
        )
    return published


def annotation_evidence(records: list[dict[str, Any]]) -> dict[str, Any]:
    selected = []
    for record in records:
        selected.append(
            {
                "reviewer_ldap": record.get("reviewer_ldap"),
                "reviewer_name": record.get("reviewer_name"),
                "submitted_at": record.get("submitted_at"),
                "complete": record.get("complete"),
                "comment_exact": record.get("comment_exact", ""),
                "comment_present": bool(record.get("comment_present")),
                "comment_target_default": record.get("comment_target_default"),
                "ratings": record.get("ratings", []),
                "comment_segments": record.get("comment_segments", []),
                "interpretation_guard": record.get("interpretation_guard"),
            }
        )
    if not selected:
        status = "none_not_pass"
    elif not any(record["comment_present"] for record in selected):
        status = "empty_comments_not_pass"
    else:
        status = "present_not_automatic_pass"
    return {
        "status": status,
        "attribution_warning": (
            "Comments and ratings can target a named variant or the comparison set. "
            "Unspecified comparison-wide evidence must not be assigned to one variant. "
            "Structured preferences are not placement passes, and zero or empty annotations are not passes."
        ),
        "records": selected,
    }


def collect_visual_rubric_examples(
    run_dir: Path,
    split_cases: dict[str, dict[str, Any]],
    allowed_splits: set[str],
    assets: dict[str, dict[str, Any]],
    gallery_dir: Path,
    planned_s3_prefix: str,
) -> tuple[dict[str, Any], dict[str, str], list[dict[str, Any]]]:
    definitions: list[tuple[Path, dict[str, Any]]] = []
    if run_dir.is_dir():
        for case_id, case in sorted(split_cases.items()):
            if case["split"] not in allowed_splits:
                continue
            request_path = run_dir / case_id / "request.json"
            if not request_path.is_file():
                continue
            request = load_json(request_path)
            visual_anchors = request.get("visual_anchors")
            if visual_anchors:
                definitions.append((request_path, visual_anchors))

    if not definitions:
        return (
            {
                "status": "No fixed visual-anchor definition was available in included requests.",
                "definition_sha256": None,
                "source_request_paths": [],
                "examples": [],
            },
            {},
            [],
        )

    canonical_path, canonical = definitions[0]
    canonical_hash = sha256_json(canonical)
    for request_path, definition in definitions[1:]:
        if sha256_json(definition) != canonical_hash:
            raise ValueError(
                f"Visual-anchor definition differs between {canonical_path} and {request_path}"
            )
    examples = canonical.get("examples", [])
    kinds = [example.get("kind") for example in examples]
    if len(examples) != 5:
        raise ValueError(f"Expected 5 fixed visual anchors, found {len(examples)}")
    if kinds.count("development_human_defect_anchor") != 3:
        raise ValueError("Expected 3 development human-defect anchors")
    if kinds.count("researcher_interpreted_reference") != 2:
        raise ValueError("Expected 2 researcher-interpreted reference anchors")

    published_examples = []
    replacements: dict[str, str] = {}
    manifest_entries = []
    for example in examples:
        asset_id = example["asset_id"]
        if asset_id not in assets:
            raise KeyError(f"Visual-anchor asset is absent from assets.json: {asset_id}")
        asset = assets[asset_id]
        if example.get("sha256") != asset["sha256"]:
            raise ValueError(f"Visual-anchor hash differs from assets.json: {asset_id}")
        if example.get("s3_url") != asset["s3_url"]:
            raise ValueError(f"Visual-anchor S3 provenance differs from assets.json: {asset_id}")
        if Path(example["local_path"]).resolve() != Path(asset["local_path"]).resolve():
            raise ValueError(f"Visual-anchor local source differs from assets.json: {asset_id}")
        if example["kind"] == "development_human_defect_anchor":
            anchor_case = split_cases.get(asset_id)
            if not anchor_case or anchor_case["split"] != "development":
                raise ValueError(f"Human-defect anchor is not a development case: {asset_id}")
        suffix = Path(asset["local_path"]).suffix.lower() or ".png"
        relative = Path("assets") / "visual_rubric_examples" / f"{asset_id}{suffix}"
        copied = copy_verified_asset(
            asset,
            gallery_dir,
            planned_s3_prefix,
            relative_path=relative,
            role="visual_rubric_example_not_target",
        )
        replacements[os.fspath(Path(example["local_path"]).resolve())] = copied[
            "relative_path"
        ]
        manifest_entries.append(copied)
        published_examples.append(
            {
                "asset_id": asset_id,
                "kind": example["kind"],
                "guidance": example["guidance"],
                "asset": copied,
                "provenance": {
                    "source_field": "request.visual_anchors.examples",
                    "source_report": asset["source_report"],
                    "request_definition_sha256": canonical_hash,
                },
            }
        )
    return (
        {
            "status": canonical.get("status"),
            "definition_sha256": canonical_hash,
            "source_request_paths": [publication_path(path) for path, _ in definitions],
            "examples": published_examples,
        },
        replacements,
        manifest_entries,
    )


def publish_evaluation_summary(
    source: Path | None,
    gallery_dir: Path,
) -> dict[str, Any] | None:
    if source is None:
        return None
    source = source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Evaluation summary does not exist: {source}")
    relative = Path("raw") / "evaluation_summary.json"
    destination = gallery_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    clean = sanitize_json(load_json(source), {})
    destination.write_text(
        json.dumps(clean, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {
        "relative_path": relative.as_posix(),
        "source_path": publication_path(source),
        "source_sha256": sha256_file(source),
        "published_sha256": sha256_file(destination),
        "sanitized": True,
        "interpreted": False,
    }


def validate_existing_output(output: Path) -> None:
    if not output.exists():
        return
    data_path = output / "data.json"
    if not data_path.is_file():
        raise RuntimeError(f"Refusing to replace unrecognized output directory: {output}")
    existing = load_json(data_path)
    if existing.get("builder") != BUILDER_ID:
        raise RuntimeError(f"Refusing to replace output from another builder: {output}")


def choose_auth_source(requested: Path) -> tuple[Path, bool]:
    requested = requested.expanduser().resolve()
    if requested.is_file():
        return requested, False
    fallback = FALLBACK_AUTH_SOURCE.resolve()
    if fallback.is_file():
        return fallback, True
    raise FileNotFoundError(
        f"IMS auth source missing at preferred path {requested} and fallback {fallback}"
    )


def build(args: argparse.Namespace) -> dict[str, Any]:
    split_path = args.split.expanduser().resolve()
    assets_path = args.assets.expanduser().resolve()
    annotations_path = args.annotations.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    output = args.output.expanduser().resolve()
    validate_existing_output(output)

    split = load_json(split_path)
    assets_document = load_json(assets_path)
    annotations = load_json(annotations_path)
    split_cases = {case["id"]: case for case in split["cases"]}
    allowed_splits = {
        value.strip() for value in args.include_splits.split(",") if value.strip()
    }
    known_splits = {case["split"] for case in split_cases.values()}
    if not allowed_splits or not allowed_splits <= known_splits:
        raise ValueError(
            f"--include-splits must select known splits {sorted(known_splits)}; "
            f"got {sorted(allowed_splits)}"
        )
    allowed_rows = {
        int(case["row"])
        for case in split_cases.values()
        if case["split"] in allowed_splits
    }
    assets = {asset["id"]: asset for asset in assets_document["assets"]}
    source_report = assets_document["comparison_report"]["report_id"]
    annotations_by_row: dict[int, list[dict[str, Any]]] = {}
    for record in annotations["annotation_records"]:
        if (
            record.get("report_id") == source_report
            and int(record["row_idx"]) in allowed_rows
        ):
            annotations_by_row.setdefault(int(record["row_idx"]), []).append(record)

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.parent / f".{output.name}.building"
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir(parents=True)

    warnings = []
    visual_examples, anchor_replacements, anchor_manifest_entries = (
        collect_visual_rubric_examples(
            run_dir,
            split_cases,
            allowed_splits,
            assets,
            temporary,
            args.planned_s3_prefix,
        )
    )
    candidate_result_paths = (
        sorted(run_dir.glob("*/result.json")) if run_dir.is_dir() else []
    )
    fixed_anchor_ids = {
        example["asset_id"] for example in visual_examples["examples"]
    }
    skipped_anchor_results = []
    result_paths = []
    for candidate in candidate_result_paths:
        case = split_cases.get(candidate.parent.name)
        if case is None:
            raise ValueError(f"Result {candidate} has no frozen split entry")
        if candidate.parent.name in fixed_anchor_ids:
            skipped_anchor_results.append(candidate.parent.name)
        elif case["split"] in allowed_splits:
            result_paths.append(candidate)
    if skipped_anchor_results:
        warnings.append(
            "Fixed visual examples were excluded from target evaluation rows: "
            + ", ".join(sorted(skipped_anchor_results))
        )
    if not run_dir.is_dir():
        run_state = "results_directory_missing"
        run_message = "The configured results directory does not exist; no evaluations are shown."
    elif not result_paths:
        run_state = "no_results"
        run_message = (
            f"No result files exist yet for included splits {sorted(allowed_splits)}; "
            "no evaluations are shown and no values are inferred."
        )
    else:
        run_state = "results_available"
        run_message = (
            f"Only completed or attempted result files in included splits "
            f"{sorted(allowed_splits)} present at build time are shown."
        )

    rows = []
    copied_assets: dict[str, dict[str, Any]] = {}
    for result_path in result_paths:
        case_id = result_path.parent.name
        case = split_cases[case_id]
        result = load_json(result_path)
        generated_id = case_id
        twin_id = f"comparison-row-{int(case['row']):02d}-product_input"
        if generated_id not in assets or twin_id not in assets:
            raise KeyError(f"Missing asset manifest entry for {case_id}")
        generated_source = assets[generated_id]
        twin_source = assets[twin_id]
        if generated_source["sha256"] != case["image_sha256"]:
            raise ValueError(f"Generated-image split/manifest hash mismatch for {case_id}")
        if twin_source["sha256"] != case["input_sha256"]:
            raise ValueError(f"Twin-image split/manifest hash mismatch for {case_id}")
        for image_name, expected in (("generated_image", case["image_sha256"]), ("twin_image", case["input_sha256"])):
            result_hash = result.get("images", {}).get(image_name, {}).get("sha256")
            if result_hash and result_hash != expected:
                raise ValueError(f"Result image hash mismatch for {case_id} {image_name}")

        for asset in (generated_source, twin_source):
            if asset["id"] not in copied_assets:
                copied_assets[asset["id"]] = copy_verified_asset(
                    asset,
                    temporary,
                    args.planned_s3_prefix,
                    role=(
                        "target_original_twin"
                        if asset["type"] == "product_input"
                        else "target_generated_scene"
                    ),
                )
        generated_asset = copied_assets[generated_id]
        twin_asset = copied_assets[twin_id]
        replacements = dict(anchor_replacements)
        replacements.update({
            os.fspath(Path(generated_source["local_path"]).resolve()): generated_asset["relative_path"],
            os.fspath(Path(twin_source["local_path"]).resolve()): twin_asset["relative_path"],
        })
        raw_files = publish_raw_files(
            result_path.parent,
            case_id,
            temporary,
            replacements,
        )
        input_record = result.get("input", {})
        judgment = result.get("judgment") if result.get("ok") else None
        error = None
        if not result.get("ok"):
            error = {
                "type": result.get("error_type", "result_not_ok"),
                "status_code": result.get("status_code"),
                "message": "The result did not contain a completed judgment; no score or verdict is inferred.",
                "validation_errors": result.get("validation_errors"),
            }
        rows.append(
            {
                "id": case_id,
                "split": case["split"],
                "row": int(case["row"]),
                "variant": case["variant"],
                "product_type": input_record.get("product_type", str(case["device"]).lower()),
                "image_stage": input_record.get("image_stage", "scene_generation"),
                "original_prompt": input_record.get("scene_prompt", generated_source.get("original_prompt", "")),
                "twin_asset": twin_asset,
                "generated_asset": generated_asset,
                "judgment": judgment,
                "error": error,
                "human_evidence": annotation_evidence(annotations_by_row.get(int(case["row"]), [])),
                "model": {
                    "requested": result.get("model_requested"),
                    "returned": result.get("model_returned"),
                    "reasoning_effort": result.get("reasoning_effort"),
                    "image_detail": result.get("image_detail"),
                    "system_prompt_sha256": result.get("system_prompt_sha256"),
                    "schema_sha256": result.get("schema_sha256"),
                    "scoring_sha256": result.get("scoring_sha256"),
                },
                "raw_files": raw_files,
                "source_result": publication_path(result_path),
            }
        )

    rows.sort(key=lambda row: (row["split"], row["row"], row["variant"]))
    auth_source, auth_fallback_used = choose_auth_source(args.auth_source)
    shutil.copyfile(auth_source, temporary / "imsauth.js")
    auth_hash = sha256_file(auth_source)
    if sha256_file(temporary / "imsauth.js") != auth_hash:
        raise ValueError("IMS auth copy does not match its source bytes")

    evaluation_source = args.evaluation_summary
    if evaluation_source is None:
        default_evaluation = run_dir / "development_evaluation.json"
        if default_evaluation.is_file():
            evaluation_source = default_evaluation
    evaluation_summary = publish_evaluation_summary(evaluation_source, temporary)
    asset_manifest = sorted(
        [*copied_assets.values(), *anchor_manifest_entries],
        key=lambda item: (item["role"], item["relative_path"]),
    )
    report = {
        "builder": BUILDER_ID,
        "schema_version": 1,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "planned_s3_prefix": args.planned_s3_prefix.rstrip("/"),
        "included_splits": sorted(allowed_splits),
        "run_state": run_state,
        "run_state_message": run_message,
        "threshold_notice": (
            "Verdict thresholds are provisional and not human-calibrated. No overall human-accuracy, "
            "false-positive-rate, or deployment-reliability claim is made."
        ),
        "zero_annotations_policy": "Zero records and empty comments are not passes.",
        "visual_rubric_examples": visual_examples,
        "asset_manifest": asset_manifest,
        "evaluation_summary": evaluation_summary,
        "review_summary": load_json(args.review_summary) if args.review_summary else None,
        "sources": {
            "run_directory": publication_path(run_dir),
            "split": {"path": publication_path(split_path), "sha256": sha256_file(split_path)},
            "assets": {"path": publication_path(assets_path), "sha256": sha256_file(assets_path)},
            "annotations": {"path": publication_path(annotations_path), "sha256": sha256_file(annotations_path)},
            "auth": {
                "preferred_source": publication_path(Path(args.auth_source)),
                "used_source": publication_path(auth_source),
                "fallback_used": auth_fallback_used,
                "sha256": auth_hash,
                "copied_exactly": True,
            },
        },
        "warnings": warnings,
        "rows": rows,
    }
    (temporary / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (temporary / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (temporary / "app.js").write_text(APP_JS, encoding="utf-8")
    (temporary / "data.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    shutil.copyfile(PLACEMENT_DIR / "SUMMARY.md", temporary / "SUMMARY.md")
    shutil.copyfile(PLACEMENT_DIR / "system_prompt.md", temporary / "system_prompt.md")
    (temporary / "judgments.json").write_text(json.dumps({"threshold_status":"provisional_not_human_calibrated", "rows":[{"id":r["id"],"split":r["split"],"product_type":r["product_type"],"original_prompt":r["original_prompt"],"judgment":r.get("judgment")} for r in rows]}, indent=2)+"\n")

    previous = output.parent / f".{output.name}.previous"
    if previous.exists():
        shutil.rmtree(previous)
    if output.exists():
        output.replace(previous)
    temporary.replace(output)
    if previous.exists():
        shutil.rmtree(previous)
    return report


def main() -> None:
    args = parse_args()
    report = build(args)
    print(
        json.dumps(
            {
                "output": os.fspath(args.output.expanduser().resolve()),
                "rows": len(report["rows"]),
                "included_splits": report["included_splits"],
                "visual_rubric_examples": len(
                    report["visual_rubric_examples"]["examples"]
                ),
                "run_state": report["run_state"],
                "auth_fallback_used": report["sources"]["auth"]["fallback_used"],
                "auth_sha256": report["sources"]["auth"]["sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
