# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Image+twin placement judge. Does not generate images or repair judgments."""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, mimetypes, time
from datetime import datetime, timezone
from pathlib import Path
from scoring import aggregate_observation as aggregate, validate_runtime_input, OBSERVATION_SCHEMA

ROOT = Path(__file__).resolve().parent

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def client():
    probe = ROOT.parents[1] / 'research/source_messaging_v1_to_v6/scripts/probe_gpt55.py'
    spec = importlib.util.spec_from_file_location('placement_auth', probe)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    c, mode = module.client_and_auth_mode()
    return c.with_options(timeout=180, max_retries=0), mode

def wire_schema(value):
    # Local semantic validation retains constraints unsupported by some deployments.
    if isinstance(value, dict): return {k:wire_schema(v) for k,v in value.items() if k not in ('$schema','uniqueItems','minLength')}
    if isinstance(value, list): return [wire_schema(v) for v in value]
    return value

def judge(runtime_input, output_dir, model='gpt-5.5', visual_anchors=False):
    validate_runtime_input(runtime_input)
    output_dir=Path(output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    system=(ROOT/'system_prompt.md').read_text()
    files={k:{'path':str(Path(runtime_input[k]).resolve()),'sha256':sha256(runtime_input[k])} for k in ('generated_image','twin_image')}
    record={'started_at':datetime.now(timezone.utc).isoformat(),'input':runtime_input,'images':files,
            'model_requested':model,'reasoning_effort':'high','max_completion_tokens':12000,
            'system_prompt_sha256':sha256(ROOT/'system_prompt.md'),'schema_sha256':sha256(ROOT/'observation_schema.json'),
            'scoring_sha256':sha256(ROOT/'scoring.py'),'image_detail':'high','image_transform':'none; original bytes'}
    if visual_anchors:
        record['visual_anchors']=json.loads((ROOT/'data/visual_anchors.json').read_text())
        for anchor in record['visual_anchors']['examples']:
            if sha256(anchor['local_path'])!=anchor['sha256']: raise ValueError('Anchor bytes differ from frozen manifest')
    fingerprint=hashlib.sha256(json.dumps({k:v for k,v in record.items() if k!='started_at'},sort_keys=True).encode()).hexdigest()
    record['fingerprint']=fingerprint
    result_path=output_dir/'result.json'
    if result_path.exists():
        old=json.loads(result_path.read_text())
        if old.get('fingerprint')==fingerprint and old.get('ok'): return old
        raise RuntimeError('Output exists for failed or different request; use a new output directory')
    (output_dir/'request.json').write_text(json.dumps(record,indent=2)+'\n')
    (output_dir/'system_prompt.md').write_text(system)
    (output_dir/'observation_schema.json').write_text(json.dumps(OBSERVATION_SCHEMA,indent=2)+'\n')
    content=[{'type':'text','text':json.dumps({'product_type':runtime_input['product_type'],'scene_prompt':runtime_input['scene_prompt'],'image_stage':runtime_input['image_stage']})}]
    for label,key in [('A — scene-generation image to evaluate','generated_image'),('B — original digital-twin render for reference','twin_image')]:
        p=Path(runtime_input[key]);mime=mimetypes.guess_type(p.name)[0]
        if mime not in ('image/png','image/jpeg','image/webp'): raise ValueError('Unsupported image format')
        content += [{'type':'text','text':label},{'type':'image_url','image_url':{'url':f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode(),'detail':'high'}}]
    messages=[{'role':'system','content':system}]
    if visual_anchors:
        anchor_content=[{'type':'text','text':'Fixed visual rubric examples from DEVELOPMENT data follow. Learn their standard without assuming the target image has the same defects. Reference photos illustrate only visible relationships, not guaranteed perfect overall scores.'}]
        for anchor in record['visual_anchors']['examples']:
            p=Path(anchor['local_path']);mime=mimetypes.guess_type(p.name)[0]
            anchor_content += [{'type':'text','text':anchor['guidance']},{'type':'image_url','image_url':{'url':f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode(),'detail':'high'}}]
        messages.extend([{'role':'user','content':anchor_content},{'role':'assistant','content':'I will apply these placement standards and assess the next target independently from its own visible evidence.'}])
    messages.append({'role':'user','content':content})
    started=time.monotonic(); record['attempts']=[]
    try:
        c,mode=client();record['auth_mode']=mode
        for attempt in range(1,4):
            try:
                response=c.chat.completions.create(model=model,reasoning_effort='high',max_completion_tokens=12000,
                    messages=messages,
                    response_format={'type':'json_schema','json_schema':{'name':'placement_observation','strict':True,'schema':wire_schema(OBSERVATION_SCHEMA)}})
                record['attempts'].append({'attempt':attempt,'status':'ok'});break
            except Exception as e:
                status=getattr(e,'status_code',None);record['attempts'].append({'attempt':attempt,'error_type':type(e).__name__,'status':status})
                if attempt==3 or status not in (429,500,502,503,504): raise
                delay=min(60,5*2**(attempt-1))
                try: delay=min(60,max(delay,float(e.response.headers.get('retry-after',0))))
                except (ValueError,AttributeError):pass
                time.sleep(delay)
        raw=response.model_dump(mode='json');(output_dir/'response.json').write_text(json.dumps(raw,indent=2)+'\n')
        if not (response.model==model or response.model.startswith(model+'-')):raise RuntimeError('Unexpected model returned')
        choice=response.choices[0]
        if choice.finish_reason!='stop' or choice.message.refusal:raise RuntimeError('Incomplete/refused judgment')
        observations=json.loads(choice.message.content)
        record.update(ok=True,model_returned=response.model,usage=raw.get('usage'),judgment=aggregate(observations))
    except Exception as e:
        record.update(ok=False,error_type=type(e).__name__,status_code=getattr(e,'status_code',None))
        # Persist validation diagnostics, never exception strings containing API/HTTP details.
        if hasattr(e,'errors'): record['validation_errors']=list(e.errors)
    record['elapsed_seconds']=round(time.monotonic()-started,2)
    result_path.write_text(json.dumps(record,indent=2)+'\n');return record

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--model',default='gpt-5.5');p.add_argument('--visual-anchors',action='store_true');a=p.parse_args()
    result=judge(json.loads(Path(a.input).read_text()),a.output,a.model,a.visual_anchors)
    print(json.dumps({k:result.get(k) for k in ('ok','model_returned','elapsed_seconds','error_type','validation_errors')}))
    return 0 if result['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
