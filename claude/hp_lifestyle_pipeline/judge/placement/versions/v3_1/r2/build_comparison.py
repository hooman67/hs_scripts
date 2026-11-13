"""Audit new r2 evidence and export against the unchanged, already-frozen V3 run."""
from __future__ import annotations

import collections
import copy
import html
import json
from datetime import datetime, timezone
from pathlib import Path

import run_judge as runner
import trace_contract

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent
OUT = ROOT / "evaluation"


def verify_r1():
    before = json.loads((ROOT / "r1_integrity_before.json").read_text())
    manifest_path = R1 / "ARTIFACT_MANIFEST.json"
    if runner.sha(manifest_path) != before["manifest_sha256"]:
        raise ValueError("Original r1 manifest changed")
    manifest = json.loads(manifest_path.read_text())
    mismatches = [row["path"] for row in manifest["files"]
                  if runner.sha(row["path"]) != row["sha256"]]
    if mismatches:
        raise ValueError("Original r1 artifacts changed")
    return {"verified_utc": datetime.now(timezone.utc).isoformat(),
            "indexed_files_verified": len(manifest["files"]), "mismatches": [],
            "manifest_path": str(manifest_path), "manifest_sha256": runner.sha(manifest_path)}


def audit_r2(record):
    folder = ROOT / "calibration/runs" / record["id"]
    if not folder.exists():
        return {"ok": False, "status": "not_run_gate_blocked", "verdict": None,
                "score": None, "confidence": None, "components": None,
                "result_path": None, "result_sha256": None, "error": None,
                "model_returned": []}, []
    stages, calls, traces = {}, [], {}
    runtime = {k: record[k] for k in ("product_type", "scene_prompt")}
    runtime["image_stage"] = "scene_generation"
    for key in ("generated_image", "twin_image"):
        runtime[key] = record[key]["local_path"]
    for request_path in sorted(folder.glob("*/request.json")):
        raw_path = request_path.parent / "response.json"
        stage = raw_path.parent.name
        raw = json.loads(raw_path.read_text()) if raw_path.exists() else None
        request = json.loads(request_path.read_text())
        saved_path = raw_path.parent / "result.json"
        saved = json.loads(saved_path.read_text())
        call = {"id": record["id"], "stage": stage, "model": raw.get("model") if raw else None,
                "response_path": str(raw_path) if raw else None,
                "response_sha256": runner.sha(raw_path) if raw else None,
                "ok": saved["ok"]}
        calls.append(call)
        if request["runtime_input"] != runtime:
            raise ValueError("r2 runtime differs from frozen source inventory")
        if (request["protocol_freeze_sha256"] != runner.verify_freeze()
                or request["model_requested"] != "gpt-5.5"
                or request["reasoning_effort"] != "high"
                or request["target_comments_or_expectations_passed"] is not False):
            raise ValueError("r2 protocol/configuration/label-isolation mismatch")
        if request["system_prompt_sha256"] != runner.sha(ROOT / "prompts" / f"{stage}.md"):
            raise ValueError("r2 prompt differs from frozen role")
        if (raw_path.parent / "system_prompt.md").read_bytes() != (
            ROOT / "prompts" / f"{stage}.md").read_bytes():
            raise ValueError("Preserved request prompt differs")
        fingerprint = runner.json_sha({k: v for k, v in request.items() if k != "fingerprint"})
        if request["fingerprint"] != fingerprint or saved["fingerprint"] != fingerprint:
            raise ValueError("Request fingerprint mismatch")
        for key in ("generated_image", "twin_image"):
            if request["images"][key]["sha256"] != record[key]["sha256"]:
                raise ValueError("r2 image differs from frozen V3 baseline")
        if stage == "independent" and request["proposals"] is not None:
            raise ValueError("Names-only verifier received allegations")
        names = request["requested_components"]
        payload_schema = runner.component_schema(names) if names else runner.SCORING.OBSERVATION_SCHEMA
        schema = trace_contract.envelope_schema(payload_schema)
        if request["schema_sha256"] != runner.json_sha(schema):
            raise ValueError("Evidence envelope schema differs")
        if json.loads((raw_path.parent / "schema.json").read_text()) != schema:
            raise ValueError("Preserved request schema differs")
        if raw is None:
            if saved["ok"]:
                raise ValueError("Successful stage is missing its raw response")
            call["error_type"] = saved["error_type"]
            continue
        try:
            choice = raw["choices"][0]
            if not runner.identity_matches(raw.get("model")) or choice["finish_reason"] != "stop":
                raise ValueError("Unexpected returned model or incomplete response")
            value = json.loads(choice["message"]["content"])
            observation = trace_contract.validate(value, payload_schema)
            if names:
                runner.validate_components(observation, payload_schema)
            else:
                runner.validate_new_observation(observation)
            if (not saved["ok"] or saved["observation"] != observation
                    or saved["evidence_envelope"] != value):
                raise ValueError("Saved evidence differs from unchanged raw response")
            stages[stage] = observation
            traces[stage] = {"trace": value["trace"], "result_path": str(saved_path),
                             "result_sha256": runner.sha(saved_path)}
        except Exception as exc:
            if saved["ok"]:
                raise
            call["validation_error_type"] = type(exc).__name__
            call["validation_error"] = (
                f"Schema keyword {exc.validator} at {list(exc.absolute_path)}"
                if hasattr(exc, "validator") else str(exc).splitlines()[0])
    path = folder / "result.json"
    if not path.exists():
        error = folder / "error.json"
        return {"ok": False, "status": "error", "verdict": None, "score": None,
                "confidence": None, "components": None, "result_path": None,
                "result_sha256": None, "model_returned": sorted({c["model"] for c in calls if c["model"]}),
                "error": json.loads(error.read_text()) if error.exists() else {"type": "IncompleteRun"},
                "evidence_envelopes": traces}, calls
    result = json.loads(path.read_text())
    if result["runtime_input"] != runtime or result["protocol_freeze_sha256"] != runner.verify_freeze():
        raise ValueError("Ensemble runtime/freeze mismatch")
    for stage, artifact in result["stages"].items():
        if runner.sha(artifact["path"]) != artifact["sha256"] or stage not in stages:
            raise ValueError("Ensemble stage evidence hash mismatch")
    if set(result["stages"]) != set(stages):
        raise ValueError("Unbound or missing stage response")
    recomputed = runner.aggregate_stages(
        stages["baseline"], stages["compact"], stages.get("proposal"), stages.get("independent"))
    if any(result[key] != value for key, value in recomputed.items()):
        raise ValueError("r2 ensemble differs from raw-response recomputation")
    judgment, decision = result["application_merged_judgment"], result["final_decision"]
    return {
        "ok": True, "status": "complete", "verdict": decision["verdict"],
        "score": judgment["natural_placement_score"],
        "confidence": decision["reported_overall_confidence"],
        "components": judgment["observation"]["components"],
        "scene_reading": judgment["observation"]["scene_reading"], "coverage": judgment["coverage"],
        "verdict_reasons": decision["verdict_reasons"], "uncertainty_notes": decision["uncertainty_notes"],
        "triggered_components": result["triggered_components"],
        "consensus_resolution": result["consensus_resolution"],
        "result_path": str(path), "result_sha256": runner.sha(path), "error": None,
        "model_returned": sorted({c["model"] for c in calls if c["model"]}), "evidence_envelopes": traces,
    }, calls


