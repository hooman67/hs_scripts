# V4.5.2 Gate A early-stop diagnostic

**Decision: reject V4.5.2; do not scale.**

The frozen `each_required_issue_detected_two_of_three` criterion became mathematically impossible after repeat 2 of `tassel__printer_FrontWide__p1`: `malformed_support_furniture` was detected in 0/2 completed repeats, so the best possible final result was 1/3 while the gate required 2/3. The run was stopped before further model calls.

The chair development case completed 3/3 as `review` with `chair_displacement` and without the forbidden `missing_required_support`. Both completed wide-printer repeats failed for `misplaced_support_furniture` but missed the separate malformed-support defect.
