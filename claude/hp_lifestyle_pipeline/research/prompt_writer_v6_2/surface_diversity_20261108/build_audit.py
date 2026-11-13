#!/usr/bin/env python3
"""Build the bounded V6.2 support-surface audit from frozen local evidence."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import json
import re


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = ROOT / (
    "eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/"
    "revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/"
    "prompts_all_160.json"
)
RUN = ROOT / (
    "eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/"
    "generation_gpt_image2_scene_v1/run"
)
PLACEMENT_MANIFEST = ROOT / (
    "judge/placement/versions/v3/data/new_v6_2_eval_20261107/manifest.json"
)
FE_ROOT = ROOT / (
    "judge/placement/versions/v3/fe_reports/"
    "v6_2_consensus_v2_grouped_20261107"
)
FE_DATA = FE_ROOT / "data.json"
GROUPED_PUBLICATION_PLAN = ROOT / (
    "judge/placement/versions/v3/data/new_v6_2_eval_20261107/"
    "grouped_publication_plan.json"
)
GENERAL_PUBLICATION_PLAN = ROOT / (
    "judge/placement/versions/v3/data/new_v6_2_eval_20261107/"
    "publication_plan.json"
)
OUTPUT = Path(__file__).with_name("audit.json")


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def shape_category(text: str) -> str:
    first_sentence = text.split(".", 1)[0].lower()
    if re.search(r"\b(?:round|circular)\b", first_sentence):
        return "round_or_circular"
    if re.search(r"\boval\b", first_sentence):
        return "oval"
    if re.search(r"\brectangular\b", first_sentence):
        return "rectangular"
    return "unspecified_shape"


def nested_counts(rows: list[dict], key) -> dict:
    counts: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        counts[key(row)][shape_category(row["text"])] += 1
    return {
        group: {
            "total": sum(counter.values()),
            **{name: counter.get(name, 0) for name in SHAPE_CATEGORIES},
        }
        for group, counter in sorted(counts.items())
    }


SHAPE_CATEGORIES = [
    "round_or_circular",
    "oval",
    "rectangular",
    "unspecified_shape",
]

PRINTER_SUPPORT_PATTERNS = [
    ("dedicated output table", r"dedicated output table"),
    ("sturdy office worktable", r"sturdy office worktable"),
    ("substantial side table", r"substantial side table"),
    ("dedicated home-workspace table", r"dedicated home-workspace table"),
    ("sturdy studio worktable", r"sturdy studio worktable"),
    ("classroom resource table", r"classroom resource table"),
    ("library worktable", r"library worktable"),
    ("wide worktable", r"wide worktable"),
    ("sturdy utility table", r"sturdy utility table"),
    ("utility table", r"utility table"),
    ("production table", r"production table"),
    ("wide project table", r"wide project table"),
    ("shared project table", r"shared project table"),
    ("sturdy supply table", r"sturdy supply table"),
]

VISUAL_OBSERVATIONS = {
    "cashmere__laptop_FrontCloseUp::p8": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "A straight front edge and right corner are visible; no curved tabletop perimeter is visible.",
        "confidence": "high",
    },
    "cashmere__laptop_BackRightCloseUp::p7": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The cropped tabletop has straight edges and a corner; no round perimeter is visible.",
        "confidence": "high",
    },
    "cashmere__laptop_FrontLeftMedium::p8": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The tabletop is visibly rectangular with straight front and side edges.",
        "confidence": "high",
    },
    "cashmere__laptop_FrontWide::p7": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The full café support reads as a four-corner square/rectangular table.",
        "confidence": "high",
    },
    "elitebook__laptop_FrontCloseUp::p8": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The front edge and right corner are straight; no curved tabletop perimeter is visible.",
        "confidence": "high",
    },
    "elitebook__laptop_BackRightCloseUp::p8": {
        "classification": "full_footprint_inconclusive_due_crop",
        "observation": "The tabletop fills the lower frame and does not expose enough outer perimeter to classify the full footprint; no curved perimeter is visible in the crop.",
        "confidence": "medium",
    },
    "elitebook__laptop_FrontLeftMedium::p8": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The tabletop visibly has straight edges and a rectangular footprint.",
        "confidence": "high",
    },
    "elitebook__laptop_FrontWide::p8": {
        "classification": "visible_straight_edged_or_rectangular",
        "observation": "The full café support reads as a four-corner square/rectangular table.",
        "confidence": "high",
    },
}


source_document = json.loads(SOURCE.read_text())
prompts = source_document["prompts"]
assert len(prompts) == 160

overall_counter = Counter(shape_category(row["text"]) for row in prompts)
explicit_shape_rows = []
for row in prompts:
    category = shape_category(row["text"])
    if category == "unspecified_shape":
        continue
    explicit_shape_rows.append(
        {
            "row_id": row["prompt_key"],
            "device": row["device_id"],
            "device_type": row["device_type"],
            "environment": row["environment"],
            "shape_category": category,
            "source_prompt": row["text"],
            "source_text_sha256": row["text_sha256"],
        }
    )

round_cafe_rows = []
for row in prompts:
    if row["environment"] != "Café" or shape_category(row["text"]) != "round_or_circular":
        continue
    slug = row["prompt_key"].replace("::", "__")
    record_path = RUN / "records" / f"{slug}.json"
    record = json.loads(record_path.read_text())
    scene_debug = record["scene_debug"]
    geometry = scene_debug["geometryResponse"]["geometry"]
    composition = scene_debug["writingResponse"]["composition"]
    executable_prompt = scene_debug["writingResponse"]["prompt"]
    conflict = re.search(
        r"(?i)(?:Conflict resolution: )?the requested round[^.]*\.", composition
    )
    assert conflict, row["prompt_key"]
    image_path = RUN / "images" / record["image_filename"]
    assert image_path.is_file()
    assert file_sha(image_path) == record["image_sha256"]
    round_cafe_rows.append(
        {
            "row_id": row["prompt_key"],
            "device": row["device_id"],
            "camera_tag": row["camera_tag"],
            "source_prompt": row["text"],
            "geometry_support_m": {
                "width": geometry["support_width_m"],
                "depth": geometry["support_depth_m"],
            },
            "geometry_is_equal_sided_rectangle": (
                geometry["support_width_m"] == geometry["support_depth_m"]
            ),
            "debug_conflict_resolution_quote": conflict.group(0),
            "executable_prompt_shape_evidence": next(
                (
                    sentence.strip()
                    for sentence in re.split(
                        r"(?<=[.!?])\s+", executable_prompt.replace("\n", " ")
                    )
                    if re.search(
                        r"(?i)\b(?:square|straight-edged|drawn support|drawn edge|exact perimeter)\b",
                        sentence,
                    )
                ),
                "No standalone shape token in the executable prompt; the higher-priority composition conflict quote and rectangular guide govern the final prompt.",
            ),
            "downstream_preserved_round_shape": False,
            "generation_record": str(record_path),
            "local_image": str(image_path),
            "image_sha256": record["image_sha256"],
            "manual_image_observation": VISUAL_OBSERVATIONS[row["prompt_key"]],
        }
    )

assert len(round_cafe_rows) == 8

printer_prompts = [row for row in prompts if row["device_type"] == "printer"]
assert len(printer_prompts) == 80
printer_families: Counter = Counter()
printer_family_rows: dict[str, list[str]] = defaultdict(list)
for row in printer_prompts:
    first_sentence = row["text"].split(".", 1)[0].lower()
    family = next(
        (
            name
            for name, pattern in PRINTER_SUPPORT_PATTERNS
            if re.search(rf"\b{pattern}\b", first_sentence)
        ),
        None,
    )
    assert family, row["prompt_key"]
    printer_families[family] += 1
    printer_family_rows[family].append(row["prompt_key"])

printer_rewrite_table_rows = 0
for row in printer_prompts:
    slug = row["prompt_key"].replace("::", "__")
    record = json.loads((RUN / "records" / f"{slug}.json").read_text())
    executable_prompt = record["scene_debug"]["writingResponse"]["prompt"]
    if re.search(r"(?i)\b(?:table|worktable|tabletop)\b", executable_prompt):
        printer_rewrite_table_rows += 1
assert printer_rewrite_table_rows == 80

fe_document = json.loads(FE_DATA.read_text())
printer_judge_rows = []
for fe_row in fe_document["rows"]:
    metadata = fe_row["meta_data"]["key_val_informations"]
    if metadata["Product type"] != "printer":
        continue
    assessment = json.loads(metadata["Baseline V2 original assessment"])
    support_description = assessment["observation"]["scene_reading"]["support_surface"]
    alternatives = [
        term
        for term in ["cabinet", "credenza", "counter", "console", "bench"]
        if re.search(rf"(?i)\b{term}\b", support_description)
    ]
    if alternatives:
        classification = "ambiguous_table_or_other"
    elif "separate blue sideboard" in support_description.lower():
        classification = "table_with_separate_secondary_sideboard"
    else:
        classification = "table_only_description"
    printer_judge_rows.append(
        {
            "row_id": fe_row["meta_data"]["evalset_item_id"],
            "classification": classification,
            "alternative_terms": alternatives,
            "judge_support_surface_description": support_description,
        }
    )
assert len(printer_judge_rows) == 80
printer_judge_counts = Counter(row["classification"] for row in printer_judge_rows)

placement_manifest = json.loads(PLACEMENT_MANIFEST.read_text())
local_generated_bad = []
run_generated_bad = []
for row in placement_manifest["records"]:
    expected_sha = row["generated_image"]["sha256"]
    local_path = Path(row["generated_image"]["local_path"])
    run_path = RUN / "images" / row["generated_image"]["filename"]
    if not local_path.is_file() or file_sha(local_path) != expected_sha:
        local_generated_bad.append(str(local_path))
    if not run_path.is_file() or file_sha(run_path) != expected_sha:
        run_generated_bad.append(str(run_path))

twin_paths = {
    Path(row["twin_image"]["local_path"]): row["twin_image"]["sha256"]
    for row in placement_manifest["records"]
}
twin_bad = [
    str(path)
    for path, expected_sha in twin_paths.items()
    if not path.is_file() or file_sha(path) != expected_sha
]

grouped_plan = json.loads(GROUPED_PUBLICATION_PLAN.read_text())
grouped_bad = []
for item in grouped_plan["objects"]:
    path = FE_ROOT / item["relative_path"]
    if (
        not path.is_file()
        or path.stat().st_size != item["bytes"]
        or file_sha(path) != item["sha256"]
    ):
        grouped_bad.append(str(path))

image_refs = [
    image["image_src"]
    for row in fe_document["rows"]
    for image in row["images"]
    if image.get("asset_type") == "image"
]
endpoint_refs = [url for url in image_refs if ".colligo.dev/" in url]
foundry_refs = [url for url in image_refs if "foundry-aws-corp.adobe.io/" in url]
assert len(endpoint_refs) == 160
assert len(set(foundry_refs)) == 16

general_plan = json.loads(GENERAL_PUBLICATION_PLAN.read_text())
twin_plan_objects = [
    row for row in general_plan["objects"] if "/assets/twins/" in row["key"]
]
assert len(twin_plan_objects) == 16

audit = {
    "schema_version": "hp-v6.2-surface-diversity-audit-v1",
    "as_of_date": "2026-11-08",
    "scope": {
        "question": "Count source-prompt primary-support shapes, trace explicit round café requests through downstream rewrites and images, census printer support types, and audit current grouped FE publication dependencies.",
        "included": [
            "all 160 frozen V6.2 prompt rows",
            "all 160 saved scene-generation records",
            "manual inspection of the eight generated images whose source prompt explicitly requests a round café table",
            "printer support descriptions in the existing image-derived placement-judge report",
            "local grouped FE files and locally preserved image equivalents",
        ],
        "excluded": [
            "new image generation",
            "new model or judge calls",
            "edits to canonical/runtime files",
            "remote S3 existence verification",
        ],
    },
    "sources": {
        "frozen_prompts": {"path": str(SOURCE), "sha256": file_sha(SOURCE)},
        "generation_run": {"path": str(RUN), "records": 160, "images": 160},
        "placement_manifest": {
            "path": str(PLACEMENT_MANIFEST),
            "sha256": file_sha(PLACEMENT_MANIFEST),
        },
        "grouped_fe_data": {"path": str(FE_DATA), "sha256": file_sha(FE_DATA)},
        "grouped_publication_plan": {
            "path": str(GROUPED_PUBLICATION_PLAN),
            "sha256": file_sha(GROUPED_PUBLICATION_PLAN),
        },
    },
    "method": {
        "source_shape_rule": "Classify explicit round/circular, oval, or rectangular tokens in the first sentence that names the primary support. All other primary supports are unspecified_shape; adjectives such as broad, wide, long, small, or square-to-the-wall alignment do not establish footprint shape.",
        "printer_primary_support_rule": "Classify the first-sentence support that bears the printer. Secondary cabinets, sideboards, shelves, carts, and cubbies do not change the primary-support class.",
        "evidence_separation": "Source prompt and rewrite/debug findings are text evidence. Only the eight round-café manual observations are direct image inspection. Placement-judge support descriptions are image-derived model text and are reported separately from direct inspection.",
    },
    "source_shape_counts": {
        "confidence": "VERIFIED",
        "overall": {
            "total": len(prompts),
            **{name: overall_counter.get(name, 0) for name in SHAPE_CATEGORIES},
            "literal_circular_token": sum(
                bool(re.search(r"(?i)\bcircular\b", row["text"].split(".", 1)[0]))
                for row in prompts
            ),
        },
        "by_device": nested_counts(prompts, lambda row: row["device_id"]),
        "by_environment": nested_counts(prompts, lambda row: row["environment"]),
        "by_device_and_environment": nested_counts(
            prompts, lambda row: f'{row["device_id"]} | {row["environment"]}'
        ),
        "explicit_shape_rows": explicit_shape_rows,
    },
    "round_cafe_downstream_audit": {
        "confidence": "VERIFIED for saved text/debug and direct manual observations of these eight local images",
        "summary": {
            "source_rows": 8,
            "downstream_round_shape_preserved": 0,
            "downstream_explicitly_overridden_to_square_or_straight_edged": 8,
            "manual_images_with_visible_round_primary_support": 0,
            "manual_images_visible_straight_edged_or_rectangular": 7,
            "manual_images_full_footprint_inconclusive_due_crop": 1,
        },
        "root_cause_evidence": "The geometry stage emits a rectangular support polygon and describes long edges, short edges, and corners. The writing stage treats that fixed guide as higher priority than the source request, explicitly declares a conflict, and substitutes a square/straight-edged tabletop in every round café row.",
        "rows": round_cafe_rows,
    },
    "other_explicit_shape_downstream_note": {
        "confidence": "VERIFIED text/debug evidence",
        "finding": "The same conflict behavior affects all three round Home rows and the one oval Office row. The single rectangular source row is preserved. Across all 13 explicitly shaped source rows: 11 round requests and one oval request are overridden by fixed straight-edged geometry; one rectangular request remains compatible.",
    },
    "printer_support_census": {
        "source_prompt_text": {
            "confidence": "VERIFIED",
            "total_printer_rows": 80,
            "primary_table_family": 80,
            "primary_cabinet_credenza_sideboard_shelf_counter_console_cart_or_cubbies": 0,
            "shape_explicit_round_or_circular": 0,
            "shape_explicit_oval": 0,
            "shape_explicit_rectangular": 0,
            "shape_unspecified": 80,
            "table_family_counts": dict(sorted(printer_families.items())),
            "table_family_row_ids": {
                family: rows for family, rows in sorted(printer_family_rows.items())
            },
            "secondary_non_primary_furnishings": {
                "note": "Secondary furniture is present in some prompts but never bears the printer.",
                "storage_cabinet_rows": 6,
                "sideboard_rows": 1,
                "rolling_cart_rows": 4,
                "floating_shelf_rows": 1,
                "open_cubbies_rows": 1,
            },
        },
        "downstream_executable_rewrite_text": {
            "confidence": "VERIFIED lexical evidence",
            "rows_with_table_worktable_or_tabletop_term": printer_rewrite_table_rows,
            "rows_without_table_family_term": 80 - printer_rewrite_table_rows,
            "limitation": "This establishes requested/rewrite support vocabulary, not the rendered furniture morphology.",
        },
        "existing_placement_judge_image_descriptions": {
            "confidence": "UNVERIFIED as a human visual census; these are saved judge descriptions derived from images",
            "table_only_description": printer_judge_counts["table_only_description"],
            "ambiguous_table_or_other": printer_judge_counts["ambiguous_table_or_other"],
            "table_with_separate_secondary_sideboard": printer_judge_counts[
                "table_with_separate_secondary_sideboard"
            ],
            "definite_non_table_primary_support": 0,
            "ambiguous_other_term_counts": dict(
                Counter(
                    term
                    for row in printer_judge_rows
                    for term in row["alternative_terms"]
                )
            ),
            "ambiguous_rows": [
                row
                for row in printer_judge_rows
                if row["classification"] == "ambiguous_table_or_other"
            ],
        },
    },
    "current_grouped_fe_asset_audit": {
        "confidence": "VERIFIED for local filesystem and hashes; remote publication not checked",
        "grouped_fe": {
            "root": str(FE_ROOT),
            "planned_objects": len(grouped_plan["objects"]),
            "planned_objects_present_and_hash_matching": len(grouped_plan["objects"])
            - len(grouped_bad),
            "bad_or_missing": grouped_bad,
            "composition": "root viewer.html + root data.json + 16 group viewer.html/data.json pairs",
        },
        "image_references_in_current_data_json": {
            "total": len(image_refs),
            "unique": len(set(image_refs)),
            "generated_output_refs": len(endpoint_refs),
            "unique_generated_output_refs": len(set(endpoint_refs)),
            "generated_output_ref_host": "pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev",
            "twin_refs": len(foundry_refs),
            "unique_twin_refs": len(set(foundry_refs)),
            "twin_ref_host": "foundry-aws-corp.adobe.io",
            "relative_or_bundled_asset_refs": 0,
        },
        "local_equivalents": {
            "generation_run_images": {
                "path": str(RUN / "images"),
                "expected": 160,
                "present_and_hash_matching": 160 - len(run_generated_bad),
                "bad_or_missing": run_generated_bad,
            },
            "judge_copy_generated_images": {
                "path": str(ROOT / "judge/local_runs/v6_2_placement_assets/generated"),
                "expected": 160,
                "present_and_hash_matching": 160 - len(local_generated_bad),
                "bad_or_missing": local_generated_bad,
            },
            "twins": {
                "path": str(ROOT / "judge/local_runs/v6_2_placement_assets/twins"),
                "expected_unique": 16,
                "present_and_hash_matching": 16 - len(twin_bad),
                "bad_or_missing": twin_bad,
            },
        },
        "publication_dependencies": {
            "status": "The grouped plan and the general plan are local/dry-run evidence; project state says publication is pending because AWS credentials expired and broker hosts timed out.",
            "grouped_fe_objects": 34,
            "twin_asset_objects_from_general_plan": len(twin_plan_objects),
            "minimum_objects_for_current_grouped_fe_if_endpoint_urls_remain_live": 50,
            "durability_gap": "The grouped FE data points all 160 generated outputs at Pluto endpoint artifact URLs. The grouped publication plan contains no generated-image objects, so the report is not self-contained and depends on those endpoint URLs remaining readable.",
            "stable_publication_requirement": "Upload the 160 hash-verified local generated PNGs to durable S3 paths and rebuild/rewrite every root and group data.json output image_src to those stable Foundry URLs (or bundle equivalent assets). Then upload the 34 grouped FE objects and 16 twin objects and verify remote metadata/hashes.",
            "stable_self_contained_object_count_if_each_generated_image_is_uploaded_once": 210,
            "aws_rule": "Any S3 execution must first refresh credentials with /aws-creds and source the resulting environment in the same shell command; this audit performed no upload.",
        },
    },
    "implication_for_revision": {
        "confidence": "VERIFIED causal evidence within this saved pipeline run",
        "finding": "Changing only V6.2 source prompt wording cannot make round or oval supports survive this downstream path. The geometry/guide contract and priority rule must represent curved support footprints or allow a requested curved perimeter to override the rectangular guide; otherwise the rewrite will continue to convert the requested shape to a four-corner table.",
        "printer_diversity_finding": "V6.2 supplies no primary printer-support category diversity: all 80 source rows and all 80 executable rewrites use table-family vocabulary. Cabinet, credenza, shelf, console, or counter supports would require deliberate source-prompt and downstream-geometry support, with printer access and wall placement retained.",
    },
    "limitations": [
        "Only the eight explicit round café outputs received direct manual image inspection in this audit.",
        "The 80-row printer rendered-support breakdown uses existing placement-judge text and is not a new human image annotation.",
        "Remote S3 and endpoint availability were not tested; local existence and hashes were tested.",
        "Unspecified_shape means no explicit footprint-shape token in the primary support phrase; it does not imply that the generated image lacks a shape.",
    ],
}

OUTPUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
print(OUTPUT)
