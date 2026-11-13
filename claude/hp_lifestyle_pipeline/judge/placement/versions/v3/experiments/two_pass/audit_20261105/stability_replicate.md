# Semantic verifier stability replicate audit

Audited one separately preserved replicate of the same six posthoc development trigger cases and eight components. All six GPT-5.5 high-reasoning calls succeeded on attempt 1 with two workers. The campaign used the byte-identical frozen semantic-v3 prompt, schema, and runner; no human labels, comments, or expectations entered runtime requests.

The three originally material components all repeated as material (3/3). Both café-seating components repeated exactly. The printer-serving component repeated with the same observed visibility, severity 2, and three issue codes; confidence changed from medium to high.

The visitor-chair false-failure finding remained rejected as nonmaterial. Access/usability repeated exactly as clear. Orientation changed from unobservable/unknown to observed, severity 0, medium-confidence clear with no codes. The conclusion repeats, although the observability label does not.

The broader result shows meaningful stochastic variation. Only 3/8 components matched exactly across visibility, severity, confidence, and codes. Material classifications expanded from 3 to 5: two printer-workspace support components moved from severity 1 to severity 2. A different printer support component changed from clear to mild. No run is selected as “best,” and these results do not justify automatic candidate changes.

| Case / component | Original | Replicate | Exact |
|---|---|---|---|
| `cashmere__laptop_FrontLeftMedium__p6` / access | partial, 2, medium, `no_user_position` | same | yes |
| `cashmere__laptop_FrontLeftMedium__p6` / orientation | observed, 2, medium, `chair_alignment_conflict` | same | yes |
| `tassel__printer_FrontCloseUp__p5` / support | observed, 0, high, no codes | observed, 1, medium, `unmotivated_position` | no |
| `cashmere__laptop_FrontCloseUp__p5` / access | partial, 0, medium, no codes | same | yes |
| `cashmere__laptop_FrontCloseUp__p5` / orientation | unobservable, null, low, no codes | observed, 0, medium, no codes | no |
| `magic__printer_FrontCloseUp__p3` / support | observed, 1, medium, `unmotivated_position` | observed, 2, medium, `occupied_workstation`, `unmotivated_position` | no |
| `magic__printer_FrontLeftMedium__p1` / support | observed, 1, medium, `inappropriate_support` | observed, 2, medium, `occupied_workstation` | no |
| `tassel__printer_FrontLeftMedium__p6` / support | observed, 2, medium, three codes | observed, 2, high, same three codes | no |

Agreement was 7/8 for visibility, 4/8 for severity, 5/8 for confidence, 5/8 for issue-code lists, and 6/8 for material/nonmaterial classification. The original class counts were material 3, clear 2, unobservable 1, and mild/other 2. The replicate counts were material 5, clear 2, and mild/other 1.

Integrity checks passed for all six cases: schema validation, raw-response/assessment/result equality, trigger/proposal/source joins, five-key runtime inputs, request/result equality, and all 12 image hashes. Requests contained zero human-label/comment keys, zero exact target-comment or expectation prose hits, and zero serialized image base64 payloads.

Frozen campaign:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/verify_additions_stability_v1`

Replicate run:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/verify_additions_stability_v1/runs/stability-replicate-v1`

Machine-readable audit with exact artifact hashes:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/experiments/two_pass/audit_20261105/stability_replicate.json`

Limitations: this is one repeat over the same posthoc development triggers, not a holdout or a whole-judge accuracy estimate. It cannot estimate stable probabilities. The verifier saw no human ground truth, so the exercise measures repeatability rather than correctness. Companion issue codes are listed without invented labels or independent human assessment.
