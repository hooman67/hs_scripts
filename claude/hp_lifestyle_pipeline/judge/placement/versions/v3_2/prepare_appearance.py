"""Prepare isolated successor code and extract only actual Astra-authored prompts."""

import argparse
import ast
import json
import shutil

import common
from appearance_feedback import OUTPUT, USER_STANDARD

SOURCE = common.ROOT.parent / "v3_2_r2"
TARGET = common.ROOT.parent / "v3_2_r3"


def replace_function(text, name, replacement):
    functions = [
        node
        for node in ast.parse(text).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(functions) != 1:
        raise ValueError("Expected one exact source function: " + name)
    function = functions[0]
    lines = text.splitlines(keepends=True)
    return (
        "".join(lines[: function.lineno - 1])
        + replacement
        + "\n\n"
        + "".join(lines[function.end_lineno :])
    )


def core():
    if TARGET.exists():
        raise ValueError("Successor directory exists; do not overwrite it")
    frozen = json.loads((SOURCE / "protocol_freeze.json").read_text())
    for dependency in frozen["files"]:
        if common.sha(dependency["path"]) != dependency["sha256"]:
            raise ValueError("Predecessor changed since evaluation")
    TARGET.mkdir()
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
        old, new = SOURCE / name, TARGET / name
        text = old.read_text().replace("placement-v3.2-p1-r2", "placement-v3.2-p1-r3")
        text = text.replace("placement-v3.2-p2-r2", "placement-v3.2-p2-r3")
        if name == "common.py":
            text = replace_function(
                text,
                "model_completion",
                "def model_completion(messages, schema, cap, output, client=None):\n"
                "    import transport\n\n"
                "    return transport.model_completion(messages, schema, cap, output, client)",
            )
            text = text.replace("import threading\n", "").replace(
                "from datetime import UTC, datetime\n", ""
            )
            text = text.replace("import time\n", "")
        elif name == "p2.py":
            if text.count("cap=6000") != 1:
                raise ValueError("Unexpected reconciler cap source")
            text = text.replace("cap=6000", "cap=12000")
        elif name == "evaluate.py":
            text = text.replace(
                'common.R1 / "r2/calibration_manifest.json"',
                'common.ROOT / "calibration_manifest.json"',
            )
            old_check = "        else:\n            code = {\n"
            if text.count(old_check) != 1:
                raise ValueError("Unexpected calibration checker source")
            text = text.replace(
                old_check,
                '        elif expectation.startswith("appearance_"):\n'
                "            code = {\n"
                '                "appearance_furniture_axis_conflict": "furniture_axis_conflict",\n'
                '                "appearance_malformed_support_furniture": "malformed_support_furniture",\n'
                "            }[expectation]\n"
                '            checks[name + ":" + expectation] = (\n'
                '                component["visibility"] in {"observed", "partial"}\n'
                '                and component["severity"] is not None\n'
                '                and component["severity"] >= 1\n'
                '                and code in component["issue_codes"]\n'
                '                and result["application_merged_judgment"]["natural_placement_score"] < 100\n'
                "            )\n" + old_check,
            )
            text = text.replace(
                'choices=("calibration", "historical")',
                'choices=("calibration", "historical", "ctech")',
            )
            text = text.replace(
                '        else common.R1 / "evaluation/inventory.json"\n',
                '        else common.ROOT / "evaluation/ctech/corpus.json"\n'
                '        if args.dataset == "ctech"\n'
                '        else common.R1 / "evaluation/inventory.json"\n',
            )
            text = text.replace(
                '"source_stage": "e2e_comparison_output",',
                '"source_stage": "scene_generation" if args.dataset == "ctech" else "e2e_comparison_output",',
            )
            old_summary = (
                '    summary["all_stated_checks_matched"] = summary["complete"] and all(\n'
                '        all(row["checks"].values()) for row in rows if row["checks"] is not None\n'
                "    )\n"
            )
            if text.count(old_summary) != 1:
                raise ValueError("Unexpected source coverage-summary calculation")
            text = text.replace(
                old_summary,
                '    summary["all_stated_checks_matched"] = (\n'
                '        None if args.dataset == "ctech" else summary["complete"] and all(\n'
                '            all(row["checks"].values()) for row in rows if row["checks"] is not None\n'
                "        )\n"
                "    )\n"
                '    if args.dataset == "ctech":\n'
                '        summary["ctech_feedback_coverage_audited"] = False\n',
            )
        elif name == "freeze.py":
            text = text.replace(
                '    correction = common.ROOT / "verifier_contract_correction"\n',
                '    paths.add(str(common.ROOT / "calibration_manifest.json"))\n'
                '    paths.add(str(common.ROOT / "runtime_preparation.json"))\n'
                '    paths.add(str(common.ROOT / "evaluation/ctech/corpus.json"))\n'
                '    paths.add(str(common.ROOT / "feedback_requirements.json"))\n'
                '    correction = common.ROOT / "verifier_contract_correction"\n',
            )
        elif name == "test_common.py":
            text = text.replace("import pytest\n", "import pytest\nimport transport\n")
            text = text.replace("common.time", "transport.time")
        elif name == "test_p2.py":
            text = text.replace("[12000, 12000, 6000]", "[12000, 12000, 12000]")
        new.write_text(text)
        copies[name] = {
            "source_path": str(old),
            "source_sha256": common.sha(old),
            "initial_output_sha256": common.sha(new),
        }
    shutil.copy2(common.ROOT / "transport.py", TARGET / "transport.py")
    shutil.copy2(common.ROOT / "test_transport.py", TARGET / "test_transport.py")
    manifest = json.loads((common.R1 / "r2/calibration_manifest.json").read_text())
    original_sha = common.sha(common.R1 / "r2/calibration_manifest.json")
    for case in manifest["cases"]:
        if case["id"] == "13_elitebook_13_Front_Left_Medium_4":
            case["previous_frozen_expectation"] = case["expectation"]
            case["expectation"] = {
                "orientation_alignment": "appearance_furniture_axis_conflict",
                "scale_perspective": "appearance_malformed_support_furniture",
            }
    manifest["appearance_review_revision"] = {
        "user_standard": USER_STANDARD,
        "original_manifest_path": str(common.R1 / "r2/calibration_manifest.json"),
        "original_manifest_sha256": original_sha,
        "meaning": (
            "User-authorized appearance/penalty expectations, not retrospective recovery "
            "of the original material-construction/no-orientation gate. Old labels/results "
            "remain unchanged and old candidates remain unpromoted."
        ),
        "semantic_attribution_requires_astra_review": True,
    }
    common.write_json(TARGET / "calibration_manifest.json", manifest)
    for name in ("corpus.json", "source/data.json", "source/object.json"):
        destination = TARGET / "evaluation/refiner" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / "evaluation/refiner" / name, destination)
    destination = TARGET / "evaluation/ctech/corpus.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT / "corpus.json", destination)
    common.write_json(
        TARGET / "runtime_preparation.json",
        {
            "source_version": str(SOURCE),
            "source_protocol_sha256": common.sha(SOURCE / "protocol_freeze.json"),
            "code_copies": copies,
            "transport_source_sha256": common.sha(common.ROOT / "transport.py"),
            "mechanical_changes": [
                "New versioned protocol names; existing scorer/schemas/consensus remain unchanged.",
                "Local versioned calibration with user-confirmed appearance penalty expectations.",
                "New transport preserves completed stop through close failures and structured server-error recovery.",
                "P2 reconciler cap12000 rather than6000; old length failure remains unchanged.",
            ],
            "frozen": False,
            "prompts_extracted": False,
        },
    )
    print(TARGET)


