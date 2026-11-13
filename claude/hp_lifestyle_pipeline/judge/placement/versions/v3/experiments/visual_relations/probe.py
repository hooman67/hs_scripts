from pathlib import Path
import sys,json,base64,hashlib,time,concurrent.futures,datetime
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from run_judge import client
p=Path(__file__).resolve().parent
system=(p/'system_prompt.md').read_text()
manifest=json.loads((ROOT/'data/model_probe_cases.json').read_text())
model=sys.argv[1] if len(sys.argv)>1 else 'gpt-5.5'
out=p/model;out.mkdir(exist_ok=True)
(out/'freeze.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':model,'system_sha256':hashlib.sha256(system.encode()).hexdigest(),'manifest_sha256':hashlib.sha256((ROOT/'data/model_probe_cases.json').read_bytes()).hexdigest(),'input':'generated image and product type only; no target feedback, prompt, anchors or twin; diagnostic ablation'},indent=2))
def run(r):
 d=out/r['id'];d.mkdir(exist_ok=True)
 if (d/'response.json').exists():return
 image=Path(r['generated_image']['local_path']);a,mode=client()
 req={'model':model,'system':system,'image':str(image),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'product_type':r['device_type'],'reasoning_effort':'high','max_completion_tokens':6000}
 (d/'request.json').write_text(json.dumps(req,indent=2))
 try:
  v=a.chat.completions.create(model=model,reasoning_effort='high',max_completion_tokens=6000,messages=[{'role':'system','content':system},{'role':'user','content':[{'type':'text','text':'Product type: '+r['device_type']},{'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(image.read_bytes()).decode(),'detail':'high'}}]}])
  (d/'response.json').write_text(v.model_dump_json(indent=2));(d/'assessment.txt').write_text(v.choices[0].message.content or '');print(r['id'],'done',flush=True)
 except Exception as e:
  (d/'error.json').write_text(json.dumps({'type':type(e).__name__,'status':getattr(e,'status_code',None)}));print(r['id'],type(e).__name__,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,manifest['records']))
