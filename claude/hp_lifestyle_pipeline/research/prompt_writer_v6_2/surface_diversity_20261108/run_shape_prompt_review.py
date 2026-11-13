#!/usr/bin/env python3
"""Astra product-prompt review; preserves every submitted and returned byte."""
import ast
import datetime as dt
import json
import subprocess
from pathlib import Path
import foundry_aws_gateway.llm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'shape_prompt_review'
OUT.mkdir(exist_ok=False)
BASE = '8c358bc7989cb0e137e89db0fd325168249e2a22'
REPO = '/home/colligo/foundry-pr4349-position-exp'
def source(name):
    return subprocess.check_output(['git', '-C', REPO, 'show', BASE + ':experimental/adarabi/hp-3p-gpt25/hp3p/' + name], text=True)
pipe = source('pipeline.py')
system = source('prompts/system_3p.txt')
context = '''You are reviewing product LLM integration prompts for Adobe HP scene image generation. Return product-system-prompt text, not application code. Hooman requires Astra high effort for creative prompt revisions.

The V6.2 lifestyle writer emits 160 scene prompts (4devices x4views x10). Laptop cafes should use round tables; other plausible laptop scenes should vary support shape. Printers should use credible substantial cabinets, low credenzas, fitted counters or dedicated equipment tables, with standing access, not a person's occupied desk. Writer retains rich CTech style, varied props, populated shelves, coherent walls, camera-aware density and source-first ranking.

Observed root cause: despite original prompts asking round tables (8/10 laptop Café,11/80 laptop all), Stage A has only rectangular geometry, and Stage B strictly overrules them: 'requested round table conflicts ... use exact square tabletop'. All80 printer writer inputs previously tables. We are preparing a SMALL isolated support-shape/category correction, pending user approval to depart from earlier same-pipeline constraint. Do not relax fixed product orientation OR position OR size. The paused x-y movement experiment is separate and excluded. Do not change model, blue policy, input references, room/object policy, aesthetics or camera contract.

New geometry field support_top_shape enum rectangular/round/oval. Rectangle keeps old geometry. For round, support_width_m and support_depth_m are equal diameters; oval they are unequal diameters. Code draws projected ellipse in same support plane and camera. Product footprint and original pixel bounds remain fixed. It validates ALL four base corners inside ellipse; choose physically normal dimensions and modest offset/gap. user_edge_gap_m is measured at user-facing rim point aligned with product center, not some new straight side. Product lateral offset must leave width/curve clearance. No arbitrary camera widening/full circle/base display demands; fixed crop can show an arc only. Cabinet/credenza/fitted-counter category comes from original prompt, not shape field: normally rectangular TOP but actual cabinet body remains category described. Stage B sees actual outline and must describe shape accurately, not default all boundaries to straight edges/four corners. Rectangular printer supports usually near wall; round/oval laptop tables often freestanding. Keep user side and operating access, shared perspective, no extra people/devices, original rule product pixels unchanged.

Task: return JSON ONLY with:
1. geometry_section: full revised '# Geometry and user-side layout' section (up to before '# Blue'), minimal changes retaining all existing requirements, add explicit shape handling.
2. constant_replacements: object mapping each of _GEOMETRY_ONLY, _PRIORITY, _WRITE_OVERRIDE, _PRINTER_WALL, _WRITE_PRINTER_WALL, _LEGEND, _FINAL_CHECK to a COMPLETE replacement prose string. No Python source. Treat _GEOMETRY_ONLY as full evaluated text including printer wall phrase, not a concatenation expression. Keep original intent and other constraints. Minimize deltas.
3. change_notes: concise array of exact necessary differences and unresolved limitations. Do not claim code deployed or images tested.

Below are pinned policy sources, used as product prompt text context only.
'''
context += '\nFULL SYSTEM TEXT:\n' + system + '\nCURRENT PIPELINE PROMPT CONSTANTS:\n' + pipe[:pipe.index('_STALE_IMAGE =')]
(OUT/'request.md').write_text(context)
started = dt.datetime.now(dt.timezone.utc).isoformat()
try:
    client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=8, timeout=600)
    r = client.chat.completions.create(model='gpt-6-astra', reasoning_effort='high', max_completion_tokens=18000, messages=[{'role':'user','content':context}], response_format={'type':'json_object'})
    answer = r.choices[0].message.content or ''
    (OUT/'response.json').write_text(answer)
    (OUT/'metadata.json').write_text(json.dumps({'model':r.model,'finish_reason':r.choices[0].finish_reason,'started':started,'finished':dt.datetime.now(dt.timezone.utc).isoformat(),'usage':r.usage.model_dump()},indent=2))
    assert r.choices[0].finish_reason == 'stop' and answer
    json.loads(answer)
    print('ASTRA_SHAPE_POLICY_REVIEW_COMPLETE', flush=True)
except Exception as e:
    (OUT/'error.json').write_text(json.dumps({'type':type(e).__name__,'status_code':getattr(e,'status_code',None),'started':started}))
    raise SystemExit(type(e).__name__)
