#!/usr/bin/env python3
"""Isolate two proven recognition defects; preserve all completed paid replies."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
BASE = PROJECT / "research/source_messaging_v1_to_v6/versions/v6_5_training_r3"
DEST = BASE.with_name("v6_5_training_r4")


def main():
    if DEST.exists():
        raise FileExistsError("offline revalidation successor already exists")
    release = json.loads((BASE / "assets_manifest.json").read_text())
    for name, expected in release["files"].items():
        if hashlib.sha256((BASE / name).read_bytes()).hexdigest() != expected:
            raise ValueError("paid r3 recognition asset changed: " + name)
    shutil.copytree(BASE, DEST, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo", "assets_manifest.json",
    ))
    for path in DEST.rglob("*.py"):
        path.write_text(path.read_text().replace("v6_5_training_r3", "v6_5_training_r4").replace(
            "runtime-r3-astra-training-recognition", "runtime-r4-astra-training-recognition",
        ))
    path = DEST / "approved-v6.5-20261111.catalog.json"
    catalogue = json.loads(path.read_text())
    aliases = ["dark plaster", "brick texture", "brick textures", "concrete texture", "concrete textures"]
    for entry in catalogue["entries"]:
        if entry["id"] == "V61-GAM-035":
            entry["aliases"] = aliases
    path.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n")
    path = DEST / "recognition_provenance.json"
    provenance = json.loads(path.read_text())
    provenance["concrete_alias_resolutions"]["V61-GAM-035"] = aliases
    provenance["paid_r3_runtime"] = str(BASE)
    provenance["paid_r3_manifest_sha256"] = hashlib.sha256((BASE / "assets_manifest.json").read_bytes()).hexdigest()
    provenance["bounded_recovery_outcome"] = {"successful_banks": 14, "failed_banks": 2, "extra_semantic_calls": 15}
    provenance["r4_reason"] = (
        "Resolve an eighth existing alternative-form alias and preserve character offsets/"
        "antecedents when masking the primary counter before inventory checks. "
        "Revalidate the same actual final r3 replies; no additional model calls."
    )
    path.write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"prepared_recognition_successor": str(DEST), "additional_model_calls": 0}))


if __name__ == "__main__":
    main()
