"""Ask Astra to preregister representable feedback requirements before predictions."""

import argparse
import copy
import json
from pathlib import Path

import common
import transport
from appearance_feedback import OUTPUT, USER_STANDARD, replay, verified_analysis
from jsonschema import Draft202012Validator
from prepare_appearance import TARGET


def component_codes():
    return {
        name: sorted(values - {"chair_alignment_conflict"})
        for name, values in common.LEGACY.SCORING.ISSUE_CODES.items()
    }


def normalize_cases(result, corpus, repairs=None):
    cases = copy.deepcopy(result["cases"])
    sources = {row["id"]: row for row in corpus["records"]}
    if (
        len(cases) != len(sources)
        or {row["case_id"] for row in cases} != sources.keys()
    ):
        raise ValueError("Requirements omit or duplicate source images")
    unmatched = set()
    for case in cases:
        concerns = case["concerns"]
        if not concerns or len({item["id"] for item in concerns}) != len(concerns):
            raise ValueError("Every source needs explicit unique concern/scope records")
        for concern in concerns:
            quote = concern["source_quote"]
            if not quote.strip():
                raise ValueError("Empty source quote")
            if not any(
                quote in item["comment"]
                for item in sources[case["case_id"]]["human_feedback"]
            ):
                unmatched.add((case["case_id"], concern["id"]))
    repair_rows = repairs["repairs"] if repairs is not None else []
    repair_index = {(row["case_id"], row["concern_id"]): row for row in repair_rows}
    if len(repair_index) != len(repair_rows) or repair_index.keys() != unmatched:
        raise ValueError("Actual Astra origin repairs must match only unmatched quotes")
    codes = component_codes()
    for case in cases:
        for concern in case["concerns"]:
            concern["origin"] = "human_feedback"
            repair = repair_index.get((case["case_id"], concern["id"]))
            if repair is not None:
                concern["origin"] = repair["origin"]
                concern["original_model_excerpt"] = concern["source_quote"]
                concern["origin_repair_rationale"] = repair["rationale"]
                quote = repair["verbatim_human_quote"]
                if repair["origin"] == "human_feedback":
                    if not quote or not any(
                        quote in item["comment"]
                        for item in sources[case["case_id"]]["human_feedback"]
                    ):
                        raise ValueError("Corrected quote is not actual human feedback")
                    concern["source_quote"] = quote
                elif repair["origin"] == "astra_extra_finding" and quote is None:
                    concern["source_quote"] = None
                else:
                    raise ValueError("Malformed Astra source-origin correction")
            component = concern["component"]
            issue_codes = concern["issue_codes"]
            if issue_codes and (
                component not in codes
                or any(code not in codes[component] for code in issue_codes)
            ):
                raise ValueError("Concern codes do not belong to its component")
            if concern["scope"] == "supported_in_scope" and (
                component not in codes or not issue_codes
            ):
                raise ValueError(
                    "Supported concern lacks a representable component/code"
                )
            required = (
                concern["scope"] == "supported_in_scope"
                and concern["origin"] == "human_feedback"
            )
            concern["required_for_coverage_gate"] = required
            concern["minimum_severity"] = 1 if required else None
    if not any(
        concern["required_for_coverage_gate"]
        for case in cases
        for concern in case["concerns"]
    ):
        raise ValueError("No supported human placement requirements")
    return cases


def actual_result(receipt):
    value = replay(receipt).result()
    path = Path(receipt["chunks_path"]).with_name("parsed.json")
    if json.loads(path.read_text()) != value:
        raise ValueError("Parsed artifact differs from the actual Astra response")
    return value


def verify_requirements(requirements, corpus):
    source = actual_result(requirements["actual_astra_receipt"])
    repair_receipt = requirements.get("actual_origin_repair_receipt")
    repairs = actual_result(repair_receipt) if repair_receipt is not None else None
    cases = normalize_cases(source, corpus, repairs)
    required = sum(
        concern["required_for_coverage_gate"]
        for case in cases
        for concern in case["concerns"]
    )
    if (
        requirements["cases"] != cases
        or requirements["limitations"] != source["limitations"]
        or requirements["required_concerns"] != required
    ):
        raise ValueError(
            "Requirements differ from actual Astra source/origin decisions"
        )
    return cases


