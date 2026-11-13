#!/usr/bin/env python3
"""Eight-fixture v22 smoke: four relocation demands plus four retained controls.

This invokes the exact isolated PR4349 ``hp3p.pipeline.run_row``. Selection,
Stage-A geometry, product/style inputs and the rendered guide are replayed from
the frozen V6.1 controls. Stage B and one unmasked image edit are live. There is
no retry, best-of selection, prompt repair or mask.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from run_smoke import FrozenInputsClient, PACKAGE, PR_COMMIT, PROJECT, StyleRef, Row
import hp3p.pipeline as pipeline
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL

BASELINE = PROJECT / "smoke/baseline"
OUTPUT = PROJECT / "smoke/v22"
BASE_FIXTURES = (
    "cashmere__laptop_FrontCloseUp__p1",
    "cashmere__laptop_FrontWide__p1",
    "magic__printer_FrontCloseUp__p1",
    "magic__printer_FrontWide__p1",
)

RELOCATION_PROMPTS = {
    "cashmere__laptop_FrontCloseUp__p1": (
        "A close modern office scene. Place the fully visible laptop substantially farther toward image left than "
        "its current position, as far as its unchanged pixel size safely allows, so a broad clear planning area sits "
        "to its right. Build a pale wood worktable beneath the laptop at that chosen position, with believable edge "
        "clearances and its working edge facing the keyboard. Align an upholstered chair with the laptop's keyboard "
        "and keep the approach completely clear. A ribbed glass partition and soft daylight complete the scene."
    ),
    "cashmere__laptop_FrontWide__p1": (
        "A wide glass-walled office planning room. Move the fully visible laptop into a right-hand workstation, "
        "leaving a broad unobstructed aisle and open tabletop area on the left. Keep the laptop's exact view and pixel "
        "size. Compose a new sturdy worktable beneath it with a user-facing edge and a chair aligned directly with "
        "the keyboard. Add a felt privacy screen in the far background and cool even daylight."
    ),
    "magic__printer_FrontCloseUp__p1": (
        "A close office output station. Place the fully visible printer distinctly farther toward image right than "
        "its current position, preserving its exact view and pixel size, to leave a clear paper-sorting area on the "
        "left. Build a dedicated pale oak printer table beneath it with the complete base supported, the printer square "
        "to the table, clear standing access at the operating front, and the back of the station against a plain wall. "
        "Keep all objects beside rather than in front of the printer."
    ),
    "magic__printer_FrontWide__p1": (
        "A wide open-office output area. Relocate the fully visible printer to a right-of-center dedicated output "
        "station, leaving the left side of the room open for paper sorting and circulation. Preserve the printer's "
        "exact view and pixel size. Compose a new pale oak support table beneath it, square to the fixed printer "
        "orientation, with believable edge clearances, wall alignment and unobstructed standing access at the front. "
        "Use soft clear daylight and an orderly office background."
    ),
}


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PACKAGE, text=True).strip()
    if commit != PR_COMMIT:
        raise RuntimeError(f"Unexpected PR commit: {commit}")
    original_builder = pipeline.build_guide
    fixtures = []
    for base_slug in BASE_FIXTURES:
        source = BASELINE / base_slug
        record = json.loads((source / "record.json").read_text())
        debug = record["scene_debug"]
        guide = (source / "control_guide.png").read_bytes()
        hero = (source / "control_product.png").read_bytes()
        reference = (source / "control_reference.png").read_bytes()
        meta = debug["reference"]
        ref = StyleRef(meta["id"], meta["name"], meta["tone"], meta["content"], "image/png", reference)

        for mode, prompt in (("retained_control", record["prompt"]),
                             ("relocation_demand", RELOCATION_PROMPTS[base_slug])):
            slug = f"{base_slug}__{mode}"
            fixture_dir = OUTPUT / slug
            fixture_dir.mkdir(parents=True, exist_ok=True)
            run_dir = fixture_dir / "run"
            row = Row(slug, prompt, "frozen-v6.1-control-inputs", 2368, 1776, [])
            client = FrozenInputsClient(debug, guide, fixture_dir)

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
            (fixture_dir / "calls.json").write_text(json.dumps(client.calls, indent=2))
            if result["status"] != "ok":
                raise RuntimeError(f"{slug}: {result['error']}")
            row_dir = run_dir / "rows" / slug
            if (row_dir / "geometry_guide.png").read_bytes() != guide:
                raise RuntimeError(f"{slug}: guide differs from frozen input")
            if [call["kind"] for call in client.calls] != [
                "selection_replay", "geometry_replay", "astra_write", "image_edit"
            ]:
                raise RuntimeError(f"{slug}: unexpected call contract {client.calls}")
            fixture = {
                "slug": slug,
                "base_slug": base_slug,
                "mode": mode,
                "device_id": record["device_id"],
                "camera_id": record["camera_id"],
                "prompt": prompt,
                "pipeline_version": result["pipeline_version"],
                "guide_sha256": sha(guide),
                "output_sha256": file_sha(row_dir / "ours.png"),
                "final_prompt_sha256": sha(result["prompt"].encode()),
                "image_calls": result["image_calls"],
                "masked": result["masked"],
                "calls": client.calls,
            }
            (fixture_dir / "provenance.json").write_text(json.dumps(fixture, indent=2))
            fixtures.append(fixture)
            print(json.dumps({"completed": slug, "output_sha256": fixture["output_sha256"]}), flush=True)

    changed = [
        PACKAGE / "hp3p/prompts/system_3p.txt",
        PACKAGE / "hp3p/pipeline.py",
        PACKAGE / "hp3p/geometry.py",
        PACKAGE / "hp3p/grade.py",
        PACKAGE / "hp3p/reference_blue.py",
    ]
    manifest = {
        "schema_version": 1,
        "experiment": "v22 x-y-only product placement with independently recomposed support",
        "pr_commit": commit,
        "pipeline_version": pipeline.PIPELINE_VERSION,
        "source_hashes": {str(path.relative_to(PACKAGE)): file_sha(path) for path in changed},
        "fixtures": fixtures,
        "frozen_inputs": "V6.1 p1 products, style images, Stage-A geometry and byte-identical guides",
        "api_retries": 0,
        "best_of": 1,
        "manual_repair": False,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({"complete": len(fixtures), "manifest": str(OUTPUT / "manifest.json")}), flush=True)


if __name__ == "__main__":
    main()
