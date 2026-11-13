"""Astra audits actual predictions against preregistered appearance concerns."""

import argparse
import json
from pathlib import Path

import build_review
import common
import transport
from appearance_feedback import image_packets, replay
from jsonschema import Draft202012Validator


def load(path):
    return json.loads(path.read_text())


def native_packets(version, cases):
    preflight = load(version / "evaluation/visual_preflight.json")
    sources = {row["id"]: row for row in preflight["records"]}
    packets, packet, size = [], [], 0
    for case in cases:
        source = sources[case["id"]]
        path = Path(source["packet_path"])
        if common.sha(path) != source["packet_sha256"]:
            raise ValueError("Frozen native audit packet changed")
        visual = load(path)
        if any(
            visual["identity"]["sources"][role]["sha256"] != case[role]["sha256"]
            for role in ("generated_image", "twin_image")
        ):
            raise ValueError("Native audit packet belongs to another source pair")
        encoded = visual["base64_image_bytes"]
        if encoded > 30_000_000:
            raise ValueError("One complete native audit packet exceeds audit budget")
        if packet and size + encoded > 30_000_000:
            packets.append(packet)
            packet, size = [], 0
        packet.append({**case, "actual_visual_packet": visual})
        size += encoded
    if packet:
        packets.append(packet)
    return packets


def audit_parts(cases):
    parts, seen = [], set()
    for case in cases:
        images = (
            case["actual_visual_packet"]["delivered_images"]
            if "actual_visual_packet" in case
            else [
                {**case[role], "label": role}
                for role in ("generated_image", "twin_image")
            ]
        )
        for image in images:
            if common.sha(image["local_path"]) != image["sha256"]:
                raise ValueError("Audit source image/tile changed")
            if image["sha256"] not in seen:
                parts += common.LEGACY.image_parts(
                    case["id"] + " / " + image["label"], image["local_path"]
                )
                seen.add(image["sha256"])
    return parts


