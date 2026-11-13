"""Save public source text and retrieval metadata. URLs supplied on the command line."""
import sys, json, re, hashlib
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

DEST = Path(__file__).resolve().parents[1] / 'data' / 'primary_review'
DEST.mkdir(parents=True, exist_ok=True)

def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()[:14]
    meta = {'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        r = requests.get(url, timeout=35, headers={'User-Agent': 'Mozilla/5.0'})
        meta.update(status=r.status_code, final_url=r.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        meta['title'] = soup.title.get_text(' ', strip=True) if soup.title else ''
        meta['links'] = [{'text': a.get_text(' ', strip=True), 'href': a.get('href')} for a in soup.find_all('a', href=True)]
        for e in soup(['script', 'style', 'noscript', 'nav', 'footer']):
            e.decompose()
        body = soup.get_text('\n', strip=True)
        (DEST / (key + '.txt')).write_text(body)
        meta['text_path'] = str(DEST / (key + '.txt'))
        meta['sha256_text'] = hashlib.sha256(body.encode()).hexdigest()
        meta['chars'] = len(body)
    except Exception as e:
        meta['error'] = str(e)
    (DEST / (key + '.json')).write_text(json.dumps(meta, indent=2))
    return {k: v for k, v in meta.items() if k != 'links'}

if __name__ == '__main__':
    for result in ThreadPoolExecutor(max_workers=4).map(fetch, sys.argv[1:]):
        print(json.dumps(result))
