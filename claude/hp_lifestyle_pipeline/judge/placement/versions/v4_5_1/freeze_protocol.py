#!/usr/bin/env python3
# ruff: noqa: UP017
"""Freeze the V4.5.1 Gate A protocol before any V4.5.1 model calls."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FILES=(
 'DESIGN_AND_CLAIM_BOUNDARY.md','astra_design/SYNTHESIS.md',
 'functional_observer_system.md','geometry_observer_system.md',
 'codebook.py','build_schemas.py','scoring.py','geometry.py','run_judge.py',
 'functional_observer_schema.json','functional_observer_wire_schema.json',
 'geometry_observer_schema.json','geometry_observer_wire_schema.json',
 'data/dev_6_manifest.json','data/dev_6_preflight.json',
 'runtime_environment.json',
 'preflight_dev_gate.py','run_dev_gate.py','evaluate_gate_a.py','test_v4_5_1.py','freeze_protocol.py',
)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
missing=[name for name in FILES if not (ROOT/name).is_file()]
if missing: raise RuntimeError('missing freeze files: '+', '.join(missing))
parser=argparse.ArgumentParser()
parser.add_argument('--verify', action='store_true')
args=parser.parse_args()
freeze_path=ROOT/'protocol_freeze.json'
if args.verify:
    if not freeze_path.is_file(): raise RuntimeError('protocol freeze is missing')
    frozen=json.loads(freeze_path.read_text())
    mismatches=[name for name,expected in frozen.get('files',{}).items()
                if not (ROOT/name).is_file() or sha(ROOT/name)!=expected]
    if mismatches: raise RuntimeError('protocol freeze mismatch: '+', '.join(mismatches))
    print(json.dumps({'verified':True,'files':len(frozen['files']),
                      'protocol_freeze_sha256':sha(freeze_path)},indent=2))
    raise SystemExit(0)
value={
 'schema_version':'hp-placement-v4.5.1-gate-a-protocol-freeze-v1',
 'created_at':datetime.now(timezone.utc).isoformat(),
 'status':'frozen_before_any_v4_5_1_model_call',
 'evaluation_role':'six reused labeled development cases; three independent repeats each',
 'model':'gpt-5.5','reasoning_effort':'high','sdk_retries':0,
 'normal_calls_per_repeat':2,'maximum_calls_per_repeat':3,'shared_repair_budget_per_repeat':1,
 'repeats_per_case':3,'labels_passed_to_judge':False,'scene_prompts_passed_to_judge':False,
 'files':{name:sha(ROOT/name) for name in FILES},
}
freeze_path.write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({'files':len(FILES),'protocol_freeze_sha256':sha(freeze_path)},indent=2))
