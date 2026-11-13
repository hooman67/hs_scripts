#!/usr/bin/env python3
"""Build the text-only surface-diversity census and standalone report."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import run_generation as generation


TOKEN_RE = re.compile(r"[a-z0-9]+(?:['’-][a-z0-9]+)?", re.I)
TABLE_FAMILIES = {"table", "table_worktable", "worktable"}
KIND_TO_FAMILY = {
    "table": "table",
    "worktable": "table",
    "desk": "desk",
    "freestanding_cabinet": "freestanding_cabinet",
    "credenza_sideboard": "credenza_sideboard",
    "fitted_base_cabinetry": "fitted_counter",
    "equipment_cart": "equipment_cart",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(path: Path) -> Any:
    require(path.is_file(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def group_slug(device: str, camera: str) -> str:
    return f"{device}__{camera}".replace("/", "_").replace(" ", "_")


def primary_support(prompt: dict[str, Any]) -> dict[str, Any]:
    """Normalize finalizer metadata without inferring anything from prompt prose."""
    raw = prompt.get("primary_support")
    require(isinstance(raw, dict), f"{prompt.get('prompt_key')}: missing finalizer primary_support metadata")
    kind = raw.get("kind")
    family = raw.get("family") or KIND_TO_FAMILY.get(kind)
    shape = raw.get("shape")
    phrase = raw.get("phrase") or raw.get("text_evidence")
    require(isinstance(family, str) and family, f"{prompt.get('prompt_key')}: primary_support has no family/kind")
    require(shape in {"round", "oval", "rectangular", "square", "other", "unspecified"},
            f"{prompt.get('prompt_key')}: invalid primary_support shape {shape!r}")
    require(isinstance(phrase, str) and phrase and phrase in prompt.get("text", ""),
            f"{prompt.get('prompt_key')}: primary_support phrase is not an exact prompt quotation")
    return {
        "family": family,
        "shape": shape,
        "phrase": phrase,
        "kind": kind,
        "catalogue_id": raw.get("catalogue_id"),
        "raw": copy.deepcopy(raw),
    }


def score_distribution(values: list[int]) -> dict[str, Any]:
    require(values, "score distribution is empty")
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.fmean(values), 3),
        "median": round(float(statistics.median(values)), 3),
        "counts": dict(sorted(Counter(values).items())),
        "ten_point_bins": [
            {
                "label": f"{start}–{start + 9 if start < 90 else 100}",
                "count": sum(start <= value <= (start + 9 if start < 90 else 100) for value in values),
            }
            for start in range(0, 100, 10)
        ],
    }


def support_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    families = Counter(row["primary_support"]["family"] for row in rows)
    shapes = Counter(row["primary_support"]["shape"] for row in rows)
    named_shapes = {key: value for key, value in sorted(shapes.items()) if key != "unspecified"}
    cafe = [row for row in rows if row["device_type"] == "laptop" and str(row["environment"]).casefold() in {"café", "cafe"}]
    cafe_round = [row for row in cafe if row["primary_support"]["shape"] == "round"]
    return {
        "family_counts": dict(sorted(families.items())),
        "shape_counts": dict(sorted(shapes.items())),
        "explicit_shape_counts": named_shapes,
        "round_cafe": {
            "numerator": len(cafe_round),
            "denominator": len(cafe),
            "definition": "Laptop prompt rows whose environment is Café and whose finalizer primary_support.shape is round.",
            "row_ids": [row["row_id"] for row in cafe_round],
            "non_round_row_ids": [row["row_id"] for row in cafe if row not in cafe_round],
        },
    }


def _tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.casefold().replace("’", "'"))


def recurring_phrases(rows: list[dict[str, Any]], limit: int = 40) -> list[dict[str, Any]]:
    occurrences: dict[str, set[str]] = defaultdict(set)
    display: dict[str, str] = {}
    for row in rows:
        words = _tokens(row["text"])
        for size in range(3, 7):
            for start in range(0, len(words) - size + 1):
                phrase = " ".join(words[start:start + size])
                occurrences[phrase].add(row["row_id"])
                display.setdefault(phrase, phrase)
    candidates = [(phrase, ids) for phrase, ids in occurrences.items() if len(ids) >= 3]
    candidates.sort(key=lambda item: (-len(item[1]), -len(item[0].split()), item[0]))
    kept: list[tuple[str, set[str]]] = []
    for phrase, ids in candidates:
        if any(ids == other_ids and f" {phrase} " in f" {other} " for other, other_ids in kept):
            continue
        kept.append((phrase, ids))
        if len(kept) >= limit:
            break
    by_id = {row["row_id"]: row for row in rows}
    output: list[dict[str, Any]] = []
    for phrase, ids in kept:
        ordered = sorted(ids)
        quotes: dict[tuple[str, str, str], list[str]] = defaultdict(list)
        for row_id in ordered:
            for evidence in by_id[row_id]["prompt_record"].get("evidence") or []:
                quote_text = evidence.get("quote")
                if quote_text:
                    key = (str(evidence.get("document") or ""), str(evidence.get("path") or ""), str(quote_text))
                    quotes[key].append(row_id)
        output.append({
            "phrase": display[phrase],
            "prompt_count": len(ordered),
            "row_ids": ordered,
            "rows": [{"row_id": row_id, "fe_url": by_id[row_id]["fe_url"]} for row_id in ordered],
            "source_quotes": [
                {"document": key[0], "path": key[1], "quote": key[2], "row_ids": value}
                for key, value in sorted(quotes.items())
            ],
        })
    return output


def metric_summary(values: list[int]) -> dict[str, Any]:
    require(values, "metric distribution is empty")
    return {"count": len(values), "min": min(values), "max": max(values), "mean": round(statistics.fmean(values), 3),
            "median": round(float(statistics.median(values)), 3), "counts": dict(sorted(Counter(values).items()))}


def text_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    word_counts = [len(_tokens(row["text"])) for row in rows]
    sentence_counts = [len([part for part in re.split(r"(?<=[.!?])\s+", row["text"].strip()) if part]) for row in rows]
    prop_counts = [len(row["prop_ids"]) for row in rows]
    return {"word_count": metric_summary(word_counts), "sentence_count": metric_summary(sentence_counts),
            "declared_prop_count": metric_summary(prop_counts),
            "zero_declared_prop_rows": [row["row_id"] for row in rows if not row["prop_ids"]]}


def source_coverage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    documents: dict[str, dict[str, Any]] = {}
    reference_rows: dict[str, list[str]] = defaultdict(list)
    missing_references: list[str] = []
    for row in rows:
        reference = row["ctech_reference_id"]
        if reference:
            reference_rows[str(reference)].append(row["row_id"])
        else:
            missing_references.append(row["row_id"])
        seen_docs: set[str] = set()
        for item in row["prompt_record"].get("evidence") or []:
            document = str(item.get("document") or "(unnamed)")
            entry = documents.setdefault(document, {"prompt_rows": set(), "quote_count": 0, "paths": set()})
            entry["prompt_rows"].add(row["row_id"])
            entry["quote_count"] += bool(item.get("quote"))
            if item.get("path"):
                entry["paths"].add(str(item["path"]))
            seen_docs.add(document)
    return {
        "ctech_references": {"distinct_count": len(reference_rows), "missing_row_ids": missing_references,
                             "counts": {key: len(value) for key, value in sorted(reference_rows.items())},
                             "rows": dict(sorted(reference_rows.items()))},
        "source_documents": [
            {"document": name, "prompt_count": len(value["prompt_rows"]), "quote_count": value["quote_count"],
             "paths": sorted(value["paths"]), "row_ids": sorted(value["prompt_rows"])}
            for name, value in sorted(documents.items(), key=lambda item: (-len(item[1]["prompt_rows"]), item[0]))
        ],
    }


def lexical_audit(rows: list[dict[str, Any]], pair_limit: int = 20) -> dict[str, Any]:
    exact: dict[str, list[str]] = defaultdict(list)
    canonical: dict[str, list[str]] = defaultdict(list)
    token_sets: dict[str, set[str]] = {}
    for row in rows:
        exact[row["text"]].append(row["row_id"])
        tokens = _tokens(row["text"])
        canonical[" ".join(tokens)].append(row["row_id"])
        token_sets[row["row_id"]] = set(tokens)
    pairs = []
    for index, left in enumerate(rows):
        for right in rows[index + 1:]:
            union = token_sets[left["row_id"]] | token_sets[right["row_id"]]
            similarity = len(token_sets[left["row_id"]] & token_sets[right["row_id"]]) / max(1, len(union))
            pairs.append((similarity, left, right))
    pairs.sort(key=lambda item: (-item[0], item[1]["row_id"], item[2]["row_id"]))
    return {
        "distinct_exact_texts": len(exact), "distinct_canonical_texts": len(canonical),
        "exact_duplicate_groups": [{"row_ids": ids, "text": text} for text, ids in exact.items() if len(ids) > 1],
        "canonical_duplicate_groups": [{"row_ids": ids, "canonical_text": text} for text, ids in canonical.items() if len(ids) > 1],
        "closest_token_pairs": [
            {"jaccard": round(score, 4), "left": left["row_id"], "right": right["row_id"],
             "left_fe_url": left["fe_url"], "right_fe_url": right["fe_url"]}
            for score, left, right in pairs[:pair_limit]
        ],
    }


def bank_compliance(rows: list[dict[str, Any]], bank_audit: dict[str, Any]) -> list[dict[str, Any]]:
    banks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        banks[row["bank_id"]].append(row)
    require(len(banks) == 16 and all(len(items) == 10 for items in banks.values()), "expected 16 banks of ten")
    output = []
    for bank_id, items in sorted(banks.items()):
        items.sort(key=lambda row: row["bank_rank"])
        device_type = items[0]["device_type"]
        families = Counter(item["primary_support"]["family"] for item in items)
        shapes = Counter(item["primary_support"]["shape"] for item in items)
        errors = []
        metrics: dict[str, Any]
        if device_type == "laptop":
            round_count = sum(item["primary_support"]["shape"] == "round" for item in items)
            cafe = [item for item in items if str(item["environment"]).casefold() in {"café", "cafe"}]
            cafe_round = sum(item["primary_support"]["shape"] == "round" for item in cafe)
            if round_count < 2:
                errors.append({"code": "laptop_round_primary_minimum", "required": 2, "actual": round_count})
            if cafe_round != len(cafe):
                errors.append({"code": "cafe_primary_support_not_round", "required": len(cafe), "actual": cafe_round})
            metrics = {"round_supports": round_count, "round_minimum": 2,
                       "round_cafe_numerator": cafe_round, "round_cafe_denominator": len(cafe)}
        else:
            non_table = sum(item["primary_support"]["family"] not in TABLE_FAMILIES for item in items)
            if len(families) < 3:
                errors.append({"code": "printer_support_family_minimum", "required": 3, "actual": len(families)})
            if non_table < 5:
                errors.append({"code": "printer_non_table_primary_minimum", "required": 5, "actual": non_table})
            metrics = {"distinct_families": len(families), "family_minimum": 3,
                       "non_table_supports": non_table, "non_table_minimum": 5}
        prior = bank_audit.get(bank_id) or {}
        output.append({
            "bank_id": bank_id,
            "device_id": items[0]["device_id"],
            "device_type": device_type,
            "camera_id": items[0]["camera_id"],
            "view_role": items[0]["view_role"],
            "passed": not errors,
            "errors": errors,
            "metrics": metrics,
            "family_counts": dict(sorted(families.items())),
            "shape_counts": dict(sorted(shapes.items())),
            "finalizer_primary_support_audit": copy.deepcopy((prior.get("debug") or {}).get("primary_support_audit")),
            "rows": [
                {"row_id": item["row_id"], "rank": item["bank_rank"], "environment": item["environment"],
                 "primary_support": item["primary_support"], "fe_url": item["fe_url"]}
                for item in items
            ],
            "fe_url": f"../groups/{group_slug(items[0]['device_id'], items[0]['camera_id'])}/viewer.html",
        })
    return output


def prop_group_frequency(rows: list[dict[str, Any]], catalog_path: Path | None) -> dict[str, Any]:
    if catalog_path is None:
        return {"available": False, "reason": "No frozen approved-prop catalog was supplied; groups were not inferred."}
    catalog = load(catalog_path.resolve())
    entries = catalog.get("entries")
    require(isinstance(entries, list), "approved prop catalog must contain entries")
    by_id = {item["id"]: item for item in entries}
    group_rows: dict[str, set[str]] = defaultdict(set)
    group_assignments: Counter[str] = Counter()
    prop_rows: dict[str, set[str]] = defaultdict(set)
    bank_groups: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        for prop_id in row["prompt_record"].get("prop_ids") or []:
            require(prop_id in by_id, f"{row['row_id']}: approved prop ID {prop_id!r} absent from supplied catalog")
            prop_rows[prop_id].add(row["row_id"])
            for group in by_id[prop_id].get("repetition_groups") or []:
                group_rows[group].add(row["row_id"])
                group_assignments[group] += 1
                bank_groups[row["bank_id"]][group] += 1
    groups = []
    for group, row_ids in group_rows.items():
        groups.append({
            "group": group,
            "prompt_count": len(row_ids),
            "assignment_count": group_assignments[group],
            "row_ids": sorted(row_ids),
            "rows": [{"row_id": row_id, "fe_url": next(row["fe_url"] for row in rows if row["row_id"] == row_id)}
                     for row_id in sorted(row_ids)],
        })
    groups.sort(key=lambda item: (-item["prompt_count"], item["group"]))
    return {
        "available": True,
        "catalog": {"path": str(catalog_path.resolve()), "sha256": sha256(catalog_path.resolve()),
                    "version": catalog.get("version"), "revision": catalog.get("revision"),
                    "purpose": catalog.get("purpose"), "entry_count": len(entries),
                    "environment_counts": dict(sorted(Counter(str(item.get("environment") or "unspecified") for item in entries).items())),
                    "role_counts": dict(sorted(Counter(str(item.get("role") or "unspecified") for item in entries).items())),
                    "repetition_group_count": len({group for item in entries for group in item.get("repetition_groups") or []})},
        "groups": groups,
        "used_props": [
            {"prop_id": prop_id, "name": by_id[prop_id].get("name"),
             "environment": by_id[prop_id].get("environment"), "role": by_id[prop_id].get("role"),
             "repetition_groups": by_id[prop_id].get("repetition_groups") or [], "prompt_count": len(row_ids),
             "row_ids": sorted(row_ids),
             "rows": [{"row_id": row_id, "fe_url": next(row["fe_url"] for row in rows if row["row_id"] == row_id)}
                      for row_id in sorted(row_ids)]}
            for prop_id, row_ids in sorted(prop_rows.items(), key=lambda item: (-len(item[1]), item[0]))
        ],
        "usage": {"assignment_count": sum(len(row["prop_ids"]) for row in rows),
                  "unique_prop_ids": len(prop_rows), "unique_repetition_groups": len(group_rows),
                  "zero_prop_row_ids": [row["row_id"] for row in rows if not row["prop_ids"]]},
        "bank_group_compliance": [
            {"bank_id": bank_id, "passed": all(count <= 1 for count in counts.values()),
             "duplicate_groups": {group: count for group, count in sorted(counts.items()) if count > 1},
             "group_counts": dict(sorted(counts.items()))}
            for bank_id, counts in sorted((bank_id, bank_groups[bank_id]) for bank_id in {row["bank_id"] for row in rows})
        ],
    }


def build_analysis(
    document: dict[str, Any], validated_rows: list[dict[str, Any]], records: dict[str, dict[str, Any]],
    source_inputs: dict[str, dict[str, Any]], prompts_path: Path, prompts_sha256: str,
    catalog_path: Path | None, run_dir: Path | None = None, run_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rows = []
    for row in sorted(validated_rows, key=lambda item: (generation.DEVICE_ORDER.index(item["device_id"]),
                      generation.VIEW_ORDER[item["device_id"]].index(item["camera_id"]), item["rank"])):
        prompt = row["prompt"]
        bank_id = prompt.get("bank_debug_ref") or row["row_id"].rsplit("::", 1)[0]
        require(bank_id in source_inputs, f"missing full source input for {bank_id}")
        record = records.get(row["row_id"])
        valid_record = generation.valid_completed_record(run_dir, row) if record and run_dir else None
        if record and record.get("status") == "done" and valid_record is None:
            status = "invalid done record / artifact missing or mismatched"
        else:
            status = record.get("status", "pending") if record else "pending"
        item = {
            "row_id": row["row_id"], "device_id": row["device_id"],
            "device_display_name": prompt.get("device_display_name") or row["device_id"],
            "device_type": prompt.get("device_type"), "camera_id": row["camera_id"],
            "camera_tag": prompt.get("camera_tag"), "view_role": prompt.get("view_role") or prompt.get("camera_tag"),
            "bank_id": bank_id, "bank_rank": row["rank"], "environment": prompt.get("environment"),
            "text": prompt.get("text"), "source_relevance_score": int(prompt["source_relevance_score"]),
            "ctech_reference_score": int(prompt["ctech_reference_score"]),
            "ctech_reference_id": prompt.get("ctech_reference_id"), "primary_support": primary_support(prompt),
            "prop_ids": list(prompt.get("prop_ids") or []), "generation_status": status,
            "generated_artifact_present": valid_record is not None,
            "fe_url": f"../groups/{group_slug(row['device_id'], row['camera_id'])}/viewer.html?rows={row['rank']}&per=1",
            "prompt_record": copy.deepcopy(prompt), "source_input_id": bank_id,
        }
        rows.append(item)
    require(len(rows) == 160, "distribution expects 160 text prompt rows")
    sources = [row["source_relevance_score"] for row in rows]
    ctech = [row["ctech_reference_score"] for row in rows]
    status_counts = Counter(row["generation_status"] for row in rows)
    supports = support_summary(rows)
    banks = bank_compliance(rows, document.get("bank_audit") or {})
    return {
        "schema_version": "hp-surface-diversity-v6.2-text-distribution-v1",
        "status": "text census; generation artifacts and image judgments reported separately",
        "inputs": {"prompts": {"path": str(prompts_path.resolve()), "sha256": prompts_sha256},
                   "approved_prop_catalog": str(catalog_path.resolve()) if catalog_path else None,
                   "run_identity": copy.deepcopy(run_manifest) if run_manifest else None},
        "scope": {
            "text_prompt_rows": 160, "banks": 16, "prompts_per_bank": 10,
            "generated_artifact_count": sum(row["generated_artifact_present"] for row in rows),
            "generation_status_counts": dict(sorted(status_counts.items())),
            "image_content_rows_audited": 0, "new_judgment_scores_used": 0,
            "scope_note": "All distributions, support labels, prop groups, and phrases are prompt-text metadata. Generated artifact counts come only from saved run records. No image content was inferred or judged here.",
        },
        "counts": {
            "environment": dict(sorted(Counter(row["environment"] for row in rows).items())),
            "product": dict(sorted(Counter(row["device_display_name"] for row in rows).items())),
            "product_type": dict(sorted(Counter(row["device_type"] for row in rows).items())),
            "view": dict(sorted(Counter(row["view_role"] for row in rows).items())),
            "endpoint_camera": dict(sorted(Counter(row["camera_id"] for row in rows).items())),
        },
        "score_distributions": {
            "source_relevance": {"label": "Prompt-writer source relevance, not a judge score", **score_distribution(sources)},
            "ctech_reference": {"label": "Prompt-writer declared C-Tech reference score, not an image judge score", **score_distribution(ctech)},
        },
        "text_metrics": text_metrics(rows),
        "source_coverage": source_coverage(rows),
        "lexical_audit": lexical_audit(rows),
        "primary_support": supports,
        "bank_compliance": banks,
        "approved_prop_groups": prop_group_frequency(rows, catalog_path),
        "recurring_phrases": recurring_phrases(rows),
        "source_inputs": copy.deepcopy(source_inputs),
        "rows": rows,
        "limitations": [
            "Primary-support counts use finalizer primary_support metadata; this builder never infers support family or shape from production prompt prose.",
            "Declared source and C-Tech scores describe prompt-writing metadata and are not image judgments.",
            "Approved-prop frequencies count declared prompt metadata, not visible image objects.",
            "Recurring phrases are exact normalized 3–6 word prompt n-grams shared by at least three rows; linked source quotes are the rows' declared source evidence, not proof that the recurring wording is verbatim source text.",
            "Generation status records only artifact availability. Image content audited remains zero until a distinct image review is supplied.",
        ],
    }


def _safe_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_html(analysis: dict[str, Any]) -> str:
    data = _safe_json(analysis)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HP V6.2 surface-diversity text distribution</title>
<style>
:root{{--bg:#0b0d12;--panel:#151923;--line:#2a3140;--text:#edf1f7;--muted:#aab3c2;--blue:#78a9ff;--green:#55d6a0;--amber:#ffd166}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,sans-serif}}a{{color:var(--blue)}}
main{{max-width:1500px;margin:auto;padding:24px}}header{{display:flex;gap:18px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}}
h1{{font-size:26px;margin:0 0 6px}}h2{{font-size:18px;margin:0 0 14px}}.muted{{color:var(--muted)}}.badge{{display:inline-block;padding:4px 8px;border:1px solid var(--amber);color:var(--amber);border-radius:999px;font-weight:700}}
.cards,.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:18px 0}}section,.card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}}.metric{{font-size:28px;font-weight:750}}table{{width:100%;border-collapse:collapse}}th,td{{padding:8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{color:var(--muted)}}
.bar{{height:7px;background:#252c39;border-radius:9px;overflow:hidden;margin-top:4px}}.bar i{{display:block;height:100%;background:var(--blue)}}
.ok{{color:var(--green)}}.bad{{color:#ff7b88}}.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}select,input{{background:#0e1219;color:var(--text);border:1px solid var(--line);padding:8px;border-radius:6px}}details{{margin:8px 0}}summary{{cursor:pointer;color:var(--blue)}}pre{{white-space:pre-wrap;word-break:break-word;background:#0d1016;padding:10px;border-radius:6px;max-height:420px;overflow:auto}}.prompt{{max-width:720px}}.nowrap{{white-space:nowrap}}
</style></head><body><main>
<header><div><span class="badge">TEXT CENSUS</span><h1>HP Lifestyle V6.2 — Surface diversity</h1><div class="muted">Prompt metadata, declared scores, approved props, and source evidence. Image content audited: 0.</div><div class="muted" id="lineage"></div></div><nav><a href="../viewer.html">All grouped FE rows</a> · <a href="downloads/analysis.json">Analysis JSON</a> · <a href="downloads/prompts_all_160.json">Frozen prompts</a></nav></header>
<div id="app"></div>
<script id="report-data" type="application/json">{data}</script>
<script>
const D=JSON.parse(document.getElementById('report-data').textContent);const app=document.getElementById('app');
const e=s=>String(s??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
const RI=D.inputs.run_identity||{{}};document.getElementById('lineage').textContent=RI.run_sha256?`Run ${{RI.run_sha256}} · ${{RI.generator}} · ${{RI.rewriterVersion}}`:'';
const entries=o=>Object.entries(o||{{}});const bars=o=>{{let m=Math.max(1,...entries(o).map(x=>x[1]));return entries(o).map(([k,v])=>`<tr><td>${{e(k)}}</td><td>${{v}}</td><td><div class="bar"><i style="width:${{100*v/m}}%"></i></div></td></tr>`).join('')}};
const dist=s=>`<table><tr><th>Range</th><th>Rows</th><th></th></tr>${{s.ten_point_bins.map(x=>`<tr><td>${{e(x.label)}}</td><td>${{x.count}}</td><td><div class="bar"><i style="width:${{x.count/Math.max(1,...s.ten_point_bins.map(y=>y.count))*100}}%"></i></div></td></tr>`).join('')}}</table><p class="muted">min ${{s.min}} · mean ${{s.mean}} · median ${{s.median}} · max ${{s.max}}</p>`;
function rowLinks(rows){{return rows.map(x=>`<a href="${{e(x.fe_url)}}">${{e(x.row_id||x)}}</a>`).join(', ')}}
const s=D.scope,p=D.primary_support,props=D.approved_prop_groups;
app.innerHTML=`<div class="cards"><div class="card"><div class="metric">${{s.text_prompt_rows}}</div><b>text prompt rows</b></div><div class="card"><div class="metric">${{s.generated_artifact_count}}</div><b>generated artifacts present</b><div class="muted">Artifact status only</div></div><div class="card"><div class="metric">${{s.image_content_rows_audited}}</div><b>image rows audited here</b></div><div class="card"><div class="metric">${{p.round_cafe.numerator}} / ${{p.round_cafe.denominator}}</div><b>round Café primary supports</b><div class="muted">Laptop text rows</div></div></div>
<div class="cols"><section><h2>Environment</h2><table>${{bars(D.counts.environment)}}</table></section><section><h2>Product</h2><table>${{bars(D.counts.product)}}</table></section><section><h2>View</h2><table>${{bars(D.counts.view)}}</table></section><section><h2>Support family</h2><table>${{bars(p.family_counts)}}</table></section><section><h2>Explicitly named shape</h2><table>${{bars(p.explicit_shape_counts)}}</table><p class="muted">Unspecified: ${{p.shape_counts.unspecified||0}}</p></section><section><h2>Generation status</h2><table>${{bars(s.generation_status_counts)}}</table></section></div>
<div class="cols"><section><h2>Source relevance distribution</h2>${{dist(D.score_distributions.source_relevance)}}</section><section><h2>C-Tech score distribution</h2>${{dist(D.score_distributions.ctech_reference)}}</section></div>
<div class="cols"><section><h2>Prompt length</h2><pre>${{e(JSON.stringify(D.text_metrics,null,2))}}</pre></section><section><h2>C-Tech reference coverage</h2><p><b>${{D.source_coverage.ctech_references.distinct_count}}</b> distinct declared references · ${{D.source_coverage.ctech_references.missing_row_ids.length}} missing rows</p><table>${{bars(D.source_coverage.ctech_references.counts)}}</table></section><section><h2>Declared source-document coverage</h2><table><tr><th>Document</th><th>Prompt rows</th><th>Quotes</th></tr>${{D.source_coverage.source_documents.map(x=>`<tr><td>${{e(x.document)}}</td><td>${{x.prompt_count}}</td><td>${{x.quote_count}}</td></tr>`).join('')}}</table></section></div>
<section><h2>Per-bank surface compliance</h2><table><tr><th>Bank</th><th>Type</th><th>Status</th><th>Metrics</th><th>Families / shapes</th></tr>${{D.bank_compliance.map(b=>`<tr><td><a href="${{e(b.fe_url)}}">${{e(b.bank_id)}}</a></td><td>${{e(b.device_type)}}</td><td class="${{b.passed?'ok':'bad'}}">${{b.passed?'pass':'fail'}}</td><td><pre>${{e(JSON.stringify(b.metrics,null,2))}}</pre></td><td><details><summary>Counts and all primary_support rows</summary><pre>${{e(JSON.stringify({{families:b.family_counts,shapes:b.shape_counts,rows:b.rows,finalizer_audit:b.finalizer_primary_support_audit}},null,2))}}</pre></details></td></tr>`).join('')}}</table></section>
<section><h2>Approved prop catalog and repetition groups</h2>${{props.available?`<p class="muted">Catalog ${{e(props.catalog.version)}} · ${{e(props.catalog.revision)}} · SHA-256 ${{e(props.catalog.sha256)}}</p><pre>${{e(JSON.stringify({{catalog:props.catalog,usage:props.usage}},null,2))}}</pre><table><tr><th>Group</th><th>Prompt rows</th><th>Assignments</th><th>FE rows</th></tr>${{props.groups.map(g=>`<tr><td>${{e(g.group)}}</td><td>${{g.prompt_count}}</td><td>${{g.assignment_count}}</td><td>${{rowLinks(g.rows)}}</td></tr>`).join('')}}</table><details><summary>Per-bank repetition-group compliance</summary><pre>${{e(JSON.stringify(props.bank_group_compliance,null,2))}}</pre></details>`:`<p class="muted">${{e(props.reason)}}</p>`}}</section>
<section><h2>Approved prop ID frequency</h2>${{props.available?`<table><tr><th>Prop</th><th>Environment / role</th><th>Prompt rows</th><th>FE rows</th></tr>${{props.used_props.map(x=>`<tr><td>${{e(x.prop_id)}} · ${{e(x.name)}}</td><td>${{e(x.environment)}} · ${{e(x.role)}}<br><span class="muted">${{e(x.repetition_groups.join(', '))}}</span></td><td>${{x.prompt_count}}</td><td>${{rowLinks(x.rows)}}</td></tr>`).join('')}}</table>`:`<p class="muted">Catalog pending.</p>`}}</section>
<section><h2>Lexical duplicate and closest-pair audit</h2><p>${{D.lexical_audit.distinct_exact_texts}} exact texts · ${{D.lexical_audit.distinct_canonical_texts}} canonical texts</p><details><summary>Duplicates and 20 closest token-overlap pairs</summary><pre>${{e(JSON.stringify(D.lexical_audit,null,2))}}</pre></details></section>
<section><h2>Recurring exact prompt phrases with declared source quotes</h2><p class="muted">Normalized 3–6 word phrases in at least three prompt rows. Source quotes are the exact evidence attached to those rows.</p>${{D.recurring_phrases.map(x=>`<details><summary>“${{e(x.phrase)}}” · ${{x.prompt_count}} rows</summary><p>${{rowLinks(x.rows)}}</p><pre>${{e(JSON.stringify(x.source_quotes,null,2))}}</pre></details>`).join('')}}</section>
<section><h2>Prompt rows</h2><div class="filters"><select id="env"><option value="">All environments</option></select><select id="prod"><option value="">All products</option></select><select id="view"><option value="">All views</option></select><select id="fam"><option value="">All support families</option></select><select id="shape"><option value="">All shapes</option></select><input id="search" placeholder="Search prompts"></div><div id="rows"></div></section>
<section><h2>Scope and limits</h2><pre>${{e(JSON.stringify({{scope:D.scope,limitations:D.limitations}},null,2))}}</pre></section>`;
function options(id,values){{document.getElementById(id).insertAdjacentHTML('beforeend',[...new Set(values)].sort().map(v=>`<option>${{e(v)}}</option>`).join(''))}};
options('env',D.rows.map(r=>r.environment));options('prod',D.rows.map(r=>r.device_display_name));options('view',D.rows.map(r=>r.view_role));options('fam',D.rows.map(r=>r.primary_support.family));options('shape',D.rows.map(r=>r.primary_support.shape));
function renderRows(){{const value=id=>document.getElementById(id).value;let q=value('search').toLowerCase();let rows=D.rows.filter(r=>(!value('env')||r.environment===value('env'))&&(!value('prod')||r.device_display_name===value('prod'))&&(!value('view')||r.view_role===value('view'))&&(!value('fam')||r.primary_support.family===value('fam'))&&(!value('shape')||r.primary_support.shape===value('shape'))&&(!q||r.text.toLowerCase().includes(q)));document.getElementById('rows').innerHTML=`<p class="muted">${{rows.length}} / ${{D.rows.length}} text rows</p><table><tr><th>FE row</th><th>Prompt</th><th>Scores</th><th>Primary support</th><th>Data</th></tr>${{rows.map(r=>`<tr><td class="nowrap"><a href="${{e(r.fe_url)}}">${{e(r.row_id)}}</a><br>${{e(r.environment)}} · ${{e(r.view_role)}}<br><span class="muted">generation: ${{e(r.generation_status)}}</span></td><td class="prompt">${{e(r.text)}}</td><td>Source ${{r.source_relevance_score}}<br>C-Tech ${{r.ctech_reference_score}}</td><td>${{e(r.primary_support.family)}} · ${{e(r.primary_support.shape)}}<br>“${{e(r.primary_support.phrase)}}”</td><td><details><summary>Full source input/output</summary><h3>Final prompt record</h3><pre>${{e(JSON.stringify(r.prompt_record,null,2))}}</pre><h3>Full source input</h3><pre>${{e(JSON.stringify(D.source_inputs[r.source_input_id],null,2))}}</pre></details></td></tr>`).join('')}}</table>`}};
['env','prod','view','fam','shape'].forEach(id=>document.getElementById(id).onchange=renderRows);document.getElementById('search').oninput=renderRows;renderRows();
</script></main></body></html>'''


def build(
    prompts_path: Path, prompts_sha256: str, run_dir: Path, output: Path,
    source_inputs: dict[str, dict[str, Any]], records: dict[str, dict[str, Any]],
    catalog_path: Path | None = None,
) -> dict[str, Any]:
    document = load(prompts_path.resolve())
    validated = generation.validate_prompt_document(document, prompts_path.resolve(), prompts_sha256)
    run_manifest = load(run_dir.resolve() / "run_manifest.json")
    require(run_manifest.get("prompts_sha256") == prompts_sha256,
            "run manifest prompt hash differs from the distribution input")
    analysis = build_analysis(document, validated, records, source_inputs, prompts_path, prompts_sha256,
                              catalog_path, run_dir.resolve(), run_manifest)
    downloads = output / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    generation.atomic_json(downloads / "analysis.json", analysis)
    shutil.copy2(prompts_path.resolve(), downloads / "prompts_all_160.json")
    if catalog_path:
        shutil.copy2(catalog_path.resolve(), downloads / "approved_prop_catalog.json")
    (output / "index.html").write_text(render_html(analysis), encoding="utf-8")
    artifacts = {}
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item.name != "build_manifest.json"):
        artifacts[str(path.relative_to(output))] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    manifest = {
        "schema_version": "hp-surface-diversity-v6.2-distribution-build-v1",
        "source_prompts": str(prompts_path.resolve()), "source_prompts_sha256": prompts_sha256,
        "run_dir": str(run_dir.resolve()), "output": str(output.resolve()), "artifacts": artifacts,
    }
    generation.atomic_json(output / "build_manifest.json", manifest)
    return analysis


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--prompts-sha256", required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--catalog", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    document = load(args.prompts.resolve())
    validated = generation.validate_prompt_document(document, args.prompts.resolve(), args.prompts_sha256)
    by_id = {row["row_id"]: row for row in validated}
    bank_manifest = load(run_dir / "source/bank_inputs_manifest.json").get("assets", {})
    source_inputs = {case_id: load(Path(item["materialized_path"])) for case_id, item in bank_manifest.items()}
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = load(path)
        row_id = record.get("row_id")
        require(row_id in by_id, f"generation record references an unknown row: {row_id!r}")
        require(row_id not in records, f"duplicate generation record: {row_id}")
        require(record.get("prompt_sha256") == by_id[row_id]["prompt_sha256"],
                f"generation record prompt hash differs for {row_id}")
        records[row_id] = record
    output = args.output.resolve() if args.output else run_dir / "report/distribution"
    analysis = build(args.prompts, args.prompts_sha256, run_dir, output, source_inputs, records, args.catalog)
    print(json.dumps({"output": str(output), "text_rows": analysis["scope"]["text_prompt_rows"],
                      "generated_artifacts": analysis["scope"]["generated_artifact_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
