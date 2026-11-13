#!/usr/bin/env python3
"""Apply an explicit root-authored V4 selection approval; never infer approval."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def approve_documents(selection: dict, accepted: dict, review: dict,
                      selection_sha: str, accepted_sha: str, review_path: str,
                      review_sha: str) -> tuple[dict, dict]:
    required = {"version", "reviewer", "decision", "selection_manifest_sha256",
                "accepted_prompt_cases_sha256", "reviewed_selection_count", "notes"}
    if set(review) != required:
        raise ValueError(f"review keys must be exactly {sorted(required)}")
    if review["reviewer"] != "root" or review["decision"] != "approve_for_image_generation":
        raise ValueError("review must explicitly record root approval for image generation")
    if review["selection_manifest_sha256"] != selection_sha:
        raise ValueError("reviewed selection hash does not match")
    if review["accepted_prompt_cases_sha256"] != accepted_sha:
        raise ValueError("reviewed accepted-map hash does not match")
    if review["reviewed_selection_count"] != 108 or len(selection.get("selections", [])) != 108:
        raise ValueError("approval requires exactly 108 reviewed selections")
    if not isinstance(review["notes"], list) or any(not isinstance(x, str) for x in review["notes"]):
        raise ValueError("review notes must be an array of strings")
    if selection.get("status") != "pending_root_semantic_review":
        raise ValueError("selection is not pending root review")
    if accepted.get("status") != "complete_human_review_required" or len(accepted.get("cases", {})) != 18:
        raise ValueError("accepted map is not complete and pending human review")
    if any(x.get("semantic_review_status") != "pending_root_review" for x in selection["selections"]):
        raise ValueError("selection contains a non-pending row")
    if any(x.get("human_review_status") != "pending_root_review" or x.get("launchable") is not False
           for x in accepted["cases"].values()):
        raise ValueError("accepted map contains a non-pending case")

    approved_accepted = copy.deepcopy(accepted)
    approved_accepted["status"] = "complete"
    approved_accepted["selection_status"] = "approved_for_image_generation"
    for case in approved_accepted["cases"].values():
        case["status"] = "normalized_validator_passed"
        case["human_review_status"] = "accepted"
        case["launchable"] = True

    approved_selection = copy.deepcopy(selection)
    approved_selection["status"] = "approved_for_image_generation"
    for row in approved_selection["selections"]:
        row["semantic_review_status"] = "accepted"
    approved_selection["approval"] = {
        "review_path": review_path, "review_sha256": review_sha,
        "reviewed_pending_selection_sha256": selection_sha,
        "reviewed_pending_accepted_map_sha256": accepted_sha,
        "decision": review["decision"], "reviewer": review["reviewer"],
        "reviewed_selection_count": review["reviewed_selection_count"],
        "notes": review["notes"],
    }
    return approved_selection, approved_accepted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    args = parser.parse_args()
    selection_path = HERE / "selection_manifest.json"
    accepted_path = HERE / "accepted_prompt_cases.json"
    selection_sha = file_sha(selection_path)
    accepted_sha = file_sha(accepted_path)
    review_sha = file_sha(args.review)
    selection = json.loads(selection_path.read_text())
    accepted = json.loads(accepted_path.read_text())
    review = json.loads(args.review.read_text())
    approved_selection, approved_accepted = approve_documents(
        selection, accepted, review, selection_sha, accepted_sha,
        str(args.review.resolve()), review_sha)
    accepted_path.write_text(json.dumps(approved_accepted, ensure_ascii=False, indent=2) + "\n")
    final_accepted_sha = file_sha(accepted_path)
    approved_selection["accepted_prompt_cases_sha256"] = final_accepted_sha
    approved_selection["approval"]["approved_accepted_map_sha256"] = final_accepted_sha
    selection_path.write_text(json.dumps(approved_selection, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "approved_for_image_generation",
                      "selection_manifest_sha256": file_sha(selection_path),
                      "accepted_prompt_cases_sha256": final_accepted_sha,
                      "selection_count": 108}, indent=2))


if __name__ == "__main__":
    main()

