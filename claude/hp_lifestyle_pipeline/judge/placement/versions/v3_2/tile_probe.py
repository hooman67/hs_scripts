# /// script
# requires-python = ">=3.12"
# dependencies = ["Pillow", "jsonschema", "foundry-aws-gateway[llm]>=2.0.0"]
# ///
"""Test whether fixed, native-pixel scene tiles expose the disputed evidence."""

import json
import math

import common

OUTPUT = common.ROOT / "astra_native_tile_probe"


def main():
    from PIL import Image

    cases = json.loads((common.R1 / "r2/calibration_manifest.json").read_text())[
        "cases"
    ]
    directory = common.ROOT.parents[2] / "local_runs/placement_v3_2_native_tile_probe"
    directory.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in cases:
        entry = {
            "id": case["id"],
            "expected_criteria": case["expectation"],
            "scene": case["generated_image"],
            "reference": case["twin_image"],
            "tiles": [],
        }
        if case["role"] == "ctech_anchor":
            scene = case["generated_image"]
            if common.sha(scene["local_path"]) != scene["sha256"]:
                raise ValueError("Original scene bytes changed")
            with Image.open(scene["local_path"]) as image:
                w, h = image.size
                bounds = (
                    (0, 0, math.ceil(w * 0.55), math.ceil(h * 0.55)),
                    (math.floor(w * 0.45), 0, w, math.ceil(h * 0.55)),
                    (0, math.floor(h * 0.45), math.ceil(w * 0.55), h),
                    (math.floor(w * 0.45), math.floor(h * 0.45), w, h),
                )
                for index, box in enumerate(bounds, 1):
                    path = directory / (case["id"] + f"--tile{index}.png")
                    image.crop(box).save(path)
                    entry["tiles"].append(
                        {
                            "index": index,
                            "box_xyxy": box,
                            "path": str(path),
                            "sha256": common.sha(path),
                            "dimensions": [box[2] - box[0], box[3] - box[1]],
                            "transform": "Fixed overlapping quadrants, exact decoded original pixels saved losslessly as PNG. No resizing, sharpening, overlays or hand-selected ROI.",
                        }
                    )
        entries.append(entry)
    inputs = {
        "task": "Use the full images and exact native-pixel tiles to investigate whether the unresolved EliteBook construction criterion is a visual-resolution/perception problem. You do visual analysis and sensitive prompt design only, no code. Engineer prepared the same deterministic overlapping-quadrant transform for ALL three human anchors, not a hand-selected defect crop; controls are full-image/reference context.",
        "cases": entries,
        "evidence_history": json.loads(
            (common.ROOT / "astra_revision_consult/proposal.json").read_text()
        ),
        "constraints": (
            "The original human criteria remain: Cashmere1 no material orientation defect; Cashmere4 "
            "material product/table conflict; EliteBook4 no material orientation defect but material "
            "table-construction defect. Full uncropped originals remain authoritative. Cropping "
            "hides context and does not create missing supports or stronger evidence by itself. "
            "Inspect actual visible tabletop outline, thickness, frame, joins, member ownership "
            "and consistency, not a generic checklist. A legal thick apron, splayed frame, hidden "
            "attachment or unfamiliar form must not fail without an affirmative cue. Do not invent "
            "an accusation to meet a label, inflate confidence, introduce case IDs/coordinates in "
            "runtime prompts or suppress the Cashmere true orientation defect. Keep all schemas/"
            "scoring and P1/P2 architectures fixed. If the tiles do not reveal sufficient new "
            "evidence, say the multiscale runtime is not justified; do not generate another "
            "cosmetic prompt revision or promise promotion. All examples are development diagnostics."
        ),
        "required_json_output": {
            "case_reviews": "Three human-anchor records: actual newly visible evidence, tile ID if any, counter-evidence, construction severity/confidence/codes, orientation assessment, honest agreement/disagreement with each human criterion.",
            "multiscale_runtime_justified": "boolean; true only if meaningful visual evidence warrants a universal fixed-tile runtime, not merely to continue semantic trials",
            "evidence_that_changed": "Specific new pixel-grounded facts versus your previous full-image diagnosis, or explicit none.",
            "revised_prompts": "If and only if justified, all seven complete prompts under the same p1_baseline/p1_compact/p1_proposal/p1_independent/p2_geometry/p2_use/p2_reconcile keys; no image IDs or memorized coordinates; identify full-scene/reference/tiles by role. Otherwise null.",
            "remaining_disagreement": "Which human criteria cannot presently be substantiated and exactly what human localization/clarification would resolve the disagreement.",
        },
    }
    OUTPUT.mkdir(exist_ok=True)
    common.write_json(OUTPUT / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    for case in entries:
        parts += common.LEGACY.image_parts(
            case["id"] + " / full authoritative scene", case["scene"]["local_path"]
        )
        parts += common.LEGACY.image_parts(
            case["id"] + " / product reference", case["reference"]["local_path"]
        )
        for tile in case["tiles"]:
            parts += common.LEGACY.image_parts(
                case["id"] + f" / fixed quadrant tile{tile['index']}", tile["path"]
            )
    result, receipt = common.model_completion(
        [
            {
                "role": "system",
                "content": "You are Astra, the HP placement visual-analysis and system-prompt specialist. Investigate actual native-pixel evidence; preserve disagreement and never manufacture a promotion result.",
            },
            {"role": "user", "content": parts},
        ],
        None,
        24576,
        OUTPUT,
    )
    if type(result["multiscale_runtime_justified"]) is not bool:
        raise ValueError("Missing explicit evidence-based multiscale decision")
    if result["multiscale_runtime_justified"]:
        roles = json.loads(
            (common.ROOT / "astra_revision_consult/proposal.json").read_text()
        )["revised_prompts"]
        if not isinstance(result["revised_prompts"], dict) or set(
            result["revised_prompts"]
        ) != set(roles):
            raise ValueError("Missing complete justified successor prompts")
    elif result["revised_prompts"] is not None:
        raise ValueError("Unjustified semantic revision must not be extracted")
    common.write_json(OUTPUT / "analysis.json", result)
    common.write_json(OUTPUT / "receipt.json", receipt)


if __name__ == "__main__":
    main()
