from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from approve_selection import approve_documents


class ApprovalTests(unittest.TestCase):
    def fixtures(self):
        selection = {"status": "pending_root_semantic_review",
                     "selections": [{"semantic_review_status": "pending_root_review"}
                                    for _ in range(108)]}
        accepted = {"status": "complete_human_review_required",
                    "selection_status": "not_yet_performed",
                    "cases": {str(i): {"status": "normalized_validator_passed_pending_human_review",
                                       "human_review_status": "pending_root_review", "launchable": False}
                              for i in range(18)}}
        review = {"version": "v4-root-selection-review-v1", "reviewer": "root",
                  "decision": "approve_for_image_generation",
                  "selection_manifest_sha256": "s", "accepted_prompt_cases_sha256": "a",
                  "reviewed_selection_count": 108, "notes": ["reviewed"]}
        return selection, accepted, review

    def test_explicit_matching_review_approves(self):
        selection, accepted, review = self.fixtures()
        out_selection, out_accepted = approve_documents(selection, accepted, review,
            "s", "a", "/review.json", "r")
        self.assertEqual(out_selection["status"], "approved_for_image_generation")
        self.assertTrue(all(x["semantic_review_status"] == "accepted" for x in out_selection["selections"]))
        self.assertEqual(out_accepted["status"], "complete")
        self.assertTrue(all(x["launchable"] for x in out_accepted["cases"].values()))
        self.assertEqual(selection["status"], "pending_root_semantic_review")

    def test_hash_mismatch_rejected(self):
        selection, accepted, review = self.fixtures()
        review["selection_manifest_sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, "selection hash"):
            approve_documents(selection, accepted, review, "s", "a", "/review.json", "r")

    def test_validator_pass_alone_cannot_approve(self):
        selection, accepted, review = self.fixtures()
        review["decision"] = "validator_passed"
        with self.assertRaisesRegex(ValueError, "explicitly record root approval"):
            approve_documents(selection, accepted, review, "s", "a", "/review.json", "r")


if __name__ == "__main__":
    unittest.main()

