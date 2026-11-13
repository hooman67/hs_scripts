from __future__ import annotations

import copy

import pytest

import image_study
import report
import text_study


def fixture_document():
    original = text_study.load(text_study.ROOT / "baseline/outputs/all_160/prompts_all_160.json")
    return {
        "prompts": copy.deepcopy(original["prompts"]),
        "bank_audit": {bank: {"result": {"status": "ok"}} for bank in original["bank_audit"]},
    }


def test_failed_writer_bank_is_never_in_the_image_queue(monkeypatch):
    document = fixture_document()
    failed = document["prompts"][-1]["bank_debug_ref"]
    document["prompts"] = [prompt for prompt in document["prompts"] if prompt["bank_debug_ref"] != failed]
    document["bank_audit"][failed]["result"]["status"] = "error"
    original_load = image_study.load
    monkeypatch.setattr(
        image_study, "load", lambda path: document if path == image_study.SOURCE else original_load(path)
    )
    rows = image_study.rows()
    assert len(rows) == 150
    assert all(row["bank_id"] != failed for row in rows)
    assert [row["queue_position"] for row in rows] == list(range(1, 151))
    queue = image_study.accepted_queue(rows)
    assert queue["expected_count"] == 150 and queue["planned_count"] == 160
    assert len(queue["rows"]) == 150


def test_partial_nine_prompt_bank_is_rejected(monkeypatch):
    document = fixture_document()
    document["prompts"].pop()
    original_load = image_study.load
    monkeypatch.setattr(
        image_study, "load", lambda path: document if path == image_study.SOURCE else original_load(path)
    )
    with pytest.raises(ValueError, match="complete ten-prompt banks"):
        image_study.rows()


def test_lineage_matches_the_actual_frozen_image_baseline(monkeypatch):
    document = fixture_document()
    original_load = image_study.load
    monkeypatch.setattr(
        image_study, "load", lambda path: document if path == image_study.SOURCE else original_load(path)
    )
    catalog = original_load(image_study.PRIOR / "run/catalog.json")
    lineage = image_study.lineage(catalog)
    assert lineage["source_commit"] == image_study.COMMIT
    assert lineage["endpoint_base_url"] == image_study.BASE_URL


def test_gallery_rejects_credential_urls_and_foreign_buckets():
    with pytest.raises(ValueError, match="credentials/query"):
        report.relative(report.GATEWAY + "example.png?token=unsafe")
    with pytest.raises(ValueError, match="HP asset"):
        report.relative("https://foundry-aws-corp.adobe.io/asset/another-bucket/example.png")
