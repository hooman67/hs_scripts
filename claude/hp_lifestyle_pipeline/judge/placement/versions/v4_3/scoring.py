"""Local validation, deterministic check derivation, and scoring for compact V4.3."""
from __future__ import annotations
import hashlib,json
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
from typing import Any,Mapping
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent
ASSESSMENT_SCHEMA=json.loads((ROOT/'assessment_schema.json').read_text()); RESULT_SCHEMA=json.loads((ROOT/'result_schema.json').read_text())
ASSESSMENT_VALIDATOR=Draft202012Validator(ASSESSMENT_SCHEMA); RESULT_VALIDATOR=Draft202012Validator(RESULT_SCHEMA)
FACTS=["support_type","room_location","product_footprint_and_front","surface_position","support_edges_and_corners","load_path","room_relations","operating_approach","associated_user_position","props_activity"]
TRIGGERS=["support_role","room_use_zone","device_surface_position","props_use_relation","operating_access","user_position","device_support_axes","furniture_room_axes","product_scale","support_load_path","support_shape","shared_perspective","support_contact","shadows_reflections"]
CHECK_TRIGGERS={"support_role":["support_role"],"room_use_zone":["room_use_zone"],"device_surface_position":["device_surface_position"],"props_use_relation":["props_use_relation"],"operating_access":["operating_access"],"user_position":["user_position"],"device_support_axes":["device_support_axes"],"furniture_room_axes":["furniture_room_axes"],"product_scale":["product_scale"],"support_anatomy":["support_load_path","support_shape"],"shared_perspective":["shared_perspective"],"support_contact":["support_contact"],"shadows_reflections":["shadows_reflections"]}
ISSUE_OWNERS={"support_role":{"inappropriate_support","occupied_workstation"},"room_use_zone":{"misplaced_support_furniture","incoherent_use_zone"},"device_surface_position":{"unmotivated_device_position"},"props_use_relation":{"incoherent_prop_arrangement"},"operating_access":{"blocked_operating_path","excessive_reach"},"user_position":{"no_feasible_user_position","chair_displacement"},"device_support_axes":{"device_support_axis_conflict"},"furniture_room_axes":{"furniture_layout_conflict"},"product_scale":{"implausible_scale"},"support_anatomy":{"missing_required_support","malformed_support_furniture"},"shared_perspective":{"conflicting_perspective"},"support_contact":{"unsupported_product","floating","sinking_or_intersection"},"shadows_reflections":{"inconsistent_shadow","inconsistent_reflection"}}
COMPONENT_WEIGHTS={"support_scenario":20,"access_usability":30,"orientation_alignment":20,"scale_perspective":15,"contact_integration":15}
COMPONENT_CHECKS={"support_scenario":["support_role","room_use_zone","device_surface_position","props_use_relation"],"access_usability":["operating_access","user_position"],"orientation_alignment":["device_support_axes","furniture_room_axes"],"scale_perspective":["product_scale","support_anatomy","shared_perspective"],"contact_integration":["support_contact","shadows_reflections"]}
VIS={"observed":1.0,"partial":.5,"unobservable":0.0}; CONF={"low":0,"medium":.5,"high":1}
INPUT_SCHEMA={"type":"object","additionalProperties":False,"required":["generated_image","twin_image","product_type","scene_prompt"],"properties":{"generated_image":{"type":"string","minLength":1},"twin_image":{"type":"string","minLength":1},"product_type":{"enum":["laptop","printer"]},"scene_prompt":{"type":"string"},"target_record_id":{"type":"string","minLength":1},"device":{"type":"string","minLength":1},"camera":{"type":"string","minLength":1},"prompt_rank":{"type":["string","integer"]}}}
INPUT_VALIDATOR=Draft202012Validator(INPUT_SCHEMA)
class PlacementValidationError(ValueError):
 def __init__(self,errors): self.errors=tuple(errors); super().__init__('; '.join(errors))
def _errs(v,val):
 out=[]
 for e in sorted(val.iter_errors(v),key=lambda x:tuple(map(str,x.absolute_path))):
  p='$'+''.join(f'[{x}]' if isinstance(x,int) else f'.{x}' for x in e.absolute_path); out.append(f'{p}: {e.message}')
 return out
def validate_runtime_input(v):
 e=_errs(v,INPUT_VALIDATOR)
 if e: raise PlacementValidationError(e)
 return v
