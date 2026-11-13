"""Astra distinguishes four non-verbatim excerpts from actual C-Tech claims."""

import json

import common
import transport
from appearance_feedback import OUTPUT, replay
from jsonschema import Draft202012Validator


def main():
    directory = OUTPUT / "requirements"
    result = json.loads((directory / "result.json").read_text())
    receipt = json.loads((directory / "receipt.json").read_text())
    if replay(receipt).result() != result:
        raise ValueError("Requirement response differs from actual Astra source")
    corpus = json.loads((OUTPUT / "corpus.json").read_text())
    rows = {row["id"]: row for row in corpus["records"]}
    unmatched = []
    for case in result["cases"]:
        comments = [item["comment"] for item in rows[case["case_id"]]["human_feedback"]]
        for concern in case["concerns"]:
            if not any(concern["source_quote"] in text for text in comments):
                unmatched.append(
                    {
                        "case_id": case["case_id"],
                        "concern": concern,
                        "actual_human_comments": comments,
                    }
                )
    if len(unmatched) != 4:
        raise ValueError(
            "This correction is bounded to the four diagnosed origin errors"
        )
    output = directory / "origin_repairs"
    output.mkdir(exist_ok=False)
    properties = {
        "case_id": {"type": "string", "enum": [row["case_id"] for row in unmatched]},
        "concern_id": {
            "type": "string",
            "enum": [row["concern"]["id"] for row in unmatched],
        },
        "origin": {"type": "string", "enum": ["human_feedback", "astra_extra_finding"]},
        "verbatim_human_quote": {"type": ["string", "null"]},
        "rationale": {"type": "string"},
    }
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["repairs"],
        "properties": {
            "repairs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": list(properties),
                    "properties": properties,
                },
            }
        },
    }
    inputs = {
        "task": (
            "Correct ONLY source-origin attribution for these four entries. Their "
            "source_quote is not in the actual C-Tech comment. Decide whether each "
            "entry paraphrases a genuine human subclaim (supply an EXACT contiguous "
            "human quote) or is an additional Astra finding absent from the comment. "
            "Extra Astra findings must be preserved separately and must NOT count as "
            "C-Tech feedback-coverage requirements. Do not rejudge images, change "
            "components/codes/scope classifications or rewrite the other59 entries. "
            "Do not invent human comments or force a positive origin match."
        ),
        "entries": unmatched,
        "source_receipt": receipt,
    }
    common.write_json(output / "input.json", inputs)
    common.write_json(output / "schema.json", schema)
    repairs, repair_receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": "You are Astra, the HP feedback provenance specialist. Distinguish actual human claims from additional model findings without inventing or changing either.",
            },
            {"role": "user", "content": json.dumps(inputs)},
        ],
        schema,
        8192,
        output,
    )
    Draft202012Validator(schema).validate(repairs)
    expected = {(row["case_id"], row["concern"]["id"]) for row in unmatched}
    if (
        len(repairs["repairs"]) != 4
        or {(row["case_id"], row["concern_id"]) for row in repairs["repairs"]}
        != expected
    ):
        raise ValueError("Origin correction omitted or changed entries")
    for repair in repairs["repairs"]:
        if repair["origin"] == "human_feedback" and (
            not repair["verbatim_human_quote"]
            or not any(
                repair["verbatim_human_quote"] in item["comment"]
                for item in rows[repair["case_id"]]["human_feedback"]
            )
        ):
            raise ValueError(
                "Corrected source quote still does not match the human comment"
            )
    common.write_json(output / "result.json", repairs)
    common.write_json(output / "receipt.json", repair_receipt)
    print(
        json.dumps(
            {
                "origins_corrected": True,
                "entries": len(repairs["repairs"]),
                "new_image_judgments": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
