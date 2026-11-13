# V4.4 Gate A diagnostic

**Decision: REJECT V4.4; do not run fresh10 or 160.**

reused labeled development cases; diagnostic only, not accuracy estimate.

- Scoreable: 18/18 repeats; calls: 37 (1 repair).
- Verdict: 6/15 repeat-level; 2/5 majority case-level.
- Required issue recall: 4/21 repeat-level; 1/7 majority case-level.
- Precision-like: 4/4 predicted issue instances corresponded to required codes.
- Material fail recall: 0/9 repeats.
- Stability: verdict 5/6 cases; issue set 5/6 cases. Stability here mainly reflects stable false negatives.

| Case | Repeat verdicts | Repeat issues | Expected | Majority result |
|---|---|---|---|---|
| `elitebook__laptop_FrontLeftMedium__p1` | review, review, review | chair_displacement; chair_displacement; chair_displacement | review / chair_displacement | review / chair_displacement |
| `tassel__printer_FrontWide__p1` | pass, pass, review | none; none; misplaced_support_furniture | fail / misplaced_support_furniture, malformed_support_furniture | pass / none |
| `magic__printer_FrontLeftMedium__p1` | pass, pass, pass | none; none; none | fail / missing_required_support | pass / none |
| `tassel__printer_FrontCloseUp__p2` | pass, pass, pass | none; none; none | fail / device_support_axis_conflict, incoherent_prop_arrangement | pass / none |
| `tassel__printer_FrontRightCloseUp__p1` | pass, pass, pass | none; none; none | issue-only / conflicting_perspective | pass / none |
| `magic__printer_FrontRightCloseUp__p2` | pass, pass, pass | none; none; none | pass / clean | pass / none |

## Comparison

V4.3.1 achieved 2/5 labeled verdicts and 2/7 required codes in one run. V4.4 majority results achieved 2/5 and 1/7: no verdict improvement and worse required-code recall. V4.1 had 0/3 labeled verdicts and 0/4 issue matches on its completed subset, so V4.4 is better than that weaker baseline but still not deployable.

## Smallest V4.5 information-flow change

The second pass currently receives only scout-positive proposals. When the scout says every test is clean, the verifier is forced to return an empty result and cannot recover a false negative. All four material-defect families missed here followed that path.

Make the two visual passes independent over the same fixed tests: the verifier performs its own defect scan without seeing scout decisions. Application code accepts agreement; any material disagreement is sent to a bounded third adjudication call for only the disputed tests. Keep current deterministic subtype mapping, scoring, hashes, sentinels, and raw-pixel controls. This changes information flow rather than adding more rubric prose, and stays within the existing three-call ceiling. A V4.5 development gate should first reuse these six cases; no fresh or 160 run is justified until material-fail recall improves without harming the clean control.
