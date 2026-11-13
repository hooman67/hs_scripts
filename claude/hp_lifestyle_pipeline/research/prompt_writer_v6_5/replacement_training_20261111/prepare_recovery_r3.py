#!/usr/bin/env python3
"""Preserve the offline r2 preflight and isolate its carrier-grammar correction."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
BASE = VERSIONS / "v6_5_training_r2"
DEST = VERSIONS / "v6_5_training_r3"
STUDY = PROJECT / "eval_sets/hp_lifestyle_v6_5_training_four_devices_20261111"


def main():
    if DEST.exists() or (STUDY / "recover_text_r3.py").exists():
        raise FileExistsError("r3 recognition successor already exists")
    release = json.loads((BASE / "assets_manifest.json").read_text())
    for name, expected in release["files"].items():
        if hashlib.sha256((BASE / name).read_bytes()).hexdigest() != expected:
            raise ValueError("frozen offline r2 asset changed: " + name)
    shutil.copytree(BASE, DEST, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo", "assets_manifest.json",
    ))
    for path in DEST.rglob("*.py"):
        path.write_text(path.read_text().replace("v6_5_training_r2", "v6_5_training_r3").replace(
            "runtime-r2-astra-training-recognition", "runtime-r3-astra-training-recognition",
        ))
    for original, target in (
        ("recover_text.py", "recover_text_r3.py"), ("test_recovery.py", "test_recovery_r3.py"),
    ):
        text = (STUDY / original).read_text().replace(
            "v6_5_training_r2", "v6_5_training_r3",
        ).replace("20261111-r2-recovery", "20261111-r3-recovery").replace(
            "explicit-recovery-r2", "explicit-recovery-r3",
        ).replace("import recover_text as recovery", "import recover_text_r3 as recovery")
        with (STUDY / target).open("x") as stream:
            stream.write(text)
    path = DEST / "recognition_provenance.json"
    provenance = json.loads(path.read_text())
    provenance["offline_r2_candidate"] = str(BASE)
    provenance["offline_r2_manifest_sha256"] = hashlib.sha256((BASE / "assets_manifest.json").read_bytes()).hexdigest()
    provenance["offline_r2_extra_model_calls"] = 0
    provenance["r3_reason"] = "Preflight exposed ordinary carrier-location grammar rejected by r2; preserve r2 and correct before any paid recovery."
    path.write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"prepared_recognition_successor": str(DEST), "additional_model_calls": 0}))


if __name__ == "__main__":
    main()
