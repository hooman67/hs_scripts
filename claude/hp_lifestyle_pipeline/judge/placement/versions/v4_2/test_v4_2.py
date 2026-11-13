from __future__ import annotations

import copy
import json
import sys
import types
from pathlib import Path

import pytest
from PIL import Image

from anchor_selection import CATALOG_PATH, normalize_camera, select_anchors
from crop import create_support_crop
from scoring import PlacementValidationError, aggregate_assessment, validate_assessment, validate_runtime_input
# Unit tests do not need gateway credentials or a network client. Provide the
# import surface before loading the runner; the route test injects get_openai.
if "foundry_aws_gateway" not in sys.modules:
    fake_package = types.ModuleType("foundry_aws_gateway")
    fake_llm = types.ModuleType("foundry_aws_gateway.llm")
    fake_package.llm = fake_llm
    sys.modules["foundry_aws_gateway"] = fake_package
    sys.modules["foundry_aws_gateway.llm"] = fake_llm
import run_judge
from build_wire_schema import enum_value_count

ROOT = Path(__file__).resolve().parent
TRIGGER_OWNER_CODE = {
    "support_role": ("support_role", "inappropriate_support"),
    "room_use_zone": ("room_use_zone", "incoherent_use_zone"),
    "device_surface_position": ("device_surface_position", "unmotivated_device_position"),
    "props_use_relation": ("props_use_relation", "incoherent_prop_arrangement"),
    "operating_access": ("operating_access", "excessive_reach"),
    "user_position": ("user_position", "chair_displacement"),
    "device_support_axes": ("device_support_axes", "device_support_axis_conflict"),
    "furniture_room_axes": ("furniture_room_axes", "furniture_layout_conflict"),
    "product_scale": ("product_scale", "implausible_scale"),
    "support_load_path": ("support_anatomy", "missing_required_support"),
    "support_shape": ("support_anatomy", "malformed_support_furniture"),
    "shared_perspective": ("shared_perspective", "conflicting_perspective"),
    "support_contact": ("support_contact", "floating"),
    "shadows_reflections": ("shadows_reflections", "inconsistent_shadow"),
}
CHECKS = ["support_role", "room_use_zone", "device_surface_position", "props_use_relation", "operating_access", "user_position", "device_support_axes", "furniture_room_axes", "product_scale", "support_anatomy", "shared_perspective", "support_contact", "shadows_reflections"]


def region():
    return {"image": "generated_scene", "label": "visible scene area", "box": [0.1, 0.1, 0.8, 0.8]}


def fact():
    return {"visibility": "observed", "observation": "Visible relation is inspectable.", "regions": [region()], "visibility_limit": ""}


def clean_assessment():
    inv = {
        "scene_extent": "wide", "support_and_room_landmarks_visible": True,
        "support_type": fact(), "room_location": fact(), "product_footprint": fact(), "functional_front": fact(), "surface_position": fact(),
        "edge_families": {"longitudinal": fact(), "depth": fact()}, "visible_corners": fact(), "load_path": fact(),
        "room_relations": {"wall": fact(), "floor": fact(), "cabinets": fact(), "nearby_furniture": fact()},
        "operating_approach": fact(), "associated_chair_or_standing_position": fact(), "props_activity": fact(),
    }
    candidates, triggers = [], {}
    for i, (trigger_name, (owner, code)) in enumerate(TRIGGER_OWNER_CODE.items()):
        cid = f"tested_{i}"
        candidates.append({
            "id": cid, "physical_relation": f"distinct relation {i}", "hypothesis": f"Candidate defect {i}", "regions": [],
            "inventory_refs": ["support_type"], "trigger_ids": [trigger_name], "owner_check": owner, "issue_code": code,
            "disposition": "rejected", "disposition_evidence": "Visible evidence supports the benign condition.",
            "benign_alternative": "The observed arrangement is coherent.", "alternative_status": "remains_substantial",
            "severity": None, "confidence": "low", "warning_level": "none", "consequence": "", "missing_support_test": None,
        })
        triggers[trigger_name] = {"answer": "yes", "evidence": "Visible evidence establishes the condition.", "inventory_refs": ["support_type"], "candidate_ids": [cid], "visibility_limit": ""}
    checks = {name: {"visibility": "observed", "severity": 0, "confidence": "high", "warning_level": "none", "issue_codes": [], "evidence": "No visible defect retained.", "consequence": "", "alternative_explanation": "", "visibility_limit": "", "inventory_refs": ["support_type"], "candidate_ids": []} for name in CHECKS}
    return {"inventory": inv, "triggers": triggers, "defect_candidates": candidates, "stage_status": "assessed", "unable_reason": None,
            "functional_front": "Visible functional front.", "context_reading": "Coherent room context.", "checks": checks, "general_artifact_warnings": []}


