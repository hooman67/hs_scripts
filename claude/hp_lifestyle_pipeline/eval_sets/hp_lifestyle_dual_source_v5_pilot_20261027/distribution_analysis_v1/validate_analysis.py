#!/usr/bin/env python3
"""Validate the V5 distribution build before publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


EXPECTED_ENVIRONMENTS = {"Home", "Office", "Education", "Gaming", "Café", "Creative Studio"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("build", type=Path)
    args = parser.parse_args()
    root = args.build.resolve()
    analysis_path = root / "downloads/analysis.json"
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    points = analysis["points"]

    assert len(points) == analysis["scope"]["prompt_count"] == 160
    assert len({row["candidate_key"] for row in points}) == 160
    assert len({row["case_id"] for row in points}) == analysis["scope"]["case_count"] == 8
    assert set(Counter(row["case_id"] for row in points).values()) == {20}
    assert {row["environment"] for row in points} == EXPECTED_ENVIRONMENTS
    assert sum(row["selected"] for row in points) == 48
    assert all(sum(row["selected"] for row in points if row["case_id"] == case_id) == 6 for case_id in {row["case_id"] for row in points})
    assert all(row["selected"] == (row["rank"] <= 6) for row in points)
    assert all(0 <= row["source_relevance_score"] <= 100 for row in points)
    assert all(0 <= row["ctech_reference_score"] <= 100 for row in points)
    assert len(analysis["reference_coverage"]) == analysis["scope"]["reference_prompt_count"] == 18
    assert len(analysis["case_inputs"]) == 8
    assert all(case["smart_brief"] and case["source_messaging"] for case in analysis["case_inputs"])
    assert all(sum(bucket["count"] for bucket in analysis["distributions"][name]) == 160 for name in ("source_score_histogram", "score_histogram", "reference_similarity_histogram_scope_adjusted"))
    assert sum(analysis["distributions"]["display_environment"].values()) == 160
    assert sum(analysis["distributions"]["relationship"].values()) == 160
    assert analysis["selection_analysis"]["top6"]["count"] == 48
    assert analysis["review_accounting"]["model_normalized_validation_passes"] == 3
    assert analysis["review_accounting"]["reviewed_validation_passes"] == 8

    data_text = (root / "gallery/data.js").read_text(encoding="utf-8")
    assert data_text.startswith("const ANALYSIS = ") and data_text.endswith(";\n")
    embedded = json.loads(data_text[len("const ANALYSIS = "):-2])
    assert embedded == analysis

    html = (root / "gallery/index.html").read_text(encoding="utf-8")
    script = (root / "gallery/report.js").read_text(encoding="utf-8")
    html_ids = set(re.findall(r'id="([^"]+)"', html))
    requested_ids = set(re.findall(r'getElementById\("([^"]+)"\)', script))
    assert requested_ids <= html_ids, sorted(requested_ids - html_ids)
    for name in ("analysis.json", "pilot_prompts.txt", "pilot_prompts.json", "system_prompt.md", "candidate_metrics.csv", "lexical_audit.json", "reference_prompts.json"):
        assert (root / "downloads" / name).is_file()

    manifest = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    for relative, record in manifest["artifacts"].items():
        path = root / relative
        assert path.stat().st_size == record["bytes"]
        assert digest(path) == record["sha256"]
    print(json.dumps({"status": "pass", "prompts": len(points), "cases": len(analysis["case_inputs"]), "references": len(analysis["reference_coverage"]), "top6": sum(row["selected"] for row in points), "artifacts": len(manifest["artifacts"])}, indent=2))


if __name__ == "__main__":
    main()
