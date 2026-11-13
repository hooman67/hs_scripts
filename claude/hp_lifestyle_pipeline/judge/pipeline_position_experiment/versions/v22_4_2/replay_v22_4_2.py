#!/usr/bin/env python3
"""Read-only V22.4.2 replay over frozen calibration and smoke artifacts."""
from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import sys

import cv2
import numpy as np

PROJECT = Path('/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline')
ROOT = PROJECT / 'judge/pipeline_position_experiment'
OUT = ROOT / 'versions/v22_4_2'
PACKAGE = Path('/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25')
sys.path.insert(0, str(PACKAGE))
from hp3p.invariants import (  # noqa: E402
    GUARD_VERSION,
    TEXTURELESS_THRESHOLDS,
    _assess_fixed_textureless,
    assess_product_affine,
)

FROZEN_CALIBRATION = ROOT / 'versions/v22_4/textureless_guard_calibration_v3.json'
FULL8 = ROOT / 'smoke/v22_4_1_guard'
FAILED = ROOT / 'full160_v22_4_1/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1'
V22_4_1_SOURCE = OUT / 'pre_v22_4_2_snapshot/invariants_v22_4_1.py'

spec = importlib.util.spec_from_file_location('invariants_v22_4_1_frozen', V22_4_1_SOURCE)
v22_4_1 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(v22_4_1)


def load(path: Path):
    return json.loads(path.read_text())


def gray(path: Path):
    value = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if value is None:
        raise RuntimeError(f'cannot read {path}')
    return value


def alpha(path: Path):
    value = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if value is None or value.ndim != 3 or value.shape[2] != 4:
        raise RuntimeError(f'not RGBA: {path}')
    return value[:, :, 3] > 127


def composite(guide, mask, matrix, *, solid=None):
    height, width = guide.shape
    background = np.full_like(guide, 210)
    source = np.full_like(guide, solid, dtype=np.uint8) if solid is not None else guide
    moved = cv2.warpAffine(source, matrix, (width, height), flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=210)
    moved_mask = cv2.warpAffine(mask.astype(np.uint8) * 255, matrix, (width, height),
                                flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT,
                                borderValue=0) > 0
    background[moved_mask] = moved[moved_mask]
    return background


def compare_metric(actual, expected):
    keys = [
        'translation_x_px', 'translation_y_px', 'boundary_edge_coverage_2px',
        'boundary_distance_p90_px', 'internal_edge_coverage_2px',
        'internal_distance_p90_px', 'highpass_ncc', 'source_boundary_samples',
        'source_internal_edge_samples', 'source_appearance_samples',
    ]
    for key in keys:
        a, e = actual[key], expected[key]
        if isinstance(e, float):
            if abs(a - e) > 5e-5:
                return False, f'{key}: {a} != {e}'
        elif a != e:
            return False, f'{key}: {a} != {e}'
    return True, None


def replay_real(calibration):
    rows = []
    for frozen in calibration['real']:
        audit_path = Path(frozen['path'])
        row = audit_path.parent
        attempt = frozen['attempt']
        audit = load(audit_path)
        arguments = (
            (row / 'geometry_guide.png').read_bytes(),
            (row / f'gpt_{attempt}.png').read_bytes(),
            audit['product_bounds_px'],
        )
        keywords = dict(
            fixed_position=frozen['fixed_position'],
            product_mask=(row / 'mask.png').read_bytes(),
        )
        baseline = v22_4_1.assess_product_affine(*arguments, **keywords)
        result = assess_product_affine(*arguments, **keywords)
        rows.append({
            'path': str(audit_path), 'v22_4_1': baseline['verdict'], 'v22_4_2': result['verdict'],
            'persisted_label': frozen['label'],
            'primary_reasons': result.get('primary_reasons', result.get('reasons')),
            'fallback': result.get('textureless_fallback'),
            'dispatch_unchanged': result['verdict'] == baseline['verdict'],
        })
    return rows


def fixture_sources(calibration):
    values = {}
    for frozen in calibration['real']:
        if not frozen['fixed_position']:
            continue
        row = Path(frozen['path']).parent
        key = row.name.split('__retained_control')[0].split('__relocation_demand')[0]
        values.setdefault(key, (row / 'geometry_guide.png', row / 'mask.png'))
    return values


