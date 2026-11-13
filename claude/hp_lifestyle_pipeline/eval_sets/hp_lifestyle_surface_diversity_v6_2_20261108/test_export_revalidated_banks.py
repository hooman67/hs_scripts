from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import build_distribution as distribution
import export_revalidated_banks as exporter
import run_generation as runner


VALIDATION_SOURCE = '''
import copy

def validate_output(output, request, catalog, camera, references):
    failed = any("FORCE_VALIDATION_FAILURE" in row["text"] for row in output["prompts"])
    return {"passed": not failed, "errors": ([{"code": "forced_failure"}] if failed else []), "warnings": []}

def finalize_output(output, *, camera, catalog):
    value = copy.deepcopy(output)
    value["prompts"] = sorted(value["prompts"], key=lambda row: (-row["score_components"]["derived"], -row["ctech_reference_score"]))
    audit_rows = []
    for rank, row in enumerate(value["prompts"], 1):
        row["id"] = f"p{rank}"
        row["source_relevance_score"] = row["score_components"]["derived"]
        start = row["text"].index("round office table")
        support = {"family": "table", "shape": "round", "phrase": "round office table", "start": start,
                   "end": start + len("round office table"),
                   "shape_evidence": {"phrase": "round", "start": start, "end": start + 5},
                   "sentence_start": 0, "sentence_end": row["text"].index(".") + 1,
                   "device_type": "printer" if "printer" in camera["requested_tag"] else "laptop"}
        row["primary_support"] = support
        audit_rows.append({"row_id": row["id"], "environment": row["environment"],
                           "device_type": support["device_type"], "support": copy.deepcopy(support)})
    value["debug"]["primary_support_audit"] = {"passed": True, "rows": audit_rows,
        "counts": {"families": {"table": 10}, "shapes": {"round": 10}}, "errors": []}
    value["debug"]["provenance"] = {"finalizer_version": "synthetic-frozen"}
    return value
'''

CAMERA_SOURCE = '''
def resolve_camera(registry, tag):
    return {"requested_tag": tag, "resolved_tag": tag, "device_family": "printer" if tag.startswith("printer") else "laptop"}
'''


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate(case_id: str, number: int, prefix: str = "FINAL") -> dict:
    return {
        "environment": "Office",
        "text": f"A round office table anchors {prefix} recorded scene {case_id} candidate {number}. Calm daylight fills the room.",
        "prop_ids": ["P1"], "prop_mentions": ["plain tray"],
        "score_components": {"derived": 100 - number},
        "evidence": [{"document": "smart_brief", "path": "setting", "quote": "Exact source quote"}],
        "relationship": "recorded", "explanation": "source explanation", "creative_departures": [],
        "ctech_reference_id": "CT01", "ctech_reference_score": 80 - number,
        "ctech_explanation": "reference explanation", "camera_fit_explanation": "camera explanation",
    }


def normalized(case_id: str, prefix: str = "FINAL") -> dict:
    return {
        "prompts": [candidate(case_id, number, prefix) for number in range(1, 11)],
        "debug": {"source_conflicts": [], "limitations": ["recorded limitation"],
                  "environment_rationale": "recorded rationale"},
    }


def case_records() -> list[dict]:
    records = []
    for device in runner.DEVICE_ORDER:
        device_type = "printer" if device in {"tassel", "magic"} else "laptop"
        for camera in runner.VIEW_ORDER[device]:
            case_id = f"{device}__{device_type}_{camera.replace('_', '')}"
            records.append({
                "case_id": case_id, "group_id": f"{device}__{device_type}", "pair_id": device,
                "device_id": device, "device_display_name": device.title(), "device_type": device_type,
                "camera_tag": f"{device_type}_{camera.replace('_', '')}", "source_camera_name": camera,
                "view_role": camera, "render_gallery_url": "https://example.invalid/gallery",
                "render_lookup": {"device_name": device.title(), "camera_name": camera},
                "source_pair": device, "product_identity_conflict": False,
                "source_input_path": f"/original/{case_id}.json",
                "source_input_sha256": exporter.sha256_bytes((case_id + "original").encode()),
                "frozen_input_path": f"inputs/{case_id}.json",
            })
    return records


