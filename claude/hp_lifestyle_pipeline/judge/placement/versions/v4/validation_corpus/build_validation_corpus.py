#!/usr/bin/env python3
"""Build a comment-grounded development corpus for placement-judge iteration.

This intentionally ignores FE Pass/Review/Fail button answers.  A free-text
"agree" is retained only as a relation to the exact frozen V2 judgment that
the reviewer saw; it is never promoted to an independent human verdict.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image


HERE = Path(__file__).resolve().parent
PIPELINE_ROOT = HERE.parents[4]
V3_DATA = PIPELINE_ROOT / "judge/placement/versions/v3/data"
COMMENT_INVENTORY = V3_DATA / "comment_inventory.json"
FEEDBACK_MANIFEST = V3_DATA / "feedback_20261105/manifest.json"


# Only conclusions stated directly in free text are represented here.  Button
# answers are deliberately unavailable to this map.  Qualifiers stay explicit
# so downstream policy owners can decide whether/how to map them.
DIRECT_LABELS: dict[str, dict[str, str]] = {
    "magic__printer_FrontCloseUp__p4": {
        "label": "pass",
        "qualifier": "placement_only_with_nonplacement_and_context_concerns",
        "trigger_quote": "This is a pass for the printer.",
    },
    "magic__printer_FrontCloseUp__p5": {
        "label": "fail",
        "qualifier": "unqualified",
        "trigger_quote": "this should be a fail",
    },
    "magic__printer_FrontWide__p2": {
        "label": "pass",
        "qualifier": "minor_adjustment_suggested",
        "trigger_quote": "this is a pass",
    },
    "cashmere__laptop_BackRightCloseUp__p5": {
        "label": "pass",
        "qualifier": "weak",
        "trigger_quote": "it might be a weak pass",
    },
    "cashmere__laptop_BackRightCloseUp__p6": {
        "label": "fail",
        "qualifier": "unqualified",
        "trigger_quote": "This is a fail.",
    },
    "cashmere__laptop_FrontLeftMedium__p6": {
        "label": "fail",
        "qualifier": "unqualified",
        "trigger_quote": "Thsi si a fail.",
    },
    "cashmere__laptop_FrontWide__p4": {
        "label": "fail",
        "qualifier": "unqualified",
        "trigger_quote": "fail.",
    },
    "elitebook__laptop_BackRightCloseUp__p5": {
        "label": "fail",
        "qualifier": "weak",
        "trigger_quote": "this is weak fail",
    },
    "elitebook__laptop_FrontLeftMedium__p5": {
        "label": "ambiguous",
        "qualifier": "insufficient_scene_clues",
        "trigger_quote": "Id say this is an ambiguous case.",
    },
    "elitebook__laptop_FrontLeftMedium__p6": {
        "label": "pass",
        "qualifier": "borderline",
        "trigger_quote": "I'd say this is border line pass.",
    },
}


RELATION_RE = re.compile(
    r"(?:"
    r"\b(?:i\s+)?(?:agree|agreed|ageed)"
    r"(?:(?:\s+(?:w\s+ith|with)\s+(?:your|yoru)\s+"
    r"(?:judg(?:e)?ment|comments?))|(?=[\s.!/]*$)|(?=[.!/]))"
    r"|\byour (?:comments?|feedback) (?:are |is )?(?:all )?(?:accurate|correct)\b"
    r")",
    re.IGNORECASE,
)


PURE_RELATION_RE = re.compile(
    r"^(?:i\s+)?(?:agree|agreed|ageed)"
    r"(?:\s+with\s+(?:your\s+)?(?:judg(?:e)?ment|comments?))?[\s.!/]*$",
    re.IGNORECASE,
)


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_comment(value: str) -> str:
    return " ".join(value.split())


def verified_image(asset_id: str, kind: str, data: dict[str, Any]) -> dict[str, Any]:
    path = Path(data["local_path"])
    if not path.is_file():
        raise FileNotFoundError(f"{asset_id}: missing {kind}: {path}")
    actual_sha = sha256_path(path)
    if actual_sha != data["sha256"]:
        raise ValueError(f"{asset_id}: {kind} SHA mismatch")
    if path.stat().st_size != data["bytes"]:
        raise ValueError(f"{asset_id}: {kind} byte-size mismatch")
    with Image.open(path) as image:
        width, height = image.size
        fmt = image.format
    if [width, height] != [data["width"], data["height"]]:
        raise ValueError(f"{asset_id}: {kind} dimension mismatch")
    return {
        "filename": data["filename"],
        "local_path": str(path),
        "sha256": actual_sha,
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "format": fmt,
        "s3_uri": data.get("s3_uri") or data.get("source_s3_uri"),
        "public_url": data.get("public_url") or data.get("source_public_url"),
        "verification": {
            "local_file_exists": True,
            "sha256_matches_frozen_mapping": True,
            "bytes_match_frozen_mapping": True,
            "dimensions_match_frozen_mapping": True,
        },
    }


def main() -> None:
    source = json.loads(COMMENT_INVENTORY.read_text())
    feedback_manifest = json.loads(FEEDBACK_MANIFEST.read_text())
    snapshot_by_family = {x["family"]: x for x in feedback_manifest}
    source_snapshot_by_family = {
        x["family"]: x for x in source["sources"]["selected_annotation_snapshots"]
    }
    native_rows_by_family: dict[str, dict[str, dict[str, Any]]] = {}

    for family, item in snapshot_by_family.items():
        path = Path(item["path"])
        if sha256_path(path) != item["sha256"]:
            raise ValueError(f"annotation snapshot hash mismatch: {family}")
        if source_snapshot_by_family[family]["sha256"] != item["sha256"]:
            raise ValueError(f"annotation provenance disagreement: {family}")
        native = json.loads(path.read_text())
        native_rows = {row["evalset_item_id"]: row for row in native["rows"]}
        if len(native_rows) != len(native["rows"]):
            raise ValueError(f"duplicate native annotation row IDs: {family}")
        native_rows_by_family[family] = native_rows

    records: list[dict[str, Any]] = []
    excluded_empty: list[str] = []
    evidence_counts: dict[str, int] = {}

    for item in source["records"]:
        asset_id = item["id"]
        comment = item["comments"]["row"] or ""
        clean_comment = normalized_comment(comment)
        native_row = native_rows_by_family[item["family"]].get(asset_id)
        if native_row is None:
            raise ValueError(f"{asset_id}: missing from native annotation snapshot")
        if (native_row.get("comment") or "") != comment:
            raise ValueError(f"{asset_id}: comment differs from native annotation snapshot")
        if sha256_text(comment) != item["comments"]["row_comment_sha256"]:
            raise ValueError(f"{asset_id}: comment SHA differs from frozen inventory")
        if native_row.get("key") != item["source_row_identity"]["key"]:
            raise ValueError(f"{asset_id}: native annotation key mismatch")
        if native_row.get("row_idx") != item["source_row_identity"]["row_idx"]:
            raise ValueError(f"{asset_id}: native annotation row index mismatch")
        if not clean_comment:
            excluded_empty.append(asset_id)
            continue
        if item["asset"]["image_stage"] != "scene_generation":
            raise ValueError(f"{asset_id}: image is not scene-generation output")
        if sha256_text(item["asset"]["scene_prompt"]) != item["asset"]["scene_prompt_sha256"]:
            raise ValueError(f"{asset_id}: scene-prompt SHA mismatch")

        direct = DIRECT_LABELS.get(asset_id)
        relation = bool(RELATION_RE.search(clean_comment))
        relation_only = bool(PURE_RELATION_RE.fullmatch(clean_comment))
        if direct:
            if direct["trigger_quote"].lower() not in clean_comment.lower():
                raise ValueError(f"{asset_id}: direct-label trigger no longer present")
            evidence_class = "direct_verdict_or_ambiguity_label"
        elif relation_only:
            evidence_class = "relational_agreement_only"
        elif relation:
            evidence_class = "relational_agreement_with_concrete_comment"
        else:
            evidence_class = "issue_or_assessment_only_no_direct_verdict"
        evidence_counts[evidence_class] = evidence_counts.get(evidence_class, 0) + 1

        if evidence_class == "direct_verdict_or_ambiguity_label":
            validation_roles = ["direct_free_text_outcome_development_check"]
        elif evidence_class == "issue_or_assessment_only_no_direct_verdict":
            validation_roles = ["comment_grounded_issue_detection_development_check"]
        elif evidence_class == "relational_agreement_with_concrete_comment":
            validation_roles = [
                "relational_consistency_development_check",
                "comment_grounded_issue_detection_development_check",
            ]
        else:
            validation_roles = ["relational_consistency_development_check"]

        prior_reference = None
        if relation:
            run = item["v2_actual_run"]
            judgment = run["judgment"]
            prior_reference = {
                "relation": "reviewer_comment_refers_to_displayed_frozen_v2_judgment",
                "recoverable": True,
                "independent_human_verdict_label": False,
                "v2_result_path": run["result_path"],
                "v2_result_sha256": run["result_sha256"],
                "v2_policy_version": judgment["policy_version"],
                "v2_verdict_reference_only": judgment["verdict"],
                "v2_natural_placement_score_reference_only": judgment[
                    "natural_placement_score"
                ],
                "v2_summary_reference_only": judgment["observation"]["summary"],
                "v2_verdict_reasons_reference_only": judgment["verdict_reasons"],
            }
            result_path = Path(run["result_path"])
            if sha256_path(result_path) != run["result_sha256"]:
                raise ValueError(f"{asset_id}: prior V2 result hash mismatch")

        generated = verified_image(
            asset_id, "generated scene", item["asset"]["generated_image"]
        )
        twin = verified_image(asset_id, "digital twin", item["asset"]["twin_image"])

        snapshot = source_snapshot_by_family[item["family"]]
        records.append(
            {
                "id": asset_id,
                "family": item["family"],
                "device": item["asset"]["device"],
                "device_type": item["asset"]["device_type"],
                "candidate_id": item["asset"]["candidate_id"],
                "camera": item["asset"]["view"],
                "image_stage": "scene_generation",
                "scene_prompt": item["asset"]["scene_prompt"],
                "scene_prompt_sha256": item["asset"]["scene_prompt_sha256"],
                "human_evidence": {
                    "comment_exact": comment,
                    "comment_normalized_for_display": clean_comment,
                    "comment_sha256": sha256_text(comment),
                    "evidence_class": evidence_class,
                    "validation_roles": validation_roles,
                    "direct_label": direct,
                    "prior_judge_relation": prior_reference,
                    "button_answer_used": False,
                    "annotation_snapshot": {
                        "family": item["family"],
                        "path": snapshot["path"],
                        "s3_uri": snapshot["s3_uri"],
                        "sha256": snapshot["sha256"],
                        "source_row_identity": item["source_row_identity"],
                    },
                },
                "assets": {
                    "generated_scene": generated,
                    "digital_twin_reference": twin,
                },
            }
        )

    unknown_direct_ids = sorted(set(DIRECT_LABELS) - {x["id"] for x in records})
    if unknown_direct_ids:
        raise ValueError(f"direct-label IDs not found: {unknown_direct_ids}")

    output = {
        "schema_version": "hp-natural-placement-comment-corpus-v4.1-1",
        "source_snapshots_retrieved_through_utc": max(
            x["retrieved_at"]
            for x in source["sources"]["selected_annotation_snapshots"]
        ),
        "status": "development_corpus_not_held_out_not_accuracy_estimate",
        "purpose": "Comment-grounded inventory for Natural Placement Judge V4.1 iteration.",
        "contracts": {
            "human_button_answers": "ignored_entirely",
            "direct_labels": (
                "Only verdict/ambiguity conclusions stated in free-text comments are labels."
            ),
            "issue_only_comments": (
                "Concrete observations without a direct verdict remain issue-only evidence."
            ),
            "agreement_comments": (
                "Agreement is relational to the exact frozen V2 result and is not an "
                "independent human verdict."
            ),
            "empty_comments": "excluded_not_treated_as_pass_or_ground_truth",
            "absent_rows": "excluded_not_inferred_reviewed",
            "image_stage": "scene_generation_only",
            "evaluation_claim": (
                "This corpus is development evidence and cannot support unbiased held-out "
                "accuracy claims."
            ),
        },
        "sources": {
            "comment_inventory": {
                "path": str(COMMENT_INVENTORY),
                "sha256": sha256_path(COMMENT_INVENTORY),
            },
            "feedback_manifest": {
                "path": str(FEEDBACK_MANIFEST),
                "sha256": sha256_path(FEEDBACK_MANIFEST),
            },
            "annotation_snapshots": source["sources"][
                "selected_annotation_snapshots"
            ],
            "asset_mapping": source["sources"]["v2_assets"],
            "prior_judge_runs_reference_only": source["sources"]["v2_actual_runs"],
        },
        "counts": {
            "persisted_annotation_rows": len(source["records"]),
            "included_nonempty_comment_rows": len(records),
            "excluded_empty_comment_rows": len(excluded_empty),
            "source_report_rows": source["counts"]["source_report_rows"],
            "rows_absent_from_annotation_snapshots": len(
                source["join_validation"][
                    "absent_annotation_ids_not_inferred_reviewed"
                ]
            ),
            "evidence_classes": dict(sorted(evidence_counts.items())),
            "direct_labels": {
                label: sum(
                    1
                    for record in records
                    if (record["human_evidence"]["direct_label"] or {}).get("label")
                    == label
                )
                for label in ["pass", "fail", "ambiguous"]
            },
            "device_types": {
                value: sum(1 for record in records if record["device_type"] == value)
                for value in ["laptop", "printer"]
            },
        },
        "exclusions": {
            "empty_comment_row_ids": sorted(excluded_empty),
            "absent_annotation_row_ids": source["join_validation"][
                "absent_annotation_ids_not_inferred_reviewed"
            ],
        },
        "verification": {
            "all_annotation_snapshot_hashes_match": True,
            "all_comments_match_exact_native_annotation_rows": True,
            "all_included_assets_are_scene_generation": True,
            "all_generated_scene_local_files_verified": True,
            "all_digital_twin_local_files_verified": True,
            "all_local_image_hashes_bytes_and_dimensions_match_frozen_mapping": True,
            "all_relational_prior_v2_result_hashes_match": True,
            "join_key": source["join_validation"]["join_key"],
            "row_idx_used_for_join": False,
        },
        "records": records,
    }

    manifest_path = HERE / "manifest.json"
    manifest_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")

    report = f"""# Natural Placement Judge V4.1 comment-grounded validation inventory

