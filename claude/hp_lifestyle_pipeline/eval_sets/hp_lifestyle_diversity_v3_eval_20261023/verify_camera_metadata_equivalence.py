#!/usr/bin/env python3
"""Prove metadata-aware finalization is byte-equivalent on all 18 approved banks."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V3 = ROOT / "research/source_messaging_v1_to_v6/versions/v3"
sys.path.insert(0, str(V3 / "scripts"))
from camera_profile_resolver import load_registry  # noqa: E402
from finalize_output import finalize_output  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rendered(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def main() -> None:
    archived_path = V3 / "experiments/finalizer_v1_exact/finalize_output.py"
    spec = importlib.util.spec_from_file_location("archived_finalizer_v1", archived_path)
    archived = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(archived)
    registry = load_registry(V3 / "camera_profiles.json")
    accepted_path = HERE / "accepted_prompt_cases.json"
    selection_path = HERE / "selection_manifest.json"
    accepted_before, selection_before = sha(accepted_path), sha(selection_path)
    accepted = json.loads(accepted_path.read_text())
    cases = []
    for case_id, case in sorted(accepted["cases"].items()):
        record_path = Path(case["record_path"])
        normalized_path = Path(case["normalized_output_path"])
        log_path = Path(case["normalization_log_path"])
        record = json.loads(record_path.read_text())
        raw_input = json.loads(record["raw_input_json"])
        legacy_output, legacy_log = archived.finalize_output(record["parsed_output"])
        enhanced_output, enhanced_log = finalize_output(record["parsed_output"],
                                                         raw_input=raw_input, registry=registry)
        if enhanced_output != legacy_output or enhanced_log != legacy_log:
            raise RuntimeError(f"metadata-aware finalizer changed approved case: {case_id}")
        if rendered(enhanced_output) != normalized_path.read_bytes():
            raise RuntimeError(f"normalized output bytes changed: {case_id}")
        if rendered(enhanced_log) != log_path.read_bytes():
            raise RuntimeError(f"normalization log bytes changed: {case_id}")
        if "camera_metadata_repair" in enhanced_log:
            raise RuntimeError(f"unexpected production camera repair: {case_id}")
        cases.append({"case_id": case_id, "record_sha256": sha(record_path),
                      "normalized_output_sha256": sha(normalized_path),
                      "normalization_log_sha256": sha(log_path), "byte_equivalent": True})
    if sha(accepted_path) != accepted_before or sha(selection_path) != selection_before:
        raise RuntimeError("accepted/selection artifact changed during read-only proof")
    report = {"version": "v3-finalizer-camera-metadata-equivalence-v1", "passed": True,
              "approved_case_count": len(cases), "camera_repairs_in_production": 0,
              "archived_finalizer_path": str(archived_path), "archived_finalizer_sha256": sha(archived_path),
              "enhanced_finalizer_path": str(V3 / "scripts/finalize_output.py"),
              "enhanced_finalizer_sha256": sha(V3 / "scripts/finalize_output.py"),
              "accepted_prompt_cases_sha256": accepted_before,
              "selection_manifest_sha256": selection_before, "cases": cases}
    target = HERE / "finalizer_camera_metadata_equivalence.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"passed": True, "cases": len(cases),
                      "report": str(target), "report_sha256": sha(target)}, indent=2))


if __name__ == "__main__":
    main()
