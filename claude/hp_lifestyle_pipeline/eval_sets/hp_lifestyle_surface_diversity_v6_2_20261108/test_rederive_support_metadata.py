from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path

import rederive_support_metadata as derive
import run_generation as runner
import build_distribution as distribution


LIVE_SURFACES = (
    Path(__file__).resolve().parents[2]
    / "research/source_messaging_v1_to_v6/versions/v6_2/surfaces.py"
)


def laptop_text(rank: int) -> tuple[str, str]:
    if rank == 1:
        return "A circular living-room end table anchors a calm home workspace. Soft daylight fills the room.", "Home"
    if rank == 2:
        return "A round bistro table anchors a quiet neighborhood café. Soft daylight fills the room.", "Café"
    if rank == 3:
        return "A round dining-room table anchors a calm home workspace. Soft daylight fills the room.", "Home"
    return "A rectangular office desk anchors a focused office workspace. Soft daylight fills the room.", "Office"


def printer_text(rank: int) -> str:
    if rank <= 3:
        return "A dedicated printer work table supports the device in an office. Soft daylight fills the room."
    if rank <= 6:
        return "A wide freestanding storage cabinet supports the device in an office. Soft daylight fills the room."
    if rank <= 8:
        return "A broad sturdy low credenza supports the device in an office. Soft daylight fills the room."
    return "A built-in equipment counter supports the device in an office. Soft daylight fills the room."


def synthetic_document(surfaces: types.ModuleType) -> dict:
    prompts = []
    bank_audit = {}
    for device in runner.DEVICE_ORDER:
        device_type = "printer" if device in {"tassel", "magic"} else "laptop"
        for camera in runner.VIEW_ORDER[device]:
            bank_id = f"{device}__{device_type}_{camera.replace('_', '')}"
            audit_rows = []
            bank_prompts = []
            for rank in range(1, 11):
                text, environment = laptop_text(rank) if device_type == "laptop" else (printer_text(rank), "Office")
                support = surfaces.infer_primary_support(text, device_type)
                if rank == 1 and device_type == "laptop":
                    support = copy.deepcopy(support)
                    support["shape"] = "unspecified"
                    support["shape_evidence"] = None
                row = {
                    "prompt_key": f"{bank_id}::p{rank}", "id": f"p{rank}", "bank_debug_ref": bank_id,
                    "bank_rank": rank, "device_id": device, "device_display_name": device.title(),
                    "device_type": device_type, "source_pair": "synthetic", "camera_tag": f"{device_type}_{camera}",
                    "source_camera_name": camera, "view_role": camera, "render_gallery_url": "https://example.invalid",
                    "render_lookup": {"synthetic": True}, "environment": environment, "text": text,
                    "text_sha256": hashlib.sha256(text.encode()).hexdigest(), "primary_support": support,
                    "source_relevance_score": 80, "ctech_reference_score": 75, "ctech_reference_id": "CT01",
                    "score_components": {"source": 80}, "evidence": [{"document": "brief", "quote": "Exact quote"}],
                    "prop_ids": ["P1"], "prop_mentions": ["plain prop"], "relationship": "synthetic",
                    "explanation": "source", "ctech_explanation": "ctech", "camera_fit_explanation": "camera",
                    "creative_departures": [],
                }
                bank_prompts.append(row)
                audit_rows.append({"id": row["id"], "text": text, "device_type": device_type,
                                   "environment": environment})
            audit = surfaces.audit_bank(audit_rows, device_type)
            if device_type == "laptop":
                audit = copy.deepcopy(audit)
                first = audit["rows"][0]["support"]
                first["shape"] = "unspecified"
                first["shape_evidence"] = None
                audit["counts"]["shapes"]["round"] -= 1
                audit["counts"]["shapes"]["unspecified"] = audit["counts"]["shapes"].get("unspecified", 0) + 1
            prompts.extend(bank_prompts)
            bank_audit[bank_id] = {
                "selected_result_path": f"/immutable/results/{bank_id}.json",
                "selected_result_sha256": hashlib.sha256(bank_id.encode()).hexdigest(),
                "selected_raw_output_sha256": hashlib.sha256((bank_id + "raw").encode()).hexdigest(),
                "source_input_path": f"/immutable/inputs/{bank_id}.json",
                "source_input_sha256": hashlib.sha256((bank_id + "source").encode()).hexdigest(),
                "manual_prompt_edits": False, "additional_model_calls": 0,
                "debug": {"primary_support_audit": audit, "provider_attempt": 1},
            }
    return {
        "version": "hp-lifestyle-spatial-composition-v6.2-all-four-devices-v1",
        "revision": "synthetic-original-r4", "selection_rule": "unchanged",
        "device_source_mapping": [{"device": device} for device in runner.DEVICE_ORDER],
        "bank_audit": bank_audit, "provenance": {"kind": "recorded_model_output"},
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16,
                   "candidates_per_bank": 10, "prompts": 160},
        "prompts": prompts,
    }


class RederiveSupportMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.surface_sha = derive.sha256_path(LIVE_SURFACES)
        cls.surfaces = derive.load_surfaces(LIVE_SURFACES, cls.surface_sha)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.document = synthetic_document(self.surfaces)
        self.input = self.root / "prompts_all_160.json"
        self.input.write_text(json.dumps(self.document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.input_sha = derive.sha256_path(self.input)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_living_room_correction_and_production_export_compatibility(self) -> None:
        output = self.root / "derived"
        result = derive.create_export(self.input, self.input_sha, LIVE_SURFACES, self.surface_sha, output, True)
        self.assertEqual(8, result["changed_support_rows"])
        self.assertEqual(self.input_sha, derive.sha256_path(self.input))
        final = json.loads((output / "prompts_all_160.json").read_text())
        original = self.document
        self.assertEqual([row["prompt_key"] for row in original["prompts"]],
                         [row["prompt_key"] for row in final["prompts"]])
        for before, after in zip(original["prompts"], final["prompts"], strict=True):
            self.assertEqual(derive._without_support(before), derive._without_support(after))
        living_rows = [row for row in final["prompts"] if "circular living-room end table" in row["text"]]
        self.assertEqual(8, len(living_rows))
        self.assertTrue(all(row["primary_support"]["shape"] == "round" for row in living_rows))
        self.assertTrue(all(row["primary_support"]["phrase"] == "circular living-room end table" for row in living_rows))
        rows = runner.validate_prompt_document(final, output / "prompts_all_160.json",
                                               derive.sha256_path(output / "prompts_all_160.json"))
        self.assertEqual(160, len(rows))
        self.assertEqual(160, len([distribution.primary_support(row["prompt"]) for row in rows]))
        top = json.loads((output / "prompts_top6_96.json").read_text())
        self.assertEqual(96, len(top["prompts"]))
        self.assertTrue(all(row["bank_rank"] <= 6 for row in top["prompts"]))
        audit = json.loads((output / "support_metadata_changes.json").read_text())
        self.assertEqual({"rows": 160, "changed": 8, "unchanged": 152}, audit["summary"])
        first_bank = final["prompts"][0]["bank_debug_ref"]
        self.assertIn("original_debug", final["bank_audit"][first_bank])
        self.assertEqual(self.document["bank_audit"][first_bank]["selected_raw_output_sha256"],
                         final["bank_audit"][first_bank]["selected_raw_output_sha256"])

    def test_shape_label_must_match_exact_frozen_text_evidence(self) -> None:
        bad = types.ModuleType("bad_surfaces")

        def infer(text: str, device_type: str | None = None) -> dict:
            support = copy.deepcopy(self.surfaces.infer_primary_support(text, device_type))
            if "circular living-room" in text:
                support["shape"] = "oval"
            return support

        def audit(rows: list[dict], device_type: str | None = None) -> dict:
            evidence = [{"row_id": row["id"], "environment": row.get("environment"),
                         "device_type": row.get("device_type"),
                         "support": infer(row["text"], row.get("device_type"))} for row in rows]
            return {"passed": True, "rows": evidence, "counts": {"families": {}, "shapes": {}}, "errors": []}

        bad.infer_primary_support = infer
        bad.audit_bank = audit
        with self.assertRaisesRegex(ValueError, "shape label 'oval' disagrees"):
            derive.derive_document(
                self.document, bad, input_path=self.input, input_sha256=self.input_sha,
                surfaces_path=LIVE_SURFACES, surfaces_sha256=self.surface_sha,
                tool_path=Path(derive.__file__), tool_sha256=derive.sha256_path(Path(derive.__file__)),
            )

    def test_hash_pin_and_immutable_destination_are_enforced(self) -> None:
        with self.assertRaisesRegex(ValueError, "input export SHA-256 mismatch"):
            derive.create_export(self.input, "0" * 64, LIVE_SURFACES, self.surface_sha,
                                 self.root / "never", False)
        destination = self.root / "exists"
        destination.mkdir()
        with self.assertRaisesRegex(FileExistsError, "already exists"):
            derive.create_export(self.input, self.input_sha, LIVE_SURFACES, self.surface_sha,
                                 destination, False)


if __name__ == "__main__":
    unittest.main()
