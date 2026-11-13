# NEW160 independent mechanical audit

Status: **pass**. The 160 manifest IDs exactly match baseline V2, compact V3, two-pass, verified, and combined front-end rows. The laptop and printer FE splits contain the exact corresponding 80 IDs each.

The frozen pipeline was independently recomputed for every record. All 160 verified-compact scores, component merges and provenance, application-merged scores, and final-policy decisions exactly match the saved envelopes. The frozen verified merger SHA-256 is `11594dccc74ba3ed5e986d0b32be7f531b63205186df7abb86b7ef5bed336922`; the scorer is `d7061d8252b67c1b75dd6f6e680b05ab74545a3d9776763cc152bc6fd48c6006`; the two-pass combiner is `87e5ac23a0ef9254f7c43b499197539abe2670db243f427a9d477ddc6cbfb1e1`.

Final verified verdict counts by device:

| Device | Pass | Review | Fail |
|---|---:|---:|---:|
| cashmere | 25 | 3 | 12 |
| elitebook | 25 | 1 | 14 |
| magic | 33 | 0 | 7 |
| tassel | 34 | 0 | 6 |

The five trigger components were independently derived from the saved predictions and exactly match the trigger manifest:

- `cashmere__laptop_BackRightCloseUp__p9` / `access_usability`
- `elitebook__laptop_BackRightCloseUp__p7` / `orientation_alignment`
- `elitebook__laptop_BackRightCloseUp__p9` / `access_usability`
- `elitebook__laptop_BackRightCloseUp__p9` / `orientation_alignment`
- `magic__printer_FrontLeftMedium__p6` / `support_scenario`

These are four verifier cases and five component assessments. All four calls succeeded on attempt 1. Each raw response body parses to the saved assessment and its hash matches the verified overlay. Exact raw body hashes are in the JSON audit.

The final result differs from baseline V2 for only one record: `elitebook__laptop_BackRightCloseUp__p9`, pass to fail. That change was already made by the two-pass merge. The verifier overlay changed zero two-pass verdicts. The other three verifier cases were fail in baseline V2, compact V3, two-pass, and verified outputs.

Input coverage is complete: 160 prompt text/hash checks, 160 generated-image hashes, 160 twin-image hashes, 320 stage runtime-input checks, and 960 stage artifact hashes. The 160 generated-image hashes are unique; 16 twin hashes are reused across views. Every manifest row is `evaluation_target_unlabeled`, and all label-provenance flags are false.

The FE contract also passes. Each combined row shows the exact manifest generated-scene URL, the twin identified by its manifest hash and filename, the exact original prompt, final score and verdict, and matching device/product/candidate/camera/environment metadata. All 16 shared twin assets hash correctly. Global FE metadata states `scene_generation` and that human labels were not passed to the judge. The build remains `local_build_validated_not_published`.

Core regression tests passed: 16 tests across the FE builder, two-pass merger, and verified-addition workflow.

This is an unlabeled set, so the audit establishes provenance, deterministic policy behavior, and FE presentation integrity rather than accuracy. No network fetch, model call, or AWS write was performed.
