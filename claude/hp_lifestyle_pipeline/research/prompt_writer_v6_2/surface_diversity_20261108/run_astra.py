#!/usr/bin/env python3
"""Bounded product prompt-design review through the approved Direct OpenAI route."""
import datetime as dt
import json
import os
import argparse
from pathlib import Path
import foundry_aws_gateway.llm

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--attempt', default='r2')
args = parser.parse_args()
out_dir = ROOT / args.attempt
out_dir.mkdir(exist_ok=False)
task = (ROOT / 'astra_brief.md').read_text()
task += '\n\n## Current complete system prompt\n\n' + (PROJECT / 'research/source_messaging_v1_to_v6/versions/v6_2/system_prompt.md').read_text()
source = PROJECT / 'eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/prompts_all_160.json'
rows = json.loads(source.read_text())['prompts']
task += '\n\n## Representative frozen scenes\n\n' + json.dumps([{'id': x['prompt_key'], 'environment': x['environment'], 'text': x['text']} for x in rows if x['camera_tag'] in ['laptop_FrontWide','printer_FrontWide'] and x['device_id'] in ['cashmere','magic']], ensure_ascii=False, indent=2)
(out_dir / 'astra_request.md').write_text(task)
started = dt.datetime.now(dt.timezone.utc).isoformat()
client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600)
try:
    r = client.chat.completions.create(model='gpt-6-astra', reasoning_effort='high', max_completion_tokens=24000, messages=[{'role':'user','content':task}])
    (out_dir / 'astra_response.md').write_text(r.choices[0].message.content or '')
    meta = {'started':started, 'finished':dt.datetime.now(dt.timezone.utc).isoformat(), 'model':r.model, 'finish_reason':r.choices[0].finish_reason,'usage':r.usage.model_dump()}
    (out_dir / 'astra_metadata.json').write_text(json.dumps(meta,indent=2))
    if r.choices[0].finish_reason != 'stop' or not r.choices[0].message.content:
        raise RuntimeError('incomplete_astra_response')
    print('ASTRA_REVIEW_COMPLETE', flush=True)
except Exception as e:
    (out_dir / 'astra_error.json').write_text(json.dumps({'started':started,'error_type':type(e).__name__,'status_code':getattr(e,'status_code',None)}))
    raise SystemExit(type(e).__name__)
