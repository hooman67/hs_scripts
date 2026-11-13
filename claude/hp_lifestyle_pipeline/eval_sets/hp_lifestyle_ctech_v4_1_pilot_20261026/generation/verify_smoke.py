"""Verify the four recorded integration checks without API calls or scene edits."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw
E=Path(__file__).resolve().parents[1]
M=E/'image_generation_manifest.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 m=json.loads(M.read_text());r=Path(m['run_dir']);pilot={x['candidate_key']:x for x in json.loads(Path(m['pilot_prompts']['path']).read_text())['prompts']};renders={x['camera_tag']:x for x in m['renders']};records=[]
 for p in (r/'records').glob('*.json'):
  d=json.loads(p.read_text())
  if d['candidate_id']=='p1':records.append((p,d))
 assert len(records)==4 and {d['camera_tag'] for p,d in records}==set(renders)
 evidence=[];dest=E/'generation/smoke_review';dest.mkdir(exist_ok=True)
 for p,d in sorted(records):
  a=renders[d['camera_tag']];b=d['reference_binding'];q=d['request_payload'];im=d['generated_image'];c=pilot[d['candidate_key']]
  assert d['status']=='done' and d['returned_seed']==42
  assert q['prompt']==d['debugData']['rawPrompt']==c['text']
  assert q['referenceBlobs']==[{'id':b['blob_id']}]
  assert b['camera_tag']==a['camera_tag'] and b['device_type']==a['device_type']
  assert b['original_png_path']==a['path'] and b['original_png_sha256']==a['sha256']==sha(a['path'])
  assert b['original_png_bytes']==a['bytes']==Path(a['path']).stat().st_size
  assert b['image_generation_manifest_sha256']==sha(M)==d['provenance']['image_generation_manifest_sha256']
  assert sha(im['path'])==im['sha256']
  assert q['size']=={'width':2368,'height':1776} and Image.open(im['path']).size==(2368,1776)
  assert sha(Path(m['pilot_prompts']['path']))==d['provenance']['pilot_prompts_sha256']==m['pilot_prompts']['sha256']
  canvas=Image.new('RGB',(1440,570),'white');ImageDraw.Draw(canvas).text((12,8),a['camera_tag']+' | corrected input / output',fill='black')
  for i,img in enumerate([a['path'],im['path']]):canvas.paste(Image.open(img).convert('RGB').resize((720,540)),(i*720,30))
  cp=dest/(a['camera_tag']+'.png');canvas.save(cp)
  evidence.append({'camera_tag':a['camera_tag'],'candidate_key':d['candidate_key'],'record_path':str(p),'record_sha256':sha(p),'input_sha256':a['sha256'],'output_sha256':im['sha256'],'comparison_path':str(cp),'comparison_sha256':sha(cp),'binding_and_prompt_checks':'passed'})
 out={'version':'hp-v4.1-smoke-review-v1','reviewed_at':datetime.now(timezone.utc).isoformat(),'status':'integration_passed_continue_authorized_120','manifest_sha256':sha(M),'checked_images':4,'expected_total':120,'remaining':116,'records':evidence,'root_visual_review':'Root inspected all four input/output composites. Expected device types, recognizable device geometry and approximate close/wide framing are present. No measured geometric identity or user image-quality acceptance is claimed.','observed_downstream_changes':['Laptop close-up: downstream rewrite added mug, notebook, pen, partitions and plant although environment prompt requested no props/background fixtures.','Printer close-up: downstream rewrite added a succulent and room fixtures beyond the requested paper stack.','Printer wide: downstream rewrite introduced a credenza and cool color grade. These are endpoint-stage behavior, not edits to the frozen pilot prompt.'],'decision':'Proceed with remaining116 within user-authorized pilot. Retain all exact requests and debug so downstream expansion can be reviewed.'}
 (E/'smoke_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({'verified':4,'remaining':116,'review':str(E/'smoke_review.json')})
if __name__=='__main__':main()
