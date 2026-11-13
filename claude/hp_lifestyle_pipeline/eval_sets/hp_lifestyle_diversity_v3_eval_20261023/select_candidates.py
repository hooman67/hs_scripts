#!/usr/bin/env python3
"""Select six diverse candidates per accepted bank using the frozen rank-bin rule."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STOP = frozenset("a an and are as at be by for from in into is it its of on or that the their this to with".split())
FIELDS = ("surface", "light", "local_props", "background_details", "people")
BINS = ((1, 10, "1-10"), (11, 20, "11-20"), (21, 30, "21-30"))
STRATA = {"1-10": "upper_rank_1_10", "11-20": "middle_rank_11_20",
          "21-30": "lower_rank_21_30"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tokens(candidate: dict) -> set[str]:
    sig = candidate["visual_signature"]
    chunks = []
    for field in FIELDS:
        value = sig[field]
        chunks.extend(value if isinstance(value, list) else [value])
    return {term for term in re.findall(r"[a-z]+", " ".join(chunks).lower()) if term not in STOP}


def jaccard_distance(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else 1.0 - len(left & right) / len(union)


def choose_bank(candidates: list[dict]) -> list[dict]:
    selected = []
    selected_keys = set()
    # First/highest-ranked candidate in each ordinal rank bin.
    for lo, hi, label in BINS:
        item = min((c for c in candidates if lo <= c["rank"] <= hi), key=lambda c: c["rank"])
        selected.append((item, label, "highest_ranked_seed", None))
        selected_keys.add(item["candidate_key"])
    # One maximin candidate per bin, in ascending-bin order.
    for lo, hi, label in BINS:
        pool = [c for c in candidates if lo <= c["rank"] <= hi and c["candidate_key"] not in selected_keys]
        selected_envs = {entry[0]["environment"] for entry in selected}
        scored = []
        for item in pool:
            distance = min(jaccard_distance(tokens(item), tokens(chosen[0])) for chosen in selected)
            novel_environment = item["environment"] not in selected_envs
            scored.append((distance, novel_environment, -item["rank"], item))
        distance, novel, _, item = max(scored, key=lambda row: (row[0], row[1], row[2]))
        selected.append((item, label, "maximin_visual_signature", distance))
        selected_keys.add(item["candidate_key"])
    rows = []
    for ordinal, (item, label, reason, distance) in enumerate(selected, 1):
        rows.append({"selection_ordinal": ordinal, "candidate_key": item["candidate_key"],
                     "candidate_id": item["id"], "rank": item["rank"], "rank_bin": label,
                     "selection_stratum": STRATA[label],
                     "score_total": item["source_relevance_score"],
                     "selection_reason": reason, "minimum_jaccard_distance": distance,
                     "environment": item["environment"], "relationship": item["relationship"],
                     "text": item["text"], "text_sha256": item["text_sha256"],
                     "visual_signature": item["visual_signature"]})
    return rows


def main() -> None:
    accepted_path = HERE / "accepted_prompt_cases.json"
    accepted = json.loads(accepted_path.read_text())
    manifest_path = HERE / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    cases_by_id = {c["case_id"]: c for c in manifest["cases"]}
    selections = []
    for case_id in sorted(accepted["cases"]):
        case = accepted["cases"][case_id]
        render = next(r for r in manifest["renders"] if r["render_id"] == case["render_id"])
        for row in choose_bank(case["candidates"]):
            row.update({"selection_key": f"{case_id}::{row['candidate_id']}::selected",
                        "case_id": case_id, "group_id": case["group_id"],
                        "source_id": case["source_id"], "device_type": case["device_type"],
                        "camera_tag": case["camera_tag"], "view_role": case["view_role"],
                        "render_id": case["render_id"], "render_path": render["path"],
                        "render_sha256": render["sha256"], "input_sha256": case["input_sha256"],
                        "accepted_record_path": case["record_path"],
                        "accepted_record_sha256": case["record_sha256"],
                        "semantic_review_status": "pending_root_review"})
            selections.append(row)
    doc = {"version": "v3-selection-maximin-visual-signature-v1",
           "status": "pending_root_semantic_review",
           "algorithm": {"rank_bins": ["1-10", "11-20", "21-30"],
             "rank_bin_meaning": "ordinal ranks, not absolute score bands",
             "selection_strata": STRATA,
             "per_bin_count": 2,
             "seed": "first/highest-ranked candidate in each bin",
             "second": "largest minimum Jaccard distance to all already selected candidates",
             "features": list(FIELDS), "normalization": "lowercase ASCII alphabetic tokens; fixed common stopwords removed",
             "stopwords": sorted(STOP), "tie_breaks": ["novel environment among already selected", "lower rank"],
             "bin_processing_order": ["1-10", "11-20", "21-30"]},
           "manifest_path": str(manifest_path), "manifest_sha256": sha(manifest_path.read_bytes()),
           "accepted_prompt_cases_path": str(accepted_path),
           "accepted_prompt_cases_sha256": sha(accepted_path.read_bytes()),
           "counts": {"accepted_banks": len(accepted["cases"]), "selected": len(selections)},
           "selections": selections}
    target = HERE / "selection_manifest.json"
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(doc["counts"], indent=2))


if __name__ == "__main__":
    main()
