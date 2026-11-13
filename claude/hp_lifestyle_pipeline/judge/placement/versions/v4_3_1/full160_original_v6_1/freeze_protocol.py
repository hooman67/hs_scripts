#!/usr/bin/env python3
"""Create the immutable preparation freeze for the original V6.1 full-160 run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION_ROOT = HERE.parent
DEFAULT_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
EXPECTED_MANIFEST_SHA256 = "fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_sha256(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def protocol_version() -> str:
    source = (VERSION_ROOT / "run_judge.py").read_text(encoding="utf-8")
    match = re.search(r'^PROTOCOL_VERSION = "([^"]+)"$', source, flags=re.MULTILINE)
    if match is None:
        raise SystemExit("could not read PROTOCOL_VERSION from frozen runner")
    return match.group(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=HERE / "protocol_freeze.json")
    args = parser.parse_args()
    manifest = args.manifest.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite freeze: {output}")
    if sha256(manifest) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("verified original V6.1 manifest hash differs")
    protocol_files = [
        "PROVENANCE.md",
        "system_prompt.md",
        "assessment_schema.json",
        "result_schema.json",
        "wire_schema.json",
        "scoring.py",
        "crop.py",
        "anchor_selection.py",
        "anchors/anchor_catalog.json",
        "run_judge.py",
    ]
    batch_files = ["run_batch.py", "build_grouped_report.py"]
    for relative in protocol_files:
        if not (VERSION_ROOT / relative).is_file():
            raise SystemExit(f"missing protocol source: {VERSION_ROOT / relative}")
    for name in batch_files:
        if not (HERE / name).is_file():
            raise SystemExit(f"missing batch source: {HERE / name}")
    wire = json.loads((VERSION_ROOT / "wire_schema.json").read_text(encoding="utf-8"))
    payload = {
        "schema_version": "hp-placement-v4.3.1-full160-freeze-v1",
        "status": "prepared_not_launched",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_version": protocol_version(),
        "dataset": "original V6.1 scene-generation images",
        "manifest": {"path": str(manifest), "sha256": sha256(manifest), "records": 160},
        "model": {
            "requested": "gpt-5.5",
            "route": "foundry_direct_openai",
            "reasoning_effort": "high",
            "max_completion_tokens": 24000,
            "sdk_retries": 0,
            "application_total_attempts_max": 2,
            "timeout_seconds": 600,
            "concurrency_default": 2,
            "concurrency_max": 2,
        },
        "files": {relative: sha256(VERSION_ROOT / relative) for relative in protocol_files},
        "batch_files": {name: sha256(HERE / name) for name in batch_files},
        "result_audit_hashes": {
            "system_prompt_sha256": sha256(VERSION_ROOT / "system_prompt.md"),
            "assessment_schema_sha256": sha256(VERSION_ROOT / "assessment_schema.json"),
            "wire_schema_sha256": canonical_json_sha256(wire),
            "scoring_sha256": sha256(VERSION_ROOT / "scoring.py"),
            "crop_algorithm_sha256": sha256(VERSION_ROOT / "crop.py"),
            "anchor_catalog_sha256": sha256(VERSION_ROOT / "anchors/anchor_catalog.json"),
        },
        "execution_gate": "No model call is authorized by this freeze. A live runner invocation additionally requires --acknowledge-launch-authorized.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "sha256": sha256(output), "status": payload["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
