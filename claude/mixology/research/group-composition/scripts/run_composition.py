"""Bounded composition research: Astra rewrite and unchanged imagegen CLI edit.

Run one explicitly selected case/version. The caller must confirm model readiness.
No image SDK calls are made here; image generation uses the installed skill CLI.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

from foundry_aws_gateway import llm
from PIL import Image

TOPIC = Path('/home/colligo/hs_scripts/claude/mixology/research/group-composition')
SOURCE = Path('/home/colligo/mixology_data/refraction_research_2026-10-19/assets/ref_inputs')
ORIGINAL_SOURCE = Path('/home/colligo/mixology_data/source_restored_2026-10-19/ref_inputs')
RUNS = Path('/home/colligo/mixology_data/refraction_research_2026-10-19/composition/runs')
CLI = Path('/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py')
INPUTS = [
    ('315fb11e7cc94ecf8103ee2cf98227ae.png', 'clear drink with red upper layer'),
    ('6b61ea2d3b3f46959c6a0403879f8299.png', 'red iced drink'),
    ('b82dd27cd8c4471ea84aa21f9878e980.png', 'amber iced drink'),
    ('edbf33f823b842df9cd34393caea6cca.png', 'dark cola with red syrup'),
    ('TCCC–Crafted-Sept-2026.png', 'upright orange drink with red syrup'),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    os.umask(0o077)
    logging.disable(logging.CRITICAL)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', choices=['v1', 'v2'], required=True)
    parser.add_argument('--case', choices=['side_by_side', 'staggered'], required=True)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    case = json.loads((TOPIC / 'cases.json').read_text())[args.case]
    folder = RUNS / f'{args.version}_{args.case}'
    folder.mkdir(parents=True, exist_ok=True)
    record_path = folder / 'record.json'
    if record_path.exists():
        old = json.loads(record_path.read_text())
        if old['status'] == 'complete':
            print(f'SKIP completed {folder.name}', flush=True)
            return
        if old['status'] != 'prepared' or (folder / 'output.png').exists():
            raise RuntimeError('Existing attempt requires explicit review before retry')
    system = (TOPIC / 'prompts' / f'system_{args.version}.md').read_text()
    input_images = []
    content = [{'type': 'input_text', 'text': case['user_prompt']}]
    for index, (filename, identifier) in enumerate(INPUTS, 1):
        source = SOURCE / filename
        expected = ('152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da'
                    if index == 5 else digest(ORIGINAL_SOURCE / filename))
        assert digest(source) == expected, 'Staged source must match the recorded original'
        role = f'Image {index}: authoritative compositing input for one finished drink, {identifier}'
        with Image.open(source) as im:
            dimensions = list(im.size)
        input_images.append({'path': str(source), 'role': role, 'sha256': digest(source),
                             'dimensions': dimensions, 'image_index': index,
                             'original_source': str(source if index == 5 else ORIGINAL_SOURCE / filename)})
        content.extend([{'type': 'input_text', 'text': role},
                        {'type': 'input_image', 'image_url': 'data:image/png;base64,' +
                         base64.b64encode(source.read_bytes()).decode()}])
    record = {'id': folder.name, 'version': args.version, 'case_id': args.case,
              'case': case, 'status': 'prepared', 'prepared_at': utc(),
              'input_images': input_images, 'system_prompt': system,
              'user_prompt': case['user_prompt'], 'image_prompt': None,
              'rewriter_model': 'gpt-6-astra', 'image_model': 'gpt-image-2.5-sunburst',
              'quality': 'high', 'size_requested': '1536x1024',
              'output': str(folder / 'output.png'), 'output_dimensions': None,
              'output_sha256': None, 'image_seconds': None,
              'cli_path': str(CLI), 'cli_sha256': digest(CLI),
              'script_sha256': digest(Path(__file__)),
              'generation_mode': 'unchanged bundled imagegen CLI, edit, no augmentation',
              'scope': 'composition only; no added refractions; no auxiliary images',
              'visual_review': None}
    (folder / 'system_prompt.md').write_text(system)
    (folder / 'user_prompt.txt').write_text(case['user_prompt'] + '\n')
    save(record_path, record)
    if args.prepare_only:
        print(f'PREPARED {folder.name}: {len(input_images)} ordered source images', flush=True)
        return
    start = time.monotonic()
    try:
        record.update(status='rewrite_running', started_at=utc())
        save(record_path, record)
        client = llm.get_openai().with_options(timeout=180, max_retries=1)
        before = time.monotonic()
        response = client.responses.create(
            model='gpt-6-astra', reasoning={'effort': 'medium'}, max_output_tokens=2600,
            instructions=system, input=[{'role': 'user', 'content': content}])
        prompt = response.output_text.strip()
        if response.status != 'completed' or not prompt:
            raise RuntimeError('Rewriter did not complete')
        record['rewriter'] = {
            'returned_model': response.model, 'request_id': response._request_id,
            'response_id': response.id, 'reasoning_effort': 'medium',
            'max_output_tokens': 2600, 'seconds': round(time.monotonic() - before, 2),
            'usage': response.usage.model_dump(mode='json') if response.usage else None,
            'image_roles': [im['role'] for im in input_images]}
        (folder / 'image_prompt.txt').write_text(prompt + '\n')
        record.update(image_prompt=prompt, status='image_running')
        save(record_path, record)
        print(f'IMAGE {folder.name}: rewritten prompt {len(prompt.split())} words', flush=True)
        credentials = llm.get_openai()
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = credentials.api_key
        env['OPENAI_BASE_URL'] = str(credentials.base_url)
        if credentials.project:
            env['OPENAI_PROJECT_ID'] = credentials.project
        command = [sys.executable, str(CLI), 'edit', '--model', record['image_model']]
        for im in input_images:
            command += ['--image', im['path']]
        command += ['--prompt-file', str(folder / 'image_prompt.txt'), '--quality', 'high',
                    '--size', record['size_requested'], '--output-format', 'png',
                    '--out', str(folder / 'output.png'), '--no-augment']
        record['cli_argv'] = command
        save(record_path, record)
        before = time.monotonic()
        process = subprocess.run(command, env=env, capture_output=True, text=True, timeout=480)
        log = (process.stdout + '\n' + process.stderr).replace(credentials.api_key, '[REDACTED]')
        (folder / 'image_cli.log').write_text(log)
        record.update(cli_returncode=process.returncode,
                      image_seconds=round(time.monotonic() - before, 2))
        if process.returncode:
            raise RuntimeError('Image CLI failed; inspect sanitized log')
        with Image.open(folder / 'output.png') as im:
            im.load()
            record.update(output_dimensions=list(im.size), output_mode=im.mode)
        if digest(CLI) != record['cli_sha256']:
            raise RuntimeError('Bundled CLI changed during execution')
        record.update(status='complete', completed_at=utc(),
                      total_seconds=round(time.monotonic() - start, 2),
                      output_sha256=digest(folder / 'output.png'))
        save(record_path, record)
        print(f'DONE {folder.name}: {record["output_dimensions"]}, {record["image_seconds"]} seconds', flush=True)
    except Exception as exc:
        record.update(status='failed', failed_at=utc(), error_type=type(exc).__name__,
                      error_status=getattr(exc, 'status_code', None))
        save(record_path, record)
        print(f'FAILED {folder.name}: {type(exc).__name__}', flush=True)
        raise


if __name__ == '__main__':
    main()
