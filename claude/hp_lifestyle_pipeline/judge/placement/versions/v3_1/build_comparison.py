"""Audit fresh raw evidence and render the V3/V3.1 side-by-side JSON and local HTML."""
from __future__ import annotations

import argparse
import collections
import html
import json
from datetime import datetime, timezone
from pathlib import Path

import run_judge as updated
import frozen_v3
import calibrate_anchors

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / "evaluation"
ANCHOR_LABELS = {
    "07_cashmere_x_Front_Wide_1": "C-Tech: must not fail placement/chair alignment; not a global positive label for unrelated dimensions.",
    "07_cashmere_x_Front_Wide_4": "C-Tech: must fail for consequential laptop/table misalignment, independently of chair alignment.",
    "13_elitebook_13_Front_Left_Medium_4": "C-Tech: no product-placement failure, but fail for hallucinated table form/extra legs. Astra could not corroborate this geometry allegation from the exact attachment; preserve that disagreement.",
}


def audit_case(version, record):
    folder = FOLDER / "runs" / version / record["id"]
    path = folder / "result.json"
    if not path.exists():
        error = folder / "error.json"
        return {
            "ok": False, "status": "error" if error.exists() else "pending",
            "verdict": None, "score": None, "confidence": None, "components": None,
            "result_path": None,
            "error": json.loads(error.read_text()) if error.exists() else None,
        }, []
    result = json.loads(path.read_text())
    if result["protocol_freeze_sha256"] != updated.verify_freeze():
        raise ValueError("Ensemble protocol hash mismatch")
    runtime = result["runtime_input"]
    expected = {key: record[key] for key in ("product_type", "scene_prompt")}
    expected["image_stage"] = "scene_generation"
    for key in ("generated_image", "twin_image"):
        expected[key] = record[key]["local_path"]
        if updated.sha(expected[key]) != record[key]["sha256"]:
            raise ValueError("Target image differs from inventory")
    if runtime != expected or set(runtime) != updated.INPUT_KEYS:
        raise ValueError("Ensemble runtime-input identity mismatch")
    stages, calls = {}, []
    for stage, artifact in result["stages"].items():
        stage_path = Path(artifact["path"])
        if updated.sha(stage_path) != artifact["sha256"]:
            raise ValueError("Stage hash differs from ensemble source binding")
        saved = json.loads(stage_path.read_text())
        request = json.loads((stage_path.parent / "request.json").read_text())
        raw_path = stage_path.parent / "response.json"
        raw = json.loads(raw_path.read_text())
        choice = raw["choices"][0]
        if not updated.identity_matches(raw.get("model")) or choice["finish_reason"] != "stop":
            raise ValueError("Unexpected model identity or incomplete response")
        if choice["message"].get("refusal"):
            raise ValueError("Model refusal")
        value = json.loads(choice["message"]["content"])
        original = (saved.get("observation") or saved.get("assessment")
                    or saved.get("judgment", {}).get("observation"))
        if not saved["ok"] or value != original:
            raise ValueError("Raw observation was edited or stage failed")
        if request.get("runtime_input", request.get("input")) != runtime:
            raise ValueError("Stage is not bound to target runtime input")
        for key in ("generated_image", "twin_image"):
            image = request["images"][key]
            if image["sha256"] != record[key]["sha256"]:
                raise ValueError("Stage image hash differs")
        if request["model_requested"] != "gpt-5.5" or request["reasoning_effort"] != "high":
            raise ValueError("Stage model configuration mismatch")
        if stage == "independent":
            if request.get("proposals") is not None or request.get("proposed_components"):
                raise ValueError("Names-only check received accusations")
        if version == "v3":
            prompt = (frozen_v3.V2 / "system_prompt.md" if stage == "baseline"
                      else frozen_v3.V3 / "system_prompt.md" if stage == "compact"
                      else frozen_v3.PROPOSAL.PROMPT_PATH if stage == "proposal"
                      else frozen_v3.INDEPENDENT.PROMPT_PATH)
            if stage == "baseline":
                frozen_v3.V2_SCORING.validate_observation(value)
            elif stage == "compact":
                updated.SCORING.validate_observation(value)
            else:
                module = frozen_v3.PROPOSAL if stage == "proposal" else frozen_v3.INDEPENDENT
                names = list(value["components"])
                module.validate_response(value, module.response_schema(names), names)
        else:
            prompt = ROOT / "prompts" / f"{stage}.md"
            if stage in {"baseline", "compact"}:
                updated.validate_new_observation(value)
            else:
                updated.validate_components(value, updated.component_schema(list(value["components"])))
        if request["system_prompt_sha256"] != updated.sha(prompt):
            raise ValueError("Stage rubric differs from correct version")
        stages[stage] = value
        calls.append({"id": record["id"], "version": version, "stage": stage,
                      "model": raw["model"], "response_path": str(raw_path),
                      "response_sha256": updated.sha(raw_path)})
    aggregator = frozen_v3.aggregate if version == "v3" else updated.aggregate_stages
    recomputed = aggregator(stages["baseline"], stages["compact"],
                           stages.get("proposal"), stages.get("independent"))
    if any(result[key] != value for key, value in recomputed.items()):
        raise ValueError("Deterministic ensemble recomputation differs")
    judgment, decision = result["application_merged_judgment"], result["final_decision"]
    return {
        "ok": True, "status": "complete", "verdict": decision["verdict"],
        "score": judgment["natural_placement_score"],
        "confidence": decision["reported_overall_confidence"],
        "components": judgment["observation"]["components"],
        "scene_reading": judgment["observation"]["scene_reading"],
        "coverage": judgment["coverage"], "verdict_reasons": decision["verdict_reasons"],
        "uncertainty_notes": decision["uncertainty_notes"],
        "triggered_components": result["triggered_components"],
        "consensus_resolution": result["consensus_resolution"],
        "result_path": str(path), "result_sha256": updated.sha(path), "error": None,
    }, calls


