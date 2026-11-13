"""Astra rewriter/critic with the unchanged bundled imagegen CLI for every image edit."""
from __future__ import annotations
import argparse
import base64
import concurrent.futures
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from foundry_aws_gateway import llm
from PIL import Image

PROJECT=Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
CLI=Path('/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py')
USER='Add refractions.'
JUDGE='''You are evaluating image edits for a beverage-art-direction research experiment. Judge the output against the original edit target for drink identity and against the positive examples only for lighting STYLE. Positive examples may have different crops or drinks: do not require copying their ingredients or composition. The negative example was rejected by the user for vein-like caustics. The desired effect is broad colored transmitted light containing bright irregular branching optical ridges with dominant concentrations, finer tapering forks, and natural unevenness, grounded on a receiving surface. Generic glow, uniform veins, decorative lightning, repetitive nets, and glitter do not satisfy it. Assess only what you can actually see. Separate crop changes from ingredient changes. Modest reframing can be evaluated separately; do not silently call it exact preservation. Return JSON with refraction_score (0-5), identity_score (0-5), composition_score (0-5), coherent_light_score (0-5), vein_like (boolean), dominant_failure, observations (list), successful_features (list), next_smallest_change, and verdict ("promising", "mixed", or "poor"). Explain concrete visible evidence, not praise. Scores are advisory, not a customer verdict.'''


def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data): Path(p).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def utc(): return datetime.now(timezone.utc).isoformat()
def picture(path):
    path=Path(path);mime='image/png' if path.suffix.lower()=='.png' else 'image/jpeg'
    return {'type':'input_image','image_url':f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()}
def role_image(label,path): return [{'type':'input_text','text':label},picture(path)]
def client(): return llm.get_openai().with_options(timeout=180,max_retries=1)


def generate(case_id,version,style_files,system_version=None,user_prompt=USER):
    case=json.loads((PROJECT/'cases.json').read_text())[case_id]
    out=RUN/'runs'/f'{version}_{case_id}'
    out.mkdir(parents=True,exist_ok=True)
    record_path=out/'record.json'
    if record_path.exists():
        old=json.loads(record_path.read_text())
        if old.get('status')=='complete':
            print(f'SKIP complete {out.name}',flush=True);return
        if (out/'output.png').exists():
            raise RuntimeError(f'Existing output requires review before retry: {out}')
    if case.get('deprecated'):
        raise ValueError(f'Case {case_id} is historical-only; use {case["replacement_case"]} for new generation.')
    target=RUN/'assets'/case['input']
    start=time.monotonic()
    record={'id':out.name,'version':version,'case_id':case_id,'case':case,'started_at':utc(),
        'user_prompt':user_prompt,'system_version':system_version or version,'rewriter_model':None if version=='baseline' else 'gpt-6-astra',
        'image_model':'gpt-image-2.5-sunburst','quality':'high','size_requested':'auto',
        'input_images':[{'path':str(target),'role':'edit target','sha256':digest(target)}],
        'status':'started','cli_sha256':digest(CLI)}
    save(record_path,record)
    try:
        if version=='baseline':
            prompt=(RUN/'pdf_context'/'customer_page5_prompt.txt').read_text().strip()
            system='No GPT rewriter used. Verbatim image prompt from customer PDF page 5 is sent directly to Sunburst.'
            record['user_prompt']='Customer PDF page 5 verbatim prompt (baseline comparator)'
        else:
            system=(PROJECT/'prompts'/f'system_{system_version or version}.md').read_text()
            content=[{'type':'input_text','text':user_prompt}]+role_image('Image 1 — edit target, authoritative for drink identity and composition.',target)
            for n,style in enumerate(style_files,start=2):
                p=RUN/'assets'/style
                content+=role_image(f'Image {n} — lighting style reference ONLY, not a replacement for Image 1. This image will also be sent to the image editor.',p)
                record['input_images'].append({'path':str(p),'role':'lighting style reference','sha256':digest(p)})
            reply=client().responses.create(model='gpt-6-astra',reasoning={'effort':'medium'},max_output_tokens=3000,
                instructions=system,input=[{'role':'user','content':content}])
            prompt=reply.output_text.strip()
            if reply.status!='completed' or not prompt: raise RuntimeError('Rewriter did not complete')
            record['rewriter']={'returned_model':reply.model,'request_id':reply._request_id,
                'response_id':reply.id,'usage':reply.usage.model_dump(mode='json') if reply.usage else None,
                'reasoning_effort':'medium','max_output_tokens':3000}
        (out/'system_prompt.md').write_text(system)
        (out/'user_prompt.txt').write_text(record['user_prompt']+'\n')
        (out/'image_prompt.txt').write_text(prompt+'\n')
        record['system_prompt']=system;record['image_prompt']=prompt
        record['status']='image_running';save(record_path,record)
        print(f'IMAGE {out.name}: rewriter ready, {len(prompt.split())} words',flush=True)
        c=llm.get_openai();env=os.environ.copy()
        env['OPENAI_API_KEY']=c.api_key;env['OPENAI_PROJECT_ID']=c.project;env['OPENAI_BASE_URL']=str(c.base_url)
        args=[sys.executable,str(CLI),'edit','--model','gpt-image-2.5-sunburst']
        for im in record['input_images']: args+=['--image',im['path']]
        args+=['--prompt-file',str(out/'image_prompt.txt'),'--quality','high','--size','auto',
            '--output-format','png','--out',str(out/'output.png'),'--no-augment']
        before=time.monotonic()
        process=subprocess.run(args,env=env,capture_output=True,text=True,timeout=480)
        log=(process.stdout+'\n'+process.stderr).replace(c.api_key,'[REDACTED]')
        (out/'image_cli.log').write_text(log)
        record['cli_returncode']=process.returncode;record['image_seconds']=round(time.monotonic()-before,2)
        if process.returncode: raise RuntimeError('Image CLI failed; see sanitized log')
        with Image.open(out/'output.png') as image:
            image.load();record['output_dimensions']=list(image.size);record['output_mode']=image.mode
        record.update(status='complete',output=str(out/'output.png'),output_sha256=digest(out/'output.png'),
                      completed_at=utc(),total_seconds=round(time.monotonic()-start,2))
        save(record_path,record)
        print(f'DONE {out.name}: {record["output_dimensions"]}, {record["image_seconds"]}s',flush=True)
    except Exception as exc:
        record.update(status='failed',error_type=type(exc).__name__,error_status=getattr(exc,'status_code',None))
        save(record_path,record)
        print(f'FAILED {out.name}: {type(exc).__name__}',flush=True)
        raise


