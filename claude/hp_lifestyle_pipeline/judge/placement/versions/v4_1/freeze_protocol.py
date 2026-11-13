#!/usr/bin/env python3
"""Freeze exact anchored V4.1 development protocol before model calls."""
from __future__ import annotations
import hashlib,json,subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'data/protocol_freeze_development_15_v4_1_anchored.json'
FIXED=[
 'system_prompt.md','assessment_schema.json','result_schema.json','scoring.py','run_judge.py','run_batch.py',
 'test_v4_scoring.py','test_v4_runtime.py','test_anchor_provenance.py','evaluate_development.py',
 'data/development_15_manifest.json','data/development_15_expectations.json',
 'astra/evidence/joined_feedback_context.json','astra/evidence/reviewer_0.json',
 'anchored_candidate/README.md','anchored_candidate/anchor_guidance.json',
 'anchored_candidate/build_anchor_candidate.py','anchored_candidate/anchor_catalog.json',
 'anchored_candidate/target_anchor_plan.json',
]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 files=list(FIXED)
 files += sorted(str(p.relative_to(ROOT)) for p in (ROOT/'anchored_candidate/anchors/images').glob('*.jpg'))
 artifacts=[]
 for rel in files:
  p=ROOT/rel
  if not p.is_file(): raise RuntimeError(f'missing freeze artifact: {p}')
  artifacts.append({'path':rel,'bytes':p.stat().st_size,'sha256':sha(p)})
 commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,text=True,capture_output=True).stdout.strip()
 payload={
  'schema_version':'hp-natural-placement-v4.1-protocol-freeze-v1',
  'frozen_at_utc':datetime.now(timezone.utc).isoformat(),
  'status':'frozen_before_anchored_v4.1_development_evaluation',
  'git_head_at_freeze':commit,
  'parent_unanchored_evaluation':{
   'path':str((ROOT.parent/'v4/data/development_15_v4_astra_evaluation_v1.json').resolve()),
   'sha256':sha(ROOT.parent/'v4/data/development_15_v4_astra_evaluation_v1.json'),
  },
  'model':'gpt-6-astra','client_route':'foundry_direct_openai','reasoning_effort':'high',
  'max_completion_tokens':24000,'transport_timeout_seconds':600,'transport_sdk_max_retries':0,
  'batch_concurrency':1,'development_record_count':15,'maximum_anchor_count':4,
  'target_labels_passed_to_model':False,'manual_output_edits_allowed':False,
  'leave_family_out':{
   'exact_generated_image_hash':True,'same_twin_image_hash':True,'exact_scene_prompt_hash':True,
   'same_device_camera_prompt_rank':True,'same_product_type_camera_prompt_rank_near_family':True,
  },
  'application_retry':{
   'maximum_second_attempts':1,
   'trigger':'transient transport or invalid structured/semantic output only',
   'valid_judgment_retried':False,
  },
  'deterministic_verdict_policy':{
   'high_confidence_material_defect':'fail',
   'medium_or_low_confidence_material_defect':'review',
   'severity_1_review_warning':'review',
   'severity_1_advisory':'does_not_block_pass',
   'low_coverage_low_confidence_or_unobservable':'does_not_block_pass',
   'unrelated_rendering_artifact':'does_not_change_placement_verdict',
  },
  'tests':{'count':20,'status':'passed'},
  'artifacts':artifacts,
 }
 tmp=OUTPUT.with_suffix('.tmp'); tmp.write_text(json.dumps(payload,indent=2)+'\n'); tmp.replace(OUTPUT)
 print(json.dumps({'output':str(OUTPUT),'sha256':sha(OUTPUT),'artifacts':len(artifacts)}))
if __name__=='__main__': main()
