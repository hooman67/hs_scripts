"""Ask Astra to diagnose actual calibration failures and author a new revision."""

import argparse
import json
import shutil

import common

OUTPUT = common.ROOT / "astra_revision_consult"
ROLES = (
    "p1_baseline",
    "p1_compact",
    "p1_proposal",
    "p1_independent",
    "p2_geometry",
    "p2_use",
    "p2_reconcile",
)


def consult():
    summary_path = common.ROOT / "evaluation/calibration/summary.json"
    summary = json.loads(summary_path.read_text())
    if len(summary["records"]) != 12 or not summary.get("complete"):
        raise ValueError(
            "Both original six-case calibrations must be terminal before revision"
        )
    manifest_path = common.R1 / "r2/calibration_manifest.json"
    cases = json.loads(manifest_path.read_text())["cases"]
    inputs = {
        "task": "Analyze the actual supplied images and the actual Astra P1/P2 predictions. Diagnose errors and propose a materially justified next revision of all seven complete system prompts. You do sensitive visual reasoning and prompt design only; the engineer handles code, schemas, retrieval, freezing, execution and reporting.",
        "current_protocol_sha256": common.verify_freeze(),
        "actual_judge_model": common.MODEL,
        "actual_calibration": summary,
        "current_system_prompts": {
            role: (common.ROOT / "prompts" / (role + ".txt")).read_text()
            for role in ROLES
        },
        "fixed_final_schema": common.OBSERVATION_SCHEMA,
        "fixed_verifier_schema_example": common.LEGACY.component_schema(
            ["orientation_alignment"]
        ),
        "human_criterion_cases_and_controls": cases,
        "critical_question": (
            "P1 and P2 now catch the Cashmere consequential product/table conflict while tolerating "
            "the harmless-chair example. On the EliteBook case both fail ORIENTATION, miss the "
            "required CONSTRUCTION defect and describe table joins as plausible. The human says "
            "no material product rotation but malformed table. Compare target/reference and "
            "competing rigid groups: is the apparent axis disagreement actually a distorted or "
            "misconstructed support? Identify concrete exposed geometric evidence and alternatives. "
            "Do not merely relabel an unsupported orientation accusation as construction to match "
            "the human. An impossible join is not required for material construction awkwardness, "
            "but an unfamiliar legal design or occluded support must not fail. Preserve disagreement "
            "if pixels do not justify the criterion. Investigate controls for false positives, "
            "including fitted supports, tight crops and unknown hidden construction."
        ),
        "constraints": (
            "Keep five deterministic dimensions/weights/scoring and all strict schemas unchanged; "
            "P1 retains complementary primaries/additions consensus and component-only verifiers; "
            "P2 retains two blind always-on specialists plus image-based reconciler. Never introduce "
            "image IDs, memorized coordinates, per-case exceptions or output the target feedback "
            "as evidence. No confidence inflation or threshold manipulation. Current examples and "
            "the64-case feedback corpus informed design; these are development diagnostics, not "
            "unseen holdout accuracy. The three original criterion labels remain unchanged. "
            "Produce concise transferable visual policy, not an exhaustive reasoning trace. "
            "Do not resample current model answers or claim promotion."
        ),
        "required_json_output": {
            "case_analysis": "Six case records with actual visible support/counter-evidence and error mechanism; identify remaining honest label/pixel disagreement.",
            "change_hypothesis": "Why this revision should fix the observed attribution/false-positive mechanism without suppressing real product/table conflicts.",
            "revised_prompts": {
                role: "Complete runnable system-prompt string, not a patch or advice"
                for role in ROLES
            },
            "remaining_limitations": "Explicit unresolved criteria and risks; do not promise passing calibration.",
        },
    }
    OUTPUT.mkdir(exist_ok=True)
    common.write_json(OUTPUT / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    for case in cases:
        for role in ("generated_image", "twin_image"):
            image = case[role]
            if common.sha(image["local_path"]) != image["sha256"]:
                raise ValueError("Consultation image differs from the frozen case")
            parts += common.LEGACY.image_parts(
                case["id"] + " / " + role, image["local_path"]
            )
    result, receipt = common.model_completion(
        [
            {
                "role": "system",
                "content": "You are Astra, the visual-analysis and system-prompt-design specialist for the HP placement judge. Use actual pixels and preserve honest disagreement; no code or orchestration work.",
            },
            {"role": "user", "content": parts},
        ],
        None,
        24576,
        OUTPUT,
    )
    prompts = result["revised_prompts"]
    if set(prompts) != set(ROLES) or any(
        not isinstance(text, str) or len(text.strip()) < 400
        for text in prompts.values()
    ):
        raise ValueError("Revision is missing complete required role prompts")
    common.write_json(OUTPUT / "proposal.json", result)
    common.write_json(OUTPUT / "receipt.json", receipt)


def extract():
    source = OUTPUT / "proposal.json"
    proposal = json.loads(source.read_text())
    target = common.ROOT.parent / "v3_2_r2"
    target.mkdir(exist_ok=False)
    copies = {}
    for name in (
        "common.py",
        "p1.py",
        "p2.py",
        "evaluate.py",
        "freeze.py",
        "refiner.py",
        "test_common.py",
        "test_p2.py",
    ):
        old, new = common.ROOT / name, target / name
        text = old.read_text().replace("placement-v3.2-p1-r1", "placement-v3.2-p1-r2")
        text = text.replace("placement-v3.2-p2-r1", "placement-v3.2-p2-r2")
        new.write_text(text)
        copies[name] = {
            "source": str(old),
            "source_sha256": common.sha(old),
            "output_sha256": common.sha(new),
        }
    for role, text in proposal["revised_prompts"].items():
        path = target / "prompts" / (role + ".txt")
        path.parent.mkdir(exist_ok=True)
        path.write_text(text)
    gates = json.loads((common.ROOT / "promotion_gates.json").read_text())
    gates["candidate_protocol"] = "v3.2-p1-p2-r2"
    gates["predecessor"] = {
        "path": str(common.ROOT),
        "freeze_sha256": common.verify_freeze(),
    }
    common.write_json(target / "promotion_gates.json", gates)
    common.write_json(
        target / "preparation.json",
        {
            "prompt_source": str(source),
            "prompt_source_sha256": common.sha(source),
            "actual_astra_receipt": json.loads((OUTPUT / "receipt.json").read_text()),
            "code_copies": copies,
            "gates_unchanged": True,
            "revision_reason": proposal["change_hypothesis"],
        },
    )
    for name in ("corpus.json", "source/data.json", "source/object.json"):
        new = target / "evaluation/refiner" / name
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(common.ROOT / "evaluation/refiner" / name, new)
    print(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("consult", "extract"))
    args = parser.parse_args()
    {"consult": consult, "extract": extract}[args.command]()


if __name__ == "__main__":
    main()
