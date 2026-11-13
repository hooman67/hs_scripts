#!/usr/bin/env python3
"""Freeze exact Astra authorship, declared engineering deltas and predecessors."""
import hashlib
import json
from pathlib import Path

from catalog import validate_catalog

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_5"
IMMUTABLE_ASSETS = (
    "camera.py", "input.schema.json", "model_output.schema.json", "reference_library.json",
    "source_inputs.py", "surfaces.py",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    provenance = json.loads((HERE / "authoring_provenance.json").read_text())
    if digest(BASE / "assets_manifest.json") != provenance["rejected_predecessor_asset_manifest_sha256"]:
        raise ValueError("rejected predecessor manifest changed")
    predecessor = json.loads((BASE / "assets_manifest.json").read_text())
    for name, expected in predecessor["files"].items():
        if digest(BASE / name) != expected:
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
    assets = {
        str(path.relative_to(HERE)): digest(path)
        for path in sorted(HERE.rglob("*"))
        if path.is_file() and path.name != "assets_manifest.json"
        and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }
    (HERE / "assets_manifest.json").write_text(json.dumps({
        "version": "v6.5-astra-training-20261111-r1", "files": assets,
        "unchanged_assets": list(IMMUTABLE_ASSETS),
        "authorized_engineering_changes": [
            "Concrete-object inventory instead of within/across-scene group exclusivity",
            "Entry-owned aliases, exact mention-form binding and explicit carrier contents",
            "No people/cropped limbs and no additional electronic accessories",
            "Object-attached paper/art safeguards and two narrow repeatable safety phrases",
            "Cited substantive printer setting support and secondary-furniture role recognition",
        ],
        "authoring_provenance_sha256": digest(HERE / "authoring_provenance.json"),
        "human_image_acceptance_claimed": False,
    }, indent=2) + "\n")
    print(json.dumps({"assets": len(assets), "approved_entries": len(catalogue["entries"])}))


if __name__ == "__main__":
    main()
