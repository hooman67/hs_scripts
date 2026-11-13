# Residual-p95 threshold sensitivity

Predeclared comparison of 3.2, 3.5, and 4.0 px. Every other frozen full-affine threshold remains unchanged. HIGH-FILL calibration rows and fixed-position fallback attempts also retain the ±8 px x/y translation gate.

| Threshold | Calibration accepted passed | Calibration rejected rejected | False rejects | False accepts | New attempt 1 | New fixed fallback |
|---:|---:|---:|---:|---:|---|---|
| 3.2 | 15/15 | 13/13 | 0 | 0 | FAIL (residual_p95) | FAIL (fixed_translation_x) |
| 3.5 | 15/15 | 13/13 | 0 | 0 | PASS | FAIL (fixed_translation_x) |
| 4.0 | 15/15 | 13/13 | 0 | 0 | PASS | FAIL (fixed_translation_x) |

## Row-level calibration outcomes

| Label | Version | Row | p95 px | 3.2 | 3.5 | 4.0 |
|---|---|---|---:|---|---|---|
| rejected | v22 | `cashmere__laptop_FrontCloseUp__p1__relocation_demand` | 2.457 | FAIL: singular_min, fixed_translation_x, fixed_translation_y | FAIL: singular_min, fixed_translation_x, fixed_translation_y | FAIL: singular_min, fixed_translation_x, fixed_translation_y |
| rejected | v22 | `cashmere__laptop_FrontCloseUp__p1__retained_control` | 3.746 | FAIL: singular_min, residual_p95, fixed_translation_x, fixed_translation_y | FAIL: singular_min, residual_p95, fixed_translation_x, fixed_translation_y | FAIL: singular_min, fixed_translation_x, fixed_translation_y |
| accepted | v22 | `cashmere__laptop_FrontWide__p1__relocation_demand` | 2.829 | PASS | PASS | PASS |
| accepted | v22 | `cashmere__laptop_FrontWide__p1__retained_control` | 2.008 | PASS | PASS | PASS |
| rejected | v22 | `magic__printer_FrontCloseUp__p1__relocation_demand` | 2.253 | FAIL: singular_min, fixed_translation_x | FAIL: singular_min, fixed_translation_x | FAIL: singular_min, fixed_translation_x |
| rejected | v22 | `magic__printer_FrontCloseUp__p1__retained_control` | 2.489 | FAIL: inlier_ratio, singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull, fixed_translation_x | FAIL: inlier_ratio, singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull, fixed_translation_x | FAIL: inlier_ratio, singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull, fixed_translation_x |
| rejected | v22 | `magic__printer_FrontWide__p1__relocation_demand` | 1.813 | FAIL: singular_max, anisotropy, rotation | FAIL: singular_max, anisotropy, rotation | FAIL: singular_max, anisotropy, rotation |
| rejected | v22 | `magic__printer_FrontWide__p1__retained_control` | 2.941 | FAIL: singular_max, anisotropy, shear, span_y, quadrants | FAIL: singular_max, anisotropy, shear, span_y, quadrants | FAIL: singular_max, anisotropy, shear, span_y, quadrants |
| rejected | v22_1 | `cashmere__laptop_FrontCloseUp__p1__relocation_demand` | 3.046 | FAIL: singular_min, fixed_translation_x, fixed_translation_y | FAIL: singular_min, fixed_translation_x, fixed_translation_y | FAIL: singular_min, fixed_translation_x, fixed_translation_y |
| accepted | v22_1 | `cashmere__laptop_FrontCloseUp__p1__retained_control` | 2.242 | PASS | PASS | PASS |
| rejected | v22_1 | `cashmere__laptop_FrontWide__p1__relocation_demand` | 2.299 | FAIL: singular_min | FAIL: singular_min | FAIL: singular_min |
| accepted | v22_1 | `cashmere__laptop_FrontWide__p1__retained_control` | 1.749 | PASS | PASS | PASS |
| rejected_position_under_new_policy | v22_1 | `magic__printer_FrontCloseUp__p1__relocation_demand` | 1.556 | FAIL: fixed_translation_x | FAIL: fixed_translation_x | FAIL: fixed_translation_x |
| accepted | v22_1 | `magic__printer_FrontCloseUp__p1__retained_control` | 1.905 | PASS | PASS | PASS |
| accepted | v22_1 | `magic__printer_FrontWide__p1__relocation_demand` | 1.281 | PASS | PASS | PASS |
| accepted | v22_1 | `magic__printer_FrontWide__p1__retained_control` | 1.162 | PASS | PASS | PASS |
| accepted | v22_2 | `cashmere__laptop_FrontCloseUp__p1__relocation_demand` | 2.366 | PASS | PASS | PASS |
| accepted | v22_2 | `cashmere__laptop_FrontCloseUp__p1__retained_control` | 2.511 | PASS | PASS | PASS |
| rejected | v22_2 | `cashmere__laptop_FrontWide__p1__relocation_demand` | 2.260 | FAIL: singular_min | FAIL: singular_min | FAIL: singular_min |
| accepted | v22_2 | `magic__printer_FrontCloseUp__p1__relocation_demand` | 2.268 | PASS | PASS | PASS |
| accepted | v22_2 | `magic__printer_FrontCloseUp__p1__retained_control` | 2.477 | PASS | PASS | PASS |
| rejected | v22_2 | `magic__printer_FrontWide__p1__relocation_demand` | 2.004 | FAIL: singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull | FAIL: singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull | FAIL: singular_min, singular_max, anisotropy, rotation, shear, span_y, quadrants, hull |
| accepted | v22_2_1 | `cashmere__laptop_FrontCloseUp__p1__relocation_demand` | 2.459 | PASS | PASS | PASS |
| accepted | v22_2_1 | `cashmere__laptop_FrontCloseUp__p1__retained_control` | 2.064 | PASS | PASS | PASS |
| rejected | v22_2_1 | `cashmere__laptop_FrontWide__p1__relocation_demand` | 2.840 | FAIL: singular_min | FAIL: singular_min | FAIL: singular_min |
| accepted | v22_2_1 | `magic__printer_FrontCloseUp__p1__relocation_demand` | 1.967 | PASS | PASS | PASS |
| accepted | v22_2_1 | `magic__printer_FrontCloseUp__p1__retained_control` | 1.742 | PASS | PASS | PASS |
| rejected | v22_2_1 | `magic__printer_FrontWide__p1__relocation_demand` | 2.438 | FAIL: singular_max, rotation | FAIL: singular_max, rotation | FAIL: singular_max, rotation |
| unlabeled_new_attempt | v22_3_1 | `cashmere__laptop_FrontWide__p1__relocation_demand__attempt1` | 3.242 | FAIL: residual_p95 | PASS | PASS |
| unlabeled_new_attempt | v22_3_1 | `cashmere__laptop_FrontWide__p1__relocation_demand__attempt2` | 2.423 | FAIL: fixed_translation_x | FAIL: fixed_translation_x | FAIL: fixed_translation_x |
