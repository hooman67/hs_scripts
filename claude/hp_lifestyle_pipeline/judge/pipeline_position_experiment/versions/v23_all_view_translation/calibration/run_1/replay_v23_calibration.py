#!/usr/bin/env python3
"""Read-only V23 replay and synthetic calibration.

The Foundry checkout is imported but never modified. Existing evidence trees are
read only. V23 first-attempt semantics use ``fixed_position=False`` for every
camera/view. The distinct Stage-B recovery mode uses ``fixed_position=True``.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time

import cv2
import numpy as np


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
ROOT = PROJECT / "judge/pipeline_position_experiment"
OUT = ROOT / "versions/v23_all_view_translation/calibration"
PACKAGE = Path("/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25")
INVARIANTS_PATH = PACKAGE / "hp3p/invariants.py"
FROZEN_CALIBRATION = ROOT / "versions/v22_4/textureless_guard_calibration_v3.json"
sys.path.insert(0, str(PACKAGE))

from hp3p.invariants import (  # noqa: E402
    GUARD_VERSION,
    TEXTURELESS_THRESHOLDS,
    THRESHOLDS,
    _assess_translation_textureless,
    assess_product_affine,
)


def load(path: Path):
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def combined_sha256(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=str):
        digest.update(str(path).encode())
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


def gray(path: Path) -> np.ndarray:
    value = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if value is None:
        raise RuntimeError(f"cannot read {path}")
    return value


def alpha(path: Path) -> np.ndarray:
    value = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if value is None or value.ndim != 3 or value.shape[2] != 4:
        raise RuntimeError(f"not RGBA: {path}")
    return value[:, :, 3] > 127


def png_bytes(image: np.ndarray) -> bytes:
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("could not encode synthetic PNG")
    return encoded.tobytes()


def rgba_bytes(mask: np.ndarray) -> bytes:
    image = np.zeros((*mask.shape, 4), np.uint8)
    image[:, :, 3] = mask.astype(np.uint8) * 255
    return png_bytes(image)


def affine_composite(guide: np.ndarray, mask: np.ndarray, matrix: np.ndarray,
                     *, solid: int | None = None) -> np.ndarray:
    height, width = guide.shape
    source = np.full_like(guide, solid) if solid is not None else guide
    product = cv2.warpAffine(source, matrix, (width, height), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=210)
    moved_mask = cv2.warpAffine(mask.astype(np.uint8), matrix, (width, height),
                                flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT,
                                borderValue=0) > 0
    output = np.full_like(guide, 210)
    output[moved_mask] = product[moved_mask]
    return output


def perspective_composite(guide: np.ndarray, mask: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    height, width = guide.shape
    product = cv2.warpPerspective(guide, matrix, (width, height), flags=cv2.INTER_LINEAR,
                                  borderMode=cv2.BORDER_CONSTANT, borderValue=210)
    moved_mask = cv2.warpPerspective(mask.astype(np.uint8), matrix, (width, height),
                                     flags=cv2.INTER_NEAREST,
                                     borderMode=cv2.BORDER_CONSTANT, borderValue=0) > 0
    output = np.full_like(guide, 210)
    output[moved_mask] = product[moved_mask]
    return output


def fixture_sources(calibration: dict) -> dict[str, tuple[Path, Path]]:
    values = {}
    for frozen in calibration["real"]:
        if not frozen["fixed_position"]:
            continue
        row = Path(frozen["path"]).parent
        key = row.name.split("__retained_control")[0].split("__relocation_demand")[0]
        values.setdefault(key, (row / "geometry_guide.png", row / "mask.png"))
    return dict(sorted(values.items()))


def v23_real_expected(record: dict) -> str:
    """Relabel only failures caused solely by the superseded position lock."""
    if record["label"] != "fail":
        return record["label"]
    reasons = set(record.get("affine_reasons", []))
    position_only = bool(reasons) and reasons <= {"fixed_translation_x", "fixed_translation_y"}
    return "pass" if position_only else "fail"


def summarize_result(result: dict) -> dict:
    fallback = result.get("textureless_fallback")
    return {
        "verdict": result["verdict"],
        "reasons": result.get("reasons", []),
        "method": fallback.get("method") if fallback else "affine",
        "translation_x_px": result.get("translation_x_px"),
        "translation_y_px": result.get("translation_y_px"),
        "primary_verdict": result.get("primary_verdict"),
        "primary_reasons": result.get("primary_reasons"),
        "fallback_dispatch_reason": result.get("fallback_dispatch_reason"),
        "textureless_fallback": fallback,
    }


def replay_real(calibration: dict) -> list[dict]:
    rows = []
    for frozen in calibration["real"]:
        audit_path = Path(frozen["path"])
        row = audit_path.parent
        attempt = frozen["attempt"]
        audit = load(audit_path)
        args = ((row / "geometry_guide.png").read_bytes(),
                (row / f"gpt_{attempt}.png").read_bytes(), audit["product_bounds_px"])
        kwargs = {"product_mask": (row / "mask.png").read_bytes()}
        started = time.perf_counter()
        all_view = assess_product_affine(*args, fixed_position=False, **kwargs)
        all_view_ms = (time.perf_counter() - started) * 1000
        started = time.perf_counter()
        recovery = assess_product_affine(*args, fixed_position=True, **kwargs)
        recovery_ms = (time.perf_counter() - started) * 1000
        rows.append({
            "path": str(audit_path),
            "attempt": attempt,
            "frozen_label": frozen["label"],
            "frozen_fixed_position": frozen["fixed_position"],
            "frozen_reasons": frozen.get("affine_reasons", []),
            "v23_all_view_expected": v23_real_expected(frozen),
            "v23_all_view": summarize_result(all_view),
            "v23_fixed_recovery": summarize_result(recovery),
            "all_view_runtime_ms": all_view_ms,
            "fixed_recovery_runtime_ms": recovery_ms,
        })
    return rows


def frozen_synthetic_expected(record: dict, fixed_position: bool) -> str:
    if fixed_position:
        return record["label"]
    if record["transform"] in {"identity", "allowed_translation_8px",
                                "excess_translation_12px", "brightness_shift"}:
        return "pass"
    return "fail"


def replay_frozen_synthetic(calibration: dict, fixtures: dict) -> list[dict]:
    rows = []
    for frozen in calibration["synthetic"]:
        guide_path, mask_path = fixtures[frozen["fixture"]]
        guide, mask = gray(guide_path), alpha(mask_path)
        matrix = np.asarray(frozen["matrix"], np.float32)
        if frozen["transform"] == "brightness_shift":
            source = np.clip(guide.astype(np.float32) * 0.72 + 24, 0, 255).astype(np.uint8)
            output = affine_composite(source, mask, matrix)
        else:
            output = affine_composite(
                guide, mask, matrix,
                solid=28 if frozen["transform"] == "solid_dark_product" else None,
            )
        mode_results = {}
        for mode, fixed in (("all_view", False), ("fixed_recovery", True)):
            started = time.perf_counter()
            result = _assess_translation_textureless(guide, output, mask,
                                                     fixed_position=fixed)
            mode_results[mode] = {
                "expected": frozen_synthetic_expected(frozen, fixed),
                "runtime_ms": (time.perf_counter() - started) * 1000,
                "result": result,
            }
        rows.append({
            "fixture": frozen["fixture"],
            "transform": frozen["transform"],
            "frozen_label": frozen["label"],
            **mode_results,
        })
    return rows


def alpha_bounds(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def full_size_cases(fixture: str, guide: np.ndarray, mask: np.ndarray) -> list[dict]:
    height, width = guide.shape
    x0, y0, x1, y1 = alpha_bounds(mask)
    center = ((x0 + x1 - 1) / 2, (y0 + y1 - 1) / 2)
    legal = {"x_min": -x0, "x_max": width - x1,
             "y_min": -y0, "y_max": height - y1}
    candidates = []

    def affine_case(name: str, expected: str, matrix, *, fixed=False, solid=None,
                    tags=()):
        candidates.append({"name": name, "expected": expected, "fixed_position": fixed,
                           "output": affine_composite(guide, mask, np.asarray(matrix, np.float32),
                                                      solid=solid),
                           "tags": list(tags), "transform": np.asarray(matrix).tolist()})

    identity = np.float32([[1, 0, 0], [0, 1, 0]])
    dx_large = max(-x0, min(width - x1, 120 if width - x1 >= 120 else -120))
    dy_large = max(-y0, min(height - y1, 80 if height - y1 >= 80 else -80))
    # If an axis cannot move in the preferred direction, use half of its largest legal motion.
    if abs(dx_large) <= 8:
        dx_large = legal["x_min"] // 2 if abs(legal["x_min"]) > 8 else legal["x_max"] // 2
    if abs(dy_large) <= 8:
        dy_large = legal["y_min"] // 2 if abs(legal["y_min"]) > 8 else legal["y_max"] // 2
    move = np.float32([[1, 0, dx_large], [0, 1, dy_large]])
    fill = float(mask.mean())
    bbox_width_fraction = (x1 - x0) / width
    bbox_height_fraction = (y1 - y0) / height
    high_fill = bbox_width_fraction >= 0.45 or bbox_height_fraction >= 0.45
    tags = ["full_resolution", "large_translation"]
    if high_fill:
        tags.append("high_fill_close")
    affine_case("identity", "pass", identity, tags=["full_resolution"])
    affine_case("large_legal_translation", "pass", move, tags=tags)
    affine_case("legal_top_left_extreme", "pass",
                [[1, 0, legal["x_min"]], [0, 1, legal["y_min"]]],
                tags=["full_resolution", "legal_frame_extreme"])
    affine_case("legal_bottom_right_extreme", "pass",
                [[1, 0, legal["x_max"]], [0, 1, legal["y_max"]]],
                tags=["full_resolution", "legal_frame_extreme"])
    affine_case("one_pixel_crop_left", "fail",
                [[1, 0, legal["x_min"] - 1], [0, 1, legal["y_min"]]],
                tags=["full_resolution", "one_pixel_crop"])
    affine_case("one_pixel_crop_right", "fail",
                [[1, 0, legal["x_max"] + 1], [0, 1, legal["y_max"]]],
                tags=["full_resolution", "one_pixel_crop"])

    rotation = cv2.getRotationMatrix2D(center, 2.0, 1.0)
    rotation[:, 2] += (dx_large, dy_large)
    affine_case("rotation_2deg_after_move", "fail", rotation,
                tags=["full_resolution", "rotation", "large_translation"])
    for scale in (0.96, 1.04):
        matrix = cv2.getRotationMatrix2D(center, 0, scale)
        matrix[:, 2] += (dx_large, dy_large)
        affine_case(f"scale_{scale:.2f}_after_move", "fail", matrix,
                    tags=["full_resolution", "scale", "large_translation"])
    anisotropic = np.float32([
        [0.96, 0, center[0] * (1 - 0.96) + dx_large],
        [0, 1.04, center[1] * (1 - 1.04) + dy_large],
    ])
    affine_case("anisotropy_after_move", "fail", anisotropic,
                tags=["full_resolution", "anisotropy", "large_translation"])
    shear = np.float32([[1, 0.06, dx_large - 0.06 * center[1]], [0, 1, dy_large]])
    affine_case("shear_after_move", "fail", shear,
                tags=["full_resolution", "shear", "large_translation"])
    perspective = np.float32([
        [1, 0, dx_large], [0, 1, dy_large], [0.0002, -0.00012, 1],
    ])
    candidates.append({
        "name": "perspective_warp_after_move", "expected": "fail", "fixed_position": False,
        "output": perspective_composite(guide, mask, perspective),
        "tags": ["full_resolution", "perspective", "large_translation"],
        "transform": perspective.tolist(),
    })
    affine_case("solid_dark_substitute", "fail", move, solid=28,
                tags=["full_resolution", "dark_distractor"])
    # A spatially separate dark patch must not displace an otherwise valid registration.
    valid = affine_composite(guide, mask, move)
    patch_w, patch_h = max(20, (x1 - x0) // 8), max(20, (y1 - y0) // 8)
    valid[5:5 + min(patch_h, height // 5), 5:5 + min(patch_w, width // 5)] = 28
    candidates.append({
        "name": "valid_product_with_dark_distractor", "expected": "pass",
        "fixed_position": False, "output": valid,
        "tags": ["full_resolution", "dark_distractor", "large_translation"],
        "transform": move.tolist(),
    })
    # Fixed recovery is separately bounded: exactly eight pixels passes; nine fails.
    affine_case("fixed_recovery_translation_8px", "pass", [[1, 0, 8], [0, 1, -8]],
                fixed=True, tags=["full_resolution", "fixed_recovery"])
    affine_case("fixed_recovery_translation_9px", "fail", [[1, 0, 9], [0, 1, 0]],
                fixed=True, tags=["full_resolution", "fixed_recovery"])
    for case in candidates:
        case.update({"fixture": fixture, "shape": [height, width],
                     "alpha_fill_fraction": fill,
                     "bbox_width_fraction": bbox_width_fraction,
                     "bbox_height_fraction": bbox_height_fraction,
                     "density_class": ("HIGH-FILL/CLOSE" if high_fill
                                       else "LOWER-FILL/MEDIUM-WIDE"),
                     "legal_translation": legal})
    return candidates


def compact_duplicate_case() -> dict:
    source = np.full((600, 800), 210, np.uint8)
    mask = np.zeros_like(source, np.uint8)
    polygon = np.asarray([[240, 190], [560, 190], [540, 390], [260, 390]], np.int32)
    cv2.fillConvexPoly(mask, polygon, 1)
    source[mask > 0] = 38
    cv2.rectangle(source, (375, 265), (425, 315), 75, 4)
    cv2.line(source, (280, 355), (520, 355), 82, 3)
    first = affine_composite(source, mask > 0, np.float32([[1, 0, -160], [0, 1, -120]]))
    second = affine_composite(source, mask > 0, np.float32([[1, 0, 170], [0, 1, 130]]))
    output = np.where(second != 210, second, first)
    started = time.perf_counter()
    result = _assess_translation_textureless(source, output, mask > 0, fixed_position=False)
    return {"fixture": "compact_duplicate_fixture", "name": "duplicate_ambiguity",
            "shape": [600, 800], "expected": "unverifiable",
            "runtime_ms": (time.perf_counter() - started) * 1000,
            "tags": ["duplicate", "ambiguity"], "result": result}


def run_added_synthetic(fixtures: dict) -> list[dict]:
    rows = []
    deterministic_probe = None
    for fixture, (guide_path, mask_path) in fixtures.items():
        guide, mask = gray(guide_path), alpha(mask_path)
        for case in full_size_cases(fixture, guide, mask):
            started = time.perf_counter()
            result = _assess_translation_textureless(
                guide, case.pop("output"), mask, fixed_position=case["fixed_position"],
            )
            case["runtime_ms"] = (time.perf_counter() - started) * 1000
            case["result"] = result
            rows.append(case)
            if deterministic_probe is None and case["name"] == "large_legal_translation":
                deterministic_probe = (fixture, guide, mask, case["transform"], result)
    rows.append(compact_duplicate_case())
    if deterministic_probe is not None:
        fixture, guide, mask, matrix, first = deterministic_probe
        output = affine_composite(guide, mask, np.asarray(matrix, np.float32))
        started = time.perf_counter()
        second = _assess_translation_textureless(guide, output, mask, fixed_position=False)
        rows.append({
            "fixture": fixture, "name": "deterministic_repeat", "shape": list(guide.shape),
            "expected": "pass", "runtime_ms": (time.perf_counter() - started) * 1000,
            "tags": ["full_resolution", "determinism"], "result": second,
            "byte_equal_json": json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True),
            "first_result_sha256": hashlib.sha256(
                json.dumps(first, sort_keys=True).encode()).hexdigest(),
            "second_result_sha256": hashlib.sha256(
                json.dumps(second, sort_keys=True).encode()).hexdigest(),
        })
    return rows


def compatible_artifact_rows() -> list[Path]:
    roots = [ROOT / "smoke"] + sorted(ROOT.glob("full160*"))
    seen = set()
    rows = []
    for search_root in roots:
        if not search_root.is_dir():
            continue
        for result_path in sorted(search_root.rglob("result.json")):
            row = result_path.parent
            if "/run/jobs/" in str(result_path):
                continue
            required = [row / "geometry_guide.png", row / "mask.png"]
            images = sorted(row.glob("gpt_*.png"))
            if not all(path.is_file() for path in required) or not images:
                continue
            identity = tuple(path.resolve() for path in required + images)
            if identity in seen:
                continue
            seen.add(identity)
            rows.append(row)
    return rows


def replay_artifact_row(row: Path) -> dict | None:
    saved = load(row / "result.json")
    bounds = saved.get("guide_info", {}).get("product_bounds_px")
    if bounds is None:
        return None
    attempts = []
    for image in sorted(row.glob("gpt_*.png")):
        attempt = int(image.stem.split("_")[-1])
        args = ((row / "geometry_guide.png").read_bytes(), image.read_bytes(), bounds)
        mask_bytes = (row / "mask.png").read_bytes()
        all_view = assess_product_affine(*args, fixed_position=False, product_mask=mask_bytes)
        fixed = assess_product_affine(*args, fixed_position=True, product_mask=mask_bytes)
        attempts.append({"attempt": attempt, "all_view": summarize_result(all_view),
                         "fixed_recovery": summarize_result(fixed)})
    old_guard = saved.get("product_invariant_guard", {})
    old_selection_observable = (isinstance(old_guard, dict)
                                and "selected_attempt" in old_guard)
    old_selected = old_guard.get("selected_attempt") if old_selection_observable else None
    first = next((item for item in attempts if item["attempt"] == 1), None)
    v23_selected = 1 if first and first["all_view"]["verdict"] == "pass" else next(
        (item["attempt"] for item in attempts
         if item["attempt"] > 1 and item["fixed_recovery"]["verdict"] == "pass"), None)
    all_view_selected = next(
        (item["attempt"] for item in attempts if item["all_view"]["verdict"] == "pass"), None)
    evidence = [row / "result.json", row / "geometry_guide.png", row / "mask.png",
                *sorted(row.glob("gpt_*.png"))]
    return {
        "row": str(row), "pipeline_version": saved.get("pipeline_version"),
        "old_density": saved.get("guide_density_class"),
        "old_selection_observable": old_selection_observable,
        "old_selected_attempt": old_selected,
        "v23_policy_selected_attempt": v23_selected,
        "all_view_counterfactual_selected_attempt": all_view_selected,
        "selection_changed": old_selection_observable and old_selected != v23_selected,
        "input_sha256": combined_sha256(evidence), "attempts": attempts,
    }


def classify(expected: str, actual: str) -> tuple[int, int]:
    return (int(expected == "fail" and actual == "pass"),
            int(expected == "pass" and actual != "pass"))


def runtime_summary(values: list[float]) -> dict:
    ordered = sorted(values)
    if not ordered:
        return {"count": 0}
    def percentile(q):
        index = (len(ordered) - 1) * q
        lo, hi = math.floor(index), math.ceil(index)
        return ordered[lo] if lo == hi else ordered[lo] + (ordered[hi] - ordered[lo]) * (index - lo)
    return {"count": len(ordered), "min_ms": ordered[0],
            "median_ms": statistics.median(ordered), "p95_ms": percentile(0.95),
            "max_ms": ordered[-1], "total_ms": sum(ordered)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    calibration = load(FROZEN_CALIBRATION)
    fixtures = fixture_sources(calibration)
    source_hash_before = sha256(INVARIANTS_PATH)
    prior_result = None
    prior_result_path = OUT / "replay_results.json"
    if prior_result_path.is_file():
        candidate = load(prior_result_path)
        if candidate.get("guard_source_sha256") == source_hash_before:
            prior_result = candidate

    def phase(name: str, compute, prior_key: str):
        checkpoint = OUT / f"checkpoint_{name}.json"
        if checkpoint.is_file():
            payload = load(checkpoint)
            if payload.get("guard_source_sha256") == source_hash_before:
                print(f"checkpoint reuse: {name}", flush=True)
                return payload["data"]
        if prior_result is not None and prior_key in prior_result:
            data = prior_result[prior_key]
            print(f"final-result checkpoint reuse: {name}", flush=True)
        else:
            print(f"phase start: {name}", flush=True)
            data = compute()
            print(f"phase complete: {name}", flush=True)
        checkpoint.write_text(json.dumps({"guard_source_sha256": source_hash_before,
                                          "data": data}, indent=2) + "\n")
        return data

    real = phase("real", lambda: replay_real(calibration), "real")
    frozen_synthetic = phase(
        "frozen_synthetic", lambda: replay_frozen_synthetic(calibration, fixtures),
        "frozen_synthetic")
    added_synthetic = phase(
        "added_synthetic", lambda: run_added_synthetic(fixtures), "added_synthetic")

    def compute_prior():
        replayed, incompatible = [], []
        rows = compatible_artifact_rows()
        for index, row in enumerate(rows, 1):
            try:
                item = replay_artifact_row(row)
                if item is None:
                    incompatible.append({"row": str(row), "reason": "missing_bounds"})
                else:
                    replayed.append(item)
            except Exception as exc:  # preserve every incompatibility explicitly
                incompatible.append({"row": str(row),
                                     "reason": f"{type(exc).__name__}: {exc}"})
            if index % 10 == 0:
                print(f"phase prior_artifacts: {index}/{len(rows)}", flush=True)
        return {"rows": replayed, "skipped": incompatible}

    prior_payload = phase("prior_artifacts", compute_prior, "prior_artifacts")
    prior, skipped = prior_payload["rows"], prior_payload["skipped"]
    # Enrich results from the initial pre-checkpoint run without recomputing images.
    for item in prior:
        if "old_selection_observable" not in item:
            saved = load(Path(item["row"]) / "result.json")
            guard = saved.get("product_invariant_guard")
            item["old_selection_observable"] = (isinstance(guard, dict)
                                                 and "selected_attempt" in guard)
            item["selection_changed"] = (
                item["old_selection_observable"]
                and item["old_selected_attempt"] != item["v23_policy_selected_attempt"])
    for item in added_synthetic:
        if item.get("shape") == [1776, 2368] and "density_class" not in item:
            name = item["fixture"]
            guide_path, mask_path = fixtures[name]
            mask = alpha(mask_path)
            x0, y0, x1, y1 = alpha_bounds(mask)
            height, width = mask.shape
            wf, hf = (x1 - x0) / width, (y1 - y0) / height
            item["bbox_width_fraction"], item["bbox_height_fraction"] = wf, hf
            item["density_class"] = ("HIGH-FILL/CLOSE" if wf >= 0.45 or hf >= 0.45
                                     else "LOWER-FILL/MEDIUM-WIDE")
            if item["name"] == "large_legal_translation" and item["density_class"] == "HIGH-FILL/CLOSE":
                item.setdefault("tags", []).append("high_fill_close")
    source_hash_after = sha256(INVARIANTS_PATH)
    if source_hash_after != source_hash_before:
        raise RuntimeError("Foundry invariants.py changed during replay; discard and rerun")

    real_labeled = [item for item in real if item["v23_all_view_expected"] in {"pass", "fail"}]
    real_errors = [classify(item["v23_all_view_expected"], item["v23_all_view"]["verdict"])
                   for item in real_labeled]
    frozen_modes = [(mode, item[mode]) for item in frozen_synthetic
                    for mode in ("all_view", "fixed_recovery")]
    frozen_errors = [classify(payload["expected"], payload["result"]["verdict"])
                     for _, payload in frozen_modes]
    added_errors = [classify(item["expected"], item["result"]["verdict"])
                    for item in added_synthetic]
    full_runtime = [item["runtime_ms"] for item in added_synthetic
                    if item["shape"] == [1776, 2368]]
    result = {
        "version": "v23-all-view-translation-read-only-calibration-v1",
        "as_of": "2026-11-06",
        "guard_version": GUARD_VERSION,
        "guard_source": str(INVARIANTS_PATH),
        "guard_source_sha256": source_hash_before,
        "frozen_calibration": str(FROZEN_CALIBRATION),
        "frozen_calibration_sha256": sha256(FROZEN_CALIBRATION),
        "thresholds": THRESHOLDS,
        "textureless_thresholds": TEXTURELESS_THRESHOLDS,
        "semantics": {
            "first_attempt": "fixed_position=False for every product, camera, and fill class",
            "recovery": "subsequent Stage-B attempt fixed_position=True",
            "real_relabel": "Only old failures caused solely by fixed_translation_x/y become V23 passes",
        },
        "summary": {
            "real_attempts": len(real),
            "real_labeled_attempts": len(real_labeled),
            "real_historical_proxy_false_accepts": sum(x for x, _ in real_errors),
            "real_historical_proxy_false_rejects": sum(y for _, y in real_errors),
            "real_label_limitation": (
                "Historical guard verdicts are regression proxies, not independent human truth"
            ),
            "frozen_synthetic_mode_checks": len(frozen_modes),
            "frozen_synthetic_false_accepts": sum(x for x, _ in frozen_errors),
            "frozen_synthetic_false_rejects": sum(y for _, y in frozen_errors),
            "added_synthetic_checks": len(added_synthetic),
            "added_synthetic_false_accepts": sum(x for x, _ in added_errors),
            "added_synthetic_false_rejects": sum(y for _, y in added_errors),
            "full_resolution_added_checks": sum(
                item["shape"] == [1776, 2368] for item in added_synthetic),
            "high_fill_legal_motion_checks": sum(
                "high_fill_close" in item.get("tags", []) for item in added_synthetic),
            "deterministic_repeat_equal": all(
                item.get("byte_equal_json", True) for item in added_synthetic),
            "prior_rows": len(prior),
            "prior_rows_with_observable_old_selection": sum(
                item["old_selection_observable"] for item in prior),
            "prior_selection_changes": sum(item["selection_changed"] for item in prior),
            "prior_incomparable_without_old_selection": sum(
                not item["old_selection_observable"] for item in prior),
            "prior_skipped": len(skipped),
            "full_resolution_runtime": runtime_summary(full_runtime),
        },
        "real": real,
        "frozen_synthetic": frozen_synthetic,
        "added_synthetic": added_synthetic,
        "prior_artifacts": {"rows": prior, "skipped": skipped},
    }
    (OUT / "replay_results.json").write_text(json.dumps(result, indent=2) + "\n")
    manifest = {
        "guard_source": {"path": str(INVARIANTS_PATH), "sha256": source_hash_before},
        "frozen_calibration": {"path": str(FROZEN_CALIBRATION),
                               "sha256": sha256(FROZEN_CALIBRATION)},
        "fixtures": {
            name: {str(path): sha256(path) for path in paths}
            for name, paths in fixtures.items()
        },
        "prior_rows": {item["row"]: item["input_sha256"] for item in prior},
    }
    (OUT / "input_evidence_sha256.json").write_text(json.dumps(manifest, indent=2) + "\n")
    summary = result["summary"] | {
        "guard_version": GUARD_VERSION,
        "guard_source_sha256": source_hash_before,
        "changed_prior_selections": [
            {"row": item["row"], "old": item["old_selected_attempt"],
             "v23": item["v23_policy_selected_attempt"]}
            for item in prior if item["selection_changed"]
        ],
        "skipped": skipped,
    }
    print(json.dumps(summary, indent=2))
    # Frozen-real labels are historical guard verdicts rather than independent
    # visual truth, and the frozen brightness-shift positives intentionally
    # expose stricter V23 appearance behavior. Report those disagreements; do
    # not hide them by weakening thresholds or relabeling old evidence.
    assert not result["summary"]["added_synthetic_false_accepts"]
    assert not result["summary"]["added_synthetic_false_rejects"]
    assert result["summary"]["deterministic_repeat_equal"]


if __name__ == "__main__":
    main()
