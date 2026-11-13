#!/usr/bin/env python3
"""Freeze exact Astra authorship, declared engineering deltas and predecessors."""
import hashlib
import json
from pathlib import Path

from catalog import validate_catalog

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_5_training"
REJECTED = HERE.parent / "v6_5"
IMMUTABLE_ASSETS = (
    "camera.py", "input.schema.json", "model_output.schema.json", "reference_library.json",
    "source_inputs.py", "surfaces.py",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if (HERE / "assets_manifest.json").exists():
        raise FileExistsError("recognition successor is already frozen")
    recognition = json.loads((HERE / "recognition_provenance.json").read_text())
    offline = Path(recognition["offline_r2_candidate"])
    if digest(offline / "assets_manifest.json") != recognition["offline_r2_manifest_sha256"]:
        raise ValueError("offline r2 preflight manifest changed")
    for name, expected in json.loads((offline / "assets_manifest.json").read_text())["files"].items():
        if digest(offline / name) != expected:
            raise ValueError("offline r2 preflight asset changed: " + name)
    if digest(BASE / "assets_manifest.json") != recognition["original_manifest_sha256"]:
        raise ValueError("native trial asset manifest changed")
    for name, expected in json.loads((BASE / "assets_manifest.json").read_text())["files"].items():
        if digest(BASE / name) != expected:
            raise ValueError("frozen native trial runtime changed: " + name)
    provenance = json.loads((HERE / "authoring_provenance.json").read_text())
    if digest(REJECTED / "assets_manifest.json") != provenance["rejected_predecessor_asset_manifest_sha256"]:
        raise ValueError("rejected predecessor manifest changed")
    predecessor = json.loads((REJECTED / "assets_manifest.json").read_text())
    for name, expected in predecessor["files"].items():
        if digest(REJECTED / name) != expected:
            raise ValueError("rejected predecessor changed: " + name)
    for name in IMMUTABLE_ASSETS:
        if digest(HERE / name) != digest(BASE / name):
            raise ValueError("immutable support/schema/source/camera contract changed: " + name)
    proposal_path = Path(provenance["astra_proposal_path"])
    if digest(proposal_path) != provenance["astra_proposal_sha256"]:
        raise ValueError("actual Astra design changed")
    proposal = json.loads(proposal_path.read_text())
    if (
        (HERE / "system_prompt.md").read_text() != proposal["system_prompt"]
        or (HERE / "repair_addendum.txt").read_text() != proposal["repair_instruction"]
        or json.loads((HERE / "bank_policy.json").read_text()) != proposal["bank_policy"]
    ):
        raise ValueError("replacement text or policy differs from actual Astra authorship")
    catalogue = json.loads((HERE / "approved-v6.5-20261111.catalog.json").read_text())
    validate_catalog(catalogue)
    original_catalogue = json.loads((BASE / "approved-v6.5-20261111.catalog.json").read_text())
    if {key: value for key, value in catalogue.items() if key != "entries"} != {
        key: value for key, value in original_catalogue.items() if key != "entries"
    }:
        raise ValueError("recognition correction changed catalogue identity")
    for current, original in zip(catalogue["entries"], original_catalogue["entries"], strict=True):
        if {key: value for key, value in current.items() if key != "aliases"} != {
            key: value for key, value in original.items() if key != "aliases"
        }:
            raise ValueError("recognition correction changed an approved prop or its role")
        if current["id"] not in recognition["concrete_alias_resolutions"] and current != original:
            raise ValueError("unreviewed alias change: " + current["id"])
    for name in (
        "system_prompt.md", "repair_addendum.txt", "bank_policy.json",
        "prop_guidance.json", "camera_profiles.json", "prop_lexicon.json",
    ):
        if digest(HERE / name) != digest(BASE / name):
            raise ValueError("authored instructions or camera/detection configuration changed: " + name)
    assets = {
        str(path.relative_to(HERE)): digest(path)
        for path in sorted(HERE.rglob("*"))
        if path.is_file() and path.name != "assets_manifest.json"
        and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }
    (HERE / "assets_manifest.json").write_text(json.dumps({
        "version": "v6.5-astra-training-20261111-r3-recognition", "files": assets,
        "unchanged_assets": list(IMMUTABLE_ASSETS),
        "authorized_engineering_changes": [
            "Seven precise existing-form alias resolutions; no new approvals",
            "Bounded definite references after a valid concrete declaration",
            "Furniture accessories and negated/secondary support-role recognition",
            "Local annotation/writing safeguards and declared board-content relationships",
            "Depicted botanical subjects versus physical props; bounded carrier grammar",
            "Unresolved choices remain invalid after earlier unrelated negated text",
        ],
        "recognition_provenance_sha256": digest(HERE / "recognition_provenance.json"),
        "native_trial_successful_banks": 0, "native_trial_failed_banks": 16,
        "authoring_provenance_sha256": digest(HERE / "authoring_provenance.json"),
        "human_image_acceptance_claimed": False,
    }, indent=2) + "\n")
    print(json.dumps({"assets": len(assets), "approved_entries": len(catalogue["entries"])}))


if __name__ == "__main__":
    main()
