#!/usr/bin/env python3
"""Freeze one fully validated 160-prompt V6.2 export from recorded GPT-5.5 banks.

The writer intentionally returns an explicit error when its initial response and
single repair do not validate.  Evaluation retries were recorded in immutable
revisions.  This builder performs no model calls and edits no prompt text.  It
selects, per bank, the newest recorded raw response that passes the current
frozen validator/catalog, applies the normal deterministic finalizer, and writes
complete provenance for the selected response.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from research.source_messaging_v1_to_v6.versions.v6_2.camera import resolve_camera
from research.source_messaging_v1_to_v6.versions.v6_2.validation import (
    finalize_output,
    validate_output,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MASTER = PROJECT / "research/source_messaging_v1_to_v6/versions/v6_2"
REVISION_NAMES = [
    "v6.2-full160-20261107-r4",
    "v6.2-full160-20261107-r3",
    "v6.2-full160-20261107-r2",
    "v6.2-full160-20261107-r1",
]
BASE_REVISION = HERE / "revisions" / REVISION_NAMES[0]
OUTPUT_REVISION = HERE / "revisions/v6.2-full160-20261107-r5-validated-composite"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_sha(value: Any) -> str:
    return sha_bytes(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if OUTPUT_REVISION.exists():
        raise FileExistsError(OUTPUT_REVISION)
    catalog_path = MASTER / "approved-v6.2-20261106.catalog.json"
    registry_path = MASTER / "camera_profiles.json"
    references_path = MASTER / "reference_library.json"
    validation_path = MASTER / "validation.py"
    catalog = load(catalog_path)
    registry = load(registry_path)
    references = load(references_path)
    snapshot = load(BASE_REVISION / "snapshot_manifest.json")
    cases = {case["case_id"]: case for case in snapshot["cases"]}
    all_rows: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []
    bank_audit: dict[str, Any] = {}

    for case_id in snapshot["authorized_text_case_ids"]:
        case = cases[case_id]
        request_path = BASE_REVISION / "inputs" / f"{case_id}.json"
        request = load(request_path)
        camera = resolve_camera(registry, request["camera_tag"])
        selected: tuple[str, Path, int, dict[str, Any], dict[str, Any]] | None = None
        considered: list[dict[str, Any]] = []
        for revision_name in REVISION_NAMES:
            result_path = HERE / "revisions" / revision_name / "results" / f"{case_id}.json"
            if not result_path.is_file():
                continue
            result = load(result_path)
            attempts = result.get("audit", {}).get("attempts", [])
            for attempt_number, attempt in reversed(list(enumerate(attempts, start=1))):
                raw = attempt.get("parsed_output")
                if not isinstance(raw, dict):
                    continue
                validation = validate_output(raw, request, catalog, camera, references)
                considered.append(
                    {
                        "revision": revision_name,
                        "result_path": str(result_path),
                        "result_sha256": sha_file(result_path),
                        "attempt": attempt_number,
                        "raw_output_sha256": canonical_sha(raw),
                        "passed_current_validation": validation["passed"],
                        "error_codes": [item["code"] for item in validation["errors"]],
                    }
                )
                if validation["passed"]:
                    selected = (revision_name, result_path, attempt_number, raw, validation)
                    break
            if selected:
                break
        if selected is None:
            raise ValueError(f"no recorded bank passes current V6.2 validation: {case_id}")
        revision_name, result_path, attempt_number, raw, validation = selected
        finalized = finalize_output(raw, camera=camera, catalog=catalog)
        prompts = finalized["prompts"]
        if len(prompts) != 10 or [item["id"] for item in prompts] != [f"p{i}" for i in range(1, 11)]:
            raise ValueError(f"invalid finalized bank: {case_id}")
        bank_audit[case_id] = {
            "selection_policy": "newest recorded raw bank passing current frozen validation",
            "selected_revision": revision_name,
            "selected_result_path": str(result_path),
            "selected_result_sha256": sha_file(result_path),
            "selected_attempt": attempt_number,
            "selected_raw_output_sha256": canonical_sha(raw),
            "current_validation": validation,
            "source_input_path": str(request_path),
            "source_input_sha256": sha_file(request_path),
            "considered": considered,
            "manual_prompt_edits": False,
            "additional_model_calls": 0,
        }
        for rank, candidate in enumerate(prompts, start=1):
            row = {
                "prompt_key": f"{case_id}::{candidate['id']}",
                "device_id": case["device_id"],
                "device_display_name": case["device_display_name"],
                "device_type": case["device_type"],
                "source_pair": case["source_pair"],
                "camera_tag": case["camera_tag"],
                "source_camera_name": case["source_camera_name"],
                "view_role": case["view_role"],
                "render_gallery_url": case["render_gallery_url"],
                "render_lookup": case["render_lookup"],
                "bank_rank": rank,
                **candidate,
                "text_sha256": sha_bytes(candidate["text"].encode()),
                "bank_debug_ref": case_id,
            }
            all_rows.append(row)
            if rank <= 6:
                top_rows.append(dict(row))

    if len(all_rows) != 160 or len(top_rows) != 96:
        raise ValueError("composite export has wrong row counts")
    if len({row["prompt_key"] for row in all_rows}) != 160:
        raise ValueError("composite prompt keys are not unique")
    counts = Counter(row["bank_debug_ref"] for row in all_rows)
    if len(counts) != 16 or set(counts.values()) != {10}:
        raise ValueError("composite bank counts are invalid")

    shared = {
        "revision": OUTPUT_REVISION.name,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_rule": snapshot["scope"]["selection_rule"],
        "device_source_mapping": snapshot["device_source_mapping"],
        "bank_audit": bank_audit,
        "provenance": {
            "kind": "deterministically_revalidated_recorded_gpt55_banks",
            "manual_prompt_edits": False,
            "additional_model_calls": 0,
            "catalog": {"path": str(catalog_path), "sha256": sha_file(catalog_path)},
            "validation": {"path": str(validation_path), "sha256": sha_file(validation_path)},
            "camera_registry": {"path": str(registry_path), "sha256": sha_file(registry_path)},
            "reference_library": {"path": str(references_path), "sha256": sha_file(references_path)},
            "candidate_revisions_newest_first": REVISION_NAMES,
        },
    }
    all_output = {
        "version": "hp-lifestyle-spatial-composition-v6.2-all-four-devices-v1",
        **shared,
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "prompts": all_rows,
    }
    top_output = {
        "version": "hp-lifestyle-spatial-composition-v6.2-top6-four-devices-v1",
        **shared,
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "selected_per_bank": 6, "prompts": 96},
        "prompts": top_rows,
    }
    destination = OUTPUT_REVISION / "exports/final"
    write(destination / "prompts_all_160.json", all_output)
    write(destination / "prompts_top6_96.json", top_output)
    write(
        destination / "validation.json",
        {
            "passed": True,
            "all_16_banks_pass_current_validation": True,
            "all_160_prompts_exported": True,
            "manual_prompt_edits": False,
            "additional_model_calls": 0,
            "selected_revision_counts": dict(
                Counter(value["selected_revision"] for value in bank_audit.values())
            ),
            "files": {
                name: {"sha256": sha_file(destination / name), "bytes": (destination / name).stat().st_size}
                for name in ("prompts_all_160.json", "prompts_top6_96.json")
            },
        },
    )
    print(json.dumps({"output": str(destination), "prompts": 160, "banks": 16}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
