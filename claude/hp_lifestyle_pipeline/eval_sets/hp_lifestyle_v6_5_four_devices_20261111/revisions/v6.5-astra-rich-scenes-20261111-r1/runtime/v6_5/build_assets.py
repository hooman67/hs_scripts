#!/usr/bin/env python3
"""Verify the V6.4 predecessor and freeze the isolated Astra-authored V6.5 assets."""
import hashlib
import json
from pathlib import Path

from catalog import validate_catalog

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_4"
IMMUTABLE_ASSETS = (
    "camera.py", "content_policy.py", "input.schema.json", "model_output.schema.json",
    "reference_library.json", "source_inputs.py", "surfaces.py",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    baseline = json.loads((HERE / "baseline_manifest.json").read_text())
    for name, expected in baseline["files"].items():
        if digest(BASE / name) != expected:
            raise ValueError(f"frozen V6.4 file changed: {name}")
    for name in IMMUTABLE_ASSETS:
        if digest(HERE / name) != baseline["files"][name]:
            raise ValueError(f"V6.5 changed an immutable predecessor contract: {name}")
    provenance = json.loads((HERE / "authoring_provenance.json").read_text())
    if digest(provenance["astra_proposal_path"]) != provenance["astra_proposal_sha256"]:
        raise ValueError("Astra design evidence changed")
    if digest(HERE / "system_prompt.md") != provenance["current_system_prompt_sha256"]:
        raise ValueError("system prompt no longer equals the exact Astra patches")
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
        "version": "v6.5-astra-rich-scenes-20261111-r1",
        "baseline": baseline, "files": assets,
        "unchanged_assets": list(IMMUTABLE_ASSETS),
        "authoring_provenance_sha256": digest(HERE / "authoring_provenance.json"),
        "human_image_acceptance_claimed": False,
    }, indent=2) + "\n")
    print(json.dumps({"assets": len(assets), "approved_entries": len(catalogue["entries"])}))


if __name__ == "__main__":
    main()
