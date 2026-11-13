#!/usr/bin/env python3
"""Build and verify a leak-resistant leave-family-out visual calibration plan.

This creates artifacts only. It never calls a model and never changes the frozen V4 run.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image

HERE = Path(__file__).resolve().parent
V4 = HERE.parent
MANIFEST = V4 / "data/development_15_manifest.json"
EXPECTATIONS = V4 / "data/development_15_expectations.json"
GUIDANCE = HERE / "anchor_guidance.json"
CATALOG = HERE / "anchor_catalog.json"
PLAN = HERE / "target_anchor_plan.json"
IMAGE_DIR = HERE / "anchors/images"
MAX_ANCHORS = 4
MAX_LONG_EDGE = 768
JPEG_QUALITY = 78
CLUSTER_GROUP = {
    "chair_calibration": "chair",
    "support_layout_geometry": "support_layout",
    "support_room_placement": "support_layout",
    "support_layout_and_prop_coherence": "support_layout",
    "support_anatomy": "support_anatomy",
    "device_room_position": "device_position",
    "device_axis_and_prop_coherence": "device_position",
    "crop_observability": "observation_scope",
    "artifact_scope": "observation_scope",
}
CATEGORY_PRIORITY = {
    "laptop": ["chair", "support_layout", "support_anatomy", "observation_scope"],
    "printer": ["support_layout", "support_anatomy", "device_position", "observation_scope"],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_camera(record: dict[str, Any]) -> str:
    return record["view"]["camera_tag"].split("_", 1)[1]


def prompt_rank(record: dict[str, Any]) -> str:
    return record["candidate_id"]


def exact_family(record: dict[str, Any]) -> str:
    return "|".join((record["device"], normalized_camera(record), prompt_rank(record)))


def broad_family(record: dict[str, Any]) -> str:
    return "|".join((record["device_type"], normalized_camera(record), prompt_rank(record)))


def make_thumbnail(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((MAX_LONG_EDGE, MAX_LONG_EDGE), Image.Resampling.LANCZOS)
        image.save(destination, format="JPEG", quality=JPEG_QUALITY, optimize=True)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    expectations = json.loads(EXPECTATIONS.read_text())
    guidance = json.loads(GUIDANCE.read_text())
    records = {row["id"]: row for row in manifest["records"]}
    expectation_rows = {row["record_id"]: row for row in expectations["records"]}
    guidance_rows = {row["record_id"]: row for row in guidance["anchors"]}
    if len(guidance_rows) != len(guidance["anchors"]):
        raise RuntimeError("Duplicate anchor guidance record_id")
    if set(guidance_rows) - set(records):
        raise RuntimeError("Anchor guidance references an unknown manifest record")

    anchors = []
    for anchor_id, guide in guidance_rows.items():
        record = records[anchor_id]
        expected = expectation_rows[anchor_id]
        if not expected["verdict_labeled"] or expected["explicit_verdict"] != guide["calibration_verdict"]:
            raise RuntimeError(f"Calibration verdict/provenance mismatch for {anchor_id}")
        source = Path(record["generated_image"]["local_path"])
        if sha256_file(source) != record["generated_image"]["sha256"]:
            raise RuntimeError(f"Source image hash mismatch for {anchor_id}")
        thumbnail = IMAGE_DIR / f"{anchor_id}.jpg"
        make_thumbnail(source, thumbnail)
        anchors.append({
            "anchor_id": anchor_id,
            "product_type": record["device_type"],
            "device": record["device"],
            "camera": normalized_camera(record),
            "prompt_rank": prompt_rank(record),
            "exact_family": exact_family(record),
            "near_duplicate_family": broad_family(record),
            "generated_image_sha256": record["generated_image"]["sha256"],
            "twin_image_sha256": record["twin_image"]["sha256"],
            "scene_prompt_sha256": record["scene_prompt_sha256"],
            "human_comment_sha256": sha256_bytes(expected["human_comment_exact"].encode()),
            "issue_cluster": guide["issue_cluster"],
            "calibration_category": CLUSTER_GROUP[guide["issue_cluster"]],
            "calibration_verdict": guide["calibration_verdict"],
            "guidance": guide["guidance"],
            "thumbnail": {
                "path": str(thumbnail.resolve()),
                "sha256": sha256_file(thumbnail),
                "max_long_edge": MAX_LONG_EDGE,
                "jpeg_quality": JPEG_QUALITY,
            },
        })

    catalog = {
        "schema_version": "placement-v4-anchor-catalog-v1",
        "source_manifest": str(MANIFEST.resolve()),
        "source_manifest_sha256": sha256_file(MANIFEST),
        "source_expectations": str(EXPECTATIONS.resolve()),
        "source_expectations_sha256": sha256_file(EXPECTATIONS),
        "source_annotation_sha256": expectations["annotation_sha256"],
        "guidance_source": str(GUIDANCE.resolve()),
        "guidance_source_sha256": sha256_file(GUIDANCE),
        "anchor_count": len(anchors),
        "anchors": anchors,
    }
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n")

    plans = []
    for target_id, target in records.items():
        exclusions: dict[str, list[str]] = {}
        eligible = []
        for anchor in anchors:
            reasons = []
            if anchor["generated_image_sha256"] == target["generated_image"]["sha256"]:
                reasons.append("exact_generated_image_hash")
            if anchor["twin_image_sha256"] == target["twin_image"]["sha256"]:
                reasons.append("same_twin_image_hash")
            if anchor["scene_prompt_sha256"] == target["scene_prompt_sha256"]:
                reasons.append("exact_scene_prompt_hash")
            if anchor["exact_family"] == exact_family(target):
                reasons.append("same_device_camera_prompt_rank_family")
            if anchor["near_duplicate_family"] == broad_family(target):
                reasons.append("same_product_type_camera_prompt_rank_near_family")
            if reasons:
                exclusions[anchor["anchor_id"]] = reasons
            else:
                eligible.append(anchor)

        # Deterministic, target-label-independent selection. Categories are chosen only
        # from target product type, never from its annotation. Within each category,
        # prefer the same product type and comparable framing, then catalog order.
        framing = normalized_camera(target)
        eligible.sort(key=lambda a: (
            0 if a["product_type"] == target["device_type"] else 1,
            0 if a["camera"] == framing else 1,
            a["anchor_id"],
        ))
        selected = []
        seen_clusters: set[str] = set()
        for category in CATEGORY_PRIORITY[target["device_type"]]:
            options = [a for a in eligible if a["calibration_category"] == category]
            if options:
                selected.append(options[0])
                seen_clusters.add(options[0]["issue_cluster"])
        for anchor in eligible:
            if len(selected) == MAX_ANCHORS:
                break
            if anchor in selected or anchor["issue_cluster"] in seen_clusters:
                continue
            selected.append(anchor)
            seen_clusters.add(anchor["issue_cluster"])
        if len(selected) < MAX_ANCHORS:
            raise RuntimeError(f"Only {len(selected)} eligible diverse anchors for {target_id}")

        plan = {
            "target_record_id": target_id,
            "target_product_type": target["device_type"],
            "target_device": target["device"],
            "target_camera": framing,
            "target_prompt_rank": prompt_rank(target),
            "target_generated_image_sha256": target["generated_image"]["sha256"],
            "target_twin_image_sha256": target["twin_image"]["sha256"],
            "target_scene_prompt_sha256": target["scene_prompt_sha256"],
            "target_exact_family": exact_family(target),
            "target_near_duplicate_family": broad_family(target),
            "selected_anchor_ids": [anchor["anchor_id"] for anchor in selected],
            "excluded_anchor_ids_with_reasons": exclusions,
        }
        plans.append(plan)

    output = {
        "schema_version": "placement-v4-target-anchor-plan-v1",
        "status": "candidate_only_not_frozen_or_evaluated",
        "target_labels_or_verdicts_in_runtime_target_text": False,
        "maximum_anchor_count": MAX_ANCHORS,
        "selection_uses_target_annotation": False,
        "source_catalog": str(CATALOG.resolve()),
        "source_catalog_sha256": sha256_file(CATALOG),
        "targets": plans,
    }
    PLAN.write_text(json.dumps(output, indent=2) + "\n")
    verify(catalog, output, records)
    print(json.dumps({"catalog": str(CATALOG), "plan": str(PLAN), "anchors": len(anchors), "targets": len(plans)}))


def verify(catalog: dict[str, Any], plan: dict[str, Any], records: dict[str, Any]) -> None:
    anchors = {a["anchor_id"]: a for a in catalog["anchors"]}
    if plan["maximum_anchor_count"] != MAX_ANCHORS or plan["target_labels_or_verdicts_in_runtime_target_text"]:
        raise RuntimeError("Invalid runtime provenance policy")
    for target in plan["targets"]:
        if len(target["selected_anchor_ids"]) > MAX_ANCHORS:
            raise RuntimeError("Anchor limit exceeded")
        if len(set(target["selected_anchor_ids"])) != len(target["selected_anchor_ids"]):
            raise RuntimeError("Duplicate selected anchor")
        target_record = records[target["target_record_id"]]
        for anchor_id in target["selected_anchor_ids"]:
            anchor = anchors[anchor_id]
            violations = []
            if anchor["generated_image_sha256"] == target_record["generated_image"]["sha256"]:
                violations.append("exact image")
            if anchor["twin_image_sha256"] == target_record["twin_image"]["sha256"]:
                violations.append("same twin")
            if anchor["scene_prompt_sha256"] == target_record["scene_prompt_sha256"]:
                violations.append("exact prompt")
            if anchor["exact_family"] == exact_family(target_record):
                violations.append("exact family")
            if anchor["near_duplicate_family"] == broad_family(target_record):
                violations.append("near family")
            if violations:
                raise RuntimeError(f"Leak for {target['target_record_id']} <- {anchor_id}: {violations}")
            thumbnail = Path(anchor["thumbnail"]["path"])
            if sha256_file(thumbnail) != anchor["thumbnail"]["sha256"]:
                raise RuntimeError(f"Thumbnail provenance mismatch: {anchor_id}")


if __name__ == "__main__":
    main()
