#!/usr/bin/env python3
"""Build the v2 placement-judge human-evidence audit from raw submissions."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE_ROOT = ROOT / "judge/placement/data/sources"
OUT = ROOT / "judge/placement/versions/v2/data/human_evidence.json"
INVENTORY = ROOT / "judge/placement/data/annotation_inventory.json"
V1_SPLIT = ROOT / "judge/placement/data/split.json"

REPORTS = {
    "hp16-p0-ablation-full32-20261104T182602Z-eval": {
        "title": "HP16 P0 controlled ablation, V6 user prompts",
        "stage": "scene_generation_output",
        "stage_confidence": "high",
        "stage_basis": "Direct one-call generation.png model outputs; no downstream relight asset is present in the report.",
    },
    "hp16-v6prompt-v14-e2e32-20261103T200020Z": {
        "title": "HP16, V6 user prompts: V13 vs V14",
        "stage": "scene_generation_output",
        "stage_confidence": "high",
        "stage_basis": "Report metadata describes one image call and model_output assets. The filename final denotes the report's image-call output, not a downstream relight.",
    },
    "hp16-v6prompt-v15-vs-v151-e2e32-20261103T232957Z": {
        "title": "HP16, V6 user prompts: V15 vs V15.1",
        "stage": "scene_generation_output",
        "stage_confidence": "high",
        "stage_basis": "Report metadata describes one image call and model_output assets. The filename final denotes the report's image-call output, not a downstream relight.",
    },
    "hp-v13-v14-laptop-printer30-20261103T015107Z-viewer": {
        "title": "HP V13 vs V14 — laptop + printer 30 input / final comparison",
        "stage": "report_final_model_output_stage_unverified",
        "stage_confidence": "medium",
        "stage_basis": "Assets are labeled final/model_output and V14 lineage points to the scene generator, but the supplied report has no endpoint stage manifest and V13 provenance is only a run name.",
    },
}

LATEST_LABELS = [
    (25, "v14", "printer", "printer/table misaligned"),
    (12, "v13", "printer", "printer should wall-align/towardside notmiddle"),
    (9, "v14", "laptop", "laptop too far chair + blocked access"),
    (29, "v13", "laptop", "laptop too far chair though narrative appealing"),
]

LATEST_ASSET_VERIFICATION = {
    (25, "v14"): {
        "sha256": "4ceb50f8a4605789bb2c5437de503899c1e11b7c0b81a85a8978e7764862c4b4",
        "prior_quote": "Product angle does not align with table angle.",
        "prior_attribution": "comparison_set_ambiguous",
    },
    (12, "v13"): {
        "sha256": "bcd88892c5a5b416f5becca8e4102de1ebae1337462031e1a9d27a8b47100a98",
        "prior_quote": "Hallucinations and scene alignment should match product angle",
        "prior_attribution": "comparison_set_ambiguous",
    },
    (9, "v14"): {
        "sha256": "53618cc0df28274b5ae69596d09ba5f4f145b7e1e35f7d0e1c5164b4694b896b",
        "prior_quote": "Product needs to be closer to the table edge.",
        "prior_attribution": "exact_variant_single_output_row",
    },
    (29, "v13"): {
        "sha256": "b465f94249d56d50fa5a2404fb925bb69d8ae559e2e264b2172881fa69d602eb",
        "prior_quote": "v13 - product too far from the table edge closer to the chair.",
        "prior_attribution": "exact_variant_explicit",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_variant(label: str, position: int) -> str:
    lower = label.lower()
    if "v15.1" in lower:
        return "v151"
    for name in ("v13", "v14", "v15"):
        if name in lower:
            return name
    return f"p{position + 1}"


def split_exact_clauses(text: str) -> list[str]:
    parts = re.split(r"(?:\r?\n)+|(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def classify_clause(quote: str) -> tuple[str, bool]:
    q = quote.lower()
    if re.fullmatch(r"(?:good|ok)", q.strip()):
        return "broad_positive_not_placement_groundtruth", False
    if "product placement & scale" in q:
        if any(term in q for term in ("closer", "middle", "center", "realistic", "individual")):
            return "placement_defect_with_detail", True
        return "placement_dimension_flag_without_detail", True
    if any(
        term in q
        for term in (
            "closer to the edge",
            "closer to the table edge",
            "closer to the back edge",
            "closer to the edge/chair",
            "closer to the edge near the chair",
            "too far from the table edge",
            "product angle does not align",
            "angle of table should align",
            "table angle should align",
            "scene alignment should match product angle",
            "table position related to product angle",
            "scene should be oriented in the same angle",
            "product is floating",
            "no weight",
            "table placement",
            "desk placement",
            "table location not realistic",
            "table in middle of room",
            "table in the middle of the room",
            "printer in the middle of the table",
            "furniture too close",
            "ottoman too close",
            "props on the table are facing the wrong direction",
            "props not oriented in the right direction",
            "props need to be facing and surrounding",
            "props on table do not appear to be connected",
        )
    ):
        return "placement_or_usability_defect_with_detail", True
    if "placement issues" in q:
        return "placement_defect_without_detail", True
    if q.startswith("ok -"):
        return "mixed_positive_and_scene_context_not_placement_pass", False
    if any(term in q for term in ("appears to be on an individuals desk", "printers should not be in a cafe setting")):
        return "placement_adjacent_scenario_suitability", True
    return "nonplacement_or_broad_context", False


def attribution_for_clause(
    quote: str,
    displayed_variants: list[str],
    forced_variant: str | None = None,
) -> dict:
    if forced_variant:
        return {
            "type": "exact_variant",
            "variants": [forced_variant],
            "basis": "The per-variant question_comments field names the target variant.",
        }
    mentioned = []
    for variant in ("v13", "v14", "v15", "v151"):
        if re.search(rf"\b{re.escape(variant)}\b", quote.lower()):
            mentioned.append(variant)
    if mentioned:
        return {
            "type": "exact_variant" if len(mentioned) == 1 else "exact_multiple_variants",
            "variants": mentioned,
            "basis": "The exact clause explicitly names the variant(s).",
        }
    if len(displayed_variants) == 1:
        return {
            "type": "exact_variant",
            "variants": displayed_variants,
            "basis": "Only one output was displayed on this annotation row.",
        }
    return {
        "type": "comparison_set_ambiguous",
        "variants": displayed_variants,
        "basis": "The clause does not name a variant and multiple outputs were displayed.",
    }


def main() -> None:
    inventory = json.loads(INVENTORY.read_text())
    inventory_report = {item["report_id"]: item for item in inventory["reports"]}
    annotation_records = []
    structured_votes = []
    text_annotations = []
    quote_clauses = []
    source_files = []
    answer_distributions: dict[str, Counter] = defaultdict(Counter)

    for report_id, report_meta in REPORTS.items():
        annotation_dir = SOURCE_ROOT / report_id / "annotations"
        for annotation_path in sorted(annotation_dir.glob("*.json")):
            raw = json.loads(annotation_path.read_text())
            reviewer = raw.get("reviewer", {})
            reviewer_id = reviewer.get("ldap") or raw.get("ldap")
            source_files.append(
                {
                    "report_id": report_id,
                    "annotation_file": str(annotation_path),
                    "sha256": sha256(annotation_path),
                    "reviewer_ldap": reviewer_id,
                    "submitted_at": raw.get("submitted_at"),
                }
            )
            for row_position, row in enumerate(raw["rows"]):
                variants = []
                for position, asset in enumerate(row.get("comparison_assets", [])):
                    variants.append(
                        {
                            "variant": normalize_variant(asset["label"], position),
                            "display_label": asset["label"],
                            "image_url": asset["image_src"],
                        }
                    )
                displayed = [variant["variant"] for variant in variants]
                row_base = {
                    "report_id": report_id,
                    "reviewer_ldap": reviewer_id,
                    "submitted_at": raw.get("submitted_at"),
                    "row_idx": row["row_idx"],
                    "row_key": row["key"],
                    "stage": report_meta["stage"],
                    "stage_confidence": report_meta["stage_confidence"],
                    "displayed_variants": variants,
                }
                annotation_records.append(
                    {
                        **row_base,
                        "complete": row.get("complete"),
                        "answers": row.get("answers", {}),
                        "comment_exact": row.get("comment", ""),
                        "question_comments_exact": row.get("question_comments", {}),
                        "source_json_pointer": f"$.rows[{row_position}]",
                    }
                )
                for question_id, answer in row.get("answers", {}).items():
                    answer_distributions[f"{report_id}:{question_id}"][answer] += 1
                    structured_votes.append(
                        {
                            **{key: row_base[key] for key in ("report_id", "reviewer_ldap", "row_idx", "row_key", "stage")},
                            "question_id": question_id,
                            "answer_exact": answer,
                            "placement_groundtruth": False,
                            "interpretation_guard": "A pairwise/best-of-four/broad-dimension vote is not an absolute placement pass or fail.",
                            "source_json_pointer": f"$.rows[{row_position}].answers.{question_id}",
                        }
                    )

                top_comment = row.get("comment", "")
                if top_comment:
                    text_id = f"{report_id}:{reviewer_id}:row{row['row_idx']:02d}:comment"
                    text_annotations.append(
                        {
                            **row_base,
                            "text_id": text_id,
                            "field": "comment",
                            "exact_quote": top_comment,
                            "source_json_pointer": f"$.rows[{row_position}].comment",
                        }
                    )
                    for clause_position, clause in enumerate(split_exact_clauses(top_comment)):
                        category, usable = classify_clause(clause)
                        quote_clauses.append(
                            {
                                **{key: row_base[key] for key in ("report_id", "reviewer_ldap", "row_idx", "row_key", "stage", "stage_confidence")},
                                "text_id": text_id,
                                "clause_index": clause_position,
                                "exact_quote": clause,
                                "category": category,
                                "placement_rubric_evidence": usable,
                                "attribution": attribution_for_clause(clause, displayed),
                                "source_json_pointer": f"$.rows[{row_position}].comment",
                            }
                        )

                for field, exact_quote in row.get("question_comments", {}).items():
                    forced = field.removesuffix("_comment")
                    text_id = f"{report_id}:{reviewer_id}:row{row['row_idx']:02d}:{field}"
                    text_annotations.append(
                        {
                            **row_base,
                            "text_id": text_id,
                            "field": f"question_comments.{field}",
                            "exact_quote": exact_quote,
                            "source_json_pointer": f"$.rows[{row_position}].question_comments.{field}",
                        }
                    )
                    for clause_position, clause in enumerate(split_exact_clauses(exact_quote)):
                        category, usable = classify_clause(clause)
                        quote_clauses.append(
                            {
                                **{key: row_base[key] for key in ("report_id", "reviewer_ldap", "row_idx", "row_key", "stage", "stage_confidence")},
                                "text_id": text_id,
                                "clause_index": clause_position,
                                "exact_quote": clause,
                                "category": category,
                                "placement_rubric_evidence": usable,
                                "attribution": attribution_for_clause(clause, displayed, forced),
                                "source_json_pointer": f"$.rows[{row_position}].question_comments.{field}",
                            }
                        )

    prior_split = json.loads(V1_SPLIT.read_text())
    latest_labels = []
    for row_idx, variant, product, label_paraphrase in LATEST_LABELS:
        verified = LATEST_ASSET_VERIFICATION[(row_idx, variant)]
        latest_labels.append(
            {
                "authority": "USER-CONFIRMED",
                "source": "latest user adjudication, represented by the normalized label paraphrase supplied in the task specification",
                "row_idx": row_idx,
                "variant": variant,
                "product_category": product,
                "verdict": "fail",
                "label_paraphrase": label_paraphrase,
                "label_text_status": "paraphrase_not_verbatim_quote",
                "attribution": "exact_variant",
                "stage": "report_final_model_output_stage_unverified",
                "stage_confidence": "medium",
                "stage_basis": "The exact gallery bytes match the older report originals, but the source report lacks a complete raw-PNG endpoint stage chain and V13 provenance is only a run name. A later regression manifest calling the assets scene_generation is not independent stage proof.",
                "source_asset_id": f"comparison-row-{row_idx:02d}-{variant}",
                "source_asset_sha256": verified["sha256"],
                "image_url": f"https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v1_20261104/gallery/assets/row_{row_idx:02d}/{variant}_final.png",
                "user_supplied_gallery_url": f"https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v1_20261104/gallery/assets/row_{row_idx:02d}/{variant}_final.png",
                "verified_report_public_url": f"https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp-v13-v14-laptop-printer30-20261103T015107Z-viewer/originals/{row_idx:02d}/{variant}_final.png",
                "gallery_byte_verification": {
                    "status": "verified",
                    "basis": "published_report.json records download_verified=true for this gallery object with the same SHA-256 as the preserved source asset.",
                    "published_report": "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/data/published_report.json",
                    "published_report_sha256": "e9f0ba61dc76cfebb17c9a119f2b580a8d8674663dd78987076fb28e94c450e8",
                },
                "prior_corroborating_annotation": {
                    "exact_quote": verified["prior_quote"],
                    "attribution": verified["prior_attribution"],
                    "authority": "older reviewer annotation; subordinate to the latest direct user adjudication",
                },
                "dataset_role": "latest_user_adjudication_distinct_from_prior_annotation_corpus",
                "image_level_holdout_independence": False,
                "independence_note": "This row/variant was present in the prior v1 pilot corpus; retain as the strongest adjudication, but do not claim it is an unseen image-level holdout.",
            }
        )

    category_counts = Counter(item["category"] for item in quote_clauses)
    attribution_counts = Counter(item["attribution"]["type"] for item in quote_clauses)
    top_comments = sum(1 for item in text_annotations if item["field"] == "comment")
    question_comments = len(text_annotations) - top_comments
    report_rows = sum(item["rows"] for item in inventory_report.values())
    report_summary = []
    for report_id, report_meta in REPORTS.items():
        inv = inventory_report[report_id]
        report_summary.append(
            {
                "report_id": report_id,
                "title": report_meta["title"],
                "report_rows": inv["rows"],
                "reviewer_submissions": len(inv["reviewers"]),
                "stage": report_meta["stage"],
                "stage_confidence": report_meta["stage_confidence"],
                "stage_basis": report_meta["stage_basis"],
                "source_data_file": inv["source_data_file"],
                "source_data_sha256": inv["source_sha256"],
            }
        )

    output = {
        "schema": "hp-placement-human-evidence-v2@1",
        "as_of_date": "2026-11-04",
        "scope": {
            "decision_supported": "Evidence input for placement judge v2 rubric and evaluation design.",
            "included": "Every raw row, structured answer, top-level comment, and per-variant question_comments value in the four supplied human-annotated reports, plus four newer direct user FAIL adjudications.",
            "excluded": "The printer guidance report is authored training/guidance material, not a human annotation submission.",
            "storage_preflight": "PASS: checkout resolves under backed-up /home/colligo/hs_scripts; /mnt/localssd was not used.",
        },
        "live_s3_annotation_check": {
            "checked_on": "2026-11-04 America/Los_Angeles",
            "method": "Read-only aws s3api list-objects-v2 on each included report's annotations/ prefix; no object was downloaded or overwritten.",
            "result": "MATCH: five live annotation objects have the same keys and byte sizes as the five preserved local files; no additional or newer reviewer object was present.",
            "objects": [
                {"report_id": "hp-v13-v14-laptop-printer30-20261103T015107Z-viewer", "key": "annotations/reviewer_0.json", "last_modified": "2026-11-03T17:21:01+00:00", "bytes": 38058},
                {"report_id": "hp16-v6prompt-v14-e2e32-20261103T200020Z", "key": "annotations/reviewer_0.json", "last_modified": "2026-11-04T00:00:22+00:00", "bytes": 31158},
                {"report_id": "hp16-v6prompt-v14-e2e32-20261103T200020Z", "key": "annotations/reviewer_1.json", "last_modified": "2026-11-04T00:45:18+00:00", "bytes": 37254},
                {"report_id": "hp16-v6prompt-v15-vs-v151-e2e32-20261103T232957Z", "key": "annotations/reviewer_0.json", "last_modified": "2026-11-03T23:42:48+00:00", "bytes": 32301},
                {"report_id": "hp16-p0-ablation-full32-20261104T182602Z-eval", "key": "annotations/reviewer_0.json", "last_modified": "2026-11-04T19:03:38+00:00", "bytes": 54785},
            ],
        },
        "summary": {
            "reports": len(REPORTS),
            "report_case_rows": report_rows,
            "reviewer_submissions": len(source_files),
            "reviewer_row_records": len(annotation_records),
            "structured_answers": len(structured_votes),
            "nonempty_top_level_comments": top_comments,
            "nonempty_per_variant_question_comments": question_comments,
            "all_nonempty_text_annotations": len(text_annotations),
            "exact_quote_clauses": len(quote_clauses),
            "placement_rubric_evidence_clauses": sum(item["placement_rubric_evidence"] for item in quote_clauses),
            "latest_direct_user_fail_labels": len(latest_labels),
            "correction_to_prior_inventory": "The prior inventory counted only 29 top-level comments. It omitted the 63 nonempty per-variant question_comments values in zperkins's HP16 V13-vs-V14 submission, including mixed multiline values. The complete raw-schema audit contains 92 nonempty text annotations before the four newer direct user labels.",
        },
        "evidence_rules": [
            "Structured best-of-four, overall-preference, fidelity, realism, lighting, and blue-element votes are preserved but never converted to placement pass/fail ground truth.",
            "Per-variant question_comments fields have exact variant attribution, but broad Good/OK text is not a placement pass unless the source explicitly says placement passed.",
            "An unqualified top-level comment on a two-output row has comparison-set-ambiguous attribution. A single-output row or an explicitly named variant has exact attribution.",
            "Mixed comments are split into exact quoted clauses; non-placement clauses remain present and separately classified.",
            "Empty comment fields are unlabeled, not passes.",
            "The four latest user FAIL adjudications are the strongest evidence and remain distinct from the older report corpus; their short descriptive labels are paraphrases, not verbatim user quotations.",
        ],
        "latest_user_adjudications": latest_labels,
        "split_transition": {
            "user_instruction": "Prior v1 held-out rows now serve as training evidence; latest user labels remain distinct.",
            "prior_v1_held_out_rows_now_training": prior_split["held_out_rows"],
            "prior_v1_held_out_case_ids_now_training": [
                item["id"] for item in prior_split["cases"] if item["split"] == "held_out"
            ],
            "leakage_guard": "Rows 9/v14, 12/v13, and 29/v13 overlap the latest adjudications, and row 25/v14 was prior development. These labels are suitable for adjudicated evaluation/regression checks, not for claiming unseen image-level generalization after rubric development uses the prior corpus.",
        },
        "reports": report_summary,
        "source_annotation_files": source_files,
        "answer_distributions": {
            key: dict(sorted(value.items())) for key, value in sorted(answer_distributions.items())
        },
        "annotation_records": annotation_records,
        "structured_votes": structured_votes,
        "text_annotations": text_annotations,
        "exact_quote_clauses": quote_clauses,
        "audit_distributions": {
            "clause_categories": dict(sorted(category_counts.items())),
            "attribution_types": dict(sorted(attribution_counts.items())),
        },
        "limitations": [
            "Only one report contains detailed free-text top-level comments; only one reviewer supplied the per-variant question_comments fields.",
            "Broad labels such as Product Placement & Scale identify a defective dimension but do not reveal the defect mechanism.",
            "The 30-row report's scene-generation stage is plausible but lacks a complete stage manifest; its exact quotes retain that uncertainty.",
            "The published-report manifest verifies gallery byte identity against the preserved source-asset hashes; that upload verification does not resolve the source report's incomplete pipeline-stage provenance.",
            "The annotation pool is purposive and cannot establish calibrated accuracy, prevalence, specificity, or production thresholds.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