def card(version, value):
    esc = html.escape
    if not value["ok"]:
        return f"<div><h3>{version}: {esc(value['status'])}</h3><pre>{esc(json.dumps(value['error'], indent=2))}</pre></div>"
    rows = []
    for dimension, comp in value["components"].items():
        rows.append(
            f"<tr><td>{esc(dimension)}</td><td>{comp['severity']}</td>"
            f"<td>{esc(comp['visibility'])} / {esc(comp['confidence'])}</td>"
            f"<td>{esc(', '.join(comp['issue_codes']))}</td>"
            f"<td>{esc(comp['evidence'])}<br>{esc(comp['consequence'])}</td></tr>")
    return (
        f"<div><h3>{version}: {esc(value['verdict'])} / {value['score']}</h3>"
        f"<p>Confidence {esc(value['confidence'])}; coverage {value['coverage']}</p>"
        f"<p>{esc(' | '.join(value['verdict_reasons'] + value['uncertainty_notes']))}</p>"
        "<table><thead><tr><th>Dimension</th><th>Severity</th><th>Visibility/confidence</th>"
        "<th>Codes</th><th>Evidence / consequence</th></tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
        f"<details><summary>Full assessment, consensus and provenance</summary><pre>{esc(json.dumps(value, indent=2, ensure_ascii=False))}</pre></details></div>")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    inventory = json.loads((FOLDER / "inventory.json").read_text())
    records, calls = [], []
    for source in inventory["records"]:
        record = {key: source[key] for key in (
            "id", "source_row_id", "variant", "generated_image", "twin_image",
            "scene_prompt", "product_type", "source_image_stage")}
        for version in ("v3", "v3_1"):
            record[version], evidence = audit_case(version, source)
            calls.extend(evidence)
        both = record["v3"]["ok"] and record["v3_1"]["ok"]
        record["verdict_changed"] = (record["v3"]["verdict"] != record["v3_1"]["verdict"]) if both else None
        record["changed_dimensions"] = [
            dimension for dimension in updated.SCORING.COMPONENT_WEIGHTS
            if any(record["v3"]["components"][dimension][key] != record["v3_1"]["components"][dimension][key]
                   for key in ("severity", "visibility", "confidence", "issue_codes"))
        ] if both else []
        record["ctech_anchor_label"] = ANCHOR_LABELS.get(record["id"])
        records.append(record)
    complete = all(r[v]["ok"] for r in records for v in ("v3", "v3_1"))
    if not complete and not args.allow_partial:
        raise ValueError("Incomplete comparison: use --allow-partial to expose pending/errors explicitly")
    counts = {
        v: dict(collections.Counter(r[v]["verdict"] if r[v]["ok"] else r[v]["status"] for r in records))
        for v in ("v3", "v3_1")}
    result = {
        "schema_version": "placement-v3-v3.1-side-by-side-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_viewer": inventory["source_viewer"],
        "inventory": {"path": str(FOLDER / "inventory.json"), "sha256": updated.sha(FOLDER / "inventory.json"),
                      **{k: inventory[k] for k in (
                          "row_count", "output_count", "unique_asset_count", "input_twin_count")}},
        "versions": {
            "v3": {
                "method": "Fresh original V2 exemplar + compact V3 + consensus-v2; no reused old judgments",
                "model_requested": "gpt-5.5", "reasoning_effort": "high",
                "model_returned": sorted({c["model"] for c in calls if c["version"] == "v3"}),
                "primary_max_completion_tokens": 12000, "component_check_max_completion_tokens": 6000,
            },
            "v3_1": {
                "method": "Fresh Astra-reviewed V3-derived rubrics; unchanged scoring/schema and consensus-v2",
                "model_requested": "gpt-5.5", "reasoning_effort": "high",
                "model_returned": sorted({c["model"] for c in calls if c["version"] == "v3_1"}),
                "primary_max_completion_tokens": 12000, "component_check_max_completion_tokens": 6000,
                "anchor_gate_met": False, "promoted": False,
            },
            "protocol_freeze": {"path": str(ROOT / "protocol_freeze.json"),
                                "sha256": updated.verify_freeze()},
        },
        "claim_boundary": "Model predictions on user-supplied historical E2E development images, outside scene-stage calibration. Not human acceptance, accuracy or 90-new-image evaluation.",
        "records": records,
        "summary": {"complete": complete, "counts": counts, "record_count": len(records),
                    "verdict_changed_count": sum(r["verdict_changed"] is True for r in records),
                    "actual_successful_model_response_count": len(calls)},
    }
    updated.write_json(FOLDER / "comparison.json", result)
    updated.write_json(FOLDER / "evidence_audit.json", {
        "protocol_freeze_sha256": updated.verify_freeze(),
        "complete": complete, "raw_model_outputs_unchanged": True,
        "deterministic_recomputation_matches": True, "calls": calls,
    })
    source_anchors = json.loads((ROOT / "sources/manifest.json").read_text())["cases"]
    calibration = []
    for case in source_anchors:
        item = {"id": case["id"], "source_url": case["generated_image"]["url"]}
        for version in ("v3", "v3_1"):
            path = FOLDER / "runs" / version / case["id"] / "result.json"
            if path.exists():
                item[version] = calibrate_anchors.summarize(case, json.loads(path.read_text()))
        calibration.append(item)
    updated.write_json(FOLDER / "anchor_calibration.json", {
        "cases": calibration, "development_only": True, "semantic_resampling": False,
        "astra_disagreement": (
            "Astra corroborates both row07 placement labels, but cannot corroborate the "
            "user-supplied row13 L-shaped-table/extra-legs label from the exact image. "
            "The C-Tech geometry-fail label remains authoritative supplied feedback, not invented visual evidence."),
    })
    sections = []
    for record in records:
        image, twin = record["generated_image"], record["twin_image"]
        esc = html.escape
        sections.append(
            f"<section id='{esc(record['id'])}'><h2>{esc(record['source_row_id'])} — {esc(record['variant'])}</h2>"
            f"<p>{esc(record['scene_prompt'])}</p>"
            + (f"<p class='warning'>{esc(record['ctech_anchor_label'])}</p>"
               if record["ctech_anchor_label"] else "")
            +
            f"<div class='images'><figure><a href='{esc(image['url'])}'><img loading='lazy' src='../sources/img/{Path(image['local_path']).name}'></a>"
            f"<figcaption>Same target for both judges; SHA-256 <code>{image['sha256']}</code></figcaption></figure>"
            f"<figure><a href='{esc(twin['url'])}'><img loading='lazy' src='../sources/img/{Path(twin['local_path']).name}'></a>"
            "<figcaption>Exact original twin</figcaption></figure></div>"
            f"<p>Changed dimensions: {esc(', '.join(record['changed_dimensions']) or 'none / not comparable')}</p>"
            "<div class='judges'>" + card("V3", record["v3"]) + card("V3.1", record["v3_1"]) + "</div></section>")
    page = (
        "<!doctype html><meta charset='utf-8'><title>Fresh V3 vs V3.1 placement judges</title>"
        "<style>body{font:15px system-ui;margin:2em;background:#f5f6f8;color:#18202a}"
        "section{background:white;padding:1em;margin:1.5em 0;border-radius:10px}"
        ".images,.judges{display:grid;grid-template-columns:1fr 1fr;gap:1em}"
        "figure{margin:0}img{max-width:100%;max-height:530px}table{border-collapse:collapse;width:100%;font-size:12px}"
        "td,th{border:1px solid #ddd;padding:.4em;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere}"
        ".warning{background:#fff0d6;border-left:5px solid #b75b00;padding:1em}"
        "code{overflow-wrap:anywhere}@media(max-width:1100px){.judges{grid-template-columns:1fr}}</style>"
        "<h1>Fresh frozen V3 vs V3.1</h1><p>" + html.escape(result["claim_boundary"]) + "</p>"
        "<p class='warning'><strong>V3.1 calibration gate NOT MET; do not promote.</strong> "
        "The actual V3.1 run misses the required row07_4 alignment failure and row13_4 geometry failure. "
        "Labels and model disagreements are preserved; no judgments were hand-edited or resampled.</p>"
        "<p>Actual inventory: " + str(len(records)) + " outputs. Raw judgments are unedited. "
        "No independent publication was performed. C-Tech anchor labels are development evidence, not pass-rate ground truth.</p>"
        "<pre>" + html.escape(json.dumps(result["summary"], indent=2)) + "</pre>"
        + "".join(sections))
    (FOLDER / "comparison.html").write_text(page)
    print(json.dumps(result["summary"]))


if __name__ == "__main__":
    main()
