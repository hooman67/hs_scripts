"""Astra diagnoses actual appearance-revision regressions before another version."""

import argparse
import json
from pathlib import Path

import build_review
import common
import transport
from appearance_feedback import USER_STANDARD, verified_analysis
from audit_feedback import audit_parts, native_packets
from feedback_followup import FEEDBACK
from feedback_requirements import verify_requirements
from revise import ROLES

EXEMPLAR_AUDIT_SYSTEM = (
    "You are Astra, the HP visual-analysis and judge-policy specialist. "
    "Audit the supplied actual exemplar evidence. Return a JSON object; "
    "no code or unearned promotion."
)


def exemplar_messages(inputs):
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    for anchor in inputs["actual_exemplars"]["selected"]:
        if (
            not Path(anchor["local_path"]).resolve().is_relative_to("/home/colligo")
            or common.sha(anchor["local_path"]) != anchor["sha256"]
        ):
            raise ValueError("Exemplar evidence must match its durable original")
        parts += common.LEGACY.image_parts(
            anchor["asset_id"] + ": " + anchor["guidance"], anchor["local_path"]
        )
    encoded_bytes = sum(
        len(part["image_url"]["url"].split(",", 1)[1])
        for part in parts
        if part["type"] == "image_url"
    )
    if encoded_bytes > 105_000_000 or (
        "encoded_image_bytes" in inputs
        and inputs["encoded_image_bytes"] != encoded_bytes
    ):
        raise ValueError("Exemplar audit image budget or recorded byte count differs")
    inputs["encoded_image_bytes"] = encoded_bytes
    parts[0]["text"] = json.dumps(inputs)
    return [
        {"role": "system", "content": EXEMPLAR_AUDIT_SYSTEM},
        {"role": "user", "content": parts},
    ]


def audit_exemplars(version):
    diagnosis = build_review.successor_diagnosis(version)
    if diagnosis is None:
        raise ValueError(
            "Finish the actual failure diagnosis before auditing exemplars"
        )
    for item in json.loads((version / "protocol_freeze.json").read_text())["files"]:
        if common.sha(item["path"]) != item["sha256"]:
            raise ValueError("Frozen candidate changed")
    summary = json.loads((version / "evaluation/calibration/summary.json").read_text())
    failed = [
        row
        for row in build_review.indexed(summary).values()
        if row["candidate"] == "p1" and not all(row["checks"].values())
    ]
    if len(failed) != 1:
        raise ValueError("This bounded audit requires one actual failed P1 case")
    result = json.loads(Path(failed[0]["result_path"]).read_text())
    source = Path(result["stages"]["baseline"]["path"]).with_name("exemplars.json")
    supplied = json.loads(source.read_text())
    selected, excluded = common.LEGACY.select_anchors(result["runtime_input"])
    if supplied != {"selected": selected, "excluded": excluded}:
        raise ValueError("Exemplars differ from the actual frozen baseline delivery")
    inputs = {
        "task": (
            "Audit the actual frozen baseline exemplar images and exact guidance, as "
            "requested in your completed failure diagnosis. This is newly supplied "
            "exemplar evidence, not a redraw of the same target judgments. Inspect "
            "every exemplar and distinguish original human labels, researcher "
            "interpretations and present visual assessment. Do not silently relabel "
            "human examples. Identify any concrete contradiction or unsupported "
            "guidance affecting the authorized appearance boundary; distinguish "
            "that from merely missing contrastive examples. These exemplars reach "
            "ONLY P1 baseline, not P1 compact or any P2 branch, so do not attribute "
            "P2's independent misses to them. State whether this new evidence "
            "establishes any genuinely justified remedy, or precisely what new "
            "human-reviewed contrastive evidence is still needed. If proposing "
            "guidance corrections, supply your exact replacement strings, their "
            "image evidence, scope and limitations; proposals are not implemented "
            "or a demonstrated recovery. No code, forced confidence, target-specific "
            "exceptions, gate waivers or cosmetic seven-prompt rewrite."
        ),
        "user_confirmed_standard": USER_STANDARD,
        "source_revision": version.name,
        "protocol_freeze_sha256": common.sha(version / "protocol_freeze.json"),
        "actual_exemplar_artifact": str(source),
        "actual_exemplar_artifact_sha256": common.sha(source),
        "actual_exemplars": supplied,
        "current_system_prompts": {
            role: (version / "prompts" / (role + ".txt")).read_text() for role in ROLES
        },
        "actual_completed_failure_diagnosis": diagnosis["analysis"],
        "failure_diagnosis_receipt": diagnosis["receipt"],
        "image_scope": (
            "Only the actual baseline exemplar originals below are visually supplied "
            "in this call. The target diagnosis is prior actual analysis, not a new "
            "independent target-image inspection. Historical failure exemplars and "
            "researcher-interpreted references are not comprehensive placement gold "
            "or a human-labeled clean/minor-appearance contrastive set."
        ),
    }
    messages = exemplar_messages(inputs)
    output = version / "astra_exemplar_audit"
    output.mkdir(exist_ok=False)
    common.write_json(output / "input.json", inputs)
    analysis, receipt = transport.model_completion(messages, None, 16384, output)
    common.write_json(output / "analysis.json", analysis)
    common.write_json(output / "receipt.json", receipt)
    print(json.dumps({"exemplar_audit_complete": True, "exemplars": len(selected)}))


