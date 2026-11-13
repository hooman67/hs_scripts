from build_triggers import confirmed_material, baseline_reliable, trigger_components
from run_verifier import response_schema, validate_response
from merge_verified_v2_new160 import final_policy


def comp(severity, confidence="high", visibility="observed", codes=None):
    return {"visibility":visibility,"severity":severity,"confidence":confidence,"evidence":"Visible evidence.","consequence":"Correction needed." if severity else "","issue_codes":codes or ([] if not severity else ["unmotivated_position"])}


def test_trigger_is_strictly_new_confirmed_material():
    names=["support_scenario","access_usability","orientation_alignment","scale_perspective","contact_integration"]
    base={name:comp(0) for name in names}; compact={name:comp(0) for name in names}
    compact["support_scenario"]=comp(2)
    value={"stages":{"baseline_v2":{"judgment":{"observation":{"components":base}}},"compact_v3":{"judgment":{"observation":{"components":compact}}}}}
    assert trigger_components(value)==["support_scenario"]
    assert confirmed_material(comp(2))
    assert not confirmed_material(comp(2,"low"))
    assert not confirmed_material(comp(1))
    assert not baseline_reliable(comp(None,"low","unobservable"))


def test_dynamic_schema_requires_every_and_only_proposed_component():
    names=["support_scenario","access_usability"]
    schema=response_schema(names)
    value={"schema_version":"placement-verifier-components-v1","components":{"support_scenario":comp(0),"access_usability":{**comp(0),"issue_codes":[]}}}
    validate_response(value,schema,names)
    value["components"].pop("access_usability")
    try: validate_response(value,schema,names)
    except ValueError: pass
    else: raise AssertionError("dropped component accepted")


def test_unobservable_clear_keeps_pass_with_note_and_confidence_cap():
    merged={"verdict":"pass","verdict_reasons":["pass_criteria_met"],"confidence":"high"}
    decision=final_policy("pass",merged,{"orientation_alignment":comp(None,"low","unobservable",[])})
    assert decision["verdict"]=="pass"
    assert decision["verdict_override"] is None
    assert decision["reported_overall_confidence"]=="medium"
    assert decision["uncertainty_notes"]
    assert "baseline component remains selected" not in decision["uncertainty_notes"][0]


def test_low_confidence_positive_material_caps_baseline_pass_to_review():
    merged={"verdict":"pass","verdict_reasons":["pass_criteria_met"],"confidence":"medium"}
    decision=final_policy("pass",merged,{"access_usability":comp(2,"low","partial",["no_user_position"])})
    assert decision["verdict"]=="review"
    assert decision["low_confidence_material_components"]==["access_usability"]


def test_existing_baseline_fail_is_preserved_despite_uncertainty():
    merged={"verdict":"fail","verdict_reasons":["clear_placement_defect_veto"],"confidence":"high"}
    decision=final_policy("fail",merged,{"access_usability":comp(2,"low","partial",["no_user_position"])})
    assert decision["verdict"]=="fail"
