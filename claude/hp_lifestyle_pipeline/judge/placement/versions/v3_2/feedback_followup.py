"""Give Astra the user's localized evidence without altering frozen judgments."""

import json

import common

SOURCE = common.ROOT.parent / "v3_2_r2"
OUTPUT = common.ROOT / "astra_localized_feedback"
CASE_ID = "13_elitebook_13_Front_Left_Medium_4"
FEEDBACK = (
    "The laptop's front edge is not aligned with the front edge of the table. "
    "Also, there is an extra piece of wood coming out of the top of the backrest "
    "of the chair."
)
ROLES = (
    "p1_baseline",
    "p1_compact",
    "p1_proposal",
    "p1_independent",
    "p2_geometry",
    "p2_use",
    "p2_reconcile",
)


def main():
    frozen = json.loads((SOURCE / "protocol_freeze.json").read_text())
    for item in frozen["files"]:
        if common.sha(item["path"]) != item["sha256"]:
            raise ValueError("Predecessor changed since its judgments")
    cases = json.loads((common.R1 / "r2/calibration_manifest.json").read_text())[
        "cases"
    ]
    tiles = json.loads(
        (common.ROOT / "astra_native_tile_probe/input.json").read_text()
    )["cases"]
    tile_cases = {case["id"]: case for case in tiles}
    if (OUTPUT / "proposal.json").exists():
        raise ValueError("Completed consultation must not be semantically resampled")
    expanded = {}
    for dataset in ("historical", "refiner"):
        summary = json.loads(
            (SOURCE / "evaluation" / dataset / "summary.json").read_text()
        )
        if not summary["terminal"]:
            raise ValueError("Expansion must finish before this evidence snapshot")
        expanded[dataset] = {
            "summary_path": str(SOURCE / "evaluation" / dataset / "summary.json"),
            "summary_sha256": common.sha(
                SOURCE / "evaluation" / dataset / "summary.json"
            ),
            "expected": summary["expected"],
            "complete": sum(row["status"] == "complete" for row in summary["records"]),
            "errors": [
                {
                    key: row.get(key)
                    for key in ("id", "candidate", "error_type", "error")
                }
                for row in summary["records"]
                if row["status"] == "error"
            ],
        }
    inputs = {
        "task": (
            "Inspect the actual images using the user's NEW localized feedback. "
            "You alone do sensitive visual analysis and system-prompt design; "
            "the engineer supplies code, source bindings, gates and evaluations."
        ),
        "new_user_feedback": {"case_id": CASE_ID, "verbatim": FEEDBACK},
        "provenance_and_contradiction": (
            "The original frozen EliteBook label demanded no material orientation failure "
            "and a TABLE-construction failure. The user's latest explicit clarification "
            "instead names laptop/front-table edge misalignment and a protruding piece "
            "above the CHAIR backrest. Do not rewrite old results or pretend those were "
            "the old labels. Evaluate this new evidence independently, distinguish human "
            "expectations from what the actual pixels support, and identify which "
            "criterion labels should apply to a prospective successor. Do not turn a "
            "single pair of differently sloped projected edges into proof of rotation, "
            "nor call an ordinary chair upright/projection a defect without an exposed "
            "construction or appearance inconsistency. Do not demand physical "
            "impossibility if the exposed member is clearly malformed or unmotivated."
        ),
        "predecessor": {
            "version": str(SOURCE),
            "protocol_sha256": common.sha(SOURCE / "protocol_freeze.json"),
            "calibration": json.loads(
                (SOURCE / "evaluation/calibration/summary.json").read_text()
            ),
            "system_prompts": {
                role: (SOURCE / "prompts" / (role + ".txt")).read_text()
                for role in ROLES
            },
            "expansion": expanded,
        },
        "previous_native_pixel_analysis": json.loads(
            (common.ROOT / "astra_native_tile_probe/analysis.json").read_text()
        ),
        "cases": cases,
        "constraints": (
            "Preserve all strict schemas, deterministic five-component scoring/weights, "
            "retired chair-pose code and both P1/P2 architectures. P1 uses complementary "
            "primaries with requested-component-only verifiers; P2 has mutually blind "
            "always-on geometry/use specialists and a final image reconciler. Full "
            "uncropped original/reference images are authoritative; fixed native-pixel "
            "quadrants aid consultation only, not a new runtime. Do not put image IDs, "
            "coordinates, target labels, desired answers or memorized furniture into "
            "judge prompts. Preserve genuine Cashmere alignment detection and harmless "
            "chair-offset tolerance; inspect all three non-gold controls for the same "
            "failure mechanism. Only author a successor if new visual evidence warrants "
            "a transferable correction; no cosmetic semantic reroll. Do not write code "
            "or claim promotion/held-out accuracy. The engineer will separately fix "
            "transport/schema orchestration problems, not alter old model results."
        ),
        "schemas": {
            "final": common.OBSERVATION_SCHEMA,
            "component_verifier_example": common.LEGACY.component_schema(
                list(common.SCORING.COMPONENT_WEIGHTS)
            ),
            "geometry": json.loads(
                (
                    SOURCE
                    / "evaluation/calibration/p2"
                    / CASE_ID
                    / "p2_geometry/schema.json"
                ).read_text()
            ),
            "use": json.loads(
                (
                    SOURCE
                    / "evaluation/calibration/p2"
                    / CASE_ID
                    / "p2_use/schema.json"
                ).read_text()
            ),
        },
        "required_json_output": {
            "localized_case_analysis": (
                "Actual pixel-grounded evidence/counter-evidence for BOTH newly named "
                "issues; member ownership, consequence, severity/confidence, component "
                "and issue codes. Preserve any disagreement with the user."
            ),
            "other_case_analysis": "The other five cases: transferable mechanism and controls.",
            "successor_justified": "boolean, supported by new evidence rather than desired labels",
            "change_hypothesis": "Concise causal failure diagnosis and transferable policy change.",
            "prospective_criterion_expectations": (
                "For the EliteBook, state whether each latest human expectation is "
                "visually substantiated; distinguish a changed label from improved detection."
            ),
            "revised_prompts": {
                role: "Complete runnable prompt string IF justified; otherwise revised_prompts=null"
                for role in ROLES
            },
            "remaining_limitations": "Unresolved evidence, regression and operational risks.",
        },
    }
    OUTPUT.mkdir(exist_ok=True)
    common.write_json(OUTPUT / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    for case in cases:
        for role in ("generated_image", "twin_image"):
            image = case[role]
            if common.sha(image["local_path"]) != image["sha256"]:
                raise ValueError("Consultation image differs from frozen source")
            parts += common.LEGACY.image_parts(
                case["id"] + " / " + role, image["local_path"]
            )
        for tile in tile_cases[case["id"]]["tiles"]:
            if common.sha(tile["path"]) != tile["sha256"]:
                raise ValueError("Native-pixel consultation tile changed")
            parts += common.LEGACY.image_parts(
                case["id"] + f" / fixed quadrant {tile['index']}", tile["path"]
            )
    result, receipt = common.model_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are Astra, the HP placement visual-analysis and system-prompt "
                    "specialist. Inspect actual localized evidence; preserve honest "
                    "disagreement and never manufacture promotion."
                ),
            },
            {"role": "user", "content": parts},
        ],
        None,
        24576,
        OUTPUT,
    )
    if type(result["successor_justified"]) is not bool:
        raise ValueError("Missing explicit evidence-based successor decision")
    prompts = result["revised_prompts"]
    if result["successor_justified"]:
        if (
            not isinstance(prompts, dict)
            or set(prompts) != set(ROLES)
            or any(
                not isinstance(text, str) or len(text.strip()) < 400
                for text in prompts.values()
            )
        ):
            raise ValueError("Missing seven complete justified Astra prompts")
    elif prompts is not None:
        raise ValueError("Unjustified prompt revision must not be extracted")
    common.write_json(OUTPUT / "proposal.json", result)
    common.write_json(OUTPUT / "receipt.json", receipt)
    print(
        json.dumps(
            {"complete": True, "successor_justified": result["successor_justified"]}
        )
    )


if __name__ == "__main__":
    main()
