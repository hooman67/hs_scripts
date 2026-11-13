"""Strict local validation and deterministic V4.4 scout/verifier reconciliation."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any, Mapping
from jsonschema import Draft202012Validator
from codebook import DEFECT_SUBTYPES, NONDEFECT_SUBTYPE, SUBTYPE_FIELD, TEST_ISSUES, issue_for, issue_for_subtype
ROOT = Path(__file__).resolve().parent
SCOUT_SCHEMA = json.loads((ROOT / "scout_schema.json").read_text())
VERIFIER_SCHEMA = json.loads((ROOT / "verifier_schema.json").read_text())
SCOUT_VALIDATOR = Draft202012Validator(SCOUT_SCHEMA)
VERIFIER_VALIDATOR = Draft202012Validator(VERIFIER_SCHEMA)
COMPONENT_TESTS = {
    "support_scenario": ["support_role", "support_room_placement", "device_surface_position", "prop_activity_relation"],
    "access_usability": ["operating_access", "user_position"],
    "orientation_alignment": ["device_support_axes", "furniture_room_axes"],
    "scale_perspective": ["product_scale", "load_path", "support_anatomy", "shared_perspective"],
    "contact_integration": ["support_contact", "shadows_reflections"],
}
SEVERITY_PENALTY = {1: 12, 2: 40, 3: 70}
PENALTY_GROUPS = {
    "support_scene": {"support_role", "support_room_placement", "device_surface_position"},
    "operating_use": {"prop_activity_relation", "operating_access", "user_position"},
    "orientation_perspective": {"device_support_axes", "furniture_room_axes", "shared_perspective"},
    "scale": {"product_scale"},
    "structure_contact": {"load_path", "support_anatomy", "support_contact"},
    "light_transport": {"shadows_reflections"},
}
class PlacementValidationError(ValueError):
    def __init__(self, errors: list[str] | tuple[str, ...]):
        self.errors = tuple(errors); super().__init__("; ".join(self.errors))
def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
def _schema_errors(value: Any, validator: Draft202012Validator) -> list[str]:
    errors=[]
    for error in sorted(validator.iter_errors(value), key=lambda item: tuple(map(str,item.absolute_path))):
        path="$"+"".join(f"[{part}]" if isinstance(part,int) else f".{part}" for part in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors
def _valid_region(region: Mapping[str,Any]|None)->bool:
    if not region:return False
    x0,y0,x1,y1=region["box"]; return x1>x0 and y1>y0
def validate_scout(value: Mapping[str,Any])->Mapping[str,Any]:
    errors=_schema_errors(value,SCOUT_VALIDATOR)
    if value.get("stage_status")=="unable":
        if value.get("unable_reason") is None or value.get("inventory") is not None or value.get("tests") is not None: errors.append("unable scout requires a reason and null inventory/tests")
    elif value.get("stage_status")=="assessed":
        if value.get("unable_reason") is not None or value.get("inventory") is None or value.get("tests") is None: errors.append("assessed scout requires inventory/tests and null unable_reason")
        tests=value.get("tests") or []; ids=[test.get("test_id") for test in tests]
        if len(ids)!=len(set(ids)) or set(ids)!=set(TEST_ISSUES): errors.append("scout tests must contain every fixed test exactly once")
        for index,test in enumerate(tests):
            defect,severity=test.get("defect"),test.get("severity")
            if defect=="yes":
                if severity not in {1,2,3} or not _valid_region(test.get("region")): errors.append(f"tests[{index}] yes requires severity 1-3 and positive region")
                if test.get("test_id") in SUBTYPE_FIELD:
                    subtype=value.get("inventory",{}).get(SUBTYPE_FIELD[test["test_id"]])
                    if subtype not in DEFECT_SUBTYPES[test["test_id"]]: errors.append(f"tests[{index}] yes requires a defect subtype for {test['test_id']}")
            elif defect in {"no","unknown"}:
                if severity!=0: errors.append(f"tests[{index}] no/unknown requires severity=0")
                if defect=="unknown" and not str(test.get("visibility_limit","")).strip(): errors.append(f"tests[{index}] unknown requires visibility_limit")
                if test.get("test_id") in SUBTYPE_FIELD:
                    subtype=value.get("inventory",{}).get(SUBTYPE_FIELD[test["test_id"]])
                    required="unresolved" if defect=="unknown" else NONDEFECT_SUBTYPE[test["test_id"]]
                    if subtype!=required: errors.append(f"tests[{index}] {defect} requires {SUBTYPE_FIELD[test['test_id']]}={required}")
    if errors: raise PlacementValidationError(errors)
    return value
def defect_proposals(scout: Mapping[str,Any])->list[dict[str,Any]]:
    if scout["stage_status"]!="assessed": return []
    return [{"test_id":t["test_id"],"scout_severity":t["severity"],"visible_test":t["visible_test"],"direct_evidence":t["direct_evidence"],"counterevidence":t["counterevidence"],"visibility_limit":t["visibility_limit"],"region":t["region"]} for t in scout["tests"] if t["defect"]=="yes"]
def validate_verifier(value:Mapping[str,Any],proposals:list[Mapping[str,Any]])->Mapping[str,Any]:
    errors=_schema_errors(value,VERIFIER_VALIDATOR)
    if value.get("stage_status")=="unable":
        if value.get("unable_reason") is None or value.get("results"): errors.append("unable verifier requires reason and empty results")
    elif value.get("stage_status")=="verified":
        if value.get("unable_reason") is not None: errors.append("verified response requires null unable_reason")
        expected={p["test_id"] for p in proposals}; actual={r.get("test_id") for r in value.get("results",[])}
        if len(actual)!=len(value.get("results",[])) or actual!=expected: errors.append("verifier results must correspond one-to-one with all scout defect proposals")
        for index,result in enumerate(value.get("results",[])):
            decision,severity=result.get("decision"),result.get("severity")
            if decision=="confirmed":
                if severity not in {1,2,3} or result.get("observability")=="hidden" or not _valid_region(result.get("region")): errors.append(f"results[{index}] confirmed requires severity 1-3, visible/partial observability, and positive region")
                test_id=result.get("test_id"); subtype=result.get("observed_subtype")
                if test_id in DEFECT_SUBTYPES and subtype not in DEFECT_SUBTYPES[test_id]: errors.append(f"results[{index}] confirmed {test_id} requires an independently observed subtype")
                if test_id not in DEFECT_SUBTYPES and subtype!="not_applicable": errors.append(f"results[{index}] unambiguous test requires observed_subtype=not_applicable")
            elif decision in {"rejected","uncertain"} and severity!=0: errors.append(f"results[{index}] rejected/uncertain requires severity 0")
            elif decision in {"rejected","uncertain"} and result.get("observed_subtype")!="not_applicable": errors.append(f"results[{index}] rejected/uncertain requires observed_subtype=not_applicable")
            if decision=="uncertain" and result.get("observability")=="hidden": errors.append(f"results[{index}] uncertain requires visible or partial observability")
            if result.get("observability")=="hidden" and not str(result.get("visibility_limit","")).strip(): errors.append(f"results[{index}] hidden requires visibility_limit")
    if errors: raise PlacementValidationError(errors)
    return value
def _sentinel(reason:str,warnings:list[Mapping[str,Any]]|None=None)->dict[str,Any]:
    return {"rules_version":"hp-placement-v4.4-deterministic-v2","score":0,"score_valid":False,"verdict":"review","reason":reason,"checks":{},"components":{},"confirmed_issues":[],"uncertain_proposals":[],"advisories":[],"warnings":list(warnings or []),"penalty_causes":{},"owned_issue_codes":[],"explanation":"The product/support placement could not be assessed reliably."}
def error_sentinel(message:str)->dict[str,Any]:
    result=_sentinel("execution_error"); result["explanation"]=f"Judge execution failed: {message}"; return result
def reconcile(scout:Mapping[str,Any],verifier:Mapping[str,Any])->dict[str,Any]:
    validate_scout(scout); proposals=defect_proposals(scout)
    if verifier is None: raise PlacementValidationError(["a completed verifier is required even when scout proposals are empty"])
    validate_verifier(verifier,proposals)
    if scout["stage_status"]=="unable" or verifier["stage_status"]=="unable": return _sentinel("unassessable_target",scout.get("general_artifact_warnings"))
    scout_by_id={t["test_id"]:t for t in scout["tests"]}; verifier_by_id={r["test_id"]:r for r in verifier["results"]}
    checks={}; confirmed=[]; uncertain=[]
    for test_id in TEST_ISSUES:
        test=scout_by_id[test_id]; issue_code=issue_for(test_id,scout["inventory"]); state="tested_absent" if test["defect"]=="no" else "unobservable"; severity=0; evidence=test["direct_evidence"]; observability="hidden" if test["defect"]=="unknown" else "visible"
        if test["defect"]=="yes":
            result=verifier_by_id[test_id]; evidence=result["direct_evidence"]; observability=result["observability"]
            if result["decision"]=="confirmed":
                issue_code=issue_for_subtype(test_id,result["observed_subtype"]); state,severity="confirmed",result["severity"]; confirmed.append({"test_id":test_id,"issue_code":issue_code,"severity":severity,"evidence":evidence,"region":result["region"]})
            elif result["decision"]=="uncertain":
                state="unobservable" if observability=="hidden" else "uncertain"; uncertain.append({"test_id":test_id,"issue_code":issue_code,"severity":0,"scout_severity":test["severity"],"evidence":evidence,"region":result["region"]})
            else: state="unobservable" if observability=="hidden" else "not_confirmed"
        checks[test_id]={"state":state,"issue_code":issue_code,"severity":severity,"observability":observability,"evidence":evidence,"visibility_limit":test["visibility_limit"]}
    if all(check["state"]=="unobservable" for check in checks.values()): return _sentinel("all_relations_unobservable",scout["general_artifact_warnings"])
    # Frozen application-owned groups prevent model-controlled grouping and
    # apply at most one penalty to related consequences in the same domain.
    penalties={}
    for group,test_ids in PENALTY_GROUPS.items():
        group_confirmed=[item for item in confirmed if item["test_id"] in test_ids]
        group_uncertain=[item for item in uncertain if item["test_id"] in test_ids]
        severity=max((item["severity"] for item in group_confirmed),default=0)
        amount=SEVERITY_PENALTY[severity] if severity else (6 if group_uncertain else 0)
        penalties[group]={"severity":severity,"confirmed_tests":[item["test_id"] for item in group_confirmed],"uncertain_tests":[item["test_id"] for item in group_uncertain],"penalty":amount}
    raw_score=max(0,100-sum(c["penalty"] for c in penalties.values()))
    if any(i["severity"]>=2 for i in confirmed): verdict,score="fail",min(59,raw_score)
    elif any(i["severity"]==1 for i in confirmed) or uncertain: verdict,score="review",min(89,max(60,raw_score))
    else: verdict,score="pass",100
    components={}
    for component,test_ids in COMPONENT_TESTS.items():
        states=[checks[t]["state"] for t in test_ids]
        components[component]={"state":"fail" if any(checks[t]["state"]=="confirmed" and checks[t]["severity"]>=2 for t in test_ids) else ("review" if any(s in {"confirmed","uncertain"} for s in states) else "pass"),"tests":test_ids}
    parts=[f"{i['issue_code']} (severity {i['severity']}): {i['evidence']}" for i in confirmed]+[f"Unresolved {i['issue_code']}: {i['evidence']}" for i in uncertain]
    if not parts: parts.append("No placement defect was independently confirmed in observable regions.")
    if scout["general_artifact_warnings"]: parts.append("Separate rendering warnings: "+"; ".join(i["evidence"] for i in scout["general_artifact_warnings"]))
    return {"rules_version":"hp-placement-v4.4-deterministic-v2","score":score,"score_valid":True,"verdict":verdict,"reason":"confirmed_material_defect" if verdict=="fail" else ("reviewable_finding" if verdict=="review" else "no_confirmed_defect"),"checks":checks,"components":components,"confirmed_issues":confirmed,"uncertain_proposals":uncertain,"advisories":[],"warnings":scout["general_artifact_warnings"],"penalty_causes":penalties,"owned_issue_codes":sorted({i["issue_code"] for i in confirmed}),"explanation":" ".join(parts)}
