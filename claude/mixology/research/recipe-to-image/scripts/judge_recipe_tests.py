"""Advisory actual Astra/high vision critique; preserve all judge inputs and metadata."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from foundry_aws_gateway import llm

ROOT=Path('/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image')
PROMPT='''You are a skeptical commercial product-image evaluator. Compare candidate images with the provided fixed neutral master, and evaluate each against its supplied recipe and comparison photograph. The master defines cup/view, not beverage identity. Comparison photographs define appearance only, not geometry. Do not assume the generation method or favor a method label. Estimate visual differences honestly; no pixel-exact or physical-metrology claims from vision. Evaluate: cup silhouette/width/taper/base construction; rim ellipse and camera viewpoint; upright axis and flat surface contact (look for backward lean, floating or an underside implying tilt); complete framing; cream remains soft serve, not whipped cream; syrup/base identity and no invented ingredients; ingredient syrup amount does not prove appearance from pixels. Condensation is not carbonation: distinguish droplets on exterior from bubbles in liquid, particularly for tea. Return JSON only with candidate id, geometry_matches_master (boolean), grounding_plausible (boolean), recipe_appearance_matches (boolean), visible_defects (list), camera_and_geometry_notes (string), recipe_notes (string), and limitations (list). A good appearance cannot excuse cup/view drift. All outputs are research samples, not customer approved.'''


def main(ids):
    target=ROOT/'analysis'/('judge_'+ids[0]+'.json')
    if target.exists():
        raise RuntimeError('Judge already exists; do not duplicate')
    images=[(ROOT/'runs/master_neutral_v1/output.png','Fixed common cup/camera master')]
    records=[]
    for run_id in ids:
        record=json.loads((ROOT/'runs'/run_id/'record.json').read_text())
        records.append(record)
        images.extend([(ROOT/'runs'/run_id/'output.png','Candidate '+run_id),
                       (Path(record['comparison_original']['path']),'Appearance comparison only for '+run_id)])
    content=[{'type':'input_text','text':'Judge these candidates individually:\n'+json.dumps([
        {'id':r['id'],'recipe':r['recipe']['recipe'],'house_appearance':r['recipe']['appearance_policy']} for r in records])}]
    inputs=[]
    for path,role in images:
        content.append({'type':'input_text','text':role})
        content.append({'type':'input_image','image_url':'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode(),'detail':'high'})
        inputs.append({'path':str(path),'role':role,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    request={'model':'gpt-6-astra','reasoning':{'effort':'high'},'system_prompt':PROMPT,'candidates':[
        {'id':r['id'],'recipe':r['recipe']} for r in records],'images':inputs,'created_at':datetime.now(timezone.utc).isoformat()}
    target.parent.mkdir(exist_ok=True)
    target.with_name(target.stem+'_request.json').write_text(json.dumps(request,indent=2,ensure_ascii=False)+'\n')
    client=llm.get_openai().with_options(timeout=300,max_retries=0)
    response=client.responses.create(model='gpt-6-astra',reasoning={'effort':'high'},
        input=[{'role':'system','content':PROMPT},{'role':'user','content':content}])
    result={'requested_model':'gpt-6-astra','reasoning_effort':'high','response_model':response.model,
            'status':response.status,'request_id':response._request_id,'response_id':response.id,
            'usage':response.usage.model_dump(mode='json') if response.usage else None,'text':response.output_text}
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'file':str(target),'model':response.model,'status':response.status,'text':response.output_text}),flush=True)


if __name__=='__main__':
    os.environ['FOUNDRY_AWS_GATEWAY_HOST']='https://foundry-aws-pluto.adobe.io'
    parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='+');args=parser.parse_args()
    main(args.ids)
