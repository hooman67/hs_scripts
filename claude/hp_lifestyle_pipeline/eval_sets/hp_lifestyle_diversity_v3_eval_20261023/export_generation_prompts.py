#!/usr/bin/env python3
"""Export frozen V3 candidate text without downstream prompt rewriting."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"
ACCEPTED_PATH = HERE / "accepted_prompt_cases.json"
SELECTION_PATH = HERE / "selection_manifest.json"
ALL_OUTPUT_PATH = HERE / "generation_prompts.json"
SELECTED_OUTPUT_PATH = HERE / "generation_prompts_selected.json"

EXPECTED_SOURCES = 9
EXPECTED_CASES = 18
EXPECTED_PER_CASE = 30
EXPECTED_PROMPTS = 540
EXPECTED_SELECTED_PER_CASE = 6
EXPECTED_SELECTED = 108
EXPECTED_SELECTED_PER_BIN = 2
RANK_BINS = {"1-10": range(1, 11), "11-20": range(11, 21), "21-30": range(21, 31)}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def load_json(path: Path) -> tuple[dict[str, Any], bytes, str]:
    raw = path.read_bytes()
    return json.loads(raw), raw, sha256_bytes(raw)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_exports() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest, _, manifest_sha = load_json(MANIFEST_PATH)
    accepted, _, accepted_sha = load_json(ACCEPTED_PATH)
    selection, _, selection_sha = load_json(SELECTION_PATH)

    require(accepted.get("status") == "complete", "accepted prompt map is not complete")
    require(selection.get("status") == "approved_for_image_generation", "selection is not approved")
    require(accepted.get("manifest_sha256") == manifest_sha, "accepted map manifest hash mismatch")
    require(selection.get("manifest_sha256") == manifest_sha, "selection manifest hash mismatch")
    require(
        selection.get("accepted_prompt_cases_sha256") == accepted_sha,
        "selection accepted-map hash mismatch",
    )

    manifest_cases = {case["case_id"]: case for case in manifest["cases"]}
    accepted_cases = accepted["cases"]
    sources = {source["source_id"]: source for source in manifest["sources"]}
    require(len(sources) == EXPECTED_SOURCES, f"expected {EXPECTED_SOURCES} sources")
    for source in sources.values():
        source_path = Path(source["source_json_path"])
        require(source_path.is_file(), f"missing source JSON: {source_path}")
        require(sha256_bytes(source_path.read_bytes()) == source["sha256"], f"source JSON hash mismatch: {source_path}")
    for name in ("system_prompt", "output_schema", "camera_profiles"):
        artifact = manifest["provenance"][name]
        artifact_path = Path(artifact["path"])
        require(artifact_path.is_file(), f"missing provenance artifact: {artifact_path}")
        require(sha256_bytes(artifact_path.read_bytes()) == artifact["sha256"], f"provenance hash mismatch: {name}")
    require(len(manifest_cases) == EXPECTED_CASES, f"expected {EXPECTED_CASES} cases")
    require(set(accepted_cases) == set(manifest_cases), "accepted/manifest case coverage mismatch")

    selections: dict[str, dict[str, Any]] = {}
    selection_counts_by_case: Counter[str] = Counter()
    selection_counts_by_case_bin: Counter[tuple[str, str]] = Counter()
    for item in selection["selections"]:
        key = item["candidate_key"]
        require(key not in selections, f"duplicate selection candidate key: {key}")
        require(item.get("semantic_review_status") == "accepted", f"selection is not accepted: {key}")
        require(item["case_id"] in manifest_cases, f"selection has unknown case: {key}")
        selections[key] = item
        selection_counts_by_case[item["case_id"]] += 1
        selection_counts_by_case_bin[(item["case_id"], item["rank_bin"])] += 1
    require(len(selections) == EXPECTED_SELECTED, f"expected {EXPECTED_SELECTED} selections")

    rows: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    source_ids: set[str] = set()
    camera_tags: set[str] = set()
    for case_id in sorted(manifest_cases):
        case = manifest_cases[case_id]
        bank = accepted_cases[case_id]
        for field in (
            "case_id", "group_id", "source_id", "device_type", "camera_tag",
            "view_role", "render_id", "input_path", "input_sha256",
        ):
            require(bank[field] == case[field], f"accepted case mismatch for {case_id}/{field}")
        input_path = Path(case["input_path"])
        require(input_path.is_file(), f"missing case input: {case_id}")
        require(sha256_bytes(input_path.read_bytes()) == case["input_sha256"], f"case input hash mismatch: {case_id}")
        require(bank.get("human_review_status") == "accepted", f"bank lacks human acceptance: {case_id}")
        require(bank.get("launchable") is True, f"bank is not launchable: {case_id}")
        candidates = bank["candidates"]
        require(len(candidates) == EXPECTED_PER_CASE, f"expected 30 candidates: {case_id}")
        require({candidate["rank"] for candidate in candidates} == set(range(1, 31)), f"rank coverage mismatch: {case_id}")
        require({candidate["id"] for candidate in candidates} == {f"p{i}" for i in range(1, 31)}, f"id coverage mismatch: {case_id}")
        source = sources[case["source_id"]]
        source_ids.add(case["source_id"])
        camera_tags.add(case["camera_tag"])

        for candidate in sorted(candidates, key=lambda value: value["rank"]):
            key = candidate["candidate_key"]
            require(key == f"{case_id}::{candidate['id']}", f"candidate key mismatch: {key}")
            require(key not in seen_keys, f"duplicate candidate key: {key}")
            seen_keys.add(key)
            require(candidate["text_sha256"] == sha256_text(candidate["text"]), f"text hash mismatch: {key}")
            expected_bin = next(label for label, ranks in RANK_BINS.items() if candidate["rank"] in ranks)
            require(candidate["rank_bin"] == expected_bin, f"rank-bin mismatch: {key}")

            selected = selections.get(key)
            if selected is not None:
                for selection_field, candidate_field in (
                    ("candidate_id", "id"),
                    ("rank", "rank"),
                    ("rank_bin", "rank_bin"),
                    ("environment", "environment"),
                    ("relationship", "relationship"),
                    ("text", "text"),
                    ("text_sha256", "text_sha256"),
                    ("score_total", "source_relevance_score"),
                ):
                    require(
                        selected[selection_field] == candidate[candidate_field],
                        f"selection/candidate mismatch for {key}/{selection_field}",
                    )
                require(selected["source_id"] == case["source_id"], f"selection source mismatch: {key}")
                require(selected["camera_tag"] == case["camera_tag"], f"selection camera mismatch: {key}")

            rows.append(
                {
                    "case_id": case_id,
                    "candidate_key": key,
                    "source_id": case["source_id"],
                    "source_json_path": source["source_json_path"],
                    "source_json_sha256": source["sha256"],
                    "device_type": case["device_type"],
                    "camera_tag": case["camera_tag"],
                    "view_role": case["view_role"],
                    "id": candidate["id"],
                    "rank": candidate["rank"],
                    "rank_bin": candidate["rank_bin"],
                    "environment": candidate["environment"],
                    "subsetting": candidate["subsetting"],
                    "text": candidate["text"],
                    "text_sha256": candidate["text_sha256"],
                    "score": candidate["source_relevance_score"],
                    "score_components": candidate["score_components"],
                    "relationship": candidate["relationship"],
                    "explanation": candidate["explanation"],
                    "creative_departures": candidate["creative_departures"],
                    "selected_for_image_eval": selected is not None,
                    "selection_key": selected["selection_key"] if selected else None,
                    "selection_ordinal": selected["selection_ordinal"] if selected else None,
                    "selection_stratum": selected["selection_stratum"] if selected else None,
                    "selection_reason": selected["selection_reason"] if selected else None,
                }
            )

    require(len(rows) == EXPECTED_PROMPTS, f"expected {EXPECTED_PROMPTS} prompts")
    require(len(seen_keys) == EXPECTED_PROMPTS, "candidate keys are not unique")
    require(source_ids == set(sources), "source coverage mismatch")
    require(len(camera_tags) == 4, "expected four type-specific close/wide camera tags")
    require(sum(row["selected_for_image_eval"] for row in rows) == EXPECTED_SELECTED, "selected projection mismatch")
    require(set(selections) <= seen_keys, "selection contains candidates absent from accepted bank")
    for case_id in manifest_cases:
        require(selection_counts_by_case[case_id] == EXPECTED_SELECTED_PER_CASE, f"selection count mismatch: {case_id}")
        for rank_bin in RANK_BINS:
            require(
                selection_counts_by_case_bin[(case_id, rank_bin)] == EXPECTED_SELECTED_PER_BIN,
                f"selection rank-bin count mismatch: {case_id}/{rank_bin}",
            )

    provenance = {
        "manifest_path": str(MANIFEST_PATH),
        "manifest_sha256": manifest_sha,
        "accepted_prompt_cases_path": str(ACCEPTED_PATH),
        "accepted_prompt_cases_sha256": accepted_sha,
        "selection_manifest_path": str(SELECTION_PATH),
        "selection_manifest_sha256": selection_sha,
        "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
        "output_schema_sha256": manifest["provenance"]["output_schema"]["sha256"],
        "camera_profiles_sha256": manifest["provenance"]["camera_profiles"]["sha256"],
        "prompt_text_source": "accepted_prompt_cases normalized candidate text",
        "downstream_prompt_rewriting_applied": False,
    }
    validation = {
        "manifest_case_coverage_exact": True,
        "candidate_keys_unique": True,
        "candidate_text_sha256_verified": True,
        "source_and_case_input_sha256_verified": True,
        "prompt_schema_registry_sha256_verified": True,
        "selection_hash_link_verified": True,
        "selection_candidate_fields_verified": True,
        "selection_coverage_exact": True,
        "selected_only_is_exact_filter": True,
    }
    counts = {
        "sources": len(source_ids),
        "camera_tags": len(camera_tags),
        "cases": len(manifest_cases),
        "prompts": len(rows),
        "selected_for_image_eval": EXPECTED_SELECTED,
        "not_selected_for_image_eval": EXPECTED_PROMPTS - EXPECTED_SELECTED,
        "prompts_per_case": EXPECTED_PER_CASE,
    }
    common = {
        "version": "hp-lifestyle-diversity-v3-generation-prompts-v1",
        "as_of": manifest["as_of"],
        "provenance": provenance,
        "validation": validation,
    }
    all_doc = {**common, "scope": "all_540_normalized_candidates", "counts": counts, "prompts": rows}
    selected_rows = [row for row in rows if row["selected_for_image_eval"]]
    selected_doc = {
        **common,
        "scope": "selected_108_image_eval_candidates",
        "counts": {
            **counts,
            "prompts": len(selected_rows),
            "not_selected_for_image_eval": 0,
            "prompts_per_case": EXPECTED_SELECTED_PER_CASE,
            "total_candidate_inventory": EXPECTED_PROMPTS,
        },
        "prompts": selected_rows,
    }
    require(selected_rows == [row for row in all_doc["prompts"] if row["selected_for_image_eval"]], "selected filter mismatch")
    return all_doc, selected_doc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify existing exports are current")
    args = parser.parse_args()
    all_doc, selected_doc = build_exports()
    outputs = ((ALL_OUTPUT_PATH, all_doc), (SELECTED_OUTPUT_PATH, selected_doc))
    if args.check:
        for path, document in outputs:
            require(path.exists(), f"missing export: {path}")
            require(path.read_bytes() == json_bytes(document), f"stale export: {path}")
    else:
        for path, document in outputs:
            path.write_bytes(json_bytes(document))
    print(
        json.dumps(
            {
                "checked": args.check,
                "outputs": [
                    {
                        "path": str(path),
                        "prompts": len(document["prompts"]),
                        "sha256": sha256_bytes(json_bytes(document)),
                    }
                    for path, document in outputs
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
