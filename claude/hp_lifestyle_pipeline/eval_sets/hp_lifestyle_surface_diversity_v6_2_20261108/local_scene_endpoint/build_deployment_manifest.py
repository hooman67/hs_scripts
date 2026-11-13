#!/usr/bin/env python3
"""Build the immutable wrapper/assets manifest without invoking generation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import endpoint

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record(relative: str) -> dict:
    path = HERE / relative
    return {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size}


def main() -> None:
    wrapper_files = [
        "endpoint.py",
        "prepare_input_bundle.py",
        "build_deployment_manifest.py",
        "preflight_provider.py",
        "launch_endpoint.sh",
        "endpoint-requirements.txt",
        "test_endpoint.py",
    ]
    reference_files = [
        "runtime/assets/styles.json",
        "runtime/hp3p/data/ref_captions.json",
        "runtime/assets/source_text_transfer_manifest.json",
        "runtime/assets/source_artifact_manifest.json",
    ]
    input_manifest = json.loads((HERE / "input_bundle/manifest.json").read_text(encoding="utf-8"))
    candidate = endpoint.lineage()
    candidate.pop("deploymentManifestSha256", None)
    value = {
        "schema_version": 1,
        "candidate": candidate,
        "generation_default_enabled": False,
        "network_default": {"host": "127.0.0.1", "port": 8137},
        "wrapper_files": [record(name) for name in wrapper_files],
        "reference_assets": [record(name) for name in reference_files],
        "fixed_input_bundle": {
            **record("input_bundle/manifest.json"),
            "view_count": len(input_manifest["entries"]),
            "views": [
                {
                    "digital_twin_id": item["digital_twin_id"],
                    "camera_id": item["camera_id"],
                    "product_sha256": item["product_sha256"],
                    "product_bytes": item["product_bytes"],
                    "control_record_sha256": item["control_record_sha256"],
                }
                for item in input_manifest["entries"]
            ],
        },
        "failed_smoke_evidence": record("failed_smoke_20261109_manifest.json"),
        "provider_credentials": "server-managed foundry_aws_gateway; no value stored in this tree",
        "paid_calls_during_preparation": 0,
    }
    path = HERE / "deployment_manifest.json"
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"deployment_manifest_sha256={sha256(path)}")


if __name__ == "__main__":
    main()
