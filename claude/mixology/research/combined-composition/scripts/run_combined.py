"""Bounded combined composition + V3-style refraction runs via existing FAL transport."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import sys

ROOT = Path('/home/colligo/hs_scripts/claude/mixology')
TOPIC = ROOT / 'research/combined-composition'
sys.path.insert(0, str(ROOT / 'research/model-access/scripts'))
import run_fal_experiments as base

SOURCES = list(base.INPUTS)
SOURCES[4] = ('TCCC–Crafted-Sept-2026.png', 'upright orange drink with red syrup')
STYLE = 'image_027_p10_xref1385.jpg'


def configuration(kind, case_id, version):
    case = json.loads((TOPIC / 'cases.json').read_text())[case_id]
    system = (TOPIC / 'prompts' / f'system_{version}.md').read_text()
    images = []
    for i, source_index in enumerate(case['input_indices'], 1):
        name, label = SOURCES[source_index - 1]
        path = base.RUN / 'assets/ref_inputs' / name
        images.append(base.image_record(path, f'DRINK: authoritative cup/contents source, {label}', i))
    if 5 in case['input_indices']:
        assert base.digest(base.RUN / 'assets/ref_inputs' / SOURCES[4][0]) == '152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da'
    images.append(base.image_record(base.RUN / 'assets' / STYLE,
        'STYLE ONLY: customer-approved V3 caustic texture/focal intensity/falloff; not another drink. Do not copy colors, objects, camera or projection placement.', len(images) + 1))
    folder = base.RUN / 'combined/runs' / f'{version}_{case_id}'
    return folder, dict(
        id=folder.name, version=version, kind=kind, case_id=case_id, case=case,
        system_version=version, system_prompt=system, user_prompt=case['user_prompt'],
        input_images=images, drink_count=len(images)-1, provider='fal.ai',
        fal_endpoint=base.IMAGE_ENDPOINT, rewriter_endpoint=base.VISION_ENDPOINT,
        rewriter_model='gpt-6-astra', rewriter_requested_model=base.ASTRA,
        image_model='gpt-image-2.5-sunburst', quality='high',
        size_requested='1536x1024', output_format='png', status='prepared',
        prepared_at=base.utc(), script_sha256=base.digest(__file__),
        transport_script_sha256=base.digest(Path(base.__file__)),
        generation_mode='FAL queue API; combined composition and V3-derived relighting',
        provider_limitations='Requested model identifiers; backend snapshot and Astra effort unexposed. reasoning=true; no automatic fallback requested.',
        output=str(folder / 'output.png'), visual_review=None)


def judge(run_id):
    folder = base.RUN / 'combined/runs' / run_id
    record = json.loads((folder / 'record.json').read_text())
    if record['status'] != 'complete':
        raise RuntimeError('Cannot judge an incomplete image')
    if (folder / 'judge.json').exists():
        print('SKIP judged ' + run_id, flush=True)
        return
    images = list(record['input_images'])
    images.append(base.image_record(folder / 'output.png', 'CANDIDATE combined output', len(images) + 1))
    system = (
        'Evaluate the candidate group against the ordered original drink images and STYLE-ONLY image. '
        'The style image is not an identity/geometry/color/camera authority. Assess cup count, individual '
        'rim/body/base proportions and upright surface contact, cream/ice/syrup identity, arrangement and framing; '
        'then V3 irregular branching focused-light texture versus veins/webs/stars, per-drink transmitted hue '
        'and opacity, one shared light direction, continuity from each cup onto its support-plane field, '
        'correct downstream direction and absence of invented wall/background caustics. Dark cola transmits '
        'less light than clear amber; opaque cream must stay opaque. Compare key direction requested by the user '
        'with actual shadows/projections. Look specifically for blue/pink leakage from the style image, '
        'neutralized or whitened liquid, a shared undifferentiated pool, floor patterns detached from their cups '
        'and a curved floor becoming a wall. Do not invent precise pixel measurements or ray-tracing evidence. '
        'Return only JSON with identity_score, geometry_score, arrangement_score, refraction_score, '
        'color_attribution_score, coherent_light_score, grounding_score (0-5), observations (list), '
        'per_drink_color_evidence (list), direction_evidence, dominant_failure, next_smallest_change and verdict. '
        'Scores are advisory, never customer approval; state uncertainty and partial occlusion.')
    prompt = ('User request: ' + record['user_prompt'] + '\nExpected key: ' + record['case']['key_direction']
              + '; projected fields: ' + record['case']['projection_direction'] + '.\n'
              + '\n'.join(f'Image {i}: {im["role"]}' for i, im in enumerate(images, 1)))
    response = base.vision(system, prompt, images, folder, 'critic', max_tokens=5000)
    raw = response['output'].strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    result = json.loads(raw)
    result['_meta'] = dict(requested_model=base.ASTRA, returned_model=None,
                           provider='fal.ai via OpenRouter', system_prompt=system,
                           request_prompt=prompt, input_images=images,
                           usage=response.get('usage'), time=base.utc(), reasoning_effort=None)
    base.save(folder / 'judge.json', result)
    print('JUDGED ' + run_id + ': ' + str(result.get('verdict')), flush=True)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['generate', 'judge'])
    parser.add_argument('--cases', nargs='+', required=True)
    parser.add_argument('--version', default='v1')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    base.configuration = configuration
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = [pool.submit(base.generate, 'combined', case, args.version) if args.action == 'generate'
                else pool.submit(judge, case) for case in args.cases]
        for future in concurrent.futures.as_completed(jobs):
            future.result()


if __name__ == '__main__':
    main()
