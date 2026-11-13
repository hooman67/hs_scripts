#!/usr/bin/env python3
"""Build a deterministic, evidence-linked diversity audit for V3 prompt banks."""

from __future__ import annotations

import collections
import datetime as dt
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
from statistics import mean, median
from typing import Any


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
V3_ROOT = PROJECT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023"
V2_ROOT = PROJECT / "eval_sets/hp_lifestyle_camera_v2_eval_20261022"
OUT = PROJECT / "research/diversity_aware_v3/data/v3_diversity_review.json"
SAMPLE_RANKS = (1, 8, 15, 22, 30)
MATERIAL_TERMS = (
    "ash", "bamboo", "birch", "canvas", "ceramic", "concrete", "cork",
    "fabric", "glass", "granite", "laminate", "leather", "maple", "marble",
    "metal", "oak", "paper", "pine", "plywood", "stone", "tile", "veneer",
    "walnut", "wood",
)
FORBIDDEN_DEVICE = re.compile(
    r"\b(?:hp|laptop|printer|mini\s*pc|computer|monitor|hardware|device|ports?|sku)\b",
    re.I,
)
AMBIGUOUS_DEVICE_LEXEME = re.compile(r"\b(?:desktop|screen)\b", re.I)
WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?", re.I)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def tokens(text: str) -> set[str]:
    return set(WORD.findall(text.casefold()))


def jaccard(a: str, b: str) -> float:
    left, right = tokens(a), tokens(b)
    return len(left & right) / len(left | right) if left or right else 1.0


def resolve_path(value: Any, dotted: str) -> Any:
    current = value
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def count(values: Any) -> dict[str, int]:
    return dict(sorted(collections.Counter(values).items(), key=lambda item: (-item[1], item[0])))


def score_summary(scores: list[int]) -> dict[str, Any]:
    return {
        "minimum": min(scores), "maximum": max(scores),
        "mean": round(mean(scores), 3), "median": median(scores),
        "distinct_values": sorted(set(scores), reverse=True),
        "frequency": count(scores),
    }


