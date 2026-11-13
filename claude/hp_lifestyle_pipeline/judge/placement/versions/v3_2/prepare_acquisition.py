"""Extract Astra's actual acquisition-and-tiles successor without editing its prompts."""

import argparse
import json
import shutil
from importlib.metadata import version

import common
from appearance_feedback import replay
from feedback_requirements import verify_requirements
from revise import ROLES

SOURCE = common.ROOT.parent / "v3_2_r3"
TARGET = common.ROOT.parent / "v3_2_r4"


def prepare():
    if TARGET.exists():
        raise ValueError("Successor exists; do not overwrite")
    for item in json.loads((SOURCE / "protocol_freeze.json").read_text())["files"]:
        if common.sha(item["path"]) != item["sha256"]:
            raise ValueError("Frozen predecessor changed")
    directory = SOURCE / "astra_successor_consult"
    proposal = json.loads((directory / "proposal.json").read_text())
    receipt = json.loads((directory / "receipt.json").read_text())
    if replay(receipt).result() != proposal or not proposal["successor_justified"]:
        raise ValueError("No actual justified Astra successor")
    prompts = proposal["revised_prompts"]
    runtime = proposal["runtime_change_required"]
    acquisition = runtime["acquisition_phase"]["prompt"]
    if (
        not runtime["required"]
        or set(prompts) != set(ROLES)
        or not isinstance(acquisition, str)
        or len(acquisition.strip()) < 400
    ):
        raise ValueError("Incomplete actual acquisition policy")
    requirements = json.loads((SOURCE / "feedback_requirements.json").read_text())
    verify_requirements(
        requirements, json.loads((SOURCE / "evaluation/ctech/corpus.json").read_text())
    )
    TARGET.mkdir()
    copies = {}
    for name in (
        "common.py",
        "p1.py",
        "p2.py",
        "evaluate.py",
        "freeze.py",
        "refiner.py",
        "transport.py",
        "test_common.py",
        "test_p2.py",
        "test_transport.py",
        "test_calibration.py",
    ):
        source, target = SOURCE / name, TARGET / name
        text = source.read_text()
        text = text.replace("placement-v3.2-p1-r3", "placement-v3.2-p1-r4")
        text = text.replace("placement-v3.2-p2-r3", "placement-v3.2-p2-r4")
        target.write_text(text)
        copies[name] = {"source_path": str(source), "source_sha256": common.sha(source)}
    (TARGET / "prompts").mkdir()
    for role, text in {**prompts, "visual_acquisition": acquisition}.items():
        if not isinstance(text, str) or len(text.strip()) < 400:
            raise ValueError("Missing complete actual prompt")
        (TARGET / "prompts" / (role + ".txt")).write_text(text)
    for name in (
        "calibration_manifest.json",
        "feedback_requirements.json",
        "evaluation/ctech/corpus.json",
        "evaluation/refiner/corpus.json",
        "evaluation/refiner/source/data.json",
        "evaluation/refiner/source/object.json",
    ):
        target = TARGET / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / name, target)
    gates = json.loads((SOURCE / "promotion_gates.json").read_text())
    gates.update(
        candidate_protocol="v3.2-p1-p2-r4-acquisition-tiles-appearance-review",
        calibration_manifest=str(TARGET / "calibration_manifest.json"),
        predecessor={
            "path": str(SOURCE),
            "freeze_sha256": common.sha(SOURCE / "protocol_freeze.json"),
        },
    )
    common.write_json(TARGET / "promotion_gates.json", gates)
    common.write_json(
        TARGET / "visual_policy.json",
        {
            "tile_size_pixels": 768,
            "overlap_pixels": 192,
            "max_encoded_image_bytes": 45_000_000,
            "acquisition_completion_tokens": 12000,
            "all_full_images_retained": True,
            "image_adapter_detail": "high",
            "actual_astra_runtime_policy": runtime,
            "decoded_pixel_crops_only": True,
            "no_case_specific_region_selection": True,
        },
    )
    common.write_json(
        TARGET / "preparation.json",
        {
            "prompt_source_path": str(directory / "proposal.json"),
            "prompt_source_sha256": common.sha(directory / "proposal.json"),
            "actual_astra_receipt": receipt,
            "runtime_change_required": runtime,
            "source_version": str(SOURCE),
            "code_copies": copies,
            "preregistered_feedback_requirements_unchanged": True,
            "original_physical_gate_not_retroactively_met": True,
        },
    )
    common.write_json(
        TARGET / "runtime_preparation.json",
        {
            "status": "implementation_in_progress_before_freeze",
            "source_version": str(SOURCE),
            "source_protocol_sha256": common.sha(SOURCE / "protocol_freeze.json"),
            "prompts_extracted_unchanged": True,
            "code_copies": copies,
        },
    )
    print(TARGET)


def finalize():
    if (TARGET / "protocol_freeze.json").exists():
        raise ValueError("Frozen runtime cannot be changed")
    preparation = json.loads((TARGET / "preparation.json").read_text())
    proposal = json.loads(
        (SOURCE / "astra_successor_consult/proposal.json").read_text()
    )
    if replay(preparation["actual_astra_receipt"]).result() != proposal:
        raise ValueError("Actual prompt source changed")
    for role, text in {
        **proposal["revised_prompts"],
        "visual_acquisition": proposal["runtime_change_required"]["acquisition_phase"][
            "prompt"
        ],
    }.items():
        if (TARGET / "prompts" / (role + ".txt")).read_text() != text:
            raise ValueError("Extracted prompt differs from actual Astra output")
    if common.sha(TARGET / "feedback_requirements.json") != common.sha(
        SOURCE / "feedback_requirements.json"
    ):
        raise ValueError("Preregistered requirements changed")
    runtime = json.loads((TARGET / "runtime_preparation.json").read_text())
    runtime["status"] = "prepared_before_protocol_freeze"
    runtime["final_runtime_files"] = {
        path.name: common.sha(path)
        for path in TARGET.glob("*.py")
        if not path.name.startswith("test_")
    }
    runtime["packages"] = {
        name: version(name)
        for name in ("openai", "foundry-aws-gateway", "jsonschema", "pillow")
    }
    common.write_json(TARGET / "runtime_preparation.json", runtime)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "finalize"))
    args = parser.parse_args()
    {"prepare": prepare, "finalize": finalize}[args.command]()


if __name__ == "__main__":
    main()
