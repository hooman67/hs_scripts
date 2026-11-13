#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment')
rows=json.loads((ROOT/'affine_guard_calibration.json').read_text())
newp=ROOT/'smoke/v22_3_1_guard/cashmere__laptop_FrontWide__p1__relocation_demand/provenance.json'
new=json.loads(newp.read_text())['product_invariant_guard']['attempts']

def checks(r,p95,fixed):
    matrix=r.get('matrix') or r.get('full_affine_matrix')
    tx,ty=matrix[0][2],matrix[1][2]
    values={
      'verifiable':r.get('verifiable',True),
      'inliers':r.get('inliers',0)>=20,
      'inlier_ratio':r.get('inlier_ratio',0)>=.55,
      'singular_min':r.get('singular_min',r.get('singular_values',[0,0])[-1])>=.98,
      'singular_max':r.get('singular_max',r.get('singular_values',[0,0])[0])<=1.02,
      'anisotropy':r.get('anisotropy_ratio',999)<=1.02,
      'rotation':abs(r.get('rotation_deg',999))<=1,
      'shear':r.get('column_shear_cos',999)<=.02,
      'residual_median':r.get('residual_median_px',999)<=1.5,
      'residual_p95':r.get('residual_p95_px',999)<=p95,
      'span_x':r.get('source_span_x_fraction',0)>=.45,
      'span_y':r.get('source_span_y_fraction',0)>=.40,
      'quadrants':r.get('source_quadrants',0)>=3,
      'hull':r.get('source_hull_fraction',0)>=.12,
      'corners':r.get('corners_in_frame',False),
    }
    if fixed:
      values['fixed_translation_x']=abs(tx)<=8
      values['fixed_translation_y']=abs(ty)<=8
    return values

def label_ok(label,pred):
    expected = label=='accepted'
    return pred==expected

records=[]
for r in rows:
  fixed='FrontCloseUp' in r['slug']
  rec={'set':'calibration','version':r['version'],'slug':r['slug'],'label':r['evidence_label'],
       'p95':r.get('residual_p95_px'),'fixed_position':fixed,'outcomes':{}}
  for p in (3.2,3.5,4.0):
    c=checks(r,p,fixed);rec['outcomes'][str(p)]={'pass':all(c.values()),'failed':[k for k,v in c.items() if not v]}
  records.append(rec)
for i,r in enumerate(new,1):
  fixed=i==2
  rec={'set':'new_v22_3_1','version':'v22_3_1','slug':f'cashmere__laptop_FrontWide__p1__relocation_demand__attempt{i}',
       'label':'unlabeled_new_attempt','p95':r.get('residual_p95_px'),'fixed_position':fixed,'outcomes':{}}
  for p in (3.2,3.5,4.0):
    c=checks(r,p,fixed);rec['outcomes'][str(p)]={'pass':all(c.values()),'failed':[k for k,v in c.items() if not v]}
  records.append(rec)
(ROOT/'residual_p95_sensitivity.json').write_text(json.dumps(records,indent=2)+'\n')
lines=['# Residual-p95 threshold sensitivity','',
 'Predeclared comparison of 3.2, 3.5, and 4.0 px. Every other frozen full-affine threshold remains unchanged. HIGH-FILL calibration rows and fixed-position fallback attempts also retain the ±8 px x/y translation gate.','',
 '| Threshold | Calibration accepted passed | Calibration rejected rejected | False rejects | False accepts | New attempt 1 | New fixed fallback |',
 '|---:|---:|---:|---:|---:|---|---|']
for p in ('3.2','3.5','4.0'):
 cal=[r for r in records if r['set']=='calibration']; acc=[r for r in cal if r['label']=='accepted']; rej=[r for r in cal if r['label']!='accepted']
 ap=sum(r['outcomes'][p]['pass'] for r in acc); rr=sum(not r['outcomes'][p]['pass'] for r in rej)
 fr=[r['slug'] for r in acc if not r['outcomes'][p]['pass']];fa=[r['slug'] for r in rej if r['outcomes'][p]['pass']]
 n1=records[-2]['outcomes'][p];n2=records[-1]['outcomes'][p]
 fmt=lambda n: 'PASS' if n['pass'] else 'FAIL ('+', '.join(n['failed'])+')'
 lines.append(f"| {p} | {ap}/{len(acc)} | {rr}/{len(rej)} | {len(fr)} | {len(fa)} | {fmt(n1)} | {fmt(n2)} |")
lines += ['','## Row-level calibration outcomes','', '| Label | Version | Row | p95 px | 3.2 | 3.5 | 4.0 |','|---|---|---|---:|---|---|---|']
for r in records:
 def short(p):
  x=r['outcomes'][p]; return 'PASS' if x['pass'] else 'FAIL: '+', '.join(x['failed'])
 lines.append(f"| {r['label']} | {r['version']} | `{r['slug']}` | {r['p95']:.3f} | {short('3.2')} | {short('3.5')} | {short('4.0')} |")
(ROOT/'RESIDUAL_P95_SENSITIVITY.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[:12]))
