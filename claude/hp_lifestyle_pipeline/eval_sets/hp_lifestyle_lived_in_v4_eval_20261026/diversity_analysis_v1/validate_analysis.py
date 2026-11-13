#!/usr/bin/env python3
"""Validate the isolated V4 distribution report without publication calls."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
EVAL = ROOT / "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026"
HERE = EVAL / "diversity_analysis_v1"
OUTPUT = ROOT / "local_data/reports/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1"
REPORT = HERE / "local_validation.json"
EXPECTED_ENVIRONMENTS = {"Home", "Office", "Education", "Gaming", "Café", "Creative Studio"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class HtmlInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))


def publisher_files() -> set[str]:
    tree = ast.parse((HERE / "publish_analysis.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "FILES" for target in node.targets):
            return set(ast.literal_eval(node.value))
    raise ValueError("publisher FILES allowlist not found")


def main() -> int:
    checks: list[str] = []

    def require(value: bool, message: str) -> None:
        if not value:
            raise ValueError(message)
        checks.append(message)

    try:
        manifest = json.loads((OUTPUT / "source_manifest.json").read_text(encoding="utf-8"))
        artifacts = manifest["artifacts"]
        require(manifest["version"] == "hp-v4-diversity-analysis-build-v1-native-environment", "build manifest is the V4 native-environment version")
        require(manifest["counts"] == {"prompts": 540, "references": 10, "candidate_csv_rows": 540}, "build manifest records 540 prompts, 10 references, and 540 CSV rows")
        for relative, expected in artifacts.items():
            path = OUTPUT / relative
            require(path.is_file() and path.stat().st_size == expected["bytes"] and sha256(path) == expected["sha256"], f"artifact bytes and SHA match: {relative}")

        analysis = json.loads((OUTPUT / "downloads/analysis.json").read_text(encoding="utf-8"))
        inputs = analysis["inputs"]
        for key, path in (
            ("generation_prompts", EVAL / "generation_prompts.json"),
            ("accepted_prompt_cases", EVAL / "accepted_prompt_cases.json"),
            ("selection_manifest", EVAL / "selection_manifest.json"),
            ("lexical_audit", ROOT / "research/lived_in_v4/data/v4_generation_prompt_stats.json"),
        ):
            require(inputs[key]["sha256"] == sha256(path), f"analysis input hash matches current frozen {key}")
        require(analysis["scope"]["prompt_count"] == 540 and len(analysis["points"]) == 540, "analysis contains exactly 540 point records")
        require(analysis["scope"]["reference_prompt_count"] == 10 and len(analysis["reference_coverage"]) == 10, "analysis contains exactly 10 reference records")
        counts = analysis["distributions"]["display_environment"]
        require(set(counts) == EXPECTED_ENVIRONMENTS and sum(counts.values()) == 540, "native environment distribution covers the exact six categories and sums to 540")
        require(counts == analysis["distributions"]["canonical_environment"], "display compatibility alias has the exact native environment distribution")
        require(all(point["display_environment"] == point["environment"] and point["display_environment_rule"] == "native_v4_environment" for point in analysis["points"]), "all 540 point rows preserve native environment without relabeling")
        require(sum(item["count"] for item in analysis["distributions"]["score_histogram"]) == 540, "source-relevance histogram sums to 540")
        require(sum(analysis["distributions"]["relationship"].values()) == 540, "source-relationship distribution sums to 540")
        require({item["label"] for item in analysis["distributions"]["reference_similarity_by_display_environment"]} == EXPECTED_ENVIRONMENTS, "reference similarity is grouped over all six native environments")
        require(sum(item["assigned_prompt_count"] for item in analysis["reference_coverage"]) == 540, "nearest-reference assignments sum to 540")
        require(analysis["methods"]["semantic_embedding"]["revision"] == "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", "semantic method records the frozen MiniLM revision")
        require(analysis["methods"]["semantic_embedding"]["model_loading"] == "local_files_only=True; no network resolution", "semantic model loading is forced offline")
        require("not an image-quality" in analysis["methods"]["semantic_embedding"]["interpretation"], "semantic proximity is explicitly not labeled image quality")

        with (OUTPUT / "downloads/candidate_metrics.csv").open(encoding="utf-8", newline="") as stream:
            csv_rows = list(csv.DictReader(stream))
        require(len(csv_rows) == 540 and len({row["candidate_key"] for row in csv_rows}) == 540, "candidate CSV contains 540 unique candidate keys")
        require({row["candidate_key"] for row in csv_rows} == {row["candidate_key"] for row in analysis["points"]}, "candidate CSV and analysis JSON contain the same candidate keys")

        data_js = (OUTPUT / "gallery/data.js").read_text(encoding="utf-8")
        require(data_js.startswith("const ANALYSIS = ") and data_js.rstrip().endswith(";"), "gallery data uses the expected JavaScript wrapper")
        serialized = json.loads(data_js[len("const ANALYSIS = "):].rstrip()[:-1])
        require(serialized == analysis, "gallery data and downloadable analysis JSON are semantically identical")

        index = (OUTPUT / "gallery/index.html").read_text(encoding="utf-8")
        report_js = (OUTPUT / "gallery/report.js").read_text(encoding="utf-8")
        inventory = HtmlInventory(); inventory.feed(index); inventory.close()
        referenced_ids = set(re.findall(r'getElementById\("([^"]+)"\)', report_js))
        require(referenced_ids <= inventory.ids, "every JavaScript DOM ID exists in gallery HTML")
        for href in inventory.links:
            if href.startswith("../"):
                require((OUTPUT / "gallery" / href).resolve().is_file(), f"download link resolves locally: {href}")
        require(not re.search(r"\bV3\b|accepted display taxonomy|splits only explicit", index + "\n" + report_js), "gallery has no stale V3 or post-hoc taxonomy claims")

        allowed = publisher_files()
        require(allowed == set(artifacts) | {"source_manifest.json"}, "publisher allowlist exactly matches build artifacts plus source manifest")

        publication_path = HERE / "publication.json"
        published = publication_path.exists()
        if published:
            publication = json.loads(publication_path.read_text(encoding="utf-8"))
            require(publication["version"] == "hp-v4-diversity-analysis-publication-v1", "publication record has the expected version")
            require(publication["preflight_prefix_was_empty"] is True, "publication record confirms the isolated prefix was empty")
            require(publication["active_image_gallery_touched"] is False, "publication record confirms the active image gallery was untouched")
            require(publication["remote_object_count"] == len(allowed), "publication record has the exact allowlisted object count")
            published_objects = {item["relative_path"]: item for item in publication["objects"]}
            require(set(published_objects) == allowed, "publication record contains exactly the allowlisted objects")
            for relative in sorted(allowed):
                local = OUTPUT / relative
                record = published_objects[relative]
                require(local.is_file() and local.stat().st_size == record["bytes"] and sha256(local) == record["sha256"], f"publication record matches local artifact: {relative}")
        else:
            require(not publication_path.exists(), "no publication record exists")

        node = shutil.which("node")
        if node:
            result = subprocess.run([node, "--check", str(OUTPUT / "gallery/report.js")], text=True, capture_output=True, check=False)
            require(result.returncode == 0, "report.js passes node --check")
            js_syntax = {"status": "passed", "runtime": node}
        else:
            js_syntax = {"status": "skipped", "reason": "no JavaScript runtime is installed; DOM/data contracts were checked statically"}

        result: dict[str, Any] = {
            "version": "hp-v4-diversity-analysis-local-validation-v1",
            "status": "passed",
            "output": str(OUTPUT),
            "environment_counts": counts,
            "relationship_counts": analysis["distributions"]["relationship"],
            "source_relevance_score_histogram": analysis["distributions"]["score_histogram"],
            "reference_similarity_quantiles": analysis["headline"]["semantic_nearest_reference_scope_adjusted_quantiles"],
            "exact_duplicate_prompt_groups": analysis["headline"]["exact_duplicate_prompt_groups"],
            "canonical_duplicate_prompt_groups": analysis["headline"]["canonical_duplicate_prompt_groups"],
            "js_syntax": js_syntax,
            "browser_render": {"status": "not_performed", "reason": "no supported browser is installed on this host"},
            "published": published,
            "checks": checks,
        }
    except Exception as exc:
        result = {"version": "hp-v4-diversity-analysis-local-validation-v1", "status": "failed", "error": {"type": type(exc).__name__, "message": str(exc)}, "checks": checks}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
