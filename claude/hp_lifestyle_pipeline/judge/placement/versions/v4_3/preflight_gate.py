#!/usr/bin/env python3
"""Verify gate target provenance, anchor exclusions, and crop behavior before freeze."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from anchor_selection import normalize_camera, select_anchors, target_fingerprint
from crop import create_support_crop

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "v4" / "data" / "development_15_manifest.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    gate = json.loads((ROOT / "data" / "gate_6_manifest.json").read_text())
    source = {r["id"]: r for r in json.loads(SOURCE.read_text())["records"]}
    targets = [r["runtime_input"] for r in gate["records"]]
    rows = []
    for row in gate["records"]:
        record_id, runtime = row["record_id"], row["runtime_input"]
        generated, twin = Path(runtime["generated_image"]), Path(runtime["twin_image"])
        observed = {"generated": sha(generated), "twin": sha(twin), "prompt": hashlib.sha256(runtime["scene_prompt"].encode()).hexdigest()}
        expected = source[record_id]["hashes"]
        matches = observed == {"generated": expected["generated_image_sha256"], "twin": expected["twin_image_sha256"], "prompt": expected["scene_prompt_sha256"]}
        with tempfile.TemporaryDirectory(prefix="hp-v42-preflight-") as temporary:
            _, crop = create_support_crop(generated, twin, temporary)
        selected, selection = select_anchors(runtime, exclusion_targets=targets)
        selected_ok = True
        for anchor in selected:
            for target in targets:
                fp = target_fingerprint(target)
                collisions = [
                    anchor["generated"]["byte_sha256"] == fp["generated_byte_sha256"],
                    anchor["generated"]["pixel_sha256"] == fp["generated_pixel_sha256"],
                    anchor["twin"]["byte_sha256"] == fp["twin_byte_sha256"],
                    anchor["twin"]["pixel_sha256"] == fp["twin_pixel_sha256"],
                    anchor["prompt_sha256"] == fp["prompt_sha256"],
                    anchor["product_type"] == fp["product_type"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"],
                    anchor["device"] == fp["device"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"],
                ]
                selected_ok &= not any(collisions)
        rows.append({"record_id": record_id, "paths_exist": generated.is_file() and twin.is_file(), "hashes_match_frozen_source": matches,
                     "observed_hashes": observed, "crop_status": crop["localization_status"], "crop_fallback_reason": crop["fallback_reason"],
                     "crop_match_count": crop["match_count"], "crop_inlier_count": crop["inlier_count"],
                     "selected_anchor_ids": selection["selected_anchor_ids"], "selection_has_no_union_leakage": selected_ok})
    report = {"schema_version": "hp-placement-v4.3-gate-preflight-v1", "all_paths_and_hashes_valid": all(r["paths_exist"] and r["hashes_match_frozen_source"] for r in rows),
              "all_anchor_selections_leak_free": all(r["selection_has_no_union_leakage"] for r in rows), "rows": rows}
    out = ROOT / "data" / "gate_6_preflight.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    if not report["all_paths_and_hashes_valid"] or not report["all_anchor_selections_leak_free"]:
        raise SystemExit(1)
    print(json.dumps({"all_paths_and_hashes_valid": True, "all_anchor_selections_leak_free": True,
                      "crop_statuses": {r["record_id"]: r["crop_status"] for r in rows}}, indent=2))


if __name__ == "__main__":
    main()
