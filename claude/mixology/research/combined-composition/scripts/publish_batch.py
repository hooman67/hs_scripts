"""Snapshot the live gallery before edits, then publish and verify this authorized batch."""
import argparse
import concurrent.futures
import hashlib
import json
import mimetypes
from pathlib import Path

import boto3

RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
BUCKET = 'foundry-tccc-enterprise-adobe-assets'
PREFIX = 'mixology/refraction_research_2026-10-19/'
BASELINE = RUN / '_review/combined_prepublication_2026-10-20'
MIME = {'.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
        '.md': 'text/markdown', '.json': 'application/json', '.txt': 'text/plain'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def preflight(s3):
    BASELINE.mkdir(parents=True, exist_ok=False)
    previous = json.loads((RUN / '_review/s3_verification.json').read_text())
    keys = [f['path'] for f in previous['files'] if f['path'].startswith('gallery/')
            or f['path'].endswith('/output.png')]
    evidence = []
    for path in keys:
        response = s3.get_object(Bucket=BUCKET, Key=PREFIX+path)
        data = response['Body'].read()
        saved = BASELINE / path
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(data)
        if path.startswith('gallery/'):
            assert data == (RUN / path).read_bytes(), f'Live gallery diverged: {path}'
        evidence.append(dict(path=path, sha256=sha(data), bytes=len(data)))
    (BASELINE / 'manifest.json').write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps({'preflight': 'pass', 'files': len(evidence), 'path': str(BASELINE)}))


def publish(s3):
    baseline = json.loads((BASELINE / 'manifest.json').read_text())
    # No blind overwrite if someone changed the live gallery since our preflight.
    for item in baseline:
        if item['path'].startswith('gallery/'):
            current = s3.get_object(Bucket=BUCKET, Key=PREFIX+item['path'])['Body'].read()
            assert sha(current) == item['sha256'], 'Live gallery changed since preflight'
    files = [p for p in RUN.rglob('*') if p.is_file()
             and not {'_review', '_archive', '__pycache__'}.intersection(p.parts)
             and p.suffix not in ('.lock', '.tmp')]
    def upload(p):
        mime = MIME.get(p.suffix, mimetypes.guess_type(p.name)[0] or 'application/octet-stream')
        data = p.read_bytes()
        key = PREFIX+str(p.relative_to(RUN))
        s3.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType=mime, CacheControl='no-cache')
        result = s3.get_object(Bucket=BUCKET, Key=key)
        readback = result['Body'].read()
        assert sha(readback) == sha(data), key
        assert result['ContentType'] == mime, key
        return dict(path=str(p.relative_to(RUN)), sha256=sha(data), bytes=len(data), content_type=mime)
    # Upload dependencies before the HTML entry point.
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        evidence = list(pool.map(upload, [p for p in files if p != RUN/'gallery/index.html']))
    evidence.append(upload(RUN/'gallery/index.html'))
    result = dict(bucket=BUCKET, prefix=PREFIX.rstrip('/'), all_bytes_verified=True,
                  file_count=len(evidence), total_bytes=sum(x['bytes'] for x in evidence), files=evidence,
                  gateway_authentication='Authenticated S3 readback; local browser IMS mocked, not a signed-in gateway browser test.')
    (RUN/'_review/s3_verification.json').write_text(json.dumps(result, indent=2)+'\n')
    (RUN/'_review/combined_publication_2026-10-20.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'files'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'publish'])
    args = parser.parse_args()
    client = boto3.client('s3', region_name='us-west-2')
    (preflight if args.action == 'preflight' else publish)(client)
