#!/usr/bin/env python3
# ruff: noqa: UP017
"""Hash-check six reused inputs and build deterministic V4.5.3 aids without model calls."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from geometry import (
    create_furniture_room_crop,
    create_geometry_overlay,
    create_support_crop,
)

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'data/dev_6_manifest.json').read_text())
asset_root=ROOT/'data/dev_6_preflight_assets'
if asset_root.exists(): shutil.rmtree(asset_root)
asset_root.mkdir(parents=True)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
rows=[]
for row in manifest['records']:
    runtime=row['runtime_input']; errors=[]
    actual={'generated_image_sha256':sha(runtime['generated_image']),'twin_image_sha256':sha(runtime['twin_image'])}
    if actual!=row['frozen_hashes']: errors.append('input hash mismatch')
    if set(runtime)!={'generated_image','twin_image','product_type'}: errors.append('runtime key leakage')
    out=asset_root/row['record_id']; out.mkdir()
    product,product_meta=create_support_crop(runtime['generated_image'],runtime['twin_image'],out)
    room,room_meta=create_furniture_room_crop(runtime['generated_image'],product,out)
    overlay,overlay_meta=create_geometry_overlay(runtime['generated_image'],product,product_meta,out)
    rows.append({'record_id':row['record_id'],'errors':errors,'product_crop_status':product_meta.get('localization_status'),'product_crop_sha256':sha(product),'room_crop_sha256':sha(room),'room_unwarped':room_meta.get('unwarped'),'overlay_sha256':sha(overlay),'segments':overlay_meta.get('selected_segment_count')})
report={'schema_version':'hp-placement-v4.5.3-dev-six-preflight-v1','created_at':datetime.now(timezone.utc).isoformat(),'model_calls':0,'all_passed':all(not r['errors'] for r in rows),'rows':rows}
(ROOT/'data/dev_6_preflight.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['all_passed'] and len(rows)==6
print(json.dumps({'all_passed':True,'rows':len(rows),'model_calls':0},indent=2))
