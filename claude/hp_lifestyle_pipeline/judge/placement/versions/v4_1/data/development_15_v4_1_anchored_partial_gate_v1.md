# development-15-v4-1-anchored-astra development evaluation

- Completed OK: 7 / 15
- Verdict match: 1 / 6
- V3 verdict match on the same completed labeled cases: 0 / 6
- Expected-issue detection: 0 / 6

Two comments without an explicit absolute verdict are excluded from verdict accuracy. Missing comments are never inferred as passes. Model outputs were not edited.

| Record | Human verdict | V4 | Match | Expected issue(s) | Observed issue(s) |
|---|---:|---:|---:|---|---|
| elitebook__laptop_FrontLeftMedium__p1 | review | pass | False | chair_displacement | none |
| tassel__printer_FrontWide__p1 | fail | pass | False | malformed_support_furniture, misplaced_support_furniture | none |
| cashmere__laptop_FrontLeftMedium__p1 | review | review | True | chair_displacement | missing_required_support |
| tassel__printer_FrontCloseUp__p1 | fail | pass | False | misplaced_support_furniture | none |
| elitebook__laptop_FrontCloseUp__p1 | review | pass | False | none specified | none |
| tassel__printer_FrontRightCloseUp__p1 | unlabeled | pass | None | conflicting_perspective | none |
| magic__printer_FrontLeftMedium__p1 | fail | pass | False | missing_required_support | none |
| tassel__printer_FrontLeftMedium__p2 | fail | missing | None | unmotivated_device_position | none |
| elitebook__laptop_FrontLeftMedium__p2 | fail | missing | None | missing_required_support | none |
| elitebook__laptop_FrontWide__p2 | pass | missing | None | furniture_layout_conflict | none |
| tassel__printer_FrontCloseUp__p2 | fail | missing | None | device_support_axis_conflict, incoherent_prop_arrangement | none |
| magic__printer_FrontRightCloseUp__p2 | pass | missing | None | unrelated_rendering_artifact | none |
| tassel__printer_FrontRightCloseUp__p2 | fail | missing | None | misplaced_support_furniture, incoherent_prop_arrangement | none |
| elitebook__laptop_BackRightCloseUp__p3 | unlabeled | missing | None | none specified | none |
| elitebook__laptop_FrontLeftMedium__p3 | pass | missing | None | none specified | none |

## Expected-issue detection by cluster

- chair_calibration: 0 / 2
- support_geometry_layout: 0 / 4
- device_position_orientation: 0 / 0
- prop_coherence: 0 / 0
- artifact_scope: 0 / 0
