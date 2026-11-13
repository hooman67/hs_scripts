#!/usr/bin/env python3
"""Create immutable V4.4 Gate A protocol freeze before model calls."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
files=[
 'DESIGN_AND_CLAIM_BOUNDARY.md','build_schemas.py','codebook.py','scoring.py','geometry.py','run_judge.py','run_dev_gate.py','preflight_dev_gate.py',
 'scout_system_prompt.md','verifier_system_prompt.md','scout_schema.json','scout_wire_schema.json','verifier_schema.json','verifier_wire_schema.json',
 'data/dev_6_manifest.json','data/dev_6_preflight.json','test_v4_4.py','astra_design/astra_task.md','astra_design/astra_output.md']
missing=[name for name in files if not (ROOT/name).is_file()]
if missing: raise SystemExit('missing: '+', '.join(missing))
freeze={'schema_version':'hp-placement-v4.4-gate-a-protocol-freeze-v1','created_at':datetime.now(timezone.utc).isoformat(),'status':'frozen_before_any_v4_4_model_call','evaluation_role':'six reused labeled development cases; three independent repeats each','model':'gpt-5.5','reasoning_effort':'high','sdk_retries':0,'maximum_calls_per_repeat':3,'shared_repair_budget_per_repeat':1,'repeats_per_case':3,'labels_passed_to_judge':False,'files':{name:sha(ROOT/name) for name in files}}
(ROOT/'protocol_freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
print(sha(ROOT/'protocol_freeze.json'))
