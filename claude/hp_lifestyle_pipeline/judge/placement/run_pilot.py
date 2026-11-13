# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Bounded pilot. Attribution, split names and annotations never enter the model call."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

try:
    from .run_judge import _load_visual_anchors, judge, sha256
except ImportError:  # Direct script execution.
    from run_judge import _load_visual_anchors, judge, sha256  # type: ignore


ROOT = Path(__file__).resolve().parent


def _validate_run_name(run: str) -> None:
    if not run or Path(run).name != run or run in {".", ".."}:
        raise ValueError("--run must be one directory name")


def _select_cases(
    split: Mapping[str, Any],
    split_name: str,
    rows: Sequence[int] | None,
    limit: int | None,
) -> list[Mapping[str, Any]]:
    cases = split.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Split manifest has no cases array")
    split_cases = [
        case
        for case in cases
        if isinstance(case, dict) and case.get("split") == split_name
    ]
    if not split_cases:
        raise ValueError(f"Split contains no cases: {split_name}")
    if limit is not None and limit <= 0:
        raise ValueError("--limit must be positive")
    if rows:
        if len(set(rows)) != len(rows):
            raise ValueError("--rows must not contain duplicates")
        available_rows = {case.get("row") for case in split_cases}
        unknown_rows = sorted(set(rows) - available_rows)
        if unknown_rows:
            raise ValueError(
                f"Requested rows are not in {split_name}: {unknown_rows}"
            )
        split_cases = [case for case in split_cases if case.get("row") in rows]
    selected = split_cases[:limit]
    if not selected:
        raise ValueError("Pilot selection is empty")
    return selected


def _asset_index(assets: Any) -> tuple[Dict[str, Mapping[str, Any]], list[Mapping[str, Any]]]:
    if not isinstance(assets, list):
        raise ValueError("Asset manifest has no assets array")
    by_id: Dict[str, Mapping[str, Any]] = {}
    normalized = []
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get("id"), str):
            raise ValueError("Asset manifest contains an invalid asset")
        if asset["id"] in by_id:
            raise ValueError(f"Duplicate asset id: {asset['id']}")
        by_id[asset["id"]] = asset
        normalized.append(asset)
    return by_id, normalized


def _anchor_demonstration_rows(
    anchors: Mapping[str, Any], split: Mapping[str, Any]
) -> set[int]:
    cases = split.get("cases")
    examples = anchors.get("examples")
    if not isinstance(cases, list) or not isinstance(examples, list):
        raise ValueError("Anchor or split manifest is invalid")
    cases_by_id = {
        case.get("id"): case for case in cases if isinstance(case, dict)
    }
    rows = set()
    for anchor in examples:
        if (
            isinstance(anchor, dict)
            and anchor.get("kind") == "development_human_defect_anchor"
        ):
            case = cases_by_id.get(anchor.get("asset_id"))
            if not isinstance(case, dict) or case.get("split") != "development":
                raise ValueError("Anchor does not map to a development case")
            rows.add(case["row"])
    if len(rows) != 3:
        raise ValueError("Expected three development demonstration rows")
    return rows


def _assert_asset_bytes(asset: Mapping[str, Any], expected_hash: Any, role: str) -> str:
    if not isinstance(expected_hash, str) or not expected_hash:
        raise ValueError(f"Split case has no expected {role} hash")
    if asset.get("sha256") != expected_hash:
        raise ValueError(f"{role} manifest hash differs from frozen split")
    local_path = asset.get("local_path")
    if not isinstance(local_path, str) or not local_path:
        raise ValueError(f"{role} asset has no local path")
    if sha256(local_path) != expected_hash:
        raise ValueError(f"{role} bytes differ from frozen split")
    return local_path


