import copy
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hp_comparison_study", HERE / "study.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


@pytest.fixture
def documents():
    full = study.load(study.BASELINE)
    singles = {("cashmere", "laptop_FrontCloseUp"), ("magic", "printer_FrontCloseUp")}
    rows = [row for row in full["prompts"]
            if row["bank_rank"] <= (1 if (row["device_id"], row["camera_tag"]) in singles else 2)]
    assert len(rows) == 30
    return full, {"prompts": copy.deepcopy(rows)}


def test_matched_selection_requires_unchanged_source_records(documents):
    full, selected = documents
    assert len(study.validate_matched(selected, full)) == 30
    selected["prompts"][0]["text"] += " changed"
    with pytest.raises(ValueError, match="differ"):
        study.validate_matched(selected, full)


def test_matched_selection_rejects_duplicate_or_missing_bank(documents):
    full, selected = documents
    selected["prompts"][-1] = selected["prompts"][0]
    with pytest.raises(ValueError, match="unique"):
        study.validate_matched(selected, full)


def test_legacy_shape_prototype_is_not_exact_pr4523():
    with pytest.raises(ValueError, match="PR/commit"):
        study.catalog_lineage("pr4523", "http://127.0.0.1:8137", {
            "rewriterVersion": "Adobe-Firefly/foundry#4349 / 8c358bc7989c + surface-shape-r1",
        })


def test_catalog_requires_pipeline_and_candidate_source_commit():
    version = f"Adobe-Firefly/foundry#4523 / {study.COMMITS['pr4523'][:12]} / {study.PIPELINES['pr4523']}"
    with pytest.raises(ValueError, match="source commit"):
        study.catalog_lineage("pr4523", "http://127.0.0.1:8138", {
            "rewriterVersion": version, "candidateLineage": {"sourceCommit": study.COMMITS["pr4417"]},
        })
    with pytest.raises(ValueError, match="expected pipeline"):
        study.catalog_lineage("pr4523", "http://127.0.0.1:8138", {
            "rewriterVersion": version.replace(study.PIPELINES["pr4523"], "other"),
        })


def test_generating_without_paid_authorization_never_reads_or_submits(monkeypatch):
    monkeypatch.setattr(study, "verified_manifest", lambda: pytest.fail("execution reached manifest"))
    with pytest.raises(PermissionError, match="paid"):
        study.generate(smoke=False, paid=False)


def test_full_queues_require_explicit_smoke_review(monkeypatch):
    monkeypatch.setattr(study, "verified_manifest", lambda: {"cells": []})
    with pytest.raises(PermissionError, match="smoke-reviewed"):
        study.generate(smoke=False, paid=True)
