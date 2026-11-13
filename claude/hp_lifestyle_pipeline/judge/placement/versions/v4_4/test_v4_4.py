from __future__ import annotations
import json, sys, types
from pathlib import Path
from types import SimpleNamespace
import pytest
if "foundry_aws_gateway" not in sys.modules:
    package=types.ModuleType("foundry_aws_gateway"); llm=types.ModuleType("foundry_aws_gateway.llm"); package.llm=llm
    sys.modules["foundry_aws_gateway"]=package; sys.modules["foundry_aws_gateway.llm"]=llm
import run_judge
from codebook import DEFECT_SUBTYPES, TEST_ISSUES, issue_for
from scoring import PlacementValidationError, defect_proposals, error_sentinel, reconcile, validate_scout, validate_verifier
ROOT=Path(__file__).resolve().parent
def region(box=None): return {"label":"visible relation","box":box or [0.1,0.1,0.9,0.9]}
def clean_scout():
    tests=[{"test_id":test_id,"defect":"no","severity":0,"visible_test":"Compared the visible relation in raw pixels.","direct_evidence":"Visible geometry is coherent.","counterevidence":"","visibility_limit":"","region":region()} for test_id in TEST_ISSUES]
    return {"stage_status":"assessed","unable_reason":None,"inventory":{"scene_extent":"wide","product_front_and_footprint":"Visible product front and footprint.","support_type_and_room_location":"Visible support beside a wall.","support_topology_and_edges":"Visible coherent support edges.","visible_load_path":"Visible connected load path.","furniture_wall_floor_perspective":"Visible coherent depth.","operating_and_user_approach":"Visible open approach.","props_and_activity_zone":"Visible coherent activity.","contact_scale_shadows":"Visible coherent contact and scale.","support_role_class":"compatible_support","support_room_class":"coherent","operating_access_class":"open","user_position_class":"coherent","support_contact_class":"supported","light_transport_class":"coherent"},"tests":tests,"general_artifact_warnings":[]}
def set_defect(scout,test_id,severity,box=None):
    test=next(t for t in scout["tests"] if t["test_id"]==test_id); test.update(defect="yes",severity=severity,direct_evidence="Direct visible defect.",region=region(box)); return test
def verifier_for(proposals,decision="confirmed",severity=2,observability="visible",subtypes=None):
    subtypes=subtypes or {}
    def subtype(test_id):
        if decision!="confirmed" or test_id not in DEFECT_SUBTYPES: return "not_applicable"
        return subtypes.get(test_id,next(iter(DEFECT_SUBTYPES[test_id])))
    return {"stage_status":"verified","unable_reason":None,"results":[{"test_id":p["test_id"],"decision":decision,"severity":severity if decision=="confirmed" else 0,"observability":observability,"observed_subtype":subtype(p["test_id"]),"direct_evidence":"Independent raw-pixel witness.","counterevidence":"","visibility_limit":"hidden relation" if observability=="hidden" else "","region":p["region"] if decision=="confirmed" else None} for p in proposals]}
def empty_verifier(): return {"stage_status":"verified","unable_reason":None,"results":[]}
def test_clean_and_partly_unobservable_can_pass():
    scout=clean_scout(); scout["inventory"]["user_position_class"]="unresolved"; next(t for t in scout["tests"] if t["test_id"]=="user_position").update(defect="unknown",visibility_limit="Chair is outside crop.",region=None)
    result=reconcile(scout,empty_verifier()); assert result["verdict"]=="pass" and result["score"]==100
def test_all_unknown_is_unassessable_review():
    scout=clean_scout()
    for test in scout["tests"]: test.update(defect="unknown",severity=0,visibility_limit="Relation is hidden.",region=None)
    for field in ("support_role_class","support_room_class","operating_access_class","user_position_class","support_contact_class","light_transport_class"): scout["inventory"][field]="unresolved"
    result=reconcile(scout,empty_verifier()); assert not result["score_valid"] and result["score"]==0 and result["verdict"]=="review"
def test_every_positive_including_severity_one_requires_verifier():
    scout=clean_scout(); scout["inventory"]["user_position_class"]="chair_displacement"; set_defect(scout,"user_position",1)
    proposals=defect_proposals(scout); assert len(proposals)==1
    with pytest.raises(PlacementValidationError): reconcile(scout,None)
    result=reconcile(scout,verifier_for(proposals,severity=1)); assert result["verdict"]=="review" and result["score"]==88