def card(name, result, expectations):
    esc = html.escape
    title = (f"{result['verdict']} / {result['score']} / {result['confidence']}"
             if result["ok"] else result["status"])
    rows = []
    for dimension, label in (
        ("orientation_alignment", "Placement / product-table alignment"),
        ("scale_perspective", "Table/chair geometry + scale/perspective"),
    ):
        expected = expectations.get(dimension, "unlabeled")
        description = {
            "unlabeled": "Unlabeled — no global positive implied",
            "no_material_defect": "No material placement/alignment defect",
            "no_new_material_defect": "Stability control: no new material defect (not human gold)",
            "material_furniture_axis_conflict": "MUST detect material laptop/table misalignment",
            "material_malformed_support_furniture": "MUST detect malformed table/support geometry",
        }[expected]
        component = (result.get("components") or {}).get(dimension)
        if component:
            actual = (f"severity {component['severity']} · {component['confidence']} · "
                      f"{component['visibility']} · codes {component['issue_codes']}")
            if expected == "unlabeled":
                outcome = "Not labeled"
            elif expected in {"no_material_defect", "no_new_material_defect"}:
                matched = component["visibility"] in {"observed", "partial"} and component["severity"] in {0, 1}
                outcome = "MATCH" if matched else "NOT MET / UNRESOLVED"
            else:
                code = ("furniture_axis_conflict" if dimension == "orientation_alignment"
                        else "malformed_support_furniture")
                matched = trace_contract.material(component) and code in component["issue_codes"]
                outcome = "DETECTED" if matched else "MISSED"
        else:
            actual, outcome = "Not run / no judgment", "NOT EVALUATED"
        rows.append(f"<tr><th>{esc(label)}</th><td>{esc(actual)}</td>"
                    f"<td>{esc(description)}</td><td><b>{esc(outcome)}</b></td></tr>")
    details = {"components": result.get("components"), "verdict_reasons": result.get("verdict_reasons"),
               "uncertainty_notes": result.get("uncertainty_notes"),
               "evidence_envelopes": result.get("evidence_envelopes"), "error": result.get("error")}
    return (f'<article class="judge"><h3>{esc(name)}</h3><p><b>Overall verdict / score / confidence: '
            f'{esc(title)}</b></p><table><thead><tr><th>Criterion</th><th>Model observation</th>'
            f'<th>Criterion expectation</th><th>Outcome</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
            f'<details><summary>Criterion evidence and trace</summary><pre>'
            f'{esc(json.dumps(details, indent=2))}</pre></details></article>')


