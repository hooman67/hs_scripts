from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import Draft202012Validator

import run_judge
from codebook import (
    ALL_TESTS,
    COHERENT_SUBTYPES,
    DEFECT_SUBTYPES,
    FUNCTIONAL_TESTS,
    GEOMETRY_TESTS,
)
from scoring import (
    PlacementValidationError,
    error_sentinel,
    synthesize,
    validate_functional,
    validate_geometry,
)

ROOT = Path(__file__).resolve().parent

def region(label="relation"):
    return {"label": label, "box": [0.1, 0.1, 0.8, 0.8]}

def relation(test_id, state="coherent", subtype=None):
    if subtype is None:
        subtype = min(COHERENT_SUBTYPES[test_id])
    return {
        "test_id": test_id, "observability": "visible", "state": state, "subtype": subtype,
        "direct_evidence": "The named visible relation was compared in the raw pixels.",
        "counterevidence": "Visible geometry supports this observation." if state == "coherent" else "",
        "visibility_limit": "none", "region": region(test_id) if state == "defect" else None,
    }

def clean_functional():
    return {
        "stage_status": "assessed", "unable_reason": None,
        "product_front": {"state": "observed", "region": region("product front"), "evidence": "The functional front is visible."},
        "visible_user_positions": [],
        "relations": [relation(test_id) for test_id in FUNCTIONAL_TESTS],
        "unrelated_artifacts": [],
    }

def clean_geometry():
    return {
        "stage_status": "assessed", "unable_reason": None,
        "support_inventory": {"visible_elements": [], "exposed_required_regions": [], "visible_breaks_or_negative_space": []},
        "edge_observations": [],
        "relations": [relation(test_id) for test_id in GEOMETRY_TESTS],
        "unrelated_artifacts": [],
    }

def set_defect(value, test_id, subtype):
    item = next(r for r in value["relations"] if r["test_id"] == test_id)
    item.update(state="defect", subtype=subtype, region=region(test_id), counterevidence="")
    return item

def add_edge(value, owner):
    value["edge_observations"].append({"owner": owner, "p0": [0.1, 0.2], "p1": [0.8, 0.3], "raw_pixel_evidence": f"Visible {owner} edge."})

def test_strict_test_sets_and_order_validate():
    assert validate_functional(clean_functional())["stage_status"] == "assessed"
    assert validate_geometry(clean_geometry())["stage_status"] == "assessed"
    bad = clean_functional(); bad["relations"].reverse()
    with pytest.raises(PlacementValidationError, match="prescribed order"):
        validate_functional(bad)

def test_state_observability_subtype_and_region_polarity():
    bad = clean_functional(); item = bad["relations"][0]; item.update(state="defect", subtype="occupied_personal_workstation", region=None)
    with pytest.raises(PlacementValidationError, match="positive-area"):
        validate_functional(bad)
    bad = clean_functional(); item = bad["relations"][0]; item.update(state="unresolved", subtype="unresolved", observability="visible")
    with pytest.raises(PlacementValidationError, match="hidden or partial"):
        validate_functional(bad)
    bad = clean_functional(); item = bad["relations"][0]; item.update(state="coherent", subtype="occupied_personal_workstation")
    with pytest.raises(PlacementValidationError, match="state=coherent"):
        validate_functional(bad)

def test_exact_gate_failure_is_rejected_by_local_and_wire_schemas_with_choices():
    bad = clean_functional()
    operating = next(item for item in bad["relations"] if item["test_id"] == "operating_access")
    operating["subtype"] = "coherent_axes"
    local_schema = json.loads((ROOT / "functional_observer_schema.json").read_text())
    wire_schema = json.loads((ROOT / "functional_observer_wire_schema.json").read_text())
    assert list(Draft202012Validator(local_schema).iter_errors(bad))
    assert list(Draft202012Validator(wire_schema).iter_errors(bad))
    with pytest.raises(PlacementValidationError) as caught:
        validate_functional(bad)
    message = str(caught.value)
    assert "operating_access state=coherent" in message
    assert "subtype='coherent_axes'" in message
    assert "allowed=['open']" in message