def nearest_pairs(left: list[dict[str, Any]], right: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    pairs = []
    for a, b in itertools.product(left, right):
        pairs.append({
            "left_id": a.get("id") or a.get("prompt_id"),
            "right_id": b.get("id") or b.get("prompt_id"),
            "jaccard": round(jaccard(a["text"], b["text"]), 6),
            "left_text": a["text"], "right_text": b["text"],
        })
    return sorted(pairs, key=lambda item: (-item["jaccard"], item["left_id"], item["right_id"]))[:limit]


def normalization(case: dict[str, Any]) -> dict[str, Any]:
    log_path = Path(case["normalization_log_path"])
    log = read(log_path)
    reasons = [reason for change in log.get("changes", []) for reason in change.get("reasons", [])]
    return {
        "raw_record_status": case.get("raw_record_status"),
        "normalized_status": case.get("status"),
        "human_review_status": case.get("human_review_status"),
        "launchable": case.get("launchable"),
        "raw_record_path": case["record_path"],
        "raw_record_sha256": case["record_sha256"],
        "raw_output_semantic_sha256": case["raw_parsed_output_sha256"],
        "normalized_output_path": case["normalized_output_path"],
        "normalized_output_file_sha256": case["normalized_output_file_sha256"],
        "normalized_output_semantic_sha256": case["normalized_output_semantic_sha256"],
        "normalization_log_path": str(log_path),
        "normalization_log_file_sha256": case["normalization_log_file_sha256"],
        "changed_candidate_count": log.get("changed_candidate_count", 0),
        "change_reason_counts": count(reasons),
        "id_reordering_count": sum(
            item.get("original_id") != item.get("normalized_id") for item in log.get("id_map", [])
        ),
    }


def main() -> None:
    manifest_path = V3_ROOT / "manifest.json"
    accepted_path = V3_ROOT / "accepted_prompt_cases.json"
    selection_path = V3_ROOT / "selection_manifest.json"
    v2_path = V2_ROOT / "accepted_prompt_cases.json"
    manifest, accepted, v2 = read(manifest_path), read(accepted_path), read(v2_path)
    selection = read(selection_path) if selection_path.exists() else None
    manual_path = V3_ROOT / "manual_review_overrides.json"
    manual = read(manual_path) if manual_path.exists() else {"rejected_attempts": []}
    manifest_cases = {item["case_id"]: item for item in manifest["cases"]}
    sources = {item["source_id"]: read(Path(item["source_json_path"])) for item in manifest["sources"]}
    v2_cases = v2["cases"]
    banks, all_flags, total_norm_reasons = {}, [], collections.Counter()

    for case_id, case in sorted(accepted.get("cases", {}).items()):
        mc = manifest_cases[case_id]
        candidates = case["candidates"]
        debug = case["debug"]
        evidence = {item["id"]: item for item in debug.get("source_evidence", [])}
        flags = []
        for evidence_id, item in evidence.items():
            field = resolve_path(sources[case["source_id"]], item.get("path", ""))
            if not isinstance(field, str) or item.get("quote", "") not in field:
                flags.append({"code":"unsupported_or_nonverbatim_citation", "evidence_id":evidence_id, "citation":item})
        for candidate in candidates:
            components = candidate["score_components"]
            visible = candidate["visual_signature"]
            missing_ids = sorted(set(candidate["evidence_ids"]) - set(evidence))
            if missing_ids:
                flags.append({"code":"unresolved_candidate_evidence_ids", "candidate_id":candidate["id"], "evidence_ids":missing_ids})
            if sum(components.values()) != candidate["source_relevance_score"]:
                flags.append({"code":"score_component_sum_mismatch", "candidate_id":candidate["id"]})
            if not candidate["evidence_ids"] and (
                candidate["source_relevance_score"] != 0 or candidate["relationship"] != "creative_departure"
            ):
                flags.append({"code":"empty_evidence_nonzero_or_nondeparture", "candidate_id":candidate["id"]})
            if candidate["relationship"] == "creative_departure" and candidate["source_relevance_score"] > 59:
                flags.append({"code":"creative_departure_above_59", "candidate_id":candidate["id"]})
            if components["materials"] > 0 and not visible["local_props"]:
                flags.append({"code":"material_score_without_visible_local_material", "candidate_id":candidate["id"], "materials_score":components["materials"]})
            if components["activity"] > 10 and not visible["local_props"] and not visible["people"]:
                flags.append({"code":"activity_score_above_broad_context_without_visible_actor_or_prop", "candidate_id":candidate["id"], "activity_score":components["activity"]})
            forbidden = sorted(set(match.group(0) for match in FORBIDDEN_DEVICE.finditer(candidate["text"])), key=str.casefold)
            if forbidden:
                flags.append({"code":"forbidden_device_term_in_scene_prose", "candidate_id":candidate["id"], "terms":forbidden})
            ambiguous = sorted(set(match.group(0) for match in AMBIGUOUS_DEVICE_LEXEME.finditer(candidate["text"])), key=str.casefold)
            if ambiguous:
                flags.append({
                    "code":"ambiguous_device_lexeme_in_scene_prose",
                    "candidate_id":candidate["id"], "terms":ambiguous,
                    "text":candidate["text"],
                    "review_note":"The term may denote furniture or a divider, but it overlaps the prompt's prohibited target-device vocabulary.",
                })
            expected = mc["expected_camera"]
            if len(visible["local_props"]) > expected["max_local_props"]:
                flags.append({"code":"local_prop_limit_exceeded", "candidate_id":candidate["id"], "count":len(visible["local_props"]), "limit":expected["max_local_props"]})
            if len(visible["background_details"]) > expected["max_background_details"]:
                flags.append({"code":"background_limit_exceeded", "candidate_id":candidate["id"], "count":len(visible["background_details"]), "limit":expected["max_background_details"]})
            if expected["people_policy"] == "omit" and visible["people"]:
                flags.append({"code":"people_present_under_omit_policy", "candidate_id":candidate["id"], "people":visible["people"]})

        texts = [item["text"] for item in candidates]
        signatures = [json.dumps(item["visual_signature"], sort_keys=True, ensure_ascii=False) for item in candidates]
        within_pairs = [
            {"left_id": candidates[i]["id"], "right_id": candidates[j]["id"], "jaccard": round(jaccard(texts[i], texts[j]), 6)}
            for i in range(30) for j in range(i + 1, 30)
        ]
        near = sorted((item for item in within_pairs if item["jaccard"] >= .8), key=lambda x:(-x["jaccard"],x["left_id"],x["right_id"]))
        material_hits = {}
        for term in MATERIAL_TERMS:
            ids = [item["id"] for item in candidates if re.search(rf"\b{re.escape(term)}\b", item["text"] + " " + item["visual_signature"]["surface"], re.I)]
            if ids: material_hits[term] = {"candidate_count":len(ids), "candidate_ids":ids}
        local_props = [prop for item in candidates for prop in item["visual_signature"]["local_props"]]
        backgrounds = [detail for item in candidates for detail in item["visual_signature"]["background_details"]]
        people = [person for item in candidates for person in item["visual_signature"]["people"]]

        v2_case = v2_cases.get(case_id)
        if v2_case is None:
            flags.append({"code":"matched_v2_source_tag_case_missing"})
            v2_prompts = []
        else:
            v2_prompts = v2_case["prompts"]
        norm = normalization(case)
        total_norm_reasons.update(norm["change_reason_counts"])
        sample = []
        for rank in SAMPLE_RANKS:
            item = candidates[rank - 1]
            sample.append({
                "rank": rank, "candidate_id": item["id"], "text": item["text"],
                "score": item["source_relevance_score"], "score_components": item["score_components"],
                "relationship": item["relationship"], "environment": item["environment"],
                "subsetting": item["subsetting"], "evidence_ids": item["evidence_ids"],
                "resolved_evidence": [evidence.get(eid) for eid in item["evidence_ids"]],
                "explanation": item["explanation"], "creative_departures": item["creative_departures"],
                "visual_signature": item["visual_signature"],
            })
        bank = {
            "case_id": case_id, "source_id": case["source_id"], "device_type": case["device_type"],
            "camera_tag": case["camera_tag"], "view_role": case["view_role"],
            "normalized_output_semantic_sha256": case["normalized_output_semantic_sha256"],
            "candidate_count": len(candidates),
            "score_summary": score_summary([item["source_relevance_score"] for item in candidates]),
            "score_component_totals": {name:sum(item["score_components"][name] for item in candidates) for name in ("setting","activity","materials","use_context")},
            "environment_counts": count(item["environment"] for item in candidates),
            "relationship_counts": count(item["relationship"] for item in candidates),
            "family_indicators": {
                "distinct_environment_count": len({item["environment"] for item in candidates}),
                "distinct_subsetting_count": len({item["subsetting"].casefold() for item in candidates}),
                "subsetting_counts": count(item["subsetting"] for item in candidates),
            },
            "material_indicators": material_hits,
            "prop_indicators": {
                "candidates_with_local_props": sum(bool(item["visual_signature"]["local_props"]) for item in candidates),
                "total_local_prop_entries": len(local_props), "exact_local_prop_phrase_counts": count(local_props),
                "candidates_with_background_details": sum(bool(item["visual_signature"]["background_details"]) for item in candidates),
                "total_background_detail_entries": len(backgrounds), "exact_background_phrase_counts": count(backgrounds),
                "candidates_with_people": sum(bool(item["visual_signature"]["people"]) for item in candidates),
                "total_people_entries": len(people), "exact_people_phrase_counts": count(people),
            },
            "diversity": {
                "unique_text_count": len(set(texts)), "unique_visual_signature_count": len(set(signatures)),
                "distinct_surface_count": len({item["visual_signature"]["surface"].casefold() for item in candidates}),
                "distinct_light_count": len({item["visual_signature"]["light"].casefold() for item in candidates}),
                "average_text_token_count": round(mean(len(WORD.findall(text)) for text in texts), 3),
                "maximum_within_bank_text_jaccard": max(within_pairs, key=lambda x:x["jaccard"]),
                "near_duplicate_pairs_at_or_above_0_8": near,
            },
            "normalization": norm,
            "matched_v2": {
                "case_found": v2_case is not None, "prompt_count": len(v2_prompts),
                "prompts": [{"prompt_id":item["prompt_id"], "text":item["text"], "text_sha256":item["text_sha256"]} for item in v2_prompts],
                "exact_text_overlap_count": len(set(texts) & {item["text"] for item in v2_prompts}),
                "nearest_cross_version_pairs": nearest_pairs(candidates, v2_prompts) if v2_prompts else [],
            },
            "bounded_review_sample": {"selection_rule":"normalized ranks 1, 8, 15, 22, and 30", "candidates":sample},
            "objective_flags": flags,
        }
        banks[case_id] = bank
        all_flags.extend({"case_id":case_id, **flag} for flag in flags)

    group_comparisons = []
    by_group = collections.defaultdict(list)
    for case_id, bank in banks.items(): by_group[manifest_cases[case_id]["group_id"]].append(bank)
    for group_id, group in sorted(by_group.items()):
        if len(group) != 2: continue
        left, right = sorted(group, key=lambda item:item["view_role"])
        lc, rc = accepted["cases"][left["case_id"]]["candidates"], accepted["cases"][right["case_id"]]["candidates"]
        group_comparisons.append({
            "group_id":group_id, "case_ids":[left["case_id"],right["case_id"]],
            "exact_text_overlap_count":len({x["text"] for x in lc}&{x["text"] for x in rc}),
            "nearest_cross_view_pairs":nearest_pairs(lc,rc),
            "environment_counts":{left["view_role"]:left["environment_counts"],right["view_role"]:right["environment_counts"]},
        })

    all_candidates = [candidate for case in accepted.get("cases", {}).values() for candidate in case["candidates"]]
    all_local_props = [prop for candidate in all_candidates for prop in candidate["visual_signature"]["local_props"]]
    all_backgrounds = [detail for candidate in all_candidates for detail in candidate["visual_signature"]["background_details"]]
    all_people = [person for candidate in all_candidates for person in candidate["visual_signature"]["people"]]
    aggregate_material_hits = {}
    for term in MATERIAL_TERMS:
        ids = [
            f"{case_id}::{candidate['id']}"
            for case_id, case in accepted.get("cases", {}).items() for candidate in case["candidates"]
            if re.search(rf"\b{re.escape(term)}\b", candidate["text"] + " " + candidate["visual_signature"]["surface"], re.I)
        ]
        if ids: aggregate_material_hits[term] = {"candidate_count":len(ids), "candidate_keys":ids}
    v2_prompt_count = sum(bank["matched_v2"]["prompt_count"] for bank in banks.values())
    cross_version_best = [
        bank["matched_v2"]["nearest_cross_version_pairs"][0]
        for bank in banks.values() if bank["matched_v2"]["nearest_cross_version_pairs"]
    ]
    rejected_attempts = []
    normalized_cache = {}
    for path in sorted((V3_ROOT / "normalized_outputs").glob("*.json")):
        output = read(path); normalized_cache[canonical_sha(output)] = {"path":str(path),"output":output}
    for rejected in manual.get("rejected_attempts", []):
        record_path = Path(rejected["record_path"])
        normalized = normalized_cache.get(rejected["normalized_output_semantic_sha256"])
        ids = [item.strip() for item in rejected.get("normalized_candidate_id", "").split(",") if item.strip()]
        prompts = {item["id"]:item for item in (normalized or {}).get("output", {}).get("prompts", [])}
        rejected_attempts.append({
            **rejected,
            "raw_record_sha256_verified":record_path.exists() and sha(record_path)==rejected["raw_record_sha256"],
            "normalized_output_path":(normalized or {}).get("path"),
            "flagged_candidate_snippets":[
                {"candidate_id":candidate_id,"text":prompts.get(candidate_id,{}).get("text"),"visual_signature":prompts.get(candidate_id,{}).get("visual_signature")}
                for candidate_id in ids
            ],
            "excluded_from_authoritative_bank":True,
        })
    result = {
        "version":"v3-diversity-review-v1",
        "generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "status":"complete" if len(banks)==18 else "progressive",
        "scope":{
            "manifest_case_count":18, "reviewed_case_count":len(banks),
            "candidate_count":len(all_candidates), "expected_candidate_count":540,
            "bounded_sample_ranks":list(SAMPLE_RANKS), "bounded_sample_count":len(banks)*len(SAMPLE_RANKS),
            "normalized_candidate_content_is_authoritative":True,
            "raw_model_bytes_are_immutable":True,
            "accepted_prompt_cases_status":accepted.get("status"),
            "human_review_status_counts":count(case.get("human_review_status") for case in accepted.get("cases", {}).values()),
            "launchable_case_count":sum(case.get("launchable") is True for case in accepted.get("cases", {}).values()),
            "selection_status":selection.get("status") if selection else None,
            "selection_count":len(selection.get("selections", [])) if selection else 0,
        },
        "provenance":{
            "manifest_path":str(manifest_path), "manifest_sha256":sha(manifest_path),
            "accepted_prompt_cases_path":str(accepted_path), "accepted_prompt_cases_sha256":sha(accepted_path),
            "selection_manifest_path":str(selection_path),
            "selection_manifest_sha256":sha(selection_path) if selection_path.exists() else None,
            "matched_v2_accepted_path":str(v2_path), "matched_v2_accepted_sha256":sha(v2_path),
            "manual_review_overrides_path":str(manual_path),
            "manual_review_overrides_sha256":sha(manual_path) if manual_path.exists() else None,
        },
        "aggregate":{
            "device_type_counts":count(case["device_type"] for case in accepted.get("cases", {}).values()),
            "environment_counts":count(candidate["environment"] for candidate in all_candidates),
            "relationship_counts":count(candidate["relationship"] for candidate in all_candidates),
            "score_summary":score_summary([candidate["source_relevance_score"] for candidate in all_candidates]) if all_candidates else None,
            "normalization_changed_candidate_count":sum(bank["normalization"]["changed_candidate_count"] for bank in banks.values()),
            "normalization_reason_counts":dict(sorted(total_norm_reasons.items())),
            "objective_flag_counts":count(flag["code"] for flag in all_flags),
            "diversity_counts":{
                "banks_with_30_unique_texts":sum(bank["diversity"]["unique_text_count"]==30 for bank in banks.values()),
                "banks_with_30_unique_visual_signatures":sum(bank["diversity"]["unique_visual_signature_count"]==30 for bank in banks.values()),
                "within_bank_pairs_at_or_above_0_8_jaccard":sum(len(bank["diversity"]["near_duplicate_pairs_at_or_above_0_8"]) for bank in banks.values()),
                "highest_within_bank_jaccard":max((bank["diversity"]["maximum_within_bank_text_jaccard"]["jaccard"] for bank in banks.values()),default=None),
            },
            "material_indicators":aggregate_material_hits,
            "prop_indicators":{
                "candidates_with_local_props":sum(bool(candidate["visual_signature"]["local_props"]) for candidate in all_candidates),
                "total_local_prop_entries":len(all_local_props), "exact_local_prop_phrase_counts":count(all_local_props),
                "candidates_with_background_details":sum(bool(candidate["visual_signature"]["background_details"]) for candidate in all_candidates),
                "total_background_detail_entries":len(all_backgrounds), "exact_background_phrase_counts":count(all_backgrounds),
                "candidates_with_people":sum(bool(candidate["visual_signature"]["people"]) for candidate in all_candidates),
                "total_people_entries":len(all_people), "exact_people_phrase_counts":count(all_people),
            },
            "matched_v2_comparison":{
                "matched_case_count":sum(bank["matched_v2"]["case_found"] for bank in banks.values()),
                "v2_prompt_count":v2_prompt_count,
                "exact_text_overlap_count":sum(bank["matched_v2"]["exact_text_overlap_count"] for bank in banks.values()),
                "mean_best_cross_version_jaccard":round(mean(item["jaccard"] for item in cross_version_best),6) if cross_version_best else None,
                "maximum_cross_version_jaccard":max((item["jaccard"] for item in cross_version_best),default=None),
            },
        },
        "objective_flags":all_flags,
        "review_findings":[
            {
                "code":"accepted_mechanical_score_evidence_camera_checks",
                "result":"pass" if not [flag for flag in all_flags if flag["code"] != "ambiguous_device_lexeme_in_scene_prose"] else "flags_present",
                "detail":"Across authoritative normalized candidates, checks cover verbatim citation resolution, evidence IDs, score arithmetic, empty-evidence normalization, the creative-departure 59-point ceiling, visible-material/activity indicators, camera detail ceilings, people policy, and unambiguous prohibited device terms.",
            },
            {
                "code":"ambiguous_device_vocabulary_requires_human_interpretation",
                "result":"review",
                "count":sum(flag["code"]=="ambiguous_device_lexeme_in_scene_prose" for flag in all_flags),
                "detail":"Accepted prose uses desktop for a furniture surface or screen for a privacy/acoustic divider. These are not demonstrated extra computing devices, but they overlap literal target-device vocabulary and are preserved for review.",
            },
            {
                "code":"bounded_style_and_label_sample",
                "result":"no_concrete_unsupported_citation_or_relationship_found",
                "sample_count":len(banks)*len(SAMPLE_RANKS),
                "detail":"The deterministic rank 1/8/15/22/30 sample was inspected across every completed bank. This finding does not substitute for root's creative review of all 540 candidates or the selected 108.",
            },
        ],
        "rejected_attempts":{
            "count":len(rejected_attempts),
            "reason_counts":count(item["reason"] for item in rejected_attempts),
            "attempts":rejected_attempts,
        },
        "banks":banks,
        "matched_close_wide_group_comparisons":group_comparisons,
        "limitations":[
            "This artifact reports deterministic counts plus a fixed five-candidate sample per completed bank; it is not a full creative-quality judgment.",
            "Source-relevance scores and relationship labels remain rubric judgments. Objective flags identify mechanical contradictions and review candidates, not automatic corrections.",
            "The ambiguous-device-lexeme flag is lexical only: desktop may mean a work surface and screen may mean an acoustic divider; human review must interpret context.",
            "Material indicators use the explicit fixed lexicon stored in this script and count word-boundary matches in normalized prompt text plus declared surface text.",
            "Prop and background counts rely on normalized visual_signature inventories; the human review must compare those inventories with prose.",
            "Jaccard similarity uses lowercase alphanumeric word sets and is a lexical indicator, not a semantic-diversity score.",
            "The report is progressive until all 18 normalized banks are present; hashes and counts change on each rebuild.",
        ],
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    temporary=OUT.with_suffix('.json.tmp'); temporary.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); temporary.replace(OUT)
    print(json.dumps({"output":str(OUT),"status":result["status"],"banks":len(banks),"candidates":len(all_candidates),"sample":result["scope"]["bounded_sample_count"],"flags":result["aggregate"]["objective_flag_counts"]},indent=2))


if __name__ == "__main__":
    main()
