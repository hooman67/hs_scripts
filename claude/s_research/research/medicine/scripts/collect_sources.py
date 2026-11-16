#!/usr/bin/env python3
"""Fetch bounded public source sets; preserve text and access failures for audit."""
import concurrent.futures
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import urllib.request

BASE = Path(__file__).resolve().parents[1]
AS_OF = date.today().isoformat()

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.hidden += 1
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'tr', 'div', 'br'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript') and self.hidden:
            self.hidden -= 1
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'tr'):
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def fetch(item):
    key, url = item
    record = {'id': key, 'url': url, 'retrieval_date': AS_OF}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (public research)'})
        with urllib.request.urlopen(req, timeout=25) as response:
            raw = response.read()
            record.update(status=response.status, resolved_url=response.url,
                          content_type=response.headers.get('Content-Type', ''),
                          sha256=hashlib.sha256(raw).hexdigest())
        content = raw.decode('utf-8', errors='replace')
        if 'json' in record['content_type']:
            record['text'] = content
        else:
            parser = TextParser()
            parser.feed(content)
            lines = [re.sub(r'\s+', ' ', s).strip() for s in ''.join(parser.parts).splitlines()]
            record['text'] = '\n'.join(s for s in lines if s)
        first_text = record['text'][:500].lower()
        blocked = len(record['text']) < 80 or any(s in first_text for s in (
            'recaptcha', 'checking your browser', 'access denied', 'enable javascript'))
        record['content_access'] = 'blocked or non-content response' if blocked else 'inspectable content'
        return record
    except Exception as exc:
        record['error'] = str(exc)
        return record

def main():
    source_file = Path(sys.argv[1])
    items = json.loads(source_file.read_text())
    destination = BASE / 'data' / (source_file.stem + '_retrieved.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, items.items()))
    destination.write_text(json.dumps(records, indent=2, ensure_ascii=False) + '\n')
    pattern = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
    for r in records:
        print('\nSOURCE', r['id'], r.get('status', r.get('error')), r.get('resolved_url', r['url']))
        if 'text' not in r:
            continue
        lines = r['text'].splitlines()
        if pattern:
            hits = [i for i, line in enumerate(lines) if pattern.search(line)]
            shown = set()
            for i in hits[:16]:
                for j in range(max(0, i-1), min(len(lines), i+2)):
                    if j not in shown:
                        print(lines[j][:1100])
                        shown.add(j)
        else:
            print(r['text'][:1000])
    print('\nEvidence saved:', destination)

if __name__ == '__main__':
    main()
