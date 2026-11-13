import json

import cv2
import numpy as np

from hp3p.invariants import _assess_fixed_textureless, assess_product_affine


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


def _textureless_fixture():
    source = np.full((600, 800), 210, np.uint8)
    alpha = np.zeros_like(source, np.uint8)
    polygon = np.asarray([[240, 190], [560, 190], [540, 390], [260, 390]], np.int32)
    cv2.fillConvexPoly(alpha, polygon, 255)
    source[alpha > 0] = 38
    cv2.rectangle(source, (375, 265), (425, 315), 75, 4)
    cv2.line(source, (280, 355), (520, 355), 82, 3)
    return source, alpha > 0


def _move_product(source, alpha, matrix, *, solid=None):
    height, width = source.shape
    product = np.full_like(source, solid) if solid is not None else source
    moved_product = cv2.warpAffine(product, np.asarray(matrix, np.float32), (width, height),
                                   borderValue=210)
    moved_alpha = cv2.warpAffine(alpha.astype(np.uint8), np.asarray(matrix, np.float32),
                                 (width, height), flags=cv2.INTER_NEAREST, borderValue=0) > 0
    output = np.full_like(source, 210)
    output[moved_alpha] = moved_product[moved_alpha]
    return output


def test_alpha_textureless_fallback_accepts_exact_shape_with_bounded_translation():
    source, alpha = _textureless_fixture()
    moved = _move_product(source, alpha, [[1, 0, 8], [0, 1, -8]])
    result = _assess_fixed_textureless(source, moved, alpha)
    assert result["verdict"] == "pass"
    assert result["translation_x_px"] == 8
    assert result["translation_y_px"] == -8


def test_alpha_textureless_fallback_rejects_scale_rotation_shear_and_dark_blob():
    source, alpha = _textureless_fixture()
    center = (400, 290)
    invalid = [
        cv2.getRotationMatrix2D(center, 0, 0.96),
        cv2.getRotationMatrix2D(center, 2, 1),
        np.float32([[1, 0.06, -0.06 * center[1]], [0, 1, 0]]),
    ]
    for matrix in invalid:
        result = _assess_fixed_textureless(source, _move_product(source, alpha, matrix), alpha)
        assert result["verdict"] == "fail"
    dark = _assess_fixed_textureless(
        source, _move_product(source, alpha, [[1, 0, 0], [0, 1, 0]], solid=28), alpha,
    )
    assert dark["verdict"] == "fail"
    assert dark["checks"]["internal_structure_floor"] is False
