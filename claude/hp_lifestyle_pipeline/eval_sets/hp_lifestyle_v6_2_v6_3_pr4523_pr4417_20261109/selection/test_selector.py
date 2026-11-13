"""Synthetic, local-only tests; the recorded V6.2 source is never edited."""

import copy
import hashlib
import importlib.util
import io
import json
import shutil
import unittest
import uuid
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE.parents[1]
    / "hp_lifestyle_surface_diversity_v6_2_20261108"
    / "exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json"
)
SPEC = importlib.util.spec_from_file_location("hp_study_selector", HERE / "selector.py")
selector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selector)


def synthetic_copy(source, version):
    result = copy.deepcopy(source)
    result["version"] = f"synthetic-{version}"
    result["selection_rule"] = "synthetic 160-record test fixture, not study output"
    snapshot = result["provenance"]["validation_snapshot"]
    result["snapshot_manifest_path"] = snapshot["manifest_path"]
    result["snapshot_manifest_sha256"] = snapshot["manifest_sha256"]
    for row in result["prompts"]:
        rank = row["bank_rank"]
        row["text"] = (
            f"Synthetic {version} {row['device_id']} {row['camera_tag']} "
            f"scene {rank} with shared desk details and a variation {rank % 3}."
        )
        row["text_sha256"] = hashlib.sha256(row["text"].encode()).hexdigest()
        row["environment"] = ("Office", "Home", "Cafe")[rank % 3]
        row["ctech_reference_id"] = f"SYNTHETIC-REF-{rank % 4}"
        row["source_relevance_score"] = 100 - rank * 3
        row["ctech_reference_score"] = 40 + rank * 5
        row["prop_ids"] = [f"synthetic-prop-{rank % 5}"]
        row["creative_departures"] = ["synthetic departure"] if rank % 4 == 0 else []
        row["synthetic_extra_field"] = {"must_survive": version}
    return result


class SelectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_bytes = SOURCE.read_bytes()
        cls.original = json.loads(cls.original_bytes)
        cls.v63 = synthetic_copy(cls.original, "v6.3")
        cls.v62 = synthetic_copy(cls.original, "v6.2")
        cls.source_copy = copy.deepcopy(cls.v63)
        cls.selected = selector.select_prompts(cls.v63)

    @classmethod
    def tearDownClass(cls):
        if SOURCE.read_bytes() != cls.original_bytes:
            raise AssertionError("real V6.2 source changed during tests")

    def test_exact_30_all_banks_devices_7_or_8_and_preservation(self):
        rows = self.selected["prompts"]
        banks = Counter(selector._bank(row) for row in rows)
        self.assertEqual(len(rows), 30)
        self.assertEqual(len(banks), 16)
        self.assertEqual(Counter(banks.values()), {2: 14, 1: 2})
        self.assertEqual(sorted(Counter(row["device_id"] for row in rows).values()),
                         [7, 7, 8, 8])
        self.assertEqual(len({device for (device, _), n in banks.items() if n == 1}), 2)
        source_index = {selector._key(row): row for row in self.v63["prompts"]}
        for row in rows:
            self.assertEqual(row, source_index[selector._key(row)])
        self.assertEqual(self.selected["provenance"], self.v63["provenance"])
        self.assertEqual(self.v63, self.source_copy)
        metadata = self.selected["selection"]
        self.assertEqual(metadata["seed"], 42)
        self.assertEqual(metadata["target_proportion"], 30 / 160)
        self.assertEqual(metadata["source_counts"]["candidates_per_bank"], 10)
        self.assertIn("not an optimality guarantee", metadata["caveat"])
        full_features = Counter()
        for row in self.v63["prompts"]:
            full_features.update(selector._features(row))
        targets = {key: count * (30 / 160) for key, count in full_features.items()}
        selected_by_bank = {
            bank: [row for row in rows if selector._bank(row) == bank]
            for bank in sorted(banks)
        }
        objective, _, _ = selector._objective(
            [selector._option(records) for records in selected_by_bank.values()],
            targets,
            16,
        )
        self.assertEqual(metadata["objective"], objective)

    def test_determinism_including_shuffled_input(self):
        self.assertEqual(selector.select_prompts(self.v63), self.selected)
        shuffled = copy.deepcopy(self.v63)
        shuffled["prompts"].reverse()
        other = selector.select_prompts(shuffled)
        self.assertEqual(other["prompts"], self.selected["prompts"])
        self.assertEqual(other["selection"]["objective"],
                         self.selected["selection"]["objective"])

    def test_corrupted_text_hash_rejected(self):
        data = copy.deepcopy(self.v63)
        data["prompts"][0]["text"] += " corruption"
        with self.assertRaisesRegex(ValueError, "text_sha256 mismatch"):
            selector.select_prompts(data)

    def test_duplicate_and_missing_ranks_rejected(self):
        duplicate = copy.deepcopy(self.v63)
        duplicate["prompts"][1]["bank_rank"] = duplicate["prompts"][0]["bank_rank"]
        missing_field = copy.deepcopy(self.v63)
        del missing_field["prompts"][0]["bank_rank"]
        removed = copy.deepcopy(self.v63)
        removed["prompts"].pop()
        for data in (duplicate, missing_field, removed):
            with self.subTest(case=len(data["prompts"])):
                with self.assertRaises(ValueError):
                    selector.select_prompts(data)
        uneven = copy.deepcopy(self.v63)
        uneven["prompts"][0]["camera_tag"] = "extra-view"
        with self.assertRaisesRegex(ValueError, "four devices"):
            selector.select_prompts(uneven)

    def test_invalid_finite_scores_rejected(self):
        for field in ("source_relevance_score", "ctech_reference_score"):
            for value in (float("nan"), float("inf"), -float("inf"),
                          -1, 101, True, "90", None):
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.v63)
                    data["prompts"][0][field] = value
                    with self.assertRaisesRegex(ValueError, "finite and in 0..100"):
                        selector.select_prompts(data)

    def test_required_metadata_props_and_prompt_keys(self):
        mutations = [
            ("version", ""),
            ("selection_rule", ""),
            ("snapshot_manifest_path", ""),
            ("snapshot_manifest_sha256", "invalid"),
            ("device_source_mapping", []),
        ]
        for field, value in mutations:
            with self.subTest(field=field):
                data = copy.deepcopy(self.v63)
                data[field] = value
                with self.assertRaises(ValueError):
                    selector.select_prompts(data)
        for field, value in (
            ("prop_ids", ["duplicate", "duplicate"]),
            ("prop_ids", [42]),
            ("creative_departures", "not a list"),
            ("creative_departures", [None]),
            ("prompt_key", self.v63["prompts"][1]["prompt_key"]),
        ):
            with self.subTest(field=field):
                data = copy.deepcopy(self.v63)
                data["prompts"][0][field] = value
                with self.assertRaises(ValueError):
                    selector.select_prompts(data)

    def test_actual_legacy_baseline_schema_validates_without_selection(self):
        banks = selector._validate_document(self.original)
        self.assertEqual(len(banks), 16)
        self.assertEqual(selector._snapshot(self.original)["metadata_location"],
                         "provenance.validation_snapshot")
        _, metadata = selector._read_input(SOURCE)
        self.assertEqual(metadata["sha256"], selector._sha(self.original_bytes))

    def test_exact_baseline_matching_not_independent_selection(self):
        baseline = copy.deepcopy(self.v62)
        baseline["prompts"].reverse()
        for row in baseline["prompts"]:
            row["environment"] = "Deliberately different environment"
            row["ctech_reference_score"] = 1
        expected = {selector._key(row): row for row in baseline["prompts"]}
        with patch.object(selector, "select_prompts",
                          side_effect=AssertionError("must not optimize baseline")):
            matched = selector.match_baseline(self.selected, baseline)
        self.assertEqual([selector._key(row) for row in matched["prompts"]],
                         [selector._key(row) for row in self.selected["prompts"]])
        self.assertEqual(matched["prompts"],
                         [expected[selector._key(row)] for row in self.selected["prompts"]])
        self.assertEqual(matched["provenance"], baseline["provenance"])
        bad = copy.deepcopy(baseline)
        for row in bad["prompts"]:
            if row["device_id"] == "cashmere":
                row["device_id"] = "renamed-device"
        for mapping in bad["device_source_mapping"]:
            if mapping["device_id"] == "cashmere":
                mapping["device_id"] = "renamed-device"
        with self.assertRaisesRegex(ValueError, "bank keys must match exactly"):
            selector.match_baseline(self.selected, bad)
        bad = copy.deepcopy(baseline)
        bad["prompts"][0]["text_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "text_sha256 mismatch"):
            selector.match_baseline(self.selected, bad)

    def test_feature_targets_pair_options_and_objective(self):
        row = copy.deepcopy(self.v63["prompts"][0])
        row["source_relevance_score"] = 100
        row["ctech_reference_score"] = 100
        features = selector._features(row)
        self.assertIn(("source_score_band", 10), features)
        self.assertIn(("reference_score_band", 20), features)
        self.assertEqual({key[0] for key in features}, set(selector.WEIGHTS))
        bank = self.v63["prompts"][:10]
        option = selector._option([row, row])
        targets = {key: count * (30 / 160)
                   for key, count in option["features"].items()}
        targets[("environment", "Missing")] = 10 * (30 / 160)
        objective, _, _ = selector._objective([option], targets, 16)
        self.assertEqual(objective["duplicate_texts"], 1)
        self.assertEqual(objective["missing_environments"], 1)
        self.assertEqual(objective["within_bank_jaccard_divided_by_16"], 1 / 16)
        self.assertAlmostEqual(
            objective["total"],
            objective["weighted_absolute_deviation_divided_by_30"]
            + 1 / 16 + 1000 + 1,
        )
        a = selector._option(bank[:2])
        b = selector._option(bank[2:4])
        full = Counter()
        for record in bank:
            full.update(selector._features(record))
        targets = {key: value * 30 / 160 for key, value in full.items()}
        before, counts, texts = selector._objective([a], targets, 16)
        after, _, _ = selector._objective([b], targets, 16)
        self.assertAlmostEqual(selector._delta(a, b, counts, texts, targets, 16),
                               after["total"] - before["total"])

    def test_cli_synthetic_exports_hash_checks_and_exclusive_output(self):
        work = HERE / f".test-artifacts-{uuid.uuid4().hex}"
        work.mkdir()
        try:
            manifest = work / "synthetic_manifest.json"
            manifest.write_text('{"synthetic": true}\n', encoding="utf-8")
            inputs = []
            for name, data in (("v63", self.v63), ("v62", self.v62)):
                fixture = copy.deepcopy(data)
                fixture["snapshot_manifest_path"] = str(manifest)
                fixture["snapshot_manifest_sha256"] = selector._sha(manifest.read_bytes())
                path = work / f"{name}.json"
                path.write_text(json.dumps(fixture), encoding="utf-8")
                inputs.append(path)
            output = work / "new-output"
            argv = [str(inputs[0]), "--baseline", str(inputs[1]),
                    "--output-dir", str(output), "--seed", "42"]
            # Optimization is already tested above; this test targets CLI I/O.
            def reuse_selection(data, seed):
                metadata = copy.deepcopy(self.selected["selection"])
                metadata["source_document_sha256"] = selector._canonical_sha(data)
                metadata["source_snapshot"] = selector._snapshot(data)
                metadata["seed"] = seed
                return selector._selected_document(
                    data, self.selected["prompts"], metadata
                )

            with patch.object(selector, "select_prompts", side_effect=reuse_selection), \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(selector.main(argv), 0)
            self.assertEqual({p.name for p in output.iterdir()}, {
                "selected_v6_3_30.json", "selected_v6_3_30.txt",
                "selected_v6_2_30.json", "selected_v6_2_30.txt", "selection_report.json",
            })
            report = json.loads((output / "selection_report.json").read_text())
            self.assertEqual(report["sources"]["v6_3"]["sha256"],
                             selector._sha(inputs[0].read_bytes()))
            exported = json.loads((output / "selected_v6_3_30.json").read_text())
            self.assertEqual(exported["selection"]["source_document_sha256"],
                             report["sources"]["v6_3"]["canonical_json_sha256"])
            self.assertEqual(len(report["pair_keys"]), 30)
            for name, digest in report["output_sha256"].items():
                self.assertEqual(selector._sha((output / name).read_bytes()), digest)
            contents = {p.name: p.read_bytes() for p in output.iterdir()}
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                selector.main(argv)
            self.assertEqual(exc.exception.code, 2)
            self.assertEqual(contents, {p.name: p.read_bytes() for p in output.iterdir()})
            manifest.write_text("changed snapshot", encoding="utf-8")
            argv[4] = str(work / "must-not-exist")
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                selector.main(argv)
            self.assertEqual(exc.exception.code, 2)
            self.assertFalse((work / "must-not-exist").exists())
        finally:
            shutil.rmtree(work)


if __name__ == "__main__":
    unittest.main()
