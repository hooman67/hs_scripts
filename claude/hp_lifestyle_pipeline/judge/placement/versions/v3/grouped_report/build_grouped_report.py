#!/usr/bin/env python3
"""Build a grouped FE revision of the frozen V6.1 consensus-v2 report.

The source report remains untouched.  The combined report is reordered into
16 contiguous source-input banks of 10 prompts, and a 10-row FE report is
written for every bank.  The root report links to each bank so a reviewer can
inspect the ten variants in isolation while retaining every original image,
prompt, and judge-evidence field.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data/new_v6_1_eval_20261105/manifest.json"
DEFAULT_SOURCE_DATA = (
    ROOT / "fe_reports/v6_1_consensus_v2_20261105/combined/data.json"
)
DEFAULT_OUTPUT = ROOT / "fe_reports/v6_1_consensus_v2_grouped_20261105"
VIEWER = Path.home() / ".claude/scripts/fe_html/annotation_viewer.html"
TITLE = "HP natural-placement judge V3 — V6.1 grouped by source input (10 prompts each)"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = (
    "hp_natural_placement_judge_v3_v6_1_20261105/"
    "consensus_v2/grouped_by_source_input"
)
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(group_key: str) -> str:
    return group_key.replace(" | ", "__").replace("/", "_").replace(" ", "_")


def make_report(
    source: dict[str, Any],
    rows: list[dict[str, Any]],
    title: str,
    notes: list[Any],
    links: dict[str, str] | None = None,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-data", type=Path, default=DEFAULT_SOURCE_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--title", default=TITLE)
    parser.add_argument("--prefix", default=PREFIX)
    parser.add_argument("--writer-version", default="V6.1")
    args = parser.parse_args()

    manifest = load_json(args.manifest.resolve())
    source = load_json(args.source_data.resolve())
    require(VIEWER.is_file(), f"missing canonical FE viewer: {VIEWER}")
    records = manifest.get("records")
    rows = source.get("rows")
    require(isinstance(records, list) and len(records) == 160, "manifest must have 160 records")
    require(isinstance(rows, list) and len(rows) == 160, "source report must have 160 rows")

    record_by_id = {record["id"]: record for record in records}
    row_by_id = {
        row["meta_data"]["evalset_item_id"]: row
        for row in rows
    }
    require(len(record_by_id) == 160, "manifest IDs are not unique")
    require(len(row_by_id) == 160, "source report IDs are not unique")
    require(set(record_by_id) == set(row_by_id), "manifest/report IDs differ")

    groups: OrderedDict[str, list[tuple[int, str]]] = OrderedDict()
    for record in records:
        record_id = record["id"]
        device = record.get("device")
        camera = record.get("view", {}).get("camera_tag")
        rank = record.get("scene_prompt_source", {}).get("bank_rank")
        candidate = record.get("candidate_id")
        require(isinstance(device, str) and device, f"{record_id}: missing device")
        require(isinstance(camera, str) and camera, f"{record_id}: missing camera tag")
        require(isinstance(rank, int) and 1 <= rank <= 10, f"{record_id}: bad bank rank")
        require(candidate == f"p{rank}", f"{record_id}: candidate/rank mismatch")
        key = f"{device} | {camera}"
        groups.setdefault(key, []).append((rank, record_id))

    require(len(groups) == 16, f"expected 16 groups, found {len(groups)}")
    for key, members in groups.items():
        members.sort()
        require(len(members) == 10, f"{key}: expected 10 prompts")
        require([rank for rank, _ in members] == list(range(1, 11)), f"{key}: ranks are not 1..10")

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    group_links: dict[str, str] = {}
    root_rows: list[dict[str, Any]] = []
    group_manifest: list[dict[str, Any]] = []

    for group_index, (key, members) in enumerate(groups.items(), start=1):
        group_slug = slug(key)
        group_dir = output / "groups" / group_slug
        group_dir.mkdir(parents=True, exist_ok=True)
        group_rows: list[dict[str, Any]] = []
        for rank, record_id in members:
            row = copy.deepcopy(row_by_id[record_id])
            kv = row["meta_data"].setdefault("key_val_informations", {})
            kv = {
                "Source input group": key,
                "Source input group index": f"{group_index} of 16",
                "Prompt rank within source input": f"{rank} of 10",
                "Prompts in source input": 10,
                **kv,
            }
            row["meta_data"]["key_val_informations"] = kv
            row["meta_data"]["row_idx"] = len(root_rows) + 1
            group_rows.append(row)
            root_rows.append(copy.deepcopy(row))

        group_url = f"{GATEWAY}/{BUCKET}/{args.prefix}/groups/{group_slug}/viewer.html"
        group_links[f"Group {group_index:02d}: {key}"] = group_url
        group_notes = [
            [
                "Source-input grouping",
                {
                    "Group": key,
                    "Group index": f"{group_index} of 16",
                    "Rows": 10,
                    "Prompt ranks": "1–10",
                    "Grouping definition": "device + camera tag",
                    "Source input contract": "smart brief + source messaging + camera tag",
                },
            ],
            *copy.deepcopy(source.get("meta_texts", [])[1:]),
        ]
        group_report = make_report(
            source,
            group_rows,
            f"{args.title} — {key}",
            group_notes,
        )
        write_json(group_dir / "data.json", group_report)
        shutil.copyfile(VIEWER, group_dir / "viewer.html")
        group_manifest.append(
            {
                "index": group_index,
                "key": key,
                "slug": group_slug,
                "definition": {"device": key.split(" | ", 1)[0], "camera_tag": key.split(" | ", 1)[1]},
                "record_ids": [record_id for _, record_id in members],
                "prompt_ranks": [rank for rank, _ in members],
                "rows": 10,
                "viewer_url": group_url,
                "data_json_sha256": sha256(group_dir / "data.json"),
                "viewer_sha256": sha256(group_dir / "viewer.html"),
            }
        )

    require(len(root_rows) == 160, "root row count differs")
    require(len({row["meta_data"]["evalset_item_id"] for row in root_rows}) == 160, "root IDs differ")
    root_notes = [
        [
            "Source-input grouping",
            {
                "Grouping definition": "device + camera tag",
                "Why this is the runtime source-input bank": f"Each {args.writer_version} call receives one product's smart brief and source messaging plus one camera tag, then returns ranks 1–10.",
                "Groups": 16,
                "Prompts per group": 10,
                "Rows": 160,
                "Navigation": "Use the 16 report links above to review one source-input bank at a time. The combined rows below are also contiguous by group and rank.",
            },
        ],
        *copy.deepcopy(source.get("meta_texts", [])[1:]),
    ]
    root_report = make_report(source, root_rows, args.title, root_notes, group_links)
    write_json(output / "data.json", root_report)
    shutil.copyfile(VIEWER, output / "viewer.html")

    build_manifest = {
        "schema_version": "hp-placement-grouped-fe-report-v1",
        "title": args.title,
        "grouping_definition": {
            "key": "device + camera_tag",
            "runtime_input": "smart brief + source messaging + camera tag",
            "groups": 16,
            "prompts_per_group": 10,
            "rank_source": "scene_prompt_source.bank_rank",
        },
        "source_manifest": str(args.manifest.resolve()),
        "source_manifest_sha256": sha256(args.manifest.resolve()),
        "source_report_data": str(args.source_data.resolve()),
        "source_report_data_sha256": sha256(args.source_data.resolve()),
        "canonical_viewer": str(VIEWER.resolve()),
        "canonical_viewer_sha256": sha256(VIEWER.resolve()),
        "output": str(output),
        "publish_destination": f"s3://{BUCKET}/{args.prefix}/",
        "viewer_url": f"{GATEWAY}/{BUCKET}/{args.prefix}/viewer.html",
        "rows": 160,
        "groups": group_manifest,
        "root_data_json_sha256": sha256(output / "data.json"),
        "root_viewer_sha256": sha256(output / "viewer.html"),
    }
    write_json(output / "build_manifest.json", build_manifest)
    print(json.dumps({
        "output": str(output),
        "groups": len(groups),
        "rows": len(root_rows),
        "viewer_url": build_manifest["viewer_url"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