def test_every_relation_schema_branch_pairs_test_state_and_own_subtypes():
    functional_schema = json.loads((ROOT / "functional_observer_wire_schema.json").read_text())
    geometry_schema = json.loads((ROOT / "geometry_observer_wire_schema.json").read_text())
    for schema, tests in ((functional_schema, FUNCTIONAL_TESTS), (geometry_schema, GEOMETRY_TESTS)):
        item_schema = schema["properties"]["relations"]["anyOf"][0]["items"]
        branches = item_schema["anyOf"]
        assert len(branches) == 3 * len(tests)
        seen = set()
        for branch in branches:
            props = branch["properties"]
            test_id, state = props["test_id"]["enum"][0], props["state"]["enum"][0]
            seen.add((test_id, state))
            if state == "coherent":
                assert set(props["subtype"]["enum"]) == COHERENT_SUBTYPES[test_id]
            elif state == "defect":
                assert set(props["subtype"]["enum"]) == DEFECT_SUBTYPES[test_id]
            else:
                assert props["subtype"]["enum"] == ["unresolved"]
        assert seen == {(test_id, state) for test_id in tests for state in ("coherent", "defect", "unresolved")}

def test_functional_application_owned_mapping_and_severity():
    expected = {
        ("user_position", "chair_offset"): ("chair_displacement", 1, "review"),
        ("support_room_placement", "central_rectangular_home_printer_support_without_shared_use"): ("misplaced_support_furniture", 2, "fail"),
    }
    for (test_id, subtype), (code, severity, verdict) in expected.items():
        functional, geometry = clean_functional(), clean_geometry()
        set_defect(functional, test_id, subtype)
        result = synthesize(functional, geometry, "printer" if "home_printer" in subtype else "laptop")
        assert result["verdict"] == verdict
        issue = result["confirmed_issues"][0]
        assert (issue["issue_code"], issue["severity"]) == (code, severity)

@pytest.mark.parametrize("test_id,subtype,code", [
    ("load_path", "visible_missing_support", "missing_required_support"),
    ("support_anatomy", "malformed_connected_furniture", "malformed_support_furniture"),
    ("device_support_axes", "visible_axis_conflict", "device_support_axis_conflict"),
    ("shared_perspective", "incompatible_geometry_or_depth", "conflicting_perspective"),
])
def test_required_geometry_families_are_severity_two(test_id, subtype, code):
    functional, geometry = clean_functional(), clean_geometry()
    set_defect(geometry, test_id, subtype)
    if test_id == "load_path":
        geometry["support_inventory"]["exposed_required_regions"].append({"region": region(), "connected_support_visible": False})
        geometry["support_inventory"]["visible_breaks_or_negative_space"].append({"region": region(), "kind": "unsupported_span"})
    if test_id == "support_anatomy":
        geometry["support_inventory"]["visible_breaks_or_negative_space"].append({"region": region(), "kind": "impossible_junction"})
    if test_id == "device_support_axes":
        add_edge(geometry, "product_front"); add_edge(geometry, "support_front")
    if test_id == "shared_perspective":
        add_edge(geometry, "support_front"); add_edge(geometry, "wall")
    result = synthesize(functional, geometry, "printer")
    assert result["verdict"] == "fail" and result["score"] <= 59
    assert result["confirmed_issues"][0]["issue_code"] == code
    assert result["confirmed_issues"][0]["severity"] == 2

def test_geometry_structured_fact_requirements_reject_unsupported_conclusions():
    geometry = clean_geometry(); set_defect(geometry, "load_path", "visible_missing_support")
    with pytest.raises(PlacementValidationError, match="exposed region"):
        validate_geometry(geometry)
    geometry = clean_geometry(); set_defect(geometry, "device_support_axes", "visible_axis_conflict")
    with pytest.raises(PlacementValidationError, match="named product and support edges"):
        validate_geometry(geometry)

def test_unrelated_artifacts_are_zero_penalty_and_clean_stays_pass():
    functional, geometry = clean_functional(), clean_geometry()
    functional["unrelated_artifacts"] = [{"region": region("glasses"), "evidence": "Unrelated glasses are malformed."}]
    result = synthesize(functional, geometry, "laptop")
    assert result["verdict"] == "pass" and result["score"] == 100
    assert result["owned_issue_codes"] == [] and len(result["warnings"]) == 1

def test_frozen_penalty_groups_charge_one_physical_domain_once():
    functional, geometry = clean_functional(), clean_geometry()
    set_defect(geometry, "load_path", "visible_missing_support")
    set_defect(geometry, "support_anatomy", "malformed_connected_furniture")
    geometry["support_inventory"]["exposed_required_regions"].append({"region": region(), "connected_support_visible": False})
    geometry["support_inventory"]["visible_breaks_or_negative_space"].append({"region": region(), "kind": "unsupported_span"})
    result = synthesize(functional, geometry, "printer")
    assert result["penalty_causes"]["structure_contact"]["penalty"] == 40
    assert result["score"] == 59  # material-defect verdict cap