def replay_synthetic(calibration):
    fixtures = fixture_sources(calibration)
    rows = []
    for frozen in calibration['synthetic']:
        guide_path, mask_path = fixtures[frozen['fixture']]
        guide, mask = gray(guide_path), alpha(mask_path)
        matrix = np.asarray(frozen['matrix'], np.float32)
        transform = frozen['transform']
        if transform == 'brightness_shift':
            adjusted = np.clip(guide.astype(np.float32) * .72 + 24, 0, 255).astype(np.uint8)
            output = composite(adjusted, mask, matrix)
        else:
            output = composite(guide, mask, matrix, solid=28 if transform == 'solid_dark_product' else None)
        result = _assess_fixed_textureless(guide, output, mask)
        metrics_match, metric_error = compare_metric(result, frozen['metrics'])
        rows.append({
            'fixture': frozen['fixture'], 'transform': transform, 'expected': frozen['label'],
            'actual': result['verdict'], 'verdict_match': result['verdict'] == frozen['label'],
            'metrics_match_frozen': metrics_match, 'metric_error': metric_error,
            'metrics': result,
        })
    return rows


def replay_row(row: Path, assess=assess_product_affine):
    saved = load(row / 'result.json')
    fixed = saved['guide_density_class'] == 'HIGH-FILL/CLOSE'
    attempts = []
    for image in sorted(row.glob('gpt_*.png')):
        number = int(image.stem.split('_')[-1])
        result = assess(
            (row / 'geometry_guide.png').read_bytes(), image.read_bytes(),
            saved['guide_info']['product_bounds_px'], fixed_position=fixed,
            product_mask=(row / 'mask.png').read_bytes(),
        )
        attempts.append({'attempt': number, 'verdict': result['verdict'], 'reasons': result['reasons'],
                         'primary_reasons': result.get('primary_reasons'),
                         'fallback': result.get('textureless_fallback')})
    selected = next((item['attempt'] for item in attempts if item['verdict'] == 'pass'), None)
    return {'row': row.name, 'fixed_position': fixed,
            'saved_selected_attempt': saved.get('product_invariant_guard', {}).get('selected_attempt'),
            'replayed_selected_attempt': selected, 'attempts': attempts}


def main():
    calibration = load(FROZEN_CALIBRATION)
    real = replay_real(calibration)
    synthetic = replay_synthetic(calibration)
    failed_baseline = replay_row(FAILED, v22_4_1.assess_product_affine)
    failed = replay_row(FAILED)
    full8 = [replay_row(path.parent) for path in sorted(FULL8.rglob('result.json'))]
    result = {
        'version': 'v22.4.2-dispatch-replay-v1',
        'guard_version': GUARD_VERSION,
        'thresholds': TEXTURELESS_THRESHOLDS,
        'source_calibration': str(FROZEN_CALIBRATION),
        'calibration': {
            'real_attempts': len(real),
            'real_dispatch_changes': sum(not row['dispatch_unchanged'] for row in real),
            'synthetic_attempts': len(synthetic),
            'synthetic_false_accepts': sum(row['expected']=='fail' and row['actual']=='pass' for row in synthetic),
            'synthetic_false_rejects': sum(row['expected']=='pass' and row['actual']=='fail' for row in synthetic),
            'synthetic_metric_mismatches': sum(not row['metrics_match_frozen'] for row in synthetic),
            'real': real,
            'synthetic': synthetic,
        },
        'failed_v22_4_1_first_row_baseline_replay': failed_baseline,
        'failed_v22_4_1_first_row': failed,
        'prior_full8': full8,
        'prior_full8_selection_mismatches': sum(
            row['saved_selected_attempt'] != row['replayed_selected_attempt'] for row in full8),
    }
    (OUT / 'replay_results.json').write_text(json.dumps(result, indent=2) + '\n')
    summary = {
        'guard_version': GUARD_VERSION,
        'calibration': {key:value for key,value in result['calibration'].items() if key not in {'real','synthetic'}},
        'failed_first_row': failed,
        'full8_rows': len(full8),
        'full8_selection_mismatches': result['prior_full8_selection_mismatches'],
    }
    print(json.dumps(summary, indent=2))
    assert result['calibration']['real_dispatch_changes'] == 0
    assert result['calibration']['synthetic_false_accepts'] == 0
    assert result['calibration']['synthetic_false_rejects'] == 0
    assert result['calibration']['synthetic_metric_mismatches'] == 0
    assert failed['replayed_selected_attempt'] == 2
    assert result['prior_full8_selection_mismatches'] == 0

if __name__ == '__main__':
    main()
