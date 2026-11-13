#!/usr/bin/env python3
"""Freeze the six previously used development targets without labels or eval metadata."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
source=ROOT.parent/'v4_3_1/data/gate_6_manifest.json'
data=json.loads(source.read_text())
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
records=[]
for row in data['records']:
    runtime={key:row['runtime_input'][key] for key in ('generated_image','twin_image','product_type','scene_prompt')}
    records.append({'record_id':row['record_id'],'runtime_input':runtime,'frozen_hashes':{'generated_image_sha256':sha(runtime['generated_image']),'twin_image_sha256':sha(runtime['twin_image']),'scene_prompt_sha256':hashlib.sha256(runtime['scene_prompt'].encode()).hexdigest()}})
out={'schema_version':'hp-placement-v4.4-development-six-manifest-v1','evaluation_role':'reused labeled development cases; not held-out validation','labels_passed_to_judge':False,'records':records}
(ROOT/'data/dev_6_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(records))
