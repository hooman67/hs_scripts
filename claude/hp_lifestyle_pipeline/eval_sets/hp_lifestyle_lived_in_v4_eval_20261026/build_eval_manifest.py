#!/usr/bin/env python3
"""Build the immutable 18-case V4 text-eval manifest and exact two-key inputs."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V2_MANIFEST = ROOT / "eval_sets/hp_lifestyle_camera_v2_eval_20261022/manifest.json"
RENDERS = ROOT / "research/diversity_aware_v3/data/eval_four_renders.json"
V4 = ROOT / "research/source_messaging_v1_to_v6/versions/v4"
PROMPT = V4 / "system_prompt.md"
INPUT_SCHEMA = V4 / "input.schema.json"
OUTPUT_SCHEMA = V4 / "output.schema.json"
REGISTRY = V4 / "camera_profiles.json"
sys.path.insert(0, str(V4 / "scripts"))
from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402

ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text() == text:
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def main() -> None:
    required = (V2_MANIFEST, RENDERS, PROMPT, INPUT_SCHEMA, OUTPUT_SCHEMA, REGISTRY)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"V4 manifest prerequisites are missing: {missing}")
    v2 = json.loads(V2_MANIFEST.read_text())
    render_doc = json.loads(RENDERS.read_text())
    registry = load_registry(REGISTRY)
    render_by_type_role = {}
    renders = []
    for pair in render_doc["pairs"]:
        dtype = pair["effective_device_type"]
        for raw in pair["renders"]:
            role = raw["role"]
            profile = resolve_profile(registry, raw["camera_tag"])
            if profile["resolution"] != "exact" or profile["device_type"] != dtype:
                raise RuntimeError(f"V4 registry does not exactly resolve {raw['camera_tag']}")
            rid = f"{dtype}__{pair['device_id']}__{role}"
            item = {
                "render_id": rid,
                "pair_id": pair["pair_id"],
                "device_type": dtype,
                "role": role,
                "camera_tag": raw["camera_tag"],
                "source_camera_name": raw["source_camera_name"],
                "path": raw["source_png_absolute_path"],
                "sha256": raw["source_png_sha256"],
                "bytes": raw["source_png_bytes"],
                "width": raw["source_width_px"],
                "height": raw["source_height_px"],
                "effective_profile": profile["effective_profile"],
            }
            render_by_type_role[(dtype, role)] = item
            renders.append(item)

    inputs_dir = HERE / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    sources = []
    for source in v2["sources"]:
        source_path = Path(source["source_json_path"])
        source_obj = json.loads(source_path.read_text())
        sources.append({
            "source_id": source["source_id"], "device_type": source["device_type"],
            "source_json_path": str(source_path), "sha256": sha(source_path),
            "bytes": source_path.stat().st_size,
        })
        for role in ("close_up", "wide"):
            render = render_by_type_role[(source["device_type"], role)]
            case_id = f"{source['source_id']}__{render['camera_tag']}"
            group_id = f"{source['source_id']}__{source['device_type']}_FrontRight"
            input_path = inputs_dir / f"{case_id}.json"
            write_json(input_path, {"source_messaging": source_obj, "camera_tag": render["camera_tag"]})
            cases.append({
                "case_id": case_id, "group_id": group_id,
                "source_id": source["source_id"], "device_type": source["device_type"],
                "view_role": role, "camera_tag": render["camera_tag"],
                "input_path": str(input_path), "input_sha256": sha(input_path),
                "render_id": render["render_id"],
                "expected_camera": {"requested_tag": render["camera_tag"],
                    "resolved_tag": render["camera_tag"], "device_type": source["device_type"],
                    "profile_version": registry["version"], "resolution": "exact",
                    **render["effective_profile"]},
                "pairing_semantics": "same_source_relevance_stratum_only_independently_generated_scene_bank",
            })

    provenance = {}
    for key, path in (("system_prompt", PROMPT), ("input_schema", INPUT_SCHEMA),
                      ("output_schema", OUTPUT_SCHEMA), ("camera_profiles", REGISTRY),
                      ("render_manifest", RENDERS), ("source_manifest", V2_MANIFEST)):
        provenance[key] = {"path": str(path), "sha256": sha(path)}
    manifest = {
        "version": "hp-lifestyle-lived-in-v4-eval-2026-10-26-v1",
        "as_of": str(date.today()), "status": "authorized_full_18_case_text_batch",
        "scope": {"source_count": len(sources), "case_count": len(cases),
                  "render_count": len(renders), "candidates_per_case": 30,
                  "runtime_input_fields": ["source_messaging", "camera_tag"],
                  "environments": list(ENVIRONMENTS),
                  "independent_close_wide_calls": True, "text_generation_authorized": True,
                  "authorized_text_case_count": len(cases), "image_generation_authorized": True,
                  "image_generation_gate": "exactly_108_root_accepted_selection_rows_required"},
        "model": {"deployment": "gpt-5.5", "reasoning_effort": "medium",
                  "max_completion_tokens": 24000, "temperature": None,
                  "strict_output_schema": True, "max_concurrency": 2,
                  "max_transient_attempts": 100, "semantic_retries": 0},
        "provenance": provenance,
        "join_contract": {"case_key": "cases[].case_id", "group_key": "cases[].group_id",
            "accepted_case_join": "accepted_prompt_cases.cases[case_id]",
            "candidate_key": "{case_id}::{candidate_id}",
            "selection_join": "selection_manifest.selections[].candidate_key"},
        "sources": sources, "renders": renders, "cases": cases,
        "authorized_probe_case_ids": [
            "ee810cf51bb82bb4__printer_FrontRightCloseUp",
            "ee810cf51bb82bb4__printer_FrontRightWide",
            "22fdbf19f03d1a31__laptop_FrontRightCloseUp",
            "22fdbf19f03d1a31__laptop_FrontRightWide",
        ],
        "authorized_text_case_ids": [case["case_id"] for case in cases],
    }
    if len(sources) != 9 or len(cases) != 18 or len(renders) != 4:
        raise RuntimeError("unexpected V4 inventory counts")
    write_json(HERE / "manifest.json", manifest)
    print(json.dumps({"sources": len(sources), "cases": len(cases), "renders": len(renders),
                      "manifest": str(HERE / 'manifest.json')}, indent=2))


if __name__ == "__main__":
    main()