def extract():
    directory = OUTPUT / "synthesis"
    proposal = json.loads((directory / "proposal.json").read_text())
    receipt = json.loads((directory / "receipt.json").read_text())
    if common.sha(receipt["chunks_path"]) != receipt["chunks_sha256"]:
        raise ValueError("Prompt-authoring source stream changed")
    collector = common.Collector()
    from pathlib import Path

    with Path(receipt["chunks_path"]).open() as stream:
        for line in stream:
            collector.feed(json.loads(line))
    if collector.result() != proposal:
        raise ValueError("Prompts differ from the actual Astra response")
    if (TARGET / "protocol_freeze.json").exists() or (TARGET / "prompts").exists():
        raise ValueError("Successor prompts already exist or are frozen")
    runtime = json.loads((TARGET / "runtime_preparation.json").read_text())
    runtime["final_runtime_files"] = {
        path.name: common.sha(path)
        for path in TARGET.glob("*.py")
        if not path.name.startswith("test_")
    }
    runtime["preparation_helper_sha256"] = common.sha(__file__)
    common.write_json(TARGET / "runtime_preparation.json", runtime)
    (TARGET / "prompts").mkdir()
    for role, text in proposal["revised_prompts"].items():
        (TARGET / "prompts" / (role + ".txt")).write_text(text)
    common.write_json(
        TARGET / "preparation.json",
        {
            "actual_astra_receipt": receipt,
            "prompt_source_path": str(directory / "proposal.json"),
            "prompt_source_sha256": common.sha(directory / "proposal.json"),
            "user_confirmed_standard": USER_STANDARD,
            "original_physical_gate_not_retroactively_met": True,
            "change_hypothesis": proposal["change_hypothesis"],
        },
    )
    gates = json.loads((SOURCE / "promotion_gates.json").read_text())
    gates.update(
        candidate_protocol="v3.2-p1-p2-r3-appearance-review",
        calibration_manifest=str(TARGET / "calibration_manifest.json"),
        calibration_sha256=common.sha(TARGET / "calibration_manifest.json"),
        criterion_mode="appearance_review",
        required_criteria=(
            "Preserve genuine Cashmere material alignment detection and harmless chair-offset "
            "tolerance. Catch both user-localized EliteBook appearance concerns with positive "
            "component evidence/codes and score deductions; no forced material fail. Original "
            "physical gate remains unmet by predecessors and is not relabeled as recovered."
        ),
        ctech_source_cases=30,
        semantic_attribution_requires_astra_review=True,
        evidence_disagreements=(
            "Astra audits whether predictions actually address the localized human concerns "
            "and relevant new C-Tech comments. Whole-image FAIL/OK is not placement gold; "
            "unsupported/out-of-scope interpretations remain explicit."
        ),
        predecessor={
            "path": str(SOURCE),
            "freeze_sha256": common.sha(SOURCE / "protocol_freeze.json"),
        },
    )
    common.write_json(TARGET / "promotion_gates.json", gates)
    print(json.dumps({"prompts_extracted": True, "version": str(TARGET)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("core", "extract"))
    args = parser.parse_args()
    {"core": core, "extract": extract}[args.command]()


if __name__ == "__main__":
    main()
