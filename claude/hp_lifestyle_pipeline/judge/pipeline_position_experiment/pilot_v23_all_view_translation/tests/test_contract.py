from __future__ import annotations

import unittest

from common import load_json, sha256_file, sha256_json
from config import (
    EXPECTED_CELLS,
    FREEZE,
    JOB_ROOT,
    LOG_ROOT,
    MAX_OUTER_JOBS,
    PACKAGE,
    PIPELINE_VERSION,
    PROGRESS,
    RUN_ROOT,
    SELECTED_ROW_SLUGS,
    SOURCE_HASHES,
)
from preflight import verify
from run_pilot import job_id


class PilotContractTest(unittest.TestCase):
    def test_preflight_and_exact_four_cell_selection(self):
        result = verify(allow_progress=True)
        self.assertEqual(result["rows"], 4)
        self.assertEqual(MAX_OUTER_JOBS, 1)
        freeze = load_json(FREEZE)
        self.assertEqual(tuple(freeze["selected_row_slugs"]), SELECTED_ROW_SLUGS)
        self.assertEqual(tuple(tuple(x) for x in freeze["expected_cells"]), EXPECTED_CELLS)
        self.assertEqual([x["bank_rank"] for x in freeze["records"]], [1, 1, 1, 1])

    def test_frozen_v23_sources_are_exact(self):
        actual = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
        self.assertEqual(actual, SOURCE_HASHES)
        freeze = load_json(FREEZE)
        self.assertEqual(actual, freeze["treatment"]["source_hashes"])
        self.assertEqual(freeze["treatment"]["pipeline_version"], PIPELINE_VERSION)

    def test_freeze_payload_and_record_hashes(self):
        freeze = load_json(FREEZE)
        payload = dict(freeze)
        expected = payload.pop("freeze_payload_sha256")
        self.assertEqual(sha256_json(payload), expected)
        for row in freeze["records"]:
            self.assertEqual(sha256_file(__import__("pathlib").Path(row["path"])), row["sha256"])

    def test_single_outer_job_identity(self):
        self.assertEqual(job_id("fixture"), "fixture__outer_job_1")
        self.assertEqual(MAX_OUTER_JOBS, 1)

    def test_preparation_did_not_launch_or_create_runtime_trees(self):
        self.assertFalse(RUN_ROOT.exists())
        self.assertFalse(JOB_ROOT.exists())
        self.assertFalse(PROGRESS.exists())
        self.assertFalse(LOG_ROOT.exists())


if __name__ == "__main__":
    unittest.main()
