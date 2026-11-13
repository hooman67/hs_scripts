from pathlib import Path
import cv2,json,numpy as np,sys
ROOT=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment')
PKG=Path('/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25')
sys.path.insert(0,str(PKG))
from hp3p.invariants import assess_product_affine
new=ROOT/'full160_v22_4_3/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1'
old=ROOT/'full160_v22_4_2_1/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1'
items={'prior_accepted':old/'gpt_1.png','fresh_attempt_1':new/'gpt_1.png','fresh_attempt_2':new/'gpt_2.png'}
guide=(new/'geometry_guide.png').read_bytes(); maskbytes=(new/'mask.png').read_bytes(); bounds=[576,536,1996,1402]
mask=cv2.imread(str(new/'mask.png'),cv2.IMREAD_UNCHANGED)[:,:,3]>127
contours,_=cv2.findContours(mask.astype(np.uint8)*255,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contour=max(contours,key=cv2.contourArea)
poly=cv2.approxPolyDP(contour,20,True).reshape(-1,2)
# Order starts at left-base in these frozen inputs.
labels=['base_front','lid_bottom','lid_right','lid_top','lid_left','base_rear']
rows={}
panels=[]
for name,path in items.items():
 res=assess_product_affine(guide,path.read_bytes(),bounds,fixed_position=True,product_mask=maskbytes)
 fb=res.get('textureless_fallback',{})
 dx=int(fb.get('translation_x_px',0)); dy=int(fb.get('translation_y_px',0))
 bgr=cv2.imread(str(path)); gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
 edges=cv2.Canny(gray,50,150)>0
 dist=cv2.distanceTransform((~edges).astype(np.uint8),cv2.DIST_L2,3)
 segs={}
 overlay=bgr.copy()
 for i,label in enumerate(labels):
  p0=poly[i].astype(float); p1=poly[(i+1)%len(poly)].astype(float)
  n=max(2,int(np.linalg.norm(p1-p0)))
  pts=np.linspace(p0,p1,n)
  xs=np.clip(np.rint(pts[:,0]+dx).astype(int),0,gray.shape[1]-1)
  ys=np.clip(np.rint(pts[:,1]+dy).astype(int),0,gray.shape[0]-1)
  vals=dist[ys,xs]
  segs[label]={'samples':len(vals),'coverage_2px':float((vals<=2).mean()),'median_px':float(np.median(vals)),'p90_px':float(np.percentile(vals,90))}
  cv2.line(overlay,tuple((poly[i]+[dx,dy]).astype(int)),tuple((poly[(i+1)%len(poly)]+[dx,dy]).astype(int)),(0,0,255),3)
 # output edges cyan, alpha polygon red
 overlay[edges]=(255,255,0)
 crop=overlay[430:1470,500:2070]
 cv2.putText(crop,name,(20,45),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),3,cv2.LINE_AA)
 cv2.putText(crop,f"boundary={fb.get('boundary_edge_coverage_2px'):.3f} internal={fb.get('internal_edge_coverage_2px'):.3f} shift=({dx},{dy})",(20,90),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2,cv2.LINE_AA)
 panels.append(cv2.resize(crop,(785,520)))
 rows[name]={'guard':res,'segments':segs}
canvas=np.full((1040,1570,3),255,np.uint8)
for i,p in enumerate(panels): canvas[(i//2)*520:(i//2+1)*520,(i%2)*785:(i%2+1)*785]=p
out=ROOT/'versions/v22_4_3'
cv2.imwrite(str(out/'fresh_failure_edge_overlays.jpg'),canvas,[cv2.IMWRITE_JPEG_QUALITY,95])
(out/'fresh_failure_diagnostics.json').write_text(json.dumps({'polygon':poly.tolist(),'segment_labels':labels,'rows':rows},indent=2)+'\n')
print(json.dumps({k:{'boundary':v['guard']['textureless_fallback']['boundary_edge_coverage_2px'],'internal':v['guard']['textureless_fallback']['internal_edge_coverage_2px'],'segments':v['segments']} for k,v in rows.items()},indent=2))
