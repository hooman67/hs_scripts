#!/usr/bin/env python3
# /// script
# dependencies = ["boto3"]
# ///
"""Publish only this V5 review; verify bytes and content type in private Foundry S3."""
import hashlib,json,mimetypes,shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import boto3
HERE=Path(__file__).resolve().parent
BUCKET='foundry-hp-enterprise-adobe-assets'
PREFIX='eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/'
# Recreate presentation copies from the pinned canonical runtime after a fresh checkout.
version=HERE.parents[1]/'research/source_messaging_v1_to_v6/versions/v5'
pilot=json.loads((HERE/'manifest.json').read_text())
current_sha=hashlib.sha256((version/'system_prompt.md').read_bytes()).hexdigest()
scoring_policy=json.loads((HERE/'review_scoring_policy.json').read_text()) if (HERE/'review_scoring_policy.json').exists() else {}
assert current_sha==scoring_policy.get('current_runtime_system_sha256',pilot['provenance']['system_prompt']['sha256']), 'runtime does not match declared review policy'
(HERE/'runtime').mkdir(exist_ok=True)
for name in ['system_prompt.md','system_prompt.template.md','input.schema.json','output.schema.json','camera_profiles.json','reference_library.json','README.md','artifact_hashes.json']:
 shutil.copyfile(version/name,HERE/'runtime'/name)
pin=HERE/'runtime/by_sha256'/current_sha;pin.mkdir(parents=True,exist_ok=True)
shutil.copyfile(version/'system_prompt.md',pin/'system_prompt.md')
client=boto3.client('s3',region_name='us-west-2')
manifest=json.loads((HERE/'build_manifest.json').read_text())
paths={HERE/f for f in manifest['artifacts']}
for folder in ['runtime','review_logs','reviewed_outputs','normalized_outputs','validation','records/attempts','records/provider_responses','experiments','inputs','scoring_contract_smoke']:
 paths.update(p for p in (HERE/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ['build_manifest.json','manifest.json','input_projection_manifest.json','reviewed_prompt_cases.json','reviewed_validation.json','independent_review.json','reviewed_independent_check.json','execution_summary.json','status_inventory.json','build_reviewed.py','build_review.py','build_inputs.py','run_gpt55.py','record_integrity.py','review_scoring_policy.json','README.md','publish_review.py']:
 if (HERE/name).exists():paths.add(HERE/name)

def publish(path):
 rel=path.relative_to(HERE).as_posix();body=path.read_bytes();sha=hashlib.sha256(body).hexdigest()
 content={'html':'text/html','js':'application/javascript','json':'application/json','md':'text/markdown','txt':'text/plain','py':'text/plain'}.get(path.suffix[1:],mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
 key=PREFIX+rel;client.put_object(Bucket=BUCKET,Key=key,Body=body,ContentType=content,CacheControl='no-cache',Metadata={'sha256':sha})
 got=client.get_object(Bucket=BUCKET,Key=key)
 if hashlib.sha256(got['Body'].read()).hexdigest()!=sha or got['ContentType']!=content:raise RuntimeError('S3 verification failed '+rel)
 return {'file':rel,'bytes':len(body),'sha256':sha,'content_type':content,'verified':True}
# Upload dependencies before the entry page so the first load is complete.
entry=HERE/'gallery/index.html';rows=[]
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(publish,sorted(paths-{entry})))
rows.append(publish(entry))
report={'status':'published_and_s3_bytes_verified','published_at':datetime.now(timezone.utc).isoformat(),'bucket':BUCKET,'prefix':PREFIX,'gallery_url':f'https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}gallery/index.html','files':rows,'browser_visual_verification':False,'notes':'S3 authenticated bytes and Content-Type verified; corporate browser rendering not tested here.'}
(HERE/'publication.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'gallery_url':report['gallery_url']},indent=2))
