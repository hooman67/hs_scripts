#!/usr/bin/env python3
"""Build a validated 16×10 FE report from a complete V4.3.1 full-160 run.

This script performs no model calls and no uploads. It reuses the already
published, verified V6.1 generated-scene and digital-twin URL mapping while
validating every manifest/result/protocol hash and recomputing V4.3.1 scores.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
VERSION_ROOT = HERE.parent
DEFAULT_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
DEFAULT_ASSET_MAP = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/fe_reports/"
    "v6_1_consensus_v2_grouped_20261105/data.json"
)
DEFAULT_VIEWER = Path(
    "/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html"
)
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(VERSION_ROOT) not in sys.path:
    sys.path.insert(0, str(VERSION_ROOT))
from run_batch import load_json, require, runtime_input, sha256, validate_freeze, validate_manifest, validate_saved_result  # noqa: E402


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    return value.replace(" | ", "__").replace("/", "_").replace(" ", "_")


def validated_asset_urls(path: Path, records: list[Mapping[str, Any]]) -> dict[str, tuple[str, str]]:
    source = load_json(path)
    rows = source.get("rows") if isinstance(source, Mapping) else None
    require(isinstance(rows, list) and len(rows) == 160, "asset-map FE report must have 160 rows")
    mapped: dict[str, tuple[str, str]] = {}
    for row in rows:
        require(isinstance(row, Mapping), "asset-map row invalid")
        metadata = row.get("meta_data")
        images = row.get("images")
        require(isinstance(metadata, Mapping) and isinstance(images, list), "asset-map row fields missing")
        record_id = metadata.get("evalset_item_id")
        require(isinstance(record_id, str) and record_id not in mapped, "asset-map ID invalid or duplicate")
        image_assets = [item for item in images if isinstance(item, Mapping) and item.get("asset_type") == "image"]
        require(len(image_assets) >= 2, f"{record_id}: asset-map image columns missing")
        generated = image_assets[0].get("image_src")
        twin = image_assets[1].get("image_src")
        require(isinstance(generated, str) and generated.startswith("https://"), f"{record_id}: generated URL invalid")
        require(isinstance(twin, str) and twin.startswith("https://"), f"{record_id}: twin URL invalid")
        mapped[record_id] = (generated, twin)
    by_id = {str(record["id"]): record for record in records}
    require(set(mapped) == set(by_id), "asset-map IDs differ from manifest")
    twin_url_by_hash: dict[str, str] = {}
    for record_id, record in by_id.items():
        generated_url, twin_url = mapped[record_id]
        expected_generated = record["generated_image"].get("public_url")
        require(generated_url == expected_generated, f"{record_id}: generated URL differs from manifest")
        twin_hash = str(record["twin_image"]["sha256"])
        if twin_hash in twin_url_by_hash:
            require(twin_url_by_hash[twin_hash] == twin_url, f"{record_id}: twin URL differs for identical twin hash")
        else:
            twin_url_by_hash[twin_hash] = twin_url
    require(len(twin_url_by_hash) == 16, "asset-map must contain 16 unique twins")
    return mapped


def validate_progress(run_dir: Path, manifest: Path, freeze: Path, record_ids: list[str]) -> Mapping[str, Any]:
    path = run_dir / "progress.json"
    progress = load_json(path)
    require(progress.get("schema_version") == "hp-placement-v4.3.1-full160-progress-v1", "progress schema differs")
    require(progress.get("status") == "complete", "judge run is not complete")
    require(progress.get("manifest") == str(manifest), "progress manifest path differs")
    require(progress.get("manifest_sha256") == sha256(manifest), "progress manifest hash differs")
    require(progress.get("protocol_freeze") == str(freeze), "progress freeze path differs")
    require(progress.get("protocol_freeze_sha256") == sha256(freeze), "progress freeze hash differs")
    require(progress.get("model") == "gpt-5.5", "progress model differs")
    require(progress.get("record_ids") == record_ids, "progress record order differs")
    items = progress.get("items")
    require(isinstance(items, Mapping) and set(items) == set(record_ids), "progress items differ")
    for record_id in record_ids:
        item = items[record_id]
        require(isinstance(item, Mapping) and item.get("status") in {"done", "cached"}, f"{record_id}: progress incomplete")
        result_path = run_dir / record_id / "result.json"
        require(Path(str(item.get("result_path", ""))).resolve() == result_path.resolve(), f"{record_id}: progress result path differs")
        require(item.get("result_sha256") == sha256(result_path), f"{record_id}: progress result hash differs")
    return progress


def assessment_text(result: Mapping[str, Any]) -> str:
    derived = result.get("derived")
    if not isinstance(derived, Mapping):
        assessment = result.get("assessment", {})
        return "JUDGE ASSESSMENT\nUNASSESSABLE\n\n" + str(assessment.get("unable_reason", "No reason recorded."))
    lines = [
        "JUDGE ASSESSMENT",
        f"Predicted verdict: {str(derived['verdict']).upper()} · Score: {derived['score']}/100 · Confidence: {derived['confidence']} · Coverage: {derived['coverage']}",
        "",
        "Explanation",
        str(derived["explanation"]),
        "",
        "Retained findings",
    ]
    findings = derived.get("findings", [])
    if findings:
        for finding in findings:
            lines.extend([
                f"- {finding['issue_code']} ({finding['category']}, severity {finding['severity']}, {finding['confidence']} confidence)",
                f"  evidence: {finding['evidence']}",
                f"  consequence: {finding['consequence']}",
            ])
    else:
        lines.append("- None")
    lines.extend(["", "Deterministic checks"])
    for name, check in derived.get("checks", {}).items():
        lines.extend([
            f"\n{name}",
            f"visibility: {check['visibility']}",
            f"severity: {check['severity']}",
            f"confidence: {check['confidence']}",
            f"issue_codes: {', '.join(check['issue_codes']) if check['issue_codes'] else 'none'}",
            f"evidence: {check['evidence']}",
            f"consequence: {check['consequence'] or 'none'}",
            f"visibility_limit: {check['visibility_limit'] or 'none'}",
        ])
    warnings = result.get("assessment", {}).get("general_artifact_warnings", [])
    lines.extend(["", "General artifact warnings", json.dumps(warnings, indent=2, ensure_ascii=False)])
    return "\n".join(lines)


def make_row(index: int, record: Mapping[str, Any], result: Mapping[str, Any], urls: tuple[str, str]) -> dict[str, Any]:
    derived = result.get("derived") or {}
    verdict = derived.get("verdict", "unassessable")
    score = derived.get("score")
    source = record["scene_prompt_source"]
    kv = {
        "Dataset / batch": record["device_type"],
        "Product type": record["device_type"],
        "Product": record["product"],
        "Device": record["device"],
        "V6.1 candidate": record["candidate_id"],
        "Camera": record["view"]["camera_tag"],
        "Environment": source.get("environment"),
        "Original scene prompt": record["scene_prompt"],
        "Judge V4.3.1 verdict": verdict,
        "Judge score": score,
        "Judge confidence": derived.get("confidence"),
        "Judge coverage": derived.get("coverage"),
        "Owned issue codes": ", ".join(derived.get("owned_issue_codes", [])) or "none",
        "Judge explanation": derived.get("explanation"),
        "Protocol version": result["audit"]["protocol_version"],
        "Model requested": result["audit"]["model_requested"],
        "Model returned": result["audit"]["model_returned"],
        "Result SHA-256": sha256(Path(result["_result_path"])),
    }
    score_label = "unassessable" if score is None else f"{score}/100"
    return {
        "meta_data": {"row_idx": index, "evalset_item_id": record["id"], "key_val_informations": kv},
        "images": [
            {
                "asset_type": "image",
                "is_model_input_or_output": "model_output",
                "image_src": urls[0],
                "meta_text": {"label": "Generated scene — rate natural placement", "Judge predicted verdict": str(verdict).upper(), "Judge score": score_label},
            },
            {
                "asset_type": "image",
                "is_model_input_or_output": "model_input",
                "image_src": urls[1],
                "meta_text": {"label": "Digital twin — identity and orientation reference only"},
            },
            {"asset_type": "text", "text_content": "SCENE PROMPT\n\n" + str(record["scene_prompt"])},
            {"asset_type": "text", "text_content": assessment_text(result)},
            {"asset_type": "text", "text_content": "STRUCTURED JUDGE OUTPUT\n\n" + json.dumps({"assessment": result.get("assessment"), "derived": result.get("derived"), "audit": result.get("audit"), "raw_attempts": result.get("raw_attempts")}, indent=2, ensure_ascii=False)},
        ],
    }


def report(source_title: str, rows: list[dict[str, Any]], notes: list[Any], links: Mapping[str, str] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"is_secure": True, "meta_texts": [source_title, *notes], "rows": copy.deepcopy(rows)}
    if links:
        payload["links"] = dict(links)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--freeze", type=Path, default=HERE / "protocol_freeze.json")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--asset-map-data", type=Path, default=DEFAULT_ASSET_MAP)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--viewer", type=Path, default=DEFAULT_VIEWER)
    parser.add_argument("--title", default="HP natural-placement judge V4.3.1 — original V6.1 scenes grouped by source input")
    parser.add_argument("--bucket", default="foundry-hp-enterprise-adobe-assets")
    parser.add_argument("--prefix", required=True)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    freeze_path = args.freeze.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    output = args.output.expanduser().resolve()
    viewer = args.viewer.expanduser().resolve()
    prefix = args.prefix.strip("/")
    require(prefix, "publish prefix must be nonempty")
    require(not output.exists(), f"output already exists: {output}")
    require(viewer.is_file(), f"canonical viewer missing: {viewer}")
    records = validate_manifest(manifest_path)
    freeze = validate_freeze(freeze_path, manifest_path)
    record_ids = [str(record["id"]) for record in records]
    progress = validate_progress(run_dir, manifest_path, freeze_path, record_ids)
    urls = validated_asset_urls(args.asset_map_data.expanduser().resolve(), records)

    results: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = str(record["id"])
        path = run_dir / record_id / "result.json"
        result = dict(validate_saved_result(path, runtime_input(record), freeze))
        result["_result_path"] = str(path)
        results[record_id] = result
    verdicts = Counter((result.get("derived") or {}).get("verdict", "unassessable") for result in results.values())

    groups: OrderedDict[str, list[tuple[int, Mapping[str, Any]]]] = OrderedDict()
    for record in records:
        key = f"{record['device']} | {record['view']['camera_tag']}"
        groups.setdefault(key, []).append((int(record["scene_prompt_source"]["bank_rank"]), record))
    require(len(groups) == 16, f"expected 16 groups, found {len(groups)}")
    for key, members in groups.items():
        members.sort(key=lambda item: item[0])
        require([rank for rank, _ in members] == list(range(1, 11)), f"{key}: prompt ranks differ")

    output.mkdir(parents=True)
    links: OrderedDict[str, str] = OrderedDict()
    root_rows: list[dict[str, Any]] = []
    group_builds: list[dict[str, Any]] = []
    common_notes = [
        ["Evaluation inputs", {"Manifest": str(manifest_path), "Manifest SHA-256": sha256(manifest_path), "Rows": 160, "Generated image stage": "scene_generation", "Human labels passed to judge": "No"}],
        ["Frozen judge", {"Protocol": freeze["protocol_version"], "Protocol freeze SHA-256": sha256(freeze_path), "Requested model": "gpt-5.5", "Application scoring": "deterministically recomputed and validated", "Raw responses": "preserved per row in the durable run directory"}],
        ["Judge verdicts", dict(sorted(verdicts.items()))],
        ["Human review", {"Image question": "Is the IMAGE naturally arranged?", "Judge question": "Do you agree with the JUDGE assessment and explanation?", "Instruction": "Rate image quality and judge agreement separately."}],
    ]
    for group_index, (key, members) in enumerate(groups.items(), 1):
        group_slug = slug(key)
        group_dir = output / "groups" / group_slug
        group_dir.mkdir(parents=True)
        group_rows: list[dict[str, Any]] = []
        for rank, record in members:
            row = make_row(len(root_rows) + 1, record, results[str(record["id"])], urls[str(record["id"])])
            row["meta_data"]["key_val_informations"] = {
                "Source input group": key,
                "Source input group index": f"{group_index} of 16",
                "Prompt rank within source input": f"{rank} of 10",
                "Prompts in source input": 10,
                **row["meta_data"]["key_val_informations"],
            }
            group_rows.append(row)
            root_rows.append(copy.deepcopy(row))
        group_url = f"{GATEWAY}/{args.bucket}/{prefix}/groups/{group_slug}/viewer.html"
        links[f"Group {group_index:02d}: {key}"] = group_url
        group_notes = [["Source-input grouping", {"Group": key, "Group index": f"{group_index} of 16", "Rows": 10, "Prompt ranks": "1–10"}], *common_notes]
        write_json(group_dir / "data.json", report(f"{args.title} — {key}", group_rows, group_notes))
        shutil.copyfile(viewer, group_dir / "viewer.html")
        group_builds.append({"index": group_index, "key": key, "slug": group_slug, "record_ids": [str(record["id"]) for _, record in members], "rows": 10, "viewer_url": group_url, "data_json_sha256": sha256(group_dir / "data.json"), "viewer_sha256": sha256(group_dir / "viewer.html")})

    root_notes = [["Source-input grouping", {"Grouping definition": "device + camera tag", "Groups": 16, "Prompts per group": 10, "Rows": 160, "Navigation": "Use the 16 links to inspect each source-input bank separately."}], *common_notes]
    write_json(output / "data.json", report(args.title, root_rows, root_notes, links))
    shutil.copyfile(viewer, output / "viewer.html")
    build = {
        "schema_version": "hp-placement-v4.3.1-grouped-fe-report-v1",
        "status": "local_build_validated_not_published",
        "manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
        "protocol_freeze": {"path": str(freeze_path), "sha256": sha256(freeze_path)},
        "run": {"path": str(run_dir), "progress_sha256": sha256(run_dir / "progress.json"), "workers": progress.get("workers")},
        "asset_map": {"path": str(args.asset_map_data.expanduser().resolve()), "sha256": sha256(args.asset_map_data.expanduser().resolve())},
        "canonical_viewer": {"path": str(viewer), "sha256": sha256(viewer)},
        "rows": 160,
        "groups": group_builds,
        "verdicts": dict(sorted(verdicts.items())),
        "bucket": args.bucket,
        "prefix": prefix,
        "viewer_url": f"{GATEWAY}/{args.bucket}/{prefix}/viewer.html",
        "root_data_json_sha256": sha256(output / "data.json"),
        "root_viewer_sha256": sha256(output / "viewer.html"),
    }
    write_json(output / "build_manifest.json", build)
    print(json.dumps({"status": "built_and_validated_not_published", "output": str(output), "rows": 160, "groups": 16, "objects": 34, "verdicts": dict(verdicts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
