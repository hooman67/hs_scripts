"""Verify all core native-pixel packets and full baseline image budgets before calls."""

import json
from pathlib import Path

import common
import visual


def main():
    if (common.ROOT / "protocol_freeze.json").exists():
        raise ValueError("Preflight must precede protocol freeze")
    budget = json.loads((common.ROOT / "visual_policy.json").read_text())[
        "max_encoded_request_image_bytes"
    ]
    records = []
    for dataset, filename, key in (
        ("calibration", "calibration_manifest.json", "cases"),
        ("ctech", "evaluation/ctech/corpus.json", "records"),
    ):
        for case in json.loads((common.ROOT / filename).read_text())[key]:
            runtime = {name: case[name] for name in ("product_type", "scene_prompt")}
            runtime["image_stage"] = "scene_generation"
            for name in ("generated_image", "twin_image"):
                runtime[name] = case[name]["local_path"]
                if common.sha(runtime[name]) != case[name]["sha256"]:
                    raise ValueError("Original source bytes changed")
            packet = visual.prepare(runtime)
            anchors, _ = common.LEGACY.select_anchors(runtime)
            total = packet["base64_image_bytes"] + sum(
                4 * ((Path(anchor["local_path"]).stat().st_size + 2) // 3)
                for anchor in anchors
            )
            if total > budget:
                raise ValueError(f"Full baseline exceeds budget: {case['id']}: {total}")
            manifest = (
                common.ROOT
                / "evaluation/visual_packets"
                / common.fingerprint(packet["identity"])
                / "manifest.json"
            )
            records.append(
                {
                    "dataset": dataset,
                    "id": case["id"],
                    "packet_path": str(manifest.resolve()),
                    "packet_sha256": common.sha(manifest),
                    "full_images": 2,
                    "delivered_images": len(packet["delivered_images"]),
                    "coverage_tiles": len(packet["coverage"]),
                    "packet_encoded_image_bytes": packet["base64_image_bytes"],
                    "baseline_total_encoded_image_bytes": total,
                }
            )
            print(json.dumps(records[-1]), flush=True)
    if len(records) != 36:
        raise ValueError("Core source set is not six calibration plus thirty C-Tech")
    common.write_json(
        common.ROOT / "evaluation/visual_preflight.json",
        {
            "actual_model_calls": 0,
            "full_originals_retained": True,
            "max_encoded_image_bytes": budget,
            "records": records,
            "complete": True,
        },
    )


if __name__ == "__main__":
    main()
