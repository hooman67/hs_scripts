"""Prepare versioned Astra prompts and a fixed development promotion gate."""

import json
from pathlib import Path

import common
from correct_verifiers import MARKERS

ROOT = Path(__file__).resolve().parent
SOURCE = common.R1 / "astra_refiner_followup_20261110/synthesis_resumed_20261111"


def main():
    if (ROOT / "preparation.json").exists():
        raise ValueError("Preparation already exists; preserve the frozen candidate")
    mappings = {
        "p1_baseline": "P1/P1_baseline",
        "p1_compact": "P1/P1_compact",
        "p1_proposal": "P1/P1_proposal_verifier",
        "p1_independent": "P1/P1_independent_verifier",
        "p2_geometry": "P2/P2_geometry_discovery",
        "p2_use": "P2/P2_use_location_discovery",
        "p2_reconcile": "P2/P2_reconciler",
    }
    provenance = []
    for role, relative in mappings.items():
        source = SOURCE / "proposals" / relative
        original = source.read_text()
        text = original
        correction = None
        if role in ("p1_proposal", "p1_independent"):
            marker = MARKERS[role][1]
            head = original[: original.index(marker)]
            patches = ROOT / "verifier_contract_correction/corrections.json"
            text = head + json.loads(patches.read_text())[role] + "\n"
            correction = {
                "method": "Astra-authored replacement output-contract tail; original visual-rule prefix byte-identical.",
                "source": str(patches),
                "sha256": common.sha(patches),
                "unchanged_prefix_sha256": common.hashlib.sha256(
                    head.encode()
                ).hexdigest(),
            }
        output = ROOT / "prompts" / (role + ".txt")
        output.parent.mkdir(exist_ok=True)
        output.write_text(text)
        provenance.append(
            {
                "role": role,
                "source": str(source),
                "source_sha256": common.sha(source),
                "output": str(output),
                "output_sha256": common.sha(output),
                "correction": correction,
            }
        )
    calibration = common.R1 / "r2/calibration_manifest.json"
    gate = {
        "candidate_protocol": "v3.2-p1-p2-r1",
        "development_only": True,
        "model": common.MODEL,
        "reasoning_effort": "high",
        "model_change": "Explicit latest user requirement: Astra judges actual images and authors sensitive prompt changes. Compare against frozen GPT-5.5 incumbent/r1/r2; architecture and model effects are coupled.",
        "source_stage": "e2e_comparison_output; not held-out scene-stage accuracy",
        "calibration_manifest": str(calibration),
        "calibration_sha256": common.sha(calibration),
        "required_criteria": "All three C-Tech criterion labels retained: harmless-chair no placement failure; material Cashmere product/table conflict; EliteBook construction failure without orientation penalty.",
        "controls": "No new material orientation/construction failures in the three frozen non-gold stability controls.",
        "operational": "Zero semantic/validation failures in six calibration cases; successful completed comparison required before promotion.",
        "promotion_scope": "Versioned research/review judge, not a human-calibrated autonomous acceptance gate or production endpoint deployment.",
        "no_label_leakage": True,
        "semantic_samples_per_candidate_revision_case": 1,
        "evidence_disagreements": "EliteBook criterion unresolved by Astra but not waived; failure to meet it blocks promotion.",
    }
    common.write_json(ROOT / "promotion_gates.json", gate)
    common.write_json(ROOT / "preparation.json", {"prompts": provenance, "gates": gate})


if __name__ == "__main__":
    main()
