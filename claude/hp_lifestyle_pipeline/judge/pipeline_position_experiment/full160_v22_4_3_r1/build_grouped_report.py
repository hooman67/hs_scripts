#!/usr/bin/env python3
"""Build the V22.4.3-R1 bounded-retry qualitative-assembly FE report.

No upload is performed. The report includes control, treatment, digital twin,
both raw image attempts when a fallback occurred, guard evidence, Stage-B audit
metadata, and optional treatment-judge evidence.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any

from common import atomic_json, load_json, require, sha256_file
from config import (
    CONTROL_GROUPED_JUDGE_REPORT,
    CONTROL_REPORT,
    FE_VIEWER,
    FREEZE,
    JOB_ROOT,
    PIPELINE_VERSION,
    PROGRESS,
    REPORT_ROOT,
    S3_BUCKET,
    S3_PREFIX,
)
from preflight import verify as verify_preflight


GATEWAY = "https://foundry-aws-corp.adobe.io/asset"
TITLE = "HP V22.4.3-R1 bounded-retry qualitative assembly — V6.1 grouped by source input"


def link_or_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        require(sha256_file(destination) == sha256_file(source), f"existing asset differs: {destination}")
        return
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def normalized_id(value: str) -> str:
    return value.replace("::", "__")


def affine_summary(guard: dict) -> str:
    rows = []
    for index, attempt in enumerate(guard.get("attempts", []), start=1):
        rows.append(
            f"attempt {index}: {attempt.get('verdict')} · "
            f"translation=({attempt.get('translation_x_px'):.1f}, {attempt.get('translation_y_px'):.1f}) px · "
            f"rotation={attempt.get('rotation_deg'):.3f}° · "
            f"singular={attempt.get('singular_values')} · "
            f"p95={attempt.get('residual_p95_px'):.3f} px · "
            f"reasons={attempt.get('reasons')}"
        )
    return "\n".join(rows)


def image_card(src: str, label: str, role: str = "model_input", **meta: Any) -> dict:
    return {
        "asset_type": "image",
        "is_model_input_or_output": role,
        "image_src": src,
        "meta_text": {"label": label, **meta},
    }


def text_card(content: str, label: str) -> dict:
    return {
        "asset_type": "text",
        "text_content": content,
        "meta_text": {"label": label},
    }


def source_maps() -> tuple[dict, dict]:
    control = load_json(CONTROL_REPORT)
    require(len(control.get("rows", [])) == 160, "control report must have 160 rows")
    control_by_slug = {normalized_id(row["row_id"]): row for row in control["rows"]}
    twins = load_json(CONTROL_GROUPED_JUDGE_REPORT)
    require(len(twins.get("rows", [])) == 160, "control judge report must have 160 rows")
    twin_by_slug = {}
    for row in twins["rows"]:
        slug = normalized_id(row["meta_data"]["evalset_item_id"])
        images = [asset for asset in row["images"] if asset.get("asset_type") == "image"]
        require(len(images) >= 2, f"{slug}: control judge row lacks digital twin")
        twin_by_slug[slug] = images[1]["image_src"]
    require(set(control_by_slug) == set(twin_by_slug), "control/twin IDs differ")
    return control_by_slug, twin_by_slug


def validate_sources_only() -> dict:
    verify_preflight(allow_progress=True)
    freeze = load_json(FREEZE)
    control, twins = source_maps()
    slugs = {item["row_slug"] for item in freeze["records"]}
    require(slugs == set(control) == set(twins), "frozen/control/twin row IDs differ")
    groups: dict[str, list[int]] = {}
    for item in freeze["records"]:
        key = f"{item['device_id']}__{item['camera_tag']}"
        groups.setdefault(key, []).append(item["bank_rank"])
    require(len(groups) == 16, "expected 16 banks")
    require(all(sorted(ranks) == list(range(1, 11)) for ranks in groups.values()), "every bank must have ranks 1..10")
    return {"ok": True, "rows": 160, "banks": 16, "prompts_per_bank": 10}


def build(judge_report: Path | None = None) -> dict:
    validate_sources_only()
    require(PROGRESS.is_file(), f"missing progress: {PROGRESS}")
    progress = load_json(PROGRESS)
    require(progress.get("complete") is True and len(progress.get("done", [])) == 160, "full160 is incomplete")
    freeze = load_json(FREEZE)
    control_by_slug, twin_by_slug = source_maps()

    judge_by_slug: dict[str, dict] = {}
    judge_hash = None
    if judge_report:
        judge_report = judge_report.resolve()
        judge = load_json(judge_report)
        require(len(judge.get("rows", [])) == 160, "treatment judge report must have 160 rows")
        judge_by_slug = {
            normalized_id(row["meta_data"]["evalset_item_id"]): row
            for row in judge["rows"]
        }
        require(set(judge_by_slug) == set(control_by_slug), "treatment judge IDs differ")
        judge_hash = sha256_file(judge_report)

    records = sorted(
        freeze["records"],
        key=lambda item: (item["device_id"], item["camera_tag"], item["bank_rank"]),
    )
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for item in records:
        groups.setdefault(f"{item['device_id']}__{item['camera_tag']}", []).append(item)
    require(len(groups) == 16 and all(len(rows) == 10 for rows in groups.values()), "grouping contract failed")

    if REPORT_ROOT.exists():
        shutil.rmtree(REPORT_ROOT)
    REPORT_ROOT.mkdir(parents=True)
    rows_by_group: OrderedDict[str, list[dict]] = OrderedDict()
    audit_rows = []
    for group_index, (group, items) in enumerate(groups.items(), start=1):
        report_rows = []
        for item in items:
            slug = item["row_slug"]
            record = load_json(Path(item["path"]))
            control = control_by_slug[slug]
            row_progress = progress["rows"][slug]
            selected_job_id = row_progress["selected_job_id"]
            job_dir = JOB_ROOT / selected_job_id
            status = load_json(job_dir / "status.json")
            require(status["stage"] == "done", f"{slug}: treatment not done")
            provenance = load_json(job_dir / "provenance.json")
            require(sha256_file(job_dir / "provenance.json") == status["provenanceSha256"], f"{slug}: provenance changed")
            require(provenance["pipeline_version"] == PIPELINE_VERSION, f"{slug}: pipeline differs")
            artifacts = provenance["artifacts"]
            selected_source = Path(artifacts["ours.png"]["path"])
            guide_source = Path(artifacts["geometry_guide.png"]["path"])
            asset_dir = REPORT_ROOT / "assets" / slug
            link_or_copy(selected_source, asset_dir / "selected.png")
            link_or_copy(guide_source, asset_dir / "guide.png")
            for attempt in range(1, provenance["image_calls"] + 1):
                link_or_copy(Path(artifacts[f"gpt_{attempt}.png"]["path"]), asset_dir / f"attempt_{attempt}.png")

            guard = provenance["product_invariant_guard"]
            selected = guard["selected_attempt"]
            root_rel = f"assets/{slug}"
            group_rel = f"../../assets/{slug}"

            def cards(prefix: str) -> list[dict]:
                values = [
                    image_card(
                        f"{prefix}/selected.png",
                        "V22.4.3-R1 selected qualitative-assembly output",
                        "model_output",
                        **{
                            "Selected attempt": selected,
                            "Guard verdict": guard["attempts"][selected - 1]["verdict"],
                        },
                    ),
                    image_card(control["image_url"], "Original V6.1 control output", "model_output"),
                    image_card(twin_by_slug[slug], "Digital twin reference"),
                    image_card(f"{prefix}/guide.png", "Frozen geometry guide"),
                ]
                if provenance["image_calls"] == 2:
                    for attempt in (1, 2):
                        metric = guard["attempts"][attempt - 1]
                        values.append(
                            image_card(
                                f"{prefix}/attempt_{attempt}.png",
                                f"Raw image attempt {attempt}",
                                "model_output",
                                **{"Guard verdict": metric["verdict"], "Guard reasons": json.dumps(metric["reasons"])},
                            )
                        )
                values.append(text_card(record["prompt"], "Original V6.1 scene prompt"))
                values.append(
                    text_card(
                        json.dumps(
                            {
                                "stage_b_attempts": provenance["stage_b_attempts"],
                                "image_calls": provenance["image_calls"],
                                "product_invariant_guard": guard,
                                "calls": provenance["calls"],
                                "source_hashes": provenance["source_hashes"],
                                "outer_job_protocol": row_progress,
                            },
                            indent=2,
                        ),
                        "Treatment Stage-B, image-attempt, and guard audit",
                    )
                )
                if slug in judge_by_slug:
                    judge_row = judge_by_slug[slug]
                    values.extend(
                        copy.deepcopy(
                            [asset for asset in judge_row["images"] if asset.get("asset_type") == "text"]
                        )
                    )
                return values

            base_kv = {
                "Source input bank": group,
                "Bank index": f"{group_index} of 16",
                "Prompt rank": f"{item['bank_rank']} of 10",
                "Device": item["device_id"],
                "Device type": item["device_type"],
                "Camera": item["camera_tag"],
                "Environment": record["environment"],
                "Source relevance score": record["source_relevance_score"],
                "C-Tech reference score": record["ctech_reference_score"],
                "Pipeline treatment": PIPELINE_VERSION,
                "Stage-B attempts": len(provenance["stage_b_attempts"]),
                "Image attempts": provenance["image_calls"],
                "Guard selected attempt": selected,
                "Guard outcomes": " → ".join(attempt["verdict"] for attempt in guard["attempts"]),
                "Affine guard evidence": affine_summary(guard),
                "Original scene prompt": record["prompt"],
                "Control job ID": record["job_id"],
                "Prompt SHA-256": record["prompt_sha256"],
                "Treatment provenance SHA-256": status["provenanceSha256"],
                "Outer-job classification": row_progress["classification"],
                "Selected outer job": selected_job_id,
                "Outer jobs attempted": len(row_progress["jobs"]),
            }
            if slug in judge_by_slug:
                judge_kv = judge_by_slug[slug]["meta_data"].get("key_val_informations", {})
                base_kv.update({f"Treatment judge · {key}": value for key, value in judge_kv.items() if key.startswith("Judge")})
            root_row = {
                "meta_data": {"row_idx": len(audit_rows) + 1, "evalset_item_id": slug, "key_val_informations": base_kv},
                "images": cards(root_rel),
            }
            group_row = copy.deepcopy(root_row)
            group_row["images"] = cards(group_rel)
            report_rows.append(group_row)
            audit_rows.append(root_row)
        rows_by_group[group] = report_rows

    root_links = {}
    group_manifest = []
    for index, (group, group_rows) in enumerate(rows_by_group.items(), start=1):
        group_dir = REPORT_ROOT / "groups" / group
        group_dir.mkdir(parents=True)
        group_data = {
            "is_secure": True,
            "meta_texts": [
                f"{TITLE} — {group}",
                ["Treatment", {"Version": PIPELINE_VERSION, "Rows": 10, "Ranks": "1–10", "Guard": "unchanged V22.4.3", "Outer retry": "at most one, exact guard rejection only", "Interpretation": "qualitative assembly; not native reliability"}],
            ],
            "rows": group_rows,
        }
        atomic_json(group_dir / "data.json", group_data)
        shutil.copy2(FE_VIEWER, group_dir / "viewer.html")
        url = f"{GATEWAY}/{S3_BUCKET}/{S3_PREFIX}/groups/{group}/viewer.html"
        root_links[f"Bank {index:02d}: {group}"] = url
        group_manifest.append(
            {
                "index": index,
                "group": group,
                "rows": 10,
                "ranks": list(range(1, 11)),
                "data_sha256": sha256_file(group_dir / "data.json"),
                "viewer_sha256": sha256_file(group_dir / "viewer.html"),
                "url": url,
            }
        )

    root_data = {
        "is_secure": True,
        "meta_texts": [
            TITLE,
            [
                "Experiment contract",
                {
                    "Rows": 160,
                    "Banks": 16,
                    "Prompts per bank": 10,
                    "Treatment": PIPELINE_VERSION,
                    "Inputs held fixed": "V6.1 prompts, digital twins, camera tags, Stage-A geometry, and guide images",
                    "Changed": "Stage-B/final product-position policy",
                    "Guard": "Every live output must pass full-affine product invariants; one bounded fixed-position fallback is allowed",
                    "Assembly wrapper": "At most one new outer job after exact guard rejection; first passing job selected",
                    "Reliability claim": "None; protocol rates are reported separately from native V22.4.3",
                    "First-job passes": progress["counts"]["first_job_pass"],
                    "Recovered on retry": progress["counts"]["recovered_on_retry"],
                    "Terminal failures": progress["counts"]["terminal_failure"],
                },
            ],
        ],
        "links": root_links,
        "rows": audit_rows,
    }
    atomic_json(REPORT_ROOT / "data.json", root_data)
    shutil.copy2(FE_VIEWER, REPORT_ROOT / "viewer.html")
    manifest = {
        "schema_version": "hp-position-flex-v22.4.3-r1-grouped-fe-v1",
        "title": TITLE,
        "rows": 160,
        "banks": 16,
        "prompts_per_bank": 10,
        "freeze": str(FREEZE),
        "freeze_sha256": sha256_file(FREEZE),
        "progress": str(PROGRESS),
        "progress_sha256": sha256_file(PROGRESS),
        "optional_treatment_judge_report": str(judge_report) if judge_report else None,
        "optional_treatment_judge_sha256": judge_hash,
        "pipeline_version": PIPELINE_VERSION,
        "assembly_counts": progress["counts"],
        "assembly_rates": progress["rates"],
        "native_reliability_claim": False,
        "publish_destination": f"s3://{S3_BUCKET}/{S3_PREFIX}/",
        "viewer_url": f"{GATEWAY}/{S3_BUCKET}/{S3_PREFIX}/viewer.html",
        "groups": group_manifest,
        "root_data_sha256": sha256_file(REPORT_ROOT / "data.json"),
        "root_viewer_sha256": sha256_file(REPORT_ROOT / "viewer.html"),
    }
    atomic_json(REPORT_ROOT / "build_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-inputs-only", action="store_true")
    parser.add_argument("--judge-report", type=Path)
    args = parser.parse_args()
    result = validate_sources_only() if args.validate_inputs_only else build(args.judge_report)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

