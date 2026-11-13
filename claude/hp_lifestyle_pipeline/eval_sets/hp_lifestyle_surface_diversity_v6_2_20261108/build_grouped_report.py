#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Build canonical FE reports for a surface-diversity generation run."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any

import run_generation as generation
import build_distribution as distribution


DEFAULT_VIEWER = Path.home() / ".claude/scripts/fe_html/annotation_viewer.html"
DEFAULT_TITLE = "HP Lifestyle V6.2 — Surface Diversity (160 prompts, GPT Image 2.5)"
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(path: Path) -> Any:
    require(path.is_file(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    generation.atomic_json(path, value)


def group_slug(device: str, camera: str) -> str:
    return f"{device}__{camera}".replace("/", "_").replace(" ", "_")


def evidence_text(prompt: dict[str, Any]) -> str:
    evidence = prompt.get("evidence") or []
    return "\n".join(
        f"- {item.get('document', '')}{(' · ' + item.get('path', '')) if item.get('path') else ''}: {item.get('quote', '')}"
        for item in evidence
    ) or "None supplied"


def prompt_text(prompt: dict[str, Any], source_input: dict[str, Any]) -> str:
    score_components = prompt.get("score_components") or {}
    return (
        f"FULL SCENE PROMPT\n{prompt.get('text', '')}\n\n"
        f"SCORES\nSource relevance: {prompt.get('source_relevance_score', 'n/a')}\n"
        f"C-Tech reference: {prompt.get('ctech_reference_score', 'n/a')}\n"
        f"Score components / smart brief and source messaging:\n{json.dumps(score_components, indent=2, ensure_ascii=False)}\n\n"
        f"FULL SMART BRIEF\n{source_input.get('smart_brief') or 'Not supplied'}\n\n"
        f"FULL SOURCE MESSAGING\n{source_input.get('source_messaging') or 'Not supplied'}\n\n"
        f"SMART BRIEF + SOURCE EVIDENCE\n{evidence_text(prompt)}\n\n"
        f"SOURCE EXPLANATION\n{prompt.get('explanation') or 'Not supplied'}\n\n"
        f"C-TECH EXPLANATION\n{prompt.get('ctech_explanation') or 'Not supplied'}\n\n"
        f"CAMERA-FIT EXPLANATION\n{prompt.get('camera_fit_explanation') or 'Not supplied'}\n\n"
        f"CREATIVE DEPARTURES\n{json.dumps(prompt.get('creative_departures') or [], indent=2, ensure_ascii=False)}\n\n"
        f"COMPLETE FROZEN PROMPT RECORD\n{json.dumps(prompt, indent=2, ensure_ascii=False)}"
    )


def load_judgments(path: Path | None, prompts_sha256: str, row_ids: set[str]) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    document = load(path.resolve())
    require(document.get("source_prompts_sha256") == prompts_sha256,
            "judgment source_prompts_sha256 does not match this frozen prompt document")
    items = document.get("rows", document.get("judgments"))
    require(isinstance(items, list), "judgment file must contain rows or judgments")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        row_id = item.get("row_id", item.get("id"))
        require(row_id in row_ids, f"judgment references an unknown row: {row_id!r}")
        require(row_id not in result, f"duplicate judgment row: {row_id}")
        result[row_id] = item
    return result


def build_row(
    row: dict[str, Any], record: dict[str, Any] | None, judgment: dict[str, Any] | None,
    bucket: str, prefix: str, row_idx: int, source_input: dict[str, Any],
    run_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prompt = row["prompt"]
    support = distribution.primary_support(prompt)
    twin_name = f"{row['device_id']}__{row['camera_id']}.png"
    base = f"{GATEWAY}/{bucket}/{prefix.rstrip('/')}"
    status = record.get("status", "pending") if record else "pending"
    image_url = f"{base}/images/{row['row_slug']}.png" if status == "done" else None
    judgment_status = "complete" if judgment else "pending — no new judgment result supplied"
    run_manifest = run_manifest or {}
    key_values = {
        "Generation status": status,
        "Judgment status": judgment_status,
        "Product type": prompt.get("device_type"),
        "Environment": prompt.get("environment"),
        "View": prompt.get("view_role") or prompt.get("camera_tag"),
        "Surface family": support["family"],
        "Surface shape": support["shape"],
        "Device": prompt.get("device_display_name", row["device_id"]),
        "Camera tag": prompt.get("camera_tag"),
        "Endpoint camera": row["camera_id"],
        "Prompt rank": row["rank"],
        "Primary support exact phrase": support["phrase"],
        "Primary support finalizer metadata": json.dumps(support["raw"], ensure_ascii=False),
        "Full scene prompt": prompt.get("text"),
        "Source relevance score": prompt.get("source_relevance_score"),
        "C-Tech reference score": prompt.get("ctech_reference_score"),
        "C-Tech reference": prompt.get("ctech_reference_id"),
        "Relationship": prompt.get("relationship"),
        "Approved prop IDs": ", ".join(prompt.get("prop_ids") or []),
        "Smart-brief/source score components": json.dumps(prompt.get("score_components") or {}, ensure_ascii=False),
        "Full smart brief": source_input.get("smart_brief"),
        "Full source messaging": source_input.get("source_messaging"),
        "Source evidence": evidence_text(prompt),
        "Source explanation": prompt.get("explanation"),
        "C-Tech explanation": prompt.get("ctech_explanation"),
        "Camera-fit explanation": prompt.get("camera_fit_explanation"),
        "Output image": image_url or "Pending",
        "Job ID": record.get("job_id") if record else None,
        "Run lineage": (run_manifest.get("lineage") or {}).get("label"),
        "Generator": run_manifest.get("generator"),
        "Rewriter": run_manifest.get("rewriterVersion"),
        "Pipeline version": (run_manifest.get("lineage") or {}).get("pipelineVersion"),
        "Run SHA-256": run_manifest.get("run_sha256"),
    }
    assets: list[dict[str, Any]] = [
        {
            "asset_type": "image", "is_model_input_or_output": "model_input",
            "image_src": f"{base}/twins/{twin_name}",
            "meta_text": {"label": "Digital twin / exact fixed camera input", "Device": row["device_id"], "Camera": row["camera_id"]},
        },
    ]
    if image_url:
        assets.append({
            "asset_type": "image", "is_model_input_or_output": "model_output", "image_src": image_url,
            "meta_text": {"label": "GPT Image 2.5 scene output", "Status": status, "SHA-256": record.get("image_sha256")},
        })
    else:
        assets.append({
            "asset_type": "text", "is_model_input_or_output": "model_output",
            "text_content": f"GENERATION {status.upper()}\nNo generated output is present for this row.",
            "meta_text": {"label": "Generation output status"},
        })
    assets.append({
        "asset_type": "text", "is_model_input_or_output": "model_input",
        "text_content": prompt_text(prompt, source_input),
        "meta_text": {"label": "Full frozen prompt, scores, source, and explanations"},
    })
    debug = {
        "record": record or {"status": "pending"},
        "scene_debug": (record or {}).get("scene_debug"),
        "runtime": (record or {}).get("runtime"),
        "stage_statuses": (record or {}).get("stage_statuses"),
    }
    assets.append({
        "asset_type": "text", "is_model_input_or_output": "model_output",
        "text_content": "GENERATION / PIPELINE DEBUG\n" + json.dumps(debug, indent=2, ensure_ascii=False),
        "meta_text": {"label": "Output provenance and debug"},
    })
    assets.append({
        "asset_type": "text", "is_model_input_or_output": "model_output",
        "text_content": ("NEW JUDGMENT RESULT\n" + json.dumps(judgment, indent=2, ensure_ascii=False)) if judgment
                        else "JUDGMENT PENDING\nNo result from a new surface-diversity judgment run was supplied. No prior judgment was copied.",
        "meta_text": {"label": "New judgment only", "Status": judgment_status},
    })
    return {"meta_data": {"row_idx": row_idx, "evalset_item_id": row["row_id"], "key_val_informations": key_values}, "images": assets}


def make_report(title: str, rows: list[dict[str, Any]], notes: list[Any], links: dict[str, str] | None = None) -> dict[str, Any]:
    report: dict[str, Any] = {"is_secure": True, "meta_texts": [title, *notes], "rows": copy.deepcopy(rows)}
    if links:
        report["links"] = links
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--prompts-sha256", required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="defaults to RUN_DIR/report")
    parser.add_argument("--judgments", type=Path, help="new-run judgments only; source hash must match")
    parser.add_argument("--catalog", type=Path, help="optional frozen approved-prop catalog for distribution frequencies")
    parser.add_argument("--prompts-txt", type=Path, help="optional frozen plain-text prompt export")
    parser.add_argument("--viewer", type=Path, default=DEFAULT_VIEWER)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--bucket", default=generation.BUCKET)
    parser.add_argument("--prefix", default=generation.DEFAULT_PREFIX)
    args = parser.parse_args()
    prompts_path = args.prompts.resolve()
    document = load(prompts_path)
    validated = generation.validate_prompt_document(document, prompts_path, args.prompts_sha256)
    rows = sorted(validated, key=lambda row: (generation.DEVICE_ORDER.index(row["device_id"]),
                  generation.VIEW_ORDER[row["device_id"]].index(row["camera_id"]), row["rank"]))
    require(args.viewer.resolve().is_file(), f"missing canonical viewer: {args.viewer.resolve()}")
    run_dir = args.run_dir.resolve()
    run_manifest = load(run_dir / "run_manifest.json")
    require(run_manifest.get("prompts_sha256") == args.prompts_sha256,
            "run manifest prompt hash differs from the requested frozen input")
    require(run_manifest.get("bucket") == args.bucket and run_manifest.get("prefix") == args.prefix,
            "report bucket/prefix differs from the immutable run manifest")
    output = args.output.resolve() if args.output else run_dir / "report"
    output.mkdir(parents=True, exist_ok=True)
    downloads = output / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    shutil.copy2(prompts_path, downloads / "prompts_all_160.json")
    prompts_txt = args.prompts_txt.resolve() if args.prompts_txt else prompts_path.with_suffix(".txt")
    require(prompts_txt.is_file(), f"missing frozen plain-text prompt export: {prompts_txt}")
    shutil.copy2(prompts_txt, downloads / "prompts_all_160.txt")
    by_row = {row["row_id"]: row for row in rows}
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = load(path)
        row_id = record.get("row_id")
        require(row_id in by_row, f"generation record references an unknown row: {row_id!r}")
        require(row_id not in records, f"duplicate generation record: {row_id}")
        require(record.get("prompt_sha256") == by_row[row_id]["prompt_sha256"],
                f"generation record prompt hash differs for {row_id}")
        if record.get("status") == "done" and generation.valid_completed_record(run_dir, by_row[row_id]) is None:
            records[row_id] = {
                "row_id": row_id,
                "prompt_sha256": by_row[row_id]["prompt_sha256"],
                "status": "invalid — output artifact missing or hash-mismatched",
                "source_record": record,
            }
        else:
            records[row_id] = record
    bank_manifest = load(run_dir / "source/bank_inputs_manifest.json").get("assets", {})
    source_inputs = {case_id: load(Path(item["materialized_path"])) for case_id, item in bank_manifest.items()}
    require(len(source_inputs) == 16, "run must contain all 16 materialized bank source inputs")
    judgments = load_judgments(args.judgments, args.prompts_sha256, {row["row_id"] for row in rows})
    grouped: OrderedDict[tuple[str, str], list[dict[str, Any]]] = OrderedDict()
    for row in rows:
        grouped.setdefault((row["device_id"], row["camera_id"]), []).append(row)
    require(len(grouped) == 16 and all(len(items) == 10 for items in grouped.values()), "expected 16 groups of ten")
    root_rows: list[dict[str, Any]] = []
    links: dict[str, str] = {}
    group_manifest: list[dict[str, Any]] = []
    for group_index, ((device, camera), members) in enumerate(grouped.items(), start=1):
        slug = group_slug(device, camera)
        group_dir = output / "groups" / slug
        group_dir.mkdir(parents=True, exist_ok=True)
        report_rows = []
        for member in members:
            case_id = member["prompt"].get("bank_debug_ref") or member["row_id"].rsplit("::", 1)[0]
            require(case_id in source_inputs, f"missing materialized source input for {case_id}")
            report_row = build_row(member, records.get(member["row_id"]), judgments.get(member["row_id"]),
                                   args.bucket, args.prefix, len(root_rows) + 1, source_inputs[case_id], run_manifest)
            report_rows.append(report_row)
            root_rows.append(copy.deepcopy(report_row))
        url = f"{GATEWAY}/{args.bucket}/{args.prefix.rstrip('/')}/report/groups/{slug}/viewer.html"
        links[f"Group {group_index:02d}: {device} | {camera}"] = url
        support_counts = distribution.support_summary([
            {"primary_support": distribution.primary_support(item["prompt"]),
             "device_type": item["prompt"].get("device_type"), "environment": item["prompt"].get("environment"),
             "row_id": item["row_id"]}
            for item in members
        ])
        notes = [["Source-input group", {"Group": f"{device} | {camera}", "Rows": 10, "Ranks": "1-10",
                  "Surface families": support_counts["family_counts"], "Surface shapes": support_counts["shape_counts"],
                  "Generator": run_manifest.get("generator"), "Rewriter": run_manifest.get("rewriterVersion"),
                  "Pipeline version": (run_manifest.get("lineage") or {}).get("pipelineVersion"),
                  "Lineage": (run_manifest.get("lineage") or {}).get("label"),
                  "Run SHA-256": run_manifest.get("run_sha256"),
                  "Judgments": "New matching-source results where supplied; otherwise pending"}]]
        write(group_dir / "data.json", make_report(f"{args.title} — {device} | {camera}", report_rows, notes))
        shutil.copyfile(args.viewer.resolve(), group_dir / "viewer.html")
        group_manifest.append({"index": group_index, "device": device, "camera": camera, "rows": 10,
                               "viewer_url": url, "record_ids": [item["row_id"] for item in members],
                               "data_json_sha256": generation.sha256_path(group_dir / "data.json")})
    all_support_counts = distribution.support_summary([
        {"primary_support": distribution.primary_support(item["prompt"]),
         "device_type": item["prompt"].get("device_type"), "environment": item["prompt"].get("environment"),
         "row_id": item["row_id"]}
        for item in rows
    ])
    distribution_url = f"{GATEWAY}/{args.bucket}/{args.prefix.rstrip('/')}/report/distribution/index.html"
    links["Text distribution and surface compliance"] = distribution_url
    links["Frozen prompts — JSON"] = f"{GATEWAY}/{args.bucket}/{args.prefix.rstrip('/')}/report/downloads/prompts_all_160.json"
    links["Frozen prompts — TXT"] = f"{GATEWAY}/{args.bucket}/{args.prefix.rstrip('/')}/report/downloads/prompts_all_160.txt"
    notes = [["Run scope", {"Rows": 160, "Groups": 16, "Prompts per group": 10,
              "Generator": run_manifest.get("generator"), "Rewriter": run_manifest.get("rewriterVersion"),
              "Pipeline version": (run_manifest.get("lineage") or {}).get("pipelineVersion"),
              "Lineage": (run_manifest.get("lineage") or {}).get("label"),
              "Endpoint": run_manifest.get("endpoint"), "Run SHA-256": run_manifest.get("run_sha256"),
              "Catalog SHA-256": run_manifest.get("catalog_sha256"),
              "Frozen prompts SHA-256": args.prompts_sha256,
              "Surface families": all_support_counts["family_counts"],
              "Surface shapes": all_support_counts["shape_counts"],
              "Round Café text rows": f"{all_support_counts['round_cafe']['numerator']} / {all_support_counts['round_cafe']['denominator']}",
              "Judgments": f"{len(judgments)} new matching-source results; {160 - len(judgments)} pending",
              "Navigation": "Use the 16 group links for each device/view bank; combined rows are contiguous by bank and rank."}]]
    write(output / "data.json", make_report(args.title, root_rows, notes, links))
    shutil.copyfile(args.viewer.resolve(), output / "viewer.html")
    distribution_analysis = distribution.build(
        prompts_path, args.prompts_sha256, run_dir, output / "distribution",
        source_inputs, records, args.catalog.resolve() if args.catalog else None,
    )
    manifest = {
        "schema_version": "hp-surface-diversity-v6.2-grouped-fe-v1", "title": args.title,
        "source_prompts": str(prompts_path), "source_prompts_sha256": args.prompts_sha256,
        "run_identity": run_manifest,
        "run_dir": str(run_dir), "judgments": str(args.judgments.resolve()) if args.judgments else None,
        "judgment_count": len(judgments), "pending_judgment_count": 160 - len(judgments),
        "canonical_viewer": str(args.viewer.resolve()), "canonical_viewer_sha256": generation.sha256_path(args.viewer.resolve()),
        "output": str(output), "publish_destination": f"s3://{args.bucket}/{args.prefix.rstrip('/')}/report/",
        "viewer_url": f"{GATEWAY}/{args.bucket}/{args.prefix.rstrip('/')}/report/viewer.html",
        "rows": len(root_rows), "groups": group_manifest,
        "distribution": {"path": str(output / "distribution/index.html"), "viewer_url": distribution_url,
                         "text_rows": distribution_analysis["scope"]["text_prompt_rows"],
                         "generated_artifacts": distribution_analysis["scope"]["generated_artifact_count"]},
        "root_data_json_sha256": generation.sha256_path(output / "data.json"),
        "root_viewer_sha256": generation.sha256_path(output / "viewer.html"),
        "downloads": {
            "prompts_all_160.json": {"sha256": generation.sha256_path(downloads / "prompts_all_160.json"),
                                      "bytes": (downloads / "prompts_all_160.json").stat().st_size},
            "prompts_all_160.txt": {"sha256": generation.sha256_path(downloads / "prompts_all_160.txt"),
                                     "bytes": (downloads / "prompts_all_160.txt").stat().st_size},
        },
    }
    write(output / "build_manifest.json", manifest)
    print(json.dumps({"output": str(output), "rows": len(root_rows), "groups": len(grouped), "viewer_url": manifest["viewer_url"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
