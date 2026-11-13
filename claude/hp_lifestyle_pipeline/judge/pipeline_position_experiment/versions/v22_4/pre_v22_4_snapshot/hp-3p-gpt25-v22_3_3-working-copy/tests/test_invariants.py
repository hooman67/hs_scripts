import json

import cv2
import numpy as np

from hp3p.invariants import assess_product_affine


def _fixture(matrix=None):
    rng = np.random.default_rng(7)
    guide = np.full((600, 800, 3), 245, np.uint8)
    texture = rng.integers(0, 220, (240, 320, 3), np.uint8)
    cv2.rectangle(texture, (15, 15), (305, 225), (10, 10, 10), 5)
    cv2.line(texture, (20, 200), (295, 35), (250, 250, 250), 7)
    guide[160:400, 220:540] = texture
    if matrix is None:
        output = guide.copy()
    else:
        output = cv2.warpAffine(guide, np.asarray(matrix, np.float32), (800, 600),
                                flags=cv2.INTER_LINEAR, borderValue=(245, 245, 245))
    return cv2.imencode(".png", guide)[1].tobytes(), cv2.imencode(".png", output)[1].tobytes()


def test_full_affine_guard_accepts_exact_and_lower_fill_translation_but_locks_high_fill():
    guide, exact = _fixture()
    result = assess_product_affine(guide, exact, [220, 160, 540, 400], fixed_position=True)
    assert result["verdict"] == "pass"
    assert len(result["full_affine_matrix"]) == 2 and len(result["singular_values"]) == 2
    guide, moved = _fixture([[1, 0, 110], [0, 1, -35]])
    assert assess_product_affine(guide, moved, [220, 160, 540, 400], fixed_position=False)["verdict"] == "pass"
    locked = assess_product_affine(guide, moved, [220, 160, 540, 400], fixed_position=True)
    assert locked["verdict"] == "fail"
    assert "fixed_translation_x" in locked["reasons"]


def test_full_affine_guard_rejects_scale_and_shear():
    guide, scaled = _fixture([[0.94, 0, 20], [0, 0.94, 20]])
    scale = assess_product_affine(guide, scaled, [220, 160, 540, 400], fixed_position=False)
    assert scale["verdict"] == "fail"
    assert "singular_min" in scale["reasons"]
    guide, sheared = _fixture([[1, 0.08, 0], [0, 1, 0]])
    shear = assess_product_affine(guide, sheared, [220, 160, 540, 400], fixed_position=False)
    assert shear["verdict"] == "fail"
    assert "anisotropy" in shear["reasons"] or "shear" in shear["reasons"]


def test_guard_results_are_strict_json_round_trip_for_pass_fail_and_unverifiable():
    guide, exact = _fixture()
    passing = assess_product_affine(guide, exact, [220, 160, 540, 400], fixed_position=True)
    guide, scaled = _fixture([[0.94, 0, 20], [0, 0.94, 20]])
    failing = assess_product_affine(guide, scaled, [220, 160, 540, 400], fixed_position=False)
    blank = cv2.imencode(".png", np.full((600, 800, 3), 245, np.uint8))[1].tobytes()
    unverifiable = assess_product_affine(blank, blank, [220, 160, 540, 400], fixed_position=True)

    assert passing["verdict"] == "pass"
    assert failing["verdict"] == "fail"
    assert unverifiable["verdict"] == "unverifiable"
    for result in (passing, failing, unverifiable):
        assert json.loads(json.dumps(result)) == result
