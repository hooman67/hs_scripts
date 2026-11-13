"""Scoped snapshot/publish/readback. Caller must hold the shared gallery flock throughout."""
import argparse
import concurrent.futures
import hashlib
import json
import mimetypes
from pathlib import Path
import boto3

RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
AUDIT=RUN/'_review/recipe_publication_2026-10-20'
BUCKET='foundry-tccc-enterprise-adobe-assets'
PREFIX='mixology/refraction_research_2026-10-19/'
ALLOWED_EXISTING={'gallery/index.html','gallery/data.js','gallery/style.css','gallery/main.js','prompt_package/scripts/build_gallery.py','prompt_package/scripts/validate_gallery.py'}


def sha(data):return hashlib.sha256(data).hexdigest()


def eligible(path):return '_review' not in path.parts and '_archive' not in path.parts and '__pycache__' not in path.parts and path.suffix not in ['.lock','.tmp']


def snapshot(s3):
    AUDIT.mkdir(parents=True,exist_ok=False)
    names=[]
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET,Prefix=PREFIX):
        names.extend(x['Key'][len(PREFIX):] for x in page.get('Contents',[]) if eligible(Path(x['Key'])))
    def one(name):
        obj=s3.get_object(Bucket=BUCKET,Key=PREFIX+name);body=obj['Body'].read()
        local=RUN/name
        assert local.exists() and sha(local.read_bytes())==sha(body),f'Live/local mismatch before recipe merge: {name}'
        if name.startswith('gallery/') or name=='prompt_package/scripts/build_gallery.py':
            p=AUDIT/'before'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
        return {'path':name,'sha256':sha(body),'bytes':len(body),'content_type':obj['ContentType']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:records=list(pool.map(one,names))
    (AUDIT/'before_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({'snapshot_verified':True,'objects':len(records),'bytes':sum(r['bytes'] for r in records)}))


def publish(s3):
    baseline=json.loads((AUDIT/'before_manifest.json').read_text());known={r['path']:r for r in baseline}
    changes=[]
    # Include only this branch and explicit shared gallery files; never publish a peer's in-flight artifacts.
    paths=[p for p in (RUN/'recipe-to-image').rglob('*') if p.is_file() and eligible(p)]
    paths += [RUN/name for name in ALLOWED_EXISTING]
    for name,row in known.items():
        path=RUN/name
        assert path.exists(),f'Baseline file removed: {name}'
        changed=sha(path.read_bytes())!=row['sha256']
        if changed:assert name in ALLOWED_EXISTING,f'Unrelated baseline mutation: {name}'
    for path in paths:
        name=str(path.relative_to(RUN));body=path.read_bytes()
        if name in known and sha(body)==known[name]['sha256']:continue
        mime={'.js':'application/javascript','.css':'text/css','.html':'text/html','.md':'text/plain','.txt':'text/plain','.json':'application/json','.py':'text/plain'}.get(path.suffix,mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        changes.append((name,body,mime))
    # Dependencies first, gallery HTML last.
    changes.sort(key=lambda x:(x[0]=='gallery/index.html',x[0].startswith('gallery/'),x[0]))
    for name,body,mime in changes:s3.put_object(Bucket=BUCKET,Key=PREFIX+name,Body=body,ContentType=mime)
    expected={**known,**{name:{'path':name,'sha256':sha(body),'bytes':len(body),'content_type':mime} for name,body,mime in changes}}
    def check(row):
        obj=s3.get_object(Bucket=BUCKET,Key=PREFIX+row['path']);body=obj['Body'].read()
        assert sha(body)==row['sha256'],row['path']
        assert obj['ContentType'].split(';')[0]==row['content_type'].split(';')[0],row['path']
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:verified=list(pool.map(check,expected.values()))
    result={'verified':True,'bucket':BUCKET,'prefix':PREFIX,'changed_or_new_files':[n for n,_,_ in changes],
            'baseline_objects_preserved':len(known),'verified_objects':len(verified),'verified_bytes':sum(r['bytes'] for r in verified),'files':verified,
            'url':'https://foundry-aws-corp.adobe.io/asset/'+BUCKET+'/'+PREFIX+'gallery/index.html#recipe-to-image',
            'live_signed_in_gateway_browser':'Not verified from this Pluto job; authenticated S3 bytes and local mocked-IMS browser are separate checks.'}
    (AUDIT/'publication.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['files','changed_or_new_files']}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['snapshot','publish']);args=p.parse_args()
    client=boto3.client('s3',region_name='us-west-2')
    (snapshot if args.mode=='snapshot' else publish)(client)
