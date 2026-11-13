#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Strictly validate and publish the terminal HP V6.2 surface image run receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image

import run_generation as generation


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def artifact_entry(run_dir: Path, path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(run_dir).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": generation.sha256_path(path),
    }


def validate_local_run(run_dir: Path, release_gate_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = generation.load_json(run_dir / "run_manifest.json")
    queue = generation.load_json(run_dir / "queue_manifest.json")
    prompts_path = run_dir / "source/prompts_all_160.json"
    document = generation.load_json(prompts_path)
    rows = generation.interleave(generation.validate_prompt_document(
        document, prompts_path, manifest["prompts_sha256"],
    ))
    for position, row in enumerate(rows, 1):
        row["queue_position"] = position
    expected_queue = generation.queue_document(rows)
    require(queue == expected_queue, "queue manifest differs from the frozen prompt-derived queue")
    require(generation.canonical_sha256(queue) == manifest["queue_manifest_sha256"],
            "queue manifest hash differs from immutable run identity")
    require(manifest["run_sha256"] == generation.canonical_sha256({
        key: value for key, value in manifest.items() if key != "run_sha256"
    }), "run manifest self-hash differs")

    by_id = {row["row_id"]: row for row in rows}
    records = [generation.load_json(path) for path in sorted((run_dir / "records").glob("*.json"))]
    require(len(records) == generation.EXPECTED_COUNT, f"expected 160 records, found {len(records)}")
    require({record.get("row_id") for record in records} == set(by_id), "terminal record keys differ from frozen queue")
    require(all(record.get("status") == "done" for record in records), "every terminal record must be done")
    require(len(list((run_dir / "images").glob("*.png"))) == generation.EXPECTED_COUNT,
            "image directory must contain exactly 160 PNG files")
    require(len(list((run_dir / "jobs").glob("*.json"))) == generation.EXPECTED_COUNT,
            "jobs directory must contain exactly 160 job journals")

    device_counts: Counter[str] = Counter()
    view_counts: Counter[str] = Counter()
    bank_counts: Counter[str] = Counter()
    dimensions: Counter[str] = Counter()
    image_artifacts: list[dict[str, Any]] = []
    lineage = manifest["lineage"]
    expected_endpoint_lineage = {
        "candidateId": lineage["label"], "sourceCommit": lineage["source_commit"],
        "patchSha256": lineage["patch_sha256"], "codeTreeSha256": lineage["runtime_tree_sha256"],
        "candidateManifestSha256": lineage["source_manifest_sha256"],
        "configSha256": lineage["candidate_config_sha256"],
        "deploymentManifestSha256": lineage["deployment_manifest_sha256"],
        "pipelineVersion": lineage["pipelineVersion"], "generator": lineage["generator"],
        "rewriterVersion": lineage["rewriterVersion"],
        "textModel": lineage["scene_contract"]["textModel"],
        "imageModel": lineage["scene_contract"]["imageModel"],
    }
    for record in records:
        row = by_id[record["row_id"]]
        require(generation.valid_completed_record(run_dir, row) is not None,
                f"invalid completed record or image binding: {row['row_id']}")
        require(record.get("prompt_record_sha256") == row["prompt_record_sha256"],
                f"prompt record hash differs: {row['row_id']}")
        for key, expected in (
            ("device_id", row["device_id"]), ("digital_twin_id", row["digital_twin_id"]),
            ("camera_id", row["camera_id"]), ("prompt", row["prompt"]["text"]),
            ("prompt_sha256", row["prompt_sha256"]),
        ):
            require(record.get(key) == expected, f"record {key} binding differs: {row['row_id']}")
        require(record.get("run_sha256") == manifest["run_sha256"], f"run hash differs: {row['row_id']}")
        require(record.get("catalog_sha256") == manifest["catalog_sha256"],
                f"catalog hash differs: {row['row_id']}")
        require(record.get("lineage") == manifest["lineage"], f"lineage differs: {row['row_id']}")
        job = generation.load_json(generation.paths(run_dir, row)["job"])
        status = generation.load_json(generation.paths(run_dir, row)["status"])
        expected_request = {
            "digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"],
            "prompt": row["prompt"]["text"],
        }
        require(job.get("request") == expected_request, f"saved request differs: {row['row_id']}")
        require(job.get("request_sha256") == generation.canonical_sha256(expected_request),
                f"saved request hash differs: {row['row_id']}")
        require(job.get("run_sha256") == manifest["run_sha256"] and job.get("lineage") == lineage,
                f"saved job run/lineage differs: {row['row_id']}")
        endpoint_lineage = status.get("candidateLineage") or {}
        for key, expected in expected_endpoint_lineage.items():
            require(endpoint_lineage.get(key) == expected,
                    f"endpoint deployment lineage differs: {row['row_id']} {key}")
        scene = (status.get("stages") or {}).get("scene") or {}
        require(status.get("done") is True and scene.get("status") == "done" and scene.get("has_image") is True,
                f"endpoint status is not terminal scene success: {row['row_id']}")
        evidence = record.get("image_input_order_evidence")
        generation.validate_scene_detail(scene.get("detail") or {}, row, manifest["lineage"], evidence)
        if evidence is not None:
            item = generation.paths(run_dir, row)
            require(generation.sha256_path(item["debug"]) == evidence.get("debug_response_sha256"),
                    f"debug response hash differs: {row['row_id']}")
            require(generation.sha256_path(item["calls"]) == evidence.get("calls_evidence_sha256"),
                    f"calls evidence hash differs: {row['row_id']}")
            require(generation.sha256_path(item["guide"]) == evidence.get("guide_sha256"),
                    f"guide hash differs: {row['row_id']}")
            debug = generation.load_json(item["debug"])
            debug_input = (debug.get("job") or {}).get("input") or {}
            hero_detail = ((debug.get("status") or {}).get("stages") or {}).get("hero", {}).get("detail") or {}
            require(debug_input.get("productSha256") == hero_detail.get("productSha256"),
                    f"debug product/twin hash binding differs: {row['row_id']}")
            require(((debug.get("job") or {}).get("request") or {}).get("digitalTwinId") == row["digital_twin_id"],
                    f"debug digital twin binding differs: {row['row_id']}")
            require(((debug.get("job") or {}).get("request") or {}).get("cameraId") == row["camera_id"],
                    f"debug camera binding differs: {row['row_id']}")
            proven = generation.validate_debug_image_input_evidence(
                debug, evidence["guide_sha256"], row, job, status,
                manifest["lineage"],
            )
            for key in ("method", "proven_order", "guide_sha256", "output_sha256", "image_call"):
                require(evidence.get(key) == proven.get(key), f"saved debug proof differs: {row['row_id']} {key}")
        image_path = generation.paths(run_dir, row)["image"]
        with Image.open(image_path) as image:
            require(image.format == "PNG", f"output is not PNG: {row['row_id']}")
            require(image.size == generation.EXPECTED_SIZE, f"output dimensions differ: {row['row_id']}")
            dimensions[f"{image.width}x{image.height}"] += 1
        device_counts[row["device_id"]] += 1
        view_counts[f"{row['device_id']}::{row['camera_id']}"] += 1
        bank_counts[row["bank_id"]] += 1
        image_artifacts.append(artifact_entry(run_dir, image_path))

    require(device_counts == Counter({device: 40 for device in generation.DEVICE_ORDER}),
            f"device coverage differs: {dict(device_counts)}")
    require(set(view_counts.values()) == {10} and len(view_counts) == 16,
            f"device/view coverage differs: {dict(view_counts)}")
    require(set(bank_counts.values()) == {10} and len(bank_counts) == 16,
            f"bank coverage differs: {dict(bank_counts)}")

    sources = generation.load_json(run_dir / "source/source_manifest.json")
    require(sources.get("sha256") == manifest["prompts_sha256"], "materialized source manifest hash differs")
    bank_inputs = generation.load_json(run_dir / "source/bank_inputs_manifest.json")
    require(len(bank_inputs.get("assets") or {}) == 16, "source bank-input manifest must contain 16 assets")
    for name, item in bank_inputs["assets"].items():
        path = Path(item["materialized_path"])
        require(path.is_file() and generation.sha256_path(path) == item["sha256"],
                f"source bank input changed: {name}")
    twins = generation.load_json(run_dir / "twin_manifest.json")
    require(len(twins.get("assets") or {}) == 16, "twin manifest must contain 16 assets")
    for name, item in twins["assets"].items():
        path = run_dir / "twins" / name
        require(path.is_file() and generation.sha256_path(path) == item["sha256"], f"twin changed: {name}")

    release_gate = generation.load_json(release_gate_path)
    require(release_gate.get("passed_release_gate") is True, "smoke release gate did not pass")
    require(release_gate.get("run_sha256") == manifest["run_sha256"], "release gate belongs to another run")
    require(release_gate.get("source_prompts_sha256") == manifest["prompts_sha256"],
            "release gate belongs to another prompt set")
    deployment_manifest_path = Path(__file__).resolve().parent / "local_scene_endpoint/deployment_manifest.json"
    require(deployment_manifest_path.is_file(), "frozen deployment manifest is missing")
    require(generation.sha256_path(deployment_manifest_path) == lineage["deployment_manifest_sha256"],
            "frozen deployment manifest hash differs from run lineage")

    report_manifest = generation.load_json(run_dir / "report/build_manifest.json")
    report_data = generation.load_json(run_dir / "report/data.json")
    require(report_manifest.get("run_identity") == manifest, "report run identity differs")
    require(report_manifest.get("rows") == 160 and len(report_manifest.get("groups") or []) == 16,
            "report must contain 160 rows and 16 groups")
    require(all(group.get("rows") == 10 for group in report_manifest["groups"]),
            "every report group must contain 10 rows")
    require(len(report_data.get("rows") or []) == 160, "native FE root data must contain 160 rows")
    require(report_manifest.get("judgment_count") == 0 and report_manifest.get("pending_judgment_count") == 160,
            "report must retain all judgments as pending")
    distribution = report_manifest.get("distribution") or {}
    require(distribution.get("text_rows") == 160 and distribution.get("generated_artifacts") == 160,
            "distribution report must distinguish 160 text rows and 160 generated artifacts")
    distribution_manifest = generation.load_json(run_dir / "report/distribution/build_manifest.json")
    require(distribution_manifest.get("source_prompts_sha256") == manifest["prompts_sha256"],
            "distribution report source prompt binding differs")
    distribution_analysis = generation.load_json(run_dir / "report/distribution/downloads/analysis.json")
    require((distribution_analysis.get("scope") or {}).get("text_prompt_rows") == 160,
            "distribution analysis text row count differs")
    require((distribution_analysis.get("scope") or {}).get("generated_artifact_count") == 160,
            "distribution analysis generated artifact count differs")

    local = {
        "terminal_record_count": len(records), "done_count": len(records), "failed_count": 0,
        "image_count": len(image_artifacts), "image_dimensions": dict(dimensions),
        "device_counts": dict(sorted(device_counts.items())),
        "device_view_counts": dict(sorted(view_counts.items())),
        "bank_counts": dict(sorted(bank_counts.items())),
        "queue_complete": True,
        "source_binding": {
            "prompts_sha256": manifest["prompts_sha256"],
            "queue_manifest_sha256": manifest["queue_manifest_sha256"],
            "source_bank_input_count": 16, "twin_count": 16,
            "release_gate_path": str(release_gate_path.resolve()),
            "release_gate_sha256": generation.sha256_path(release_gate_path),
            "deployment_manifest_path": str(deployment_manifest_path),
            "deployment_manifest_sha256": generation.sha256_path(deployment_manifest_path),
        },
        "report": {
            "rows": 160, "groups": 16, "rows_per_group": 10,
            "judgments": 0, "pending_judgments": 160,
            "distribution_text_rows": 160, "distribution_generated_artifacts": 160,
            "viewer_url": report_manifest["viewer_url"],
        },
    }
    return local, image_artifacts


