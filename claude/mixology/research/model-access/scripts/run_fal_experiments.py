"""Explicit fal provider variant of the bounded Mixology experiments.

Retains exact system/user prompts and ordered original image bytes. Uses the
documented Astra vision router and Sunburst edit endpoint, not the OpenAI CLI.
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests
from PIL import Image

from fal_transport import call

ROOT = Path('/home/colligo/hs_scripts/claude/mixology')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
REF = ROOT / 'research/refraction-prompts'
GROUP = ROOT / 'research/group-composition'
IMAGE_ENDPOINT = 'openai/gpt-image-2.5/sunburst/edit'
VISION_ENDPOINT = 'openrouter/router/vision'
ASTRA = 'openai/gpt-6-astra'
INPUTS = [
    ('315fb11e7cc94ecf8103ee2cf98227ae.png', 'clear drink with red upper layer'),
    ('6b61ea2d3b3f46959c6a0403879f8299.png', 'red iced drink'),
    ('b82dd27cd8c4471ea84aa21f9878e980.png', 'amber iced drink'),
    ('edbf33f823b842df9cd34393caea6cca.png', 'dark cola with red syrup'),
    ('TCCC–Crafted-Sept-2026.png', 'upright orange drink with red syrup'),
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def data_uri(path):
    path = Path(path)
    mime = 'image/png' if path.suffix.lower() == '.png' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def image_record(path, role, index):
    with Image.open(path) as image:
        dimensions = list(image.size)
    return dict(path=str(path), role=role, image_index=index,
                sha256=digest(path), dimensions=dimensions)


def vision(system, prompt, images, folder, stage, max_tokens=3000):
    return call(VISION_ENDPOINT, {
        'model': ASTRA, 'system_prompt': system, 'prompt': prompt,
        'image_urls': [data_uri(x['path']) for x in images],
        'max_tokens': max_tokens, 'reasoning': True, 'enable_web_search': False,
    }, folder, stage)


def configuration(kind, case_id, version):
    if kind == 'refraction':
        if not case_id.startswith('new_'):
            raise ValueError('This provider batch is limited to the five new drink cases')
        case = json.loads((REF / 'cases.json').read_text())[case_id]
        system = (REF / 'prompts/system_v3.md').read_text()
        assert hashlib.sha256(system.encode()).hexdigest() == '652fd8895c132e7cf6d311052f55a823dbe7ea09b749077a32d82faa6948eb9e'
        images = [image_record(RUN / 'assets' / case['input'],
                              'edit target, authoritative for drink identity and composition', 1),
                  image_record(RUN / 'assets/image_003_p03_xref116.jpg',
                              'lighting style reference ONLY, not a replacement for Image 1', 2)]
        user, size, system_version = 'Add refractions.', 'auto', 'v3'
        folder = RUN / 'runs' / f'{version}_{case_id}'
    else:
        case = json.loads((GROUP / 'cases.json').read_text())[case_id]
        composition_system = 'v2' if version == 'v2fal' else 'v1'
        system = (GROUP / 'prompts' / f'system_{composition_system}.md').read_text()
        images = []
        indices = case.get('input_indices', list(range(1, len(INPUTS) + 1)))
        if not indices or len(set(indices)) != len(indices) or any(
                type(index) is not int or not 1 <= index <= len(INPUTS) for index in indices):
            raise ValueError('Composition inputs must be distinct valid one-based source indices')
        for i, source_index in enumerate(indices, 1):
            filename, identifier = INPUTS[source_index - 1]
            path = RUN / 'assets/ref_inputs' / filename
            expected = ('152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da'
                        if source_index == 5 else digest(Path('/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs') / filename))
            assert digest(path) == expected
            images.append(image_record(path, 'authoritative compositing input for one finished drink, ' + identifier, i))
        user, size, system_version = case['user_prompt'], '1536x1024', composition_system
        folder = RUN / 'composition/runs' / f'{version}_{case_id}'
    return folder, dict(
        id=folder.name, version=version, kind=kind, case_id=case_id, case=case,
        system_version=system_version, system_prompt=system, user_prompt=user,
        input_images=images, provider='fal.ai', fal_endpoint=IMAGE_ENDPOINT,
        rewriter_model='gpt-6-astra', rewriter_endpoint=VISION_ENDPOINT,
        rewriter_requested_model=ASTRA, image_model='gpt-image-2.5-sunburst',
        quality='high', size_requested=size, output_format='png',
        status='prepared', prepared_at=utc(), script_sha256=digest(__file__),
        generation_mode='fal queue API; user-authorized provider switch; no prompt augmentation',
        provider_limitations='Requested exact model IDs; response schemas do not expose backend model snapshot. Astra reasoning effort is not exposed; reasoning=true is mandatory (false was rejected by the endpoint). Temperature is omitted (router schema default 1).',
        output=str(folder / 'output.png'), visual_review=None,
    )


def generate(kind, case_id, version):
    folder, record = configuration(kind, case_id, version)
    folder.mkdir(parents=True, exist_ok=True)
    record_path = folder / 'record.json'
    if record_path.exists():
        old = json.loads(record_path.read_text())
        if old['status'] == 'complete':
            print('SKIP complete ' + folder.name, flush=True)
            return
        for field in ['system_prompt', 'user_prompt', 'input_images', 'fal_endpoint']:
            if old[field] != record[field]:
                raise RuntimeError('Existing run inputs differ; use a new version')
        record = old
    else:
        save(record_path, record)
        (folder / 'system_prompt.md').write_text(record['system_prompt'])
        (folder / 'user_prompt.txt').write_text(record['user_prompt'] + '\n')
    started = time.monotonic()
    try:
        record.update(status='rewrite_running', started_at=record.get('started_at', utc()))
        save(record_path, record)
        request = record['user_prompt'] + '\n\nImages are supplied in this exact order:\n' + '\n'.join(
            f'Image {i}: {im["role"]}.' for i, im in enumerate(record['input_images'], 1))
        before = time.monotonic()
        rewrite_stage = record.get('rewriter_stage', 'rewriter')
        rewrite = vision(record['system_prompt'], request, record['input_images'], folder, rewrite_stage)
        prompt = rewrite['output'].strip()
        if not prompt or len(prompt) > 32000:
            raise RuntimeError('Empty or over-limit image prompt')
        if kind == 'refraction' and not prompt.lower().startswith('relight image 1'):
            raise RuntimeError('Rewriter did not follow V3 response contract; review before image submission')
        record.update(image_prompt=prompt, status='image_running', rewriter={
            'requested_model': ASTRA, 'returned_model': None, 'provider': 'fal.ai via OpenRouter',
            'request_prompt': request, 'reasoning_effort': None, 'reasoning_field': True,
            'seconds': round(time.monotonic() - before, 2), 'usage': rewrite.get('usage'),
            'queue_record': str(folder / f'{rewrite_stage}_queue.json'),
        })
        (folder / 'image_prompt.txt').write_text(prompt + '\n')
        save(record_path, record)
        print(f'IMAGE {folder.name}: {len(prompt.split())} prompt words', flush=True)
        size = 'auto' if record['size_requested'] == 'auto' else {'width': 1536, 'height': 1024}
        before = time.monotonic()
        result = call(IMAGE_ENDPOINT, {
            'prompt': prompt, 'image_urls': [data_uri(im['path']) for im in record['input_images']],
            'quality': 'high', 'image_size': size, 'num_images': 1,
            'output_format': 'png', 'enable_safety_checker': True,
        }, folder, 'image')
        record['image_seconds'] = round(time.monotonic() - before, 2)
        if len(result.get('images', [])) != 1:
            raise RuntimeError('Expected exactly one output image')
        output = folder / 'output.png'
        if not output.exists():
            url = result['images'][0]['url']
            parsed = urlsplit(url)
            if parsed.scheme != 'https' or not (parsed.hostname or '').endswith('.fal.media'):
                raise RuntimeError('Unexpected generated-image host; inspect without forwarding credentials')
            response = requests.get(url, timeout=(15, 120))
            response.raise_for_status()
            with output.open('xb') as stream:
                stream.write(response.content)
        with Image.open(output) as image:
            image.load()
            if image.format != 'PNG':
                raise RuntimeError('Expected original PNG bytes')
            record.update(output_dimensions=list(image.size), output_mode=image.mode)
        record.update(status='complete', output_sha256=digest(output), completed_at=utc(),
                      total_seconds=round(time.monotonic() - started, 2))
        save(record_path, record)
        print(f'DONE {folder.name}: {record["output_dimensions"]}', flush=True)
    except Exception as error:
        record.update(status='failed', error_type=type(error).__name__,
                      error_status=getattr(error, 'status_code', None), failed_at=utc())
        save(record_path, record)
        print(f'FAILED {folder.name}: {type(error).__name__}', flush=True)
        raise


def judge(kind, run_id):
    folder = RUN / ('runs' if kind == 'refraction' else 'composition/runs') / run_id
    record = json.loads((folder / 'record.json').read_text())
    if record['status'] != 'complete':
        raise RuntimeError('Cannot judge incomplete generation')
    if (folder / 'judge.json').exists():
        print('SKIP judged ' + run_id, flush=True)
        return
    if kind == 'refraction':
        sys.path.insert(0, str(REF / 'scripts'))
        from run_experiments import JUDGE
        system = JUDGE
        images = [record['input_images'][0], image_record(folder / 'output.png', 'candidate output', 2),
                  image_record(RUN / 'assets' / record['case']['positive'], 'approved lighting STYLE, different drink', 3),
                  image_record(RUN / 'assets/image_015_p06_xref590.jpg', 'rejected vein-like lighting style', 4)]
    else:
        system = (f'Evaluate a beverage composition against its {len(record["input_images"])} ordered source images. '
                  'Do not evaluate refraction styling: none should be added. Assess drink count/identity, '
                  'each cup body height relative to its rim width, base width and molded geometry, '
                  'cream and syrup patterns, source viewing angles, complete framing, and requested layout. '
                  'Ignore overall scaling and image margins. Do not invent precise pixel measurements. '
                  'Return only JSON with identity_score, geometry_score, arrangement_score (each 0-5), '
                  'observations (list), dominant_failure, next_smallest_change, and verdict. '
                  'Give concrete visual evidence and uncertainty. Scores are advisory, not user acceptance.')
        images = record['input_images'] + [image_record(folder / 'output.png', 'candidate group output', len(record['input_images']) + 1)]
    prompt = 'Evaluate the candidate and return JSON. User arrangement/request: ' + record['user_prompt'] + '\n' + '\n'.join(
        f'Image {i}: {im["role"]}' for i, im in enumerate(images, 1))
    reply = vision(system, prompt, images, folder, 'critic', max_tokens=3500)
    raw = reply['output'].strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    result = json.loads(raw)
    result['_meta'] = dict(requested_model=ASTRA, returned_model=None, provider='fal.ai via OpenRouter',
                           system_prompt=system, request_prompt=prompt, input_images=images,
                           usage=reply.get('usage'), time=utc(), reasoning_effort=None)
    save(folder / 'judge.json', result)
    print('JUDGED ' + run_id + ': ' + str(result.get('verdict')), flush=True)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['generate', 'judge'])
    parser.add_argument('--kind', choices=['refraction', 'composition'], required=True)
    parser.add_argument('--cases', nargs='+', required=True, help='Case IDs for generation; run IDs for judging')
    parser.add_argument('--version')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if args.action == 'generate' and not args.version:
        parser.error('--version required for generation')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(generate, args.kind, case, args.version) if args.action == 'generate'
                   else pool.submit(judge, args.kind, case) for case in args.cases]
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == '__main__':
    main()
