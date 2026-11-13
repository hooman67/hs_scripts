from __future__ import annotations
import json,sys,types
from pathlib import Path
import pytest
from PIL import Image
from anchor_selection import CATALOG_PATH,select_anchors
from build_wire_schema import enum_count
from crop import create_support_crop
from scoring import RESULT_SCHEMA,PlacementValidationError,aggregate_assessment,derive_checks,validate_assessment,validate_result,validate_runtime_input
if 'foundry_aws_gateway' not in sys.modules:
 p=types.ModuleType('foundry_aws_gateway'); l=types.ModuleType('foundry_aws_gateway.llm'); p.llm=l; sys.modules['foundry_aws_gateway']=p; sys.modules['foundry_aws_gateway.llm']=l
import run_judge
import run_remaining_five
ROOT=Path(__file__).resolve().parent
FACTS=["support_type","room_location","product_footprint_and_front","surface_position","support_edges_and_corners","load_path","room_relations","operating_approach","associated_user_position","props_activity"]
OWNER={"support_role":("support_role","inappropriate_support"),"room_use_zone":("room_use_zone","incoherent_use_zone"),"device_surface_position":("device_surface_position","unmotivated_device_position"),"props_use_relation":("props_use_relation","incoherent_prop_arrangement"),"operating_access":("operating_access","excessive_reach"),"user_position":("user_position","chair_displacement"),"device_support_axes":("device_support_axes","device_support_axis_conflict"),"furniture_room_axes":("furniture_room_axes","furniture_layout_conflict"),"product_scale":("product_scale","implausible_scale"),"support_load_path":("support_anatomy","missing_required_support"),"support_shape":("support_anatomy","malformed_support_furniture"),"shared_perspective":("shared_perspective","conflicting_perspective"),"support_contact":("support_contact","floating"),"shadows_reflections":("shadows_reflections","inconsistent_shadow")}
def reg(): return {"image":"generated_scene","label":"visible region","box":[.1,.1,.8,.8]}
def clean():
 facts={n:{"visibility":"observed","observation":"Visible relation.","region":reg(),"visibility_limit":""} for n in FACTS}
 inv={"scene_extent":"wide","support_and_room_landmarks_visible":True,**facts}; triggers={}; cs=[]
 for i,(t,(owner,code)) in enumerate(OWNER.items()):
  cid=f'tested_{i}'; triggers[t]={"answer":"yes","visibility":"observed","evidence":"Positive condition visible.","fact_refs":["support_type"],"candidate_id":cid,"visibility_limit":""}
  cs.append({"id":cid,"physical_relation":f'distinct relation {i}',"hypothesis":f'tested hypothesis {i}',"trigger_ids":[t],"owner_check":owner,"issue_code":code,"disposition":"rejected","evidence":"Visible benign arrangement.","benign_alternative":"Positive condition holds.","alternative_status":"remains_substantial","severity":None,"confidence":"low","warning_level":"none","consequence":"","region":None,"missing_support_test":None})
 return {"inventory":inv,"triggers":triggers,"defect_candidates":cs,"stage_status":"assessed","unable_reason":None,"general_artifact_warnings":[]}
def retain(a,t,severity=2,confidence='high',warning='none'):
 owner,code=OWNER[t]; cid=a['triggers'][t]['candidate_id']; c=next(c for c in a['defect_candidates'] if c['id']==cid); a['triggers'][t]['answer']='no'; c.update(disposition='retained',evidence='Specific visible defect.',alternative_status='excluded_by_visible_evidence' if confidence=='high' else 'remains_substantial',severity=severity,confidence=confidence,warning_level=warning,consequence='Believability impaired.',region=reg())
 if code=='missing_required_support': c['missing_support_test']={"exposed_required_region":reg(),"required_support_reason":"Span requires support.","visible_break_evidence":"Visible connection terminates.","alternate_load_paths":"Distant panel only.","hidden_limits":"No connector bridges exposed break."}
def test_clean_pass_and_derived_checks():
 a=clean(); validate_assessment(a); d=aggregate_assessment(a); assert d['verdict']=='pass' and len(d['checks'])==13
def test_unknown_does_not_lower_pass():
 a=clean(); a['triggers']['user_position'].update(answer='unknown',visibility='unobservable',visibility_limit='Chair outside crop.'); validate_assessment(a); assert aggregate_assessment(a)['verdict']=='pass'
def test_chair_review():
 a=clean(); retain(a,'user_position',1,'high','review'); assert aggregate_assessment(a)['verdict']=='review'; assert derive_checks(a)['user_position']['issue_codes']==['chair_displacement']
def test_confirmed_candidate_fails_despite_higher_uncertain_same_check():
 a=clean(); retain(a,'support_load_path',2,'high'); retain(a,'support_shape',4,'low'); d=aggregate_assessment(a); assert d['verdict']=='fail' and d['score']<=59
def test_invalid_ref_and_id_fail_local():
 a=clean(); a['triggers']['support_role']['fact_refs']=['bad_ref'];
 with pytest.raises(PlacementValidationError): validate_assessment(a)
 b=clean(); b['defect_candidates'][0]['id']='INVALID!'
 with pytest.raises(PlacementValidationError): validate_assessment(b)
def test_wire_compact_and_strict_shape():
 assert enum_count(run_judge.WIRE_SCHEMA)<1000 and len(json.dumps(run_judge.WIRE_SCHEMA))<30000
 failures=[]
 def walk(v,p='$'):
  if isinstance(v,dict):
   if 'const' in v and 'type' not in v: failures.append(p+' const')
   if v.get('type')=='object' or 'properties' in v:
    if v.get('additionalProperties') is not False or set(v.get('required',[]))!=set(v.get('properties',{})): failures.append(p+' object')
   for k,x in v.items(): walk(x,p+'.'+k)
  elif isinstance(v,list):
   for i,x in enumerate(v): walk(x,f'{p}[{i}]')
 walk(run_judge.WIRE_SCHEMA); assert failures==[]
