#!/usr/bin/env python3
from __future__ import annotations
import base64,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import foundry_aws_gateway.llm

HERE=Path(__file__).resolve().parent
TASK=HERE/'astra_task.md'
EXACT=HERE/'evidence/exact_7_predictions.json'
PRIOR=HERE/'evidence/prior_v6_anchor_candidates.json'
SHEETS=HERE/'evidence/contact_sheet_manifest.json'
V41=HERE.parent.parent/'v4_1'
CURRENT={'system_prompt':V41/'system_prompt.md','assessment_schema':V41/'assessment_schema.json','scoring':V41/'scoring.py','anchor_catalog':V41/'anchored_candidate/anchor_catalog.json'}
MANIFEST=HERE/'request_manifest.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,v):
 t=p.with_suffix('.tmp'); t.write_text(json.dumps(v,indent=2)+'\n'); t.replace(p)

def main():
 sheet_manifest=json.loads(SHEETS.read_text())
 if sheet_manifest['pair_count']!=7 or sheet_manifest['sheet_count']>3 or not sheet_manifest['all_pairs_covered_once']: raise RuntimeError('bad contact sheet coverage')
 sections=[TASK.read_text()]
 sections += [f"\n\n## EXACT CURRENT {name.upper()}\n\n```\n{path.read_text()}\n```" for name,path in CURRENT.items()]
 sections += [f"\n\n## EXACT SEVEN FAILED-GATE PREDICTIONS AND HUMAN EVIDENCE\n\n```json\n{EXACT.read_text()}\n```",f"\n\n## VERIFIED PRIOR-V6 ANCHOR CANDIDATES\n\n```json\n{PRIOR.read_text()}\n```"]
 content=[{'type':'text','text':'\n'.join(sections)}]
 image_entries=[]
 for i,s in enumerate(sheet_manifest['sheets'],1):
  p=Path(s['path']); data='data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
  content += [{'type':'text','text':f"CONTACT SHEET {i}: generated scene left, original twin right. IDs: {', '.join(s['record_ids'])}"},{'type':'image_url','image_url':{'url':data,'detail':'high'}}]
  image_entries.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'record_ids':s['record_ids']})
 manifest={'schema_version':'placement-v4.2-astra-redesign-request-v1','created_at_utc':datetime.now(timezone.utc).isoformat(),'route':'foundry_aws_gateway.llm.get_openai direct OpenAI','model_requested':'gpt-6-astra','reasoning_effort':'medium','max_completion_tokens':24000,'max_retries':2,'timeout_seconds':600,'concurrency':1,'task':{'path':str(TASK),'sha256':sha(TASK)},'exact_predictions':{'path':str(EXACT),'sha256':sha(EXACT)},'prior_v6_candidates':{'path':str(PRIOR),'sha256':sha(PRIOR)},'contact_sheet_manifest':{'path':str(SHEETS),'sha256':sha(SHEETS)},'current_artifacts':{k:{'path':str(p),'sha256':sha(p)} for k,p in CURRENT.items()},'images':image_entries,'credentials_recorded':False}
 atomic(MANIFEST,manifest)
 client=foundry_aws_gateway.llm.get_openai().with_options(max_retries=2,timeout=600.0)
 response=client.chat.completions.create(model='gpt-6-astra',messages=[{'role':'user','content':content}],reasoning_effort='medium',max_completion_tokens=24000)
 choice=response.choices[0]; answer=choice.message.content or ''; print(answer); print(json.dumps({'model':response.model,'finish_reason':choice.finish_reason,'total_tokens':getattr(response.usage,'total_tokens',None)}),file=sys.stderr)
 if not answer.strip() or choice.finish_reason!='stop': raise RuntimeError(f'incomplete Astra answer finish={choice.finish_reason}')
 return 0
if __name__=='__main__': raise SystemExit(main())
