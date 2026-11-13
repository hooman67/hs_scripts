"""Apply the pre-prediction gates; never turn a known miss into a promotion."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import common
from feedback_requirements import verify_requirements


def feedback_review(version, gates, candidate):
    if not gates.get("semantic_attribution_requires_astra_review"):
        return {"required": False, "complete": True, "qualified": True}
    requirements_path = version / "feedback_requirements.json"
    audit_path = version / "evaluation/feedback_coverage_audit.json"
    if not requirements_path.exists() or not audit_path.exists():
        return {
            "required": True,
            "complete": False,
            "qualified": False,
            "status": "missing_preregistered_requirements_or_actual_astra_audit",
        }
    requirements = json.loads(requirements_path.read_text())
    audit = json.loads(audit_path.read_text())
    corpus_path = version / "evaluation/ctech/corpus.json"
    verify_requirements(requirements, json.loads(corpus_path.read_text()))
    if requirements["corpus_sha256"] != common.sha(corpus_path):
        raise ValueError(
            "Requirements differ from actual Astra analysis or source corpus"
        )
    if audit["protocol_freeze_sha256"] != common.sha(
        version / "protocol_freeze.json"
    ) or audit["feedback_requirements_sha256"] != common.sha(requirements_path):
        raise ValueError(
            "Feedback audit belongs to another candidate or requirement set"
        )
    expected = {
        (case["case_id"], concern["id"])
        for case in requirements["cases"]
        for concern in case["concerns"]
        if concern["required_for_coverage_gate"]
    }
    calibration = json.loads((version / "calibration_manifest.json").read_text())
    expected.update(
        (case["id"], name + ":" + expectation)
        for case in calibration["cases"]
        for name, expectation in case["expectation"].items()
        if expectation != "unlabeled"
    )
    seen = {}
    for source in audit["runs"]:
        input_path = Path(source["input_path"])
        if common.sha(input_path) != source["input_sha256"]:
            raise ValueError("Astra feedback-audit input changed")
        inputs = json.loads(input_path.read_text())
        if inputs["protocol_freeze_sha256"] != audit["protocol_freeze_sha256"]:
            raise ValueError("Astra feedback audit consumed another protocol")
        for case in inputs["cases"]:
            for prediction in case["actual_predictions"]:
                if prediction["status"] != "complete":
                    continue
                result_path = Path(prediction["result_path"])
                if common.sha(result_path) != prediction["result_sha256"]:
                    raise ValueError("Audited prediction changed")
                result = json.loads(result_path.read_text())
                if (
                    result["protocol_freeze_sha256"] != audit["protocol_freeze_sha256"]
                    or result["candidate"] != prediction["candidate"]
                    or result["application_merged_judgment"]["observation"]
                    != prediction["observation"]
                    or result["application_merged_judgment"]["natural_placement_score"]
                    != prediction["score"]
                    or result["final_decision"]["verdict"] != prediction["verdict"]
                    or any(
                        common.sha(result["runtime_input"][role])
                        != case[role]["sha256"]
                        for role in ("generated_image", "twin_image")
                    )
                ):
                    raise ValueError(
                        "Feedback audit is not bound to the actual case/prediction"
                    )
        receipt = source["receipt"]
        if common.sha(receipt["chunks_path"]) != receipt["chunks_sha256"]:
            raise ValueError("Astra coverage-audit source stream changed")
        collector = common.Collector()
        with Path(receipt["chunks_path"]).open() as stream:
            for line in stream:
                collector.feed(json.loads(line))
        result = collector.result()
        for row in result["records"]:
            if row["candidate"] != candidate:
                continue
            for check in row["checks"]:
                key = (row["id"], check["requirement_id"])
                if key in seen or type(check["matched"]) is not bool:
                    raise ValueError("Duplicate or malformed semantic coverage check")
                seen[key] = check
    missing = sorted(expected - seen.keys())
    misses = [
        {"id": key[0], "requirement_id": key[1], "evidence": seen[key]["evidence"]}
        for key in sorted(expected & seen.keys())
        if not seen[key]["matched"]
    ]
    return {
        "required": True,
        "complete": not missing,
        "qualified": bool(expected) and not missing and not misses,
        "required_concerns": len(expected),
        "missing_checks": missing,
        "missed_concerns": misses,
        "status": "actual_astra_semantic_coverage_review",
    }


def assess(version):
    freeze_path = version / "protocol_freeze.json"
    frozen = json.loads(freeze_path.read_text())
    for dependency in frozen["files"]:
        if common.sha(dependency["path"]) != dependency["sha256"]:
            raise ValueError("Candidate dependency changed since predictions")
    summary = json.loads((version / "evaluation/calibration/summary.json").read_text())
    gates = json.loads((version / "promotion_gates.json").read_text())
    if len(summary["records"]) != 12:
        raise ValueError("All12 candidate calibration results must be terminal")
    candidates = {}
    for candidate in ("p1", "p2"):
        rows = [row for row in summary["records"] if row["candidate"] == candidate]
        if len(rows) != 6 or len({row["id"] for row in rows}) != 6:
            raise ValueError(
                "Candidate does not contain all six fixed calibration cases"
            )
        errors = [row["id"] for row in rows if row["status"] != "complete"]
        mismatches = [
            {
                "id": row["id"],
                "criteria": [
                    key for key, matched in row["checks"].items() if not matched
                ],
            }
            for row in rows
            if row["status"] == "complete" and not all(row["checks"].values())
        ]
        expanded = {}
        for dataset, expected in (("historical", 128), ("refiner", 81)):
            path = version / "evaluation" / dataset / "summary.json"
            items = []
            if path.exists():
                document = json.loads(path.read_text())
                if document["protocol_freeze_sha256"] != common.sha(freeze_path):
                    raise ValueError("Expanded evaluation belongs to another protocol")
                items = [
                    row for row in document["records"] if row["candidate"] == candidate
                ]
            expanded[dataset] = {
                "expected": expected,
                "completed": sum(row["status"] == "complete" for row in items),
                "errors": sum(row["status"] == "error" for row in items),
                "all_complete": len(items) == expected
                and len({row["id"] for row in items}) == expected
                and all(row["status"] == "complete" for row in items),
            }
        eligible = (
            not errors
            and not mismatches
            and all(item["all_complete"] for item in expanded.values())
        )
        semantic = feedback_review(version, gates, candidate)
        if gates.get("ctech_source_cases"):
            path = version / "evaluation/ctech/summary.json"
            document = json.loads(path.read_text()) if path.exists() else None
            if document is not None and document[
                "protocol_freeze_sha256"
            ] != common.sha(freeze_path):
                raise ValueError("C-Tech evaluation belongs to another protocol")
            items = (
                [row for row in document["records"] if row["candidate"] == candidate]
                if document is not None
                else []
            )
            expanded["ctech"] = {
                "expected": gates["ctech_source_cases"],
                "completed": sum(row["status"] == "complete" for row in items),
                "errors": sum(row["status"] == "error" for row in items),
                "all_complete": len(items) == gates["ctech_source_cases"]
                and len({row["id"] for row in items}) == gates["ctech_source_cases"]
                and all(row["status"] == "complete" for row in items),
            }
        eligible = (
            eligible
            and semantic["qualified"]
            and all(item["all_complete"] for item in expanded.values())
        )
        candidates[candidate] = {
            "promoted": eligible,
            "status": (
                "promoted_research_review_judge"
                if eligible
                else "not_promoted_calibration_gate_failed"
                if errors or mismatches
                else "not_promoted_semantic_feedback_audit_pending_or_failed"
                if not semantic["qualified"]
                else "not_promoted_expanded_evaluation_pending"
            ),
            "calibration_errors": errors,
            "unwaived_criterion_mismatches": mismatches,
            "expanded_evaluations": expanded,
            "semantic_feedback_review": semantic,
        }
    selected = (
        "p2"
        if candidates["p2"]["promoted"]
        else "p1"
        if candidates["p1"]["promoted"]
        else None
    )
    result = {
        "version": version.name,
        "as_of_utc": datetime.now(UTC).isoformat(),
        "status": (
            "promoted_research_review_judges"
            if selected
            else "NOT PROMOTED - required gates not met"
        ),
        "selected_candidate": selected,
        "candidates": candidates,
        "model": common.MODEL,
        "reasoning_effort": "high",
        "protocol_freeze_sha256": common.sha(freeze_path),
        "promotion_gates_sha256": common.sha(version / "promotion_gates.json"),
        "promotion_scope": "Versioned research/review use only; no production endpoint/default/PR deployment.",
        "automatic_acceptance_authorized": False,
        "held_out_accuracy": None,
        "false_positive_rate": None,
        "limitations": [
            "All six historical examples and64 feedback cases informed design; not unseen holdout.",
            "Historical anchors/128-image comparison are E2E diagnostics, not scene-stage accuracy.",
            "64 refiner baselines have SHA-verified pre-relighting scene-stage lineage;17 edits are post-refiner diagnostics;47 exact passthroughs reuse predictions.",
            (
                "User-authorized appearance/penalty criteria are versioned separately; this is not recovery of the original physical/material gate."
                if gates.get("criterion_mode") == "appearance_review"
                else "Human criterion labels are unchanged; an overall fail is not agreement if the criterion is wrong."
            ),
            "Unchanged score weights/thresholds remain provisional; high confidence is model-reported, not human acceptance.",
        ],
    }
    common.write_json(version / "release_status.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version-root", type=Path, default=common.ROOT)
    args = parser.parse_args()
    print(json.dumps(assess(args.version_root), indent=2))


if __name__ == "__main__":
    main()
