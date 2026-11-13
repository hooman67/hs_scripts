# Independent names-only component check

Generated: `2026-11-05T23:57:54.073042+00:00`

Coverage: 10 cases and 13 component assessments; no missing records.

This is an explicitly inspected development probe. It is not held-out validation and makes no merge or promotion decision.

## Direction counts

- `clear_nonmaterial->clear_nonmaterial`: 3
- `clear_nonmaterial->material`: 1
- `material->clear_nonmaterial`: 4
- `material->material`: 4
- `unknown->material`: 1

## Component comparisons

| Case | Component | Earlier | Names-only | Direction |
|---|---|---:|---:|---|
| cashmere__laptop_FrontLeftMedium__p6 | access_usability | material (s=2, medium) | material (s=2, medium) | material->material |
| cashmere__laptop_FrontLeftMedium__p6 | orientation_alignment | material (s=2, medium) | material (s=2, medium) | material->material |
| tassel__printer_FrontCloseUp__p5 | support_scenario | clear_nonmaterial (s=0, high) | clear_nonmaterial (s=0, high) | clear_nonmaterial->clear_nonmaterial |
| cashmere__laptop_FrontCloseUp__p5 | access_usability | clear_nonmaterial (s=0, medium) | material (s=2, medium) | clear_nonmaterial->material |
| cashmere__laptop_FrontCloseUp__p5 | orientation_alignment | unknown (s=None, low) | material (s=2, medium) | unknown->material |
| magic__printer_FrontCloseUp__p3 | support_scenario | clear_nonmaterial (s=1, medium) | clear_nonmaterial (s=0, high) | clear_nonmaterial->clear_nonmaterial |
| magic__printer_FrontLeftMedium__p1 | support_scenario | clear_nonmaterial (s=1, medium) | clear_nonmaterial (s=0, medium) | clear_nonmaterial->clear_nonmaterial |
| tassel__printer_FrontLeftMedium__p6 | support_scenario | material (s=2, medium) | material (s=2, high) | material->material |
| cashmere__laptop_BackRightCloseUp__p9 | access_usability | material (s=3, high) | clear_nonmaterial (s=0, medium) | material->clear_nonmaterial |
| elitebook__laptop_BackRightCloseUp__p7 | orientation_alignment | material (s=2, high) | clear_nonmaterial (s=0, medium) | material->clear_nonmaterial |
| elitebook__laptop_BackRightCloseUp__p9 | access_usability | material (s=3, high) | clear_nonmaterial (s=0, high) | material->clear_nonmaterial |
| elitebook__laptop_BackRightCloseUp__p9 | orientation_alignment | material (s=2, high) | clear_nonmaterial (s=0, high) | material->clear_nonmaterial |
| magic__printer_FrontLeftMedium__p6 | support_scenario | material (s=2, high) | material (s=2, high) | material->material |
