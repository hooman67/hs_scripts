#!/usr/bin/env python3
"""Validate the local V4.1 distribution report and frozen text gate."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
HERE = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
OUTPUT = PROJECT / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
PROMPTS = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/pilot_prompts.json"
USER_REFERENCE_ADDITIONS = PROJECT / "research/source_messaging_v1_to_v6/versions/v4.1/user_reference_additions.json"
EXPECTED_ENVIRONMENTS = {"Home", "Office", "Education", "Gaming", "Café", "Creative Studio"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_plain_text_prompts(document: dict) -> str:
    lines = [
        "HP V4.1 C-Tech pilot prompts",
        f"Version: {document['version']}",
        f"Status: {document['status']}",
        f"Prompt count: {document['prompt_count']}",
        "",
    ]
    for row in document["prompts"]:
        lines.extend([
            f"[{row['candidate_key']}]",
            f"Case: {row['case_id']}",
            f"Camera: {row['camera_tag']} ({row['view_role']})",
            f"Environment: {row['environment']} · {row['subsetting']}",
            row["text"],
            "",
        ])
    return "\n".join(lines)


class Inventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.ids: set[str] = set(); self.links: list[str] = []; self.scripts: list[str] = []

    def handle_starttag(self, tag, attrs) -> None:
        values = dict(attrs)
        if values.get("id"): self.ids.add(values["id"])
        if tag == "a" and values.get("href"): self.links.append(values["href"])
        if tag == "script" and values.get("src"): self.scripts.append(values["src"])


def main() -> None:
    checks = []

    def require(value: bool, message: str) -> None:
        if not value: raise ValueError(message)
        checks.append(message)

    manifest = json.loads((OUTPUT / "source_manifest.json").read_text(encoding="utf-8"))
    require(manifest["version"] == "hp-v4.1-ctech-pilot-distribution-build-v1", "expected build version")
    require(manifest["counts"] == {"prompts": 120, "references": 18, "baseline_prompts": 120, "candidate_csv_rows": 120}, "expected 120/18/120 counts")
    for relative, record in manifest["artifacts"].items():
        path = OUTPUT / relative
        require(path.is_file() and path.stat().st_size == record["bytes"] and sha256(path) == record["sha256"], f"artifact matches manifest: {relative}")
    publisher_tree = ast.parse((HERE / "publish_analysis.py").read_text(encoding="utf-8"))
    publisher_files = next(ast.literal_eval(node.value) for node in publisher_tree.body
                           if isinstance(node, ast.Assign)
                           and any(isinstance(target, ast.Name) and target.id == "FILES" for target in node.targets))
    require(set(publisher_files) == set(manifest["artifacts"]) | {"source_manifest.json"},
            "publisher allowlist exactly matches generated report artifacts")

    analysis = json.loads((OUTPUT / "downloads/analysis.json").read_text(encoding="utf-8"))
    require(analysis["status"] == "text_review_only_no_image_generation_authorized", "report preserves no-image gate")
    require(len(analysis["points"]) == 120 and len({row["candidate_key"] for row in analysis["points"]}) == 120, "120 unique metric points")
    edited_points = [row for row in analysis["points"] if row.get("editorially_scene_edited") is True]
    require(len(edited_points) == 8, "eight prompts disclose editorial scene edits")
    require(all(any(edit.get("field") == "text" for edit in row.get("editorial_edits", []))
                for row in edited_points), "each editorially scene-edited prompt preserves its text patch")
    require(all(row.get("raw_correction_text") and row.get("repair_normalized_text")
                for row in analysis["points"]), "all prompts preserve raw and normalized correction text")
    review_accounting = analysis["review_accounting"]
    require(review_accounting["reviewed_candidate_count"] == 120
            and review_accounting["editorially_scene_edited_candidate_count"] == 8,
            "review accounting discloses 8 of 120 editorial scene edits")
    require(set(review_accounting["editorially_scene_edited_candidate_keys"])
            == {row["candidate_key"] for row in edited_points},
            "review accounting keys match editorial scene-edit badges")
    correction = review_accounting["bounded_model_correction"]
    require(correction["banks"] == correction["correction_calls"]
            == correction["bank_passes_after_correction"] == 4
            and correction["semantic_retries"] == 0,
            "review accounting discloses one bounded correction per bank")
    require("not evidence of single-call production reliability" in correction["description"],
            "review accounting makes no single-call reliability claim")
    require(len(analysis["references"]) == 18 and len(analysis["reference_coverage"]) == 18, "eighteen C-Tech references")
    require(len(analysis["case_inputs"]) == 4 and {row["case_id"] for row in analysis["case_inputs"]}
            == {row["case_id"] for row in analysis["points"]}, "four complete frozen case inputs cover every candidate")
    require(all(row["source_messaging"] and row["camera_tag"] and row["expected_camera"]
                for row in analysis["case_inputs"]), "case inputs include full source messaging and camera metadata")
    counts = Counter(row["environment"] for row in analysis["points"])
    require(set(counts) == EXPECTED_ENVIRONMENTS and sum(counts.values()) == 120, "six native environments sum to 120")
    require(dict(sorted(counts.items())) == analysis["distributions"]["display_environment"], "environment chart equals exact point counts")
    require(sum(analysis["distributions"]["relationship"].values()) == 120, "C-Tech relationship counts sum to 120")
    require(sum(item["count"] for item in analysis["distributions"]["score_histogram"]) == 120, "declared score histogram sums to 120")
    require(sum(item["count"] for item in analysis["distributions"]["reference_similarity_histogram_scope_adjusted"]) == 120, "measured similarity histogram sums to 120")
    require({row["label"] for row in analysis["v4_baseline_comparison"]} == {"all", "close_up", "wide"}, "V4 comparison covers all/close/wide")
    feedback = analysis["feedback_pattern_comparison"]
    require(feedback["interpretation"].casefold() == "lexical indicators, not a complete style judgment.",
            "feedback comparison states its lexical-only interpretation")
    require({row["indicator"] for row in feedback["comparison_rows"]}
            == {"unnatural_framing_or_place_phrase", "microscopic_wear_or_story_marker"},
            "feedback comparison covers both requested indicators")
    comparison_by_indicator = {row["indicator"]: row for row in feedback["comparison_rows"]}
    for corpus_key, count_key in (("v4", "v4_affected_prompt_count"),
                                  ("v4_1", "v4_1_affected_prompt_count")):
        corpus = feedback["corpora"][corpus_key]
        require(corpus["prompt_count"] == 120, f"{corpus_key} feedback corpus contains 120 prompts")
        for indicator, category in corpus["categories"].items():
            findings = category["findings"]
            require(category["affected_prompt_count"] == len(findings)
                    == len({row["candidate_key"] for row in findings}),
                    f"{corpus_key} {indicator} counts affected prompts once")
            require(comparison_by_indicator[indicator][count_key] == len(findings),
                    f"{corpus_key} {indicator} table count matches evidence")
            for finding in findings:
                require(bool(finding["matches"]), f"{corpus_key} {indicator} finding preserves matches")
                for match in finding["matches"]:
                    require(finding["text"][match["start"]:match["end"]] == match["matched_span"],
                            f"{corpus_key} {indicator} matched span and offsets agree")
    require(set(feedback["methods"]["microscopic_wear_or_story_marker"]["requested_exclusions"])
            == {"pastry crumbs", "half-finished coffee", "overgrown plants",
                "lived-in and authentic with subtle imperfections"},
            "C-Tech broad lived-in examples remain excluded from marker regex")
    require(analysis["methods"]["semantic_embedding"]["revision"] == "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", "frozen MiniLM revision")
    additions = json.loads(USER_REFERENCE_ADDITIONS.read_text(encoding="utf-8"))
    raw_by_id = {row["reference_id"]: row["text"] for row in additions["occurrences"]
                 if row["reference_id"] in {f"CT{number:02d}" for number in range(11, 19)}}
    refs_by_id = {row["reference_id"]: row for row in analysis["references"]}
    require(all(refs_by_id[reference_id]["original_text"] == raw_text
                for reference_id, raw_text in raw_by_id.items()), "CT11-CT18 display verbatim user raw examples")
    require(all(refs_by_id[f"CT{number:02d}"]["raw_source_kind"] == "october_guidance"
                for number in range(1, 11)), "CT01-CT10 retain October raw examples")
    require(analysis["inputs"]["user_reference_additions"]["raw_sha256"] == additions["raw_sha256"],
            "user raw source hash is recorded")
    require((OUTPUT / "downloads/pilot_prompts.json").read_bytes() == PROMPTS.read_bytes(),
            "downloaded pilot prompts are byte-identical to frozen export")
    prompt_document = json.loads(PROMPTS.read_text(encoding="utf-8"))
    require((OUTPUT / "downloads/pilot_prompts.txt").read_text(encoding="utf-8")
            == render_plain_text_prompts(prompt_document),
            "plain-text prompt download deterministically contains all frozen prompts")
    system_prompt = Path(analysis["inputs"]["system_prompt"]["path"])
    require((OUTPUT / "downloads/system_prompt.md").read_bytes() == system_prompt.read_bytes(),
            "downloaded system prompt is byte-identical to frozen input")

    data_js = (OUTPUT / "gallery/data.js").read_text(encoding="utf-8")
    require(data_js.startswith("const ANALYSIS = ") and data_js.rstrip().endswith(";"), "gallery data wrapper")
    require(json.loads(data_js[len("const ANALYSIS = "):].rstrip()[:-1]) == analysis, "gallery data equals analysis JSON")
    html = (OUTPUT / "gallery/index.html").read_text(encoding="utf-8")
    js = (OUTPUT / "gallery/report.js").read_text(encoding="utf-8")
    inventory = Inventory(); inventory.feed(html); inventory.close()
    ids = set(re.findall(r'getElementById\("([^"]+)"\)', js))
    require(ids <= inventory.ids, "all JavaScript DOM IDs exist")
    require({"../downloads/pilot_prompts.json", "../downloads/pilot_prompts.txt",
             "../downloads/system_prompt.md"} <= set(inventory.links),
            "plain-text prompts, full pilot JSON, and system prompt are linked for download")
    require("https://auth-stg1.services.adobe.com/imslib/imslib.js" in inventory.scripts
            and "./imsauth.js" in inventory.scripts, "gallery retains IMS authentication")
    for href in inventory.links:
        if href.startswith("../"):
            require((OUTPUT / "gallery" / href).resolve().is_file(), f"download resolves: {href}")
    with (OUTPUT / "downloads/candidate_metrics.csv").open(encoding="utf-8", newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    require(len(csv_rows) == 120 and len({row["candidate_key"] for row in csv_rows}) == 120, "CSV contains 120 unique candidates")

    result = {"version": "hp-v4.1-distribution-local-validation-v1", "status": "passed",
              "output": str(OUTPUT), "published": (HERE / "publication.json").exists(),
              "environment_counts": dict(sorted(counts.items())), "checks": checks}
    (HERE / "local_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
