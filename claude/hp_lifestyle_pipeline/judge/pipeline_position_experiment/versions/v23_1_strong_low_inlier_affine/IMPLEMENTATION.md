# V23.1 implementation freeze

**Implemented:** 2026-11-06  
**Status:** source tests passed; fresh pilot pending

The calibrated strong-low-inlier path is integrated into the isolated Foundry checkout:

`/home/colligo/foundry-pr4349-position-exp`

It retains the ordinary 20-inlier requirement. A 17--19-inlier fit may be accepted only when its
inlier ratio is at least 0.70, source spans are at least 0.70 horizontally and 0.60 vertically,
all four quadrants are covered, source hull coverage is at least 0.25, and every existing
non-count invariant passes. In fixed-recovery mode, the fixed-translation checks are also
mandatory. The exception is recorded explicitly in each guard audit.

## Frozen source identity

| File | SHA-256 |
|---|---|
| `hp3p/invariants.py` | `808bde48be35ba6093dc01d0cc23808f0c7f4509b62e79dce64d1033674c19a6` |
| `hp3p/pipeline.py` | `ef1158a882dca0c8a85d01e3ed427d036282b29341fa5beeb88c9d4db39d9137` |
| `hp3p/prompts/system_3p.txt` | `324ce0e449804bc0d17ac0cf5ed10587716bc9d7e6ef72b9a91e439745b6aaec` |
| `tests/test_invariants.py` | `1e155becabbb90be7e543f78972dedb80ef110c41308491ab40601d4109f946e` |
| `tests/test_pipeline.py` | `a642dede710b6c54ce626cec304e5ac06acd553c7abf70431a7b2779c425905e` |
| `tests/test_prompts.py` | `8c09e3404b7e867cac1b3a502ecaf9e8095d51f68cb4539fc3d0ff16c92cfc5b` |

Pipeline version:

`unified-blue-scale-v23.1-all-view-rigid-translation-strong-low-inlier-twin-camera-guide-only-no-edit-mask`

## Verification

- Full package: **180 passed**.
- Ruff `F`, `E9`, and import-order checks: passed.
- Python compilation: passed.
- `git diff --check`: passed.
- Preserved Tassel printer-wide attempts: both pass primary affine verification; the first attempt
  is selected and neither dispatches to the alpha fallback.
- Full candidate calibration: frozen 110/110 and added 82/82 with zero false accepts/rejects; zero
  changes among prior V23 run-3 decisions or selections.

Calibration report:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/CALIBRATION_REPORT.md`

The next gate is a fresh eight-cell pilot: four representative V6.1 laptop/printer close/wide
rows plus four explicit relocation-demand diagnostics. This distinguishes ordinary scene behavior
from the executable contract's ability to preserve view and scale under material x-y movement.