def judge(run_id):
    folder=RUN/'runs'/run_id
    if (folder/'judge.json').exists():
        print('SKIP judged '+run_id,flush=True);return
    r=json.loads((folder/'record.json').read_text())
    if r['status']!='complete': return
    source=Path(r['input_images'][0]['path']);positive=RUN/'assets'/r['case']['positive']
    negative=RUN/'assets'/'image_015_p06_xref590.jpg'
    content=[{'type':'input_text','text':'Evaluate the candidate and return JSON according to the requested scoring fields.'}]
    content+=role_image('A: original edit target. Preserve drink identity from this image.',source)
    content+=role_image('B: candidate output to judge.',folder/'output.png')
    content+=role_image('C: user-approved lighting STYLE reference. '+r['case']['pair_status'],positive)
    content+=role_image('D: user-rejected vein-like lighting example. This is a different image, shown only to calibrate pattern rejection.',negative)
    if r['case_id']=='single':
        content+=role_image('E: strongest user-approved group example; judge only optical pattern hierarchy, not drink contents.',RUN/'assets'/'image_027_p10_xref1385.jpg')
    response=client().responses.create(model='gpt-6-astra',instructions=JUDGE,
        input=[{'role':'user','content':content}],reasoning={'effort':'medium'},
        text={'format':{'type':'json_object'}},max_output_tokens=3500)
    parsed=json.loads(response.output_text)
    parsed['_meta']={'model':response.model,'request_id':response._request_id,'time':utc(),
                     'usage':response.usage.model_dump(mode='json') if response.usage else None,
                     'system_prompt':JUDGE,'image_roles':[c['text'] for c in content if c['type']=='input_text']}
    save(folder/'judge.json',parsed)
    print(json.dumps({'run':run_id,**{k:parsed.get(k) for k in ['refraction_score','identity_score','composition_score','vein_like','dominant_failure','next_smallest_change','verdict']}}),flush=True)


def main():
    os.umask(0o077);logging.disable(logging.CRITICAL)
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    g=sub.add_parser('generate');g.add_argument('--version',required=True);g.add_argument('--cases',nargs='+',required=True)
    g.add_argument('--style',nargs='*',default=[]);g.add_argument('--workers',type=int,default=2)
    g.add_argument('--system-version');g.add_argument('--user-prompt',default=USER)
    j=sub.add_parser('judge');j.add_argument('run_ids',nargs='+');j.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures=([pool.submit(generate,c,a.version,a.style,a.system_version,a.user_prompt) for c in a.cases] if a.command=='generate'
                 else [pool.submit(judge,r) for r in a.run_ids])
        for future in concurrent.futures.as_completed(futures): future.result()


if __name__=='__main__':main()
