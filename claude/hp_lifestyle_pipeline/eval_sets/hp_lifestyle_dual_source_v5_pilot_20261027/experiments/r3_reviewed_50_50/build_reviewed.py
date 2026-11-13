#!/usr/bin/env python3
"""Replay explicit root review edits separately from raw/normalized GPT outputs."""
import copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
VERSION=HERE.parents[1]/'research/source_messaging/versions/v5'
sys.path.insert(0,str(VERSION/'scripts'))
from finalize_output import finalize_output
from validate_output import validate_output
from camera_profile_resolver import load_registry

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def put(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
assert sha(HERE/'manifest.json')=='8ff485ef7078c6cb9ec950885bbdc0c1bd50a0ca4933fefca4d541c8857e3c8c', 'review patches are pinned to r3'
manifest=json.loads((HERE/'manifest.json').read_text());registry=load_registry(VERSION/'camera_profiles.json');schema=json.loads((VERSION/'output.schema.json').read_text())
cases={};outputs={};originals={};logs=[];audits={}
for c in manifest['cases']:
 cid=c['case_id'];a=json.loads((HERE/'validation'/f'{cid}.json').read_text());path=Path(a['normalized_output_path']);o=json.loads(path.read_text());assert sha(path)==a['normalized_output_file_sha256'];assert sha(Path(a['record_path']))==a['raw_record_sha256'];outputs[cid]=copy.deepcopy(o);originals[cid]=copy.deepcopy(o);audits[cid]=a;cases[cid]=c

def cid(pair,wide=False):
 typ='laptop' if pair in ('cashmere','elitebook') else 'printer'
 return f'{pair}__{typ}_FrontRight'+('Wide' if wide else 'CloseUp')
def p(pair,n,wide=False):return outputs[cid(pair,wide)]['prompts'][n-1]
def edit(pair,n,old,new,wide=False,reason='Camera-feasibility correction: preserve C-Tech style while removing excess scene demands.'):
 c=p(pair,n,wide);assert old in c['text'],(pair,n,old);c['text']=c['text'].replace(old,new)
 c['camera_omissions'].append(reason)
def sig(pair,n,wide=False,**kw):p(pair,n,wide)['visual_signature'].update(kw)
def ctech(pair,n,wide=False,reason='Same-category adaptation includes wording, light, material or objects beyond deletion/grammar of the cited reference.'):
 c=p(pair,n,wide);c['ctech_relationship']='close_adaptation';c['ctech_reference_score']=min(78,c['ctech_reference_score']);c['ctech_explanation']=reason;c['ctech_changes'].append('Root review: '+reason)
def score(pair,n,values,wide=False,why='Root review credits only the setting, broad activity/materials and context visible in this final scene.'):
 c=p(pair,n,wide)
 for doc in ('smart_brief','source_messaging'):c['score_components'][doc]=dict(zip(('setting','activity','materials','use_context'),values))
 c['explanation']=why

# Precisely scoped camera/ordinary-language edits, addressed using original normalized IDs.
edit('cashmere',4,'with clean shelving and plants creating','with plants creating',True);sig('cashmere',4,True,background_details=['multiple workstations','plants'])
edit('cashmere',7,'simple furniture, a notebook, briefing papers, and a pen on a wooden desk','a wooden desk holding a notebook, briefing papers, and a pen',True)
for pair in ('cashmere','elitebook','deskjet_2955'):
 edit(pair,20,' positioned against a textured wall','',True)
edit('deskjet_2955',1,'simple furniture, a return label, form, and stack of papers','a simple desk holding a return label, form, and stack of papers',True);sig('deskjet_2955',1,True,surface='simple desk',background_details=[])
edit('deskjet_2955',5,'simple furniture, a recipe, visual planning page, and pen','a simple desk holding a recipe, visual planning page, and pen',True);sig('deskjet_2955',5,True,surface='simple desk',background_details=[])
edit('laserjet',11,'Warm natural light and simple furniture keep','Warm natural light keeps')
edit('laserjet',3,'A finance workteam office desk','A desk in a modern finance office',reason='Replace an awkward compound place name with ordinary language.')
edit('laserjet',4,'A legal workteam office desk','A desk in a modern law office',reason='Replace an awkward compound place name with ordinary language.')
edit('laserjet',2,'while clean shelving and plants create','while plants create',True);sig('laserjet',2,True,background_details=['multiple workstations','plants'])
edit('laserjet',4,'simple desks holding notebooks, forms, and papers','a simple desk holding a notebook, forms, and papers',True)
edit('laserjet',4,'Plants and subtle personal touches on the workstations keep','Plants keep',True);sig('laserjet',4,True,surface='simple desk',local_props=['notebook','forms','papers'],background_details=['plants'])
edit('laserjet',5,'shared workteam desk','shared office desk',True,reason='Use ordinary office furniture language.')
edit('laserjet',8,'simple desks, notebooks, papers, plants, and subtle personal touches on the workstations','a simple desk holding a notebook and papers, with plants nearby',True);sig('laserjet',8,True,surface='simple desk',local_props=['notebook','papers'],background_details=['plants'])
edit('laserjet',9,'Layered office furnishings create natural depth. ','',True)
edit('laserjet',15,'simple furniture, a book, notebook, and stack of papers','a simple desk holding a book, notebook, and stack of papers',True);sig('laserjet',15,True,surface='simple desk',background_details=[])
edit('laserjet',17,' positioned against a textured wall','',True)
edit('laserjet',19,'surround the simple furniture','sit nearby',True)

# Two quoted passages had correct general meaning but were not verbatim.
o=outputs[cid('deskjet_2955',True)];i=json.loads(Path(cases[cid('deskjet_2955',True)]['input_path']).read_text())
for e in o['debug']['source_evidence']:
 if e['id']=='e4':e['quote']='household lists, recipes, small photos, or visual planning pages'
 if e['id']=='e11':e['quote']='Simple HP home printing helps finish labels, forms, worksheets, scans, and creative projects.'
 assert e['quote'] in i[e['document']]

# Explicit C-Tech classification review; none of these changes modify scene text.
for pair,wide,nums in [
 ('elitebook',False,[3,6,7,16]),('elitebook',True,[3,4,11,14,16]),
 ('deskjet_2955',False,[8,14,16,19]),('deskjet_2955',True,[17]),
 ('laserjet',False,[7,8,11,12,15,18]),('laserjet',True,[19]),
 ('cashmere',False,[5,7,10,12,14,15]),('cashmere',True,[13])]:
 for n in nums:ctech(pair,n,wide)

# Conservative score corrections from final prose, not the document's entire implied workflow.
for n in (4,5):score('elitebook',n,[30,10,10,10],True)
score('deskjet_2955',8,[30,10,10,10])
for n in (9,10):score('deskjet_2955',n,[0,20,20,0],True,why='Both documents support worksheets/home learning, but neither establishes this classroom or library. Credit the visible worksheet only; the institution is a creative departure.')
score('deskjet_2955',11,[0,10,20,0],True,why='Both documents support household forms; the study-room institution is invented. Credit only the visible form, not an academic workflow.')
for n in (5,7):score('laserjet',n,[30,10,10,10])
for n in (11,12,13):
 score('cashmere',n,[10,0,0,10],why='Both documents support broad professional work; this creative-office venue is inferred and no creative task/material survives the tight view.')
 p('cashmere',n)['relationship']='creative_departure'
for n in (9,10,11):
 c=p('cashmere',n,True);score('cashmere',n,[0,0,0,0],True,why='Creative departure following C-Tech. Do not ground this sketching scene in Flip-dependent messaging when the paired brief identifies a different product. No compatible shared source evidence is claimed.')
 c['evidence_ids']=[];c['relationship']='creative_departure';c['creative_departures'].append('Creative-office sketching is a C-Tech alternative; excluded mismatched-product use-case evidence.')

# Record every changed field recursively, then re-run the same deterministic contract.
def differences(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  for k in sorted(set(a)|set(b)):
   yield from differences(a.get(k),b.get(k),path+'/'+str(k))
 elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  for index,(x,y) in enumerate(zip(a,b)):yield from differences(x,y,path+'/'+str(index))
 elif a!=b:yield {'path':path,'before':a,'after':b}
reviewed={};reports={};prose_edits=0;changes=0
for key,o in outputs.items():
 original=originals[key];a=audits[key];m=cases[key];inp=json.loads(Path(m['input_path']).read_text())
 prefinal=copy.deepcopy(o);patches=list(differences(original,prefinal));changes+=len(patches)
 prose_edits+=sum(x['text']!=y['text'] for x,y in zip(original['prompts'],o['prompts']))
 out,log=finalize_output(o,raw_input=inp,registry=registry);val=validate_output(out,inp,schema,registry);reports[key]=val
 if not val['passed']:print(key,val['errors'])
 outpath=HERE/'reviewed_outputs'/f'{key}.json';put(outpath,out)
 put(HERE/'review_logs'/f'{key}.json',{'normalized_input_path':a['normalized_output_path'],'normalized_input_sha256':sha(Path(a['normalized_output_path'])),'root_field_edits':patches,'post_review_finalization':log,'validation':val})
 reviewed[key]={**m,'status':'root_reviewed_editorial_pilot_not_raw_model_success','human_review_status':'root_text_review_complete_with_logged_edits','launchable':False,'normalized_output_path':a['normalized_output_path'],'reviewed_output_path':str(outpath),'record_path':a['record_path'],'record_sha256':a['raw_record_sha256'],'candidates':[dict(c,candidate_key=f"{key}::{c['id']}",rank=n) for n,c in enumerate(out['prompts'],1)],'debug':out['debug'],'review_log_path':str(HERE/'review_logs'/f'{key}.json'),'model_normalized_validation_passed':a['normalized_validation']['passed']}
assert all(v['passed'] for v in reports.values()),'reviewed outputs still violate contract'
review={'version':'v5-r3-root-reviewed-pilot-v1','status':'root_reviewed_with_logged_edits_waiting_for_user','review_disclosure':f'160 GPT-5.5 candidate texts reviewed. Root edited {prose_edits} scene texts and corrected audit fields/scores with full before/after logs. Before editorial review, 3 of 8 normalized model banks passed mechanical validation; this is not evidence of unaided runtime reliability. No V5 images generated.','selection_status':'top_six_by_reviewed_source_score_text_only','cases':reviewed,'counts':{'cases':8,'candidates':160,'scene_texts_edited':prose_edits,'field_edits':changes,'reviewed_validation_passes':8,'model_normalized_validation_passes':3},'launchable':False}
put(HERE/'reviewed_prompt_cases.json',review)
put(HERE/'reviewed_validation.json',reports)
print(review['counts'])
