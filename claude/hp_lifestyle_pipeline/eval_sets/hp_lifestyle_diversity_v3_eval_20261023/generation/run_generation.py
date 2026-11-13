#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "pillow"]
# ///
"""Resumable HP diversity-V3 image generation with immutable provenance.

Exactly six selected candidates from each of 18 source/camera groups expand to
exactly 108 rows. Each group is bound to one approved render. Reference PNG
bytes and every candidate/selection artifact are verified before upload; async
job identities are journaled before polling so a restart never blindly
resubmits a known job.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import httpx
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVAL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = EVAL_ROOT / "manifest.json"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
SELECTION_PATH = EVAL_ROOT / "selection_manifest.json"
DEFAULT_RUN_DIR = (
    PROJECT_ROOT
    / "local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023"
)

BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev"
UPLOAD_URL = f"{BASE_URL}/v2/storage/image"
GENERATE_URL = f"{BASE_URL}/v1/image/generate"
METADATA_URL = f"{BASE_URL}/v1/metadata"
OPENAPI_URL = f"{BASE_URL}/openapi.json"
MODEL_ID = "hp-image"
REWRITER_MODEL = "gemini-3.1-pro"
NUM_INFERENCE_STEPS = 50
SEED = 42
N = 1
POLL_INTERVAL_SECONDS = 5
DEFAULT_POLL_WINDOW_SECONDS = 1800
MAX_WORKERS = 8
MAX_SAFE_SUBMIT_ATTEMPTS = 3
TARGET_PIXEL_BUDGET = 2368 * 1776
EXPECTED_SOURCE_COUNT = 9
EXPECTED_GROUP_COUNT = 18
EXPECTED_CANDIDATE_INVENTORY_COUNT = 540
EXPECTED_SELECTION_COUNT = 108
EXPECTED_SELECTIONS_PER_GROUP = 6
EXPECTED_RENDER_COUNT = 4
SELECTION_STRATA = {
    "upper_rank_1_10": {"rank_bin": "1-10", "ranks": range(1, 11)},
    "middle_rank_11_20": {"rank_bin": "11-20", "ranks": range(11, 21)},
    "lower_rank_21_30": {"rank_bin": "21-30", "ranks": range(21, 31)},
}
EXPECTED_SELECTIONS_PER_STRATUM = 2

_print_lock = threading.Lock()
_binding_lock = threading.Lock()

BINDING_PROVENANCE_FIELDS = (
    "blob_id",
    "render_id",
    "original_png_path",
    "original_png_sha256",
    "original_png_bytes",
    "original_png_width",
    "original_png_height",
    "source_camera_name",
    "device_type",
    "product_provenance",
    "source_manifest_sha256",
    "upload_endpoint",
    "content_type",
)

ROW_IDENTITY_FIELDS = (
    "row_id",
    "case_id",
    "group_id",
    "selection_key",
    "source_id",
    "render_id",
    "candidate_id",
    "device_type",
    "camera_tag",
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def log(message: str) -> None:
    with _print_lock:
        print(f"[{dt.datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def atomic_write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp"
    )
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_write_json(path: Path, value: Any) -> None:
    value = sanitize_endpoint_value(value)
    atomic_write_bytes(
        path,
        (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_stem(row_id: str) -> str:
    readable = re.sub(r"[^A-Za-z0-9._-]+", "_", row_id).strip("_")[:90]
    return f"{sha256_bytes(row_id.encode())[:20]}__{readable}"


def sanitize_endpoint_value(value: Any) -> Any:
    """Strip presigned URLs and auth material before any JSON artifact is written."""
    sensitive_keys = {
        "authorization",
        "presignedurl",
        "x-gw-ims-user-token",
        "x-amz-security-token",
        "x-amz-credential",
        "x-amz-signature",
    }
    if isinstance(value, dict):
        return {
            key: sanitize_endpoint_value(child)
            for key, child in value.items()
            if key.casefold() not in sensitive_keys
        }
    if isinstance(value, list):
        return [sanitize_endpoint_value(child) for child in value]
    if isinstance(value, str) and any(
        marker in value.casefold()
        for marker in ("x-amz-signature=", "x-amz-credential=", "x-amz-security-token=")
    ):
        return "[redacted_presigned_url]"
    return value


def safe_error(exc: BaseException) -> str:
    value = sanitize_endpoint_value(f"{type(exc).__name__}: {exc}")
    return str(value)


def exact_ratio_dimensions(source_width: int, source_height: int) -> tuple[int, int]:
    """Choose exact-ratio multiples of 16 near the historical pixel budget."""
    divisor = math.gcd(source_width, source_height)
    ratio_width = source_width // divisor
    ratio_height = source_height // divisor
    if (ratio_width, ratio_height) == (16, 9):
        return 2560, 1440

    factor_multiple = math.lcm(
        16 // math.gcd(ratio_width, 16),
        16 // math.gcd(ratio_height, 16),
    )
    candidates: list[tuple[int, int]] = []
    factor = factor_multiple
    while ratio_width * factor <= 3072 and ratio_height * factor <= 3072:
        width, height = ratio_width * factor, ratio_height * factor
        if width >= 256 and height >= 256:
            candidates.append((width, height))
        factor += factor_multiple
    if not candidates:
        raise ValueError(
            f"No exact-ratio endpoint dimensions for {source_width}x{source_height}"
        )
    return min(
        candidates,
        key=lambda size: (abs(size[0] * size[1] - TARGET_PIXEL_BUDGET), -size[0]),
    )


def stable_binding(binding: dict[str, Any]) -> dict[str, Any]:
    return {field: binding.get(field) for field in BINDING_PROVENANCE_FIELDS}


def require_file_hash(path_value: str, expected_sha256: str, label: str) -> Path:
    path = Path(path_value)
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    actual = sha256_path(path)
    if actual != expected_sha256:
        raise ValueError(f"{label} SHA-256 differs: {actual} != {expected_sha256}")
    return path


def load_inputs() -> tuple[
    dict[str, Any], str, dict[str, Any], str, dict[str, Any], str
]:
    manifest_raw = MANIFEST_PATH.read_bytes()
    accepted_raw = ACCEPTED_PATH.read_bytes()
    selection_raw = SELECTION_PATH.read_bytes()
    manifest_sha256 = sha256_bytes(manifest_raw)
    accepted_sha256 = sha256_bytes(accepted_raw)
    selection_sha256 = sha256_bytes(selection_raw)
    manifest = json.loads(manifest_raw)
    accepted = json.loads(accepted_raw)
    selection = json.loads(selection_raw)
    if accepted.get("manifest_sha256") != manifest_sha256:
        raise ValueError(
            "Accepted candidate bank targets a different V3 manifest: "
            f"{accepted.get('manifest_sha256')} != {manifest_sha256}"
        )
    if selection.get("manifest_sha256") != manifest_sha256:
        raise ValueError(
            "Selection manifest targets a different V3 manifest: "
            f"{selection.get('manifest_sha256')} != {manifest_sha256}"
        )
    if selection.get("accepted_prompt_cases_sha256") != accepted_sha256:
        raise ValueError(
            "Selection manifest targets a different accepted candidate bank: "
            f"{selection.get('accepted_prompt_cases_sha256')} != {accepted_sha256}"
        )
    expected_manifest_counts = {
        "source_count": EXPECTED_SOURCE_COUNT,
        "case_count": EXPECTED_GROUP_COUNT,
        "render_count": EXPECTED_RENDER_COUNT,
        "candidates_per_case": 30,
    }
    for field, expected in expected_manifest_counts.items():
        if manifest.get("scope", {}).get(field) != expected:
            raise ValueError(f"V3 manifest {field} must be {expected}")
    expected_selection_counts = {
        "accepted_banks": EXPECTED_GROUP_COUNT,
        "selected": EXPECTED_SELECTION_COUNT,
    }
    for field, expected in expected_selection_counts.items():
        if selection.get("counts", {}).get(field) != expected:
            raise ValueError(f"V3 selection {field} must be {expected}")
    if len(manifest.get("sources", [])) != EXPECTED_SOURCE_COUNT:
        raise ValueError("V3 manifest must contain exactly nine sources")
    if len(manifest.get("cases", [])) != EXPECTED_GROUP_COUNT:
        raise ValueError("V3 manifest must contain exactly 18 source/camera groups")
    if len(manifest.get("renders", [])) != EXPECTED_RENDER_COUNT:
        raise ValueError("V3 manifest must contain exactly four approved renders")
    if len(selection.get("selections", [])) != EXPECTED_SELECTION_COUNT:
        raise ValueError("V3 selection manifest must contain exactly 108 selections")
    accepted_counts = accepted.get("counts", {})
    if accepted.get("status") not in {
        "complete_human_review_required",
        "complete",
    }:
        raise ValueError(
            "Accepted candidate bank must be complete or complete_human_review_required"
        )
    if accepted_counts.get("accepted_cases") != EXPECTED_GROUP_COUNT:
        raise ValueError("Accepted candidate bank must contain exactly 18 cases")
    if accepted_counts.get("candidates") != EXPECTED_CANDIDATE_INVENTORY_COUNT:
        raise ValueError("Accepted candidate bank must contain exactly 540 candidates")
    if len(accepted.get("cases", {})) != EXPECTED_GROUP_COUNT:
        raise ValueError("Accepted candidate case mapping must contain exactly 18 cases")
    return (
        manifest,
        manifest_sha256,
        accepted,
        accepted_sha256,
        selection,
        selection_sha256,
    )


def validate_render(render: dict[str, Any]) -> None:
    if render["device_type"] not in {"laptop", "printer"}:
        raise ValueError(f"Excluded device type reached runner: {render['device_type']}")
    path = Path(render["path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    raw = path.read_bytes()
    if len(raw) != render["bytes"] or sha256_bytes(raw) != render["sha256"]:
        raise ValueError(f"Render bytes differ from manifest: {render['render_id']}")
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Reference is not an original PNG: {path}")
    with Image.open(path) as image:
        native_size = image.size
        image_format = image.format
    if native_size != (render["width"], render["height"]) or image_format != "PNG":
        raise ValueError(f"Render image metadata differs from manifest: {render['render_id']}")
    output_size = exact_ratio_dimensions(render["width"], render["height"])
    if output_size != (render["output_width"], render["output_height"]):
        raise ValueError(
            f"Manifest output dimensions violate exact-ratio policy for {render['render_id']}: "
            f"{render['output_width']}x{render['output_height']} != {output_size[0]}x{output_size[1]}"
        )
    if render.get("preserve_aspect_ratio") is not True:
        raise ValueError(f"Render does not require aspect preservation: {render['render_id']}")
    if render["width"] * render["output_height"] != render["height"] * render["output_width"]:
        raise ValueError(f"Output aspect ratio differs for {render['render_id']}")


def normalized_render(render: dict[str, Any]) -> dict[str, Any]:
    value = dict(render)
    output_width, output_height = exact_ratio_dimensions(render["width"], render["height"])
    value.update(
        {
            "output_width": output_width,
            "output_height": output_height,
            "preserve_aspect_ratio": True,
            "product_provenance": render.get("product_provenance") or render.get("pair_id"),
        }
    )
    return value


def build_rows(
    manifest: dict[str, Any], accepted: dict[str, Any], selection: dict[str, Any]
) -> list[dict[str, Any]]:
    cases = {item["case_id"]: item for item in manifest["cases"]}
    renders = {item["render_id"]: normalized_render(item) for item in manifest["renders"]}
    sources = {item["source_id"]: item for item in manifest["sources"]}
    accepted_cases = accepted["cases"]
    if len(cases) != len(manifest["cases"]):
        raise ValueError("Duplicate case_id in V3 manifest")
    if len(renders) != len(manifest["renders"]):
        raise ValueError("Duplicate render_id in V3 manifest")
    if len(sources) != len(manifest["sources"]):
        raise ValueError("Duplicate source_id in V3 manifest")
    for source in sources.values():
        if source.get("device_type") not in {"laptop", "printer"}:
            raise ValueError(f"Excluded source device type: {source.get('device_type')}")
        require_file_hash(
            source["source_json_path"], source["sha256"], "source JSON"
        )
    if set(accepted_cases) != set(cases):
        raise ValueError("Accepted candidate case IDs must exactly match the 18 manifest cases")
    for case_id, case in cases.items():
        require_file_hash(case["input_path"], case["input_sha256"], f"input for {case_id}")
        if case["render_id"] not in renders:
            raise ValueError(f"Case has unknown render: {case_id}")
        render = renders[case["render_id"]]
        if render["device_type"] != case["device_type"] or render["camera_tag"] != case["camera_tag"]:
            raise ValueError(f"Case has cross-type or cross-tag render: {case_id}")
        bank = accepted_cases[case_id]
        candidates = bank.get("candidates", [])
        if len(candidates) != 30:
            raise ValueError(f"Accepted case must contain exactly 30 candidates: {case_id}")
        if {candidate.get("rank") for candidate in candidates} != set(range(1, 31)):
            raise ValueError(f"Accepted case ranks must be exactly 1..30: {case_id}")
        keys = [candidate.get("candidate_key") for candidate in candidates]
        if len(set(keys)) != 30:
            raise ValueError(f"Accepted case candidate keys must be unique: {case_id}")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    case_counts: dict[str, int] = {}
    stratum_counts: dict[tuple[str, str], int] = {}
    for item in sorted(selection["selections"], key=lambda value: value["selection_key"]):
        required = {
            "selection_key", "candidate_key", "case_id", "group_id", "source_id",
            "device_type", "camera_tag", "view_role", "candidate_id", "rank", "rank_bin",
            "selection_stratum",
            "score_total", "selection_reason", "text", "text_sha256", "render_id",
            "render_path", "render_sha256", "input_sha256", "accepted_record_path",
            "accepted_record_sha256", "semantic_review_status",
        }
        missing = sorted(required - set(item))
        if missing:
            raise ValueError(f"Selection {item.get('selection_key')} lacks fields: {missing}")
        case_id = item["case_id"]
        if case_id not in cases:
            raise ValueError(f"Selection contains unknown case: {case_id}")
        case = cases[case_id]
        for field in (
            "case_id", "group_id", "source_id", "device_type", "camera_tag",
            "view_role", "render_id", "input_sha256",
        ):
            if item[field] != case[field]:
                raise ValueError(f"Selection {item['selection_key']} differs from case for {field}")
        accepted_case = accepted_cases.get(case_id)
        if not accepted_case or accepted_case.get("status") not in {
            "normalized_validator_passed_pending_human_review",
            "normalized_validator_passed",
        }:
            raise ValueError(f"Selection has no accepted candidate bank: {case_id}")
        for field in (
            "case_id", "group_id", "source_id", "device_type", "camera_tag",
            "view_role", "render_id", "input_sha256",
        ):
            if accepted_case[field] != case[field]:
                raise ValueError(f"Accepted bank {case_id} differs from manifest for {field}")
        source = sources[item["source_id"]]
        if source["device_type"] != item["device_type"]:
            raise ValueError(f"Cross-type source association: {item['selection_key']}")
        render = renders[item["render_id"]]
        if render["device_type"] != item["device_type"] or render["camera_tag"] != item["camera_tag"]:
            raise ValueError(f"Cross-type or cross-tag render association: {item['selection_key']}")
        if item["render_path"] != render["path"] or item["render_sha256"] != render["sha256"]:
            raise ValueError(f"Selection render identity differs: {item['selection_key']}")
        require_file_hash(
            item["accepted_record_path"], item["accepted_record_sha256"],
            f"accepted record for {item['selection_key']}",
        )
        if item["accepted_record_path"] != accepted_case["record_path"] or item["accepted_record_sha256"] != accepted_case["record_sha256"]:
            raise ValueError(f"Selection accepted-record identity differs: {item['selection_key']}")
        candidates = {candidate["candidate_key"]: candidate for candidate in accepted_case["candidates"]}
        candidate = candidates.get(item["candidate_key"])
        if not candidate:
            raise ValueError(f"Selection candidate is absent from accepted bank: {item['selection_key']}")
        expected_candidate_key = f"{case_id}::{item['candidate_id']}"
        expected_selection_key = f"{case_id}::{item['candidate_id']}::selected"
        if item["candidate_key"] != expected_candidate_key or item["selection_key"] != expected_selection_key:
            raise ValueError(f"Selection/candidate key mismatch: {item['selection_key']}")
        for selection_field, candidate_field in (
            ("candidate_id", "id"), ("rank", "rank"), ("rank_bin", "rank_bin"),
            ("score_total", "source_relevance_score"), ("text", "text"),
            ("text_sha256", "text_sha256"),
        ):
            if item[selection_field] != candidate[candidate_field]:
                raise ValueError(f"Selection differs from candidate for {selection_field}: {item['selection_key']}")
        if not item["text"] or sha256_bytes(item["text"].encode("utf-8")) != item["text_sha256"]:
            raise ValueError(f"Candidate text hash mismatch: {item['selection_key']}")
        if isinstance(item.get("score_total"), bool) or not isinstance(item.get("score_total"), (int, float)) or not 0 <= item["score_total"] <= 100:
            raise ValueError(f"Invalid 0-100 score: {item['selection_key']}")
        components = candidate["score_components"]
        if not isinstance(components, dict) or any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in components.values()):
            raise ValueError(f"Invalid rubric components: {item['selection_key']}")
        if not math.isclose(sum(components.values()), item["score_total"], abs_tol=1e-9):
            raise ValueError(f"Rubric components do not sum to score: {item['selection_key']}")
        rank = item["rank"]
        matching_strata = [
            name for name, definition in SELECTION_STRATA.items()
            if item["rank_bin"] == definition["rank_bin"] and rank in definition["ranks"]
        ]
        if len(matching_strata) != 1:
            raise ValueError(f"Rank/bin mismatch: {item['selection_key']}")
        stratum = matching_strata[0]
        if item["selection_stratum"] != stratum:
            raise ValueError(f"Rank/selection-stratum mismatch: {item['selection_key']}")
        if not isinstance(candidate["creative_departures"], list):
            raise ValueError(f"creative_departures must be an explicit list: {item['selection_key']}")
        forbidden = {key for key in candidate if key.casefold() in {"product", "product_name", "productname"}}
        if forbidden:
            raise ValueError(f"Runtime product-name fields are prohibited: {sorted(forbidden)}")
        row_id = (
            f"{item['source_id']}__{item['camera_tag']}__"
            f"{item['candidate_id']}__{item['render_id']}"
        )
        if row_id in seen:
            raise ValueError(f"Duplicate generation row ID: {row_id}")
        seen.add(row_id)
        case_counts[case_id] = case_counts.get(case_id, 0) + 1
        stratum_key = (case_id, stratum)
        stratum_counts[stratum_key] = stratum_counts.get(stratum_key, 0) + 1
        rows.append(
            {
                "row_id": row_id,
                "case_id": case_id,
                "group_id": item["group_id"],
                "selection_key": item["selection_key"],
                "source_id": item["source_id"],
                "render_id": item["render_id"],
                "candidate_id": item["candidate_id"],
                "device_type": item["device_type"],
                "camera_tag": item["camera_tag"],
                "source": source,
                "case": case,
                "render": render,
                "selection": item,
                "candidate": candidate,
                "accepted_case": accepted_case,
                "selected_candidate_sha256": canonical_sha256(candidate),
                "selection_row_sha256": canonical_sha256(item),
            }
        )
    if set(case_counts) != set(cases):
        raise ValueError("Every V3 source/camera case must have selected candidates")
    if any(count != EXPECTED_SELECTIONS_PER_GROUP for count in case_counts.values()):
        raise ValueError("Every V3 source/camera case must select exactly six candidates")
    for case_id in cases:
        for stratum in SELECTION_STRATA:
            if stratum_counts.get((case_id, stratum)) != EXPECTED_SELECTIONS_PER_STRATUM:
                raise ValueError(
                    f"Case {case_id} must select exactly two candidates from {stratum}"
                )
    if len(rows) != EXPECTED_SELECTION_COUNT:
        raise ValueError("V3 runner must expand to exactly 108 rows")
    return rows


def build_payload(row: dict[str, Any], blob_id: str) -> dict[str, Any]:
    render = row["render"]
    return {
        "prompt": row["candidate"]["text"],
        "size": {
            "width": render["output_width"],
            "height": render["output_height"],
        },
        "referenceBlobs": [{"id": blob_id}],
        "seeds": [SEED],
        "n": N,
        "modelSpecificPayload": {
            "enablePromptRewrite": True,
            "rewriterModel": REWRITER_MODEL,
            "numInferenceSteps": NUM_INFERENCE_STEPS,
        },
    }


def binding_document(run_dir: Path, manifest_sha256: str) -> dict[str, Any]:
    path = run_dir / "blob_bindings.json"
    if not path.exists():
        return {
            "schema_version": 1,
            "manifest_sha256": manifest_sha256,
            "upload_endpoint": UPLOAD_URL,
            "bindings": {},
        }
    document = read_json(path)
    if document.get("manifest_sha256") != manifest_sha256:
        raise ValueError("Blob cache belongs to a different manifest")
    if document.get("upload_endpoint") != UPLOAD_URL:
        raise ValueError("Blob cache belongs to a different upload endpoint")
    return document


def validate_binding(
    binding: dict[str, Any], render: dict[str, Any], manifest_sha256: str
) -> None:
    expected = {
        "render_id": render["render_id"],
        "original_png_path": str(Path(render["path"]).resolve()),
        "original_png_sha256": render["sha256"],
        "original_png_bytes": render["bytes"],
        "original_png_width": render["width"],
        "original_png_height": render["height"],
        "source_manifest_sha256": manifest_sha256,
        "upload_endpoint": UPLOAD_URL,
        "content_type": "image/png",
    }
    if not binding.get("blob_id"):
        raise ValueError(f"Binding lacks blob ID: {render['render_id']}")
    for field, value in expected.items():
        if binding.get(field) != value:
            raise ValueError(
                f"Cached binding differs for {render['render_id']} {field}: "
                f"{binding.get(field)!r} != {value!r}"
            )


def upload_one_reference(
    render: dict[str, Any], manifest_sha256: str
) -> dict[str, Any]:
    validate_render(render)
    path = Path(render["path"])
    raw = path.read_bytes()
    last_error = ""
    for attempt in range(1, 4):
        try:
            with httpx.Client(timeout=httpx.Timeout(180, connect=20)) as client:
                response = client.post(
                    UPLOAD_URL,
                    content=raw,
                    headers={"content-type": "image/png", "accept": "application/json"},
                )
            if 400 <= response.status_code < 500:
                raise RuntimeError(
                    f"terminal upload HTTP {response.status_code}: {response.text[:1000]}"
                )
            response.raise_for_status()
            body = response.json()
            uploaded = (body.get("images") or [{}])[0]
            if not uploaded.get("id"):
                raise ValueError(f"Upload returned no image ID: {body}")
            return {
                "blob_id": uploaded["id"],
                "render_id": render["render_id"],
                "original_png_path": str(path.resolve()),
                "original_png_sha256": sha256_bytes(raw),
                "original_png_bytes": len(raw),
                "original_png_width": render["width"],
                "original_png_height": render["height"],
                "source_camera_name": render["source_camera_name"],
                "device_type": render["device_type"],
                "product_provenance": render["product_provenance"],
                "source_manifest_sha256": manifest_sha256,
                "upload_endpoint": UPLOAD_URL,
                "content_type": "image/png",
                "uploaded_at_utc": utc_now(),
            }
        except RuntimeError as exc:
            if str(exc).startswith("terminal upload HTTP"):
                raise
            last_error = safe_error(exc)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError) as exc:
            last_error = safe_error(exc)
        if attempt < 3:
            time.sleep(3 * attempt)
    raise RuntimeError(f"Reference upload failed for {render['render_id']}: {last_error}")


def ensure_bindings(
    run_dir: Path,
    rows: list[dict[str, Any]],
    manifest_sha256: str,
    workers: int,
) -> dict[str, dict[str, Any]]:
    path = run_dir / "blob_bindings.json"
    document = binding_document(run_dir, manifest_sha256)
    required = {row["render_id"]: row["render"] for row in rows}
    for render_id, binding in document["bindings"].items():
        if render_id in required:
            validate_binding(binding, required[render_id], manifest_sha256)
    missing = [render for render_id, render in required.items() if render_id not in document["bindings"]]
    log(f"reference blobs: {len(required) - len(missing)} cached, {len(missing)} to upload")

    def upload(render: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        return render["render_id"], upload_one_reference(render, manifest_sha256)

    if missing:
        with ThreadPoolExecutor(max_workers=min(workers, len(missing))) as pool:
            futures = {pool.submit(upload, render): render for render in missing}
            for future in as_completed(futures):
                render_id, binding = future.result()
                with _binding_lock:
                    current = binding_document(run_dir, manifest_sha256)
                    current["bindings"][render_id] = binding
                    current["bindings"] = dict(sorted(current["bindings"].items()))
                    current["updated_at_utc"] = utc_now()
                    atomic_write_json(path, current)
                    document = current
                log(f"uploaded {render_id}")
    return {render_id: document["bindings"][render_id] for render_id in required}


def provenance(
    row: dict[str, Any], payload: dict[str, Any], binding: dict[str, Any],
    manifest_sha256: str, accepted_sha256: str, selection_sha256: str,
) -> dict[str, Any]:
    return {
        "manifest_sha256": manifest_sha256,
        "accepted_prompt_cases_path": str(ACCEPTED_PATH.resolve()),
        "accepted_prompt_cases_sha256": accepted_sha256,
        "selection_manifest_path": str(SELECTION_PATH.resolve()),
        "selection_manifest_sha256": selection_sha256,
        "selected_candidate_sha256": row["selected_candidate_sha256"],
        "selection_row_sha256": row["selection_row_sha256"],
        "accepted_record_path": row["selection"]["accepted_record_path"],
        "accepted_record_sha256": row["selection"]["accepted_record_sha256"],
        "raw_parsed_output_sha256": row["accepted_case"]["raw_parsed_output_sha256"],
        "normalized_output_path": row["accepted_case"]["normalized_output_path"],
        "normalized_output_file_sha256": row["accepted_case"]["normalized_output_file_sha256"],
        "normalized_output_semantic_sha256": row["accepted_case"]["normalized_output_semantic_sha256"],
        "normalization_log_path": row["accepted_case"]["normalization_log_path"],
        "normalization_log_file_sha256": row["accepted_case"]["normalization_log_file_sha256"],
        "candidate_text_sha256": row["candidate"]["text_sha256"],
        "case_sha256": canonical_sha256(row["case"]),
        "input_sha256": row["case"]["input_sha256"],
        "source_json_sha256": row["source"]["sha256"],
        "request_payload_sha256": canonical_sha256(payload),
        "reference_binding_sha256": canonical_sha256(stable_binding(binding)),
        "reference_blob_id": binding["blob_id"],
    }


def job_path(run_dir: Path, row_id: str) -> Path:
    return run_dir / "jobs" / f"{artifact_stem(row_id)}.json"


def record_path(run_dir: Path, row_id: str) -> Path:
    return run_dir / "records" / f"{artifact_stem(row_id)}.json"


def validate_existing_identity(
    value: dict[str, Any], row: dict[str, Any], payload: dict[str, Any], prov: dict[str, Any]
) -> None:
    for field in ROW_IDENTITY_FIELDS:
        if value.get(field) != row[field]:
            raise ValueError(f"Existing artifact identity mismatch for {row['row_id']} {field}")
    if value.get("request_payload") != payload or value.get("provenance") != prov:
        raise ValueError(f"Existing artifact provenance mismatch for {row['row_id']}")


def response_is_final(body: dict[str, Any], task_status: str) -> bool:
    status = str(body.get("status") or task_status or "").upper()
    return status in {"COMPLETED", "SUCCEEDED", "FAILED", "TIMEOUT", "CANCELLED"} or bool(
        body.get("outputs") or body.get("error_code") or body.get("error")
    )


def response_failed(body: dict[str, Any], task_status: str) -> bool:
    status = str(body.get("status") or task_status or "").upper()
    return status in {"FAILED", "TIMEOUT", "CANCELLED"} or bool(
        body.get("error_code") or body.get("error")
    )


def submit_job(
    run_dir: Path,
    row: dict[str, Any],
    payload: dict[str, Any],
    prov: dict[str, Any],
) -> dict[str, Any]:
    path = job_path(run_dir, row["row_id"])
    if path.exists():
        job = read_json(path)
        validate_existing_identity(job, row, payload, prov)
        if job.get("status") == "submitting":
            job.update(
                {
                    "status": "submission_ambiguous",
                    "failure_class": "process_interrupted_during_submit_held_no_retry",
                    "error": "Submission may have reached the endpoint before process interruption.",
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            return job
        if job.get("status") != "failed_retryable_no_job_created":
            return job
        if "submission_attempts" not in job:
            job["submission_attempts"] = [
                {
                    "attempt": 1,
                    "request_id": job.get("request_id"),
                    "started_at_utc": job.get("submission_started_at_utc"),
                    "finished_at_utc": job.get("updated_at_utc"),
                    "status": "legacy_confirmed_no_job_failure",
                    "http_status": job.get("submission_http_status"),
                    "error": job.get("error"),
                }
            ]
            atomic_write_json(path, job)
        if len(job.get("submission_attempts", [])) >= MAX_SAFE_SUBMIT_ATTEMPTS:
            job["status"] = "failed_terminal"
            job["failure_class"] = "safe_submit_retry_budget_exhausted"
            atomic_write_json(path, job)
            return job
    else:
        job = {
            **{field: row[field] for field in ROW_IDENTITY_FIELDS},
            "status": "new",
            "request_payload": payload,
            "provenance": prov,
            "submit_endpoint": GENERATE_URL,
            "submission_started_at_utc": utc_now(),
            "submission_attempts": [],
        }

    while len(job["submission_attempts"]) < MAX_SAFE_SUBMIT_ATTEMPTS:
        attempt_number = len(job["submission_attempts"]) + 1
        request_id = f"diversity-v3-{uuid.uuid4()}"
        attempt = {
            "attempt": attempt_number,
            "request_id": request_id,
            "started_at_utc": utc_now(),
            "status": "submitting",
        }
        job["submission_attempts"].append(attempt)
        job.update(
            {
                "status": "submitting",
                "request_id": request_id,
                "current_submission_attempt": attempt_number,
                "updated_at_utc": utc_now(),
            }
        )
        atomic_write_json(path, job)
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "x-foundry-model-id": MODEL_ID,
            "x-foundry-debug-data": "true",
            "x-request-id": request_id,
        }
        try:
            with httpx.Client(timeout=httpx.Timeout(180, connect=20)) as client:
                response = client.post(GENERATE_URL, json=payload, headers=headers)
        except (httpx.ReadTimeout, httpx.WriteTimeout) as exc:
            attempt.update(
                {"status": "ambiguous_timeout", "error": safe_error(exc), "finished_at_utc": utc_now()}
            )
            job.update(
                {
                    "status": "submission_ambiguous",
                    "failure_class": "submit_timeout_ambiguous_held_no_retry",
                    "error": safe_error(exc),
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            return job
        except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
            attempt.update(
                {
                    "status": "confirmed_no_job_connect_failure",
                    "error": safe_error(exc),
                    "finished_at_utc": utc_now(),
                }
            )
            job.update(
                {
                    "status": "failed_retryable_no_job_created",
                    "failure_class": "submit_connect_failure_confirmed_no_job",
                    "error": safe_error(exc),
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            if attempt_number < MAX_SAFE_SUBMIT_ATTEMPTS:
                time.sleep(5 * attempt_number)
                continue
            job["status"] = "failed_terminal"
            job["failure_class"] = "submit_connect_retry_budget_exhausted"
            atomic_write_json(path, job)
            return job

        try:
            body = response.json()
        except Exception:
            body = {"raw_text": response.text}
        clean_body = sanitize_endpoint_value(body)
        attempt.update(
            {
                "http_status": response.status_code,
                "response": clean_body,
                "response_headers": sanitize_endpoint_value(dict(response.headers)),
                "finished_at_utc": utc_now(),
            }
        )
        job["submission_http_status"] = response.status_code
        job["submission_response_headers"] = attempt["response_headers"]
        job["submission_response"] = clean_body
        result_href = ((body.get("links") or {}).get("result") or {}).get("href")
        response_job_id = body.get("job_id") or body.get("id") or ""

        if response.status_code == 429 or response.status_code >= 500:
            if result_href or response_job_id:
                attempt["status"] = "error_response_with_job_identity"
                job.update(
                    {
                        "status": "submission_ambiguous",
                        "failure_class": "error_response_with_job_identity_held_no_retry",
                        "job_id": response_job_id,
                        "result_url": result_href if result_href and result_href.startswith("http") else (BASE_URL + result_href if result_href else None),
                        "updated_at_utc": utc_now(),
                    }
                )
                atomic_write_json(path, job)
                return job
            attempt["status"] = f"confirmed_no_job_http_{response.status_code}"
            job.update(
                {
                    "status": "failed_retryable_no_job_created",
                    "failure_class": f"submit_http_{response.status_code}_confirmed_no_job",
                    "error": f"HTTP {response.status_code}",
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            if attempt_number < MAX_SAFE_SUBMIT_ATTEMPTS:
                time.sleep(5 * attempt_number)
                continue
            job["status"] = "failed_terminal"
            job["failure_class"] = f"submit_http_{response.status_code}_retry_budget_exhausted"
            atomic_write_json(path, job)
            return job

        if 400 <= response.status_code < 500:
            attempt["status"] = "fatal_http_4xx"
            job.update(
                {
                    "status": "failed_terminal",
                    "failure_class": f"submit_http_{response.status_code}_fatal_no_retry",
                    "error": f"HTTP {response.status_code}",
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            return job

        attempt["status"] = "response_received"
        task_status = response.headers.get("x-task-status", "")
        if response.status_code != 202 and response_is_final(body, task_status):
            job.update(
                {
                    "status": "endpoint_failed" if response_failed(body, task_status) else "completed_response_ready",
                    "task_status": task_status,
                    "final_response": clean_body,
                    "_transient_final_response": body,
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            return job

        if not result_href:
            job.update(
                {
                    "status": "submission_ambiguous",
                    "failure_class": "accepted_response_without_result_link_held_no_retry",
                    "updated_at_utc": utc_now(),
                }
            )
            atomic_write_json(path, job)
            return job
        job.update(
            {
                "status": "submitted",
                "job_id": response_job_id,
                "result_url": result_href if result_href.startswith("http") else BASE_URL + result_href,
                "submitted_at_utc": utc_now(),
                "poll_error_count": 0,
            }
        )
        atomic_write_json(path, job)
        return job
    raise AssertionError("safe submission retry loop exhausted without terminal state")


def poll_job(run_dir: Path, job: dict[str, Any], poll_window_seconds: int) -> dict[str, Any]:
    if job["status"] != "submitted":
        return job
    path = job_path(run_dir, job["row_id"])
    deadline = time.monotonic() + poll_window_seconds
    with httpx.Client(timeout=httpx.Timeout(120, connect=20)) as client:
        while time.monotonic() < deadline:
            time.sleep(POLL_INTERVAL_SECONDS)
            try:
                response = client.get(job["result_url"], headers={"accept": "application/json"})
                if response.status_code in {404, 410}:
                    job.update(
                        {
                            "status": "failed_terminal",
                            "failure_class": f"poll_http_{response.status_code}",
                            "error": response.text[:2000],
                            "updated_at_utc": utc_now(),
                        }
                    )
                    atomic_write_json(path, job)
                    return job
                response.raise_for_status()
                body = response.json()
                task_status = response.headers.get("x-task-status", "")
                job["last_poll_at_utc"] = utc_now()
                job["last_task_status"] = task_status
                if response_is_final(body, task_status):
                    job.update(
                        {
                            "status": "endpoint_failed" if response_failed(body, task_status) else "completed_response_ready",
                            "final_response": sanitize_endpoint_value(body),
                            "final_response_headers": sanitize_endpoint_value(dict(response.headers)),
                            "_transient_final_response": body,
                            "updated_at_utc": utc_now(),
                        }
                    )
                    atomic_write_json(
                        path,
                        {key: value for key, value in job.items() if not key.startswith("_transient_")},
                    )
                    return job
            except (httpx.HTTPError, ValueError) as exc:
                job["poll_error_count"] = job.get("poll_error_count", 0) + 1
                job["last_poll_error"] = safe_error(exc)
                job["last_poll_at_utc"] = utc_now()
            atomic_write_json(path, job)
    job["poll_window_exhausted_at_utc"] = utc_now()
    job["poll_window_count"] = job.get("poll_window_count", 0) + 1
    atomic_write_json(path, job)
    return job


def find_first_key(value: Any, keys: set[str]) -> Any:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in keys and child not in (None, ""):
                return child
        for child in value.values():
            found = find_first_key(child, keys)
            if found not in (None, ""):
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_first_key(child, keys)
            if found not in (None, ""):
                return found
    return None


def download_generated(url: str, destination_base: Path) -> tuple[Path, str]:
    with httpx.Client(timeout=httpx.Timeout(240, connect=20)) as client:
        with client.stream("GET", url, headers={"user-agent": "Mozilla/5.0"}) as response:
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
            suffix = {
                "image/jpeg": ".jpg",
                "image/webp": ".webp",
                "image/png": ".png",
            }.get(content_type, ".png")
            destination = destination_base.with_suffix(suffix)
            temporary = destination.with_name(f".{destination.name}.{os.getpid()}.download")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with temporary.open("wb") as handle:
                for block in response.iter_bytes(1024 * 1024):
                    handle.write(block)
            temporary.replace(destination)
    return destination, content_type


def total_latency_ms(job: dict[str, Any], completed_at_utc: str) -> float | None:
    try:
        started = dt.datetime.fromisoformat(job["submission_started_at_utc"])
        completed = dt.datetime.fromisoformat(completed_at_utc)
    except (KeyError, TypeError, ValueError):
        return None
    return round((completed - started).total_seconds() * 1000, 3)


def materialize_record(
    run_dir: Path,
    row: dict[str, Any],
    payload: dict[str, Any],
    prov: dict[str, Any],
    binding: dict[str, Any],
    job: dict[str, Any],
) -> dict[str, Any]:
    record_file = record_path(run_dir, row["row_id"])
    if record_file.exists():
        record = read_json(record_file)
        validate_existing_identity(record, row, payload, prov)
        if record.get("status") == "done":
            image = record["generated_image"]
            path = Path(image["path"])
            if not path.is_file() or path.stat().st_size != image["bytes"] or sha256_path(path) != image["sha256"]:
                raise ValueError(f"Completed output bytes changed: {row['row_id']}")
            if record.get("total_latency_ms") is None:
                durable_job = read_json(job_path(run_dir, row["row_id"]))
                record["total_latency_ms"] = total_latency_ms(
                    durable_job, record["completed_at_utc"]
                )
                atomic_write_json(record_file, record)
            return record
        # Pending/failure projections are rebuilt from the durable job journal.

    if job["status"] != "completed_response_ready":
        status = "pending" if job["status"] in {"submitted", "submitting"} else "failed"
        record = {
            **{field: row[field] for field in ROW_IDENTITY_FIELDS},
            "status": status,
            "job_status": job["status"],
            "failure_class": job.get("failure_class"),
            "error": job.get("error"),
            "request_payload": payload,
            "provenance": prov,
            "job_path": str(job_path(run_dir, row["row_id"]).resolve()),
            "updated_at_utc": utc_now(),
        }
        atomic_write_json(record_file, record)
        return record

    final_response = job.get("_transient_final_response")
    if final_response is None:
        result_url = job.get("result_url")
        if not result_url:
            raise ValueError(
                f"Completed response URL was sanitized and no result URL is available: {row['row_id']}"
            )
        with httpx.Client(timeout=httpx.Timeout(120, connect=20)) as client:
            refreshed = client.get(result_url, headers={"accept": "application/json"})
            refreshed.raise_for_status()
            final_response = refreshed.json()
    outputs = final_response.get("outputs") or []
    if not outputs:
        raise ValueError(f"Completed response has no outputs: {row['row_id']}")
    output = outputs[0]
    image_value = output.get("image") or {}
    url = image_value.get("presignedUrl")
    if not url:
        raise ValueError(f"Completed response has no output URL: {row['row_id']}")
    raw_path = run_dir / "raw_responses" / f"{artifact_stem(row['row_id'])}.json"
    sanitized_response = sanitize_endpoint_value(final_response)
    atomic_write_json(raw_path, sanitized_response)
    started = time.monotonic()
    image_path, content_type = download_generated(
        url, run_dir / "images" / artifact_stem(row["row_id"])
    )
    with Image.open(image_path) as generated:
        native_width, native_height = generated.size
        native_format = generated.format
    expected_size = (payload["size"]["width"], payload["size"]["height"])
    if (native_width, native_height) != expected_size:
        raise ValueError(
            f"Endpoint output dimensions differ for {row['row_id']}: "
            f"{native_width}x{native_height} != {expected_size[0]}x{expected_size[1]}"
        )
    debug_data = sanitize_endpoint_value(final_response.get("debugData") or {})
    used_prompt = find_first_key(
        final_response,
        {"usedprompt", "used_prompt", "rewrittenprompt", "rewritten_prompt"},
    )
    completed_at_utc = utc_now()
    record = {
        **{field: row[field] for field in ROW_IDENTITY_FIELDS},
        "status": "done",
        "current_render": row["render"],
        "source_message": row["source"],
        "case": row["case"],
        "selection": row["selection"],
        "selected_candidate": row["candidate"],
        "request_payload": payload,
        "provenance": prov,
        "reference_binding": binding,
        "job_id": job.get("job_id"),
        "request_id": job.get("request_id"),
        "job_path": str(job_path(run_dir, row["row_id"]).resolve()),
        "raw_response_path": str(raw_path.resolve()),
        "raw_response_sha256": sha256_path(raw_path),
        "returned_seed": output.get("seed"),
        "returned_dimensions_raw": {
            "width": image_value.get("width") or output.get("width") or debug_data.get("width"),
            "height": image_value.get("height") or output.get("height") or debug_data.get("height"),
            "source": "response_or_debugData",
        },
        "usedPrompt": used_prompt,
        "debugData": debug_data,
        "generated_image": {
            "path": str(image_path.resolve()),
            "filename": image_path.name,
            "sha256": sha256_path(image_path),
            "bytes": image_path.stat().st_size,
            "native_width": native_width,
            "native_height": native_height,
            "native_format": native_format,
            "content_type": content_type,
        },
        "download_latency_ms": round((time.monotonic() - started) * 1000, 3),
        "total_latency_ms": total_latency_ms(job, completed_at_utc),
        "completed_at_utc": completed_at_utc,
    }
    atomic_write_json(record_file, record)
    job["status"] = "materialized"
    job["record_path"] = str(record_file.resolve())
    job["updated_at_utc"] = utc_now()
    job.pop("_transient_final_response", None)
    job["final_response"] = sanitized_response
    atomic_write_json(job_path(run_dir, row["row_id"]), sanitize_endpoint_value(job))
    return record


def process_row(
    run_dir: Path,
    row: dict[str, Any],
    binding: dict[str, Any],
    manifest_sha256: str,
    accepted_sha256: str,
    selection_sha256: str,
    poll_window_seconds: int,
) -> dict[str, Any]:
    payload = build_payload(row, binding["blob_id"])
    prov = provenance(
        row, payload, binding, manifest_sha256, accepted_sha256, selection_sha256
    )
    existing_record = record_path(run_dir, row["row_id"])
    if existing_record.exists():
        record = read_json(existing_record)
        validate_existing_identity(record, row, payload, prov)
        if record.get("status") == "done":
            return materialize_record(run_dir, row, payload, prov, binding, {})
        # A pending record never authorizes a new submission; its job journal does.
    job = submit_job(run_dir, row, payload, prov)
    job = poll_job(run_dir, job, poll_window_seconds)
    return materialize_record(run_dir, row, payload, prov, binding, job)


def load_all_records(run_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted((run_dir / "records").glob("*.json")):
        records.append(read_json(path))
    return records


def write_progress(
    run_dir: Path,
    manifest: dict[str, Any],
    manifest_sha256: str,
    accepted: dict[str, Any],
    accepted_sha256: str,
    selection: dict[str, Any],
    selection_sha256: str,
    available_rows: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    records = load_all_records(run_dir)
    status_counts: dict[str, int] = {}
    for record in records:
        status_counts[record["status"]] = status_counts.get(record["status"], 0) + 1
    known = {record["row_id"] for record in records}
    selected_ids = {row["row_id"] for row in selected_rows}
    pending_jobs = []
    ambiguous_jobs = []
    safe_retry_jobs = []
    for path in sorted((run_dir / "jobs").glob("*.json")):
        job = read_json(path)
        if job.get("status") == "submitted":
            pending_jobs.append(job["row_id"])
        if job.get("status") == "submission_ambiguous":
            ambiguous_jobs.append(job["row_id"])
        if job.get("status") == "failed_retryable_no_job_created":
            safe_retry_jobs.append(job["row_id"])
    summary = {
        "schema_version": 1,
        "updated_at_utc": utc_now(),
        "endpoint": GENERATE_URL,
        "upload_endpoint": UPLOAD_URL,
        "manifest_path": str(MANIFEST_PATH.resolve()),
        "manifest_sha256": manifest_sha256,
        "accepted_prompt_cases_path": str(ACCEPTED_PATH.resolve()),
        "accepted_prompt_cases_sha256": accepted_sha256,
        "selection_manifest_path": str(SELECTION_PATH.resolve()),
        "selection_manifest_sha256": selection_sha256,
        "manifest_case_count": manifest["scope"]["case_count"],
        "candidate_inventory_count": accepted["counts"]["candidates"],
        "selected_candidate_count": selection["counts"]["selected"],
        "expected_generation_row_count": EXPECTED_SELECTION_COUNT,
        "available_generation_row_count": len(available_rows),
        "selected_generation_row_count": len(selected_rows),
        "record_count": len(records),
        "record_status_counts": dict(sorted(status_counts.items())),
        "selected_missing_record_count": len(selected_ids - known),
        "pending_job_count": len(pending_jobs),
        "pending_job_row_ids": pending_jobs,
        "ambiguous_submission_count": len(ambiguous_jobs),
        "ambiguous_submission_row_ids": ambiguous_jobs,
        "safe_retry_job_count": len(safe_retry_jobs),
        "safe_retry_job_row_ids": safe_retry_jobs,
        "settings": {
            "seed_request": [SEED],
            "n": N,
            "enablePromptRewrite": True,
            "rewriterModel": REWRITER_MODEL,
            "numInferenceSteps": NUM_INFERENCE_STEPS,
            "regular_output_width": 2560,
            "regular_output_height": 1440,
        },
    }
    atomic_write_json(run_dir / "summary.json", summary)
    lines = b"".join(
        (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for record in sorted(records, key=lambda item: item["row_id"])
    )
    atomic_write_bytes(run_dir / "results.jsonl", lines)
    return summary


def endpoint_preflight(run_dir: Path, manifest: dict[str, Any], manifest_sha256: str) -> dict[str, Any]:
    results: dict[str, Any] = {}
    with httpx.Client(timeout=httpx.Timeout(60, connect=20)) as client:
        openapi_response = client.get(OPENAPI_URL, headers={"accept": "application/json"})
        openapi_response.raise_for_status()
        openapi_raw = openapi_response.content
        openapi = openapi_response.json()
        metadata_response = client.get(
            METADATA_URL,
            headers={"accept": "application/json", "x-foundry-model-id": MODEL_ID},
        )
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
    image_schema = openapi["components"]["schemas"]["ImageRequest"]
    model_schema = openapi["components"]["schemas"]["ImageModelSpecificPayload"]
    checks = {
        "explicit_seed_supported": "seeds" in image_schema["properties"],
        "n_supported": "n" in image_schema["properties"],
        "reference_blob_supported": "referenceBlobs" in image_schema["properties"],
        "prompt_rewrite_supported": "enablePromptRewrite" in model_schema["properties"],
        "rewriter_model_supported": REWRITER_MODEL
        in model_schema["properties"]["rewriterModel"]["enum"],
        "inference_steps_supported": "numInferenceSteps" in model_schema["properties"],
        "png_upload_supported": "image/png"
        in openapi["paths"]["/v2/storage/image"]["post"]["requestBody"]["content"],
    }
    if not all(checks.values()):
        raise ValueError(f"Endpoint preflight checks failed: {checks}")
    output_sizes = {
        f"{normalized_render(render)['output_width']}x{normalized_render(render)['output_height']}"
        for render in manifest["renders"]
    }
    if output_sizes != {"2560x1440"}:
        raise ValueError(f"Unexpected current output-size set: {output_sizes}")
    results.update(
        {
            "schema_version": 1,
            "checked_at_utc": utc_now(),
            "base_url": BASE_URL,
            "openapi_url": OPENAPI_URL,
            "openapi_http_status": openapi_response.status_code,
            "openapi_sha256": sha256_bytes(openapi_raw),
            "metadata_url": METADATA_URL,
            "metadata_http_status": metadata_response.status_code,
            "metadata": metadata,
            "current_weights": metadata.get("provenance", {}).get("sources") or None,
            "manifest_sha256": manifest_sha256,
            "counts": manifest["scope"],
            "output_size_set": sorted(output_sizes),
            "request_checks": checks,
            "fixed_request_settings": {
                "seeds": [SEED],
                "n": N,
                "enablePromptRewrite": True,
                "rewriterModel": REWRITER_MODEL,
                "numInferenceSteps": NUM_INFERENCE_STEPS,
            },
        }
    )
    atomic_write_json(run_dir / "endpoint_preflight.json", results)
    return results


def select_rows(
    rows: list[dict[str, Any]], requested_ids: list[str], launch_all: bool,
) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in rows}
    if launch_all:
        return rows
    if not requested_ids:
        return []
    missing = sorted(set(requested_ids) - set(by_id))
    if missing:
        raise ValueError(f"Requested rows are not in the frozen V3 selection: {missing}")
    return [by_id[row_id] for row_id in requested_ids]


def require_launch_authorization(
    manifest: dict[str, Any], selection: dict[str, Any], rows: list[dict[str, Any]]
) -> None:
    if manifest.get("scope", {}).get("image_generation_authorized") is not True:
        raise ValueError("V3 manifest does not authorize image generation")
    if selection.get("status") != "approved_for_image_generation":
        raise ValueError("V3 selection manifest is not approved_for_image_generation")
    unapproved = [
        row["selection_key"]
        for row in rows
        if row["selection"].get("semantic_review_status") != "accepted"
    ]
    if unapproved:
        raise ValueError(
            f"V3 selections remain outside accepted semantic review: {unapproved[:5]}"
        )
    unapproved_banks = [
        row["case_id"]
        for row in rows
        if row["accepted_case"].get("status") != "normalized_validator_passed"
        or row["accepted_case"].get("human_review_status") != "accepted"
        or row["accepted_case"].get("launchable") is not True
    ]
    if unapproved_banks:
        raise ValueError(
            "V3 accepted banks remain outside launch approval: "
            f"{sorted(set(unapproved_banks))[:5]}"
        )
    if len(rows) != EXPECTED_SELECTION_COUNT:
        raise ValueError("Authorized V3 launch must contain exactly 108 rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--list-smoke-candidates", action="store_true")
    parser.add_argument("--row-id", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--upload-workers", type=int, default=2)
    parser.add_argument("--poll-window-seconds", type=int, default=DEFAULT_POLL_WINDOW_SECONDS)
    args = parser.parse_args()
    if args.workers < 1 or args.workers > MAX_WORKERS:
        parser.error(f"--workers must be between 1 and {MAX_WORKERS}")
    if args.upload_workers < 1 or args.upload_workers > MAX_WORKERS:
        parser.error(f"--upload-workers must be between 1 and {MAX_WORKERS}")
    if sum((bool(args.all), bool(args.row_id))) > 1:
        parser.error("Use exactly one of --all or --row-id")

    args.run_dir = args.run_dir.resolve()
    for subdir in ("jobs", "records", "raw_responses", "images", "invocations"):
        (args.run_dir / subdir).mkdir(parents=True, exist_ok=True)
    (
        manifest,
        manifest_sha256,
        accepted,
        accepted_sha256,
        selection,
        selection_sha256,
    ) = load_inputs()
    for render in manifest["renders"]:
        validate_render(normalized_render(render))
    rows = build_rows(manifest, accepted, selection)

    if args.validate_only:
        print(
            json.dumps(
                {
                    "manifest_sha256": manifest_sha256,
                    "accepted_prompt_cases_sha256": accepted_sha256,
                    "selection_manifest_sha256": selection_sha256,
                    "validated_generation_row_count": len(rows),
                    "endpoint_called": False,
                },
                indent=2,
            )
        )
        return

    preflight = endpoint_preflight(args.run_dir, manifest, manifest_sha256)

    if args.list_smoke_candidates:
        candidates = [
            row["row_id"]
            for row in rows
            if row["selection"]["selection_stratum"] == "upper_rank_1_10"
        ]
        print(json.dumps({"candidate_count": len(candidates), "row_ids": candidates}, indent=2))
        return
    if args.preflight_only:
        summary = write_progress(
            args.run_dir, manifest, manifest_sha256, accepted, accepted_sha256,
            selection, selection_sha256, rows, []
        )
        print(json.dumps({"preflight": preflight, "summary": summary}, indent=2))
        return
    selected = select_rows(rows, args.row_id, args.all)
    if not selected:
        parser.error("No generation rows selected; use --row-id or --all")
    require_launch_authorization(manifest, selection, rows)

    invocation = {
        "started_at_utc": utc_now(),
        "manifest_sha256": manifest_sha256,
        "accepted_prompt_cases_sha256": accepted_sha256,
        "selection_manifest_sha256": selection_sha256,
        "selected_row_ids": [row["row_id"] for row in selected],
        "workers": args.workers,
        "upload_workers": args.upload_workers,
        "poll_window_seconds": args.poll_window_seconds,
    }
    invocation_name = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    atomic_write_json(args.run_dir / "invocations" / f"{invocation_name}.json", invocation)
    bindings = ensure_bindings(args.run_dir, selected, manifest_sha256, args.upload_workers)
    log(f"generation rows selected={len(selected)} workers={args.workers}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                process_row,
                args.run_dir,
                row,
                bindings[row["render_id"]],
                manifest_sha256,
                accepted_sha256,
                selection_sha256,
                args.poll_window_seconds,
            ): row
            for row in selected
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
                log(f"{record['status']} {row['row_id']}")
            except Exception as exc:
                log(f"ERROR {row['row_id']}: {safe_error(exc)}")
            write_progress(
                args.run_dir,
                manifest,
                manifest_sha256,
                accepted,
                accepted_sha256,
                selection,
                selection_sha256,
                rows,
                selected,
            )
    summary = write_progress(
        args.run_dir,
        manifest,
        manifest_sha256,
        accepted,
        accepted_sha256,
        selection,
        selection_sha256,
        rows,
        selected,
    )
    print(json.dumps(summary, indent=2))
    if summary["selected_missing_record_count"] or summary["pending_job_count"] or summary["ambiguous_submission_count"] or summary["record_status_counts"].get("failed", 0):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
