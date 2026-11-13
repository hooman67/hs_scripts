# development-15-v4-astra development evaluation

- Completed OK: 15 / 15
- Verdict match: 3 / 13
- V3 verdict match on the same completed labeled cases: 2 / 13
- Expected-issue detection: 0 / 12

Two comments without an explicit absolute verdict are excluded from verdict accuracy. Missing comments are never inferred as passes. Model outputs were not edited.

| Record | Human verdict | V4 | Match | Expected issue(s) | Observed issue(s) |
|---|---:|---:|---:|---|---|
| elitebook__laptop_FrontLeftMedium__p1 | review | review | True | chair_displacement | none |
| tassel__printer_FrontWide__p1 | fail | review | False | malformed_support_furniture, misplaced_support_furniture | none |
| cashmere__laptop_FrontLeftMedium__p1 | review | review | True | chair_displacement | none |
| tassel__printer_FrontCloseUp__p1 | fail | review | False | misplaced_support_furniture | none |
| elitebook__laptop_FrontCloseUp__p1 | review | review | True | none specified | none |
| tassel__printer_FrontRightCloseUp__p1 | unlabeled | review | None | conflicting_perspective | none |
| magic__printer_FrontLeftMedium__p1 | fail | review | False | missing_required_support | none |
| tassel__printer_FrontLeftMedium__p2 | fail | review | False | unmotivated_device_position | none |
| elitebook__laptop_FrontLeftMedium__p2 | fail | review | False | missing_required_support | none |
| elitebook__laptop_FrontWide__p2 | pass | review | False | furniture_layout_conflict | none |
| tassel__printer_FrontCloseUp__p2 | fail | review | False | device_support_axis_conflict, incoherent_prop_arrangement | none |
| magic__printer_FrontRightCloseUp__p2 | pass | review | False | unrelated_rendering_artifact | none |
| tassel__printer_FrontRightCloseUp__p2 | fail | review | False | misplaced_support_furniture, incoherent_prop_arrangement | none |
| elitebook__laptop_BackRightCloseUp__p3 | unlabeled | review | None | none specified | chair_displacement |
| elitebook__laptop_FrontLeftMedium__p3 | pass | review | False | none specified | none |

## Expected-issue detection by cluster

- chair_calibration: 0 / 2
- support_geometry_layout: 0 / 7
- device_position_orientation: 0 / 2
- prop_coherence: 0 / 2
- artifact_scope: 0 / 1
