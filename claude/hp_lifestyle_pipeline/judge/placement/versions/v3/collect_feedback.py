#!/usr/bin/env python3
"""Collect and normalize natural-placement free-text feedback.

The default mode is fully offline and deterministic: it verifies the immutable
annotation snapshots named by ``data/feedback_20261105/manifest.json``, joins
every persisted annotation row to the v2 asset and actual run by ID, and writes
``data/comment_inventory.json``.

``--refresh-s3`` is an explicit read-only refresh. It obtains temporary Foundry
AWS credentials, downloads each configured annotation object, and stores new
content under a SHA-256-versioned filename. It never writes to S3 and never
overwrites an existing snapshot.

Human Pass/Review/Fail answers are intentionally excluded. UI completion is
retained only as source metadata and never controls inclusion. Both native
fe-html comment channels are preserved verbatim: row ``comment`` and optional
``question_comments``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
V2_ROOT = ROOT.parent / "v2"
DEFAULT_SNAPSHOT_DIR = ROOT / "data" / "feedback_20261105"
DEFAULT_MANIFEST = DEFAULT_SNAPSHOT_DIR / "manifest.json"
DEFAULT_OUTPUT = ROOT / "data" / "comment_inventory.json"
DEFAULT_ASSETS = V2_ROOT / "data" / "v6_assets.json"
DEFAULT_RUNS_ROOT = V2_ROOT / "runs" / "v6_batch_v1"
AWS_CREDENTIAL_HELPER = Path.home() / ".claude" / "scripts" / "foundry_aws_creds.py"
AWS_CREDENTIAL_ENV = Path.home() / ".claude" / "hshariati" / "aws_creds.env"
EXPECTED_ANNOTATION_SCHEMA = "fe-html/annotations@1"

DEFAULT_SOURCES = {
    "printers": (
        "s3://foundry-hp-enterprise-adobe-assets/eval_sets/"
        "hp_natural_placement_judge_v2_v6_20261104/printers/annotations/"
        "reviewer_0.json"
    ),
    "laptops": (
        "s3://foundry-hp-enterprise-adobe-assets/eval_sets/"
        "hp_natural_placement_judge_v2_v6_20261104/laptops/annotations/"
        "reviewer_0.json"
    ),
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(rendered)
        temp_path = Path(handle.name)
    temp_path.chmod(0o644)
    os.replace(temp_path, path)


def require_mapping(value: Any, *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a JSON object")
    return value


def require_string(value: Any, *, label: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        suffix = "" if allow_empty else " non-empty"
        raise ValueError(f"{label} must be a{suffix} string")
    return value


def unique_index(records: Sequence[Mapping[str, Any]], key: str, *, label: str) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for record in records:
        record_id = require_string(record.get(key), label=f"{label}.{key}")
        if record_id in indexed:
            raise ValueError(f"Duplicate {label} ID: {record_id}")
        indexed[record_id] = record
    return indexed


def parse_source_args(values: Sequence[str]) -> dict[str, str]:
    sources = dict(DEFAULT_SOURCES)
    for value in values:
        family, separator, uri = value.partition("=")
        if not separator or not family or not uri.startswith("s3://"):
            raise ValueError("--source must have the form FAMILY=s3://bucket/key")
        sources[family] = uri
    return sources


def s3_bucket_key(uri: str) -> tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path.lstrip("/"):
        raise ValueError(f"Malformed S3 URI: {uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def run_with_aws_credentials(command: Sequence[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    """Run one AWS command after sourcing broker credentials in that shell."""
    if not AWS_CREDENTIAL_ENV.is_file():
        raise ValueError(f"AWS credential environment file was not created: {AWS_CREDENTIAL_ENV}")
    shell = 'set -a; source "$1"; set +a; shift; exec "$@"'
    return subprocess.run(
        ["bash", "-c", shell, "collect_feedback", str(AWS_CREDENTIAL_ENV), *command],
        check=True,
        text=True,
        capture_output=capture_output,
    )


def refresh_credentials() -> None:
    if not AWS_CREDENTIAL_HELPER.is_file():
        raise ValueError(f"Missing Foundry AWS credential helper: {AWS_CREDENTIAL_HELPER}")
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("uv is required to run the Foundry AWS credential helper")
    subprocess.run(
        [uv, "run", "--script", str(AWS_CREDENTIAL_HELPER)],
        check=True,
    )


def refresh_snapshots(
    *, snapshot_dir: Path, manifest_path: Path, sources: Mapping[str, str]
) -> list[dict[str, Any]]:
    """Read current S3 objects into immutable, content-addressed snapshots."""
    refresh_credentials()
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    existing_payload = load_json(manifest_path) if manifest_path.exists() else []
    if not isinstance(existing_payload, list) or not all(
        isinstance(entry, dict) for entry in existing_payload
    ):
        raise ValueError(f"Snapshot manifest must be a JSON list: {manifest_path}")
    manifest: list[dict[str, Any]] = [dict(entry) for entry in existing_payload]

    with tempfile.TemporaryDirectory(prefix="placement-feedback-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        for family, uri in sorted(sources.items()):
            temp_path = temp_dir / f"{family}_reviewer_0.json"
            bucket, key = s3_bucket_key(uri)
            downloaded = run_with_aws_credentials(
                [
                    "aws",
                    "s3api",
                    "get-object",
                    "--bucket",
                    bucket,
                    "--key",
                    key,
                    str(temp_path),
                ],
                capture_output=True,
            )
            object_metadata = json.loads(downloaded.stdout)
            raw = temp_path.read_bytes()
            # Validate JSON before preserving the bytes as a source snapshot.
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Downloaded annotation is invalid JSON ({uri}): {exc}") from exc
            digest = sha256_bytes(raw)
            destination = snapshot_dir / f"{family}_reviewer_0_{digest[:12]}.json"
            if destination.exists():
                if sha256_file(destination) != digest:
                    raise ValueError(f"Refusing to overwrite hash-named snapshot: {destination}")
            else:
                # Exclusive creation makes the content-addressed snapshot immutable even if
                # two refreshes race. A concurrent identical writer is accepted after hashing.
                try:
                    with destination.open("xb") as handle:
                        handle.write(raw)
                except FileExistsError:
                    if sha256_file(destination) != digest:
                        raise ValueError(
                            f"Refusing to overwrite hash-named snapshot: {destination}"
                        )
            entry = {
                "family": family,
                "s3_uri": uri,
                "path": str(destination.resolve()),
                "sha256": digest,
                "last_modified": object_metadata.get("LastModified"),
                "retrieved_at": utc_now(),
            }
            if not any(
                old.get("family") == family
                and old.get("s3_uri") == uri
                and old.get("sha256") == digest
                for old in manifest
            ):
                manifest.append(entry)

    atomic_write_json(manifest_path, manifest)
    return manifest


def resolve_snapshot_path(entry: Mapping[str, Any], snapshot_dir: Path) -> Path:
    stated = Path(require_string(entry.get("path"), label="snapshot.path"))
    if stated.is_file():
        return stated
    fallback = snapshot_dir / stated.name
    if fallback.is_file():
        return fallback
    raise ValueError(f"Snapshot file does not exist: {stated}")


def selected_snapshots(manifest: Any) -> list[Mapping[str, Any]]:
    if not isinstance(manifest, list) or not all(isinstance(x, Mapping) for x in manifest):
        raise ValueError("Snapshot manifest must be a JSON list of objects")
    latest_by_family: dict[str, Mapping[str, Any]] = {}
    # Manifest append order is the version order; retain older immutable entries for audit.
    for entry in manifest:
        family = require_string(entry.get("family"), label="snapshot.family")
        latest_by_family[family] = entry
    missing = sorted(set(DEFAULT_SOURCES) - set(latest_by_family))
    if missing:
        raise ValueError(f"Snapshot manifest lacks required families: {missing}")
    return [latest_by_family[family] for family in sorted(latest_by_family)]


def validate_annotation(payload: Any, *, path: Path) -> Mapping[str, Any]:
    document = require_mapping(payload, label=str(path))
    if document.get("schema") != EXPECTED_ANNOTATION_SCHEMA:
        raise ValueError(
            f"Unexpected annotation schema in {path}: {document.get('schema')!r}"
        )
    require_mapping(document.get("reviewer"), label=f"{path}.reviewer")
    report = require_mapping(document.get("report"), label=f"{path}.report")
    if not isinstance(report.get("total_rows"), int):
        raise ValueError(f"{path}.report.total_rows must be an integer")
    if not isinstance(report.get("rows_pending"), int):
        raise ValueError(f"{path}.report.rows_pending must be an integer")
    if not isinstance(document.get("questions"), list):
        raise ValueError(f"{path}.questions must be an array")
    rows = document.get("rows")
    if not isinstance(rows, list):
        raise ValueError(f"{path}.rows must be an array")
    for index, raw_row in enumerate(rows):
        row = require_mapping(raw_row, label=f"{path}.rows[{index}]")
        require_string(row.get("key"), label=f"{path}.rows[{index}].key")
        row_idx = row.get("row_idx")
        if isinstance(row_idx, bool) or not isinstance(row_idx, int):
            raise ValueError(f"{path}.rows[{index}].row_idx must be an integer")
        require_string(
            row.get("evalset_item_id"),
            label=f"{path}.rows[{index}].evalset_item_id",
        )
        require_mapping(row.get("answers"), label=f"{path}.rows[{index}].answers")
        require_string(
            row.get("comment"),
            label=f"{path}.rows[{index}].comment",
            allow_empty=True,
        )
        question_comments = row.get("question_comments", {})
        if not isinstance(question_comments, Mapping) or not all(
            isinstance(question_id, str) and isinstance(text, str)
            for question_id, text in question_comments.items()
        ):
            raise ValueError(
                f"{path}.rows[{index}].question_comments must map question IDs to strings"
            )
        if not isinstance(row.get("complete"), bool):
            raise ValueError(f"{path}.rows[{index}].complete must be boolean")
        if row.get("blocked_by") is not None and not isinstance(row.get("blocked_by"), str):
            raise ValueError(f"{path}.rows[{index}].blocked_by must be null or string")
    return document


def load_assets(path: Path) -> tuple[Mapping[str, Any], dict[str, Mapping[str, Any]]]:
    payload = require_mapping(load_json(path), label=str(path))
    records = payload.get("records")
    if not isinstance(records, list) or not all(isinstance(x, Mapping) for x in records):
        raise ValueError(f"{path}.records must be an array of objects")
    return payload, unique_index(records, "id", label="asset")


def load_runs(runs_root: Path, assets: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    runs: dict[str, dict[str, Any]] = {}
    for result_path in sorted(runs_root.glob("*/result.json")):
        run_id = result_path.parent.name
        if run_id in runs:
            raise ValueError(f"Duplicate v2 run ID: {run_id}")
        if run_id not in assets:
            raise ValueError(f"v2 run ID has no asset: {run_id}")
        result = require_mapping(load_json(result_path), label=str(result_path))
        run_input = require_mapping(result.get("input"), label=f"{result_path}.input")
        asset = assets[run_id]
        expected_input = {
            "generated_image": asset["generated_image"]["local_path"],
            "twin_image": asset["twin_image"]["local_path"],
            "product_type": asset["device_type"],
            "scene_prompt": asset["scene_prompt"],
            "image_stage": asset["image_stage"],
        }
        for field, expected in expected_input.items():
            if run_input.get(field) != expected:
                raise ValueError(
                    f"v2 run {run_id} input {field} does not match asset ID join"
                )
        judgment = require_mapping(result.get("judgment"), label=f"{result_path}.judgment")
        runs[run_id] = {
            "run_id": run_id,
            "result_path": str(result_path.resolve()),
            "result_sha256": sha256_file(result_path),
            "fingerprint": result.get("fingerprint"),
            "model_requested": result.get("model_requested"),
            "model_returned": result.get("model_returned"),
            "judgment": judgment,
        }
    missing_runs = sorted(set(assets) - set(runs))
    extra_runs = sorted(set(runs) - set(assets))
    if missing_runs or extra_runs:
        raise ValueError(
            f"v2 asset/run ID mismatch: missing_runs={missing_runs}, extra_runs={extra_runs}"
        )
    return runs


def build_inventory(
    *,
    manifest_path: Path,
    snapshot_dir: Path,
    assets_path: Path,
    runs_root: Path,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    snapshots = selected_snapshots(manifest)
    assets_payload, assets = load_assets(assets_path)
    runs = load_runs(runs_root, assets)

    records: list[dict[str, Any]] = []
    seen_annotation_ids: set[str] = set()
    by_family: Counter[str] = Counter()
    row_comments_nonempty = 0
    question_comments_count = 0
    rows_with_any_nonempty_comment = 0
    complete_true = 0
    source_rows_total = 0
    selected_source_entries: list[dict[str, Any]] = []

    for entry in snapshots:
        family = require_string(entry.get("family"), label="snapshot.family")
        path = resolve_snapshot_path(entry, snapshot_dir)
        expected_hash = require_string(entry.get("sha256"), label="snapshot.sha256")
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            raise ValueError(
                f"Snapshot hash mismatch for {path}: expected {expected_hash}, got {actual_hash}"
            )
        document = validate_annotation(load_json(path), path=path)
        source_rows_total += int(document["report"]["total_rows"])
        selected_source_entries.append(
            {
                "family": family,
                "s3_uri": entry.get("s3_uri"),
                "path": str(path.resolve()),
                "sha256": actual_hash,
                "last_modified": entry.get("last_modified"),
                "retrieved_at": entry.get("retrieved_at"),
                "submitted_at": document.get("submitted_at"),
                "native_schema": document.get("schema"),
                "persisted_rows": len(document["rows"]),
                "report_total_rows": document["report"]["total_rows"],
                "report_rows_pending_reference_only": document["report"]["rows_pending"],
            }
        )

        for raw_row in document["rows"]:
            row = dict(raw_row)
            row_id = row["evalset_item_id"]
            if row_id in seen_annotation_ids:
                raise ValueError(f"Duplicate annotation evalset_item_id: {row_id}")
            seen_annotation_ids.add(row_id)
            if row["key"] != row_id:
                raise ValueError(
                    f"Annotation key and evalset_item_id differ for ID join: {row['key']} != {row_id}"
                )
            if row_id not in assets:
                raise ValueError(f"Annotation ID has no v2 asset: {row_id}")
            if row_id not in runs:
                raise ValueError(f"Annotation ID has no actual v2 run: {row_id}")
            asset = assets[row_id]
            expected_type = family[:-1] if family.endswith("s") else family
            if asset.get("device_type") != expected_type:
                raise ValueError(
                    f"Annotation family {family} disagrees with asset {row_id} device_type"
                )

            row_comment = row["comment"]
            question_comments = dict(row.get("question_comments", {}))
            row_nonempty = bool(row_comment)
            nested_nonempty = any(bool(text) for text in question_comments.values())
            row_comments_nonempty += int(row_nonempty)
            question_comments_count += len(question_comments)
            rows_with_any_nonempty_comment += int(row_nonempty or nested_nonempty)
            complete_true += int(row["complete"])
            by_family[family] += 1

            records.append(
                {
                    "id": row_id,
                    "family": family,
                    "source_row_identity": {
                        "key": row["key"],
                        "row_idx": row["row_idx"],
                        "evalset_item_id": row_id,
                    },
                    "comments": {
                        "row": row_comment,
                        "question_comments": question_comments,
                        "row_comment_sha256": sha256_bytes(row_comment.encode("utf-8")),
                        "question_comment_sha256": {
                            question_id: sha256_bytes(text.encode("utf-8"))
                            for question_id, text in question_comments.items()
                        },
                        "row_comment_state": (
                            "nonempty_free_text" if row_nonempty else "empty_no_concern_raised"
                        ),
                    },
                    "source_ui_metadata_reference_only": {
                        "complete": row["complete"],
                        "blocked_by": row["blocked_by"],
                    },
                    "asset": asset,
                    "v2_actual_run": runs[row_id],
                }
            )

    records.sort(key=lambda record: record["id"])
    omitted_ids = sorted(set(assets) - seen_annotation_ids)
    comments_empty = len(records) - row_comments_nonempty
    all_native_rows_joined_by_id = all(
        record["id"] == record["asset"]["id"] == record["v2_actual_run"]["run_id"]
        for record in records
    )

    return {
        "schema_version": "natural-placement-comment-inventory-v3@1",
        "scope": {
            "as_of_date": "2026-11-05",
            "source_schema": EXPECTED_ANNOTATION_SCHEMA,
            "inclusion_rule": (
                "Every row persisted in each selected native annotation snapshot is included; "
                "UI completion does not control inclusion."
            ),
            "comment_channels": ["comment", "question_comments"],
            "user_contract": [
                "Human Pass/Review/Fail button answers are excluded entirely and are not labels.",
                "Button answers are not used for severity, agreement statistics, or calibration.",
                "An empty comment on a persisted row means no concern was raised; it is not numerical ground truth.",
                "An asset ID absent from the snapshots is omitted, not reviewed.",
                "Free text such as 'agree' or 'agreed' may refer to the displayed prior v2 judge; the collector preserves it as unparsed free text rather than an explicit image label.",
            ],
        },
        "sources": {
            "snapshot_manifest": {
                "path": str(manifest_path.resolve()),
                "sha256": sha256_file(manifest_path),
            },
            "selected_annotation_snapshots": selected_source_entries,
            "v2_assets": {
                "path": str(assets_path.resolve()),
                "sha256": sha256_file(assets_path),
                "schema_version": assets_payload.get("schema_version"),
                "records": len(assets),
            },
            "v2_actual_runs": {
                "root": str(runs_root.resolve()),
                "records": len(runs),
            },
        },
        "counts": {
            "persisted_annotation_records": len(records),
            "by_family": dict(sorted(by_family.items())),
            "row_comments_nonempty": row_comments_nonempty,
            "row_comments_empty_no_concern_raised": comments_empty,
            "question_comments_preserved": question_comments_count,
            "rows_with_any_nonempty_comment": rows_with_any_nonempty_comment,
            "ui_complete_true_reference_only": complete_true,
            "ui_complete_false_reference_only": len(records) - complete_true,
            "source_report_rows": source_rows_total,
            "source_rows_absent_from_annotation_snapshots": len(omitted_ids),
            "matched_v2_assets": len(records),
            "matched_v2_actual_runs": len(records),
        },
        "join_validation": {
            "join_key": "evalset_item_id == asset.id == v2 run directory ID",
            "row_idx_used_for_join": False,
            "annotation_ids_unique": len(seen_annotation_ids) == len(records),
            "all_native_rows_joined_by_id": all_native_rows_joined_by_id,
            "all_96_v2_asset_ids_have_actual_run_ids": set(assets) == set(runs),
            "v2_run_inputs_exactly_match_asset_records": True,
            "absent_annotation_ids_not_inferred_reviewed": omitted_ids,
        },
        "records": records,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--refresh-s3",
        action="store_true",
        help="Read current annotation objects from S3 into immutable hash-named snapshots.",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        metavar="FAMILY=S3_URI",
        help="Override or add a source used by --refresh-s3 (repeatable).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.refresh_s3:
        sources = parse_source_args(args.source)
        refresh_snapshots(
            snapshot_dir=args.snapshot_dir,
            manifest_path=args.manifest,
            sources=sources,
        )
    elif args.source:
        raise ValueError("--source is only valid with --refresh-s3")

    inventory = build_inventory(
        manifest_path=args.manifest,
        snapshot_dir=args.snapshot_dir,
        assets_path=args.assets,
        runs_root=args.runs_root,
    )
    atomic_write_json(args.output, inventory)
    print(
        json.dumps(
            {
                "output": str(args.output.resolve()),
                "counts": inventory["counts"],
                "join_validation": inventory["join_validation"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
