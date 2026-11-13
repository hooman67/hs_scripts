"""Restore customer cup interiors over the shadow-free Sunburst background edit."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT = Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
FOLDER = RUN / 'input_cleanup/group_from_027_v1'
SOURCE = RUN / 'assets/image_027_p10_xref1385.jpg'
RAW = FOLDER / 'raw_sunburst.png'
OUTPUT = FOLDER / 'group_027_clean.png'
DESTINATION = RUN / 'assets/group_027_clean.png'
CLI = Path('/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUTPUT.exists() or DESTINATION.exists():
        raise FileExistsError('Preserve completed inputs; inspect before any rerun')
    source = Image.open(SOURCE).convert('RGB')
    raw = Image.open(RAW).convert('RGB')
    assert source.size == raw.size == (1402, 1122), 'Never silently resize source cups'
    a = np.asarray(raw).astype(np.int16)
    foreground = (a.min(axis=2) < 246) | ((a.max(axis=2) - a.min(axis=2)) > 8)
    mask = Image.fromarray((foreground * 255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
    selected = Image.new('L', raw.size, 0)
    # The overlapping cups form one connected silhouette; seed each cup defensively.
    for seed in [(500, 450), (800, 650), (1080, 400)]:
        assert mask.getpixel(seed) == 255, 'Seed must be inside a cup'
        component = mask.copy()
        ImageDraw.floodfill(component, seed, 128)
        selected = Image.fromarray(np.maximum(np.asarray(selected), (np.asarray(component) == 128).astype('uint8') * 255))
    filled = selected.copy()
    for point in [(0, 0), (1401, 0), (0, 1121), (1401, 1121)]:
        if filled.getpixel(point) == 0:
            ImageDraw.floodfill(filled, point, 128)
    filled = Image.fromarray((np.asarray(filled) != 128).astype('uint8') * 255)
    alpha = filled.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(0.7))
    result = Image.composite(source, raw, alpha)
    protected = np.asarray(alpha) == 255
    diff = np.abs(np.asarray(result).astype(np.int16) - np.asarray(source).astype(np.int16))
    assert not diff[protected].any(), 'Protected source pixels must remain exact'
    outside = np.asarray(filled.filter(ImageFilter.MaxFilter(17))) == 0
    b = np.asarray(result).astype(np.int16)
    checks = {
        'dimensions': list(result.size), 'source_and_output_same_dimensions': True,
        'fully_protected_pixels': int(protected.sum()),
        'protected_source_pixels_changed': int((diff[protected].max(axis=1) > 0).sum()),
        'background_pixels_checked': int(outside.sum()),
        'background_mean_rgb': [round(float(v), 3) for v in b[outside].mean(axis=0)],
        'background_pixels_chroma_gt_12': int(((b[outside].max(axis=1) - b[outside].min(axis=1)) > 12).sum()),
        'background_pixels_min_channel_lt_235': int((b[outside].min(axis=1) < 235).sum()),
    }
    assert checks['background_pixels_chroma_gt_12'] == 0
    assert checks['background_pixels_min_channel_lt_235'] == 0
    assert 0.15 < protected.mean() < 0.7, 'Plausibility check for foreground segmentation'
    result.save(OUTPUT)
    alpha.save(FOLDER / 'source_preservation_mask.png')
    filled.save(FOLDER / 'cup_silhouettes.png')
    prompt = PROJECT / 'prompts/clean_group_input_v1.txt'
    shutil.copy2(prompt, FOLDER / 'image_prompt.txt')
    (FOLDER / 'system_prompt.txt').write_text('No Astra rewriter/system prompt used. Direct background-cleanup image edit; frozen refraction system V3 was not applied.\n')
    record = {
        'id': 'group_from_027_v1', 'task': 'Remove external shadows/refractions from customer output 027',
        'status': 'complete', 'source': str(SOURCE), 'source_sha256': sha(SOURCE),
        'source_url': 'https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/assets/image_027_p10_xref1385.jpg',
        'model': 'gpt-image-2.5-sunburst', 'quality': 'high', 'size': 'auto', 'output_format': 'png',
        'system_prompt': None, 'image_prompt': prompt.read_text(), 'model_input_images': [str(SOURCE)],
        'model_input_mask': None, 'cli_sha256': sha(CLI), 'reported_image_seconds': 25.4,
        'raw_output': str(RAW), 'raw_sha256': sha(RAW), 'output': str(OUTPUT), 'output_sha256': sha(OUTPUT),
        'postprocessing': 'Extract connected cup silhouettes from the shadow-free raw edit; dilate 2px, erode 4px, feather 0.7px and restore original source pixels at fully opaque alpha. Generated cleanup retained at narrow boundaries.',
        'source_preservation_mask': str(FOLDER / 'source_preservation_mask.png'),
        'checks': checks, 'created_at': datetime.now(timezone.utc).isoformat(),
        'limitations': [
            'Derived from customer output 027, not an independently supplied original input.',
            'Pixel-exact preservation applies only to the saved fully opaque mask; narrow generated boundaries are not exact source pixels.',
            'Source camera, canvas and complete cup bases retained; no outpainting or reframing.',
        ],
        'visual_review': 'Pending final composite inspection; raw edit has clean white surroundings without external colored projections.',
    }
    (FOLDER / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
    shutil.copy2(OUTPUT, DESTINATION)
    print(json.dumps(checks))


if __name__ == '__main__':
    main()