def verify_s3(run_dir: Path, manifest: dict[str, Any], fallback_creds: Path) -> dict[str, Any]:
    paths = [
        path for path in generation.publishable_paths(run_dir)
        if path.name not in {"final_validation.json", "completion_report.md"}
    ]
    client = generation.s3_client(manifest["bucket"], fallback_creds)
    entries = []
    for path in paths:
        entry = artifact_entry(run_dir, path)
        key = f"{manifest['prefix'].rstrip('/')}/{entry['path']}"
        remote = client.head_object(Bucket=manifest["bucket"], Key=key)
        require(remote["ContentLength"] == entry["bytes"], f"S3 byte count differs: {entry['path']}")
        response = client.get_object(Bucket=manifest["bucket"], Key=key)
        digest = hashlib.sha256()
        streamed = 0
        for chunk in response["Body"].iter_chunks(chunk_size=8 * 1024 * 1024):
            if chunk:
                digest.update(chunk)
                streamed += len(chunk)
        require(streamed == entry["bytes"], f"S3 streamed byte count differs: {entry['path']}")
        require(digest.hexdigest() == entry["sha256"], f"S3 content SHA-256 differs: {entry['path']}")
        entry.update({"s3_key": key, "s3_bytes": remote["ContentLength"],
                      "s3_etag": str(remote.get("ETag") or "").strip('"'),
                      "remote_sha256": digest.hexdigest(), "verification": "remote_get_sha256"})
        entries.append(entry)
    return {
        "scope": "all allowlisted public run artifacts present before this final receipt; streaming S3 GET SHA-256 equals local SHA-256",
        "verified": True, "artifact_count": len(entries),
        "artifact_manifest_sha256": generation.canonical_sha256(entries),
        "artifacts": entries,
    }