def test_unable_and_all_unresolved_are_review_sentinels():
    functional = clean_functional(); functional.update(stage_status="unable", unable_reason="unreadable_image", product_front=None, visible_user_positions=None, relations=None)
    result = synthesize(functional, clean_geometry(), "printer")
    assert result["verdict"] == "review" and not result["score_valid"]
    functional, geometry = clean_functional(), clean_geometry()
    for value in (functional, geometry):
        for item in value["relations"]:
            item.update(state="unresolved", subtype="unresolved", observability="hidden", region=None, visibility_limit="cropped")
    result = synthesize(functional, geometry, "printer")
    assert result["reason"] == "all_relations_unobservable" and not result["score_valid"]

class FakeAPI:
    def __init__(self, outputs):
        self.outputs = list(outputs); self.calls = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
    def create(self, **kwargs):
        self.calls.append(kwargs)
        output = self.outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        finish, refusal = "stop", None
        if isinstance(output, tuple):
            output, finish, refusal = output
        usage = SimpleNamespace(prompt_tokens=100, completion_tokens=50, total_tokens=150, completion_tokens_details=SimpleNamespace(reasoning_tokens=10))
        return SimpleNamespace(id=f"resp-{len(self.calls)}", model="gpt-5.5-2026-04-23", usage=usage, choices=[SimpleNamespace(finish_reason=finish, message=SimpleNamespace(content=json.dumps(output), refusal=refusal))])

def make_runtime(tmp_path):
    from PIL import Image
    scene = tmp_path / "scene.png"; twin = tmp_path / "twin.png"
    Image.new("RGB", (32, 32), "white").save(scene); Image.new("RGB", (32, 32), "grey").save(twin)
    return {"generated_image": str(scene), "twin_image": str(twin), "product_type": "laptop", "scene_prompt": "SECRET NARRATIVE", "target_record_id": "SECRET-ID", "expected": "SECRET-LABEL"}

def patch_runtime(monkeypatch, api):
    monkeypatch.setattr(run_judge, "client", lambda: (api, "test"))
    monkeypatch.setattr(run_judge, "create_support_crop", lambda scene, twin, out: (Path(scene), {"localization_status": "fallback", "crop_box_full_scene_pixels": [0, 0, 32, 32]}))
    monkeypatch.setattr(run_judge, "create_furniture_room_crop", lambda scene, crop, out: (Path(scene), {"crop_box_full_scene_pixels": [0, 0, 32, 32], "unwarped": True}))
    monkeypatch.setattr(run_judge, "create_geometry_overlay", lambda scene, crop, prov, out: (Path(scene), {"selected_segment_count": 0, "scope_notice": "aid"}))

def test_runtime_two_independent_calls_and_no_scene_prompt_or_label_leakage(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path); api = FakeAPI([clean_functional(), clean_geometry()]); patch_runtime(monkeypatch, api)
    result = run_judge.judge(runtime, tmp_path / "run")
    assert result["status"] == "ok" and len(api.calls) == 2
    serialized = json.dumps(api.calls)
    for secret in ("SECRET NARRATIVE", "SECRET-ID", "SECRET-LABEL"):
        assert secret not in serialized
    first, second = api.calls
    assert "PRODUCT_SUPPORT_CROP" not in json.dumps(first) and "FURNITURE_ROOM_CROP" not in json.dumps(first)
    assert "PRODUCT_SUPPORT_CROP" in json.dumps(second) and "FURNITURE_ROOM_CROP" in json.dumps(second)
    assert json.dumps(clean_functional()) not in json.dumps(second)

def test_global_single_repair_and_three_call_cap(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path); api = FakeAPI([{}, clean_functional(), clean_geometry()]); patch_runtime(monkeypatch, api)
    result = run_judge.judge(runtime, tmp_path / "run")
    assert result["status"] == "ok" and len(api.calls) == 3
    api2 = FakeAPI([{}, clean_functional(), {}]); patch_runtime(monkeypatch, api2)
    failed = run_judge.judge(runtime, tmp_path / "run2")
    assert failed["status"] == "error" and len(api2.calls) == 3
    assert failed["derived"]["verdict"] == "review" and not failed["derived"]["score_valid"]

def test_repeated_exact_coherent_axes_failure_consumes_one_repair_then_fails_closed(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path)
    bad = clean_functional()
    next(item for item in bad["relations"] if item["test_id"] == "operating_access")["subtype"] = "coherent_axes"
    api = FakeAPI([bad, bad])
    patch_runtime(monkeypatch, api)
    result = run_judge.judge(runtime, tmp_path / "run")
    assert result["status"] == "error" and not result["derived"]["score_valid"]
    assert len(api.calls) == 2
    assert [call["status"] for call in result["raw_calls"]] == ["invalid", "invalid"]
    assert all("allowed=['open']" in " ".join(call["errors"]) for call in result["raw_calls"])