def _positive(r): return r is not None and r['image']=='generated_scene' and r['box'][2]>r['box'][0] and r['box'][3]>r['box'][1]
def validate_assessment(v):
 e=_errs(v,ASSESSMENT_VALIDATOR)
 if e: raise PlacementValidationError(e)
 if v['stage_status']=='unable':
  if v['unable_reason'] is None or v['inventory'] is not None or v['triggers'] is not None or v['defect_candidates']: e.append('unable invariant')
  if e: raise PlacementValidationError(e)
  return v
 if v['unable_reason'] is not None or v['inventory'] is None or v['triggers'] is None or not v['defect_candidates']: e.append('assessed requires inventory/triggers/candidates and null reason')
 inv=v['inventory']
 if inv:
  for n in FACTS:
   f=inv[n]
   if not f['observation'].strip(): e.append(f'inventory.{n} blank')
   if f['visibility']=='unobservable':
    if f['region'] is not None or not f['visibility_limit'].strip(): e.append(f'inventory.{n} unobservable invariant')
   else:
    if f['region'] is None or f['region']['box'][2]<=f['region']['box'][0] or f['region']['box'][3]<=f['region']['box'][1]: e.append(f'inventory.{n} visible fact requires region')
    if f['visibility']=='partial' and not f['visibility_limit'].strip(): e.append(f'inventory.{n} partial requires limit')
 by={}
 for c in v['defect_candidates']:
  if c['id'] in by: e.append(f'duplicate candidate {c["id"]}')
  by[c['id']]=c
  if c['issue_code'] not in ISSUE_OWNERS[c['owner_check']]: e.append(f'{c["id"]} illegal owner')
  linked=[v['triggers'][t]['answer'] for t in c['trigger_ids']]
  retained=c['disposition']=='retained'
  if retained:
   if not linked or any(a!='no' for a in linked): e.append(f'{c["id"]} retained must link only no triggers')
   if c['severity'] is None or not c['consequence'].strip() or not _positive(c['region']): e.append(f'{c["id"]} retained evidence invariant')
   if c['severity']==1 and c['warning_level'] not in {'advisory','review'}: e.append(f'{c["id"]} severity1 warning')
   if c['severity']>=2 and c['warning_level']!='none': e.append(f'{c["id"]} material warning none')
   if c['confidence']=='high' and c['alternative_status']!='excluded_by_visible_evidence': e.append(f'{c["id"]} high confidence alternative')
  else:
   if any(a=='no' for a in linked) or c['severity'] is not None or c['warning_level']!='none': e.append(f'{c["id"]} rejected invariant')
  if c['issue_code']=='chair_displacement' and retained and c['severity']!=1: e.append(f'{c["id"]} chair severity')
  if c['issue_code']=='missing_required_support' and retained:
   m=c['missing_support_test']
   if m is None or not _positive(m['exposed_required_region']): e.append(f'{c["id"]} missing support test')
  elif c['missing_support_test'] is not None: e.append(f'{c["id"]} unexpected missing support test')
 for n in TRIGGERS:
  t=v['triggers'][n]; cid=t['candidate_id']
  if cid not in by: e.append(f'trigger {n} dangling candidate')
  else:
   c=by[cid]
   if n not in c['trigger_ids']: e.append(f'{n}<->{cid} not reciprocal')
   if t['answer']=='no' and c['disposition']!='retained': e.append(f'{n} no requires retained')
   if t['answer']!='no' and c['disposition']!='rejected': e.append(f'{n} yes/unknown requires rejected')
  if t['answer']=='unknown' and not t['visibility_limit'].strip(): e.append(f'{n} unknown limit')
  if t['visibility']=='unobservable' and t['answer']!='unknown': e.append(f'{n} unobservable must unknown')
 for cid,c in by.items():
  for t in c['trigger_ids']:
   if v['triggers'][t]['candidate_id']!=cid: e.append(f'{cid}<->{t} not reciprocal')
 seen=set()
 for c in by.values():
  k=(' '.join(c['physical_relation'].lower().split()),json.dumps(c['region'],sort_keys=True),c['issue_code'])
  if k in seen: e.append(f'duplicate physical candidate {c["id"]}')
  seen.add(k)
 if inv and inv['support_and_room_landmarks_visible']:
  for n in ('room_use_zone','furniture_room_axes','shared_perspective'):
   if v['triggers'][n]['visibility']=='unobservable': e.append(f'{n} cannot be unobservable with landmarks')
 if e: raise PlacementValidationError(e)
 return v
def derive_checks(v):
 validate_assessment(v); by={c['id']:c for c in v['defect_candidates']}; checks={}
 rank={'unobservable':0,'partial':1,'observed':2}
 for owner,names in CHECK_TRIGGERS.items():
  ts=[v['triggers'][n] for n in names]; visibility=max((t['visibility'] for t in ts),key=rank.get)
  cs=[]
  for t in ts:
   c=by[t['candidate_id']]
   if c['disposition']=='retained' and c['owner_check']==owner and c not in cs: cs.append(c)
  if cs:
   severity=max(c['severity'] for c in cs); at=[c for c in cs if c['severity']==severity]; confidence=max((c['confidence'] for c in at),key=CONF.get)
   warning='review' if severity==1 and any(c['warning_level']=='review' for c in at) else 'advisory' if severity==1 else 'none'
  else: severity=None if visibility=='unobservable' else 0; confidence='low' if visibility=='unobservable' else 'high'; warning='none'
  checks[owner]={"visibility":visibility,"severity":severity,"confidence":confidence,"warning_level":warning,"issue_codes":sorted({c['issue_code'] for c in cs}),"evidence":" ".join(c['evidence'] for c in cs) or "No visible retained defect.","consequence":" ".join(c['consequence'] for c in cs),"alternative_explanation":" ".join(c['benign_alternative'] for c in cs),"visibility_limit":"; ".join(t['visibility_limit'] for t in ts if t['visibility_limit']),"inventory_refs":sorted({f for t in ts for f in t['fact_refs']}),"candidate_ids":[c['id'] for c in cs]}
 return checks
