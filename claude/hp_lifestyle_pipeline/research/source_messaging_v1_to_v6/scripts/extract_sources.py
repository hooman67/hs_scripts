"""Extract only approved source messaging and reference content; no third-party deps."""
from __future__ import annotations

import hashlib
import json
import posixpath
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / 'input_output_hp_rewriter_10_03_26'
DATA = ROOT / 'research/source_messaging_v1_to_v6/data'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(name: str, data):
    path = DATA / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def sources():
    entries, excluded, unique = [], [], {}

    def record(path, member, raw):
        obj = json.loads(raw)
        normalized = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
        key = sha(normalized)
        entry = {'path': str(path), 'member': member, 'sha256': sha(raw), 'semantic_sha256': key,
                 'top_level_type': type(obj).__name__, 'keys': list(obj) if isinstance(obj, dict) else None}
        entries.append(entry)
        if key not in unique:
            target = DATA / 'source_json' / (key[:16] + '.json')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            unique[key] = {'input_path': str(target), 'origins': [], 'keys': entry['keys']}
        unique[key]['origins'].append({'path': str(path), 'member': member, 'sha256': sha(raw)})

    for path in sorted((INPUT / 'inputs').iterdir()):
        if path.suffix.lower() == '.zip':
            with ZipFile(path) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    if Path(info.filename).name.startswith('Source Messaging') and info.filename.endswith('.json'):
                        record(path, info.filename, z.read(info))
                    else:
                        excluded.append({'path': str(path), 'member': info.filename,
                                         'reason': 'Not source messaging; contents not read'})
        elif path.name.startswith('Source Messaging') and path.suffix.lower() == '.json':
            record(path, None, path.read_bytes())
    dump('source_manifest.json', {'retrieved': '2026-10-13', 'entries': entries,
                                'unique_inputs': unique, 'excluded_without_reading': excluded})


def docx(path):
    with ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    paras = []
    for i, p in enumerate(root.findall('.//w:p', NS), 1):
        text = ''.join(t.text or '' for t in p.findall('.//w:t', NS))
        if text.strip():
            paras.append({'paragraph': i, 'text': text})
    return {'path': str(path), 'sha256': sha(path.read_bytes()), 'paragraphs': paras}


def xlsx(path, first_only):
    with ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
            strings = [''.join(t.text or '' for t in si.findall('.//s:t', NS)) for si in tree]
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = {r.attrib['Id']: r.attrib['Target'] for r in rels}
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        sheets = []
        for s in wb.findall('s:sheets/s:sheet', NS):
            rid = s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = targets[rid]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            tree = ET.fromstring(z.read(target))
            cells = []
            for c in tree.findall('.//s:sheetData/s:row/s:c', NS):
                addr = c.attrib['r']
                if first_only and re.match(r'[A-Z]+', addr).group() != 'A':
                    continue
                typ = c.attrib.get('t')
                v = c.find('s:v', NS)
                text = v.text if v is not None else ''
                if typ == 's' and text is not None:
                    text = strings[int(text)]
                elif typ == 'inlineStr':
                    text = ''.join(t.text or '' for t in c.findall('.//s:t', NS))
                if text:
                    cells.append({'cell': addr, 'text': text})
            sheets.append({'name': s.attrib['name'], 'cells': cells})
    return {'path': str(path), 'sha256': sha(path.read_bytes()),
            'allowed_columns': ['A'] if first_only else 'all', 'sheets': sheets}


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    sources()
    refs = INPUT / 'example_prompts'
    dump('october_guidance.json', docx(refs / 'HP - mAIstro Prompt Guidance (Oct 2026).docx'))
    dump('lifestyle_column_a.json', xlsx(refs / 'Eval-Set_Lifestyle-Photography_wSKUs.xlsx', True))
    dump('model_output_evalset.json', xlsx(refs / 'HP_Model-Output-EvalSet_092426.xlsx', False))
    manifest = json.loads((DATA / 'source_manifest.json').read_text())
    print(json.dumps({'source_occurrences': len(manifest['entries']),
                      'unique_json_contents': len(manifest['unique_inputs']),
                      'excluded_entries': len(manifest['excluded_without_reading'])}))


if __name__ == '__main__':
    main()
