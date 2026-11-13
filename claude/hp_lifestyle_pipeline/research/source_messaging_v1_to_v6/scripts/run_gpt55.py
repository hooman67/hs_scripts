# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Resumable sequential GPT-5.5 evaluations; requires an explicitly supplied system prompt.

No source runs are launched merely by importing this module. Retries apply only to
transient API/network errors, and every successful response is saved before review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import jsonschema
from openai import APIConnectionError, APITimeoutError

from probe_gpt55 import ROOT, client_and_auth_mode


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def retry_delay(exc, attempt):
    headers = getattr(getattr(exc, 'response', None), 'headers', {})
    for key in ('retry-after-ms', 'x-ms-retry-after-ms'):
        try:
            if headers.get(key):
                return max(0, float(headers[key]) / 1000)
        except ValueError:
            pass
    value = headers.get('retry-after')
    if value:
        try:
            return max(0, float(value))
        except ValueError:
            try:
                return max(0, (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds())
            except (ValueError, TypeError):
                pass
    return min(60, 2 ** min(attempt, 6)) + random.uniform(0, 1)


def transient(exc):
    status = getattr(exc, 'status_code', None)
    return (status in (408, 409, 429) or (status is not None and status >= 500)
            or isinstance(exc, (APIConnectionError, APITimeoutError)))


def checkpoint(path, data):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--system', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'research/source_messaging_v1_to_v6/data/source_manifest.json')
    parser.add_argument('--schema', type=Path, default=ROOT / 'research/source_messaging_v1_to_v6/output.schema.json')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--max-attempts', type=int, default=100)
    parser.add_argument('--case', action='append', help='Optional semantic hash prefix; repeat for several cases')
    args = parser.parse_args()
    if not 1 <= args.max_attempts <= 1000:
        parser.error('--max-attempts must be between 1 and 1000')
    system = args.system.read_text()
    schema = json.loads(args.schema.read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    manifest = json.loads(args.manifest.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    client, auth_mode = client_and_auth_mode()
    settings = {'model': 'gpt-5.5', 'reasoning_effort': 'medium', 'max_completion_tokens': 8000}
    request_key = digest(json.dumps({'system': system, 'schema': schema, 'settings': settings}, sort_keys=True))
    for source_hash, entry in manifest['unique_inputs'].items():
        if args.case and not any(source_hash.startswith(prefix) for prefix in args.case):
            continue
        raw = Path(entry['input_path']).read_text()
        actual_source_hash = digest(json.dumps(json.loads(raw), sort_keys=True, ensure_ascii=False, separators=(',', ':')))
        if actual_source_hash != source_hash:
            raise RuntimeError('Source content changed after the manifest was created; rebuild the manifest')
        target = args.output_dir / (source_hash[:16] + '.json')
        previous = None
        if target.exists():
            old = json.loads(target.read_text())
            if old.get('request_key') != request_key or old.get('source_semantic_sha256') != source_hash:
                raise RuntimeError('Output directory contains a different run; use a new directory')
            if old.get('response'):
                if not old.get('schema_valid'):
                    raise RuntimeError('A recorded response needs review; inspect it before repeating the case')
                print('Already recorded:', source_hash[:16], flush=True)
                continue
            previous = old
        record = {'request_key': request_key, 'started_at': datetime.now(timezone.utc).isoformat(),
                  'source_semantic_sha256': source_hash, 'source_origins': entry['origins'],
                  'raw_input_json': raw, 'system_prompt': system, 'schema': schema,
                  'settings': settings, 'auth_mode': auth_mode, 'retry_events': []}
        if previous:
            record['prior_attempts'] = previous
        for attempt in range(1, args.max_attempts + 1):
            try:
                response = client.chat.completions.create(
                    **settings, messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': raw}],
                    response_format={'type': 'json_schema', 'json_schema': {'name': 'hp_environment_prompts', 'strict': True, 'schema': schema}})
                record['response'] = response.model_dump(mode='json')
                record['completed_at'] = datetime.now(timezone.utc).isoformat()
                checkpoint(target, record)
                if not response.model.startswith('gpt-5.5') or response.choices[0].finish_reason != 'stop':
                    raise RuntimeError('Unexpected model or incomplete response; inspect the preserved raw result')
                content = response.choices[0].message.content or ''
                result = json.loads(content)
                jsonschema.validate(result, schema)
                record['parsed_output'] = result
                record['schema_valid'] = True
                checkpoint(target, record)
                print('Recorded:', source_hash[:16], 'model:', response.model, 'prompts:', len(result['prompts']), flush=True)
                break
            except Exception as exc:
                if record.get('response') or not transient(exc) or attempt == args.max_attempts:
                    record['failure'] = {'type': type(exc).__name__, 'status_code': getattr(exc, 'status_code', None),
                                         'attempt': attempt}
                    checkpoint(target, record)
                    raise RuntimeError(f"Case {source_hash[:16]} stopped: {type(exc).__name__}; response/checkpoint preserved") from None
                delay = retry_delay(exc, attempt)
                record['retry_events'].append({'attempt': attempt, 'status_code': getattr(exc, 'status_code', None),
                                               'type': type(exc).__name__, 'wait_seconds': delay})
                # Keep incomplete retries separately so a restart can resume the case.
                checkpoint(target.with_suffix('.pending.json'), record)
                print('Retry:', source_hash[:16], f'{attempt}/{args.max_attempts}', 'wait seconds:', round(delay, 1), flush=True)
                while delay > 0:
                    step = min(30, delay)
                    time.sleep(step)
                    delay -= step
                    if delay > 0:
                        print('Waiting for provider:', source_hash[:16], round(delay, 1), 'seconds remaining', flush=True)
        pending = target.with_suffix('.pending.json')
        if pending.exists():
            pending.unlink()


if __name__ == '__main__':
    main()
