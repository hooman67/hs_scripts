# V23 all-view rigid-translation experiment

**Frozen:** 2026-11-06  
**Status:** offline gate passed; image pilot not yet run

## Intended behavior

The first scene-generation attempt may retain the digital twin's image-plane position or apply one
rigid x-y translation in every camera view, including close/high-fill views. It must preserve the
same product view, projection, foreshortening, scale, silhouette, identity and details, and the
entire product must remain visible. If that attempt cannot be verified, the pipeline makes one
fixed-position recovery attempt. A second failure is explicit; the pipeline does not silently
choose an unverified image.

## Why this version exists

V22.4.3 did not implement the requested experiment. It locked every high-fill/close view and sent
failed lower-fill attempts to a fixed-position recovery. V23 removes that view-class split from the
movement policy and extends the textureless-product verifier from a local +/-8-pixel search to
deterministic full-frame rigid-translation localization. Camera density remains diagnostic only.

Exact audit of the prior mismatch:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/all_view_translation_audit_v1/REPORT.md`

## Astra consultation

The successful Direct OpenAI Astra consultation recommended the same high-level design: permit
rigid x-y translation for all views, retain one fixed-position recovery, use translation-aware
RGBA verification for textureless products, and fail closed when the invariant is not observable.
Its numerical thresholds were treated as proposals; final behavior was calibrated against the
frozen local evidence.

Full response:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v2/response.md`

Summary:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v2/SUMMARY.md`

## Frozen source identity

Foundry checkout:

`/home/colligo/foundry-pr4349-position-exp`

Base commit: `8c358bc7989cb0e137e89db0fd325168249e2a22`

| File | SHA-256 |
|---|---|
| `hp3p/invariants.py` | `8c1a8204d27eeb3ba922d6d9519113da7beeff9368301bcc9f8c9a7ec2fb2665` |
| `hp3p/pipeline.py` | `dde47ae75c6023a020ea26c405c5cf8e78183fe2de4e3219a5c279eb804b6ced` |
| `hp3p/prompts/system_3p.txt` | `324ce0e449804bc0d17ac0cf5ed10587716bc9d7e6ef72b9a91e439745b6aaec` |
| `tests/test_invariants.py` | `06a08b22e6bc0d6b1e1d0d6bb41dc749bc2fe763f4b39fe1335c62e5d1a95e78` |
| `tests/test_pipeline.py` | `a642dede710b6c54ce626cec304e5ac06acd553c7abf70431a7b2779c425905e` |
| `tests/test_prompts.py` | `8c09e3404b7e867cac1b3a502ecaf9e8095d51f68cb4539fc3d0ff16c92cfc5b` |

## Offline verification

- Full package tests: **178 passed**.
- Frozen V22.4 synthetic replay: **110/110**, zero false accepts and zero false rejects.
- Added V23 suite: **82/82**, zero false accepts, zero false rejects and zero outcome mismatches.
- A 12-pixel translation passes in all-view mode for all five full-resolution fixtures and fails
  the fixed-position recovery on `fixed_translation_x` for all five.
- Exact-frame-edge and one-pixel-crop cases fail closed as
  `silhouette_unobservable_at_canvas_boundary`; in-frame pixels cannot distinguish them reliably.
- All 95 compatible prior rows replayed. Among 48 rows with observable old selections, five gain a
  selection and four wide-view selections are lost. The four losses fail rigid-translation
  residual checks: their matched landmarks do not move by one common x-y vector. This is the
  intended orientation/projection safeguard, rather than a view-class lock.
- Full-resolution fallback runtime: median 338.9 ms, p95 401.8 ms, maximum 415.2 ms.
- The final guard source hash was identical before and after the complete replay.

Canonical calibration report:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/CALIBRATION_REPORT.md`

Final evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/run_3/`

## Remaining gate

Offline checks establish the executable contract and guard behavior; they do not establish that
GPT Image will produce better compositions. The next gate is a fresh four-image pilot: one laptop
close view, one laptop wide view, one printer close view and one printer wide view. Only after its
raw attempts, movement, orientation, guard decisions and scene quality are reviewed should the
160-row experiment begin.