def make_target(tmp,name='x'):
 s=tmp/f'{name}s.png'; t=tmp/f'{name}t.png'; Image.new('RGB',(64,48),(50,60,70)).save(s); Image.new('RGB',(64,48),'white').save(t)
 return {"generated_image":str(s),"twin_image":str(t),"product_type":"laptop","scene_prompt":"plain scene"}
def test_arbitrary_runtime_and_anchor_exclusions(tmp_path):
 target=make_target(tmp_path); validate_runtime_input(target); selected,audit=select_anchors(target); assert len(selected) in {0,4} and audit['union_target_count']==1
 catalog=json.loads(CATALOG_PATH.read_text()); anchor=catalog['records'][0]; collision={"generated_image":anchor['generated']['source_path'],"twin_image":anchor['twin']['source_path'],"product_type":anchor['product_type'],"scene_prompt":anchor['scene_prompt']}; _,a=select_anchors(target,catalog=catalog,exclusion_targets=[collision]); assert anchor['anchor_id'] in a['excluded']
def test_crop_fallback(tmp_path):
 target=make_target(tmp_path); _,p=create_support_crop(target['generated_image'],target['twin_image'],tmp_path/'crop'); assert p['localization_status']=='fallback_full_scene'
def test_runner_persists_finish_usage_and_content_metadata(tmp_path,monkeypatch):
 target=make_target(tmp_path,'run'); assessment=clean(); raw=json.dumps(assessment)
 class Obj:
  def __init__(self,**kw): self.__dict__.update(kw)
 response=Obj(model='gpt-5.5-2026-04-23',usage=Obj(total_tokens=321),choices=[Obj(finish_reason='stop',message=Obj(content=raw,refusal=None))])
 class Completions:
  def create(self,**kwargs): return response
 fake=Obj(chat=Obj(completions=Completions()))
 monkeypatch.setattr(run_judge,'client',lambda:(fake,'test_direct_route'))
 out=tmp_path/'out'; result=run_judge.judge(target,out)
 assert result['status']=='ok'; attempt=result['raw_attempts'][0]; assert attempt['finish_reason']=='stop' and attempt['total_tokens']==321 and attempt['content_bytes']==len(raw.encode())
 assert json.loads((out/'attempt_1_metadata.json').read_text())['finish_reason']=='stop'
 tampered=json.loads(json.dumps(result)); tampered['derived']['checks']['user_position']['severity']=4
 with pytest.raises(PlacementValidationError): validate_result(tampered)


def test_production_default_is_gpt55_high_reasoning():
 import inspect
 assert inspect.signature(run_judge.judge).parameters['model'].default=='gpt-5.5'
 source=Path(run_judge.__file__).read_text()
 assert 'reasoning_effort="high"' in source


def test_laptop_chair_quality_regression_rule_is_explicit():
 prompt=(ROOT/'system_prompt.md').read_text()
 assert 'When one visible chair is the only plausible associated user position, evaluate that chair even if it is partly cropped.' in prompt
 assert 'Partial visibility is not permission to invent a second, centered, off-frame chair' in prompt
 assert 'answer `user_position: no` and retain `chair_displacement` at severity 1 with `warning_level: review`' in prompt
 assert 'Use unknown only when no plausible associated chair or standing position is visible' in prompt


def test_v4_3_1_protocol_and_result_identity():
 assert run_judge.PROTOCOL_VERSION=='hp-natural-placement-v4.3.1-compact-quality-canary-v1'
 assert RESULT_SCHEMA['properties']['schema_version']['const']=='hp-natural-placement-v4.3.1-result-v1'


def test_client_route_is_direct_foundry_gateway(monkeypatch):
 calls={}
 class Dummy:
  def with_options(self,**kwargs): calls.update(kwargs); return self
 monkeypatch.setattr(run_judge.foundry_aws_gateway.llm,'get_openai',lambda:Dummy(),raising=False)
 _,route=run_judge.client(); assert route=='foundry_direct_openai'; assert calls=={'timeout':600.0,'max_retries':0}


def test_remaining_five_uses_all_six_for_anchor_exclusion():
 manifest=ROOT/'data/gate_6_manifest.json'
 remaining,exclusions=run_remaining_five.load_plan(manifest)
 assert len(remaining)==5 and len(exclusions)==6
 assert run_remaining_five.CANARY_RECORD_ID not in {r['record_id'] for r in remaining}
 assert run_remaining_five.CANARY_RECORD_ID in {r['target_record_id'] for r in exclusions}
 assert {r['record_id'] for r in remaining}|{run_remaining_five.CANARY_RECORD_ID}=={r['record_id'] for r in json.loads(manifest.read_text())['records']}


def test_frozen_quality_canary_result_is_immutable_and_valid():
 path=ROOT/'runs/quality-canary-v1-gpt55/result/result.json'
 assert run_judge.file_sha(path)=='182e3fd9f438f4b9df33616cd0f0936d994e5b01b9ff3735d1c89f882a4ddf30'
 result=json.loads(path.read_text()); validate_result(result)
 assert result['derived']['verdict']=='review'
 assert result['derived']['owned_issue_codes']==['chair_displacement']
 assert result['audit']['derived_sha256']=='9bbbdeae0af28d72f4eddf44bebe6a2c241be7382291aa2f522a7e48fe43b721'
