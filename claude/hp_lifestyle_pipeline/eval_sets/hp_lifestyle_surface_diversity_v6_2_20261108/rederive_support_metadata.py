#!/usr/bin/env python3
"""Derive corrected primary-support metadata from an immutable frozen export.

This utility never edits prompt text or selection records.  It imports one
explicitly hash-pinned ``surfaces.py`` in an isolated module namespace, derives
per-row support metadata and bank audits, and writes a new immutable directory.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType
from typing import Any


EXPECTED_PROMPTS = 160
EXPECTED_BANKS = 16
EXPECTED_PER_BANK = 10
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def require_sha(path: Path, expected: str, label: str) -> str:
    if not SHA256_RE.fullmatch(expected):
        raise ValueError(f"{label} SHA-256 must be 64 lowercase hexadecimal characters")
    actual = sha256_path(path)
    if actual != expected:
        raise ValueError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")
    return actual


def load_surfaces(path: Path, expected_sha256: str) -> ModuleType:
    """Hash-check and import a single file without adding its directory to sys.path."""
    require_sha(path, expected_sha256, "surfaces module")
    name = f"_hp_frozen_surfaces_{expected_sha256}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load surfaces module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    for function in ("infer_primary_support", "audit_bank"):
        if not callable(getattr(module, function, None)):
            raise TypeError(f"surfaces module has no callable {function}")
    return module


def validate_support(text: str, support: Any, row_id: str) -> None:
    if not isinstance(support, dict):
        raise ValueError(f"{row_id}: derived primary_support is not an object")
    required = {"family", "shape", "phrase", "start", "end", "shape_evidence", "sentence_start", "sentence_end", "device_type"}
    missing = required - set(support)
    if missing:
        raise ValueError(f"{row_id}: derived primary_support lacks {sorted(missing)}")
    start, end = support["start"], support["end"]
    if (isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int)
            or start < 0 or end <= start or end > len(text) or text[start:end] != support["phrase"]):
        raise ValueError(f"{row_id}: primary-support phrase/span does not match frozen text")
    sentence_start, sentence_end = support["sentence_start"], support["sentence_end"]
    if (not isinstance(sentence_start, int) or not isinstance(sentence_end, int)
            or sentence_start < 0 or sentence_end < end or sentence_end > len(text)):
        raise ValueError(f"{row_id}: primary-support sentence span does not cover its phrase")
    shape = support["shape"]
    evidence = support["shape_evidence"]
    if shape == "unspecified":
        if evidence is not None:
            raise ValueError(f"{row_id}: unspecified shape has shape evidence")
        return
    if shape not in {"round", "oval", "rectangular", "square"} or not isinstance(evidence, dict):
        raise ValueError(f"{row_id}: invalid derived primary-support shape/evidence")
    evidence_start, evidence_end = evidence.get("start"), evidence.get("end")
    if (not isinstance(evidence_start, int) or not isinstance(evidence_end, int)
            or evidence_start < start or evidence_end > sentence_end or evidence_end <= evidence_start
            or text[evidence_start:evidence_end] != evidence.get("phrase")):
        raise ValueError(f"{row_id}: primary-support shape evidence does not match frozen text")
    normalized = str(evidence["phrase"]).casefold()
    expected_words = {"round": {"round", "circular"}, "oval": {"oval"},
                      "rectangular": {"rectangular"}, "square": {"square"}}
    if normalized not in expected_words[shape]:
        raise ValueError(f"{row_id}: shape label {shape!r} disagrees with exact evidence {evidence['phrase']!r}")


def validate_document(document: Any) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    if not isinstance(document, dict):
        raise ValueError("frozen export must be a JSON object")
    prompts = document.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != EXPECTED_PROMPTS:
        raise ValueError("frozen export must contain exactly 160 prompts")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_keys: set[str] = set()
    for position, row in enumerate(prompts):
        if not isinstance(row, dict):
            raise ValueError(f"prompt {position} is not an object")
        key, bank_id, text = row.get("prompt_key"), row.get("bank_debug_ref"), row.get("text")
        if not isinstance(key, str) or not key or key in seen_keys:
            raise ValueError(f"invalid or duplicate prompt_key at row {position}: {key!r}")
        if not isinstance(bank_id, str) or not bank_id or not isinstance(text, str) or not text:
            raise ValueError(f"{key}: missing bank_debug_ref or text")
        rank = row.get("bank_rank")
        if isinstance(rank, bool) or not isinstance(rank, int) or not 1 <= rank <= 10:
            raise ValueError(f"{key}: bank_rank must be an integer from 1 through 10")
        if "text_sha256" in row and row["text_sha256"] != sha256_bytes(text.encode("utf-8")):
            raise ValueError(f"{key}: text_sha256 does not match frozen text")
        seen_keys.add(key)
        groups[bank_id].append(row)
    if len(groups) != EXPECTED_BANKS or any(len(rows) != EXPECTED_PER_BANK for rows in groups.values()):
        raise ValueError("frozen export must contain 16 banks of ten prompts")
    for bank_id, rows in groups.items():
        if {row["bank_rank"] for row in rows} != set(range(1, 11)):
            raise ValueError(f"{bank_id}: bank ranks are not exactly 1 through 10")
        ids = [row.get("id") for row in sorted(rows, key=lambda item: item["bank_rank"])]
        if ids != [f"p{rank}" for rank in range(1, 11)]:
            raise ValueError(f"{bank_id}: prompt IDs do not match ranks p1 through p10")
        if any(row["prompt_key"] != f"{bank_id}::{row['id']}" for row in rows):
            raise ValueError(f"{bank_id}: prompt_key does not match bank_debug_ref and prompt id")
    bank_audit = document.get("bank_audit")
    if not isinstance(bank_audit, dict) or set(bank_audit) != set(groups):
        raise ValueError("bank_audit keys must exactly match the 16 bank_debug_ref values")
    return prompts, groups


def _without_support(row: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in row.items() if key != "primary_support"}


def _bank_non_derived(entry: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(entry)
    value.pop("original_debug", None)
    value.pop("support_metadata_derivation", None)
    debug = value.get("debug")
    if isinstance(debug, dict):
        debug.pop("primary_support_audit", None)
        debug.pop("support_metadata_derivation", None)
    return value


def derive_document(
    original: dict[str, Any], surfaces: ModuleType, *, input_path: Path, input_sha256: str,
    surfaces_path: Path, surfaces_sha256: str, tool_path: Path, tool_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    original_prompts, original_groups = validate_document(original)
    existing_derivation = (original.get("provenance") or {}).get("support_metadata_derivation")
    if existing_derivation is not None:
        raise ValueError("input already contains support_metadata_derivation provenance")

    derived = copy.deepcopy(original)
    derived_prompts = derived["prompts"]
    by_key = {row["prompt_key"]: row for row in derived_prompts}
    original_by_key = {row["prompt_key"]: row for row in original_prompts}
    changes: list[dict[str, Any]] = []
    derived_audits: dict[str, dict[str, Any]] = {}

    for bank_id, original_bank_rows in original_groups.items():
        ordered = sorted(original_bank_rows, key=lambda item: item["bank_rank"])
        audit_rows = [
            {"id": row["id"], "text": row["text"], "device_type": row.get("device_type"),
             "environment": row.get("environment")}
            for row in ordered
        ]
        audit = surfaces.audit_bank(audit_rows, ordered[0].get("device_type"))
        if not isinstance(audit, dict) or not isinstance(audit.get("rows"), list):
            raise ValueError(f"{bank_id}: surfaces.audit_bank returned an invalid result")
        if not audit.get("passed"):
            raise ValueError(f"{bank_id}: corrected support audit does not pass: {audit.get('errors')}")
        support_by_id: dict[str, dict[str, Any]] = {}
        for audit_row in audit["rows"]:
            if "error" in audit_row or not isinstance(audit_row.get("support"), dict):
                raise ValueError(f"{bank_id}: audit row has no derived support: {audit_row}")
            row_id = audit_row.get("row_id")
            if row_id in support_by_id:
                raise ValueError(f"{bank_id}: duplicate audit row {row_id!r}")
            support_by_id[row_id] = audit_row["support"]
        if set(support_by_id) != {row["id"] for row in ordered}:
            raise ValueError(f"{bank_id}: audit rows do not cover p1 through p10")

        for original_row in ordered:
            key = original_row["prompt_key"]
            inferred = surfaces.infer_primary_support(original_row["text"], original_row.get("device_type"))
            if inferred != support_by_id[original_row["id"]]:
                raise ValueError(f"{key}: bank audit support differs from direct inference")
            validate_support(original_row["text"], inferred, key)
            old_support = copy.deepcopy(original_row.get("primary_support"))
            by_key[key]["primary_support"] = copy.deepcopy(inferred)
            changes.append({
                "prompt_key": key, "bank_debug_ref": bank_id, "bank_rank": original_row["bank_rank"],
                "text_sha256": sha256_bytes(original_row["text"].encode("utf-8")),
                "non_support_record_sha256": canonical_sha256(_without_support(original_row)),
                "changed": old_support != inferred,
                "old_primary_support": old_support,
                "new_primary_support": copy.deepcopy(inferred),
            })
        derived_audits[bank_id] = copy.deepcopy(audit)

    if [row["prompt_key"] for row in derived_prompts] != [row["prompt_key"] for row in original_prompts]:
        raise AssertionError("prompt ID/order changed during support derivation")
    for derived_row in derived_prompts:
        key = derived_row["prompt_key"]
        if _without_support(derived_row) != _without_support(original_by_key[key]):
            raise AssertionError(f"{key}: a non-support prompt field changed")

    original_bank_audit = original["bank_audit"]
    for bank_id, audit in derived_audits.items():
        entry = derived["bank_audit"][bank_id]
        if not isinstance(entry, dict):
            raise ValueError(f"{bank_id}: bank_audit entry is not an object")
        old_debug = entry.get("debug")
        old_surface_audit = old_debug.get("primary_support_audit") if isinstance(old_debug, dict) else None
        if isinstance(old_surface_audit, dict) and bool(old_surface_audit.get("passed")) != bool(audit.get("passed")):
            raise ValueError(f"{bank_id}: support rederivation would change the bank accept/reject decision")
        if isinstance(old_debug, dict):
            if "original_debug" in entry:
                raise ValueError(f"{bank_id}: bank_audit already contains original_debug")
            entry["original_debug"] = copy.deepcopy(old_debug)
            new_debug = copy.deepcopy(old_debug)
        else:
            new_debug = {}
        new_debug["primary_support_audit"] = copy.deepcopy(audit)
        new_debug["support_metadata_derivation"] = {
            "kind": "deterministic_hash_pinned_parser_rederivation", "raw_result_changed": False,
            "selection_decision_changed": False, "surfaces_sha256": surfaces_sha256,
        }
        entry["debug"] = new_debug
        entry["support_metadata_derivation"] = {
            "old_primary_support_audit": copy.deepcopy(old_surface_audit),
            "new_primary_support_audit_sha256": canonical_sha256(audit),
            "raw_result_hashes_preserved": True,
        }
        if _bank_non_derived(entry) != _bank_non_derived(original_bank_audit[bank_id]):
            raise AssertionError(f"{bank_id}: a selection/source/raw-result bank field changed")

    provenance = derived.get("provenance")
    if provenance is None:
        provenance = {}
        derived["provenance"] = provenance
    if not isinstance(provenance, dict):
        raise ValueError("root provenance must be an object")
    provenance["support_metadata_derivation"] = {
        "kind": "deterministic_hash_pinned_parser_rederivation",
        "input": {"path": str(input_path.resolve()), "sha256": input_sha256},
        "surfaces_module": {"path": str(surfaces_path.resolve()), "sha256": surfaces_sha256},
        "utility": {"path": str(tool_path.resolve()), "sha256": tool_sha256},
        "manual_prompt_edits": False, "additional_model_calls": 0,
        "prompt_text_changed": False, "prompt_order_changed": False,
        "selection_decisions_changed": False, "raw_result_hashes_recomputed": False,
        "changed_support_rows": sum(item["changed"] for item in changes),
        "change_audit_rows_sha256": canonical_sha256(changes),
    }

    original_provenance = copy.deepcopy(original.get("provenance") or {})
    comparable_provenance = copy.deepcopy(provenance)
    comparable_provenance.pop("support_metadata_derivation")
    if comparable_provenance != original_provenance:
        raise AssertionError("pre-existing root provenance changed during support derivation")
    for key in set(original) | set(derived):
        if key not in {"prompts", "bank_audit", "provenance"} and original.get(key) != derived.get(key):
            raise AssertionError(f"root field changed during support derivation: {key}")

    validate_document(derived)
    bank_source_and_result_provenance = {
        bank_id: {
            key: copy.deepcopy(value)
            for key, value in original_bank_audit[bank_id].items()
            if key in {
                "selected_revision", "selected_result_path", "selected_result_sha256", "selected_attempt",
                "selected_raw_output_sha256", "source_input_path", "source_input_sha256",
                "manual_prompt_edits", "additional_model_calls",
            }
        }
        for bank_id in sorted(original_bank_audit)
    }
    audit_document = {
        "schema_version": "hp-primary-support-metadata-derivation-audit-v1",
        "input": {"path": str(input_path.resolve()), "sha256": input_sha256},
        "surfaces_module": {"path": str(surfaces_path.resolve()), "sha256": surfaces_sha256},
        "utility": {"path": str(tool_path.resolve()), "sha256": tool_sha256},
        "invariants": {
            "prompt_count": 160, "bank_count": 16, "prompts_per_bank": 10,
            "prompt_key_order_unchanged": True, "prompt_text_unchanged": True,
            "all_non_support_prompt_fields_unchanged": True,
            "selection_and_raw_result_bank_fields_unchanged": True,
            "manual_prompt_edits": False, "additional_model_calls": 0,
        },
        "summary": {"rows": 160, "changed": sum(item["changed"] for item in changes),
                    "unchanged": sum(not item["changed"] for item in changes)},
        "preserved_bank_source_and_raw_result_provenance": bank_source_and_result_provenance,
        "rows": changes,
    }
    return derived, audit_document


def text_export(rows: list[dict[str, Any]]) -> str:
    blocks = []
    for row in rows:
        header = (f"[{row['prompt_key']} | {row.get('device_display_name', row.get('device_id', ''))} | "
                  f"{row.get('camera_tag', '')} | rank {row['bank_rank']} | "
                  f"source {row.get('source_relevance_score', 'n/a')} | C-Tech {row.get('ctech_reference_score', 'n/a')}]")
        blocks.append(f"{header}\n{row['text']}")
    return "\n\n".join(blocks) + "\n"


def top6_document(document: dict[str, Any], all_sha256: str) -> dict[str, Any]:
    top = copy.deepcopy(document)
    top["prompts"] = [row for row in top["prompts"] if row["bank_rank"] <= 6]
    if len(top["prompts"]) != 96:
        raise AssertionError("top-six export is not 96 rows")
    version = top.get("version")
    if isinstance(version, str):
        top["version"] = version.replace("-all-four-devices-", "-top6-four-devices-")
    counts = copy.deepcopy(top.get("counts") or {})
    counts.pop("candidates_per_bank", None)
    counts["selected_per_bank"] = 6
    counts["prompts"] = 96
    top["counts"] = counts
    top["provenance"]["support_metadata_derivation"]["subset"] = {
        "rule": "bank_rank <= 6", "source_prompts_all_160_sha256": all_sha256,
    }
    return top


def create_export(
    input_path: Path, input_sha256: str, surfaces_path: Path, surfaces_sha256: str,
    output_dir: Path, include_top6: bool,
) -> dict[str, Any]:
    input_path, surfaces_path, output_dir = input_path.resolve(), surfaces_path.resolve(), output_dir.resolve()
    require_sha(input_path, input_sha256, "input export")
    surfaces = load_surfaces(surfaces_path, surfaces_sha256)
    tool_path = Path(__file__).resolve()
    tool_sha256 = sha256_path(tool_path)
    original = load_json(input_path)
    derived, audit = derive_document(
        original, surfaces, input_path=input_path, input_sha256=input_sha256,
        surfaces_path=surfaces_path, surfaces_sha256=surfaces_sha256,
        tool_path=tool_path, tool_sha256=tool_sha256,
    )
    if output_dir.exists():
        raise FileExistsError(f"immutable output directory already exists: {output_dir}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent))
    try:
        all_json = temporary / "prompts_all_160.json"
        write_json(all_json, derived)
        atomic_text(temporary / "prompts_all_160.txt", text_export(derived["prompts"]))
        all_sha = sha256_path(all_json)
        audit["derived_prompts_all_160"] = {"sha256": all_sha, "bytes": all_json.stat().st_size}
        if include_top6:
            top = top6_document(derived, all_sha)
            write_json(temporary / "prompts_top6_96.json", top)
            atomic_text(temporary / "prompts_top6_96.txt", text_export(top["prompts"]))
        write_json(temporary / "support_metadata_changes.json", audit)
        files = {
            path.name: {"sha256": sha256_path(path), "bytes": path.stat().st_size}
            for path in sorted(temporary.iterdir()) if path.is_file()
        }
        manifest = {
            "schema_version": "hp-primary-support-metadata-derived-export-v1",
            "immutable": True, "input_untouched": sha256_path(input_path) == input_sha256,
            "manual_prompt_edits": False, "additional_model_calls": 0,
            "selection_decisions_changed": False, "raw_result_hashes_recomputed": False,
            "input": {"path": str(input_path), "sha256": input_sha256},
            "surfaces_module": {"path": str(surfaces_path), "sha256": surfaces_sha256},
            "utility": {"path": str(tool_path), "sha256": tool_sha256},
            "files": files,
        }
        write_json(temporary / "manifest.json", manifest)
        os.replace(temporary, output_dir)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return {"output": str(output_dir), "changed_support_rows": audit["summary"]["changed"],
            "prompts": 160, "banks": 16, "top6": include_top6,
            "manifest_sha256": sha256_path(output_dir / "manifest.json")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="original frozen prompts_all_160.json")
    parser.add_argument("--input-sha256", required=True)
    parser.add_argument("--surfaces", type=Path, required=True, help="explicit frozen/live surfaces.py to import in isolation")
    parser.add_argument("--surfaces-sha256", required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="must not already exist")
    parser.add_argument("--include-top6", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = create_export(args.input, args.input_sha256, args.surfaces, args.surfaces_sha256,
                           args.output_dir, args.include_top6)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