def test_confirmed_material_defect_fails_and_code_is_derived():
    scout=clean_scout(); set_defect(scout,"support_anatomy",2); result=reconcile(scout,verifier_for(defect_proposals(scout)))
    assert result["verdict"]=="fail" and result["owned_issue_codes"]==[issue_for("support_anatomy",scout["inventory"])]
def test_rejected_hidden_claim_reconciles_to_unobservable():
    scout=clean_scout(); set_defect(scout,"load_path",3); result=reconcile(scout,verifier_for(defect_proposals(scout),"rejected",0,"hidden"))
    assert result["verdict"]=="pass" and result["checks"]["load_path"]["state"]=="unobservable"
def test_verifier_hidden_observability_invariants():
    scout=clean_scout(); set_defect(scout,"load_path",2); proposals=defect_proposals(scout)
    uncertain=verifier_for(proposals,"uncertain",0,"hidden")
    with pytest.raises(PlacementValidationError,match="uncertain requires visible or partial"): validate_verifier(uncertain,proposals)
    rejected=verifier_for(proposals,"rejected",0,"hidden"); rejected["results"][0]["visibility_limit"]=""
    with pytest.raises(PlacementValidationError,match="hidden requires visibility_limit"): validate_verifier(rejected,proposals)
def test_uncertain_visible_proposal_reviews():
    scout=clean_scout(); set_defect(scout,"shared_perspective",2); result=reconcile(scout,verifier_for(defect_proposals(scout),"uncertain",0,"partial"))
    assert result["verdict"]=="review" and not result["owned_issue_codes"]
def test_static_penalty_groups_dedupe_related_geometry_but_not_unrelated_domains():
    scout=clean_scout(); set_defect(scout,"furniture_room_axes",2); set_defect(scout,"shared_perspective",3); result=reconcile(scout,verifier_for(defect_proposals(scout),severity=2))
    assert result["penalty_causes"]["orientation_perspective"]["penalty"]==40
    assert set(result["penalty_causes"]["orientation_perspective"]["confirmed_tests"])=={"furniture_room_axes","shared_perspective"}
    scout2=clean_scout(); scout2["inventory"].update(user_position_class="chair_displacement",light_transport_class="inconsistent_shadow"); set_defect(scout2,"user_position",2); set_defect(scout2,"shadows_reflections",2); result2=reconcile(scout2,verifier_for(defect_proposals(scout2)))
    assert result2["penalty_causes"]["operating_use"]["penalty"]==40 and result2["penalty_causes"]["light_transport"]["penalty"]==40
def test_narrow_issue_subtypes_are_deterministically_derived_from_inventory():
    scout=clean_scout(); scout["inventory"].update(support_role_class="occupied_personal_workstation",user_position_class="no_feasible_user_position",operating_access_class="excessive_reach")
    set_defect(scout,"support_role",2); set_defect(scout,"user_position",2); set_defect(scout,"operating_access",2)
    proposals=defect_proposals(scout); result=reconcile(scout,verifier_for(proposals,subtypes={"support_role":"occupied_personal_workstation","operating_access":"excessive_reach","user_position":"no_feasible_user_position"}))
    codes={item["test_id"]:item["issue_code"] for item in result["confirmed_issues"]}
    assert codes=={"support_role":"occupied_workstation","operating_access":"excessive_reach","user_position":"no_feasible_user_position"}
def test_invalid_scout_and_verifier_semantics_fail_locally():
    scout=clean_scout(); set_defect(scout,"load_path",2)["region"]=None
    with pytest.raises(PlacementValidationError): validate_scout(scout)
    scout=clean_scout(); set_defect(scout,"load_path",2); proposals=defect_proposals(scout); verifier=verifier_for(proposals); verifier["results"][0]["test_id"]="product_scale"
    with pytest.raises(PlacementValidationError): validate_verifier(verifier,proposals)
    subtype=clean_scout(); set_defect(subtype,"user_position",1)
    with pytest.raises(PlacementValidationError,match="defect subtype"): validate_scout(subtype)
