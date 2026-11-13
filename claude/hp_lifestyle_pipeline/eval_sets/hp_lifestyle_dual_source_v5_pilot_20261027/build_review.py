#!/usr/bin/env python3
"""Build the V5 dual-source text review, exports, and distribution view.

This is a presentation/export step only.  It does not call a model, generate
images, approve candidates, or change the accepted prompt corpus.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_ACCEPTED = HERE / "accepted_prompt_cases.json"
DEFAULT_MANIFEST = HERE / "manifest.json"
DEFAULT_REFERENCES = PROJECT / "research/source_messaging_v1_to_v6/versions/v5/reference_library.json"
DEFAULT_IMS_AUTH = (
    PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
)
DEFAULT_BASELINE = (
    PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/accepted_prompt_cases.json"
)
DEFAULT_PUBLIC_URL = (
    "https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/"
    "eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/gallery/index.html"
)
EXPECTED_ENVIRONMENTS = (
    "Home", "Office", "Education", "Gaming", "Café", "Creative Studio"
)
EXPECTED_CASES = 8
EXPECTED_PER_CASE = 20
TOP_PER_BANK = 6
RUNTIME_FIELDS = {"smart_brief", "source_messaging", "camera_tag"}
SENSITIVE_KEYS = {
    "authorization", "aws_secret_access_key", "aws_session_token", "presignedurl",
    "x-amz-credential", "x-amz-security-token", "x-amz-signature", "x-gw-ims-user-token",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    atomic_bytes(path, value.encode("utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def assert_sanitized(value: Any, location: str = "document") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in SENSITIVE_KEYS:
                raise ValueError(f"Sensitive field reached review export: {location}.{key}")
            assert_sanitized(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_sanitized(child, f"{location}[{index}]")
    elif isinstance(value, str):
        folded = value.casefold()
        if any(marker in folded for marker in ("x-amz-signature=", "x-amz-credential=", "x-amz-security-token=")):
            raise ValueError(f"Presigned credential material reached review export: {location}")


def numeric(value: Any, label: str) -> float:
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} is not numeric")
    number = float(value)
    require(math.isfinite(number) and 0 <= number <= 100, f"{label} must be within 0..100")
    return number


def score_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    """Stable source-first rank for one case/bank."""
    return (
        -numeric(candidate.get("source_relevance_score"), "source_relevance_score"),
        -numeric(candidate.get("ctech_reference_score"), "ctech_reference_score"),
        int(candidate.get("rank", 10**9)) if str(candidate.get("rank", "")).isdigit() else 10**9,
        str(candidate.get("id", "")),
    )


def distribution(values: list[float], width: int = 10) -> list[dict[str, Any]]:
    bins = []
    for low in range(0, 100, width):
        upper = low + width
        final = upper == 100
        count = sum(low <= item <= upper if final else low <= item < upper for item in values)
        bins.append({
            "low": low,
            "upper_exclusive": None if final else upper,
            "high_inclusive": 100 if final else None,
            "label": f"{low}–100" if final else f"{low}–<{upper}",
            "count": count,
        })
    require(sum(item["count"] for item in bins) == len(values), "Score histogram bins must cover every value exactly once")
    return bins


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source = [float(row["source_relevance_score"]) for row in rows]
    ctech = [float(row["ctech_reference_score"]) for row in rows]
    by_view: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_view[row["view_role"]].append(row)
    return {
        "prompt_count": len(rows),
        "environment_counts": dict(sorted(Counter(row["environment"] for row in rows).items())),
        "source_relevance_histogram": distribution(source),
        "ctech_reference_histogram": distribution(ctech),
        "source_relevance_mean": round(sum(source) / len(source), 3) if source else None,
        "ctech_reference_mean": round(sum(ctech) / len(ctech), 3) if ctech else None,
        "by_view": {
            view: {
                "count": len(group),
                "source_relevance_mean": round(sum(float(x["source_relevance_score"]) for x in group) / len(group), 3),
                "ctech_reference_mean": round(sum(float(x["ctech_reference_score"]) for x in group) / len(group), 3),
                "environment_counts": dict(sorted(Counter(x["environment"] for x in group).items())),
            }
            for view, group in sorted(by_view.items())
        },
    }


def resolve_input_path(raw_path: Any, accepted_path: Path, case_id: str) -> Path:
    candidates: list[Path] = []
    if isinstance(raw_path, str) and raw_path:
        supplied = Path(raw_path)
        candidates.append(supplied if supplied.is_absolute() else accepted_path.parent / supplied)
    candidates.append(accepted_path.parent / "inputs" / f"{case_id}.json")
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"Input wrapper missing for {case_id}; checked: {candidates}")


def load_case_inputs(
    accepted_path: Path, accepted: dict[str, Any], manifest: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    manifest_cases = {row["case_id"]: row for row in manifest.get("cases", [])}
    output: dict[str, dict[str, Any]] = {}
    for case_id, case in accepted["cases"].items():
        meta = manifest_cases.get(case_id, {})
        path = resolve_input_path(case.get("input_path") or meta.get("input_path"), accepted_path, case_id)
        payload = read_json(path)
        require(set(payload) == RUNTIME_FIELDS, f"{case_id} input must contain exactly {sorted(RUNTIME_FIELDS)}")
        require(all(isinstance(payload[key], str) for key in RUNTIME_FIELDS), f"{case_id} input fields must be strings")
        expected_sha = case.get("input_sha256") or meta.get("input_sha256")
        if expected_sha:
            require(sha256(path) == expected_sha, f"{case_id} input SHA-256 differs from its record")
        camera_tag = case.get("camera_tag") or meta.get("camera_tag")
        require(payload["camera_tag"] == camera_tag, f"{case_id} camera_tag differs from input wrapper")
        output[case_id] = {
            "path": str(path),
            "sha256": sha256(path),
            **payload,
        }
    return output


def load_references(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    document = read_json(path)
    references = document.get("references") or []
    by_id = {row.get("id"): row for row in references}
    require(len(by_id) == len(references) and None not in by_id, "Reference IDs must be present and unique")
    require(all(isinstance(row.get("text"), str) and row["text"] for row in references), "Reference text missing")
    return by_id, document


def load_review_audit(case_id: str, case: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map final reviewed IDs back to their pre-review normalized R3 rows."""
    raw_log_path = case.get("review_log_path")
    if not isinstance(raw_log_path, str) or not raw_log_path:
        return {}
    log_path = Path(raw_log_path)
    if not log_path.is_file():
        raise FileNotFoundError(f"Review log missing for {case_id}: {log_path}")
    log = read_json(log_path)
    normalized_path = Path(log["normalized_input_path"])
    require(normalized_path.is_file(), f"Pre-review normalized output missing for {case_id}")
    require(sha256(normalized_path) == log["normalized_input_sha256"], f"Pre-review normalized SHA differs for {case_id}")
    normalized = read_json(normalized_path)
    prompts = normalized.get("prompts") or []
    edits = log.get("root_field_edits") or []
    output: dict[str, dict[str, Any]] = {}
    for mapping in (log.get("post_review_finalization") or {}).get("id_map") or []:
        index = mapping.get("original_index")
        final_id = mapping.get("normalized_id")
        require(isinstance(index, int) and 0 <= index < len(prompts), f"Invalid review ID map index for {case_id}")
        require(isinstance(final_id, str) and final_id not in output, f"Invalid final review ID for {case_id}")
        prefix = f"/prompts/{index}/"
        candidate_edits = [item for item in edits if str(item.get("path", "")).startswith(prefix)]
        original = prompts[index]
        output[final_id] = {
            "original_index": index,
            "original_id": mapping.get("original_id"),
            "original_rank": mapping.get("original_rank"),
            "original_text": original.get("text"),
            "field_edits": candidate_edits,
            "review_log_url": f"../review_logs/{log_path.name}",
            "validation_url": f"../validation/{case_id}.json",
            "normalized_output_url": f"../normalized_outputs/{normalized_path.name}",
        }
    require(len(output) == len(prompts), f"Review ID map must cover every prompt for {case_id}")
    return output


