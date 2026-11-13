"""Persist the supplied PDF and rendered recipe pages; never overwrite source bytes."""
from pathlib import Path
import hashlib
import json
import shutil
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path('/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image')
SOURCE = Path('/mnt/localssd/mixology/TCCC_Crafted_Norway_Pilot_Recipe_Book_260703.pdf')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    dest = ROOT / 'sources' / SOURCE.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert sha(dest) == sha(SOURCE), 'Refusing to replace a different PDF'
    else:
        shutil.copy2(SOURCE, dest)
    assert sha(dest) == sha(SOURCE)
    document = pymupdf.open(dest)
    pages = []
    sheet = Image.new('RGB', (1500, 1800), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for i, page in enumerate(document):
        text = ROOT / 'sources' / f'page_{i+1:02d}.txt'
        text.write_text(page.get_text(), encoding='utf-8')
        if i < 2:
            continue
        out = ROOT / 'sources' / f'page_{i+1:02d}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False).save(out)
        pages.append({'page': i+1, 'path': str(out), 'sha256': sha(out), 'text': str(text)})
        preview = Image.open(out).convert('RGB')
        preview.thumbnail((740, 540))
        x, y = ((i-2) % 2)*750, ((i-2)//2)*600
        draw.text((x+10,y+10), f'PDF page {i+1}', fill='black')
        sheet.paste(preview, (x, y+40))
    sheet.save(ROOT/'sources'/'recipe_pages_contact.jpg')
    manifest = {'as_of':'2026-10-20', 'source':str(SOURCE), 'durable_copy':str(dest),
                'pdf_sha256':sha(dest), 'bytes':dest.stat().st_size, 'pages':len(document),
                'rendering':'PyMuPDF 1.6x matrix, RGB; original PDF preserved unchanged', 'renders':pages}
    (ROOT/'sources'/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
