#!/usr/bin/env python3
"""Prepare an isolated recognition correction without changing paid evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
BASE = VERSIONS / "v6_5_training"
DEST = VERSIONS / "v6_5_training_r2"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(refresh_aliases=False):
    if DEST.exists() and not refresh_aliases:
        raise FileExistsError("recognition successor already exists")
    if refresh_aliases and (DEST / "assets_manifest.json").exists():
        raise FileExistsError("recognition successor is frozen")
    manifest = json.loads((BASE / "assets_manifest.json").read_text())
    for name, digest in manifest["files"].items():
        if sha(BASE / name) != digest:
            raise ValueError("frozen original runtime changed: " + name)
    if not refresh_aliases:
        shutil.copytree(BASE, DEST, ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", "*.pyc", "*.pyo", "assets_manifest.json",
        ))
        for path in DEST.rglob("*.py"):
            text = path.read_text().replace("versions.v6_5_training", "versions.v6_5_training_r2")
            text = text.replace("from v6_5_training", "from v6_5_training_r2")
            path.write_text(text)
    sys.path.insert(0, str(VERSIONS))
    from v6_5_training.catalog import _normalise_phrase, _plural_phrase
    path = DEST / "approved-v6.5-20261111.catalog.json"
    catalogue = json.loads(path.read_text())
    aliases = {
        "V61-OFF-042": ["clear architectural partition", "frosted architectural partition"],
        "V61-OFF-035": ["soft plaster", "pale brick", "board-formed concrete finish"],
        "V61-CAF-036": ["warm plaster", "exposed brick"],
        "V61-CAF-033": ["distant chalkboard menu", "chalkboard menu"],
        "V61-CAF-018": ["small unlabelled ceramic form", "unlabelled ceramic form", "ceramic forms"],
        "V61-STU-026": ["side cabinet", "drawer unit", "flat-file cabinet"],
        "V61-STU-027": ["shelves", "shelving"],
    }
    for entry in catalogue["entries"]:
        if entry["id"] in aliases:
            # These are concrete resolutions of the existing approved names,
            # not aliases borrowed from another member of a broad group.
            entry["aliases"] = sorted({
                variant for alias in aliases[entry["id"]]
                for phrase in [_normalise_phrase(alias)]
                for variant in (phrase, _plural_phrase(phrase))
            })
    path.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n")
    (DEST / "recognition_provenance.json").write_text(json.dumps({
        "original_runtime": str(BASE),
        "original_manifest_sha256": sha(BASE / "assets_manifest.json"),
        "original_native_outcome": {"successful_banks": 0, "failed_banks": 16, "semantic_calls": 32},
        "authorization": "Fix recognition; allow one extra repair per genuinely invalid bank",
        "maximum_extra_semantic_calls_per_invalid_bank": 1,
        "original_scene_fields_edited": False,
        "original_assets_overwritten": False,
        "concrete_alias_resolutions": aliases,
    }, indent=2) + "\n")
    print(json.dumps({"prepared_recognition_successor": str(DEST)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-unfrozen-aliases", action="store_true")
    main(parser.parse_args().refresh_unfrozen_aliases)