def main():
    OUT.mkdir(exist_ok=True)
    integrity = verify_r1()
    runner.write_json(ROOT / "r1_integrity_after.json", integrity)
    original_path = R1 / "evaluation/comparison.json"
    original = json.loads(original_path.read_text())
    calibration = json.loads((ROOT / "calibration/results.json").read_text())
    if calibration["status"] == "in_progress":
        raise RuntimeError("Wait for the one calibration to finish before final export")
    selected = {row["id"]: row for row in calibration["items"]}
    records, calls = [], []
    for source in original["records"]:
        record = copy.deepcopy(source)
        if runner.sha(record["v3"]["result_path"]) != record["v3"]["result_sha256"]:
            raise ValueError("Frozen V3 comparison result changed")
        record["v3"]["baseline_reused_unchanged"] = True
        record["v3_1"], new_calls = audit_r2(record)
        calls.extend(new_calls)
        label = selected.get(record["id"])
        record["calibration_role"] = label["role"] if label else None
        record["criterion_checks"] = label["checks"] if label else None
        record["verdict_changed"] = (
            record["v3"]["verdict"] != record["v3_1"]["verdict"] if record["v3_1"]["ok"] else None)
        record["changed_dimensions"] = [
            dim for dim in runner.SCORING.COMPONENT_WEIGHTS if any(
                record["v3"]["components"][dim][field] != record["v3_1"]["components"][dim][field]
                for field in ("severity", "visibility", "confidence", "issue_codes"))
        ] if record["v3_1"]["ok"] else None
        records.append(record)
    complete = [r for r in records if r["v3_1"]["ok"]]
    counts = collections.Counter(r["v3_1"]["status"] for r in records)
    result = {
        "schema_version": "placement-v3-v3.1-r2-side-by-side-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_viewer": original["source_viewer"], "inventory": original["inventory"],
        "versions": {
            "v3": {"source": str(original_path), "source_sha256": runner.sha(original_path),
                   "baseline_reuse": "Already-frozen fresh r1 V3 run, not called again.",
                   "model_requested": "gpt-5.5",
                   "actual_models_returned": original["versions"]["v3"]["model_returned"],
                   "prior_raw_response_audit": str(R1 / "evaluation/evidence_audit.json")},
            "v3_1": {"revision": "r2", "protocol_freeze_sha256": runner.verify_freeze(),
                     "status": calibration["status"], "promoted": False,
                     "actual_models_returned": sorted({c["model"] for c in calls if c["model"]}),
                     "astra_consultation": {
                         "model_returned": json.loads((ROOT / "astra/metadata.json").read_text())["model_returned"],
                         "receipts": [{"path": str(ROOT / "astra" / name),
                                      "sha256": runner.sha(ROOT / "astra" / name)}
                                     for name in ("input.md", "config.json", "response.json",
                                                  "output.md", "metadata.json")]}},
        },
        "claim_boundary": (
            "R2 is the single bounded revision, not a promoted replacement. Only six historical "
            "cases were freshly calibrated; the other 122 r2 judgments are NOT RUN because "
            "calibration did not authorize expansion. No r1 predictions substitute for r2. "
            "Frozen V3 baseline is reused unchanged; no judgments on the new generation study."),
        "calibration": calibration,
        "source_url_availability": json.loads((ROOT / "source_url_availability.json").read_text()),
        "records": records,
        "summary": {
            "inventory_outputs": len(records), "v3_reused_complete": len(records),
            "r2_status_counts": dict(counts), "r2_complete": len(complete),
            "r2_verdicts_on_calibration_only": dict(collections.Counter(r["v3_1"]["verdict"] for r in complete)),
            "r2_scheduled_role_attempts": len(calls),
            "r2_raw_responses": sum(c["response_path"] is not None for c in calls),
            "r2_successful_validated_responses": sum(c["ok"] for c in calls),
            "r2_terminal_call_or_validation_failures": sum(not c["ok"] for c in calls),
            "all_stated_checks_matched": calibration["all_stated_checks_matched"],
            "full128_r2_started": calibration["full128_started"], "promoted": False,
        },
    }
    if calibration["all_stated_checks_matched"]:
        raise RuntimeError("Evidence review/full128 procedure must finish before this blocked-run exporter")
    runner.write_json(OUT / "comparison.json", result)
    runner.write_json(OUT / "evidence_audit.json", {
        "r1_preserved": integrity, "baseline_reuse": result["versions"]["v3"],
        "new_r2_calls": calls, "complete_r2_ensembles_recomputed_from_raw": len(complete)})
    esc = html.escape
    sections = []
    for row in records:
        images = []
        for key in ("generated_image", "twin_image"):
            image = row[key]
            images.append(
                f'<figure><img loading="lazy" src="{esc(image["url"], quote=True)}" '
                f'data-source-url="{esc(image["url"], quote=True)}" alt="{esc(key)}">'
                f'<figcaption>{esc(key)} · <a href="{esc(image["url"], quote=True)}">'
                f'original full Foundry URL</a></figcaption></figure>')
        expectations = (selected.get(row["id"]) or {}).get("expectation", {})
        sections.append(
            f'<section id="{esc(row["id"])}"><h2>{esc(row["id"])} · {esc(row["variant"])}</h2>'
            f'<div class="images">{"".join(images)}</div>'
            f'<details><summary>Full original scene prompt and source hashes</summary><pre>'
            f'{esc(row["scene_prompt"])}\n\n{esc(json.dumps({k: row[k] for k in ("generated_image", "twin_image")}, indent=2))}'
            f'</pre></details><div class="judges">{card("Frozen V3 — unchanged reuse", row["v3"], expectations)}'
            f'{card("V3.1 r2 — bounded candidate", row["v3_1"], expectations)}</div>'
            f'<pre>{esc(json.dumps({"ctech_label": row.get("ctech_anchor_label"), "criterion_checks": row["criterion_checks"]}, indent=2))}</pre>'
            f'</section>')
    document = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Frozen V3 vs V3.1 r2 — blocked calibration</title>'
        '<style>body{font:15px system-ui;margin:24px;background:#f4f4f4;color:#222}section{background:white;'
        'padding:20px;margin:20px 0}.images,.judges{display:grid;grid-template-columns:1fr 1fr;gap:18px}'
        'figure{margin:0}img{max-width:100%;height:auto}.judge{padding:14px;border:1px solid #bbb}'
        'pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}table{border-collapse:collapse;font-size:12px}'
        'th,td{border:1px solid #ccc;padding:6px;vertical-align:top}.warning{background:#ffe0dc;padding:18px}'
        '@media(max-width:800px){.images,.judges{grid-template-columns:1fr}}</style>'
        '<h1>Frozen V3 vs V3.1 r2</h1><div class="warning"><b>CALIBRATION GATE NOT MET — DO NOT PROMOTE.</b>'
        f'<p>{esc(result["claim_boundary"])}</p></div>'
        '<p>All image src attributes use full original supplied Foundry gallery URLs; '
        'no image depends on a local fixture path after copying this HTML into an iframe. '
        'Six anonymous HTTPS probes timed out on this host; public/browser access was not verified. '
        'Original downloaded image bytes remain locally available and hash-verified.</p>'
        f'<pre>{esc(json.dumps(result["summary"], indent=2))}</pre>{"".join(sections)}</html>')
    (OUT / "comparison.html").write_text(document)
    print(json.dumps(result["summary"]))


if __name__ == "__main__":
    main()
