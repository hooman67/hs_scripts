"""Freeze the exact candidates/gates before looking at new predictions."""

import json

import common


def main():
    common.LEGACY.verify_freeze()
    target = common.ROOT / "protocol_freeze.json"
    if target.exists():
        raise ValueError("Freeze already exists; revisions require a new version")
    inherited = json.loads((common.R1 / "protocol_freeze.json").read_text())
    paths = {item["path"] for item in inherited["files"]}
    paths.update(
        str(path.resolve())
        for path in common.ROOT.glob("*.py")
        if not path.name.startswith("test_")
    )
    paths.update(
        str(path.resolve()) for path in (common.ROOT / "prompts").glob("*.txt")
    )
    paths.update(
        str(common.ROOT / name) for name in ("promotion_gates.json", "preparation.json")
    )
    paths.update(
        str(common.R1 / name)
        for name in ("r2/calibration_manifest.json", "evaluation/inventory.json")
    )
    paths.add(str(common.ROOT / "calibration_manifest.json"))
    paths.add(str(common.ROOT / "runtime_preparation.json"))
    paths.add(str(common.ROOT / "evaluation/ctech/corpus.json"))
    paths.add(str(common.ROOT / "feedback_requirements.json"))
    paths.add(str(common.ROOT / "visual_policy.json"))
    paths.add(str(common.ROOT / "evaluation/visual_preflight.json"))
    paths.update(
        str(path.resolve())
        for path in (common.ROOT / "evaluation/visual_packets").glob("*/manifest.json")
    )
    correction = common.ROOT / "verifier_contract_correction"
    paths.update(str(path.resolve()) for path in correction.glob("**/*.json"))
    paths.update(str(path.resolve()) for path in correction.glob("**/*.jsonl"))
    common.write_json(
        target,
        {
            "protocol": common.ROOT.name,
            "actual_judge_model": common.MODEL,
            "reasoning_effort": "high",
            "weights_and_policy": "Unchanged frozen V3.1 deterministic scorer",
            "new_architectures": [
                "P1 complementary primaries/additions consensus",
                "P2 unconditional blind specialists/image reconciliation",
            ],
            "files": [
                {"path": path, "sha256": common.sha(path)} for path in sorted(paths)
            ],
        },
    )
    print(common.verify_freeze())


if __name__ == "__main__":
    main()
