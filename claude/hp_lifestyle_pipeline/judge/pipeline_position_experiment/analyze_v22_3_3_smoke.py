#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment')
ROOT=PROJECT/'smoke/v22_3_3_guard'
BASE=PROJECT/'smoke/baseline'
FORBIDDEN=re.compile(r'LOWER-FILL|\bx\s*[-–]\s*y\b|translat|relocat', re.I)

def sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def metric(g, key):
    v=g.get(key)
    return '' if v is None else (f'{v:.4f}' if isinstance(v,float) else str(v))

def panel(path: Path|None, title: str, size=(520,390)):
    im=Image.new('RGB',(size[0],size[1]+36),'white')
    d=ImageDraw.Draw(im); d.text((8,8),title,fill='black')
    if path and path.exists():
        src=Image.open(path).convert('RGB'); src.thumbnail(size)
        im.paste(src,((size[0]-src.width)//2,36+(size[1]-src.height)//2))
    else: d.text((8,70),'not produced',fill='red')
    return im

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    records=[]; rows=[]; sheets=[]
    for f in manifest['fixtures']:
        slug=f['slug']; rd=ROOT/slug/'run/rows'/slug; base=BASE/f['base_slug']
        result=json.loads((rd/'result.json').read_text())
        attempts=result.get('product_invariant_guard',{}).get('attempts',[])
        stage=result.get('stage_b_attempts',[])
        if len(stage)==2:
            fallback=result.get('fallback_prompt','')
            if FORBIDDEN.search(fallback): raise RuntimeError(f'{slug}: fallback contradiction')
            for name in ('stage_b_attempt_1_request.json','stage_b_attempt_1_response.json',
                         'stage_b_attempt_2_request.json','stage_b_attempt_2_response.json',
                         'image_request_attempt_1.json','image_request_attempt_2.json',
                         'product_invariant_attempt_1.json','product_invariant_attempt_2.json'):
                if not (rd/name).exists(): raise RuntimeError(f'{slug}: missing {name}')
        for i,g in enumerate(attempts,1):
            records.append({'slug':slug,'mode':f['mode'],'attempt':i,'selected':result['product_invariant_guard'].get('selected_attempt')==i,**g})
        a1=attempts[0] if attempts else {}; a2=attempts[1] if len(attempts)>1 else {}
        rows.append([slug,result['status'],str(result.get('image_calls')),str(len(stage)),
                     str(result.get('product_invariant_guard',{}).get('selected_attempt')),
                     metric(a1,'translation_x_px'),metric(a1,'translation_y_px'),metric(a1,'singular_values'),
                     metric(a1,'rotation_deg'),metric(a1,'residual_p95_px'),','.join(a1.get('reasons',[])),
                     metric(a2,'translation_x_px'),metric(a2,'translation_y_px'),metric(a2,'singular_values'),
                     metric(a2,'rotation_deg'),metric(a2,'residual_p95_px'),','.join(a2.get('reasons',[]))])
        pths=[base/'control_guide.png', rd/'gpt_1.png', rd/'gpt_2.png', rd/'ours.png']
        titles=['frozen guide','attempt 1','attempt 2','selected output']
        ps=[panel(p,t) for p,t in zip(pths,titles)]
        sheet=Image.new('RGB',(sum(x.width for x in ps),ps[0].height+54),'white')
        ImageDraw.Draw(sheet).text((8,8),slug,fill='black')
        x=0
        for p in ps: sheet.paste(p,(x,54)); x+=p.width
        sheet.save(ROOT/f'{slug}_contact.jpg',quality=90)
        sheets.append(sheet)
    (ROOT/'affine_metrics.json').write_text(json.dumps(records,indent=2)+'\n')
    headers=['fixture','status','image calls','Stage-B calls','selected','a1 tx','a1 ty','a1 singulars','a1 rot','a1 p95','a1 failures','a2 tx','a2 ty','a2 singulars','a2 rot','a2 p95','a2 failures']
    md=['# V22.3.3 eight-fixture smoke','',f"Pipeline: `{manifest['pipeline_version']}`",'', '| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']
    md += ['| '+' | '.join(r)+' |' for r in rows]
    md += ['', '## Contract checks','', '- Frozen V6.1 product, reference, Stage-A geometry and guide used for every row.', '- HIGH-FILL keeps its initial position policy.', '- LOWER-FILL may use one initial generation plus at most one fresh fixed-position Stage-B rewrite and one fallback image.', '- Every fallback executable was scanned for LOWER-FILL, x-y, translation and relocation language before the second image call.', '- No best-of selection, image retry, mask, resize or post-generation alignment.', '']
    (ROOT/'RESULTS.md').write_text('\n'.join(md))
    w=max(s.width for s in sheets); h=sum(s.height for s in sheets)
    allsheet=Image.new('RGB',(w,h),'white'); y=0
    for s in sheets: allsheet.paste(s,(0,y)); y+=s.height
    allsheet.save(ROOT/'all_fixtures_contact_sheet.jpg',quality=88)
    hashes={p.name:sha(p) for p in sorted(ROOT.glob('*')) if p.is_file()}
    (ROOT/'artifact_sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps({'fixtures':len(rows),'attempt_records':len(records),'contact_sheet':str(ROOT/'all_fixtures_contact_sheet.jpg'),'results':str(ROOT/'RESULTS.md')},indent=2))
if __name__=='__main__': main()