def test_transport_failure_uses_same_shared_repair_budget(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path); api = FakeAPI([RuntimeError("temporary"), clean_functional(), clean_geometry()]); patch_runtime(monkeypatch, api)
    result = run_judge.judge(runtime, tmp_path / "run")
    assert result["status"] == "ok" and len(api.calls) == 3 and result["raw_calls"][0]["status"] == "transport_error"

def test_cache_hash_binding_and_irrelevant_scene_prompt_does_not_invalidate(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path); api = FakeAPI([clean_functional(), clean_geometry()]); patch_runtime(monkeypatch, api)
    out = tmp_path / "run"; first = run_judge.judge(runtime, out)
    changed_prompt = dict(runtime, scene_prompt="DIFFERENT SECRET")
    assert run_judge.judge(changed_prompt, out)["audit"]["derived_sha256"] == first["audit"]["derived_sha256"]
    from PIL import Image
    Image.new("RGB", (32, 32), "black").save(runtime["generated_image"])
    with pytest.raises(PlacementValidationError, match="stale cache refused"):
        run_judge.judge(runtime, out)

def test_audit_ids_tokens_model_hashes_and_error_contract(tmp_path, monkeypatch):
    runtime = make_runtime(tmp_path); api = FakeAPI([clean_functional(), clean_geometry()]); patch_runtime(monkeypatch, api)
    result = run_judge.judge(runtime, tmp_path / "run")
    for call in result["raw_calls"]:
        assert call["response_id"] and call["latency_ms"] is not None and call["prompt_tokens"] == 100 and call["completion_tokens"] == 50
    assert result["audit"]["model_returned"] == ["gpt-5.5-2026-04-23"]
    for key in ("system_prompt_sha256", "schema_sha256", "geometry_algorithms_sha256", "synthesis_sha256", "taxonomy_sha256", "runtime_environment_sha256", "runner_sha256", "derived_sha256"):
        assert result["audit"][key]
    sentinel = error_sentinel("boom")
    assert sentinel["reason"] == "execution_error" and sentinel["verdict"] == "review" and not sentinel["score_valid"]

def test_protocol_source_guards():
    source = (ROOT / "run_judge.py").read_text()
    assert 'model: str = "gpt-5.5"' in source and 'reasoning_effort="high"' in source
    assert "max_retries=0" in source and "maximum_model_calls\": 3" in source
    assert run_judge.PROTOCOL_VERSION == "hp-natural-placement-v4.5.2-independent-observers-v1"
    assert (ROOT / "functional_observer_system.md").read_text().startswith("You are HP Natural Placement Functional")
    assert (ROOT / "geometry_observer_system.md").read_text().startswith("You are HP Natural Placement Geometry")
    assert len(ALL_TESTS) == 14

def test_gate_manifest_has_no_scene_prompts_labels_or_extra_runtime_keys():
    manifest = json.loads((ROOT / "data/dev_6_manifest.json").read_text())
    assert len(manifest["records"]) == 6
    for row in manifest["records"]:
        assert set(row["runtime_input"]) == {"generated_image", "twin_image", "product_type"}
    serialized = json.dumps(manifest).lower()
    assert "expected_verdict" not in serialized and "scene_prompt\"" not in serialized

def test_gate_runner_is_three_repeat_frozen_fail_closed_and_not_launched():
    source = (ROOT / "run_dev_gate.py").read_text()
    assert "range(1,4)" in source and "verify_freeze()" in source
    assert "verify_environment()" in source
    assert "frozen_hashes" in source and "input:{row['record_id']}" in source
    assert "result['status']!='ok' or not result['derived']['score_valid']" in source
    assert not (ROOT / "runs/dev_6_gate_a_v4_5_2_gpt55/progress.json").exists()

def test_product_crop_is_strictly_smaller_than_room_crop_without_gate_preflight(tmp_path):
    from PIL import Image, ImageDraw

    from geometry import create_furniture_room_crop, create_support_crop

    scene = Image.new("RGB", (96, 72), "white")
    twin = Image.new("RGB", (96, 72), "white")
    ImageDraw.Draw(scene).rectangle((30, 25, 65, 50), fill="navy")
    ImageDraw.Draw(twin).rectangle((30, 25, 65, 50), fill="navy")
    scene_path, twin_path = tmp_path / "scene.png", tmp_path / "twin.png"
    scene.save(scene_path); twin.save(twin_path)
    product_path, _ = create_support_crop(scene_path, twin_path, tmp_path)
    room_path, _ = create_furniture_room_crop(scene_path, product_path, tmp_path)
    product, room = Image.open(product_path), Image.open(room_path)
    assert product.width <= room.width and product.height <= room.height
    assert product.width * product.height < room.width * room.height
