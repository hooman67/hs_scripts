"""Deterministic projected-edge checks with inspectable guide overlays; not 3D metrology."""
from pathlib import Path
import json
import hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path('/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image')


def edges(image, y):
    # Median across 7 rows rejects isolated compression/antialias noise.
    band=np.median(image[y-3:y+4].min(axis=2),axis=0)
    xs=np.flatnonzero(band<235)
    xs=xs[(xs>100)&(xs<925)]
    return [int(xs.min()),int(xs.max())] if len(xs) else [None,None]


def main():
    out=ROOT/'analysis';out.mkdir(exist_ok=True)
    master=np.array(Image.open(ROOT/'runs/master_neutral_v1/output.png').convert('RGB'))
    rows=[550,650,800,1000,1200,1300]
    master_edges={str(y):edges(master,y) for y in rows}
    records=[]
    images=[]
    for p in sorted((ROOT/'runs').glob('*/output.png')):
        record=json.loads((p.parent/'record.json').read_text())
        arr=np.array(Image.open(p).convert('RGB'))
        observed={str(y):edges(arr,y) for y in rows}
        offsets=[abs(observed[str(y)][side]-master_edges[str(y)][side]) for y in rows for side in [0,1]]
        # Region above the rim contains topping and white background, never the changing liquid.
        difference=np.max(np.abs(arr[:430].astype('int16')-master[:430].astype('int16')),axis=2)
        metrics={'id':record['id'],'output_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                 'sampled_edges_px':observed,'max_sampled_edge_displacement_px':max(offsets),
                 'mean_sampled_edge_displacement_px':round(float(np.mean(offsets)),3),
                 'upper_430_rows_exact_pixel_fraction':round(float(np.mean(difference==0)),6),
                 'upper_430_rows_mean_max_channel_difference':round(float(difference.mean()),5)}
        records.append(metrics)
        overlay=Image.open(p).convert('RGB');draw=ImageDraw.Draw(overlay)
        for y in rows:
            left,right=master_edges[str(y)]
            draw.line((left,y,right,y),fill='#00bfff',width=2)
            for x in [left,right]: draw.line((x,y-15,x,y+15),fill='#00bfff',width=3)
            for x in observed[str(y)]: draw.ellipse((x-4,y-4,x+4,y+4),fill='#ee0055')
        overlay.save(out/(record['id']+'_guides.png'))
        thumb=overlay.copy();thumb.thumbnail((256,384));images.append((record['id'],thumb))
    contact=Image.new('RGB',(1024,430*((len(images)+3)//4)),'#eeeeee');draw=ImageDraw.Draw(contact)
    for i,(rid,im) in enumerate(images):
        x,y=(i%4)*256,(i//4)*430
        draw.text((x+3,y+5),rid.replace('v1_',''),fill='black')
        contact.paste(im,(x,y+38))
    contact.save(out/'geometry_contact.jpg')
    report={'method':'At six fixed image rows, median RGB-channel minimum over a 7-row band; outer pixels darker than 235 within x101..924. Blue guides=master; pink points=output. No image normalization, scaling or registration.',
            'limitations':'Projected high-contrast edge proxy, NOT exact cup segmentation or 3D pose. Threshold may select condensation, highlight or shadow rather than physical boundary. Guides require visual inspection. Region above y430 checks topping/background pixels only; it does not prove cup preservation.',
            'master_edges':master_edges,'results':records}
    (out/'geometry.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
