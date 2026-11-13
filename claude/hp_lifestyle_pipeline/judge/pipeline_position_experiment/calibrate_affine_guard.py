#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
import cv2, numpy as np
ROOT=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke')
VERSIONS=('v22','v22_1','v22_2','v22_2_1')

def metrics(row_dir: Path):
 r=json.loads((row_dir/'result.json').read_text()); x0,y0,x1,y1=r['guide_info']['product_bounds_px']
 src=cv2.imread(str(row_dir/'geometry_guide.png'),0); dst=cv2.imread(str(row_dir/'ours.png'),0)
 mask=np.zeros_like(src);mask[y0:y1,x0:x1]=255
 sift=cv2.SIFT_create();k1,d1=sift.detectAndCompute(src,mask);k2,d2=sift.detectAndCompute(dst,None)
 pairs=cv2.BFMatcher().knnMatch(d1,d2,k=2); good=[a for a,b in pairs if a.distance<.65*b.distance]
 q=np.float32([k1[m.queryIdx].pt for m in good]); t=np.float32([k2[m.trainIdx].pt for m in good])
 cv2.setRNGSeed(42);M,im=cv2.estimateAffine2D(q,t,method=cv2.RANSAC,ransacReprojThreshold=3.6,maxIters=4000,confidence=.995,refineIters=10)
 if M is None: return {'verifiable':False,'matches':len(good)}
 keep=im.ravel().astype(bool); qi=q[keep];ti=t[keep];A=M[:,:2];b=M[:,2]
 pred=qi@A.T+b;res=np.linalg.norm(pred-ti,axis=1);U,s,Vt=np.linalg.svd(A);R=U@Vt
 rot=math.degrees(math.atan2(R[1,0],R[0,0]));scale=float(math.sqrt(abs(np.linalg.det(A))))
 shear=float(abs(np.dot(A[:,0],A[:,1]))/(np.linalg.norm(A[:,0])*np.linalg.norm(A[:,1])))
 nx=(qi[:,0]-x0)/max(x1-x0,1);ny=(qi[:,1]-y0)/max(y1-y0,1)
 quadrants=len({(int(x>=.5),int(y>=.5)) for x,y in zip(nx,ny)})
 hull=cv2.convexHull(qi).reshape(-1,2); hull_fraction=float(cv2.contourArea(hull)/max((x1-x0)*(y1-y0),1)) if len(hull)>=3 else 0
 corners=np.float32([[x0,y0],[x1,y0],[x1,y1],[x0,y1]]);tc=corners@A.T+b
 h,w=dst.shape
 return {'verifiable':True,'matches':len(good),'inliers':int(keep.sum()),'inlier_ratio':float(keep.mean()),
   'full_scale':scale,'rotation_deg':rot,'singular_min':float(s.min()),'singular_max':float(s.max()),
   'anisotropy_ratio':float(s.max()/s.min()),'column_shear_cos':shear,
   'residual_median_px':float(np.median(res)),'residual_p95_px':float(np.percentile(res,95)),
   'source_span_x_fraction':float(nx.max()-nx.min()),'source_span_y_fraction':float(ny.max()-ny.min()),
   'source_quadrants':quadrants,'source_hull_fraction':hull_fraction,
   'matrix':M.tolist(),'transformed_corners':tc.tolist(),
   'corners_in_frame':bool(((tc[:,0]>=0)&(tc[:,0]<w)&(tc[:,1]>=0)&(tc[:,1]<h)).all())}

def label(v,slug):
 # Evidence labels frozen from prior human/root review and exact-contract findings.
 if v=='v22':
  return 'accepted' if ('FrontWide' in slug and 'cashmere' in slug) else 'rejected'
 if v=='v22_1':
  if 'retained_control' in slug: return 'accepted'
  if 'magic__printer_FrontCloseUp' in slug: return 'rejected_position_under_new_policy'
  if 'magic__printer_FrontWide' in slug: return 'accepted'
  return 'rejected'
 if v in ('v22_2','v22_2_1'):
  return 'accepted' if 'FrontCloseUp' in slug else 'rejected'
 return 'unknown'

rows=[]
for v in VERSIONS:
 root=ROOT/v
 for d in sorted(p for p in root.iterdir() if p.is_dir()):
  rd=d/'run/rows'/d.name
  if (rd/'ours.png').exists(): rows.append({'version':v,'slug':d.name,'evidence_label':label(v,d.name),**metrics(rd)})
out=Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/affine_guard_calibration.json')
out.write_text(json.dumps(rows,indent=2))
for r in rows:
 print(r['version'],r['slug'],r['evidence_label'], 'in',r.get('inliers'),f"ratio={r.get('inlier_ratio',0):.2f}",
       f"s=({r.get('singular_min',0):.4f},{r.get('singular_max',0):.4f})",f"aniso={r.get('anisotropy_ratio',0):.4f}",
       f"rot={r.get('rotation_deg',0):.3f}",f"shear={r.get('column_shear_cos',0):.4f}",
       f"res={r.get('residual_median_px',0):.2f}/{r.get('residual_p95_px',0):.2f}",
       f"span={r.get('source_span_x_fraction',0):.2f}/{r.get('source_span_y_fraction',0):.2f}",
       f"q={r.get('source_quadrants')} hull={r.get('source_hull_fraction',0):.3f} corners={r.get('corners_in_frame')}")
