#!/usr/bin/env python3
"""Fresh V22.4 retry of the preserved V22.3.3 full-160 first row only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from run_smoke import FrozenInputsClient, PR_COMMIT, StyleRef, Row
import hp3p.pipeline as pipeline
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment")
OLD = PROJECT / "full160_v22_3_3/run"
RECORD = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
              "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/"
              "generation_gpt_image2_scene_v1/run/records/cashmere__laptop_BackRightCloseUp__p1.json")
OUTPUT = PROJECT / "smoke/v22_4_first_row_retry"
SLUG = "cashmere__laptop_BackRightCloseUp__p1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    record = json.loads(RECORD.read_text())
    debug = record["scene_debug"]
    inputs = OLD / "inputs" / SLUG
    guide = (inputs / "guide.png").read_bytes()
    hero = (inputs / "product.png").read_bytes()
    reference = (inputs / "reference.png").read_bytes()
    meta = debug["reference"]
    ref = StyleRef(meta["id"], meta["name"], meta["tone"], meta["content"], "image/png", reference)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    run_dir = OUTPUT / "run"
    row = Row(SLUG, record["prompt"], "frozen-v6.1-first-row", 2368, 1776, [])
    client = FrozenInputsClient(debug, guide, OUTPUT)
    original_builder = pipeline.build_guide

    def frozen_guide(_hero, _mask, geometry, camera):
        if geometry != debug["geometryResponse"]["geometry"] or camera != debug["twinCamera"]:
            raise RuntimeError("Frozen guide received different geometry or camera")
        return guide, dict(debug["guideInfo"])

    pipeline.build_guide = frozen_guide
    try:
        result = pipeline.run_row(row, client, [ref], run_dir, hero, ref_count=1,
                                  size=(2368, 1776), camera=debug["twinCamera"])
    finally:
        pipeline.build_guide = original_builder
    row_dir = run_dir / "rows" / SLUG
    if (row_dir / "geometry_guide.png").read_bytes() != guide:
        raise RuntimeError("Fresh retry did not use the byte-identical frozen guide")
    provenance = {
        "experiment": "v22.4 fresh first-row retry",
        "base_commit": PR_COMMIT,
        "pipeline_version": result["pipeline_version"],
        "text_model": TEXT_MODEL,
        "image_model": IMAGE_MODEL,
        "record_sha256": sha(RECORD.read_bytes()),
        "guide_sha256": sha(guide),
        "status": result["status"],
        "error": result.get("error"),
        "image_calls": result["image_calls"],
        "guard": result.get("product_invariant_guard"),
        "calls": client.calls,
        "output_sha256": sha((row_dir / "ours.png").read_bytes()) if (row_dir / "ours.png").exists() else None,
    }
    (OUTPUT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps(provenance, indent=2), flush=True)
    if result["status"] != "ok":
        raise RuntimeError(result.get("error") or "fresh first-row retry failed")


if __name__ == "__main__":
    main()
