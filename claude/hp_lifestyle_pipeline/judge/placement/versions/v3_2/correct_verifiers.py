"""Ask Astra to fix only its incompatible P1 verifier output contracts."""

import json

import common

SOURCE = (
    common.R1
    / "astra_refiner_followup_20261110/synthesis_resumed_20261111/proposals/P1"
)
OUTPUT = common.ROOT / "verifier_contract_correction"
MARKERS = {
    "p1_proposal": (
        "P1_proposal_verifier",
        "Return the exact placement-observations-v3 object",
    ),
    "p1_independent": (
        "P1_independent_verifier",
        "Return exactly one placement-observations-v3 JSON object",
    ),
}


def main():
    inputs = {
        "task": "Correct only the output-contract section of your two proposed P1 verifiers. Do not write code, judge images or change visual/scoring policy. The existing strict runtime requires placement-verifier-components-v1 with exactly requested component names; your full observation/placeholder contract is incompatible.",
        "required_schema_example": common.LEGACY.component_schema(
            ["orientation_alignment"]
        ),
        "component_code_registry": {
            key: sorted(value) for key, value in common.SCORING.ISSUE_CODES.items()
        },
        "required_output": {
            "p1_proposal": "Complete replacement output-contract tail text",
            "p1_independent": "Complete replacement output-contract tail text",
        },
        "constraints": "Return JSON only with these two strings. Each replacement tail must define schema_version and components only; forbid unrequested placeholders and all scene-level fields. Per component: visibility/severity/confidence/evidence/consequence/issue_codes. Respect null/low/no-codes unobservable semantics, severity0 no codes, positive severity codes. Preserve legal code registry but explicitly forbid retired chair_alignment_conflict; harmless chair tolerance remains unchanged. No score/verdict. Caller will preserve the entire original visual-rule prefix unchanged and replace only the contract tail.",
        "original_prompts": {
            role: (SOURCE / filename).read_text()
            for role, (filename, _) in MARKERS.items()
        },
    }
    OUTPUT.mkdir(exist_ok=True)
    common.write_json(OUTPUT / "input.json", inputs)
    result, receipt = common.model_completion(
        [
            {
                "role": "system",
                "content": "You are the original Astra placement-judge system-prompt designer. Make the requested exact protocol-only correction without changing judgment policy.",
            },
            {"role": "user", "content": json.dumps(inputs)},
        ],
        None,
        8192,
        OUTPUT,
    )
    if set(result) != set(MARKERS) or any(
        not isinstance(value, str) or "placement-verifier-components-v1" not in value
        for value in result.values()
    ):
        raise ValueError("Astra correction has missing/wrong verifier contracts")
    common.write_json(OUTPUT / "corrections.json", result)
    common.write_json(OUTPUT / "receipt.json", receipt)


if __name__ == "__main__":
    main()