class Fixture:
    def __init__(self, root: Path, *, fail_bank: str | None = None) -> None:
        self.source = root / "source-r4"
        self.validation = root / "validation-r5"
        self.cases = case_records()
        self._create_snapshot(self.source, runtime_kind="source")
        self._create_snapshot(self.validation, runtime_kind="validation")
        self._create_results(fail_bank)

    def _create_snapshot(self, path: Path, runtime_kind: str) -> None:
        runtime = path / "runtime/v6_2"
        runtime.mkdir(parents=True)
        (runtime / "__init__.py").write_text("", encoding="utf-8")
        if runtime_kind == "validation":
            (runtime / "validation.py").write_text(VALIDATION_SOURCE, encoding="utf-8")
            (runtime / "camera.py").write_text(CAMERA_SOURCE, encoding="utf-8")
            for name in ("surfaces.py", "content_policy.py", "catalog.py"):
                (runtime / name).write_text("# frozen synthetic module\n", encoding="utf-8")
        else:
            (runtime / "cli.py").write_text("# source runtime cli\n", encoding="utf-8")
        write_json(runtime / "input.schema.json", {"type": "object", "title": "input"})
        write_json(runtime / "model_output.schema.json", {"type": "object"})
        write_json(runtime / "camera_profiles.json", {"version": "synthetic", "profiles": []})
        write_json(runtime / "reference_library.json", {"version": "synthetic", "references": []})
        write_json(runtime / "prop_lexicon.json", {"version": "synthetic", "entries": []})
        (runtime / "system_prompt.md").write_text("Synthetic frozen system prompt.\n", encoding="utf-8")
        write_json(runtime / "approved_catalog.json", {"version": "synthetic", "entries": [{"id": "P1"}]})
        prepared_cases = []
        for case in self.cases:
            source = {"smart_brief": {"setting": "Exact source quote"},
                      "source_messaging": {"message": case["case_id"]}, "camera_tag": case["camera_tag"]}
            input_path = path / case["frozen_input_path"]
            write_json(input_path, source)
            item = copy.deepcopy(case)
            item["frozen_input_sha256"] = exporter.sha256_path(input_path)
            prepared_cases.append(item)
        manifest = {
            "version": "synthetic-snapshot", "revision": path.name,
            "authorized_text_case_ids": [case["case_id"] for case in prepared_cases],
            "cases": prepared_cases,
            "scope": {"selection_rule": "stable source and C-Tech ranking"},
            "device_source_mapping": [{"device_id": device} for device in runner.DEVICE_ORDER],
            "catalog": {"frozen_path": "runtime/v6_2/approved_catalog.json"},
            "snapshot_assets": exporter._snapshot_assets(path),
        }
        write_json(path / "snapshot_manifest.json", manifest)

    def _create_results(self, fail_bank: str | None) -> None:
        run_cases = {}
        for index, case in enumerate(self.cases):
            case_id = case["case_id"]
            final = normalized(case_id)
            if case_id == fail_bank:
                final["prompts"][0]["text"] += " FORCE_VALIDATION_FAILURE"
            first = normalized(case_id, "OLD_ATTEMPT_MUST_NOT_EXPORT")
            provider = {"model": "gpt-5.5-test", "finish_reason": "stop", "usage": {"total_tokens": 1},
                        "transport_attempts": 1, "transport_events": [], "settings": {"model": "gpt-5.5"}}
            attempts = []
            for number, (kind, value, errors) in enumerate((
                ("initial", first, [{"code": "initial_rejection"}]),
                ("semantic_repair", final, [{"code": "source_runtime_false_rejection"}]),
            ), 1):
                raw = json.dumps(value, ensure_ascii=False)
                attempts.append({"number": number, "kind": kind, "raw_content": raw,
                                 "parsed_output": copy.deepcopy(value), "normalized_output": copy.deepcopy(value),
                                 "normalization_changes": [], "errors": errors, "provider": copy.deepcopy(provider),
                                 "text_changes": None, "duration_ms": 1})
                journal = self.source / "results" / f"{case_id}.json.run"
                write_json(journal / f"attempt_{number}.request.json", {"messages": [{"role": "user", "content": case_id}],
                                                                        "schema": {"type": "object"}})
                write_json(journal / f"attempt_{number}.response.json", {"content": raw, "refusal": None, **provider})
            source_status = "error" if index < 3 else "ok"
            result = {
                "status": source_status,
                "error": {"code": "source_runtime_false_rejection"} if source_status == "error" else None,
                "prompts": [] if source_status == "error" else [{"id": "stale-source-finalized"}],
                "debug": None if source_status == "error" else {"service": "source runtime"},
                "audit": {
                    "version": "source-runtime", "attempts": attempts, "semantic_calls": 2,
                    "transport_attempts_known": 2, "transport_accounting_complete": True,
                    "source_input": json.loads((self.source / case["frozen_input_path"]).read_text()),
                    "system": {
                        "sha256": exporter.sha256_path(self.source / "runtime/v6_2/system_prompt.md"),
                        "character_count": len((self.source / "runtime/v6_2/system_prompt.md").read_text()),
                    },
                    "schema": {
                        "input_sha256": exporter.canonical_sha256(json.loads((self.source / "runtime/v6_2/input.schema.json").read_text())),
                        "base_model_output_sha256": exporter.canonical_sha256(json.loads((self.source / "runtime/v6_2/model_output.schema.json").read_text())),
                        "effective_model_output_sha256": exporter.canonical_sha256({"type": "object"}),
                    },
                    "catalog": {"catalog_sha256": exporter.canonical_sha256(json.loads((self.source / "runtime/v6_2/approved_catalog.json").read_text()))},
                    "assets": {
                        "camera_registry_sha256": exporter.canonical_sha256(json.loads((self.source / "runtime/v6_2/camera_profiles.json").read_text())),
                        "reference_library_sha256": exporter.canonical_sha256(json.loads((self.source / "runtime/v6_2/reference_library.json").read_text())),
                        "prop_lexicon_sha256": exporter.sha256_path(self.source / "runtime/v6_2/prop_lexicon.json"),
                    },
                },
            }
            result_path = self.source / "results" / f"{case_id}.json"
            write_json(result_path, result)
            input_path = self.source / case["frozen_input_path"]
            launch_path = self.source / "call_journals" / f"{case_id}.launch.json"
            write_json(launch_path, {"case_id": case_id, "recorded_before_provider_process_start": True,
                                     "input_sha256": exporter.sha256_path(input_path),
                                     "catalog_sha256": exporter.sha256_path(self.source / "runtime/v6_2/approved_catalog.json"),
                                     "runtime_cli_sha256": exporter.sha256_path(self.source / "runtime/v6_2/cli.py")})
            process_path = self.source / "call_journals" / f"{case_id}.process.json"
            process = {"case_id": case_id, "returncode": 2 if source_status == "error" else 0,
                       "output_exists": True, "output_sha256": exporter.sha256_path(result_path)}
            write_json(process_path, process)
            run_cases[case_id] = copy.deepcopy(process)
        write_json(self.source / "run_complete.json", {
            "case_count": 16, "process_successes": 13, "process_failures": 3,
            "all_processes_succeeded": False, "cases": run_cases,
        })


class ExportRevalidatedBanksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_strict_final_attempt_export_and_runner_compatibility(self) -> None:
        fixture = Fixture(self.root)
        output = self.root / "derived-export"
        result = exporter.export_revalidated(fixture.source, fixture.validation, output)
        self.assertEqual({"error": 3, "ok": 13}, result["source_status_counts"])
        document = json.loads((output / "prompts_all_160.json").read_text())
        self.assertEqual(160, len(document["prompts"]))
        self.assertTrue(all("FINAL recorded scene" in row["text"] for row in document["prompts"]))
        self.assertTrue(all("OLD_ATTEMPT_MUST_NOT_EXPORT" not in row["text"] for row in document["prompts"]))
        digest = exporter.sha256_path(output / "prompts_all_160.json")
        rows = runner.validate_prompt_document(document, output / "prompts_all_160.json", digest)
        self.assertEqual(160, len(rows))
        self.assertEqual(160, len([distribution.primary_support(row["prompt"]) for row in rows]))
        first_bank = document["bank_audit"][document["prompts"][0]["bank_debug_ref"]]
        self.assertEqual(2, first_bank["selected_attempt"])
        self.assertEqual("strict source-revision final actual attempt normalized_output only",
                         first_bank["selection_policy"])
        self.assertEqual({"code": "source_runtime_false_rejection"},
                         first_bank["source_terminal_result"]["error"])
        self.assertEqual(2, len(first_bank["recorded_attempts"]))
        self.assertEqual("initial_rejection", first_bank["recorded_attempts"][0]["errors"][0]["code"])
        self.assertEqual(96, len(json.loads((output / "prompts_top6_96.json").read_text())["prompts"]))

    def test_any_frozen_validation_failure_aborts_without_output(self) -> None:
        case_id = case_records()[7]["case_id"]
        fixture = Fixture(self.root, fail_bank=case_id)
        output = self.root / "must-not-exist"
        with self.assertRaisesRegex(ValueError, "frozen revalidation failed for 1 bank"):
            exporter.export_revalidated(fixture.source, fixture.validation, output)
        self.assertFalse(output.exists())

    def test_raw_response_or_snapshot_input_drift_is_rejected(self) -> None:
        fixture = Fixture(self.root)
        case_id = fixture.cases[0]["case_id"]
        response = fixture.source / "results" / f"{case_id}.json.run/attempt_2.response.json"
        value = json.loads(response.read_text())
        value["content"] += "tampered"
        write_json(response, value)
        with self.assertRaisesRegex(ValueError, "raw response content differs"):
            exporter.export_revalidated(fixture.source, fixture.validation, self.root / "bad-journal")
        self.assertFalse((self.root / "bad-journal").exists())

    def test_internally_consistent_validation_snapshot_with_different_input_is_rejected(self) -> None:
        fixture = Fixture(self.root)
        case = fixture.cases[0]
        input_path = fixture.validation / case["frozen_input_path"]
        changed = json.loads(input_path.read_text())
        changed["source_messaging"]["message"] += " changed"
        write_json(input_path, changed)
        manifest_path = fixture.validation / "snapshot_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        new_hash = exporter.sha256_path(input_path)
        next(item for item in manifest["cases"] if item["case_id"] == case["case_id"])["frozen_input_sha256"] = new_hash
        manifest["snapshot_assets"] = exporter._snapshot_assets(fixture.validation)
        write_json(manifest_path, manifest)
        output = self.root / "different-input"
        with self.assertRaisesRegex(ValueError, "source input bytes differ between snapshots"):
            exporter.export_revalidated(fixture.source, fixture.validation, output)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