@pytest.mark.parametrize("test_id,field,bad",[
    ("support_role","support_role_class","occupied_personal_workstation"),("support_room_placement","support_room_class","misplaced_furniture"),("operating_access","operating_access_class","blocked"),("user_position","user_position_class","chair_displacement"),("support_contact","support_contact_class","floating"),("shadows_reflections","light_transport_class","inconsistent_shadow")])
def test_no_subtype_polarity_is_consistent(test_id,field,bad):
    scout=clean_scout(); scout["inventory"][field]=bad
    with pytest.raises(PlacementValidationError,match="no requires"): validate_scout(scout)
    unknown=clean_scout(); next(t for t in unknown["tests"] if t["test_id"]==test_id).update(defect="unknown",visibility_limit="Hidden.",region=None)
    with pytest.raises(PlacementValidationError,match="unknown requires"): validate_scout(unknown)
def test_prompt_regressions():
    scout=(ROOT/"scout_system_prompt.md").read_text(); verifier=(ROOT/"verifier_system_prompt.md").read_text()
    assert "defect detection, not justification" in scout and "absence of visible functional justification prevents an invented benign rescue" in scout
    assert "Absence of justification alone is never positive evidence" in scout and "Never invent a second off-frame centered chair" in scout
    assert "every supplied SCOUT_DEFECT_PROPOSAL, including severity 1" in verifier and "Missing justification alone is not evidence" in verifier
def test_fresh_ten_is_frozen_historical_development_and_leak_free():
    manifest=json.loads((ROOT/"data/fresh_10_manifest.json").read_text()); freeze=json.loads((ROOT/"data/fresh_10_selection_freeze.json").read_text())
    gate={r["record_id"] for r in json.loads((ROOT.parent/"v4_3_1/data/gate_6_manifest.json").read_text())["records"]}; anchors={r["source_record_id"] for r in json.loads((ROOT.parent/"v4_3_1/anchors/anchor_catalog.json").read_text())["records"]}; ids={r["record_id"] for r in manifest["records"]}
    assert len(ids)==10 and not ids&gate and not ids&anchors and freeze["record_ids"]==[r["record_id"] for r in manifest["records"]]
def test_wire_schemas_bounded_and_compact():
    scout=json.loads((ROOT/"scout_wire_schema.json").read_text()); verifier=json.loads((ROOT/"verifier_wire_schema.json").read_text())
    assert (ROOT/"scout_wire_schema.json").stat().st_size<10000 and (ROOT/"verifier_wire_schema.json").stat().st_size<10000
    assert '"maxLength"' in json.dumps(scout) and '"maxLength"' in json.dumps(verifier)
class FakeAPI:
    def __init__(self,outputs): self.outputs=list(outputs); self.calls=[]; self.chat=SimpleNamespace(completions=SimpleNamespace(create=self.create))
    def create(self,**kwargs):
        self.calls.append(kwargs); output=self.outputs.pop(0)
        if isinstance(output,Exception): raise output
        finish="stop"; refusal=None
        if isinstance(output,tuple): output,finish,refusal=output
        usage=SimpleNamespace(prompt_tokens=100,completion_tokens=50,total_tokens=150,completion_tokens_details=SimpleNamespace(reasoning_tokens=10))
        return SimpleNamespace(id=f"resp-{len(self.calls)}",model="gpt-5.5-2026-04-23",usage=usage,choices=[SimpleNamespace(finish_reason=finish,message=SimpleNamespace(content=json.dumps(output),refusal=refusal))])
def make_runtime(tmp_path):
    from PIL import Image
    scene=tmp_path/"scene.png"; twin=tmp_path/"twin.png"; Image.new("RGB",(32,32),"white").save(scene); Image.new("RGB",(32,32),"grey").save(twin)
    return {"generated_image":str(scene),"twin_image":str(twin),"product_type":"laptop","scene_prompt":"ordinary scene","target_record_id":"secret-id","camera":"secret-camera","prompt_rank":"secret-rank"}
def patch_runtime(monkeypatch,api):
    monkeypatch.setattr(run_judge,"client",lambda:(api,"test")); monkeypatch.setattr(run_judge,"create_support_crop",lambda scene,twin,out:(Path(scene),{"localization_status":"fallback"})); monkeypatch.setattr(run_judge,"create_geometry_overlay",lambda scene,crop,prov,out:(Path(scene),{"selected_segment_count":0,"scope_notice":"aid"}))
