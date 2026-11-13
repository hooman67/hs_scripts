# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Bounded pilot. Attribution, split names and annotations never enter the model call."""
import argparse,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from run_judge import judge
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--split',choices=['development','held_out'],required=True);p.add_argument('--limit',type=int);p.add_argument('--run',default='pilot_v1');p.add_argument('--model',default='gpt-5.5');p.add_argument('--rows',type=int,nargs='+');p.add_argument('--visual-anchors',action='store_true');a=p.parse_args()
 assets=json.loads((ROOT/'data/assets.json').read_text())['assets'];split=json.loads((ROOT/'data/split.json').read_text())
 cases=[c for c in split['cases'] if c['split']==a.split and (not a.rows or c['row'] in a.rows)][:a.limit]
 def run(c):
  image=next(x for x in assets if x['id']==c['id']);twin=next(x for x in assets if x['type']=='product_input' and x['row']==c['row'])
  runtime={'generated_image':image['local_path'],'twin_image':twin['local_path'],'product_type':image['device'].lower(),'scene_prompt':image['original_prompt'],'image_stage':'scene_generation'}
  result=judge(runtime,ROOT/'runs'/a.run/c['id'],a.model,a.visual_anchors)
  return {'id':c['id'],'split':a.split,'ok':result['ok'],'score':result.get('judgment',{}).get('natural_placement_score'),'verdict':result.get('judgment',{}).get('verdict'),'error':result.get('error_type'),'validation_errors':result.get('validation_errors')}
 results=[]
 with ThreadPoolExecutor(max_workers=2) as pool:
  tasks=[pool.submit(run,c) for c in cases]
  for f in as_completed(tasks):
   r=f.result();results.append(r);print(json.dumps(r),flush=True)
 (ROOT/'runs'/a.run/f'{a.split}_status.json').write_text(json.dumps(results,indent=2)+'\n')
 return 0 if all(r['ok'] for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