def completed_packet(directory, inputs, schema):
    if not directory.exists():
        return None
    if (
        load(directory / "input.json") != inputs
        or load(directory / "schema.json") != schema
    ):
        raise ValueError("Audit packet source/request changed; no redraw")
    receipt_path = directory / "receipt.json"
    if not receipt_path.exists():
        completed = sorted(directory.glob("attempt*/receipt.json"))
        if len(completed) != 1:
            raise ValueError(
                "Interrupted audit packet needs explicit transport diagnosis"
            )
        receipt_path = completed[0]
    receipt = load(receipt_path)
    result = replay(receipt).result()
    result_path = directory / "result.json"
    if result_path.exists() and load(result_path) != result:
        raise ValueError("Completed audit differs from actual Astra stream")
    return result, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version-root", type=Path, required=True)
    args = parser.parse_args()
    version = args.version_root.resolve()
    if version.parent != common.ROOT.parent:
        raise ValueError("Use an isolated sibling candidate")
    freeze = common.sha(version / "protocol_freeze.json")
    for item in load(version / "protocol_freeze.json")["files"]:
        if common.sha(item["path"]) != item["sha256"]:
            raise ValueError("Candidate changed since its predictions")
    requirements = load(version / "feedback_requirements.json")
    source_cases = load(version / "evaluation/ctech/corpus.json")["records"]
    case_requirements = {
        row["case_id"]: [
            concern
            for concern in row["concerns"]
            if concern["required_for_coverage_gate"]
        ]
        for row in requirements["cases"]
    }
    calibration = load(version / "calibration_manifest.json")["cases"]
    native = (version / "visual_policy.json").exists()
    groups = {
        name: native_packets(version, cases) if native else image_packets(cases)
        for name, cases in (
            ("calibration", calibration),
            ("ctech", source_cases),
        )
    }
    summaries = {
        name: load(version / "evaluation" / name / "summary.json") for name in groups
    }
    indices = {
        name: build_review.indexed(summary) for name, summary in summaries.items()
    }
    traces = (
        {
            (row["id"], row["candidate"]): row
            for row in build_review.acquisition_trace(summaries)["records"]
        }
        if native
        else None
    )
    destination = version / "evaluation/feedback_audit"
    destination.mkdir(exist_ok=True)
    audit_path = version / "evaluation/feedback_coverage_audit.json"
    if audit_path.exists():
        raise ValueError("Completed feedback audit exists; do not redraw it")
    runs = []
    roster = set()
    for dataset, packets in groups.items():
        for packet_number, packet in enumerate(packets, 1):
            directory = destination / f"{dataset}_packet{packet_number:02d}"
            cases = []
            expected = {}
            for case in packet:
                if dataset == "calibration":
                    criteria = [
                        {
                            "id": name + ":" + expectation,
                            "expectation": expectation,
                            "component": name,
                            "source": "Versioned user appearance/penalty calibration; three stability controls are non-gold.",
                        }
                        for name, expectation in case["expectation"].items()
                        if expectation != "unlabeled"
                    ]
                else:
                    criteria = case_requirements[case["id"]]
                predictions = []
                for candidate in ("p1", "p2"):
                    row = indices[dataset][(case["id"], candidate)]
                    predictions.append(
                        {
                            key: row.get(key)
                            for key in (
                                "candidate",
                                "status",
                                "score",
                                "verdict",
                                "observation",
                                "error",
                                "result_path",
                                "result_sha256",
                            )
                        }
                    )
                    if traces is not None:
                        predictions[-1]["actual_acquisition_and_stage_trace"] = traces[
                            (case["id"], candidate)
                        ]
                    expected[(case["id"], candidate)] = {
                        criterion["id"] for criterion in criteria
                    }
                cases.append(
                    {
                        "id": case["id"],
                        "scene_prompt": case["scene_prompt"],
                        "product_type": case["product_type"],
                        "generated_image": case["generated_image"],
                        "twin_image": case["twin_image"],
                        "preregistered_requirements": criteria,
                        "actual_predictions": predictions,
                        **(
                            {"actual_visual_packet": case["actual_visual_packet"]}
                            if native
                            else {}
                        ),
                    }
                )
            check_properties = {
                "requirement_id": {"type": "string"},
                "matched": {"type": "boolean"},
                "evidence": {"type": "string"},
            }
            properties = {
                "id": {"type": "string", "enum": [case["id"] for case in cases]},
                "candidate": {"type": "string", "enum": ["p1", "p2"]},
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": list(check_properties),
                        "properties": check_properties,
                    },
                },
            }
            schema = {
                "type": "object",
                "additionalProperties": False,
                "required": ["records"],
                "properties": {
                    "records": {
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
                "protocol_freeze_sha256": freeze,
                "task": (
                    "Audit the ACTUAL frozen candidate observations against the preregistered "
                    "appearance requirements and original images. Judge whether the exact "
                    "concern is explicitly recognized, attributed to the right visible "
                    "object/relation and receives an appropriate positive component/score "
                    "penalty. You do the sensitive visual/semantic judging; the application "
                    "handles deterministic gate arithmetic. Do not rewrite predictions."
                ),
                "cases": cases,
                "constraints": (
                    "Do not retrofit scope or relax a preregistered requirement to hide a miss. "
                    "A different defect in the same component does not count as matching. "
                    "For EliteBook appearance requirements: front-edge visual disagreement "
                    "and upper CHAIR-backrest concern must be stated and penalized, even if "
                    "physical plausibility remains possible. A generic TABLE-construction "
                    "complaint is not the chair finding. No hard fail is required for minor "
                    "appearance concerns. An unsupported physical-axis accusation is not "
                    "needed. For Cashmere material alignment: detect the genuine rigid "
                    "product/table conflict, not harmless chair offset. Harmless chair offset "
                    "alone must not receive an adverse placement score. Preserve non-gold "
                    "control status; no held-out accuracy/false-positive-rate claim. C-Tech "
                    "supported requirements need specific evidence AND a corresponding "
                    "positive placement component and score below100, not a narrative-only "
                    "mention. ERROR/no prediction cannot match a required finding. A minor "
                    "penalty is not automatic FAIL. Do not reclassify unlisted lighting/brand/"
                    "wall-art taste concerns as required. For each candidate/case return "
                    "exactly its listed requirement IDs, including an empty checks list "
                    "when none are required. Be concise and retain honest disagreement."
                ),
            }
            if native:
                inputs["acquisition_trace_interpretation"] = (
                    "Inspect the same complete full-image/native-tile target coverage "
                    "used by the frozen runtime. Its acquisition records are fallible "
                    "unscored observations, never additional votes or penalties. "
                    "Explain in each check's evidence whether the exact relevant cue "
                    "was acquired, recognized or rebutted by each actual discovery/"
                    "verification branch, and retained or lost in the application-"
                    "selected result. Do not invent a finding absent from these actual "
                    "artifacts or infer that a literal cue alone establishes a defect."
                )
            cached = completed_packet(directory, inputs, schema)
            if cached is None:
                directory.mkdir()
                common.write_json(directory / "input.json", inputs)
                common.write_json(directory / "schema.json", schema)
            parts = [{"type": "text", "text": json.dumps(inputs)}]
            parts += audit_parts(cases)
            response, receipt = (
                cached
                if cached is not None
                else transport.model_completion(
                    [
                        {
                            "role": "system",
                            "content": "You are Astra, the HP placement output auditor. Evaluate actual visual evidence and exact concern attribution under the preregistered appearance standard. Do not force promotion or inflate confidence.",
                        },
                        {"role": "user", "content": parts},
                    ],
                    schema,
                    32768,
                    directory,
                )
            )
            Draft202012Validator(schema).validate(response)
            actual = {}
            for row in response["records"]:
                key = (row["id"], row["candidate"])
                if key in actual or len(
                    {check["requirement_id"] for check in row["checks"]}
                ) != len(row["checks"]):
                    raise ValueError("Duplicate feedback audit record/check")
                actual[key] = {check["requirement_id"] for check in row["checks"]}
            if actual != expected:
                raise ValueError(
                    "Audit omitted, added or relabeled preregistered checks"
                )
            common.write_json(directory / "result.json", response)
            common.write_json(directory / "receipt.json", receipt)
            runs.append(
                {
                    "dataset": dataset,
                    "input_path": str((directory / "input.json").resolve()),
                    "input_sha256": common.sha(directory / "input.json"),
                    "receipt": receipt,
                }
            )
            roster.update(actual)
            print(
                json.dumps(
                    {
                        "dataset": dataset,
                        "packet": packet_number,
                        "records_audited": len(actual),
                        "reused_actual_completed_packet": cached is not None,
                    }
                ),
                flush=True,
            )
    if len(roster) != 72:
        raise ValueError(
            "Expected all twelve calibration and sixty C-Tech candidate records"
        )
    common.write_json(
        audit_path,
        {
            "schema_version": "placement-feedback-coverage-v1",
            "protocol_freeze_sha256": freeze,
            "feedback_requirements_sha256": common.sha(
                version / "feedback_requirements.json"
            ),
            "runs": runs,
            "source_is_development_not_human_gold": True,
        },
    )
    print(json.dumps({"audit_complete": True, "candidate_records": len(roster)}))


if __name__ == "__main__":
    main()