def retain(a, trigger_name, *, issue=None, severity=2, confidence="high", warning="none"):
    owner, default_issue = TRIGGER_OWNER_CODE[trigger_name]
    cid = f"retained_{trigger_name}"
    c = {
        "id": cid, "physical_relation": f"retained relation {trigger_name}", "hypothesis": "Visible placement defect", "regions": [region()],
        "inventory_refs": ["support_type"], "trigger_ids": [trigger_name], "owner_check": owner, "issue_code": issue or default_issue,
        "disposition": "retained", "disposition_evidence": "Specific visible landmarks establish the defect.", "benign_alternative": "Benign interpretation tested.",
        "alternative_status": "excluded_by_visible_evidence" if confidence == "high" else "remains_substantial", "severity": severity, "confidence": confidence,
        "warning_level": warning, "consequence": "It impairs believable placement.", "missing_support_test": None,
    }
    if c["issue_code"] == "missing_required_support":
        c["missing_support_test"] = {"exposed_required_region": region(), "required_support_reason": "Visible span requires a load path.",
            "positive_break_or_unsupported_span_evidence": "Visible rail terminates before the exposed span.", "observed_alternate_load_paths": "One distant panel is visible.",
            "hidden_alternatives_and_limits": "No hidden connector can bridge the exposed break."}
    a["defect_candidates"].append(c)
    a["triggers"][trigger_name]["answer"] = "no"
    a["triggers"][trigger_name]["candidate_ids"].append(cid)
    check = a["checks"][owner]
    check["candidate_ids"].append(cid)
    check["issue_codes"] = sorted(set(check["issue_codes"] + [c["issue_code"]]))
    max_sev = max(x["severity"] for x in a["defect_candidates"] if x["id"] in check["candidate_ids"])
    check["severity"] = max_sev
    at_max = [x for x in a["defect_candidates"] if x["id"] in check["candidate_ids"] and x["severity"] == max_sev]
    check["confidence"] = max((x["confidence"] for x in at_max), key={"low": 0, "medium": 1, "high": 2}.get)
    check["warning_level"] = "review" if max_sev == 1 and any(x["warning_level"] == "review" for x in at_max) else "advisory" if max_sev == 1 else "none"
    check["consequence"] = "Retained candidate consequence."
    check["alternative_explanation"] = "Benign alternative evaluated."


def test_clean_pass():
    a = clean_assessment()
    validate_assessment(a)
    assert aggregate_assessment(a)["verdict"] == "pass"


def test_hidden_chair_low_coverage_can_pass():
    a = clean_assessment()
    a["inventory"]["associated_chair_or_standing_position"] = {"visibility": "unobservable", "observation": "Chair is outside crop.", "regions": [], "visibility_limit": "No associated chair is visible."}
    a["triggers"]["user_position"].update(answer="unknown", visibility_limit="No associated chair is visible.")
    a["checks"]["user_position"].update(visibility="unobservable", severity=None, confidence="low", visibility_limit="No associated chair is visible.")
    validate_assessment(a)
    assert aggregate_assessment(a)["verdict"] == "pass"


def test_unknown_trigger_does_not_lower_verdict():
    a = clean_assessment()
    a["triggers"]["operating_access"].update(answer="unknown", visibility_limit="Functional path is occluded.")
    validate_assessment(a)
    assert aggregate_assessment(a)["verdict"] == "pass"


