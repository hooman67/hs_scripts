"""Restore source drink pixels inside a conservative mask after Sunburst background cleanup.

No inference here. The unchanged bundled imagegen CLI produced raw_sunburst.png.
The mask comes from that shadow-free output, not from the shadow-bearing source.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT=Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
FOLDER=RUN/'input_cleanup/overhead_from_013_v1'
SOURCE=RUN/'assets/image_013_p05_xref1594.jpg'
RAW=FOLDER/'raw_sunburst.png'
OUTPUT=FOLDER/'overhead_013_clean.png'
CLI=Path('/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    if OUTPUT.exists():raise FileExistsError('Preserve completed output; review before any rerun')
    source=Image.open(SOURCE).convert('RGB');raw=Image.open(RAW).convert('RGB')
    assert source.size==raw.size==(1537,1023),'Do not silently resize original cups'
    a=np.asarray(raw).astype(np.int16)
    foreground=(a.min(axis=2)<246)|((a.max(axis=2)-a.min(axis=2))>8)
    mask=Image.fromarray((foreground*255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
    # Select the three continuous cup silhouettes and discard isolated background specks.
    selected=Image.new('L',raw.size,0)
    for seed in [(285,220),(1325,275),(710,740)]:
        component=mask.copy();ImageDraw.floodfill(component,seed,128)
        selected=Image.fromarray(np.maximum(np.asarray(selected),(np.asarray(component)==128).astype('uint8')*255))
    # Fill enclosed white highlights and foam without extending into open background.
    filled=selected.copy()
    for point in [(0,0),(1536,0),(0,1022),(1536,1022)]:
        if filled.getpixel(point)==0:ImageDraw.floodfill(filled,point,128)
    filled=Image.fromarray((np.asarray(filled)!=128).astype('uint8')*255)
    # Boundary uses the cleaned model rim; eroded interior uses original pixels exactly.
    interior=filled.filter(ImageFilter.MinFilter(9))
    alpha=interior.filter(ImageFilter.GaussianBlur(0.7))
    result=Image.composite(source,raw,alpha)
    result.save(OUTPUT)
    alpha.save(FOLDER/'source_preservation_mask.png')
    filled.save(FOLDER/'cup_silhouettes.png')
    protected=np.asarray(alpha)==255
    diff=np.abs(np.asarray(result).astype(np.int16)-np.asarray(source).astype(np.int16))
    assert not diff[protected].any(),'Protected source pixels must remain exact'
    outside=np.asarray(filled.filter(ImageFilter.MaxFilter(17)))==0
    b=np.asarray(result).astype(np.int16)
    checks={
      'dimensions':list(result.size),'source_and_output_same_dimensions':True,
      'fully_protected_pixels':int(protected.sum()),
      'protected_source_pixels_changed':int((diff[protected].max(axis=1)>0).sum()),
      'background_pixels_checked':int(outside.sum()),
      'background_mean_rgb':[round(float(v),3) for v in b[outside].mean(axis=0)],
      'background_pixels_chroma_gt_12':int(((b[outside].max(axis=1)-b[outside].min(axis=1))>12).sum()),
      'background_pixels_min_channel_lt_235':int((b[outside].min(axis=1)<235).sum())}
    assert checks['background_pixels_chroma_gt_12']==0
    assert checks['background_pixels_min_channel_lt_235']==0
    prompt=PROJECT/'prompts/clean_overhead_input_v1.txt'
    shutil.copy2(prompt,FOLDER/'image_prompt.txt')
    (FOLDER/'system_prompt.txt').write_text('No Astra rewriter/system prompt used. Direct background-cleanup image edit; frozen refraction system V3 was not applied.\n')
    record={'id':'overhead_from_013_v1','task':'Remove external shadows/refractions to create a better overhead input',
      'status':'complete','source':str(SOURCE),'source_sha256':sha(SOURCE),
      'source_url':'https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/assets/image_013_p05_xref1594.jpg',
      'model':'gpt-image-2.5-sunburst','quality':'high','size':'auto','output_format':'png',
      'system_prompt':None,'image_prompt':prompt.read_text(),'model_input_images':[str(SOURCE)],
      'model_input_mask':None,'cli_sha256':sha(CLI),'reported_image_seconds':23.4,
      'raw_output':str(RAW),'raw_sha256':sha(RAW),'output':str(OUTPUT),'output_sha256':sha(OUTPUT),
      'postprocessing':'Extract cup silhouettes from shadow-free raw output; erode silhouette 4px after 2px dilation, feather 0.7px, restore original image pixels wherever alpha is 255. Narrow rim/edge transition remains from the generated cleanup.',
      'source_preservation_mask':str(FOLDER/'source_preservation_mask.png'),
      'checks':checks,'created_at':datetime.now(timezone.utc).isoformat(),
      'limitations':['Derived cleanup of customer output 013, not an independently supplied original input.',
                    'Pixel-exact guarantee applies only to the saved fully opaque preservation mask; generated boundary pixels are not exact source pixels.',
                    'Original image 013 canvas includes slight cup edge crops, intentionally preserved. No extra outpainting.'],
      'visual_review':'External colored beams and shadows removed in the raw edit; source interior texture restored in the delivered composite. Final composite requires visual inspection.'}
    (FOLDER/'record.json').write_text(json.dumps(record,indent=2)+'\n')
    # Future input gets a new filename, never replacing historical 012.
    destination=RUN/'assets/overhead_013_clean.png'
    if destination.exists():raise FileExistsError(destination)
    shutil.copy2(OUTPUT,destination)
    print(json.dumps(checks))

if __name__=='__main__':main()
