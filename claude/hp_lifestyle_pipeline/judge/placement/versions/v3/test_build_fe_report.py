"""Regression tests for strict FE report provenance and verified envelopes."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import build_fe_report as builder


ROOT = Path(__file__).resolve().parent
VERIFIED_RUN = (
    ROOT
    / "experiments/verify_additions/verified_runs/verified-84-v3"
)
CONSENSUS_RUN = ROOT / "experiments/consensus_policy/runs/consensus-160-v2"
CONSENSUS_PROTOCOL = ROOT / "experiments/consensus_policy/protocol_snapshot_v2/manifest.json"
NEW160_MANIFEST = ROOT / "data/new_v6_1_eval_20261105/manifest.json"


def combined_84_manifest(tmp_path: Path) -> Path:
    records = []
    for name in ("diagnostic_cases.json", "extended_validation_cases_20261105.json"):
        records.extend(builder.load_json(ROOT / "data" / name)["records"])
    assert len(records) == len({record["id"] for record in records}) == 84
    path = tmp_path / "manifest.json"
    builder.atomic_json(path, {"expected_count": len(records), "records": records})
    return path


def record_for(record_id: str) -> dict:
    for name in ("diagnostic_cases.json", "extended_validation_cases_20261105.json"):
        for record in builder.load_json(ROOT / "data" / name)["records"]:
            if record["id"] == record_id:
                return record
    raise AssertionError(record_id)


def test_verified_v2_full_builder_and_fe_contract(tmp_path: Path) -> None:
    output = tmp_path / "report"
    summary = builder.build_reports(
        manifest_path=combined_84_manifest(tmp_path),
        results_dir=VERIFIED_RUN,
        protocol_path=ROOT / "experiments/two_pass/policy.json",
        output_root=output,
        title=builder.DEFAULT_TITLE,
        ldap="hshariati",
        expected_rows=84,
        publish_bucket=builder.DEFAULT_PUBLISH_BUCKET,
        publish_prefix=builder.DEFAULT_PUBLISH_PREFIX,
    )
    assert Path(summary["build_manifest"]).is_file()
    data = builder.load_json(output / "combined/data.json")
    assert data["meta_texts"][0] == (
        "HP natural-placement judge V3 — V6.1 GPT Image 2 scene evaluation"
    )
    assert data["meta_texts"][-1][1]["Question 1 — image"] == builder.QUESTION_WIRE[0]["text"]
    assert data["meta_texts"][-1][1]["Question 2 — judge"] == builder.QUESTION_WIRE[1]["text"]
    candidate = next(
        row for row in data["rows"]
        if row["meta_data"]["evalset_item_id"] == "cashmere__laptop_FrontCloseUp__p5"
    )
    details = candidate["meta_data"]["key_val_informations"]
    for key in (
        "Baseline V2 original assessment",
        "Compact V3 original assessment",
        "Verifier component assessment",
        "Verified compact assessment",
        "Verified selected source by component",
        "Final decision and overrides",
        "Verification uncertainty notes",
    ):
        assert details[key]
    assert candidate["images"][2]["meta_text"]["label"].startswith(
        "Verified research-candidate assessment"
    )
    build = builder.load_json(output / "build_manifest.json")
    assert build["validation"]["result_format"] == "application_derived_verified_overlay_v2"
    assert build["validation"]["verified_overlay_merge_score_and_final_override_recomputed"] is True
    assert build["validation"]["run_provenance"]["verified_merger_sha256"] == (
        "11594dccc74ba3ed5e986d0b32be7f531b63205186df7abb86b7ef5bed336922"
    )


def test_verified_v2_rejects_changed_final_override(tmp_path: Path) -> None:
    record_id = "cashmere__laptop_FrontCloseUp__p5"
    source = builder.load_json(VERIFIED_RUN / record_id / "result.json")
    tampered = copy.deepcopy(source)
    tampered["final_decision"]["verdict"] = "review"
    path = tmp_path / "result.json"
    builder.atomic_json(path, tampered)
    with pytest.raises(ValueError, match="final override policy is not deterministic"):
        builder.validate_verified_result(
            record_for(record_id),
            path,
            builder.load_json(ROOT / "experiments/two_pass/policy.json"),
        )


def consensus_validation_args() -> tuple:
    protocol = builder.load_json(CONSENSUS_PROTOCOL)
    policy, generator, _ = builder.consensus_protocol_context(protocol, CONSENSUS_PROTOCOL)
    trigger = builder.load_json(
        ROOT / "experiments/verify_additions_v6_1/triggers.json"
    )
    trigger_path = ROOT / "experiments/verify_additions_v6_1/triggers.json"
    trigger_map = {
        item["id"]: list(item["proposed_components"])
        for item in trigger["records"]
    }
    return (
        builder.load_json(ROOT / "experiments/two_pass/policy.json"),
        policy,
        generator,
        trigger_path,
        builder.sha256(trigger_path),
        trigger_map,
    )


def test_consensus_full_builder_and_fe_contract(tmp_path: Path) -> None:
    output = tmp_path / "consensus-report"
    summary = builder.build_reports(
        manifest_path=NEW160_MANIFEST,
        results_dir=CONSENSUS_RUN,
        protocol_path=CONSENSUS_PROTOCOL,
        output_root=output,
        title=builder.CONSENSUS_TITLE,
        ldap="hshariati",
        expected_rows=160,
        publish_bucket=builder.DEFAULT_PUBLISH_BUCKET,
        publish_prefix=builder.CONSENSUS_PUBLISH_PREFIX,
    )
    assert Path(summary["build_manifest"]).is_file()
    data = builder.load_json(output / "combined/data.json")
    assert data["meta_texts"][0] == builder.CONSENSUS_TITLE
    disagreement = next(
        row for row in data["rows"]
        if row["meta_data"]["evalset_item_id"]
        == "elitebook__laptop_BackRightCloseUp__p9"
    )
    details = disagreement["meta_data"]["key_val_informations"]
    for key in (
        "Proposal-aware verification check",
        "Names-only independent verification check",
        "Consensus disagreement note",
        "Consensus component resolution",
        "Consensus final decision",
    ):
        assert details[key]
    assert "rejected_confident_clear_or_minor" in details["Consensus disagreement note"]
    assert disagreement["images"][2]["meta_text"]["label"].startswith(
        "Consensus revision research-candidate assessment"
    )
    build = builder.load_json(output / "build_manifest.json")
    assert build["publish_destination"]["prefix"].endswith("/consensus_v2")
    assert build["validation"]["result_format"] == (
        "application_derived_two_check_consensus_v1"
    )
    assert build["validation"][
        "consensus_both_check_results_raw_responses_and_protocols_verified"
    ] is True
    assert build["validation"][
        "consensus_resolution_merge_score_and_final_decision_recomputed"
    ] is True


def test_consensus_rejects_changed_names_only_result(tmp_path: Path) -> None:
    record_id = "elitebook__laptop_BackRightCloseUp__p9"
    records = builder.load_json(NEW160_MANIFEST)["records"]
    record = next(item for item in records if item["id"] == record_id)
    source = builder.load_json(CONSENSUS_RUN / record_id / "result.json")
    tampered = copy.deepcopy(source)
    tampered["names_only_overlay"]["assessment"]["assessment"]["components"][
        "access_usability"
    ]["evidence"] += " changed"
    path = tmp_path / "result.json"
    builder.atomic_json(path, tampered)
    with pytest.raises(ValueError, match="embedded names-only result differs"):
        builder.validate_consensus_result(
            record,
            path,
            *consensus_validation_args(),
        )
