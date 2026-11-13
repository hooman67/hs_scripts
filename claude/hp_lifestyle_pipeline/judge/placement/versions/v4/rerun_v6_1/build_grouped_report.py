#!/usr/bin/env python3
"""Build a 16-bank grouped FE report from a validated 160-row FE data file."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
DEFAULT_VIEWER = Path("/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html")
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(group_key: str) -> str:
    return group_key.replace(" | ", "__").replace("/", "_").replace(" ", "_")


def make_report(
    source: dict[str, Any], rows: list[dict[str, Any]], title: str, notes: list[Any], links: dict[str, str] | None = None
) -> dict[str, Any]:
    report = copy.deepcopy(source)
    report["meta_texts"] = [title, *notes]
    report["rows"] = copy.deepcopy(rows)
    if links:
        report["links"] = links
    else:
        report.pop("links", None)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--viewer", type=Path, default=DEFAULT_VIEWER)
    parser.add_argument("--title", required=True)
    parser.add_argument("--bucket", default="foundry-hp-enterprise-adobe-assets")
    parser.add_argument("--prefix", required=True)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    source_path = args.source_data.expanduser().resolve()
    viewer_path = args.viewer.expanduser().resolve()
    output = args.output.expanduser().resolve()
    prefix = args.prefix.strip("/")
    require(bool(prefix), "prefix must be nonempty")
    manifest = load_json(manifest_path)
    source = load_json(source_path)
    require(viewer_path.is_file(), f"missing canonical viewer: {viewer_path}")
    records = manifest.get("records")
    rows = source.get("rows")
    require(isinstance(records, list) and len(records) == 160, "manifest must have 160 records")
    require(isinstance(rows, list) and len(rows) == 160, "source report must have 160 rows")

    record_by_id = {record["id"]: record for record in records}
    row_by_id = {row["meta_data"]["evalset_item_id"]: row for row in rows}
    require(len(record_by_id) == len(row_by_id) == 160, "IDs are not unique")
    require(set(record_by_id) == set(row_by_id), "manifest/report IDs differ")

    groups: OrderedDict[str, list[tuple[int, str]]] = OrderedDict()
    for record in records:
        record_id = record["id"]
        device = record.get("device")
        camera = record.get("view", {}).get("camera_tag")
        rank = record.get("scene_prompt_source", {}).get("bank_rank")
        require(isinstance(device, str) and device, f"{record_id}: missing device")
        require(isinstance(camera, str) and camera, f"{record_id}: missing camera tag")
        require(isinstance(rank, int) and 1 <= rank <= 10, f"{record_id}: bad rank")
        require(record.get("candidate_id") == f"p{rank}", f"{record_id}: candidate/rank mismatch")
        groups.setdefault(f"{device} | {camera}", []).append((rank, record_id))
    require(len(groups) == 16, f"expected 16 groups, found {len(groups)}")

    output.mkdir(parents=True, exist_ok=False)
    group_links: dict[str, str] = {}
    root_rows: list[dict[str, Any]] = []
    group_manifest: list[dict[str, Any]] = []
    for group_index, (key, members) in enumerate(groups.items(), start=1):
        members.sort()
        require([rank for rank, _ in members] == list(range(1, 11)), f"{key}: ranks differ")
        group_slug = slug(key)
        group_dir = output / "groups" / group_slug
        group_dir.mkdir(parents=True)
        group_rows: list[dict[str, Any]] = []
        for rank, record_id in members:
            row = copy.deepcopy(row_by_id[record_id])
            existing = row["meta_data"].get("key_val_informations", {})
            row["meta_data"]["key_val_informations"] = {
                "Source input group": key,
                "Source input group index": f"{group_index} of 16",
                "Prompt rank within source input": f"{rank} of 10",
                "Prompts in source input": 10,
                **existing,
            }
            row["meta_data"]["row_idx"] = len(root_rows) + 1
            group_rows.append(row)
            root_rows.append(copy.deepcopy(row))
        group_url = f"{GATEWAY}/{args.bucket}/{prefix}/groups/{group_slug}/viewer.html"
        group_links[f"Group {group_index:02d}: {key}"] = group_url
        notes = [["Source-input grouping", {"Group": key, "Group index": f"{group_index} of 16", "Rows": 10, "Prompt ranks": "1–10", "Grouping definition": "device + camera tag"}], *copy.deepcopy(source.get("meta_texts", [])[1:])]
        write_json(group_dir / "data.json", make_report(source, group_rows, f"{args.title} — {key}", notes))
        shutil.copyfile(viewer_path, group_dir / "viewer.html")
        group_manifest.append({
            "index": group_index,
            "key": key,
            "slug": group_slug,
            "record_ids": [record_id for _, record_id in members],
            "prompt_ranks": [rank for rank, _ in members],
            "rows": 10,
            "viewer_url": group_url,
            "data_json_sha256": sha256(group_dir / "data.json"),
            "viewer_sha256": sha256(group_dir / "viewer.html"),
        })

    require(len(root_rows) == 160, "root row count differs")
    root_notes = [["Source-input grouping", {"Grouping definition": "device + camera tag", "Groups": 16, "Prompts per group": 10, "Rows": 160, "Navigation": "Use the 16 links to review one source-input bank at a time."}], *copy.deepcopy(source.get("meta_texts", [])[1:])]
    write_json(output / "data.json", make_report(source, root_rows, args.title, root_notes, group_links))
    shutil.copyfile(viewer_path, output / "viewer.html")
    build_manifest = {
        "schema_version": "hp-placement-v4-grouped-fe-report-v1",
        "status": "local_build_validated_not_published",
        "title": args.title,
        "source_manifest": str(manifest_path),
        "source_manifest_sha256": sha256(manifest_path),
        "source_report_data": str(source_path),
        "source_report_data_sha256": sha256(source_path),
        "canonical_viewer": str(viewer_path),
        "canonical_viewer_sha256": sha256(viewer_path),
        "output": str(output),
        "bucket": args.bucket,
        "prefix": prefix,
        "publish_destination": f"s3://{args.bucket}/{prefix}/",
        "viewer_url": f"{GATEWAY}/{args.bucket}/{prefix}/viewer.html",
        "rows": 160,
        "groups": group_manifest,
        "root_data_json_sha256": sha256(output / "data.json"),
        "root_viewer_sha256": sha256(output / "viewer.html"),
    }
    write_json(output / "build_manifest.json", build_manifest)
    print(json.dumps({"output": str(output), "groups": 16, "rows": 160, "objects_to_publish": 34}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
