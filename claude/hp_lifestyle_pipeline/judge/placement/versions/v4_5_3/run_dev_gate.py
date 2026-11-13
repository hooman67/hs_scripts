#!/usr/bin/env python3
# ruff: noqa: UP017
"""Sequential resumable frozen Gate A: three independent repeats for six development cases."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from run_judge import judge

ROOT=Path(__file__).resolve().parent
FREEZE=ROOT/'protocol_freeze.json'
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def verify_environment():
    expected=json.loads((ROOT/'runtime_environment.json').read_text())
    actual={'python':platform.python_version(),
            'packages':{name:version(name) for name in expected['packages']}}
    if actual!=expected: raise RuntimeError(f'runtime environment mismatch: expected={expected} actual={actual}')
    return actual
def verify_freeze():
    freeze=json.loads(FREEZE.read_text()); mismatches=[]
    for relative,expected in freeze['files'].items():
        path=ROOT/relative
        if not path.is_file() or sha(path)!=expected: mismatches.append(relative)
    frozen_manifest=json.loads((ROOT/'data/dev_6_manifest.json').read_text())
    for row in frozen_manifest['records']:
        runtime=row['runtime_input']; expected=row['frozen_hashes']
        actual={
            'generated_image_sha256':sha(runtime['generated_image']),
            'twin_image_sha256':sha(runtime['twin_image']),
        }
        if actual!=expected: mismatches.append(f"input:{row['record_id']}")
    if mismatches: raise RuntimeError('protocol freeze mismatch: '+', '.join(mismatches))
    return freeze
freeze=verify_freeze(); environment=verify_environment(); manifest=json.loads((ROOT/'data/dev_6_manifest.json').read_text())
run_root=ROOT/'runs/dev_6_gate_a_v4_5_3_gpt55'; run_root.mkdir(parents=True,exist_ok=True)
progress_path=run_root/'progress.json'
def write(value):
    temporary=progress_path.with_suffix('.tmp'); temporary.write_text(json.dumps(value,indent=2)+'\n'); temporary.replace(progress_path)
progress={'schema_version':'hp-placement-v4.5.3-dev-six-gate-a-progress-v1','protocol_freeze_sha256':sha(FREEZE),'runtime_environment':environment,'started_at':datetime.now(timezone.utc).isoformat(),'finished_at':None,'model':'gpt-5.5','repeats_per_case':3,'records':[]}
if progress_path.exists():
    progress=json.loads(progress_path.read_text())
    if progress.get('protocol_freeze_sha256')!=sha(FREEZE): raise RuntimeError('resume freeze mismatch')
seen={(r['record_id'],r['repeat']) for r in progress['records'] if r['status']=='ok'}
for row in manifest['records']:
    for repeat in range(1,4):
        if (row['record_id'],repeat) in seen: continue
        verify_freeze(); verify_environment()
        result=judge(row['runtime_input'],run_root/row['record_id']/f'repeat_{repeat}',model='gpt-5.5')
        progress['records'].append({'record_id':row['record_id'],'repeat':repeat,'status':result['status'],'score':result['derived']['score'],'score_valid':result['derived']['score_valid'],'verdict':result['derived']['verdict'],'calls':len(result['raw_calls']),'response_ids':[call.get('response_id') for call in result['raw_calls']],'result_path':str(run_root/row['record_id']/f'repeat_{repeat}'/'result.json')})
        write(progress)
        if result['status']!='ok' or not result['derived']['score_valid']:
            raise RuntimeError(f"Gate A aborted after persisted non-scoreable result: {row['record_id']} repeat {repeat} status={result['status']}")
progress['finished_at']=datetime.now(timezone.utc).isoformat(); write(progress)
print(json.dumps({'done':len(progress['records']),'expected':18,'run_root':str(run_root)},indent=2))
