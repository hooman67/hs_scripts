from __future__ import annotations

import base64
import hashlib
import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from build_fe_report import (
    PUBLISH_DESTINATION,
    QUESTION,
    REPORT_ROOT,
    TITLE,
    review_url,
    static_contract,
)
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
    ROOT,
    RUN_ROOT,
    SELECTED_ROWS,
    SOURCE_HASHES,
)
from diagnostic_prompts import PROMPTS, SOURCE
from freeze_inputs import audited_diagnostic_prompts
from preflight import verify
from run_pilot import job_id


class PilotContractTest(unittest.TestCase):
    def test_preflight_and_exact_eight_cell_selection(self):
        result = verify(allow_progress=True)
        self.assertEqual((result["rows"], result["representative_rows"],
                          result["movement_demand_rows"]), (8, 4, 4))
        self.assertEqual(MAX_OUTER_JOBS, 1)
        freeze = load_json(FREEZE)
        self.assertEqual(freeze["selected_row_slugs"], [x[0] for x in SELECTED_ROWS])
        self.assertEqual(tuple(tuple(x) for x in freeze["expected_cells"]), EXPECTED_CELLS)
        self.assertEqual([x["bank_rank"] for x in freeze["records"]], [1] * 8)

    def test_cohorts_are_explicit_and_balanced(self):
        freeze = load_json(FREEZE)
        cohorts = [x["cohort"] for x in freeze["records"]]
        self.assertEqual(cohorts[:4], ["representative_v6_1"] * 4)
        self.assertEqual(cohorts[4:], ["movement_demand_diagnostic"] * 4)
        self.assertEqual(
            [(x["device_type"], x["camera_id"]) for x in freeze["records"][4:]],
            [("laptop", "Front_CloseUp"), ("laptop", "Front_Wide"),
             ("printer", "Front_CloseUp"), ("printer", "Front_Wide")],
        )

    def test_diagnostic_prompts_are_exact_audited_fixtures(self):
        self.assertEqual(PROMPTS, audited_diagnostic_prompts(Path(SOURCE)))
        freeze = load_json(FREEZE)
        for row in freeze["records"][4:]:
            self.assertEqual(row["prompt"], PROMPTS[row["row_slug"]])
            self.assertEqual(hashlib.sha256(row["prompt"].encode()).hexdigest(),
                             row["prompt_sha256"])

    def test_frozen_v23_1_sources_are_exact(self):
        actual = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
        self.assertEqual(actual, SOURCE_HASHES)
        freeze = load_json(FREEZE)
        self.assertEqual(actual, freeze["treatment"]["source_hashes"])
        self.assertEqual(freeze["treatment"]["pipeline_version"], PIPELINE_VERSION)

    def test_freeze_payload_and_source_record_hashes(self):
        freeze = load_json(FREEZE)
        payload = dict(freeze)
        expected = payload.pop("freeze_payload_sha256")
        self.assertEqual(sha256_json(payload), expected)
        for row in freeze["records"]:
            self.assertEqual(sha256_file(Path(row["path"])), row["sha256"])

    def test_one_outer_job_and_isolation(self):
        self.assertEqual(job_id("fixture"), "fixture__outer_job_1")
        self.assertEqual(MAX_OUTER_JOBS, 1)
        self.assertNotEqual(ROOT, ROOT.parent / "pilot_v23_all_view_translation")
        self.assertIn("pilot_v23_1_all_view_translation", str(RUN_ROOT))
        self.assertEqual(JOB_ROOT.parent, RUN_ROOT)
        self.assertEqual(PROGRESS.parent, RUN_ROOT)
        self.assertEqual(LOG_ROOT.parent, ROOT)

    def test_fe_builder_is_static_gated_and_has_frozen_review_contract(self):
        contract = static_contract()
        self.assertFalse(contract["build_performed"])
        self.assertFalse(contract["upload_performed"])
        self.assertEqual(
            TITLE,
            "HP V23.1 all-view rigid-translation pilot — representative and movement-demand cases",
        )
        self.assertEqual(
            PUBLISH_DESTINATION,
            "s3://foundry-hp-enterprise-adobe-assets/"
            "hp_position_flex_v23_1_pilot_20261106/review/",
        )
        query = parse_qs(urlparse(review_url()).query)
        decoded = json.loads(base64.b64decode(query["q"][0]))
        self.assertEqual(decoded, [QUESTION])
        self.assertEqual(query["ldap"], ["hshariati"])
        self.assertFalse(REPORT_ROOT.exists())


if __name__ == "__main__":
    unittest.main()
