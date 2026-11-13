"""Resumable fal queue transport. No credentials or image data URIs in records."""
import base64
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urlsplit

import requests
from filelock import FileLock

KEY_PATTERN = re.compile(r'(?<![\w-])[\w-]{36}:[A-Za-z0-9_-]{32}(?![\w-])')
CONTROLS = {
    'x-app-fal-disable-fallback': 'true',
    'X-Fal-No-Retry': '1',
    'X-Fal-Store-IO': '0',
    'X-Fal-Object-Lifecycle-Preference': '{"expiration_duration_seconds":86400}',
    'X-Fal-Request-Start-Timeout': '120',
}


class FalError(RuntimeError):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def load_key(path=Path('/mnt/localssd/temp_creds.txt'), index=0):
    candidates = []
    for line in Path(path).read_text().splitlines():
        if 'fal' in line.lower():
            candidates.extend(KEY_PATTERN.findall(line))
    if not candidates or index >= len(candidates):
        raise FalError('No selected fal-labeled credential found')
    return candidates[index]


def sanitize(value):
    if isinstance(value, dict):
        return {key: '[REDACTED]' if key.lower() in ('authorization', 'api_key', 'token')
                else sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        if value.startswith('data:') and ';base64,' in value:
            mime, data = value.split(';base64,', 1)
            decoded = base64.b64decode(data)
            return {'mime': mime[5:], 'bytes': len(decoded), 'sha256': hashlib.sha256(decoded).hexdigest()}
        return KEY_PATTERN.sub('[REDACTED]', value)
    return value


def save(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(sanitize(data), indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def queue_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'queue.fal.run':
        raise FalError('Unexpected queue URL; refusing to forward credentials')
    return url


def check(response, folder, stage):
    if not response.ok:
        try:
            body = response.json()
        except ValueError:
            body = {'body_bytes': len(response.content)}
        save(folder / f'{stage}_error.json', {'http_status': response.status_code, 'response': body})
        raise FalError(f'fal {stage} HTTP {response.status_code}; inspect sanitized error record', response.status_code)
    return response.json()


def call(endpoint, payload, folder, stage):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    if not re.fullmatch(r'(rewriter|image|critic)(?:_r\d+)?', stage):
        raise ValueError('Unknown stage')
    with FileLock(str(folder / f'{stage}.lock'), timeout=1):
        request_path = folder / f'{stage}_request.json'
        request = {'endpoint': endpoint, 'payload': sanitize(payload), 'requested_headers': CONTROLS}
        if request_path.exists() and json.loads(request_path.read_text()) != request:
            raise FalError('Inputs changed for an existing stage; use a new run ID')
        save(request_path, request)
        result_path = folder / f'{stage}_response.json'
        if result_path.exists():
            return json.loads(result_path.read_text())
        headers = {'Authorization': 'Key ' + load_key(), **CONTROLS}
        queue_path = folder / f'{stage}_queue.json'
        submitted = folder / f'{stage}_submission.json'
        if queue_path.exists():
            queued = json.loads(queue_path.read_text())
        else:
            if submitted.exists():
                raise FalError('Submission outcome is uncertain or rejected; do not submit twice')
            save(submitted, {'state': 'submitting', 'endpoint': endpoint, 'started_epoch': time.time()})
            response = requests.post(queue_url('https://queue.fal.run/' + endpoint),
                                     json=payload, headers=headers, timeout=(15, 120), allow_redirects=False)
            queued = check(response, folder, stage)
            if not all(key in queued for key in ('request_id', 'status_url', 'response_url')):
                raise FalError('Missing queue identifiers; inspect before any retry')
            save(queue_path, queued)
            print(f'{stage.upper()} submitted {queued["request_id"]}', flush=True)
        started = time.monotonic()
        last = None
        while time.monotonic() - started < 900:
            response = requests.get(queue_url(queued['status_url']), headers=headers,
                                    timeout=(15, 45), allow_redirects=False)
            status = check(response, folder, stage)
            save(folder / f'{stage}_status.json', status)
            if status['status'] != last:
                print(f'{stage.upper()} {queued["request_id"]} {status["status"]}', flush=True)
                last = status['status']
            if status['status'] == 'COMPLETED':
                response = requests.get(queue_url(queued['response_url']), headers=headers,
                                        timeout=(15, 120), allow_redirects=False)
                result = check(response, folder, stage)
                save(result_path, result)
                return result
            time.sleep(3)
        raise FalError('Polling deadline reached; resume the saved queue ID, not a new submission')
