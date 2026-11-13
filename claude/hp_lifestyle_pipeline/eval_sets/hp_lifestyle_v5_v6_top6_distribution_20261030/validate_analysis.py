#!/usr/bin/env python3
"""Validate the frozen V5/V6 top-96 distribution artifact before publication."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILT = HERE / "built"


def main() -> None:
    analysis = json.loads(
        (BUILT / "downloads/analysis.json").read_text(encoding="utf-8")
    )
    rows = analysis["rows"]
    assert len(rows) == 192
    assert len({row["versioned_key"] for row in rows}) == 192
    assert analysis["scope"] == {
        "versions": ["V5", "V6"],
        "prompt_count_per_version": 96,
        "total_prompt_rows": 192,
        "banks_per_version": 16,
        "prompts_per_bank": 6,
        "ctech_reference_count": 18,
    }
    expected_environments = {
        "V5": {"Café": 2, "Home": 46, "Office": 48},
        "V6": {
            "Café": 6,
            "Creative Studio": 19,
            "Education": 7,
            "Home": 19,
            "Office": 45,
        },
    }
    for version in ("V5", "V6"):
        version_rows = [row for row in rows if row["version"] == version]
        assert len(version_rows) == 96
        assert (
            len({(row["device_id"], row["camera_tag"]) for row in version_rows}) == 16
        )
        assert (
            analysis["summaries"][version]["environment_counts"]
            == expected_environments[version]
        )
        assert all(0 <= row["measured_ctech_similarity"] <= 1 for row in version_rows)
    references = analysis["references"]
    assert len(references) == 18
    assert all(
        "map_x" in reference and "map_y" in reference for reference in references
    )
    prop_audit = analysis["v6_prop_audit"]
    assert prop_audit["scope"] == {
        "all_prompt_rows": 160,
        "banks": 16,
        "prompts_per_bank": 10,
        "generated_preview_rows": 96,
        "rows_without_downstream_rewrite": 64,
    }
    full = prop_audit["full_160"]
    assert full["prompt_count"] == 160
    assert full["headline"] == {
        "unique_approved_prop_ids_used": 128,
        "approved_prop_assignments": 563,
        "unique_semantic_groups_used": 97,
    }
    assert full["environment_counts"] == {
        "Café": 20,
        "Creative Studio": 25,
        "Education": 20,
        "Gaming": 16,
        "Home": 28,
        "Office": 51,
    }
    full_signals = {item["label"]: item for item in full["feedback_signals"]}
    assert full_signals["Open notebook"]["declared_group_count"] == 15
    assert full_signals["Open notebook"]["explicit_input_phrase_count"] == 13
    assert full_signals["Stack of papers"]["declared_group_count"] == 15
    assert full_signals["Stack of papers"]["explicit_input_phrase_count"] == 13
    assert full_signals["Pencil/pen cup"]["explicit_input_phrase_count"] == 0
    assert len(full["upstream_props"]) == 128
    assert len(full["semantic_groups"]) == 97

    prop_usage = prop_audit["preview_96"]
    assert analysis["prop_usage"] == prop_usage
    assert prop_usage["scope"]["image_rows"] == 96
    assert prop_usage["headline"] == {
        "unique_approved_prop_ids_used": 95,
        "approved_prop_assignments": 329,
        "unique_semantic_groups_used": 76,
        "unique_rewriter_entity_labels": 170,
    }
    feedback = {item["label"]: item for item in prop_usage["feedback_comparison"]}
    assert feedback["Open notebook"]["declared_group_count"] == 14
    assert feedback["Open notebook"]["explicit_rewrite_phrase_count"] == 12
    assert feedback["Stack of papers"]["declared_group_count"] == 14
    assert feedback["Stack of papers"]["explicit_input_phrase_count"] == 13
    assert feedback["Stack of papers"]["explicit_rewrite_phrase_count"] == 14
    assert feedback["Pencil/pen cup"]["declared_group_count"] == 0
    assert feedback["Pencil/pen cup"]["explicit_rewrite_phrase_count"] == 0
    assert len(prop_usage["upstream_props"]) == 95
    assert len(prop_usage["semantic_groups"]) == 76
    assert len(prop_usage["downstream_entities"]) == 170
    categories = {
        item["label"]: item["category"] for item in prop_usage["downstream_entities"]
    }
    assert categories["desk calendar"] == "prop_or_furnishing"
    assert categories["office chair"] == "prop_or_furnishing"
    assert categories["studio stool"] == "prop_or_furnishing"
    assert categories["floor lamp"] == "prop_or_furnishing"
    assert categories["glass partitions"] == "architecture_or_setting"
    assert categories["large windows"] == "architecture_or_setting"

    additions = prop_audit["downstream_additions"]
    assert additions["version"] == "hp-v6-downstream-prop-additions-audit-v2"
    assert additions["scope"]["rows_audited"] == 96
    assert (
        additions["scope"][
            "rows_with_confirmed_downstream_prop_or_furnishing_additions"
        ]
        == 25
    )
    assert len(additions["rows"]) == 25
    assert len({row["prompt_key"] for row in additions["rows"]}) == 25
    stack = additions["summary"]["stack_of_papers_table_explanation"]
    assert stack["explicit_input_semantic_pattern_count"] == 13
    assert stack["explicit_rewrite_semantic_pattern_count"] == 14
    assert stack["actual_rewrite_only_keys"] == ["cashmere__laptop_FrontCloseUp::p3"]
    assert (BUILT / "downloads/v6_prop_usage.json").is_file()
    assert (BUILT / "downloads/v6_prop_usage.csv").is_file()
    assert (BUILT / "downloads/v6_prompts_all_160.json").is_file()
    assert (BUILT / "downloads/downstream_prop_additions_audit.json").is_file()
    data_js = (BUILT / "gallery/data.js").read_text(encoding="utf-8")
    assert data_js.startswith("const ANALYSIS=") and data_js.endswith(";\n")
    html = (BUILT / "gallery/index.html").read_text(encoding="utf-8")
    assert "V6 prop audit · all 160" in html
    assert "Items introduced by the downstream rewriter" in html
    assert "v6_prop_usage.json" in html and "v6_prop_usage.csv" in html
    assert "v6_prompts_all_160.json" in html
    assert "downstream_prop_additions_audit.json" in html
    for asset in ("data.js", "report.js", "style.css", "imsauth.js"):
        assert asset in html
        assert (BUILT / "gallery" / asset).is_file()
    manifest = json.loads((BUILT / "build_manifest.json").read_text(encoding="utf-8"))
    assert "build_manifest.json" not in manifest["artifacts"]
    for relative_path, metadata in manifest["artifacts"].items():
        path = BUILT / relative_path
        assert path.stat().st_size == metadata["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == metadata["sha256"]
    print(
        "Validated 192 comparison rows, all 160 V6 prop inputs, 96 downstream rewrites, 25 audited addition rows, and all gallery assets."
    )


if __name__ == "__main__":
    main()