def test_advisory_can_pass_and_review_warning_reviews():
    a = clean_assessment(); retain(a, "user_position", severity=1, confidence="high", warning="advisory")
    assert aggregate_assessment(a)["verdict"] == "pass"
    b = clean_assessment(); retain(b, "user_position", severity=1, confidence="high", warning="review")
    assert aggregate_assessment(b)["verdict"] == "review"


def test_high_confirmed_fails_despite_higher_low_confidence_same_check():
    a = clean_assessment()
    retain(a, "support_load_path", severity=2, confidence="high")
    retain(a, "support_shape", severity=4, confidence="low")
    validate_assessment(a)
    result = aggregate_assessment(a)
    assert result["verdict"] == "fail" and result["score"] <= 59


def test_no_trigger_requires_exactly_one_retained():
    a = clean_assessment(); a["triggers"]["support_role"]["answer"] = "no"
    with pytest.raises(PlacementValidationError): validate_assessment(a)


def _make_target(tmp_path: Path, name: str, color, prompt="unseen prompt"):
    scene, twin = tmp_path / f"{name}_scene.png", tmp_path / f"{name}_twin.png"
    Image.new("RGB", (64, 48), color).save(scene); Image.new("RGB", (64, 48), tuple(reversed(color))).save(twin)
    return {"generated_image": str(scene), "twin_image": str(twin), "product_type": "laptop", "scene_prompt": prompt}


def test_arbitrary_unseen_runtime_needs_no_record_id(tmp_path):
    target = _make_target(tmp_path, "new", (12, 34, 56))
    validate_runtime_input(target)
    selected, audit = select_anchors(target)
    assert len(selected) in {0, 4} and "target_record_id" not in target
    assert audit["union_target_count"] == 1


def test_exact_same_twin_and_prompt_excluded(tmp_path):
    catalog = json.loads(CATALOG_PATH.read_text())
    anchor = catalog["records"][0]
    target = {"generated_image": anchor["generated"]["source_path"], "twin_image": anchor["twin"]["source_path"], "product_type": anchor["product_type"], "scene_prompt": anchor["scene_prompt"]}
    _, audit = select_anchors(target, catalog=catalog)
    reasons = audit["excluded"][anchor["anchor_id"]]
    assert {"exact_generated_hash", "same_twin_hash", "exact_prompt_hash"}.issubset(reasons)


def test_optional_family_metadata_strengthens_exclusion(tmp_path):
    catalog = json.loads(CATALOG_PATH.read_text()); anchor = catalog["records"][0]
    target = _make_target(tmp_path, "meta", (2, 80, 120), "different prompt")
    target.update(product_type=anchor["product_type"], device=anchor["device"], camera=anchor["camera"], prompt_rank=anchor["prompt_rank"])
    _, audit = select_anchors(target, catalog=catalog)
    reasons = audit["excluded"][anchor["anchor_id"]]
    assert "same_product_camera_rank_family" in reasons and "same_device_camera_rank_family" in reasons


def test_anchor_exhaustion_is_valid(tmp_path):
    target = _make_target(tmp_path, "empty", (90, 40, 20))
    empty_catalog = {"records": []}
    selected, audit = select_anchors(target, catalog=empty_catalog)
    assert selected == [] and audit["depleted"] is True


def test_client_route_is_direct_foundry_gateway(monkeypatch):
    calls = {}
    class Dummy:
        def with_options(self, **kwargs):
            calls.update(kwargs)
            return self
    monkeypatch.setattr(run_judge.foundry_aws_gateway.llm, "get_openai", lambda: Dummy(), raising=False)
    instance, route = run_judge.client()
    assert isinstance(instance, Dummy)
    assert route == "foundry_direct_openai"
    assert calls == {"timeout": 600.0, "max_retries": 0}


