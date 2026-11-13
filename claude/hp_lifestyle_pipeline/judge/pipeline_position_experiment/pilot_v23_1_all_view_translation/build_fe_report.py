#!/usr/bin/env python3
"""Build the local V23.1 eight-row FE review report after pilot completion.

This program performs no upload. It refuses to build before all eight frozen
rows have completed successfully and hash-validates every source, input,
terminal provenance record, and artifact before copying review assets.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from common import atomic_json, load_json, require, sha256_file
from config import (
    FREEZE,
    JOB_ROOT,
    PIPELINE_VERSION,
    PROGRESS,
    ROOT,
    SOURCE_HASHES,
)
from preflight import verify as verify_preflight
from run_pilot import job_id, validate_terminal

TITLE = "HP V23.1 all-view rigid-translation pilot — representative and movement-demand cases"
REPORT_ROOT = ROOT / "review_report"
VIEWER = Path("/home/colligo/.claude/scripts/fe_html/annotation_viewer.html")
S3_BUCKET = "foundry-hp-enterprise-adobe-assets"
S3_PREFIX = "hp_position_flex_v23_1_pilot_20261106/review"
PUBLISH_DESTINATION = f"s3://{S3_BUCKET}/{S3_PREFIX}/"
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"
BASE_VIEWER_URL = f"{GATEWAY}/{S3_BUCKET}/{S3_PREFIX}/viewer.html"

QUESTION = {
    "text": "Is the product placement natural, usable, and physically integrated with the scene?",
    "hard_check": False,
    "comment_box": True,
    "group": "Natural placement",
    "rubric": {
        "key": "pass",
        "name": "Pass / Fail / Borderline",
        "options": [
            {"value": "pass", "label": "Pass", "tone": "good"},
            {"value": "fail", "label": "Fail", "tone": "bad"},
            {"value": "borderline", "label": "Borderline", "tone": "neutral"},
        ],
    },
}


def review_url(ldap: str = "hshariati") -> str:
    payload = base64.b64encode(json.dumps([QUESTION], separators=(",", ":")).encode()).decode()
    return f"{BASE_VIEWER_URL}?{urlencode({'q': payload, 'ldap': ldap})}"


def static_contract() -> dict:
    preflight = verify_preflight(allow_progress=True)
    require(preflight["rows"] == 8, "preflight row count changed")
    require(VIEWER.is_file(), f"missing canonical FE viewer: {VIEWER}")
    require(PUBLISH_DESTINATION == (
        "s3://foundry-hp-enterprise-adobe-assets/"
        "hp_position_flex_v23_1_pilot_20261106/review/"
    ), "publish prefix changed")
    return {
        "ok": True,
        "rows": 8,
        "title": TITLE,
        "publish_destination": PUBLISH_DESTINATION,
        "viewer": str(VIEWER),
        "review_url": review_url(),
        "build_performed": False,
        "upload_performed": False,
    }


def link_or_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    require(source.is_file(), f"missing asset: {source}")
    require(not destination.exists(), f"refusing to overwrite report asset: {destination}")
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)
    require(sha256_file(destination) == sha256_file(source), f"copied asset differs: {destination}")


def artifact_by_name(provenance: dict, basename: str) -> dict:
    matches = [item for item in provenance["artifacts"].values()
               if Path(item["path"]).name == basename]
    require(len(matches) == 1, f"expected one {basename}, found {len(matches)}")
    item = matches[0]
    path = Path(item["path"])
    require(path.is_file() and sha256_file(path) == item["sha256"],
            f"artifact hash mismatch: {basename}")
    require(path.stat().st_size == item["bytes"], f"artifact size mismatch: {basename}")
    return item


def checked_input(provenance: dict, name: str) -> dict:
    item = provenance["input_artifacts"][name]
    path = Path(item["path"])
    require(path.is_file() and sha256_file(path) == item["sha256"],
            f"input hash mismatch: {name}")
    return item


def image_card(src: str, label: str, role: str = "model_input", **meta: Any) -> dict:
    return {
        "asset_type": "image",
        "is_model_input_or_output": role,
        "image_src": src,
        "meta_text": {"label": label, **meta},
    }


def text_card(content: str, label: str) -> dict:
    return {"asset_type": "text", "text_content": content, "meta_text": {"label": label}}


def number(value: Any, digits: int = 2) -> str:
    return "unavailable" if not isinstance(value, (int, float)) else f"{value:.{digits}f}"


def guard_summary(guard: dict) -> str:
    lines = []
    for index, attempt in enumerate(guard.get("attempts", []), 1):
        singular = attempt.get("singular_values")
        lines.append(
            f"Attempt {index}: {attempt.get('verdict')} | "
            f"translation=({number(attempt.get('translation_x_px'), 1)}, "
            f"{number(attempt.get('translation_y_px'), 1)}) px | "
            f"inliers={attempt.get('inliers', 'unavailable')} | "
            f"inlier ratio={number(attempt.get('inlier_ratio'), 3)} | "
            f"rotation={number(attempt.get('rotation_deg'), 3)}° | "
            f"singular={singular if singular is not None else 'unavailable'} | "
            f"residual p95={number(attempt.get('residual_p95_px'), 3)} px | "
            f"branch={attempt.get('verification_branch', attempt.get('method', 'affine'))} | "
            f"reasons={attempt.get('reasons', [])}"
        )
    return "\n".join(lines)


def stage_b_text(provenance: dict) -> str:
    blocks = []
    for index in range(1, len(provenance["stage_b_attempts"]) + 1):
        response_item = artifact_by_name(provenance, f"stage_b_attempt_{index}_response.json")
        response = load_json(Path(response_item["path"]))
        require(isinstance(response.get("prompt"), str) and response["prompt"].strip(),
                f"Stage-B attempt {index} lacks rewritten prompt")
        blocks.append(f"STAGE-B ATTEMPT {index}\n\n{response['prompt']}")
    return "\n\n---\n\n".join(blocks)


def executable_prompt_text(provenance: dict) -> str:
    blocks = []
    for index in range(1, int(provenance["image_calls"]) + 1):
        request_item = artifact_by_name(provenance, f"image_request_attempt_{index}.json")
        request = load_json(Path(request_item["path"]))
        require(isinstance(request.get("prompt"), str) and request["prompt"].strip(),
                f"image attempt {index} lacks executable prompt")
        blocks.append(f"IMAGE ATTEMPT {index}\n\n{request['prompt']}")
    return "\n\n---\n\n".join(blocks)


def completed_rows() -> tuple[dict, list[tuple[dict, dict, dict]]]:
    static_contract()
    require(PROGRESS.is_file(), f"pilot progress missing: {PROGRESS}")
    progress = load_json(PROGRESS)
    freeze = load_json(FREEZE)
    expected = [item["row_slug"] for item in freeze["records"]]
    require(progress.get("complete") is True, "pilot is incomplete; report build is forbidden")
    require(progress.get("first_failure") is None, "pilot has a preserved first failure")
    require(progress.get("total") == 8 and progress.get("done") == expected,
            "completed row order/set differs from freeze")
    require(set(progress.get("rows", {})) == set(expected), "progress row map differs from freeze")
    verified = []
    for item in freeze["records"]:
        slug = item["row_slug"]
        status_path = JOB_ROOT / job_id(slug) / "status.json"
        require(status_path.is_file(), f"missing terminal status: {slug}")
        status = load_json(status_path)
        success, provenance = validate_terminal(slug, status)
        require(success, f"row did not complete successfully: {slug}")
        require(provenance["cohort"] == item["cohort"], f"cohort differs: {slug}")
        require(provenance["source_row_slug"] == item["source_row_slug"],
                f"source row differs: {slug}")
        require(provenance["prompt_sha256"] == item["prompt_sha256"],
                f"scene prompt differs: {slug}")
        require(provenance["pipeline_version"] == PIPELINE_VERSION, f"pipeline differs: {slug}")
        require(provenance["source_hashes"] == SOURCE_HASHES, f"source hashes differ: {slug}")
        require(provenance["record"]["sha256"] == item["sha256"], f"record differs: {slug}")
        require(progress["rows"][slug]["job_id"] == job_id(slug), f"progress job differs: {slug}")
        verified.append((item, status, provenance))
    return progress, verified


def build() -> dict:
    progress, verified = completed_rows()
    require(not REPORT_ROOT.exists(), f"refusing to overwrite existing report: {REPORT_ROOT}")
    REPORT_ROOT.mkdir(parents=True)
    rows = []
    row_manifest = []
    for row_index, (item, status, provenance) in enumerate(verified, 1):
        slug = item["row_slug"]
        guard = provenance["product_invariant_guard"]
        selected_attempt = guard["selected_attempt"]
        require(selected_attempt in range(1, int(provenance["image_calls"]) + 1),
                f"selected attempt out of range: {slug}")
        selected = artifact_by_name(provenance, "ours.png")
        selected_raw = artifact_by_name(provenance, f"gpt_{selected_attempt}.png")
        require(selected["sha256"] == selected_raw["sha256"], f"selected output differs: {slug}")
        guide = artifact_by_name(provenance, "geometry_guide.png")
        input_guide = checked_input(provenance, "guide.png")
        require(guide["sha256"] == input_guide["sha256"], f"guide replay differs: {slug}")
        product = checked_input(provenance, "product.png")
        checked_input(provenance, "reference.png")

        asset_dir = REPORT_ROOT / "assets" / slug
        link_or_copy(Path(product["path"]), asset_dir / "digital_twin.png")
        link_or_copy(Path(guide["path"]), asset_dir / "guide.png")
        link_or_copy(Path(selected["path"]), asset_dir / "selected.png")
        attempts = []
        for attempt_index in range(1, int(provenance["image_calls"]) + 1):
            raw = artifact_by_name(provenance, f"gpt_{attempt_index}.png")
            destination = asset_dir / f"attempt_{attempt_index}.png"
            link_or_copy(Path(raw["path"]), destination)
            attempts.append({"attempt": attempt_index, "sha256": raw["sha256"]})

        guard_text = guard_summary(guard)
        rewritten = stage_b_text(provenance)
        executable = executable_prompt_text(provenance)
        raw_debug = {
            "status": status,
            "progress": progress["rows"][slug],
            "provenance": provenance,
        }
        cards = [
            image_card(f"assets/{slug}/digital_twin.png", "Digital twin render"),
            image_card(f"assets/{slug}/guide.png", "Frozen geometry guide"),
        ]
        for attempt_index, metric in enumerate(guard["attempts"], 1):
            cards.append(image_card(
                f"assets/{slug}/attempt_{attempt_index}.png",
                f"Raw image attempt {attempt_index}",
                "model_output",
                **{
                    "Guard verdict": metric.get("verdict"),
                    "Translation x px": metric.get("translation_x_px"),
                    "Translation y px": metric.get("translation_y_px"),
                    "Inlier ratio": metric.get("inlier_ratio"),
                },
            ))
        cards.extend([
            image_card(
                f"assets/{slug}/selected.png",
                "Selected output",
                "model_output",
                **{"Selected attempt": selected_attempt},
            ),
            text_card(item["prompt"], "Scene prompt"),
            text_card(rewritten, "Stage-B rewritten prompt"),
            text_card(executable, "Executable image prompt"),
            text_card(guard_text, "Guard verdict and localization metrics"),
        ])
        kv = {
            "Cohort": item["cohort"],
            "Device": item["device_id"],
            "Device type": item["device_type"],
            "Camera": item["camera_tag"],
            "Execution row": slug,
            "Source V6.1 row": item["source_row_slug"],
            "Scene prompt": item["prompt"],
            "Image attempts": provenance["image_calls"],
            "Selected attempt": selected_attempt,
            "Guard outcomes": " → ".join(x["verdict"] for x in guard["attempts"]),
            "Guard metrics": guard_text,
            "Pipeline version": PIPELINE_VERSION,
            "Prompt SHA-256": item["prompt_sha256"],
            "Selected output SHA-256": selected["sha256"],
            "Provenance SHA-256": status["provenanceSha256"],
            "Provenance/debug JSON": json.dumps(raw_debug, indent=2),
        }
        rows.append({
            "meta_data": {
                "row_idx": row_index,
                "evalset_item_id": slug,
                "key_val_informations": kv,
            },
            "images": cards,
        })
        row_manifest.append({
            "row_slug": slug,
            "cohort": item["cohort"],
            "source_row_slug": item["source_row_slug"],
            "status_sha256": sha256_file(JOB_ROOT / job_id(slug) / "status.json"),
            "provenance_sha256": status["provenanceSha256"],
            "digital_twin_sha256": product["sha256"],
            "guide_sha256": guide["sha256"],
            "attempts": attempts,
            "selected_attempt": selected_attempt,
            "selected_sha256": selected["sha256"],
        })

    data = {
        "is_secure": True,
        "meta_texts": [
            TITLE,
            [
                "Frozen evaluation contract",
                {
                    "Rows": 8,
                    "Representative V6.1 cases": 4,
                    "Movement-demand diagnostics": 4,
                    "Treatment": PIPELINE_VERSION,
                    "Execution": "one immutable outer job per row; serial; stop on first failure",
                    "Inputs held fixed": "digital twin, style reference, Stage-A response, geometry guide",
                    "Review setup": QUESTION["text"],
                    "Debug": "Open Row details for collapsible provenance/debug JSON",
                },
            ],
        ],
        "rows": rows,
    }
    atomic_json(REPORT_ROOT / "data.json", data)
    shutil.copy2(VIEWER, REPORT_ROOT / "viewer.html")
    manifest = {
        "schema_version": "hp-position-flex-v23.1-eight-row-fe-v1",
        "title": TITLE,
        "rows": 8,
        "freeze": str(FREEZE),
        "freeze_sha256": sha256_file(FREEZE),
        "progress": str(PROGRESS),
        "progress_sha256": sha256_file(PROGRESS),
        "pipeline_version": PIPELINE_VERSION,
        "source_hashes": SOURCE_HASHES,
        "question": QUESTION,
        "publish_destination": PUBLISH_DESTINATION,
        "viewer_url": BASE_VIEWER_URL,
        "review_url": review_url(),
        "upload_performed": False,
        "rows_manifest": row_manifest,
        "data_sha256": sha256_file(REPORT_ROOT / "data.json"),
        "viewer_sha256": sha256_file(REPORT_ROOT / "viewer.html"),
    }
    atomic_json(REPORT_ROOT / "build_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-static-only", action="store_true")
    args = parser.parse_args()
    result = static_contract() if args.validate_static_only else build()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