def completion_markdown(validation: dict[str, Any]) -> str:
    local, remote = validation["local_validation"], validation["s3_verification"]
    return (
        "# HP V6.2 Surface Diversity image-run completion\n\n"
        f"Validated at: {validation['validated_at_utc']}\n\n"
        f"Run SHA-256: `{validation['run_sha256']}`\n\n"
        f"Frozen prompts SHA-256: `{validation['source_prompts_sha256']}`\n\n"
        f"Terminal outputs: {local['done_count']} done, {local['failed_count']} failed. "
        "All outputs are 2368×1776 PNG files.\n\n"
        "Coverage: 4 devices × 4 fixed views × 10 prompts; every device/view bank contains 10 outputs.\n\n"
        f"Public artifact verification: {remote['artifact_count']} S3 objects matched local streaming SHA-256 hashes; "
        f"local artifact manifest SHA-256 `{remote['artifact_manifest_sha256']}`.\n\n"
        f"Gallery: {local['report']['viewer_url']}\n\n"
        "Judgments: 0 copied or created; all 160 rows remain pending judgment.\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--release-gate", type=Path, required=True)
    parser.add_argument("--fallback-creds", type=Path,
                        default=Path.home() / ".claude/hshariati/aws_creds.env")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    manifest = generation.load_json(run_dir / "run_manifest.json")
    local, _ = validate_local_run(run_dir, args.release_gate.resolve())
    remote = verify_s3(run_dir, manifest, args.fallback_creds.resolve())
    validation = {
        "schema_version": 1, "validated_at_utc": generation.now(),
        "status": "complete", "run_sha256": manifest["run_sha256"],
        "source_prompts_sha256": manifest["prompts_sha256"],
        "lineage": manifest["lineage"], "local_validation": local,
        "s3_verification": remote,
    }
    generation.atomic_json(run_dir / "final_validation.json", validation)
    (run_dir / "completion_report.md").write_text(completion_markdown(validation), encoding="utf-8")
    client = generation.s3_client(manifest["bucket"], args.fallback_creds.resolve())
    final_receipts = []
    for name in ("final_validation.json", "completion_report.md"):
        path = run_dir / name
        key = f"{manifest['prefix'].rstrip('/')}/{name}"
        client.upload_file(str(path), manifest["bucket"], key,
                           ExtraArgs={"ContentType": generation.content_type(path)})
        head = client.head_object(Bucket=manifest["bucket"], Key=key)
        require(head["ContentLength"] == path.stat().st_size, f"final receipt S3 byte count differs: {name}")
        response = client.get_object(Bucket=manifest["bucket"], Key=key)
        digest = hashlib.sha256()
        streamed = 0
        for chunk in response["Body"].iter_chunks(chunk_size=8 * 1024 * 1024):
            if chunk:
                digest.update(chunk)
                streamed += len(chunk)
        require(streamed == path.stat().st_size and digest.hexdigest() == generation.sha256_path(path),
                f"final receipt S3 content differs: {name}")
        final_receipts.append({**artifact_entry(run_dir, path), "s3_key": key,
                               "s3_bytes": head["ContentLength"],
                               "s3_etag": str(head.get("ETag") or "").strip('"'),
                               "remote_sha256": digest.hexdigest(),
                               "verification": "remote_get_sha256"})
    print(json.dumps({
        "final_validation": str(run_dir / "final_validation.json"),
        "final_validation_sha256": generation.sha256_path(run_dir / "final_validation.json"),
        "completion_report": str(run_dir / "completion_report.md"),
        "completion_report_sha256": generation.sha256_path(run_dir / "completion_report.md"),
        "final_receipts": final_receipts,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