This is a **development corpus**, not a held-out test set and not an accuracy
estimate. It contains {len(records)} V6 scene-generation rows with non-empty
human comments. The source FE button choices are ignored because the reviewer
said those buttons were used incorrectly.

## Evidence strata

| Evidence class | Rows | Meaning |
|---|---:|---|
| Direct verdict or ambiguity label | {evidence_counts.get('direct_verdict_or_ambiguity_label', 0)} | The free-text comment itself says pass, fail, weak/borderline pass/fail, or ambiguous. Qualifiers remain explicit. |
| Issue/assessment only | {evidence_counts.get('issue_or_assessment_only_no_direct_verdict', 0)} | The comment identifies a concrete concern or assessment but gives no direct rubric verdict. |
| Relational agreement + concrete comment | {evidence_counts.get('relational_agreement_with_concrete_comment', 0)} | The reviewer agrees with the displayed prior judge and adds concrete evidence. The prior V2 result is preserved as reference provenance, not as an independent human label. |
| Relational agreement only | {evidence_counts.get('relational_agreement_only', 0)} | Bare agreement is linked to the exact frozen V2 result and never promoted to an independent human verdict. |

The directly stated labels are: {output['counts']['direct_labels']['pass']} pass,
{output['counts']['direct_labels']['fail']} fail, and
{output['counts']['direct_labels']['ambiguous']} ambiguous. These small,
development-selected counts are unsuitable for estimating production accuracy.

## Inclusion and exclusions

- Included: all {len(records)} persisted rows with non-empty comments.
- Excluded: {len(excluded_empty)} persisted rows with empty comments; an empty
  comment is not treated as a pass.
- Excluded: {len(output['exclusions']['absent_annotation_row_ids'])} report rows
  absent from the saved annotation snapshots; absence is not treated as review.
- Runtime target assets are scene-generation outputs only. The twin remains a
  product reference.

## Integrity checks

- Every generated scene and twin local file was opened and checked against the
  frozen SHA-256, byte size, and dimensions.
- Every annotation snapshot matches its frozen SHA-256.
- Every relational agreement points to a frozen V2 result whose file hash was
  rechecked. Its verdict and explanation are explicitly marked reference-only.
- Asset joins use exact row ID, never row position.

## Files

- Machine-readable inventory: `{manifest_path}`
- Reproducible builder: `{HERE / 'build_validation_corpus.py'}`
- This report: `{HERE / 'REPORT.md'}`
"""
    (HERE / "REPORT.md").write_text(report)

    print(json.dumps({"manifest": str(manifest_path), "counts": output["counts"]}, indent=2))


if __name__ == "__main__":
    main()