def test_full_runtime_always_two_pass_empty_and_no_leakage(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); api=FakeAPI([clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,api)
    original=Path.read_text
    def guarded(self,*args,**kwargs):
        assert "expectations" not in self.name.lower(); return original(self,*args,**kwargs)
    monkeypatch.setattr(Path,"read_text",guarded)
    result=run_judge.judge(runtime,tmp_path/"run")
    assert result["status"]=="ok" and len(api.calls)==2 and result["derived"]["verdict"]=="pass"
    payload=json.dumps(api.calls); assert "secret-id" not in payload and "secret-camera" not in payload and "secret-rank" not in payload and "expectations" not in payload
    assert api.calls[1]["messages"][-1]["content"][-1]["text"].endswith("[]")
def test_one_global_repair_caps_total_at_three(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); api=FakeAPI([{},clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,api)
    result=run_judge.judge(runtime,tmp_path/"run"); assert result["status"]=="ok" and len(api.calls)==3
    api2=FakeAPI([{},{}]); patch_runtime(monkeypatch,api2); failed=run_judge.judge(runtime,tmp_path/"run2")
    assert failed["status"]=="error" and len(api2.calls)==2 and failed["derived"]["score"]==0 and failed["derived"]["verdict"]=="review"
def test_truncation_and_refusal_are_technical_failures_within_shared_budget(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); truncated=FakeAPI([(clean_scout(),"length",None),clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,truncated)
    result=run_judge.judge(runtime,tmp_path/"truncated"); assert result["status"]=="ok" and len(truncated.calls)==3 and result["raw_calls"][0]["status"]=="transport_error"
    refused=FakeAPI([(clean_scout(),"stop","refused"),clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,refused)
    result2=run_judge.judge(runtime,tmp_path/"refused"); assert result2["status"]=="ok" and len(refused.calls)==3 and result2["raw_calls"][0]["status"]=="transport_error"
def test_valid_visual_judgment_is_never_retried(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); scout=clean_scout(); api=FakeAPI([scout,empty_verifier()]); patch_runtime(monkeypatch,api)
    result=run_judge.judge(runtime,tmp_path/"run"); assert result["status"]=="ok" and len(api.calls)==2
def test_cache_requires_input_and_protocol_hash_match(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); api=FakeAPI([clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,api); out=tmp_path/"run"; run_judge.judge(runtime,out)
    assert run_judge.judge(runtime,out)["status"]=="ok"
    changed=dict(runtime,scene_prompt="changed")
    with pytest.raises(PlacementValidationError,match="stale cache refused"): run_judge.judge(changed,out)
def test_audit_has_ids_latency_tokens_and_derived_hash(tmp_path,monkeypatch):
    runtime=make_runtime(tmp_path); api=FakeAPI([clean_scout(),empty_verifier()]); patch_runtime(monkeypatch,api); result=run_judge.judge(runtime,tmp_path/"run")
    for call in result["raw_calls"]:
        assert call["response_id"] and call["latency_ms"] is not None and call["prompt_tokens"]==100 and call["completion_tokens"]==50 and call["response_finished_at"]
    assert result["audit"]["derived_sha256"] and result["audit"]["runner_sha256"]
def test_error_sentinel_contract():
    result=error_sentinel("boom"); assert result["score"]==0 and not result["score_valid"] and result["verdict"]=="review"
def test_protocol_is_gpt55_high_reasoning_compact_two_pass():
    source=(ROOT/"run_judge.py").read_text(); assert 'model: str = "gpt-5.5"' in source and 'reasoning_effort="high"' in source
    assert run_judge.PROTOCOL_VERSION=="hp-natural-placement-v4.4-two-pass-v2" and 'max_completion_tokens=9000' in source and 'max_completion_tokens=4000' in source
def test_gate_a_runner_fails_closed_on_first_nonscoreable_result():
    source=(ROOT/"run_dev_gate.py").read_text()
    assert "result['status']!='ok' or not result['derived']['score_valid']" in source
    assert "status={result['status']}" in source