def _prepare_case(
    case: Mapping[str, Any],
    assets_by_id: Mapping[str, Mapping[str, Any]],
    assets: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    case_id = case.get("id")
    row = case.get("row")
    variant = case.get("variant")
    device = case.get("device")
    if not (
        isinstance(case_id, str)
        and isinstance(row, int)
        and isinstance(variant, str)
        and isinstance(device, str)
    ):
        raise ValueError("Split case is missing identity fields")
    expected_id = f"comparison-row-{row:02d}-{variant}"
    if case_id != expected_id:
        raise ValueError(f"Split case id is not canonical: {case_id}")

    image = assets_by_id.get(case_id)
    if image is None:
        raise ValueError(f"Generated asset is missing: {case_id}")
    expected_image_fields = {
        "row": row,
        "variant": variant,
        "device": device,
        "type": "generated_final",
    }
    for field, expected in expected_image_fields.items():
        if image.get(field) != expected:
            raise ValueError(f"Generated asset {field} differs from frozen split")

    twins = [
        asset
        for asset in assets
        if asset.get("type") == "product_input" and asset.get("row") == row
    ]
    if len(twins) != 1:
        raise ValueError(f"Expected one product input at row {row}, found {len(twins)}")
    twin = twins[0]
    expected_twin_id = f"comparison-row-{row:02d}-product_input"
    if twin.get("id") != expected_twin_id:
        raise ValueError(f"Product input id is not canonical at row {row}")

    for field in ("source_report", "case_id", "device", "original_prompt"):
        if image.get(field) != twin.get(field):
            raise ValueError(f"Generated and product-input {field} provenance differs")
    if image.get("device") != device:
        raise ValueError("Asset device differs from split device")
    prompt = image.get("original_prompt")
    if not isinstance(prompt, str):
        raise ValueError("Generated asset has no original prompt")

    generated_path = _assert_asset_bytes(
        image, case.get("image_sha256"), "generated image"
    )
    twin_path = _assert_asset_bytes(twin, case.get("input_sha256"), "product input")
    product_type = device.lower()
    if product_type not in {"laptop", "printer"}:
        raise ValueError(f"Unsupported split device: {device}")

    return {
        "case": case,
        "runtime": {
            "generated_image": generated_path,
            "twin_image": twin_path,
            "product_type": product_type,
            "scene_prompt": prompt,
            "image_stage": "scene_generation",
        },
    }


def _safe_case_run(job: Mapping[str, Any], run_dir: Path, model: str, anchors: bool):
    case = job["case"]
    try:
        result = judge(
            job["runtime"], run_dir / case["id"], model, anchors
        )
        return {
            "id": case["id"],
            "split": case["split"],
            "ok": result["ok"],
            "natural_placement_score": result.get("judgment", {}).get(
                "natural_placement_score"
            ),
            "verdict": result.get("judgment", {}).get("verdict"),
            "model_requested": result.get("model_requested"),
            "model_returned": result.get("model_returned"),
            "error": result.get("error_type"),
            "error_type": result.get("error_type"),
            "validation_errors": result.get("validation_errors"),
        }
    except Exception as error:
        return {
            "id": case["id"],
            "split": case["split"],
            "ok": False,
            "natural_placement_score": None,
            "verdict": None,
            "model_requested": model,
            "model_returned": None,
            "error": type(error).__name__,
            "error_type": type(error).__name__,
            "validation_errors": getattr(error, "errors", None),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--split", choices=["development", "held_out"], required=True
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--run", default="pilot_v1")
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--rows", type=int, nargs="+")
    parser.add_argument("--visual-anchors", action="store_true")
    args = parser.parse_args()

    try:
        _validate_run_name(args.run)
        assets_document = json.loads(
            (ROOT / "data/assets.json").read_text(encoding="utf-8")
        )
        split = json.loads((ROOT / "data/split.json").read_text(encoding="utf-8"))
        assets_by_id, assets = _asset_index(assets_document.get("assets"))
        cases = _select_cases(split, args.split, args.rows, args.limit)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))

    run_dir = ROOT / "runs" / args.run
    run_dir.mkdir(parents=True, exist_ok=True)
    results = []
    jobs = []
    anchor_hashes = set()
    anchor_rows = set()
    if args.visual_anchors:
        try:
            anchors = _load_visual_anchors()
            anchor_hashes = {anchor["sha256"] for anchor in anchors["examples"]}
            anchor_rows = _anchor_demonstration_rows(anchors, split)
        except (OSError, json.JSONDecodeError, ValueError) as error:
            parser.error(str(error))

    for case in cases:
        try:
            job = _prepare_case(case, assets_by_id, assets)
            if case.get("row") in anchor_rows:
                raise ValueError(
                    "Development demonstration rows cannot also be pilot targets"
                )
            runtime_hashes = {
                sha256(job["runtime"]["generated_image"]),
                sha256(job["runtime"]["twin_image"]),
            }
            if anchor_hashes & runtime_hashes:
                raise ValueError("Target or twin bytes match a visual anchor")
            jobs.append(job)
        except Exception as error:
            results.append(
                {
                    "id": case.get("id"),
                    "split": case.get("split"),
                    "ok": False,
                    "natural_placement_score": None,
                    "verdict": None,
                    "model_requested": args.model,
                    "model_returned": None,
                    "error": type(error).__name__,
                    "error_type": type(error).__name__,
                    "validation_errors": getattr(error, "errors", None),
                }
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        tasks = [
            pool.submit(
                _safe_case_run,
                job,
                run_dir,
                args.model,
                args.visual_anchors,
            )
            for job in jobs
        ]
        for future in as_completed(tasks):
            result = future.result()
            results.append(result)
            print(json.dumps(result), flush=True)

    order = {case["id"]: index for index, case in enumerate(cases)}
    results.sort(key=lambda result: order.get(result["id"], len(order)))
    status_path = run_dir / f"{args.split}_status.json"
    status_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if results and all(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
