"""Stage exact customer sources and PDF context for the bounded refraction experiment."""
import hashlib
import json
import shutil
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

PROJECT = Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
SOURCE = Path('/home/colligo/mixology_data/source_restored_2026-10-19/extracted_from_pdf/native_original_streams/refraction')
PDF = Path('/home/colligo/mixology_data/source_restored_2026-10-19/260605_Mixology_AI_Art_Direction_Process.pdf')


def main():
    for name in ['assets', 'pdf_context', 'runs', 'gallery', '_review']:
        (RUN / name).mkdir(parents=True, exist_ok=True)
    records = []
    for source in sorted(SOURCE.glob('*.jpg')):
        destination = RUN / 'assets' / source.name
        if not destination.exists():
            shutil.copy2(source, destination)
        with Image.open(destination) as im:
            dimensions = list(im.size)
        records.append({'source': str(source), 'staged': str(destination), 'dimensions': dimensions,
                        'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()})
    doc = pymupdf.open(PDF)
    text = []
    for i, page in enumerate(doc):
        text.append(f'PAGE {i+1}\n{page.get_text()}')
        if i in [3, 4, 5, 9, 11]:
            page.get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False).save(RUN/'pdf_context'/f'page_{i+1:02d}.png')
    (RUN/'pdf_context'/'pdf_text.txt').write_text('\n\n'.join(text))
    raw = doc[4].get_text()
    start = raw.index('Top-down, art-directed')
    end = raw.index('Chat GPT\nImage Output', start)
    customer = raw[start:end].strip()
    (RUN/'pdf_context'/'customer_page5_prompt.txt').write_text(customer+'\n')
    (RUN/'source_manifest.json').write_text(json.dumps({'pdf':str(PDF), 'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(), 'images':records},indent=2)+'\n')
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
    except OSError:
        font=ImageFont.load_default()
    cols=4; cw=400; ch=360
    sheet=Image.new('RGB',(cols*cw,((len(records)+cols-1)//cols)*ch),'#ececec')
    draw=ImageDraw.Draw(sheet)
    for n,r in enumerate(records):
        with Image.open(r['staged']) as im:
            im=im.convert('RGB');im.thumbnail((380,300))
            x=(n%cols)*cw;y=(n//cols)*ch
            sheet.paste(im,(x+(cw-im.width)//2,y+(310-im.height)//2))
            draw.text((x+10,y+314),Path(r['staged']).name.split('_xref')[0],font=font,fill='black')
    sheet.save(RUN/'_review'/'curated_contact.jpg',quality=94)
    print(json.dumps({'staged_images':len(records),'root':str(RUN)}))


if __name__=='__main__': main()
