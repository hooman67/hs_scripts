from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("build_fe_report.py")
SPEC = importlib.util.spec_from_file_location("placement_v2_fe_builder", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def anchor(asset_id: str, kind: str = "development") -> dict[str, str]:
    return {"asset_id": asset_id, "kind": kind, "sha256": asset_id * 8}


def result(
    *,
    examples: list[dict[str, str]] | None,
    enabled: bool,
    prompt_hash: str = "prompt-hash",
) -> dict:
    value = {
        "ok": True,
        "protocol_version": "protocol-v-test",
        "model_requested": "model-test",
        "model_returned": "model-test-versioned",
        "system_prompt_sha256": prompt_hash,
        "schema_sha256": "schema-hash",
        "scoring_sha256": "scoring-hash",
        "runner_sha256": "runner-hash",
        "wire_schema_sha256": "wire-hash",
        "visual_anchors_enabled": enabled,
        "judgment": {
            "threshold_status": "provisional_not_human_calibrated",
            "policy_version": "policy-v-test",
        },
    }
    if enabled:
        value["visual_anchor_manifest_sha256"] = "historical-manifest-hash"
        value["visual_anchors"] = {"examples": examples}
    return value


class RunProvenanceTest(unittest.TestCase):
    def test_disabled_visual_context_is_supported(self) -> None:
        records = [{"id": "a"}, {"id": "b"}]
        results = {
            "a": result(examples=None, enabled=False),
            "b": result(examples=None, enabled=False),
        }
        provenance = BUILDER.validate_run_provenance(
            records,
            results,
            regression=False,
            visual_anchors_path=Path("/does/not/exist"),
        )
        self.assertFalse(provenance["visual_context_enabled"])
        self.assertEqual(provenance["visual_examples_per_row"], 0)

    def test_standard_run_derives_arbitrary_consistent_count(self) -> None:
        examples = [anchor(f"a{i}") for i in range(5)]
        records = [{"id": "row1"}, {"id": "row2"}]
        results = {
            "row1": result(examples=examples, enabled=True),
            "row2": result(examples=examples, enabled=True),
        }
        provenance = BUILDER.validate_run_provenance(
            records,
            results,
            regression=False,
            visual_anchors_path=Path("/does/not/exist"),
        )
        self.assertEqual(provenance["visual_examples_per_row"], 5)
        self.assertEqual(provenance["visual_example_union_size"], 5)
        self.assertEqual(provenance["visual_context_mode"], "consistent_shared_set")

    def test_regression_derives_union_minus_exact_target(self) -> None:
        full = [
            anchor("row1", "user_failure"),
            anchor("row2", "user_failure"),
            anchor("reference", "reference"),
        ]
        records = [{"id": "row1"}, {"id": "row2"}]
        results = {
            "row1": result(examples=[full[1], full[2]], enabled=True),
            "row2": result(examples=[full[0], full[2]], enabled=True),
        }
        provenance = BUILDER.validate_run_provenance(
            records,
            results,
            regression=True,
            visual_anchors_path=Path("/does/not/exist"),
        )
        self.assertEqual(provenance["visual_examples_per_row"], 2)
        self.assertEqual(provenance["visual_example_union_size"], 3)
        self.assertEqual(provenance["visual_context_mode"], "exact_target_excluded")

    def test_inconsistent_prompt_hash_is_rejected(self) -> None:
        records = [{"id": "a"}, {"id": "b"}]
        results = {
            "a": result(examples=None, enabled=False, prompt_hash="one"),
            "b": result(examples=None, enabled=False, prompt_hash="two"),
        }
        with self.assertRaisesRegex(ValueError, "system_prompt_sha256"):
            BUILDER.validate_run_provenance(
                records,
                results,
                regression=False,
                visual_anchors_path=Path("/does/not/exist"),
            )

    def test_review_query_round_trips_exact_viewer_wire(self) -> None:
        query = BUILDER.review_query("hshariati")
        BUILDER.validate_review_query(query, "hshariati")

    def test_evidence_leads_with_result_and_ends_with_scene_reading(self) -> None:
        judgment = {
            "weighted_component_score": 90.0,
            "applied_score_cap": 59,
            "natural_placement_score": 59,
            "confidence": "medium",
            "coverage": 1.0,
            "verdict": "fail",
            "verdict_reasons": ["clear_placement_defect_veto"],
            "observation": {
                "summary": "The support is plausible, but alignment is unnatural.",
                "components": {
                    "orientation_alignment": {
                        "visibility": "observed",
                        "severity": 2,
                        "confidence": "high",
                        "evidence": "The product is diagonal to the table.",
                        "consequence": "The placement looks staged.",
                        "issue_codes": ["furniture_axis_conflict"],
                    }
                },
                "suggested_scene_changes": ["Square the product to the table."],
                "scene_reading": {
                    "functional_front": "The operating front faces the room."
                },
            },
        }
        text = BUILDER._evidence_text(judgment)
        self.assertTrue(
            text.startswith(
                "JUDGE RESULT\nPredicted verdict: FAIL · Final score: 59/100 "
                "· Confidence: medium · Coverage: 1.0"
            )
        )
        self.assertIn(
            "Final score after cap: min(90.0, 59) = 59/100",
            text,
        )
        headings = [
            "Summary",
            "Score calculation",
            "Component evidence",
            "Suggested scene changes",
            "Detailed scene reading",
        ]
        positions = [text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(
            text.endswith(
                "functional_front: The operating front faces the room."
            )
        )

        row, _ = BUILDER.make_row(
            {
                "id": "row1",
                "device_type": "printer",
                "scene_prompt": "A printer on a side table.",
                "generated_image": {"public_url": "https://example.test/scene.png"},
                "twin_image": {
                    "source_public_url": "https://example.test/twin.png"
                },
            },
            {"visual_anchors_enabled": False, "judgment": judgment},
            1,
            researcher_question="Is the inferred user position actually visible?",
        )
        self.assertEqual(
            row["images"][0]["meta_text"],
            {
                "label": "Generated scene — review this image",
                "Judge predicted verdict": "FAIL",
                "Judge final score": "59/100",
            },
        )
        self.assertEqual(
            row["images"][2],
            {
                "asset_type": "text",
                "text_content": "Is the inferred user position actually visible?",
                "meta_text": {
                    "label": "Researcher review question (not a human label)"
                },
            },
        )

    def test_review_at_100_explains_unobservable_component(self) -> None:
        judgment = {
            "natural_placement_score": 100,
            "confidence": "low",
            "coverage": 0.7,
            "verdict": "review",
            "observation": {
                "summary": "Visible components have no confirmed defect.",
                "components": {
                    "access_usability": {
                        "visibility": "unobservable",
                        "severity": None,
                        "confidence": "low",
                        "evidence": "The user side is out of frame.",
                        "consequence": "Access cannot be accepted from this view.",
                        "issue_codes": [],
                    }
                },
            },
        }
        text = BUILDER._evidence_text(judgment)
        self.assertIn(
            "Score covers assessable components only; uncertainty prevents acceptance.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