def test_optional_target_metadata_is_not_sent_to_model(tmp_path):
    target = _make_target(tmp_path, "content", (44, 55, 66))
    target.update(target_record_id="secret_eval_record", device="secret_device", camera="secret_camera", prompt_rank="secret_rank")
    crop = Path(target["generated_image"])
    blocks = run_judge._content(target, crop, {"localization_status": "fallback_full_scene"}, [])
    text = "\n".join(str(block.get("text", "")) for block in blocks)
    assert "secret_eval_record" not in text and "secret_device" not in text and "secret_camera" not in text and "secret_rank" not in text


def test_union_target_exclusions_are_cumulative(tmp_path):
    catalog = json.loads(CATALOG_PATH.read_text())
    anchor = catalog["records"][0]
    target = _make_target(tmp_path, "primary", (10, 20, 30))
    exclusion = {"generated_image": anchor["generated"]["source_path"], "twin_image": anchor["twin"]["source_path"], "product_type": anchor["product_type"], "scene_prompt": anchor["scene_prompt"]}
    _, audit = select_anchors(target, catalog=catalog, exclusion_targets=[exclusion])
    assert anchor["anchor_id"] in audit["excluded"]


def test_six_case_union_has_no_anchor_leakage():
    catalog = json.loads(CATALOG_PATH.read_text())
    gate = json.loads((ROOT / "data" / "gate_6_manifest.json").read_text())
    targets = [r["runtime_input"] for r in gate["records"]]
    selected, _ = select_anchors(targets[0], catalog=catalog, exclusion_targets=targets)
    for anchor in selected:
        for target in targets:
            from anchor_selection import target_fingerprint
            fp = target_fingerprint(target)
            assert anchor["generated"]["byte_sha256"] != fp["generated_byte_sha256"]
            assert anchor["generated"]["pixel_sha256"] != fp["generated_pixel_sha256"]
            assert anchor["twin"]["byte_sha256"] != fp["twin_byte_sha256"]
            assert anchor["twin"]["pixel_sha256"] != fp["twin_pixel_sha256"]
            assert anchor["prompt_sha256"] != fp["prompt_sha256"]
            assert not (anchor["product_type"] == fp["product_type"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"])
            assert not (anchor["device"] == fp["device"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"])


def test_sift_failure_falls_back_to_full_scene(tmp_path):
    scene = tmp_path / "plain_scene.png"; twin = tmp_path / "plain_twin.png"
    Image.new("RGB", (128, 96), (120, 130, 140)).save(scene)
    Image.new("RGB", (128, 96), "white").save(twin)
    crop, provenance = create_support_crop(scene, twin, tmp_path / "crop")
    assert crop.is_file()
    assert provenance["localization_status"] == "fallback_full_scene"
    assert provenance["crop_box_full_scene_pixels"] == [0, 0, 128, 96]
    assert provenance["fallback_reason"]


def test_wire_schema_enum_count_below_api_limit():
    assert enum_value_count(run_judge.WIRE_SCHEMA) < 1000


def test_illegal_inventory_ref_and_candidate_id_fail_locally():
    a = clean_assessment()
    a["triggers"]["support_role"]["inventory_refs"] = ["not_a_real_inventory_ref"]
    with pytest.raises(PlacementValidationError):
        validate_assessment(a)
    b = clean_assessment()
    b["defect_candidates"][0]["id"] = "INVALID-ID!"
    with pytest.raises(PlacementValidationError):
        validate_assessment(b)


def test_wire_schema_obvious_openai_strict_requirements():
    failures = []
    def walk(value, path="$"):
        if isinstance(value, dict):
            if "const" in value and "type" not in value:
                failures.append(f"{path}: const lacks type")
            if value.get("type") == "object" or "properties" in value:
                props = value.get("properties", {})
                if value.get("additionalProperties") is not False:
                    failures.append(f"{path}: object lacks additionalProperties=false")
                if set(value.get("required", [])) != set(props):
                    failures.append(f"{path}: required does not equal properties")
            if value.get("type") == "array" and "items" not in value:
                failures.append(f"{path}: array lacks items")
            for key, child in value.items():
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")
    walk(run_judge.WIRE_SCHEMA)
    assert failures == []
