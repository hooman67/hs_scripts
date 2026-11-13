#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Run the frozen judge-v2 stack on the new 160-row V6.1 manifest.

The wrapper imports v2 modules in a fresh, verified module namespace, checks a
pre-call freeze, redirects only v2 run output into v3/runs, and delegates batch
execution unchanged. It never imports or calls the v3 judge implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[3]
V2_ROOT = ROOT.parent / "v2"
V3_RUNS_ROOT = ROOT / "runs"
DEFAULT_MANIFEST = ROOT / "data/new_v6_1_eval_20261105/manifest.json"
DEFAULT_FREEZE = ROOT / "data/v6_1_v2_baseline_freeze.json"
RUN_NAME = "v6_1_v2_baseline"
MODEL = "gpt-5.5"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    require(path.is_file(), f"missing frozen file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON in {path}: {exc}") from exc


def verify_freeze(freeze_path: Path, manifest_path: Path) -> Mapping[str, Any]:
    freeze = load_json(freeze_path)
    require(isinstance(freeze, Mapping), "freeze must be an object")
    require(freeze.get("status") == "frozen_before_v2_baseline_calls", "freeze status differs")
    require(freeze.get("model") == MODEL, "frozen model differs")
    require(freeze.get("visual_anchors") is True, "v2 baseline must use visual anchors")
    require(freeze.get("run_name") == RUN_NAME, "frozen run name differs")
    files = freeze.get("files")
    require(isinstance(files, Mapping) and files, "freeze files map missing")
    for relative, expected in files.items():
        require(isinstance(relative, str) and isinstance(expected, str), "invalid freeze entry")
        path = PROJECT_ROOT / relative
        require(sha256(path) == expected, f"frozen file changed: {relative}")
    manifest_relative = manifest_path.relative_to(PROJECT_ROOT).as_posix()
    require(files.get(manifest_relative) == sha256(manifest_path), "selected manifest differs from freeze")
    records = load_json(manifest_path).get("records")
    require(isinstance(records, list) and len(records) == 160, "manifest is not the frozen 160 rows")
    ids = [record.get("id") for record in records if isinstance(record, Mapping)]
    require(len(ids) == len(set(ids)) == 160, "manifest IDs are invalid or duplicated")
    require(freeze.get("record_ids_in_order") == ids, "manifest IDs/order differ from freeze")
    input_hashes = freeze.get("input_hashes")
    require(isinstance(input_hashes, Mapping) and set(input_hashes) == set(ids), "frozen inputs differ")
    for record in records:
        record_id = record["id"]
        require(record.get("label_provenance", {}).get("human_annotations_included") is False, f"{record_id}: human labels present")
        require(record.get("label_provenance", {}).get("passed_to_judge") is False, f"{record_id}: label pass-through differs")
        require(record.get("scene_prompt_source", {}).get("rewritten_prompt_included") is False, f"{record_id}: rewritten prompt included")
        hashes = record.get("hashes")
        require(isinstance(hashes, Mapping), f"{record_id}: input hashes missing")
        require(dict(hashes) == input_hashes[record_id], f"{record_id}: input hashes differ from freeze")
    return freeze


def load_v2_modules() -> tuple[Any, Any, Any]:
    for module_name in ("run_batch", "run_judge", "scoring"):
        require(module_name not in sys.modules, f"unsafe preloaded module: {module_name}")
    sys.path.insert(0, str(V2_ROOT))
    try:
        batch = importlib.import_module("run_batch")
        judge = importlib.import_module("run_judge")
        scoring = importlib.import_module("scoring")
    finally:
        try:
            sys.path.remove(str(V2_ROOT))
        except ValueError:
            pass
    expected = {
        "run_batch": V2_ROOT / "run_batch.py",
        "run_judge": V2_ROOT / "run_judge.py",
        "scoring": V2_ROOT / "scoring.py",
    }
    for name, module in (("run_batch", batch), ("run_judge", judge), ("scoring", scoring)):
        require(Path(module.__file__).resolve() == expected[name].resolve(), f"loaded wrong {name} module")
    require(batch.judge is judge.judge, "v2 batch is not bound to frozen v2 judge")
    require(judge.aggregate is scoring.aggregate_observation, "v2 judge is not bound to frozen v2 scoring")
    return batch, judge, scoring


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="verify freeze, imports, and all v2 inputs without model calls or run creation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(1 <= args.workers <= 32, "workers must be in 1..32")
    manifest_path = args.manifest.expanduser().resolve()
    freeze_path = args.freeze.expanduser().resolve()
    verify_freeze(freeze_path, manifest_path)
    batch, judge, _scoring = load_v2_modules()
    if args.validate_only:
        # Exercise the frozen authentication/client import path without sending a request.
        judge.client()
    batch.RUNS_ROOT = V3_RUNS_ROOT
    delegated = [
        str(Path(batch.__file__).resolve()),
        "--manifest",
        str(manifest_path),
        "--run-name",
        RUN_NAME,
        "--workers",
        str(args.workers),
        "--model",
        MODEL,
        "--visual-anchors",
    ]
    if args.validate_only:
        delegated.append("--validate-only")
    previous_argv = sys.argv
    try:
        sys.argv = delegated
        return int(batch.main())
    finally:
        sys.argv = previous_argv


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        raise SystemExit(f"error: {exc}") from exc