def _round(x): return int(Decimal(str(x)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def aggregate_assessment(v):
 checks=derive_checks(v); retained=[c for c in v['defect_candidates'] if c['disposition']=='retained']; confirmed=[c for c in retained if c['severity']>=2 and c['confidence']=='high']; uncertain=[c for c in retained if c['severity']>=2 and c['confidence']!='high']; reviews=[c for c in retained if c['severity']==1 and c['warning_level']=='review']; advisories=[c for c in retained if c['severity']==1 and c['warning_level']=='advisory']
 comps={}; tw=ws=cn=0.0
 for comp,names in COMPONENT_CHECKS.items():
  cov=sum(VIS[checks[n]['visibility']] for n in names)/len(names); ew=COMPONENT_WEIGHTS[comp]*cov; sevs=[]
  for n in names:
   c=checks[n]; vv=VIS[c['visibility']]
   if vv:
    sev=c['severity']; sevs.append(1 if sev>=2 and c['confidence']!='high' else sev); cn+=COMPONENT_WEIGHTS[comp]*vv/len(names)*CONF[c['confidence']]
  sc=100-25*max(sevs) if sevs else None
  if sc is not None: ws+=ew*sc; tw+=ew
  comps[comp]={"coverage":round(cov,3),"score":sc,"effective_weight":round(ew,3)}
 if not tw: raise PlacementValidationError(['no observable evidence'])
 cap={2:59,3:39,4:19}[max(c['severity'] for c in confirmed)] if confirmed else 79 if uncertain else None; base=ws/tw; score=_round(min(base,cap) if cap is not None else base); cov=tw/100; q=cn/tw; confidence='high' if cov>=.85 and q>=.85 and not uncertain else 'medium' if cov>=.6 and q>=.6 else 'low'; verdict='fail' if confirmed else 'review' if uncertain or reviews else 'pass'
 reasons=[]
 if confirmed: reasons.append('confirmed_material_defect')
 if uncertain: reasons.append('uncertain_material_defect')
 if reviews: reasons.append('placement_review_warning')
 if advisories: reasons.append('placement_advisory')
 if v['general_artifact_warnings']: reasons.append('general_artifact_warning')
 findings=[]
 for c in retained:
  category='confirmed_material_defect' if c in confirmed else 'uncertain_material_defect' if c in uncertain else 'placement_review_warning' if c in reviews else 'placement_advisory'; findings.append({"category":category,"candidate_id":c['id'],"owner_check":c['owner_check'],"issue_code":c['issue_code'],"severity":c['severity'],"confidence":c['confidence'],"evidence":c['evidence'],"consequence":c['consequence']})
 exp=' '.join(f"{verdict.capitalize()}: {c['issue_code']} — {c['evidence']} Consequence: {c['consequence']} Confidence: {c['confidence']}. Owned by {c['owner_check']}." for c in retained) or 'Pass: no visible placement defect was retained on observable evidence.'
 return {"rules_version":"placement-scoring-v4.3","score":score,"score_label":"100 on observable evidence" if score==100 else str(score),"verdict":verdict,"confidence":confidence,"coverage":round(cov,3),"checks":checks,"components":comps,"verdict_reasons":reasons,"findings":findings,"owned_issue_codes":sorted({c['issue_code'] for c in retained}),"explanation":exp}
def validate_result(v):
 e=_errs(v,RESULT_VALIDATOR)
 if e: raise PlacementValidationError(e)
 if v['status']=='ok':
  if v['assessment'] is None or v['derived'] is None or v['error'] is not None: e.append('ok envelope')
  else:
   validate_assessment(v['assessment']); expected=aggregate_assessment(v['assessment'])
   if v['derived']!=expected: e.append('derived output does not match deterministic recomputation')
   if v['audit'].get('derived_sha256')!=canonical_json_sha256(expected): e.append('derived_sha256 mismatch')
 elif v['status']=='unassessable':
  if v['assessment'] is None or v['assessment'].get('stage_status')!='unable' or v['derived'] is not None or v['error'] is not None: e.append('unassessable envelope')
 else:
  if v['derived'] is not None or v['error'] is None: e.append('error envelope')
 if v['status']!='ok' and v['audit'].get('derived_sha256') is not None: e.append('non-ok envelope must have derived_sha256=null')
 if e: raise PlacementValidationError(e)
 return v
def canonical_json_sha256(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
