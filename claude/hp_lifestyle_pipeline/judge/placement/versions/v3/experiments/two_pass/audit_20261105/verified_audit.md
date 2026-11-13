# Independent audit — verified additions V2

As of 2026-11-05T23:27:44Z, `verified-84-v2` is internally consistent across all 84 posthoc development cases and the six successful semantic verifier calls. The exact 20-case diagnostic and 64-case extended ID sets match the source manifests. All source-result, verifier-result, raw-response, trigger-provenance, schema, image-input, scoring, merge and final-policy checks passed.

The durable evaluator is `evaluate_verified_v2.py`, SHA-256 `f303b13b4e83da1c8cd84b013807457ef416bb5e9e73754a94f95565556a5d62`. It regenerated the saved evaluation and audit at `2026-11-05T23:29:33.064336+00:00`. Its saved broad metrics independently reproduce exactly.

## Outcome

The verifier assessed eight proposed components: three remained material at severity 2 with medium confidence, two became mild severity 1, two became severity 0, and one was unobservable. Three earlier two-pass failures became passes:

| Case | Source | Verified | Score |
|---|---:|---:|---:|
| `cashmere__laptop_FrontCloseUp__p5` | fail | pass | 59 → 100 |
| `magic__printer_FrontCloseUp__p3` | fail | pass | 59 → 95 |
| `tassel__printer_FrontCloseUp__p5` | fail | pass | 59 → 100 |

Final totals are 44 fail, 39 pass and 1 review. Diagnostic verdict checks remain 6/11. Extended explicit labels remain 2/2, and agreement with frozen V2 is restored from 55/56 to 56/56.

## Broad versus material issue matching

“Material” here means observed or partial visibility, severity at least 2, and medium or high confidence.

| Dataset | Baseline broad | Baseline material | Final broad | Final material |
|---|---:|---:|---:|---:|
| diagnostic issue checks | 3/15 | 3/15 | 5/15 | 4/15 |
| extended issue checks | 2/6 | 2/6 | 3/6 | 3/6 |

The diagnostic broad/material difference is `tassel__printer_FrontLeftMedium__p5`: its expected codes occur only in a severity-1 component. The extended checks have no broad/material difference after verification. The JSON artifact lists every nonempty code set and separately labels extra codes as `companion_codes_not_assessed`; it makes no claim that those codes are right or wrong.

## Uncertainty policy

For `cashmere__laptop_FrontCloseUp__p5`, the verifier marked `orientation_alignment` unobservable. The merge retained the assessable baseline component and the final envelope preserved an uncertainty note. Reported confidence was already medium, so no confidence override was needed. No real verifier output was low-confidence material, and no verdict override fired. The low-confidence-material pass-to-review rule therefore has unit-test coverage but no empirical example in these six calls.

## Inputs and raw provenance

All six verifier requests contain only the canonical image paths, product type, scene prompt, stage, fallible component proposals and source hashes. Target annotation keys and exact target comment/expectation prose had zero matches. Saved requests contain no image base64. Each assessment validates against its case-specific response schema; raw response content, assessment file and embedded result agree byte-for-structure. The 24 trigger source-artifact hashes and 12 source-image hashes all match.

`verifier-v1` and `verifier-v2` are preserved HTTP-400 schema-rejection attempts with no valid assessments. Only `verifier-v3` contributes model evidence here.

## Limitations

This remains posthoc development evaluation against comment-derived mappings, not holdout accuracy. Broad issue-any does not measure precision or severity correctness. The material variant is stricter but still does not establish whether companion codes are correct.

The semantic verifier runner has an exact frozen snapshot. Individual envelopes do not embed the merge-generator hash, but the final run-level audit records `merge_verified_v2.py`, SHA-256 `cb632c91f9a2959b5840b9afe1bf2f0babf376a50eba720c8fd302cd36bd76de`. That recorded generator reproduces all 84 outputs exactly.

Verification: 5/5 targeted tests passed with the pytest cache disabled.
