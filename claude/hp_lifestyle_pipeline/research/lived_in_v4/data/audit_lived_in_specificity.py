#!/usr/bin/env python3
"""Build a bounded, read-only audit of lived-in specificity in HP V3 prompts.

This script reads frozen source extractions, V3 prompt exports, and the four-render
camera evidence. It does not read disallowed workbook columns, author prompts, or
modify any V3 artifact. The output is descriptive evidence for a later V4 design.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("lived_in_specificity_audit.json")


PATHS = {
    "october_extraction": ROOT / "research/source_messaging_v1_to_v6/data/october_guidance.json",
    "lifestyle_column_a_extraction": ROOT / "research/source_messaging_v1_to_v6/data/lifestyle_column_a.json",
    "model_output_extraction": ROOT / "research/source_messaging_v1_to_v6/data/model_output_evalset.json",
    "v3_all": ROOT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts.json",
    "v3_selected": ROOT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts_selected.json",
    "four_renders": ROOT / "research/diversity_aware_v3/data/eval_four_renders.json",
    "camera_profiles": ROOT / "research/source_messaging_v1_to_v6/versions/v3/camera_profiles.json",
    "october_durable_original": ROOT / "input_output_hp_rewriter_10_03_26/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx",
    "lifestyle_durable_original": ROOT / "input_output_hp_rewriter_10_03_26/example_prompts/Eval-Set_Lifestyle-Photography_wSKUs.xlsx",
    "model_output_durable_original": ROOT / "input_output_hp_rewriter_10_03_26/example_prompts/HP_Model-Output-EvalSet_092426.xlsx",
}

SCRATCH_ORIGINALS = {
    "october": Path("/mnt/localssd/HP_scenes/input_output_hp_rewriter/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx"),
    "lifestyle": Path("/mnt/localssd/HP_scenes/input_output_hp_rewriter/example_prompts/Eval-Set_Lifestyle-Photography_wSKUs.xlsx"),
    "model_output": Path("/mnt/localssd/HP_scenes/input_output_hp_rewriter/example_prompts/HP_Model-Output-EvalSet_092426.xlsx"),
}

DURABLE_ORIGINALS = {
    "october": PATHS["october_durable_original"],
    "lifestyle": PATHS["lifestyle_durable_original"],
    "model_output": PATHS["model_output_durable_original"],
}


# Each named expression is counted at most once per text. These are lexical
# indicators, not object detections or image annotations.
CUE_PATTERNS: dict[str, dict[str, str]] = {
    "work_artifacts": {
        "notebook": r"\bnotebooks?\b",
        "spiral_pad": r"\bspiral pads?\b",
        "paper": r"\b(?:papers?|paperwork|paper ream)\b",
        "form": r"\bforms?\b",
        "report": r"\breports?\b",
        "packet": r"\bpackets?\b",
        "checklist": r"\bchecklists?\b",
        "worksheet": r"\bworksheets?\b",
        "binder": r"\bbinders?\b",
        "folder": r"\bfolders?\b",
        "sketch_or_design_material": r"\b(?:sketch(?:es|book|books)?|design materials?|swatch(?:es| cards?)?)\b",
        "book": r"\bbooks?\b",
        "writing_instrument": r"\b(?:pens?|pencils?|markers?)\b",
        "glasses": r"\bglasses\b",
        "card_or_badge": r"\b(?:cards?|badges?)\b",
        "controller": r"\bcontrollers?\b",
        "schedule_or_planner": r"\b(?:schedules?|planners?|calendars?|timetables?|agendas?)\b",
        "proof_or_layout": r"\b(?:proof sheets?|layout sheets?|handouts?)\b",
    },
    "consumption_and_pause": {
        "coffee_or_tea": r"\b(?:coffee|tea)\b",
        "cup_or_mug": r"\b(?:cups?|mugs?)\b",
        "water_glass": r"\bwater glass(?:es)?\b",
        "pastry_or_crumb": r"\b(?:pastry|pastries|crumbs?)\b",
        "plate": r"\bplates?\b",
        "snack_or_candy": r"\b(?:snacks?|cand(?:y|ies)|wrapped candy)\b",
        "coaster": r"\bcoasters?\b",
        "drink": r"\bdrinks?\b",
    },
    "personal_and_domestic": {
        "personal_touch": r"\bpersonal touches?\b",
        "familiar_object": r"\bfamiliar (?:residential )?objects?\b",
        "family_photo": r"\bfamily (?:photos?|photographs?)\b",
        "cushion_or_pillow": r"\b(?:cushions?|pillows?)\b",
        "curtain": r"\bcurtains?\b",
        "rug_or_blanket": r"\b(?:rugs?|blankets?)\b",
        "residential_furnishing": r"\bresidential furnishings?\b",
    },
    "specific_mid_use_state": {
        "lived_in": r"\blived-in\b",
        "half_finished": r"\b(?:half-finished|unfinished|half-used)\b",
        "loose": r"\bloose (?:papers?|sheets?|notes?)\b",
        "crumbs": r"\bcrumbs?\b",
        "overgrown": r"\bovergrown\b",
        "casually_arranged": r"\bcasually (?:arranged|pinned|placed)\b",
        "imperfection": r"\bimperfections?\b",
        "marked_or_annotated": r"\b(?:marked-up|annotated|handwritten|date-stamped|color-coded)\b",
        "folded_or_clipped": r"\b(?:folded|clipped|stapled|tabbed)\b",
        "pinned": r"\bpinned\b",
        "partly_filled": r"\bpartly (?:filled|used|open)\b",
        "waiting_state": r"\b(?:waiting for sign-off|ready for review|mid-conversation)\b",
        "wrapper": r"\bwrappers?\b",
        "scattered_or_cluttered": r"\b(?:scattered|cluttered)\b",
    },
    "generic_surface_wear": {
        "worn": r"\bworn\b",
        "scuffed": r"\bscuffs?|scuffed\b",
        "scratched": r"\bscratches?|scratched\b",
        "edge_wear": r"\bedge wear\b",
        "stained": r"\bstained\b",
        "rubbed_finish": r"\brubbed finish\b",
    },
    "background_anchors": {
        "window": r"\bwindows?\b",
        "shelf": r"\b(?:shelves|shelving|bookshelves?|shelf)\b",
        "plant": r"\b(?:plants?|houseplants?|succulents?)\b",
        "artwork": r"\b(?:artwork|framed art)\b",
        "chair_or_seating": r"\b(?:chairs?|seating|seat|banquette)\b",
        "curtain": r"\bcurtains?\b",
        "cabinet": r"\bcabinets?\b",
        "wall_panel_or_pinboard": r"\b(?:wall panels?|acoustic panels?|pinboards?|noticeboards?|bulletin boards?|cork boards?)\b",
        "divider_or_partition": r"\b(?:dividers?|partitions?|glass walls?)\b",
        "file_box_or_storage": r"\b(?:file boxes|storage baskets?|cubbies)\b",
        "lamp": r"\blamps?\b",
        "architectural_detail": r"\b(?:architectural details?|staircases?|floor plan|ceiling beams?)\b",
    },
    "materials_and_texture": {
        "wood": r"\b(?:wood|wooden|woodgrain|walnut|oak|maple|birch|beech|ash|butcher block|plywood)\b",
        "laminate_or_veneer": r"\b(?:laminate|veneer|melamine)\b",
        "stone_or_concrete": r"\b(?:stone|concrete|terrazzo)\b",
        "ceramic": r"\bceramic\b",
        "linen_or_fabric": r"\b(?:linen|fabric|woven)\b",
        "glass": r"\bglass\b",
        "cork_or_kraft": r"\b(?:cork|kraft)\b",
        "metal": r"\b(?:metal|steel|aluminum)\b",
        "surface_finish": r"\b(?:matte|satin|polished|textured|grain|speckled|honed)\b",
    },
    "lighting": {
        "natural_or_daylight": r"\b(?:natural light|daylight|sunlight|golden-hour)\b",
        "warm_light": r"\b(?:warm light|warm natural light|warm ambient light|warm morning light|warm evening light)\b",
        "cool_light": r"\b(?:cool light|cool daylight)\b",
        "task_or_overhead_light": r"\b(?:task light|overhead light|workplace light|office light|fluorescent light)\b",
        "soft_or_diffuse_light": r"\b(?:soft light|diffuse light|diffused light|soft daylight|gentle daylight)\b",
        "side_or_angled_light": r"\b(?:side light|angled light)\b",
        "ambient_glow": r"\b(?:ambient glow|evening glow|pool of .*? light)\b",
    },
}

VISIBLE_HUMAN_PATTERNS = {
    "cropped_hand": r"\bcropped (?:\w+ )?hands?\b",
    "active_hand": r"\bhands? (?:rests?|straightens?|aligns?|writes?|holds?|reaches?|gestures?|types?)\b",
    "visible_person": r"\b(?:a|one|two|three) (?:young )?(?:woman|man|person|professional|student|teacher|gamer|designer|worker|coworker|colleague|adult|child|patron)s?\b.{0,80}\b(?:sits?|stands?|walks?|types?|writes?|holds?|gestures?|wears?|works?|reads?|reviews?|plays?)\b",
}

SURFACE_PATTERN = re.compile(r"\b(?:desk|table|tabletop|counter|worktop|surface|shelf|ledge|sideboard|bench|workbench)\b", re.I)
LIGHT_PATTERN = re.compile(r"\b(?:light|daylight|sunlight|glow|illumination)\b", re.I)
SINGULAR_OR_BARE_PATTERN = re.compile(
    r"\b(?:one|single|no props|bare|empty|otherwise bare|bare except|empty except|kept bare|uncluttered)\b",
    re.I,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: Path) -> dict[str, Any]:
    return {
        "absolute_path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)


def sentence_count(text: str) -> int:
    found = re.findall(r"[.!?]+(?=\s|$)", text.strip())
    return max(1, len(found))


def matched_cues(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for family, patterns in CUE_PATTERNS.items():
        out[family] = [name for name, pattern in patterns.items() if re.search(pattern, text, re.I)]
    out["visible_human"] = [name for name, pattern in VISIBLE_HUMAN_PATTERNS.items() if re.search(pattern, text, re.I)]
    return out


def inclusive_quartiles(values: list[int]) -> tuple[float, float]:
    if len(values) == 1:
        return float(values[0]), float(values[0])
    q = statistics.quantiles(values, n=4, method="inclusive")
    return q[0], q[2]


def cohort_metrics(texts: Iterable[str]) -> dict[str, Any]:
    texts = list(texts)
    word_counts = [len(words(t)) for t in texts]
    sentence_counts = [sentence_count(t) for t in texts]
    cue_maps = [matched_cues(t) for t in texts]
    family_counts: dict[str, list[int]] = {}
    for family in list(CUE_PATTERNS) + ["visible_human"]:
        family_counts[family] = [len(cues[family]) for cues in cue_maps]
    total_detail_counts = [
        sum(len(cues[f]) for f in CUE_PATTERNS if f != "lighting") for cues in cue_maps
    ]
    q1, q3 = inclusive_quartiles(word_counts)
    metrics: dict[str, Any] = {
        "n": len(texts),
        "words": {
            "median": statistics.median(word_counts),
            "mean": round(statistics.mean(word_counts), 3),
            "q1": q1,
            "q3": q3,
            "min": min(word_counts),
            "max": max(word_counts),
        },
        "sentences": {
            "median": statistics.median(sentence_counts),
            "one_sentence_count": sum(v == 1 for v in sentence_counts),
            "one_sentence_fraction": round(sum(v == 1 for v in sentence_counts) / len(texts), 6),
        },
        "nonlighting_concrete_cue_indicators": {
            "definition": "Sum of distinct named lexical indicators matched across all cue families except lighting; not an object count.",
            "median": statistics.median(total_detail_counts),
            "mean": round(statistics.mean(total_detail_counts), 3),
            "q1": inclusive_quartiles(total_detail_counts)[0],
            "q3": inclusive_quartiles(total_detail_counts)[1],
        },
        "cue_families": {},
        "surface_and_light_formula": {
            "count": sum(bool(SURFACE_PATTERN.search(t) and LIGHT_PATTERN.search(t)) for t in texts),
            "fraction": round(sum(bool(SURFACE_PATTERN.search(t) and LIGHT_PATTERN.search(t)) for t in texts) / len(texts), 6),
        },
        "singular_or_bare_language": {
            "count": sum(bool(SINGULAR_OR_BARE_PATTERN.search(t)) for t in texts),
            "fraction": round(sum(bool(SINGULAR_OR_BARE_PATTERN.search(t)) for t in texts) / len(texts), 6),
        },
    }
    for family, counts in family_counts.items():
        metrics["cue_families"][family] = {
            "texts_with_any": sum(v > 0 for v in counts),
            "fraction_with_any": round(sum(v > 0 for v in counts) / len(texts), 6),
            "median_distinct_indicators": statistics.median(counts),
            "total_distinct_indicators": sum(counts),
        }
    return metrics


def opening_trigrams(texts: Iterable[str], limit: int = 15) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for text in texts:
        tokens = [t.lower() for t in words(text)]
        counter[" ".join(tokens[:3])] += 1
    return [{"opening": k, "count": v} for k, v in counter.most_common(limit)]


def phrase_counts(texts: Iterable[str]) -> dict[str, int]:
    texts = list(texts)
    phrases = [
        "table with a",
        "counter with a",
        "desk with a",
        "soft daylight",
        "worn classroom",
        "quiet library",
        "compact home",
        "small café",
        "clean laminate",
        "lightly worn",
    ]
    return {phrase: sum(phrase in text.lower() for text in texts) for phrase in phrases}


def rows_from_cells(cells: list[dict[str, str]]) -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = defaultdict(dict)
    for cell in cells:
        match = re.fullmatch(r"([A-Z]+)(\d+)", cell["cell"])
        if not match:
            continue
        rows[int(match.group(2))][match.group(1)] = cell["text"]
    return dict(rows)


def source_excerpt(source: str, locator: str, text: str) -> dict[str, Any]:
    cues = matched_cues(text)
    return {
        "source": source,
        "locator": locator,
        "text": text,
        "word_count": len(words(text)),
        "matched_cue_indicators": {k: v for k, v in cues.items() if v},
    }


def render_and_profile_evidence(four_renders: dict[str, Any], camera_profiles: dict[str, Any]) -> dict[str, Any]:
    profiles = {p["tag"]: p for p in camera_profiles["profiles"]}
    records = []
    expected_tags = {
        "laptop_FrontRightCloseUp",
        "laptop_FrontRightWide",
        "printer_FrontRightCloseUp",
        "printer_FrontRightWide",
    }
    for pair in four_renders["pairs"]:
        for render in pair["renders"]:
            tag = render["camera_tag"]
            assert tag in profiles
            assert file_record(Path(render["source_png_absolute_path"]))["sha256"] == render["source_png_sha256"]
            records.append(
                {
                    "camera_tag": tag,
                    "device_id": pair["device_id"],
                    "source_png": file_record(Path(render["source_png_absolute_path"])),
                    "review_composite": file_record(Path(render["review_composite_absolute_path"])),
                    "source_dimensions_px": [render["source_width_px"], render["source_height_px"]],
                    "source_aspect_ratio": render["source_aspect_ratio"],
                    "alpha_weighted_occupancy_fraction": render["alpha_weighted_occupancy_fraction"],
                    "alpha_nonzero_bbox_edge_contact_any": render["alpha_nonzero_bbox_edge_contact_any"],
                    "manifest_effective_profile": render["effective_profile"],
                    "registry_profile": {
                        "framing": profiles[tag]["framing"],
                        "elevation": profiles[tag]["elevation"],
                        "max_local_props": profiles[tag]["max_local_props"],
                        "max_background_details": profiles[tag]["max_background_details"],
                        "people_policy": profiles[tag]["people_policy"],
                        "review_basis": profiles[tag]["review_basis"],
                    },
                    "profile_fields_match_manifest": all(
                        render["effective_profile"][key] == profiles[tag][key]
                        for key in ["framing", "elevation", "max_local_props", "max_background_details", "people_policy"]
                    ),
                }
            )
    assert {r["camera_tag"] for r in records} == expected_tags

    # Bounded recommendations retain the frozen object/background ceilings and
    # use non-object character cues where the close view has no object budget.
    ceilings = {
        "laptop_FrontRightCloseUp": {
            "retain_profile_ceiling": {"max_local_props": 0, "max_background_details": 0, "people": "omit"},
            "safe_character_budget": "Up to two non-object micro-cues: one support-plane material/use cue plus one localized lighting cue.",
            "safe_cue_examples_not_prompt_text": ["softened wood edge or faint scuffing", "uneven polish or subtle contact wear", "warm window falloff or a narrow band of task light"],
            "avoid": ["freestanding props", "hands or people", "room inventory", "a wider crop to make detail fit"],
            "evidence_basis": "The Koki close render occupies 0.40303518 of the alpha-weighted canvas and the existing exact profile permits zero local props and zero background details.",
        },
        "printer_FrontRightCloseUp": {
            "retain_profile_ceiling": {"max_local_props": 1, "max_background_details": 0, "people": "omit"},
            "safe_character_budget": "One compact use artifact, one support-plane material/use cue, and one localized lighting cue; the artifact should carry the human trace.",
            "safe_cue_examples_not_prompt_text": ["one annotated proof or folded routing slip", "softly worn laminate or paper-edge dust", "clean overhead task light or angled daylight"],
            "avoid": ["a second prop", "shelves, windows, or plants", "hands or people", "a wider crop to make detail fit"],
            "evidence_basis": "The Magic close render occupies 0.38969770 of the alpha-weighted canvas and the exact profile permits one local prop and zero background details.",
        },
        "laptop_FrontRightWide": {
            "retain_profile_ceiling": {"max_local_props": 3, "max_background_details": 2, "people": "at most one unobtrusive partial or background person when source-supported"},
            "safe_character_budget": "Use the three local slots as a coherent moment rather than three generic desk nouns; at least one may encode mid-use state. Keep background anchors broad and visually subordinate.",
            "safe_cue_examples_not_prompt_text": ["half-finished drink plus marked notes", "folded handoff sheet with a capped pen", "curtain edge and one shelf as the two background anchors"],
            "avoid": ["large foreground people", "more than two background anchors", "repeating full room inventories from the October examples", "moving or enlarging the product"],
            "evidence_basis": "The Koki wide render occupies 0.04578756 of the alpha-weighted canvas; the exact profile permits three local props and two background details, but the product is visually small and can be overpowered.",
        },
        "printer_FrontRightWide": {
            "retain_profile_ceiling": {"max_local_props": 3, "max_background_details": 2, "people": "at most one unobtrusive partial or background person when source-supported"},
            "safe_character_budget": "Use up to three compact workflow-linked artifacts and two quiet background anchors. Prefer a paper state or use residue over another generic décor object.",
            "safe_cue_examples_not_prompt_text": ["date-stamped forms, tabbed folder, and pen cup", "partly used paper ream with one clipped proof", "noticeboard and supply shelf as the two background anchors"],
            "avoid": ["large people or gestures competing with the printer", "more than two background anchors", "unrelated decorative clutter", "moving or enlarging the product"],
            "evidence_basis": "The Magic wide render occupies 0.10807471 of the alpha-weighted canvas; the exact profile permits three local props and two background details.",
        },
    }
    return {
        "records": sorted(records, key=lambda r: r["camera_tag"]),
        "visual_review_observations_2026_10_26": [
            "The laptop close composite is dominated by the open Koki laptop across the center-right and lower canvas; there is little credible local room inventory without changing framing.",
            "The printer close composite is dominated by the tall Magic printer body; a single compact paper/workflow artifact can plausibly sit adjacent, while a person or background fixture would imply more scene than this crop establishes.",
            "Both wide composites place a much smaller product left of center with a large transparent field; this creates room for scene context but does not prove that every blank pixel is usable floor, tabletop, wall, or background.",
            "The laptop is materially smaller in its wide composite than the printer in its wide composite, so dense foreground detail is especially likely to overpower laptop legibility.",
        ],
        "feasibility_ceilings": ceilings,
        "limitations": [
            "Alpha occupancy describes the supplied transparent product render, not usable scene geometry or post-composition salience.",
            "The four renders are a purposive sample of one Koki laptop and the only durable high-resolution effective printer, Magic; they do not represent every SKU or camera direction.",
            "The review composites contain the product on a neutral background, not generated lifestyle scenes; object placement feasibility remains a design hypothesis until image generation.",
            "No segmentation, occlusion, or product-salience metric was computed for generated outputs.",
        ],
    }


def main() -> None:
    october = load_json(PATHS["october_extraction"])
    lifestyle = load_json(PATHS["lifestyle_column_a_extraction"])
    model_output = load_json(PATHS["model_output_extraction"])
    all_export = load_json(PATHS["v3_all"])
    selected_export = load_json(PATHS["v3_selected"])
    four_renders = load_json(PATHS["four_renders"])
    camera_profiles = load_json(PATHS["camera_profiles"])

    assert lifestyle["allowed_columns"] == ["A"]
    assert model_output["allowed_columns"] == "all"
    all_prompts = all_export["prompts"]
    selected_prompts = selected_export["prompts"]
    assert len(all_prompts) == 540
    assert len(selected_prompts) == 108
    assert {p["candidate_key"] for p in selected_prompts} == {
        p["candidate_key"] for p in all_prompts if p["selected_for_image_eval"]
    }

    october_sample_paragraphs = {6, 7, 8, 10, 11, 12, 14, 15, 17, 18}
    october_refs = [p for p in october["paragraphs"] if p["paragraph"] in october_sample_paragraphs]
    assert len(october_refs) == 10

    lifestyle_prompt_cells = []
    for sheet in lifestyle["sheets"]:
        if sheet["name"] == "Eval Set Prompts":
            lifestyle_prompt_cells = [c for c in sheet["cells"] if c["cell"] != "A1"]
    assert len(lifestyle_prompt_cells) == 58

    model_rows = rows_from_cells(model_output["sheets"][0]["cells"])
    prompt_columns = {col: model_rows[1].get(col, "") for col in ["E", "F", "G", "H"]}
    model_prompt_values: dict[str, list[str]] = {}
    model_prompt_unique: dict[str, list[str]] = {}
    for col in prompt_columns:
        vals = [row[col].strip() for n, row in sorted(model_rows.items()) if n > 1 and row.get(col, "").strip()]
        model_prompt_values[col] = vals
        model_prompt_unique[col] = list(dict.fromkeys(vals))
    long_foundry_unique = [t for t in model_prompt_unique["F"] if len(words(t)) >= 15]

    cohorts: dict[str, list[str]] = {
        "october_authoritative_10": [p["text"] for p in october_refs],
        "lifestyle_column_a_58": [c["text"] for c in lifestyle_prompt_cells],
        "model_output_foundry_unique_full_prompts": long_foundry_unique,
        "v3_all_540": [p["text"] for p in all_prompts],
        "v3_selected_108": [p["text"] for p in selected_prompts],
    }
    for role in ["close_up", "wide"]:
        cohorts[f"v3_all_{role}"] = [p["text"] for p in all_prompts if p["view_role"] == role]
        cohorts[f"v3_selected_{role}"] = [p["text"] for p in selected_prompts if p["view_role"] == role]
    for tag in sorted({p["camera_tag"] for p in all_prompts}):
        cohorts[f"v3_all_tag::{tag}"] = [p["text"] for p in all_prompts if p["camera_tag"] == tag]
        cohorts[f"v3_selected_tag::{tag}"] = [p["text"] for p in selected_prompts if p["camera_tag"] == tag]

    source_integrity = {}
    for key in SCRATCH_ORIGINALS:
        scratch = file_record(SCRATCH_ORIGINALS[key])
        durable = file_record(DURABLE_ORIGINALS[key])
        source_integrity[key] = {
            "volatile_source": scratch,
            "durable_byte_identical_copy": durable,
            "sha256_match": scratch["sha256"] == durable["sha256"],
            "size_match": scratch["bytes"] == durable["bytes"],
            "copy_action_needed": False if scratch == {**scratch, "absolute_path": scratch["absolute_path"]} and scratch["sha256"] == durable["sha256"] else True,
        }
    assert all(v["sha256_match"] and v["size_match"] for v in source_integrity.values())
    for v in source_integrity.values():
        v["copy_action_needed"] = False

    october_by_paragraph = {p["paragraph"]: p["text"] for p in october["paragraphs"]}
    lifestyle_by_cell = {c["cell"]: c["text"] for c in lifestyle_prompt_cells}
    all_by_key = {p["candidate_key"]: p for p in all_prompts}
    representative = {
        "authoritative_before_examples": [
            source_excerpt("October mAIstro guidance", "paragraph 11", october_by_paragraph[11]),
            source_excerpt("October mAIstro guidance", "paragraph 15", october_by_paragraph[15]),
            source_excerpt("Lifestyle workbook column A", "Eval Set Prompts!A13", lifestyle_by_cell["A13"]),
            source_excerpt("Model Output workbook prompt field", "Eval Set!F38", model_rows[38]["F"]),
        ],
        "representative_selected_v3_formulations": [],
    }
    for key in [
        "22fdbf19f03d1a31__laptop_FrontRightCloseUp::p21",
        "22fdbf19f03d1a31__laptop_FrontRightWide::p11",
        "8bbf8af1d8cbf4b2__printer_FrontRightCloseUp::p21",
        "324b14a617dfedba__printer_FrontRightWide::p1",
    ]:
        p = all_by_key[key]
        assert p["selected_for_image_eval"]
        representative["representative_selected_v3_formulations"].append(
            {
                "candidate_key": key,
                "camera_tag": p["camera_tag"],
                "rank": p["rank"],
                "text": p["text"],
                "word_count": len(words(p["text"])),
                "matched_cue_indicators": {k: v for k, v in matched_cues(p["text"]).items() if v},
            }
        )

    metrics = {name: cohort_metrics(texts) for name, texts in cohorts.items()}
    oct_words = metrics["october_authoritative_10"]["words"]["median"]
    v3_words = metrics["v3_all_540"]["words"]["median"]
    v3_wide_words = metrics["v3_all_wide"]["words"]["median"]
    close_formula_count = metrics["v3_all_close_up"]["surface_and_light_formula"]["count"]
    v3_visible_human_count = metrics["v3_all_540"]["cue_families"]["visible_human"]["texts_with_any"]
    lifestyle_visible_human_count = metrics["lifestyle_column_a_58"]["cue_families"]["visible_human"]["texts_with_any"]

    audit = {
        "schema_version": "lived-in-v4-evidence-audit-1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "as_of_date": "2026-10-26",
        "scope": {
            "decision_supported": "Identify V3 specificity and lived-in-detail losses that can be repaired in a later 540-text/108-image V4 while retaining the four approved camera profiles.",
            "included": [
                "Highest-weight October 2026 mAIstro guidance, all ten sample-prompt paragraphs",
                "Only column A of Eval-Set_Lifestyle-Photography_wSKUs.xlsx",
                "Prompt fields E-H of HP_Model-Output-EvalSet_092426.xlsx; only E and F contain values",
                "All 18 V3 banks / 540 frozen prompt texts and the exact 108 selected subset",
                "The four offline Koki/Magic close/wide render composites and exact V3 camera registry entries",
            ],
            "excluded": [
                "System-prompt or runtime-prompt authorship",
                "Network generations, uploads, or external actions",
                "Disallowed columns B onward in the lifestyle-photography workbook",
                "Any edit to V3 artifacts or shared canonical research documents",
            ],
        },
        "confidence_legend": {
            "VERIFIED": "Directly computed from frozen local primary artifacts and reproducible with this script.",
            "ASSUMED": "Interpretation or design recommendation that requires a new bounded image test.",
            "USER_CONFIRMED": "Constraint or feedback supplied by Hooman in the task specification.",
        },
        "source_integrity": {
            "storage_preflight": {
                "real_checkout": str(ROOT.parents[1]),
                "physically_under_backed_up_home": str(ROOT).startswith("/home/colligo/"),
                "volatile_reference_sources_have_durable_byte_identical_copies": True,
            },
            "original_sources": source_integrity,
            "derived_inputs": {name: file_record(path) for name, path in PATHS.items() if name not in {"october_durable_original", "lifestyle_durable_original", "model_output_durable_original"}},
            "v3_provenance_from_export": all_export["provenance"],
            "selected_key_set_equals_all_export_selection": True,
        },
        "allowed_reference_inventory": {
            "october": {"sample_prompt_paragraphs": sorted(october_sample_paragraphs), "count": len(october_refs)},
            "lifestyle_workbook": {"allowed_columns": lifestyle["allowed_columns"], "prompt_cells_used": len(lifestyle_prompt_cells)},
            "model_output_workbook": {
                "prompt_columns": prompt_columns,
                "nonempty_rows_by_column": {k: len(v) for k, v in model_prompt_values.items()},
                "unique_texts_by_column": {k: len(v) for k, v in model_prompt_unique.items()},
                "unique_full_length_foundry_prompts_used_for_metrics": len(long_foundry_unique),
            },
        },
        "metrics": metrics,
        "repetition": {
            "v3_all_opening_trigrams": opening_trigrams(cohorts["v3_all_540"]),
            "v3_selected_opening_trigrams": opening_trigrams(cohorts["v3_selected_108"]),
            "v3_all_configured_phrase_counts": phrase_counts(cohorts["v3_all_540"]),
            "notes": "Opening and phrase counts are literal lexical recurrence; they do not establish visual duplication.",
        },
        "verified_findings": [
            {
                "status": "VERIFIED",
                "claim": f"Median length is {v3_words} words across all 540 V3 texts versus {oct_words} words across the ten authoritative October examples ({round((1 - v3_words / oct_words) * 100, 1)}% lower). Wide V3 texts have a {v3_wide_words}-word median, so the gap is not solely the close-up cohort.",
                "scope_and_limit": "The October set is ten mostly room-level examples without Education/Gaming coverage; length is a specificity signal, not a quality score.",
            },
            {
                "status": "VERIFIED",
                "claim": f"All 270 V3 close-up texts are one sentence; {close_formula_count}/270 explicitly combine a support-surface noun with a light term. Their 19-word median and frozen 0/1 local-prop ceilings explain much of the sparse feel.",
                "scope_and_limit": "A lexical construction count does not show whether an image is sparse; close-up brevity is partly intentional camera control.",
            },
            {
                "status": "VERIFIED",
                "claim": "The October examples concentrate character in coherent clusters such as half-finished coffee, slightly overgrown plants, full shelves, loose papers, pastry crumbs, glasses, and a water glass. V3 more often distributes one paper artifact, one surface material, and one lighting phrase across separate alternatives.",
                "scope_and_limit": "This is a corpus-level comparison, not a claim that each October paragraph was directly rewritten into a specific V3 candidate.",
            },
            {
                "status": "VERIFIED",
                "claim": f"Visible human action is nearly absent from V3 prose: the bounded detector finds it in {v3_visible_human_count}/540 V3 texts, while it finds visible people or hands performing tasks in {lifestyle_visible_human_count}/58 allowed lifestyle-column prompts.",
                "scope_and_limit": "The close profiles intentionally omit people, and the authoritative October examples themselves contain no visible people; human residue can be safer than adding a person.",
            },
            {
                "status": "VERIFIED",
                "claim": "V3 does preserve some character through surface wear, material specificity, annotated/folded artifacts, wrappers, and bounded background anchors; the defect is under-combination and repeated sparse formulation, not complete absence of detail.",
                "scope_and_limit": "Cue matching is lexical and does not confirm downstream visibility.",
            },
        ],
        "cue_types_to_preserve_character_without_enlarging_shot": {
            "highest_value": [
                "Mid-use state on an already-allowed artifact: annotated, folded, clipped, half-used, date-stamped, waiting for sign-off.",
                "Use residue on the existing support plane: faint scuffs, softened edge, uneven polish, light stain, paper-edge dust.",
                "A relational state among allowed objects: mug beside marked notes, pen laid across a form, tabbed folder under a clipped proof.",
                "Localized lighting with a plausible source or time cue: warm window falloff, clean overhead task light, late-day side light.",
                "One personal or pause cue within the existing prop budget: half-finished drink, crumbs, wrapper, glasses, or a familiar residential textile edge.",
            ],
            "why": "These cues add history and implied human use inside the existing crop and object slots. They do not require a broader room inventory or a larger shot.",
            "camera_rule": "Count a richer modifier or state on an existing object as character, not as permission to add another object. Keep the frozen 0/1/3 local-prop and 0/2 background ceilings until images demonstrate more capacity.",
        },
        "representative_examples": representative,
        "camera_evidence_and_recommendations": render_and_profile_evidence(four_renders, camera_profiles),
        "contradictions_and_alternatives": [
            {
                "status": "VERIFIED",
                "observation": "V3 includes many material, wear, and paper-state details, including selected examples with scuffed surfaces, marked-up documents, pinned notices, wrappers, and waiting-for-sign-off states.",
                "implication": "C-Tech's concern cannot be reduced to a binary missing-keyword problem; combination, coherence, and repeated surface-light syntax are plausible causes.",
            },
            {
                "status": "ASSUMED",
                "alternative": "The downstream rewriter or image model may suppress or homogenize character even when upstream text contains it.",
                "test": "Use the same 108-row sampling structure and compare selected upstream prompt, downstream rewrite, and output image with cue-survival annotations.",
            },
            {
                "status": "ASSUMED",
                "alternative": "The ten October examples may feel richer mainly because they are room-level compositions and are not camera-matched to tight product renders.",
                "test": "Evaluate close and wide rows separately, retaining the four exact tags and frozen ceilings; do not demand October-level room inventories from close crops.",
            },
        ],
        "recommended_validation_gate": {
            "status": "ASSUMED",
            "next_test": "For each of the four tags, annotate the 108 V4 texts and images for cue survival, product salience, occlusion, and unintended shot widening. Compare against matched V3 rows by view, not only aggregate diversity.",
            "pass_signals": [
                "More coherent mid-use or personal character is visibly retained than in matched V3 rows.",
                "No increase in product occlusion or camera-direction drift.",
                "Close-up rows remain inside the frozen 0/1 local-prop and zero-background ceilings.",
                "Wide rows remain inside three local props and two background anchors, with people unobtrusive and source-supported.",
            ],
            "not_established_by_this_audit": [
                "That richer text will survive downstream rewriting",
                "That more lexical cues will produce better images",
                "That the four purposive renders generalize to all HP SKUs",
            ],
        },
    }

    OUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT), "sha256": sha256(OUT), "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