def consult(version):
    if version.parent != common.ROOT.parent:
        raise ValueError("Use an isolated frozen sibling candidate")
    freeze_path = version / "protocol_freeze.json"
    for item in json.loads(freeze_path.read_text())["files"]:
        if common.sha(item["path"]) != item["sha256"]:
            raise ValueError("Frozen candidate changed")
    summary = json.loads((version / "evaluation/calibration/summary.json").read_text())
    predictions = build_review.indexed(summary)
    if len(predictions) != 12 or not summary["complete"]:
        raise ValueError("Finish all twelve actual calibration predictions")
    cases = json.loads((version / "calibration_manifest.json").read_text())["cases"]
    requirements = json.loads((version / "feedback_requirements.json").read_text())
    verify_requirements(
        requirements, json.loads((version / "evaluation/ctech/corpus.json").read_text())
    )
    mismatches = [
        {
            "case_id": row["id"],
            "candidate": row["candidate"],
            "missed_checks": [
                name for name, matched in row["checks"].items() if not matched
            ],
        }
        for row in predictions.values()
        if not all(row["checks"].values())
    ]
    if not mismatches:
        raise ValueError("No observed calibration miss justifies a successor")
    failed_ids = {row["case_id"] for row in mismatches}
    intermediate = []
    for row in predictions.values():
        if row["id"] not in failed_ids:
            continue
        result = json.loads(Path(row["result_path"]).read_text())
        intermediate.append(
            {
                "case_id": row["id"],
                "candidate": row["candidate"],
                "actual_stage_observations": {
                    name: json.loads(Path(stage["path"]).read_text())["observation"]
                    for name, stage in result["stages"].items()
                },
            }
        )
    predecessor = common.ROOT.parent / "v3_2_r2"
    inputs = {
        "source_revision": version.name,
        "task": (
            "Diagnose these ACTUAL failed blind judge predictions and author a materially "
            "justified transferable successor, if one exists. You do sensitive visual "
            "analysis, judging and system-prompt policy; the engineer handles legwork/code. "
            "Do not cosmetically resample the same policy or manufacture promotion."
        ),
        "user_confirmed_standard": USER_STANDARD,
        "localized_elitebook_feedback": FEEDBACK,
        "frozen_protocol_sha256": common.sha(freeze_path),
        "actual_calibration_predictions": summary,
        "actual_failed_stage_observations": intermediate,
        "mechanical_unmet_checks": mismatches,
        "calibration_cases": cases,
        "current_system_prompts": {
            role: (version / "prompts" / (role + ".txt")).read_text() for role in ROLES
        },
        "prior_r2_calibration_predictions": json.loads(
            (predecessor / "evaluation/calibration/summary.json").read_text()
        ),
        "prior_r2_system_prompts": {
            role: (predecessor / "prompts" / (role + ".txt")).read_text()
            for role in ROLES
        },
        "actual_completed_ctech_analyses": [
            verified_analysis(batch) for batch in (1, 2, 3)
        ],
        "preregistered_feedback_requirements": requirements,
        "fixed_observation_schema": common.OBSERVATION_SCHEMA,
        "fixed_component_verifier_schema": common.LEGACY.component_schema(
            list(common.SCORING.COMPONENT_WEIGHTS)
        ),
        "failure_question": (
            "Inspect the actual unmet checks in this revision, including its genuine "
            "improvements and regressions rather than assuming a predecessor's outcome. "
            "Why did the written appearance policy and actual runtime mechanism fail "
            "these particular blind checks? "
            "Inspect the actual images, intermediate findings and final clearance. "
            "Identify the concrete visual evidence/counter-evidence and policy/representation "
            "mechanism; do not invent missing detail or simply repeat stronger wording. "
            "Consider whether normal-design/perspective defenses erase an actual appearance "
            "finding, whether full-image vision misses native-pixel local contours, and "
            "whether the five-component greatest-severity representation/consensus loses "
            "concerns. Preserve the known real material detection and harmless-chair "
            "tolerance. The current broader/C-Tech predictions have NOT been run, so "
            "do not claim coverage or infer them from earlier analysis."
        ),
        "constraints": (
            "Keep existing five components/codes/weights/scorer and P1/P2 output schemas. "
            "No target IDs, coordinates, memorized features, per-image exceptions or target "
            "human feedback in runtime prompts. No confidence inflation, threshold waiver "
            "or labeling physical certainty that the image does not establish. Explicit "
            "minor APPEARANCE concern plus penalty is not proof of impossibility or forced "
            "FAIL. Original material/physical predecessor gate remains separately unmet. "
            "A minor concern with low confidence may be rejected by legacy P1 consensus; "
            "do not solve that by dishonest confidence. If a materially useful runtime "
            "mechanism is necessary, explain it explicitly instead of falsely claiming "
            "prompts are sufficient. If fixed native-pixel tiles would help, specify a "
            "general whole-image-preserving rule, not a hand-selected defect ROI. Do not "
            "write code. All six anchors and30 comments are development evidence, not "
            "held-out accuracy. Supported human requirements remain frozen; three "
            "additional Astra findings are not human coverage gold."
        ),
        "required_json_output": {
            "successor_justified": "Boolean; no promise of passing.",
            "case_analysis": "Six case records with visual evidence, counter-evidence and failure mechanisms.",
            "change_hypothesis": "Concrete transferable mechanism versus R3, not cosmetic emphasis.",
            "runtime_change_required": "Explicit necessary runtime change or null; no code.",
            "revised_prompts": {
                role: "Complete runnable prompt string if justified, otherwise null"
                for role in ROLES
            },
            "remaining_limitations": "Honest disagreement, scope and regression risks.",
        },
    }
    native = (version / "visual_policy.json").exists()
    if native:
        inputs["actual_acquisition_and_stage_trace"] = build_review.acquisition_trace(
            {"calibration": summary}
        )
        inputs["actual_acquisition_and_stage_trace"]["records"] = [
            row
            for row in inputs["actual_acquisition_and_stage_trace"]["records"]
            if row["id"] in failed_ids
        ]
        inputs["actual_acquisition_and_stage_trace"]["scope"] = (
            "All actual branches for the genuinely failed case IDs. Other complete "
            "stage/acquisition artifacts remain preserved in the source version; "
            "all twelve final predictions and six full source/reference pairs are supplied."
        )
        del inputs["actual_failed_stage_observations"]
        inputs["current_visual_policy"] = json.loads(
            (version / "visual_policy.json").read_text()
        )
        immediate = Path(
            json.loads((version / "promotion_gates.json").read_text())["predecessor"][
                "path"
            ]
        )
        inputs["immediate_predecessor_calibration"] = json.loads(
            (immediate / "evaluation/calibration/summary.json").read_text()
        )
        del inputs["prior_r2_system_prompts"]
        inputs["failure_question"] += (
            " The complete native packet and actual independent unscored acquisitions "
            "were already used; do not propose them as though they were missing. "
            "Trace the localized cue through each actual acquisition, discovery, "
            "verification, reconciliation and final selection. If there is no honestly "
            "justified transferable successor under the fixed policy, say so and identify "
            "the exact missing evidence or authorization instead of supplying cosmetic "
            "wording, inventing a defect or drawing the same policy again."
        )
    output = version / "astra_successor_consult"
    output.mkdir(exist_ok=False)
    common.write_json(output / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    packets = (
        [case for packet in native_packets(version, cases) for case in packet]
        if native
        else cases
    )
    parts += audit_parts(packets)
    if (
        sum(
            len(item["image_url"]["url"].split(",", 1)[1])
            for item in parts
            if item["type"] == "image_url"
        )
        > 45_000_000
    ):
        raise ValueError("Complete successor consultation exceeds image budget")
    proposal, receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are Astra, the HP appearance-sensitive visual-analysis and "
                    "judge-system-prompt specialist. Diagnose actual preserved failures "
                    "and propose a genuinely different transferable mechanism, not "
                    "cosmetic repetition or forced accusations. No code."
                ),
            },
            {"role": "user", "content": parts},
        ],
        None,
        32768,
        output,
    )
    if type(proposal["successor_justified"]) is not bool:
        raise ValueError("Missing explicit successor decision")
    prompts = proposal["revised_prompts"]
    if proposal["successor_justified"] and (
        not isinstance(prompts, dict)
        or set(prompts) != set(ROLES)
        or any(
            not isinstance(text, str) or len(text.strip()) < 400
            for text in prompts.values()
        )
    ):
        raise ValueError("Justified successor lacks seven complete actual prompts")
    common.write_json(output / "proposal.json", proposal)
    common.write_json(output / "receipt.json", receipt)
    print(
        json.dumps(
            {
                "consultation_complete": True,
                "successor_justified": proposal["successor_justified"],
                "source_revision": version.name,
            }
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version-root", type=Path, required=True)
    parser.add_argument("--audit-exemplars", action="store_true")
    args = parser.parse_args()
    version = args.version_root.resolve()
    if version.parent != common.ROOT.parent:
        raise ValueError("Use an isolated frozen sibling candidate")
    if args.audit_exemplars:
        audit_exemplars(version)
    else:
        consult(version)


if __name__ == "__main__":
    main()