def project_rows(
    accepted: dict[str, Any], manifest: dict[str, Any], inputs: dict[str, dict[str, Any]],
    references: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    manifest_cases = {row["case_id"]: row for row in manifest.get("cases", [])}
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for case_id, case in sorted(accepted["cases"].items()):
        meta = manifest_cases.get(case_id, {})
        review_audit = load_review_audit(case_id, case)
        candidates = case.get("candidates") or []
        require(len(candidates) == EXPECTED_PER_CASE, f"{case_id} must contain exactly {EXPECTED_PER_CASE} candidates")
        ordered = sorted(candidates, key=score_key)
        for bank_rank, candidate in enumerate(ordered, 1):
            candidate_id = candidate.get("id")
            require(isinstance(candidate_id, str) and candidate_id, f"{case_id} candidate lacks id")
            candidate_key = candidate.get("candidate_key") or f"{case_id}::{candidate_id}"
            require(candidate_key not in seen, f"Duplicate candidate_key: {candidate_key}")
            seen.add(candidate_key)
            reference_id = candidate.get("ctech_reference_id")
            reference = references.get(reference_id)
            require(reference is not None, f"Unknown C-Tech reference {reference_id!r} for {candidate_key}")
            source_score = numeric(candidate.get("source_relevance_score"), f"{candidate_key}.source_relevance_score")
            ctech_score = numeric(candidate.get("ctech_reference_score"), f"{candidate_key}.ctech_reference_score")
            require(isinstance(candidate.get("text"), str) and candidate["text"].strip(), f"{candidate_key} lacks text")
            environment = candidate.get("environment")
            require(environment in EXPECTED_ENVIRONMENTS, f"Unexpected environment {environment!r} for {candidate_key}")
            view_role = case.get("view_role") or meta.get("view_role")
            require(view_role in {"close_up", "wide"}, f"Unexpected view_role for {case_id}: {view_role!r}")
            camera_tag = case.get("camera_tag") or meta.get("camera_tag")
            audit = review_audit.get(candidate_id, {})
            row = {
                "candidate_key": candidate_key,
                "case_id": case_id,
                "bank_id": case_id,
                "bank_rank_by_source": bank_rank,
                "top6_by_source_in_bank": bank_rank <= TOP_PER_BANK,
                "candidate_id": candidate_id,
                "model_rank": candidate.get("rank"),
                "pair_id": case.get("pair_id") or meta.get("pair_id") or case_id.split("__", 1)[0],
                "group_id": case.get("group_id") or meta.get("group_id"),
                "device_type": case.get("device_type") or meta.get("device_type"),
                "view_role": view_role,
                "camera_tag": camera_tag,
                "tag": camera_tag,
                "environment": environment,
                "subsetting": candidate.get("subsetting"),
                "text": candidate["text"],
                "source_relevance_score": source_score,
                "source_relationship": candidate.get("relationship"),
                "source_score_components": candidate.get("score_components") or {},
                "source_explanation": candidate.get("explanation"),
                "source_evidence_ids": candidate.get("evidence_ids") or [],
                "creative_departures": candidate.get("creative_departures") or [],
                "ctech_reference_id": reference_id,
                "ctech_reference_environment": reference.get("environment"),
                "ctech_reference_source": reference.get("source"),
                "ctech_reference_text": reference["text"],
                "ctech_reference_score": ctech_score,
                "ctech_relationship": candidate.get("ctech_relationship"),
                "ctech_changes": candidate.get("ctech_changes") or [],
                "ctech_explanation": candidate.get("ctech_explanation"),
                "smart_brief": inputs[case_id]["smart_brief"],
                "source_messaging": inputs[case_id]["source_messaging"],
                "input_path": inputs[case_id]["path"],
                "input_sha256": inputs[case_id]["sha256"],
                "case_status": case.get("status"),
                "human_review_status": case.get("human_review_status", meta.get("human_review_status", "pending")),
                "launchable": case.get("launchable", meta.get("launchable", False)),
                "case_debug": case.get("debug") or {},
                "candidate_debug": candidate.get("debug") or {},
                "review_original_r3_id": audit.get("original_id"),
                "review_original_r3_rank": audit.get("original_rank"),
                "review_original_r3_text": audit.get("original_text"),
                "review_text_changed": bool(audit) and audit.get("original_text") != candidate["text"],
                "review_field_edits": audit.get("field_edits") or [],
                "review_log_url": audit.get("review_log_url"),
                "validation_url": audit.get("validation_url"),
                "normalized_output_url": audit.get("normalized_output_url"),
            }
            rows.append(row)
    require(len(rows) == EXPECTED_CASES * EXPECTED_PER_CASE, f"Expected 160 candidates, found {len(rows)}")
    return rows


def export_document(
    rows: list[dict[str, Any]], accepted: dict[str, Any], accepted_path: Path,
    manifest_path: Path, reference_path: Path, selection: str,
) -> dict[str, Any]:
    return {
        "version": "hp-lifestyle-dual-source-v5-review-export-v1",
        "selection": selection,
        "text_only": True,
        "image_generation_included": False,
        "status": accepted.get("status"),
        "selection_status": accepted.get("selection_status"),
        "review_disclosure": accepted.get("review_disclosure"),
        "human_review_statuses": sorted({str(row["human_review_status"]) for row in rows}),
        "prompt_count": len(rows),
        "bank_count": len({row["bank_id"] for row in rows}),
        "provenance": {
            "accepted_prompt_cases": {"path": str(accepted_path), "sha256": sha256(accepted_path)},
            "manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
            "reference_library": {"path": str(reference_path), "sha256": sha256(reference_path)},
        },
        "prompts": rows,
    }


def text_export(document: dict[str, Any]) -> str:
    lines = [
        "HP lifestyle dual-source V5 pilot — text-only prompt export",
        f"Selection: {document['selection']}",
        f"Source status: {document.get('status')}",
        f"Human review statuses: {', '.join(document['human_review_statuses'])}",
        f"Prompt count: {document['prompt_count']}",
        "Metrics: model-authored rubric judgments; not embeddings and not image-quality measurements.",
        "",
    ]
    for row in document["prompts"]:
        lines.extend([
            f"[{row['candidate_key']}]",
            f"Case: {row['case_id']}",
            f"Tag: {row['camera_tag']}",
            f"Source rank in bank: {row['bank_rank_by_source']}",
            f"Source relevance score: {row['source_relevance_score']}",
            f"C-Tech reference score: {row['ctech_reference_score']}",
            f"Prompt: {row['text']}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def prompts_only_document(rows: list[dict[str, Any]], accepted: dict[str, Any]) -> dict[str, Any]:
    """Compact source-ranked export for prompt consumers."""
    prompts = [{
        "id": row["candidate_id"],
        "candidate_key": row["candidate_key"],
        "case_id": row["case_id"],
        "camera_tag": row["camera_tag"],
        "bank_rank_by_source": row["bank_rank_by_source"],
        "text": row["text"],
        "source_relevance_score": row["source_relevance_score"],
        "ctech_reference_score": row["ctech_reference_score"],
    } for row in rows]
    return {
        "version": "hp-lifestyle-dual-source-v5-prompts-only-v1",
        "status": accepted.get("status"),
        "ordering": "case_id ascending; within each bank source relevance descending, C-Tech score descending, existing rank stable",
        "prompt_count": len(prompts),
        "prompts": prompts,
    }


def non_candidate_review_edits(accepted: dict[str, Any]) -> list[dict[str, Any]]:
    """Preserve review edits outside candidate records, such as evidence fixes."""
    output = []
    for case_id, case in sorted(accepted["cases"].items()):
        raw_path = case.get("review_log_path")
        if not raw_path:
            continue
        for edit in read_json(Path(raw_path)).get("root_field_edits") or []:
            if not str(edit.get("path", "")).startswith("/prompts/"):
                output.append({"case_id": case_id, **edit})
    return output


def baseline_summary(path: Path | None, reference_ids: set[str]) -> dict[str, Any]:
    if path is None:
        return {
            "included": False,
            "label": "V4.1 frozen 120 baseline not included",
            "caveat": "Add --baseline to include a descriptive comparison. V5 uses different inputs, so no causal claim is supported.",
        }
    document = read_json(path)
    rows = []
    for case_id, case in sorted((document.get("cases") or {}).items()):
        for candidate in case.get("candidates") or []:
            if candidate.get("ctech_reference_id") not in reference_ids:
                continue
            rows.append({
                "candidate_key": candidate.get("candidate_key") or f"{case_id}::{candidate.get('id')}",
                "environment": candidate.get("environment"),
                "view_role": case.get("view_role"),
                "source_relevance_score": numeric(candidate.get("source_relevance_score"), "baseline source score"),
                "ctech_reference_score": numeric(candidate.get("ctech_reference_score"), "baseline C-Tech score"),
            })
    require(len(rows) == 120, f"Optional V4.1 baseline must contain 120 usable prompts, found {len(rows)}")
    return {
        "included": True,
        "label": "V4.1 frozen 120 baseline — different inputs",
        "path": str(path),
        "sha256": sha256(path),
        "caveat": "Descriptive context only. The V5 smart briefs/source messaging and case inventory differ, so deltas do not support causal claims.",
        "summary": summarize_rows(rows),
    }


HTML_TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HP dual-source V5 text review</title>
<style>
:root{color-scheme:dark;--bg:#0a0b0e;--panel:#151820;--line:#2b3040;--muted:#a5adbd;--ink:#f5f7fb;--accent:#66e2c4;--purple:#b3a2ff;--warn:#ffd37a;--bad:#ff8b8b}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,sans-serif}a{color:var(--accent)}button,select,input{font:inherit;color:var(--ink);background:#202531;border:1px solid #3c4357;border-radius:7px;padding:8px}button{cursor:pointer}.hidden{display:none!important}#ims{padding:7px 18px;background:#10131a;color:var(--muted);font-size:12px}.ims-button{padding:3px 8px;margin-left:8px}.loading{padding:40px}.wrap{max-width:1600px;margin:auto;padding:26px}.hero{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:start}.eyebrow{text-transform:uppercase;letter-spacing:.13em;color:var(--accent);font-size:11px;font-weight:800;margin:0 0 5px}.hero h1{font-size:34px;line-height:1.08;margin:0 0 10px}.lede{max-width:870px;color:var(--muted);font-size:16px}.downloads{display:flex;flex-direction:column;gap:6px}.banner{margin:20px 0;padding:14px 16px;border:1px solid #725d26;background:#251f10;color:#ffe3a1;border-radius:9px;font-weight:700}.tabs{display:flex;gap:8px;margin:18px 0}.tab.active{border-color:var(--accent);color:var(--accent)}.panel{border:1px solid var(--line);background:var(--panel);border-radius:11px;padding:17px;margin:14px 0}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.kpi{background:#11141a;border:1px solid var(--line);border-radius:9px;padding:13px}.kpi strong{display:block;font-size:24px}.kpi span,.note{color:var(--muted);font-size:12px}.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:end}.controls label{display:grid;gap:4px;color:var(--muted);font-size:12px}.count{margin-left:auto;color:var(--muted)}.row{border-top:1px solid var(--line);padding:14px 0}.row:first-child{border-top:0}.row-head{display:grid;grid-template-columns:minmax(260px,1fr) auto;gap:16px}.prompt{font-size:16px;margin:8px 0}.pills{display:flex;gap:6px;flex-wrap:wrap}.pill{padding:3px 7px;border-radius:999px;background:#242a36;color:#dbe2ee;font-size:11px}.score{min-width:105px;text-align:right}.score b{display:block}.score .src{color:var(--accent)}.score .ct{color:var(--purple)}details{margin-top:8px}summary{cursor:pointer;color:#d9deea;font-weight:650}.detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.detail{background:#10131a;border-radius:8px;padding:12px;overflow:auto}.detail.full{grid-column:1/-1}.detail h4{margin:0 0 7px;color:var(--muted)}pre{white-space:pre-wrap;word-break:break-word;margin:0;font:12px/1.45 ui-monospace,SFMono-Regular,monospace}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.bars{display:grid;gap:7px}.barrow{display:grid;grid-template-columns:130px 1fr 40px;gap:8px;align-items:center}.bar{height:12px;background:#252b38;border-radius:99px;overflow:hidden}.bar i{display:block;height:100%;background:var(--accent)}svg{display:block;width:100%;height:auto;background:#10131a;border-radius:8px}.legend{color:var(--muted);font-size:12px}.viewtable{width:100%;border-collapse:collapse}.viewtable th,.viewtable td{padding:7px;border-bottom:1px solid var(--line);text-align:left}.caveat{border-left:3px solid var(--warn);padding-left:11px;color:#f7dfa8}@media(max-width:800px){.hero,.grid,.detail-grid{grid-template-columns:1fr}.downloads{flex-direction:row;flex-wrap:wrap}.detail.full{grid-column:auto}.row-head{grid-template-columns:1fr}.score{text-align:left}.barrow{grid-template-columns:90px 1fr 32px}}
</style></head><body>
<div id="ims"></div><div id="loading" class="loading">Loading V5 text review…</div>
<main id="content" class="hidden"><div class="wrap">
<header class="hero"><div><p class="eyebrow">HP lifestyle writer · dual-source V5 pilot</p><h1>Text-only prompt review</h1><p class="lede">Eight smart-brief + source-messaging banks, close and wide, with model-authored source-relevance and C-Tech rubric judgments. There are no generated images and no image-quality measurements in this report.</p><p><a href="#distribution">Jump to distribution</a></p></div><nav class="downloads"><a href="../data/prompts_only.json">Prompts-only JSON</a><a href="../data/prompts_all.json">Full prompts JSON</a><a href="../data/prompts_all.txt">Prompts TXT</a><a href="../data/prompts_top6_per_bank.json">Top 6/bank JSON</a><a href="../data/prompts_top6_per_bank.txt">Top 6/bank TXT</a><a href="../data/review_data.json">Review data JSON</a><a href="../manifest.json">Run manifest</a><a href="../reviewed_prompt_cases.json">Reviewed corpus</a><a href="../status_inventory.json">Model-run status</a><a href="../runtime/system_prompt.md">V5 system prompt</a></nav></header>
<div class="banner" id="truthBanner"></div>
<div class="panel" id="reviewDisclosure"></div>
<div class="tabs"><button class="tab active" data-tab="review">Prompt review</button><button class="tab" data-tab="distribution">Distribution</button></div>
<section id="reviewTab"><div class="panel controls"><label>Case / bank<select id="caseFilter"><option value="all">All cases</option></select></label><label>Environment<select id="envFilter"><option value="all">All environments</option></select></label><label>View<select id="viewFilter"><option value="all">Close + wide</option><option value="close_up">Close-up</option><option value="wide">Wide</option></select></label><label>Within-bank order<select id="sortOrder"><option value="source">Source relevance ↓</option><option value="ctech">C-Tech score ↓</option></select></label><label>Bank selection<select id="topFilter"><option value="all">All 20 / bank</option><option value="top6">Top 6 / bank by source rank</option></select></label><span class="count" id="rowCount"></span></div><div class="panel" id="rows"></div></section>
<section id="distributionTab" class="hidden"><div class="kpis" id="kpis"></div><div class="grid"><article class="panel"><p class="eyebrow">Six-category taxonomy</p><h2>Environment counts</h2><div id="envBars"></div></article><article class="panel"><p class="eyebrow">Rubric judgments</p><h2>Score histograms</h2><h3>Source relevance</h3><div id="sourceHist"></div><h3>C-Tech reference</h3><div id="ctechHist"></div></article></div><article class="panel"><p class="eyebrow">Rubric relationship</p><h2>Source relevance × C-Tech score</h2><div id="scatter"></div><p class="note">Each point is a prompt. These coordinates are model-authored rubric judgments, not embeddings and not image-quality measurements. Green = close-up; purple = wide.</p></article><article class="panel"><p class="eyebrow">Close / wide</p><h2>View summary</h2><div id="viewSummary"></div></article><article class="panel"><p class="eyebrow">Optional historical context</p><h2>V4.1 frozen 120 baseline</h2><div id="baseline"></div></article></section>
</div></main>
<script id="review-data" type="application/json">__REVIEW_DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('review-data').textContent);const $=id=>document.getElementById(id);const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function onAuthReady(){renderAll()}function addOptions(id,values){$(id).innerHTML+=[...values].sort().map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('')}
function fmtObj(value){return esc(JSON.stringify(value??{},null,2))}function rowHtml(r){let auditLinks=r.review_log_url?`<p><a href="${esc(r.review_log_url)}">Case review log</a> · <a href="${esc(r.validation_url)}">Validator audit</a> · <a href="${esc(r.normalized_output_url)}">Pre-review normalized output</a></p>`:'';let editBadge=r.review_text_changed?'<span class="pill" style="color:#ffd37a">Root text edit</span>':'';let fieldBadge=r.review_field_edits.length?`<span class="pill">${r.review_field_edits.length} logged field edits</span>`:'';let comparison=r.review_original_r3_text!=null?`<section class="detail"><h4>Pre-review normalized R3 prompt · ${esc(r.review_original_r3_id)}</h4><pre>${esc(r.review_original_r3_text)}</pre></section><section class="detail"><h4>Reviewed prompt · ${esc(r.candidate_id)}</h4><pre>${esc(r.text)}</pre></section><section class="detail full"><h4>Logged candidate corrections</h4>${auditLinks}<pre>${fmtObj(r.review_field_edits)}</pre></section>`:'';return `<article class="row"><div class="row-head"><div><div class="pills"><span class="pill">${esc(r.case_id)}</span><span class="pill">${esc(r.environment)}</span><span class="pill">${esc(r.view_role)}</span><span class="pill">${esc(r.camera_tag)}</span><span class="pill">bank rank ${r.bank_rank_by_source}</span><span class="pill">review: ${esc(r.human_review_status)}</span>${editBadge}${fieldBadge}</div><p class="prompt">${esc(r.text)}</p><span class="note">${esc(r.candidate_key)} · ${esc(r.subsetting)}</span></div><div class="score"><b class="src">Source ${r.source_relevance_score}</b><b class="ct">C-Tech ${r.ctech_reference_score}</b><span>${esc(r.ctech_reference_id)}</span></div></div><details><summary>Review audit, full inputs, reference, explanations, and debug</summary><div class="detail-grid">${comparison}<section class="detail"><h4>Source judgment</h4><p>${esc(r.source_explanation)}</p><pre>${fmtObj(r.source_score_components)}</pre><p>${esc(r.source_relationship)}</p></section><section class="detail"><h4>C-Tech judgment</h4><p>${esc(r.ctech_explanation)}</p><pre>${fmtObj(r.ctech_changes)}</pre><p>${esc(r.ctech_relationship)}</p></section><section class="detail full"><h4>Full C-Tech reference · ${esc(r.ctech_reference_id)}</h4><pre>${esc(r.ctech_reference_text)}</pre></section><section class="detail full"><h4>Full smart brief</h4><pre>${esc(r.smart_brief)}</pre></section><section class="detail full"><h4>Full source messaging</h4><pre>${esc(r.source_messaging)}</pre></section><section class="detail"><h4>Case/debug/status</h4><pre>${fmtObj({tag:r.tag,case_status:r.case_status,human_review_status:r.human_review_status,launchable:r.launchable,debug:r.case_debug})}</pre></section><section class="detail"><h4>Candidate debug</h4><pre>${fmtObj(r.candidate_debug)}</pre></section></div></details></article>`}
function filtered(){let rows=DATA.rows.filter(r=>($('caseFilter').value==='all'||r.case_id===$('caseFilter').value)&&($('envFilter').value==='all'||r.environment===$('envFilter').value)&&($('viewFilter').value==='all'||r.view_role===$('viewFilter').value)&&($('topFilter').value==='all'||r.top6_by_source_in_bank));let mode=$('sortOrder').value;return rows.sort((a,b)=>a.case_id.localeCompare(b.case_id)||(mode==='ctech'?b.ctech_reference_score-a.ctech_reference_score||b.source_relevance_score-a.source_relevance_score:a.bank_rank_by_source-b.bank_rank_by_source)||a.candidate_key.localeCompare(b.candidate_key))}
function renderRows(){let rows=filtered();$('rowCount').textContent=`${rows.length} prompts`;$('rows').innerHTML=rows.map(rowHtml).join('')||'<p>No prompts match these filters.</p>'}
function bars(id,items,color='#66e2c4'){let max=Math.max(1,...items.map(x=>x.count));$(id).className='bars';$(id).innerHTML=items.map(x=>`<div class="barrow"><span>${esc(x.label)}</span><span class="bar"><i style="width:${100*x.count/max}%;background:${color}"></i></span><b>${x.count}</b></div>`).join('')}
function scatter(){let W=760,H=470,p=55,rows=DATA.rows;let lines=[`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Source and C-Tech score scatter plot">`];for(let n=0;n<=100;n+=20){let x=p+(W-2*p)*n/100,y=H-p-(H-2*p)*n/100;lines.push(`<line x1="${x}" y1="${p}" x2="${x}" y2="${H-p}" stroke="#272d39"/><line x1="${p}" y1="${y}" x2="${W-p}" y2="${y}" stroke="#272d39"/><text x="${x}" y="${H-20}" text-anchor="middle" fill="#a5adbd" font-size="11">${n}</text><text x="25" y="${y+4}" fill="#a5adbd" font-size="11">${n}</text>`)}lines.push(`<text x="${W/2}" y="${H-3}" text-anchor="middle" fill="#a5adbd">Source relevance score</text><text transform="translate(13 ${H/2}) rotate(-90)" text-anchor="middle" fill="#a5adbd">C-Tech score</text>`);rows.forEach(r=>{let x=p+(W-2*p)*r.source_relevance_score/100,y=H-p-(H-2*p)*r.ctech_reference_score/100,c=r.view_role==='wide'?'#b3a2ff':'#66e2c4';lines.push(`<circle cx="${x}" cy="${y}" r="4" fill="${c}" fill-opacity=".72"><title>${esc(r.candidate_key)} · ${esc(r.environment)} · source ${r.source_relevance_score} · C-Tech ${r.ctech_reference_score}</title></circle>`)});lines.push('</svg>');$('scatter').innerHTML=lines.join('')}
function renderDistribution(){let s=DATA.summary;$('kpis').innerHTML=[[s.prompt_count,'V5 prompts'],[DATA.bank_count,'prompt banks'],[Object.keys(s.environment_counts).length,'environments'],[s.source_relevance_mean,'mean source score'],[s.ctech_reference_mean,'mean C-Tech score']].map(x=>`<div class="kpi"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></div>`).join('');bars('envBars',Object.entries(s.environment_counts).map(([label,count])=>({label,count})));bars('sourceHist',s.source_relevance_histogram,'#66e2c4');bars('ctechHist',s.ctech_reference_histogram,'#b3a2ff');scatter();$('viewSummary').innerHTML=`<table class="viewtable"><thead><tr><th>View</th><th>Prompts</th><th>Mean source</th><th>Mean C-Tech</th><th>Environment counts</th></tr></thead><tbody>${Object.entries(s.by_view).map(([view,x])=>`<tr><td>${esc(view)}</td><td>${x.count}</td><td>${x.source_relevance_mean}</td><td>${x.ctech_reference_mean}</td><td>${esc(JSON.stringify(x.environment_counts))}</td></tr>`).join('')}</tbody></table>`;let b=DATA.baseline;$('baseline').innerHTML=b.included?`<p class="caveat"><strong>${esc(b.label)}</strong><br>${esc(b.caveat)}</p><table class="viewtable"><tr><th>Corpus</th><th>Prompts</th><th>Mean source</th><th>Mean C-Tech</th></tr><tr><td>V5 pilot</td><td>${s.prompt_count}</td><td>${s.source_relevance_mean}</td><td>${s.ctech_reference_mean}</td></tr><tr><td>V4.1 frozen baseline</td><td>${b.summary.prompt_count}</td><td>${b.summary.source_relevance_mean}</td><td>${b.summary.ctech_reference_mean}</td></tr></table>`:`<p class="caveat">${esc(b.label)}. ${esc(b.caveat)}</p>`}
function showTab(name,updateHash=true){document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x.dataset.tab===name));$('reviewTab').classList.toggle('hidden',name!=='review');$('distributionTab').classList.toggle('hidden',name!=='distribution');if(updateHash)history.replaceState(null,'',name==='distribution'?'#distribution':'#review')}
function disclosureHtml(){let value=DATA.review_disclosure,counts=DATA.review_counts||{};let summary=`<div class="kpis"><div class="kpi"><strong>${counts.scene_texts_edited??'—'}</strong><span>scene texts edited</span></div><div class="kpi"><strong>${counts.field_edits??'—'}</strong><span>logged field edits</span></div><div class="kpi"><strong>${counts.model_normalized_validation_passes??'—'} / ${counts.cases??'—'}</strong><span>model banks passed pre-review</span></div><div class="kpi"><strong>${counts.reviewed_validation_passes??'—'} / ${counts.cases??'—'}</strong><span>reviewed banks pass</span></div></div>`;let links='<p><a href="../reviewed_prompt_cases.json">Reviewed corpus</a> · <a href="../status_inventory.json">Model-run status</a> · <a href="../manifest.json">Run manifest</a></p>';let byCase=new Map;DATA.rows.forEach(r=>{if(!byCase.has(r.case_id))byCase.set(r.case_id,r)});let audits=`<details open><summary>Case audit files</summary><div class="detail-grid">${[...byCase.values()].map(r=>`<section class="detail"><h4>${esc(r.case_id)}</h4><a href="${esc(r.review_log_url)}">Review log</a> · <a href="${esc(r.validation_url)}">Validator audit</a> · <a href="${esc(r.normalized_output_url)}">Pre-review normalized output</a></section>`).join('')}</div></details>`;let extra=DATA.non_candidate_review_edits?.length?`<details open><summary>${DATA.non_candidate_review_edits.length} additional case/debug corrections</summary><pre>${fmtObj(DATA.non_candidate_review_edits)}</pre></details>`:'';if(!value)return summary+'<p><strong>Review disclosure:</strong> none supplied with the reviewed corpus.</p>'+links+extra+audits;if(typeof value==='string')return summary+`<p><strong>Review disclosure:</strong> ${esc(value)}</p>`+links+extra+audits;return summary+`<details open><summary>Review disclosure</summary><pre>${fmtObj(value)}</pre></details>`+links+extra+audits}
function renderAll(){if(window.__rendered)return;window.__rendered=true;let pending=DATA.human_review_statuses.some(x=>String(x).toLowerCase().includes('pending'))||String(DATA.source_status).toLowerCase().includes('review');let reviewLabel=pending?'Human review required':'Human review status recorded';$('truthBanner').textContent=`TEXT-ONLY REVIEW · NO GENERATED IMAGES · ${reviewLabel} · ${DATA.launchable_true_count} of ${DATA.rows.length} prompts marked launchable`;$('reviewDisclosure').innerHTML=disclosureHtml();addOptions('caseFilter',new Set(DATA.rows.map(x=>x.case_id)));addOptions('envFilter',new Set(DATA.rows.map(x=>x.environment)));['caseFilter','envFilter','viewFilter','sortOrder','topFilter'].forEach(id=>$(id).addEventListener('change',renderRows));document.querySelectorAll('.tab').forEach(btn=>btn.onclick=()=>showTab(btn.dataset.tab));window.addEventListener('hashchange',()=>showTab(location.hash==='#distribution'?'distribution':'review',false));renderRows();renderDistribution();showTab(location.hash==='#distribution'?'distribution':'review',false)}
document.addEventListener('DOMContentLoaded',()=>{if(location.protocol==='file:'){document.getElementById('loading').style.display='none';document.getElementById('content').classList.remove('hidden');renderAll()}else if(typeof initializeIMS==='function')initializeIMS();else{document.getElementById('loading').style.display='none';document.getElementById('content').classList.remove('hidden');renderAll()}});
</script>
<script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script><script src="./imsauth.js"></script>
</body></html>'''


def embedded_json(value: Any) -> str:
    # Prevent source text from terminating the application/json script element.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build(args: argparse.Namespace) -> dict[str, Any]:
    accepted_path = args.accepted.resolve()
    manifest_path = args.manifest.resolve()
    reference_path = args.references.resolve()
    output_root = args.output_root.resolve()
    for label, path in (("accepted prompt cases", accepted_path), ("manifest", manifest_path), ("reference library", reference_path)):
        if not path.is_file():
            raise FileNotFoundError(f"{label} missing: {path}")
    accepted = read_json(accepted_path)
    manifest = read_json(manifest_path)
    require(isinstance(accepted.get("cases"), dict), "accepted_prompt_cases.json lacks a cases object")
    require(len(accepted["cases"]) == EXPECTED_CASES, f"Expected {EXPECTED_CASES} cases, found {len(accepted['cases'])}")
    inputs = load_case_inputs(accepted_path, accepted, manifest)
    references, reference_document = load_references(reference_path)
    rows = project_rows(accepted, manifest, inputs, references)
    assert_sanitized(rows)
    environments = Counter(row["environment"] for row in rows)
    require(set(environments) == set(EXPECTED_ENVIRONMENTS), f"Expected all six environments, found {sorted(environments)}")
    top_rows = [row for row in rows if row["top6_by_source_in_bank"]]
    require(len(top_rows) == EXPECTED_CASES * TOP_PER_BANK, f"Expected 48 top-six rows, found {len(top_rows)}")
    all_doc = export_document(rows, accepted, accepted_path, manifest_path, reference_path, "all_20_per_bank")
    top_doc = export_document(top_rows, accepted, accepted_path, manifest_path, reference_path, "top_6_per_bank_by_source_relevance")
    compact_doc = prompts_only_document(rows, accepted)
    baseline = baseline_summary(args.baseline.resolve() if args.baseline else None, set(references))
    review_data = {
        "version": "hp-lifestyle-dual-source-v5-review-data-v1",
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "text_only": True,
        "no_generation_column": True,
        "metrics_interpretation": "Rubric judgments, not embeddings or image-quality measurements. Source scoring uses equal authority: sum the strongest supported value for each component across both documents; no average or sparse-document penalty.",
        "source_status": accepted.get("status"),
        "selection_status": accepted.get("selection_status"),
        "review_disclosure": accepted.get("review_disclosure"),
        "review_counts": accepted.get("counts") or {},
        "non_candidate_review_edits": non_candidate_review_edits(accepted),
        "human_review_statuses": sorted({str(row["human_review_status"]) for row in rows}),
        "launchable_true_count": sum(row["launchable"] is True for row in rows),
        "bank_count": len({row["bank_id"] for row in rows}),
        "top_per_bank": TOP_PER_BANK,
        "public_url_if_published": args.public_url,
        "summary": summarize_rows(rows),
        "baseline": baseline,
        "reference_library": reference_document,
        "rows": rows,
    }
    assert_sanitized(review_data)
    files = {
        "data/prompts_only.json": (json.dumps(compact_doc, ensure_ascii=False, indent=2) + "\n").encode(),
        "data/prompts_all.json": (json.dumps(all_doc, ensure_ascii=False, indent=2) + "\n").encode(),
        "data/prompts_all.txt": text_export(all_doc).encode(),
        "data/prompts_top6_per_bank.json": (json.dumps(top_doc, ensure_ascii=False, indent=2) + "\n").encode(),
        "data/prompts_top6_per_bank.txt": text_export(top_doc).encode(),
        "data/review_data.json": (json.dumps(review_data, ensure_ascii=False, indent=2) + "\n").encode(),
        "gallery/index.html": HTML_TEMPLATE.replace("__REVIEW_DATA__", embedded_json(review_data)).encode(),
        "gallery/imsauth.js": args.ims_auth.read_bytes(),
    }
    for relative, payload in files.items():
        atomic_bytes(output_root / relative, payload)
    artifact_records = {
        relative: {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}
        for relative, payload in files.items()
    }
    build_manifest = {
        "version": "hp-lifestyle-dual-source-v5-review-build-v1",
        "status": "built_text_only_review_artifacts",
        "source_status": accepted.get("status"),
        "human_review_statuses": review_data["human_review_statuses"],
        "image_generation_performed": False,
        "output_root": str(output_root),
        "public_url_if_published": args.public_url,
        "counts": {"cases": EXPECTED_CASES, "all_prompts": len(rows), "top6_prompts": len(top_rows), "environments": len(environments)},
        "artifacts": artifact_records,
    }
    atomic_json(output_root / "build_manifest.json", build_manifest)
    return build_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted", type=Path, default=DEFAULT_ACCEPTED)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--references", type=Path, default=DEFAULT_REFERENCES)
    parser.add_argument("--output-root", type=Path, default=HERE)
    parser.add_argument("--ims-auth", type=Path, default=DEFAULT_IMS_AUTH)
    parser.add_argument("--baseline", type=Path, help=f"Optional different-input V4.1 frozen 120 comparison (usual path: {DEFAULT_BASELINE})")
    parser.add_argument("--public-url", default=DEFAULT_PUBLIC_URL)
    return parser.parse_args()


if __name__ == "__main__":
    result = build(parse_args())
    print(json.dumps(result, ensure_ascii=False, indent=2))
