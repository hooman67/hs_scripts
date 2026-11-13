#!/usr/bin/env python3
"""Verify the frozen predecessor and record V6.4 asset hashes; do not rebuild props."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_3"
IMMUTABLE_ASSETS = (
    "approved-v6.3-20261109.catalog.json", "approved_additions.csv",
    "camera.py", "camera_profiles.json", "catalog.py", "content_policy.py",
    "input.schema.json", "model_output.schema.json", "prop_lexicon.json",
    "reference_library.json", "surfaces.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    baseline = json.loads((HERE / "baseline_manifest.json").read_text())
    for name, expected in baseline["files"].items():
        if digest(BASE / name) != expected:
            raise ValueError(f"frozen V6.3 file changed: {name}")
    for name in IMMUTABLE_ASSETS:
        if digest(HERE / name) != baseline["files"][name]:
            raise ValueError(f"V6.4 altered an unchanged V6.3 asset: {name}")
    assets = {
        str(path.relative_to(HERE)): digest(path)
        for path in sorted(HERE.rglob("*"))
        if path.is_file() and path.name != "assets_manifest.json"
        and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }
    (HERE / "assets_manifest.json").write_text(json.dumps({
        "version": "v6.4-structured-sources-20261110-r1",
        "baseline": baseline, "files": assets,
        "unchanged_assets": list(IMMUTABLE_ASSETS),
    }, indent=2) + "\n")
    print(json.dumps({"assets": len(assets), "unchanged_v63_files": len(baseline["files"])}))


if __name__ == "__main__":
    main()
