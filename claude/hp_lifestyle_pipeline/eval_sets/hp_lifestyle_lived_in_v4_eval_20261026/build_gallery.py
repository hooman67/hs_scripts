#!/usr/bin/env python3
"""Build the isolated V4 text-bank and selected-generation gallery."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image


EVAL_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = EVAL_ROOT.parents[1]
MANIFEST_PATH = EVAL_ROOT / "manifest.json"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
SELECTION_PATH = EVAL_ROOT / "selection_manifest.json"
MANUAL_REVIEW_PATH = EVAL_ROOT / "manual_review_overrides.json"
PROMPT_EXPORT_PATHS = {
    "all_540": EVAL_ROOT / "generation_prompts.json",
    "selected_108": EVAL_ROOT / "generation_prompts_selected.json",
}
TEMPLATE_DIR = EVAL_ROOT / "gallery"
DEFAULT_RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026"
SHARED_IMS_AUTH = PROJECT_ROOT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
EXPECTED_SOURCES = 9
EXPECTED_CASES = 18
EXPECTED_RENDERS = 4
EXPECTED_CANDIDATES = 540
EXPECTED_SELECTIONS = 108
EXPECTED_ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")
EXPECTED_SELECTION_STATUS = "approved_for_image_generation"
EXPECTED_SEMANTIC_STATUS = "accepted"
EXPECTED_STRATA = {
    "upper_rank_1_10": ("1-10", range(1, 11)),
    "middle_rank_11_20": ("11-20", range(11, 21)),
    "lower_rank_21_30": ("21-30", range(21, 31)),
}
MODEL_CANDIDATE_FIELDS = (
    "id", "environment", "subsetting", "text", "source_relevance_score",
    "relationship", "score_components", "evidence_ids", "explanation",
    "creative_departures", "visual_signature", "camera_omissions",
)
SECRET_PATTERNS = (
    re.compile(r"AWS_SECRET_ACCESS_KEY", re.I),
    re.compile(r"AWS_SESSION_TOKEN", re.I),
    re.compile(r"X-Amz-Signature", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r'"authorization"\s*:', re.I),
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def read_json_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    return json.loads(raw), raw


def atomic_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def validate_file(path: Path, expected_sha: str, expected_bytes: int | None = None) -> bytes:
    raw = path.read_bytes()
    if expected_bytes is not None and len(raw) != expected_bytes:
        raise ValueError(f"Byte count mismatch: {path}")
    if sha256_bytes(raw) != expected_sha:
        raise ValueError(f"SHA-256 mismatch: {path}")
    return raw


def index_unique(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    output = {}
    for item in items:
        key = item.get(field)
        if not isinstance(key, str) or not key or key in output:
            raise ValueError(f"Invalid or duplicate {field}: {key!r}")
        output[key] = item
    return output


def readiness() -> dict[str, Any]:
    result = {
        "ready": False,
        "manifest_exists": MANIFEST_PATH.is_file(),
        "image_generation_authorized": False,
        "accepted_exists": ACCEPTED_PATH.is_file(),
        "selection_exists": SELECTION_PATH.is_file(),
        "accepted_status": None,
        "selection_status": None,
        "accepted_case_count": 0,
        "root_accepted_case_count": 0,
        "candidate_count": 0,
        "selection_count": 0,
        "approved_selection_count": 0,
        "reasons": [],
    }
    if not result["manifest_exists"]:
        result["reasons"].append("manifest_missing")
        return result
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    result["image_generation_authorized"] = manifest.get("scope", {}).get("image_generation_authorized") is True
    result["manifest_source_count"] = len(manifest.get("sources", []))
    result["manifest_case_count"] = len(manifest.get("cases", []))
    result["manifest_render_count"] = len(manifest.get("renders", []))
    if not result["image_generation_authorized"]:
        result["reasons"].append("manifest_image_generation_not_authorized")
    if not result["accepted_exists"]:
        result["reasons"].append("accepted_prompt_cases_missing")
        return result
    accepted = json.loads(ACCEPTED_PATH.read_text(encoding="utf-8"))
    result["accepted_status"] = accepted.get("status")
    cases = accepted.get("cases") or {}
    result["accepted_case_count"] = len(cases)
    result["root_accepted_case_count"] = sum(
        item.get("status") == "normalized_validator_passed"
        and item.get("human_review_status") == "accepted"
        and item.get("launchable") is True
        for item in cases.values()
    )
    result["candidate_count"] = sum(len(item.get("candidates") or []) for item in cases.values())
    if (
        accepted.get("status") != "complete"
        or len(cases) != EXPECTED_CASES
        or result["candidate_count"] != EXPECTED_CANDIDATES
        or result["root_accepted_case_count"] != EXPECTED_CASES
    ):
        result["reasons"].append("validated_candidate_bank_incomplete")
    if not result["selection_exists"]:
        result["reasons"].append("selection_manifest_missing")
        return result
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    result["selection_status"] = selection.get("status")
    selections = selection.get("selections") or []
    result["selection_count"] = len(selections)
    result["approved_selection_count"] = sum(
        item.get("semantic_review_status") == EXPECTED_SEMANTIC_STATUS for item in selections
    )
    if selection.get("status") != EXPECTED_SELECTION_STATUS:
        result["reasons"].append("selection_manifest_not_root_approved")
    if len(selections) != EXPECTED_SELECTIONS or result["approved_selection_count"] != EXPECTED_SELECTIONS:
        result["reasons"].append("root_approved_selection_set_incomplete")
    result["ready"] = not result["reasons"]
    return result


def normalize_selection(item: dict[str, Any]) -> dict[str, Any]:
    return {
        **item,
        "selection_id": item.get("selection_id") or item.get("selection_key"),
        "candidate_id": item.get("candidate_id") or item.get("prompt_id"),
        "rank_stratum": item.get("selection_stratum") or item.get("rank_bin"),
        "reference_render_id": item.get("reference_render_id") or item.get("render_id"),
        "candidate_text": item.get("candidate_text") or item.get("text"),
        "candidate_text_sha256": item.get("candidate_text_sha256") or item.get("text_sha256"),
        "score_total": item.get("score_total"),
        "rubric_components": item.get("rubric_components") or item.get("score_components"),
        "score_reason": item.get("score_reason") or item.get("explanation"),
        "creative_departures": item.get("creative_departures") or [],
        "candidate_record_path": item.get("candidate_record_path") or item.get("accepted_record_path"),
        "candidate_record_sha256": item.get("candidate_record_sha256") or item.get("accepted_record_sha256"),
    }


def copy_reference_assets(renders: dict[str, dict[str, Any]], run_dir: Path, manifest_sha: str) -> dict[str, Any]:
    destination_dir = run_dir / "assets/references"
    destination_dir.mkdir(parents=True, exist_ok=True)
    assets = {}
    for render_id, render in sorted(renders.items()):
        if render.get("device_type") not in {"laptop", "printer"}:
            raise ValueError(f"Excluded device type in V4 render: {render_id}")
        source = Path(render["path"])
        raw = validate_file(source, render["sha256"], render["bytes"])
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError(f"Reference is not PNG: {source}")
        with Image.open(source) as image:
            if image.size != (render["width"], render["height"]):
                raise ValueError(f"Reference dimensions differ: {render_id}")
        filename = f"{sha256_bytes(render_id.encode())[:16]}__{render['device_type']}__{render['role']}.png"
        destination = destination_dir / filename
        if destination.exists():
            validate_file(destination, render["sha256"], render["bytes"])
        else:
            atomic_write(destination, raw)
        render["reference_asset_filename"] = filename
        assets[render_id] = {
            "render_id": render_id,
            "asset_filename": filename,
            "source_path": str(source.resolve()),
            "source_sha256": render["sha256"],
            "published_bytes_sha256": sha256_path(destination),
            "bytes": render["bytes"],
            "width": render["width"],
            "height": render["height"],
            "content_type": "image/png",
        }
    document = {
        "version": "hp-lived-in-v4-reference-assets-v1",
        "manifest_sha256": manifest_sha,
        "asset_count": len(assets),
        "total_bytes": sum(item["bytes"] for item in assets.values()),
        "assets": assets,
    }
    atomic_json(run_dir / "reference_assets.json", document)
    return document


def load_records(run_dir: Path) -> dict[str, dict[str, Any]]:
    records = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        row_id = record.get("row_id")
        if not isinstance(row_id, str) or not row_id or row_id in records:
            raise ValueError(f"Invalid or duplicate generation row in {path}")
        if record.get("status") not in {"done", "pending", "failed"}:
            raise ValueError(f"Invalid generation status in {path}")
        records[row_id] = record
    return records


def validate_done_record(
    record: dict[str, Any], render: dict[str, Any], run_dir: Path,
    candidate: dict[str, Any], selection: dict[str, Any],
    manifest_sha: str, accepted_sha: str, selection_sha: str,
) -> None:
    if record.get("status") != "done":
        return
    current = record.get("current_render") or {}
    binding = record.get("reference_binding") or {}
    if current.get("sha256") != render["sha256"] or binding.get("original_png_sha256") != render["sha256"]:
        raise ValueError(f"Reference identity mismatch: {record['row_id']}")
    if record.get("selection", {}).get("selection_key") != selection["selection_id"]:
        raise ValueError(f"Selection identity mismatch: {record['row_id']}")
    selected = record.get("selected_candidate") or {}
    if (
        selected.get("candidate_key") != candidate["candidate_key"]
        or selected.get("text_sha256") != candidate["text_sha256"]
        or selected.get("text") != candidate["text"]
        or selected.get("source_relevance_score") != candidate["source_relevance_score"]
    ):
        raise ValueError(f"Selected candidate mismatch: {record['row_id']}")
    provenance = record.get("provenance") or {}
    expected_provenance = {
        "manifest_sha256": manifest_sha,
        "accepted_prompt_cases_sha256": accepted_sha,
        "selection_manifest_sha256": selection_sha,
        "candidate_text_sha256": candidate["text_sha256"],
    }
    if any(provenance.get(key) != value for key, value in expected_provenance.items()):
        raise ValueError(f"Generation provenance mismatch: {record['row_id']}")
    payload = record.get("request_payload") or {}
    reference_blobs = payload.get("referenceBlobs") or []
    if payload.get("prompt") != candidate["text"] or reference_blobs != [{"id": binding.get("blob_id")}]:
        raise ValueError(f"Generation payload mismatch: {record['row_id']}")
    raw_path = Path(record.get("raw_response_path", ""))
    if not raw_path.is_absolute():
        raw_path = (run_dir / raw_path).resolve()
    validate_file(raw_path, record["raw_response_sha256"])
    image = record.get("generated_image") or {}
    path = Path(image.get("path", ""))
    if not path.is_absolute():
        path = (run_dir / path).resolve()
    validate_file(path, image["sha256"], image["bytes"])
    with Image.open(path) as opened:
        if opened.size != (image["native_width"], image["native_height"]):
            raise ValueError(f"Generated dimensions differ: {record['row_id']}")
    if Path(image["filename"]).name != image["filename"]:
        raise ValueError(f"Generated image filename is not flat: {record['row_id']}")


def load_full_record(case: dict[str, Any]) -> dict[str, Any]:
    path_value = case.get("record_path") or case.get("accepted_record_path")
    expected = case.get("record_sha256") or case.get("accepted_record_sha256")
    if not path_value or not expected:
        raise ValueError(f"Accepted case lacks full record provenance: {case.get('case_id')}")
    path = Path(path_value)
    raw = validate_file(path, expected)
    return json.loads(raw)


def load_normalization_audit(case: dict[str, Any], full_record: dict[str, Any]) -> dict[str, Any]:
    required = (
        "raw_parsed_output_sha256", "normalized_output_path",
        "normalized_output_file_sha256", "normalized_output_semantic_sha256",
        "normalization_log_path", "normalization_log_file_sha256",
        "validation_audit_path",
    )
    missing = [field for field in required if not case.get(field)]
    if missing:
        raise ValueError(f"Accepted case lacks normalization provenance {missing}: {case.get('case_id')}")
    raw_output = full_record.get("parsed_output")
    if not isinstance(raw_output, dict) or canonical_sha256(raw_output) != case["raw_parsed_output_sha256"]:
        raise ValueError(f"Raw parsed output identity differs: {case.get('case_id')}")
    normalized_raw = validate_file(
        Path(case["normalized_output_path"]), case["normalized_output_file_sha256"]
    )
    normalized = json.loads(normalized_raw)
    if canonical_sha256(normalized) != case["normalized_output_semantic_sha256"]:
        raise ValueError(f"Normalized output semantic hash differs: {case.get('case_id')}")
    log_raw = validate_file(Path(case["normalization_log_path"]), case["normalization_log_file_sha256"])
    normalization_log = json.loads(log_raw)
    if (
        normalization_log.get("raw_output_semantic_sha256") != case["raw_parsed_output_sha256"]
        or normalization_log.get("normalized_output_semantic_sha256") != case["normalized_output_semantic_sha256"]
    ):
        raise ValueError(f"Normalization log targets different bytes: {case.get('case_id')}")
    validation_audit = json.loads(Path(case["validation_audit_path"]).read_text(encoding="utf-8"))
    if validation_audit.get("raw_record_sha256") != case.get("record_sha256"):
        raise ValueError(f"Validation audit targets different raw record: {case.get('case_id')}")
    if validation_audit.get("normalized_output_semantic_sha256") != case["normalized_output_semantic_sha256"]:
        raise ValueError(f"Validation audit targets different normalized output: {case.get('case_id')}")
    return {
        "raw_model_record": full_record,
        "raw_model_output": raw_output,
        "normalized_output": normalized,
        "normalization_log": normalization_log,
        "validation_audit": validation_audit,
    }


def load_rejected_attempts() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    if not MANUAL_REVIEW_PATH.exists():
        return {}, {"exists": False, "path": str(MANUAL_REVIEW_PATH)}
    document = json.loads(MANUAL_REVIEW_PATH.read_text(encoding="utf-8"))
    normalized_by_semantic = {}
    for path in sorted((EVAL_ROOT / "normalized_outputs").glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        normalized_by_semantic[canonical_sha256(value)] = {"path": str(path), "output": value}
    by_case: dict[str, list[dict[str, Any]]] = {}
    for item in document.get("rejected_attempts", []):
        record_path = Path(item["record_path"])
        raw_record = json.loads(validate_file(record_path, item["raw_record_sha256"]))
        normalized = normalized_by_semantic.get(item["normalized_output_semantic_sha256"])
        if not normalized:
            raise ValueError(f"Rejected normalized output is missing: {item.get('case_id')}")
        if raw_record.get("case_id") != item.get("case_id"):
            raise ValueError(f"Rejected raw record case differs: {item.get('case_id')}")
        by_case.setdefault(item["case_id"], []).append({
            "rejection": item,
            "raw_model_record": raw_record,
            "raw_model_output": raw_record.get("parsed_output"),
            "normalized_output_path": normalized["path"],
            "normalized_output": normalized["output"],
        })
    metadata = {
        "exists": True, "path": str(MANUAL_REVIEW_PATH),
        "sha256": sha256_path(MANUAL_REVIEW_PATH),
        "status": document.get("status"),
        "rejected_attempt_count": sum(len(items) for items in by_case.values()),
        "case_count": len(by_case),
    }
    return by_case, metadata


def load_prompt_exports(manifest_sha: str, accepted_sha: str, selection_sha: str) -> dict[str, Any]:
    expected_counts = {"all_540": 540, "selected_108": 108}
    exports = {}
    for name, path in PROMPT_EXPORT_PATHS.items():
        raw = path.read_bytes()
        value = json.loads(raw)
        prompts = value.get("prompts") or []
        if len(prompts) != expected_counts[name] or value.get("counts", {}).get("prompts") != expected_counts[name]:
            raise ValueError(f"Prompt export count differs: {path}")
        provenance = value.get("provenance") or {}
        expected_provenance = {
            "manifest_sha256": manifest_sha,
            "accepted_prompt_cases_sha256": accepted_sha,
            "selection_manifest_sha256": selection_sha,
        }
        if any(provenance.get(key) != expected for key, expected in expected_provenance.items()):
            raise ValueError(f"Prompt export provenance differs: {path}")
        keys = [item.get("candidate_key") for item in prompts]
        if len(set(keys)) != len(keys) or any(
            sha256_bytes(item.get("text", "").encode("utf-8")) != item.get("text_sha256")
            for item in prompts
        ):
            raise ValueError(f"Prompt export candidate identity differs: {path}")
        if name == "selected_108" and not all(item.get("selected_for_image_eval") is True for item in prompts):
            raise ValueError(f"Selected prompt export contains an unselected row: {path}")
        exports[name] = {
            "path": str(path), "sha256": sha256_bytes(raw), "bytes": len(raw),
            "prompt_count": len(prompts),
            "download_href": "../generation_prompts.json" if name == "all_540" else "../generation_prompts_selected.json",
        }
    return exports


def build_data(run_dir: Path, final: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    gate = readiness()
    if not gate["ready"]:
        raise RuntimeError(f"Publication gate is closed: {json.dumps(gate, sort_keys=True)}")
    manifest, manifest_raw = read_json_bytes(MANIFEST_PATH)
    accepted, accepted_raw = read_json_bytes(ACCEPTED_PATH)
    selection, selection_raw = read_json_bytes(SELECTION_PATH)
    manifest_sha = sha256_bytes(manifest_raw)
    accepted_sha = sha256_bytes(accepted_raw)
    selection_sha = sha256_bytes(selection_raw)
    if accepted.get("manifest_sha256") != manifest_sha or selection.get("manifest_sha256") != manifest_sha:
        raise ValueError("Accepted or selection artifact targets a different manifest")
    if selection.get("accepted_prompt_cases_sha256") != accepted_sha:
        raise ValueError("Selection artifact targets a different accepted candidate bank")
    prompt_exports = load_prompt_exports(manifest_sha, accepted_sha, selection_sha)
    sources = index_unique(manifest["sources"], "source_id")
    renders = index_unique(manifest["renders"], "render_id")
    cases = index_unique(manifest["cases"], "case_id")
    if (len(sources), len(renders), len(cases)) != (EXPECTED_SOURCES, EXPECTED_RENDERS, EXPECTED_CASES):
        raise ValueError("V4 manifest inventory differs from 9 sources, 4 renders, and 18 cases")
    source_values = {}
    for source_id, source in sources.items():
        path = Path(source["source_json_path"])
        raw = validate_file(path, source["sha256"], source["bytes"])
        source_values[source_id] = json.loads(raw)
    reference_manifest = copy_reference_assets(renders, run_dir, manifest_sha)
    rejected_attempts_by_case, rejected_attempts_metadata = load_rejected_attempts()

    accepted_cases = accepted["cases"]
    if set(accepted_cases) != set(cases):
        raise ValueError("Accepted candidate bank does not exactly join the 18 manifest cases")
    normalized_cases = {}
    candidates = []
    candidates_by_key = {}
    for case_id, manifest_case in sorted(cases.items()):
        case = accepted_cases[case_id]
        for field in ("case_id", "group_id", "source_id", "device_type", "camera_tag", "view_role", "render_id", "input_sha256"):
            if case.get(field) != manifest_case.get(field):
                raise ValueError(f"Accepted case differs from manifest for {field}: {case_id}")
        input_path = Path(manifest_case["input_path"])
        input_raw = validate_file(input_path, manifest_case["input_sha256"])
        input_value = json.loads(input_raw)
        if set(input_value) != {"source_messaging", "camera_tag"}:
            raise ValueError(f"V4 runtime input is not tag-only: {case_id}")
        if input_value["camera_tag"] != manifest_case["camera_tag"] or input_value["source_messaging"] != source_values[manifest_case["source_id"]]:
            raise ValueError(f"V4 runtime input content differs: {case_id}")
        full_record = load_full_record(case)
        normalization_audit = load_normalization_audit(case, full_record)
        raw_candidates = case.get("candidates") or []
        if len(raw_candidates) != 30:
            raise ValueError(f"Accepted bank must contain 30 candidates: {case_id}")
        ids = []
        prior_score = math.inf
        for index, raw_candidate in enumerate(raw_candidates, 1):
            candidate_id = raw_candidate.get("id") or raw_candidate.get("candidate_id")
            candidate_key = raw_candidate.get("candidate_key") or f"{case_id}::{candidate_id}"
            rank = raw_candidate.get("rank", index)
            text = raw_candidate.get("text")
            text_sha = raw_candidate.get("text_sha256") or sha256_bytes(text.encode("utf-8"))
            score = raw_candidate.get("source_relevance_score")
            components = raw_candidate.get("score_components") or {}
            if candidate_id != f"p{index}" or rank != index or candidate_key != f"{case_id}::{candidate_id}":
                raise ValueError(f"Candidate order/key differs at rank {index}: {case_id}")
            if sha256_bytes(text.encode("utf-8")) != text_sha:
                raise ValueError(f"Candidate text hash differs: {candidate_key}")
            if sum(components.values()) != score or not 0 <= score <= 100 or score > prior_score:
                raise ValueError(f"Candidate score arithmetic/order differs: {candidate_key}")
            prior_score = score
            ids.append(candidate_id)
            normalized = {
                **raw_candidate,
                "id": candidate_id,
                "candidate_id": candidate_id,
                "candidate_key": candidate_key,
                "rank": rank,
                "rank_bin": raw_candidate.get("rank_bin") or ("1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30"),
                "text_sha256": text_sha,
                "case_id": case_id,
                "group_id": manifest_case["group_id"],
                "source_id": manifest_case["source_id"],
                "device_type": manifest_case["device_type"],
                "camera_tag": manifest_case["camera_tag"],
                "view_role": manifest_case["view_role"],
                "render_id": manifest_case["render_id"],
                "raw_candidate": raw_candidate,
                "selection": None,
            }
            if candidate_key in candidates_by_key:
                raise ValueError(f"Duplicate candidate key: {candidate_key}")
            candidates_by_key[candidate_key] = normalized
            candidates.append(normalized)
        if ids != [f"p{i}" for i in range(1, 31)]:
            raise ValueError(f"Candidate IDs are not p1..p30: {case_id}")
        normalized_output = normalization_audit["normalized_output"]
        normalized_prompts = normalized_output.get("prompts") or []
        if len(normalized_prompts) != 30:
            raise ValueError(f"Normalized output must contain 30 prompts: {case_id}")
        for accepted_candidate, normalized_candidate in zip(raw_candidates, normalized_prompts):
            accepted_model_fields = {
                key: accepted_candidate.get(key) for key in MODEL_CANDIDATE_FIELDS
            }
            if accepted_model_fields != normalized_candidate:
                raise ValueError(f"Accepted candidate differs from normalized output: {case_id}")
        if case.get("debug") != normalized_output.get("debug"):
            raise ValueError(f"Accepted debug differs from normalized output: {case_id}")
        normalized_cases[case_id] = {
            "manifest": manifest_case,
            "input": input_value,
            "accepted": case,
            "rejected_attempts": rejected_attempts_by_case.get(case_id, []),
            **normalization_audit,
        }
    if len(candidates) != EXPECTED_CANDIDATES:
        raise ValueError("Candidate inventory must be exactly 540")
    environment_counts = dict(Counter(item["environment"] for item in candidates))
    if set(environment_counts) != set(EXPECTED_ENVIRONMENTS):
        raise ValueError(f"V4 candidates must natively cover all six environments: {environment_counts}")

    normalized_selections = []
    per_case = Counter()
    per_case_stratum = Counter()
    selection_ids = set()
    for raw_selection in selection["selections"]:
        item = normalize_selection(raw_selection)
        candidate_key = item.get("candidate_key")
        if candidate_key not in candidates_by_key:
            raise ValueError(f"Selection references unknown candidate: {candidate_key}")
        candidate = candidates_by_key[candidate_key]
        case_id = candidate["case_id"]
        if item["selection_id"] in selection_ids:
            raise ValueError(f"Duplicate selection ID: {item['selection_id']}")
        selection_ids.add(item["selection_id"])
        for field in ("case_id", "group_id", "source_id", "device_type", "camera_tag", "view_role"):
            if item.get(field) != candidate.get(field):
                raise ValueError(f"Selection differs from candidate for {field}: {candidate_key}")
        if item["candidate_id"] != candidate["candidate_id"] or item["rank"] != candidate["rank"]:
            raise ValueError(f"Selection candidate identity differs: {candidate_key}")
        if item["candidate_text"] != candidate["text"] or item["candidate_text_sha256"] != candidate["text_sha256"]:
            raise ValueError(f"Selection candidate text differs: {candidate_key}")
        if item["score_total"] != candidate["source_relevance_score"]:
            raise ValueError(f"Selection candidate score differs: {candidate_key}")
        if item["reference_render_id"] != candidate["render_id"]:
            raise ValueError(f"Selection render differs: {candidate_key}")
        if item.get("semantic_review_status") != EXPECTED_SEMANTIC_STATUS:
            raise ValueError(f"Selection is not root-approved: {candidate_key}")
        per_case[case_id] += 1
        per_case_stratum[(case_id, item["rank_stratum"])] += 1
        candidate["selection"] = item
        normalized_selections.append(item)
    if len(normalized_selections) != EXPECTED_SELECTIONS or set(per_case.values()) != {6}:
        raise ValueError("Selection must contain exactly six candidates per case")
    expected_case_strata = {(case_id, stratum) for case_id in cases for stratum in EXPECTED_STRATA}
    if set(per_case_stratum) != expected_case_strata or set(per_case_stratum.values()) != {2}:
        raise ValueError("Selection must contain exactly two candidates in each rank stratum")

    records = load_records(run_dir)
    rows = []
    expected_row_ids = set()
    for item in normalized_selections:
        candidate = candidates_by_key[item["candidate_key"]]
        render_id = item["reference_render_id"]
        row_id = f"{candidate['source_id']}__{candidate['camera_tag']}__{candidate['candidate_id']}__{render_id}"
        expected_row_ids.add(row_id)
        record = records.get(row_id)
        if record:
            for field, expected in (
                ("case_id", candidate["case_id"]), ("group_id", candidate["group_id"]),
                ("selection_key", item["selection_id"]), ("source_id", candidate["source_id"]),
                ("candidate_id", candidate["candidate_id"]), ("render_id", render_id),
                ("device_type", candidate["device_type"]), ("camera_tag", candidate["camera_tag"]),
            ):
                if record.get(field) != expected:
                    raise ValueError(f"Generation record differs for {field}: {row_id}")
            validate_done_record(
                record, renders[render_id], run_dir, candidate, item,
                manifest_sha, accepted_sha, selection_sha,
            )
        rows.append({
            "row_id": row_id,
            "selection_id": item["selection_id"],
            "candidate_key": candidate["candidate_key"],
            "case_id": candidate["case_id"],
            "source_id": candidate["source_id"],
            "device_type": candidate["device_type"],
            "camera_tag": candidate["camera_tag"],
            "render_id": render_id,
            "status": record.get("status") if record else "missing",
            "result": record,
        })
    unexpected_records = sorted(set(records) - expected_row_ids)
    if unexpected_records:
        raise ValueError(f"Generation records are outside the approved 108 selections: {unexpected_records[:5]}")
    status_counts = dict(sorted(Counter(row["status"] for row in rows).items()))
    if final and (status_counts.get("missing", 0) or status_counts.get("pending", 0)):
        raise ValueError(f"Final gallery has incomplete generation rows: {status_counts}")

    system_prompt_path = Path(manifest["provenance"]["system_prompt"]["path"])
    system_prompt = validate_file(system_prompt_path, manifest["provenance"]["system_prompt"]["sha256"]).decode("utf-8")
    input_schema_path = Path(manifest["provenance"]["input_schema"]["path"])
    output_schema_path = Path(manifest["provenance"]["output_schema"]["path"])
    input_schema = json.loads(validate_file(input_schema_path, manifest["provenance"]["input_schema"]["sha256"]))
    output_schema = json.loads(validate_file(output_schema_path, manifest["provenance"]["output_schema"]["sha256"]))
    data = {
        "metadata": {
            "version": "hp-lived-in-v4-gallery-data-v1",
            "mode": "final" if final else "progressive",
            "source_count": len(sources),
            "case_count": len(cases),
            "candidate_count": len(candidates),
            "expected_candidate_count": EXPECTED_CANDIDATES,
            "selected_count": len(normalized_selections),
            "expected_selected_count": EXPECTED_SELECTIONS,
            "generation_status_counts": status_counts,
            "environment_counts": environment_counts,
            "manifest_sha256": manifest_sha,
            "accepted_prompt_cases_sha256": accepted_sha,
            "selection_manifest_sha256": selection_sha,
        },
        "run_context": {
            "manifest": manifest,
            "accepted_prompt_cases_metadata": {key: value for key, value in accepted.items() if key != "cases"},
            "selection_manifest_metadata": {key: value for key, value in selection.items() if key != "selections"},
            "selection_algorithm": selection.get("algorithm"),
            "system_prompt": system_prompt,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "reference_assets": reference_manifest,
            "rejected_attempts": rejected_attempts_metadata,
            "prompt_exports": prompt_exports,
            "publication_gate": gate,
        },
        "sources": source_values,
        "renders": renders,
        "cases": normalized_cases,
        "candidates": candidates,
        "selections": normalized_selections,
        "generation_rows": rows,
    }
    build = {
        "version": "hp-lived-in-v4-gallery-build-v1",
        "mode": "final" if final else "progressive",
        "manifest_sha256": manifest_sha,
        "accepted_prompt_cases_sha256": accepted_sha,
        "selection_manifest_sha256": selection_sha,
        "source_count": len(sources),
        "case_count": len(cases),
        "candidate_count": len(candidates),
        "selected_count": len(normalized_selections),
        "generation_row_count": len(rows),
        "generation_record_count": len(records),
        "generation_status_counts": status_counts,
        "environment_counts": environment_counts,
        "reference_asset_count": reference_manifest["asset_count"],
        "reference_asset_bytes": reference_manifest["total_bytes"],
        "publication_gate": gate,
    }
    return data, build


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--check-readiness", action="store_true")
    args = parser.parse_args()
    if args.check_readiness:
        gate = readiness()
        print(json.dumps(gate, indent=2))
        raise SystemExit(0 if gate["ready"] else 3)
    run_dir = args.run_dir.resolve()
    data, build = build_data(run_dir, args.final)
    gallery_dir = run_dir / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)
    for filename in ("index.html", "main.js", "style.css"):
        shutil.copyfile(TEMPLATE_DIR / filename, gallery_dir / filename)
    shutil.copyfile(SHARED_IMS_AUTH, gallery_dir / "imsauth.js")
    data_bytes = ("const V4_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n").encode("utf-8")
    for pattern in SECRET_PATTERNS:
        if pattern.search(data_bytes.decode("utf-8")):
            raise ValueError(f"Secret-like value found in gallery data: {pattern.pattern}")
    atomic_write(gallery_dir / "data.js", data_bytes)
    artifacts = {}
    for path in sorted(gallery_dir.iterdir()):
        if path.is_file():
            artifacts[path.name] = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256_path(path)}
    build.update({"run_dir": str(run_dir), "gallery_dir": str(gallery_dir), "artifacts": artifacts, "model_called_by_builder": False, "image_generation_called_by_builder": False})
    atomic_json(run_dir / "gallery_build.json", build)
    print(json.dumps(build, indent=2))


if __name__ == "__main__":
    main()