def finalize(corpus, directory):
    if (TARGET / "protocol_freeze.json").exists():
        raise ValueError("Feedback requirements must precede the candidate freeze")
    if (TARGET / "feedback_requirements.json").exists():
        raise ValueError("Materialized requirements already exist; do not overwrite")
    if len(corpus["records"]) != 30:
        raise ValueError("Expected all thirty exact C-Tech sources")
    receipt = json.loads((directory / "receipt.json").read_text())
    result = actual_result(receipt)
    if json.loads((directory / "result.json").read_text()) != result:
        raise ValueError("Preregistration differs from the actual response")
    repair_directory = directory / "origin_repairs"
    repair_receipt = (
        json.loads((repair_directory / "receipt.json").read_text())
        if repair_directory.exists()
        else None
    )
    repairs = actual_result(repair_receipt) if repair_receipt is not None else None
    if (
        repairs is not None
        and json.loads((repair_directory / "result.json").read_text()) != repairs
    ):
        raise ValueError("Origin correction differs from the actual response")
    cases = normalize_cases(result, corpus, repairs)
    required = sum(
        concern["required_for_coverage_gate"]
        for case in cases
        for concern in case["concerns"]
    )
    requirements = {
        "schema_version": "placement-feedback-requirements-v2",
        "cases": cases,
        "limitations": result["limitations"],
        "corpus_sha256": common.sha(OUTPUT / "corpus.json"),
        "actual_astra_response_path": str(
            Path(receipt["chunks_path"]).with_name("parsed.json")
        ),
        "actual_astra_receipt": receipt,
        "actual_origin_repair_receipt": repair_receipt,
        "gate_metadata_is_application_derived": True,
        "required_concerns": required,
    }
    verify_requirements(requirements, corpus)
    common.write_json(TARGET / "feedback_requirements.json", requirements)
    print(
        json.dumps(
            {
                "requirements_preregistered": True,
                "images": 30,
                "supported_human_concerns": required,
                "additional_astra_findings": sum(
                    concern["origin"] == "astra_extra_finding"
                    for case in cases
                    for concern in case["concerns"]
                ),
                "new_model_calls": 0,
            }
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize-existing", action="store_true")
    args = parser.parse_args()
    corpus = json.loads((OUTPUT / "corpus.json").read_text())
    records = corpus["records"]
    directory = OUTPUT / "requirements"
    if args.finalize_existing:
        finalize(corpus, directory)
        return
    if directory.exists():
        raise ValueError(
            "Requirements run exists; use --finalize-existing without redrawing it"
        )
    if (TARGET / "protocol_freeze.json").exists():
        raise ValueError("Feedback requirements must precede the candidate freeze")
    codes = component_codes()
    concern_properties = {
        "id": {"type": "string"},
        "source_quote": {"type": "string"},
        "scope": {
            "type": "string",
            "enum": [
                "supported_in_scope",
                "uncertain_in_scope",
                "disputed_in_scope",
                "out_of_scope",
                "no_defect_claim",
            ],
        },
        "component": {"type": ["string", "null"], "enum": [*codes, None]},
        "issue_codes": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": sorted({code for values in codes.values() for code in values}),
            },
        },
        "rationale": {"type": "string"},
    }
    row_properties = {
        "case_id": {"type": "string", "enum": [row["id"] for row in records]},
        "concerns": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": list(concern_properties),
                "properties": concern_properties,
            },
        },
    }
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["cases", "limitations"],
        "properties": {
            "cases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": list(row_properties),
                    "properties": row_properties,
                },
            },
            "limitations": {"type": "array", "items": {"type": "string"}},
        },
    }
    inputs = {
        "task": (
            "Preregister placement-feedback coverage requirements from the already completed "
            "actual-image analyses and exact human comments, before any successor predictions. "
            "This is sensitive scope/criterion policy, not image reanalysis or coding. Do not "
            "change the actual visual findings, invent new claims, or infer whole-image FAIL "
            "means placement FAIL."
        ),
        "standard": USER_STANDARD,
        "actual_visual_analyses": [verified_analysis(batch) for batch in (1, 2, 3)],
        "human_comments": [
            {
                "case_id": row["id"],
                "comments": [comment["comment"] for comment in row["human_feedback"]],
            }
            for row in records
        ],
        "component_codes": codes,
        "constraints": (
            "Cover all30 images and every distinct concern in the comments. Use an exact "
            "verbatim contiguous source_quote, not a paraphrase; neutral OK is explicitly "
            "no_defect_claim, not comprehensive negative gold. Assign unique concern IDs "
            "per case. supported_in_scope means a supported VISIBLE APPEARANCE concern "
            "representable in existing placement components, without requiring physical "
            "impossibility. Distinguish genuinely uncertain visual appearance and disputed "
            "claims. Lighting/brand legibility, wall-art taste and depth preferences are "
            "out of scope unless the prior actual analysis establishes a representable "
            "placement/scene-arrangement concern. Out-of-scope/disputed concerns remain "
            "explicit; do not silently omit them or force a code. Supported requirements "
            "will require actual concern detection and a score penalty of at least "
            "severity1, not automatic FAIL. Higher materiality remains visible in actual "
            "judge evidence, but free-text whole-image labels do not supply calibrated "
            "numeric severity. No new candidate predictions were supplied. These are "
            "Astra's interpretations of development feedback, not human-verified gold "
            "or held-out accuracy. Preserve scope limitations."
        ),
    }
    directory.mkdir()
    common.write_json(directory / "input.json", inputs)
    common.write_json(directory / "schema.json", schema)
    result, receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": "You are Astra, the HP visual-feedback and prompt-policy specialist. Preregister honest representable appearance requirements from actual prior analyses; do not rejudge images or retrofit labels to predictions.",
            },
            {"role": "user", "content": json.dumps(inputs)},
        ],
        schema,
        32768,
        directory,
    )
    Draft202012Validator(schema).validate(result)
    common.write_json(directory / "result.json", result)
    common.write_json(directory / "receipt.json", receipt)
    finalize(corpus, directory)


if __name__ == "__main__":
    main()
