# All-view translation audit of the V22.4.3 position experiment

Date: 2026-11-05 PST

## Scope and snapshot

This is a read-only audit of the exact working checkout at:

`/home/colligo/foundry-pr4349-position-exp`

The checkout is based on commit `8c358bc7989cb0e137e89db0fd325168249e2a22` and has the V22.4.3 experiment changes in its working tree. I made no checkout edits, model calls, or generations for this audit.

The durable V22.4.3 evidence reviewed is under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3`

The partially executed pilot is under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1`

## Finding

V22.4.3 does **not** implement Hooman's requested experiment. It allows x-y translation only for `LOWER-FILL/MEDIUM-WIDE` products and deliberately locks every `HIGH-FILL/CLOSE` product to its original frame coordinates. The stopped R1 pilot records the same conclusion after seven close-up rows.

The mismatch is present in all three enforcement layers:

1. Stage-B system and user instructions repeatedly tell close-up products not to move.
2. The executable GPT Image prompt repeats the close-up x-y lock.
3. The deterministic guard and both retry branches enforce the original position for close-ups or after any lower-fill failure.

Changing only the prose is insufficient. Changing only `fixed_position=False` is also insufficient because the textureless fallback is currently available only for fixed-position cases and searches only `[-8,+8]` pixels in each axis.

## Exact source inventory

All paths in this section are relative to `/home/colligo/foundry-pr4349-position-exp`.

### Density classifier and close-up lock

| File:lines | Current behavior | Required all-view change |
|---|---|---|
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:33` | Defines the `0.45` high-fill threshold. | Remove it from placement permission. Occupancy may remain diagnostic metadata, but must not control whether translation is legal. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:327-348` | `_density_policy` returns either a hard x-y lock or translation permission. | Replace with one all-view translation policy. Do not emit `HIGH-FILL/CLOSE` as a lock. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:487-488` | Stores the lock-bearing class and policy in each result. | Store a single all-view translation policy; if density is retained for analysis, make it explicitly non-normative. |

### Stage-B and executable-prompt locks in `pipeline.py`

| File:lines | Current behavior | Required all-view change |
|---|---|---|
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:78-95` | `_TRANSLATION_ONLY` defines two branches; lines 83 and 89 prohibit close-up motion. | Collapse to one rule: any view may use one rigid image-plane translation; exact orientation/view, projected silhouette, pixel width/height, state, and details remain invariant. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:96-107` | `_PRIORITY` says high-fill cannot change geometry and grants baseline-coordinate freedom only to lower-fill. | Remove density-conditioned language and make baseline coordinates non-binding for every view. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:113-128` | `_WRITE_OVERRIDE` tells Stage B to apply the density branch. | Tell Stage B to choose a usable final x-y for every view, without changing view/scale/projection. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:139-145` | `_LEGEND` says the active branch decides whether position is fixed. | State unconditionally that initial coordinates are only a starting location and may change by rigid x-y translation. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:146-155` | `_FINAL_CHECK` prohibits high-fill change. | Check translation-only invariants without an occupancy exception. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:431-446` | Planner body invokes a deterministic density branch. | Replace with the all-view translation policy. `Do not pretranslate the guide` at line 435 can remain because Stage A may keep drawing the baseline guide; it must not be interpreted as a Stage-B position lock. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:494-498` | Assembles the density policy into Stage B. | Assemble one policy for all views. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:510-529` | Assembles the density lock into the GPT Image prompt at least three times. | Remove every close-up lock; retain exact orientation/view, projection, silhouette, pixel dimensions, details, and full visibility. |

### Fixed-position retry machinery in `pipeline.py`

| File:lines | Current behavior | Required all-view change |
|---|---|---|
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:156-207` | Defines the fixed-position image retry, fixed Stage-B rewrite, executable policy, legend, and final check. | These cannot be used in the requested experiment. Replace with a translation-permitting invariant reminder or remove the dead machinery. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:209-276` | Validates and strips translation language from the fixed fallback. | Remove from the active path. A new retry validator should reject rotation, scale, shear, warp, reprojection, crop, and occlusion while allowing x-y movement. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:557-560` | Sets `fixed_position=True` for high-fill and passes it to the guard. | All views must be verified translation-invariantly. Replace the position-lock flag with a semantically clear `allow_translation=True`, or remove the flag once no fixed mode remains. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:567-595` | A failed high-fill attempt gets a fixed-position prompt and a fixed-position second guard. | Retry may emphasize exact orientation/scale/silhouette, but must continue to permit translation. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/pipeline.py:597-684` | Any failed lower-fill attempt triggers a new fixed-position Stage-B rewrite; the second guard is also fixed-position. | This silently changes the experiment after failure. Replace it with one translation-permitting retry path shared by all views. |

The dedicated fallback prompt is fixed-position by construction:

`experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p_fixed_position.txt:8-12,29-33,73-80,104-109,175-196`

It should not be reachable in the all-view experiment.

### Main Stage-B system-prompt locks

| File:lines | Current behavior | Required all-view change |
|---|---|---|
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:14-20` | Says a density branch decides fixed versus movable coordinates. | One all-view translation rule. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:23-26` | Defines high/lower-fill branches. | Remove branch as authority; occupancy may be descriptive only. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:32-52` | Prohibits high-fill motion and permits lower-fill motion. | Permit rigid x-y translation for all views. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:94-100` | Product-first planning repeats the high-fill lock. | Remove the conditional lock. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:108-118` | Applies the density class during support placement. | Build support around the final translated position for every view. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:144-150` | Geometry section locks high-fill frame position. | Preserve view/projection/pixel dimensions, while allowing x-y. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/prompts/system_3p.txt:260-271` | Output contract explicitly requires the active branch and a high-fill lock. | Output one translation-only contract for every view. |

### Geometry description

`experimental/adarabi/hp-3p-gpt25/hp3p/geometry.py:547-552` already says that listed coordinates are initial and that the product may undergo one rigid x-y translation. This is aligned with Hooman's actual request and can remain. In the current close-up assembled prompt, however, this sentence directly conflicts with the active high-fill lock injected elsewhere.

### Deterministic guard assumptions

| File:lines | Current behavior | Required all-view change |
|---|---|---|
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:25` | Allows only eight pixels of translation when `fixed_position=True`. | Remove position tolerance as a pass/fail invariant. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:27-34` | Textureless fallback search radius is only eight pixels. | Search the entire legal in-frame translation domain. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:64-153` | `_assess_fixed_textureless` assumes the product stayed near its original location. | Replace with a translation-invariant textureless verifier. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:156-191,203-212` | Textureless fallback is dispatched for missing descriptors/matches/fit only when `fixed_position` is true. | Dispatch for any translation-permitted view with a persisted product mask when affine evidence is unavailable. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:275-277` | Adds fixed x/y translation checks. | Delete these checks in the all-view experiment. |
| `experimental/adarabi/hp-3p-gpt25/hp3p/invariants.py:285-300` | Structurally unreliable affine evidence can use the alpha fallback only for fixed-position rows. | Allow the translation-invariant fallback for every view; retain primary metrics and dispatch reason. |

The SIFT/full-affine primary path is already translation-invariant when `fixed_position=False`: its scale, anisotropy, rotation, shear, residual, coverage, and in-frame checks do not penalize translation magnitude. The missing piece is a full-frame fallback for texture-poor products.

## Verified assembled-prompt contradiction

The preserved close-up row below is concrete evidence, not a source-only inference:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1__outer_job_1`

Its result is classified `HIGH-FILL/CLOSE`. The assembled request and executable prompt say all of the following:

- `stage_b_attempt_1_request.json` system lines 32-35: preserve exact initial x-y and do not move.
- The same system lines 39-40: lower-fill may translate.
- `stage_b_attempt_1_request.json` text line 36: active high-fill lock.
- The same text line 45: geometry description says the entire product may undergo a rigid x-y translation.
- `image_request_attempt_1.json` prompt line 3: active high-fill lock.
- The generated Stage-B layout at image-prompt line 5 says “no translation.”
- The generated composition at image-prompt line 9 says the high-fill rule overrides general translation permission.
- The image prompt repeats the high-fill lock again at lines 16, 22, 30, 32, and 44.

The deterministic result then records `fixed_position: true`. Attempt 1 fails, so attempt 2 is generated and checked under the fixed-position fallback. Therefore close-up movement is blocked by both the text and the verifier.

The R1 run was correctly stopped after seven completed rows and records:

> Current V22.4.3 policy permits x-y translation only for LOWER-FILL/MEDIUM-WIDE and retains an exact x-y lock for HIGH-FILL/CLOSE. Hooman requested translation freedom for the device without a close-up exception.

Source:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1/PARTIAL_POLICY_PILOT_STOP.md`

## Narrow design for translation-invariant verification

### 1. Keep the textured-product affine path

Use the current SIFT/full-affine path for all views without fixed-position x/y checks. A reliable fit passes only when:

- both singular values stay near one;
- anisotropy, rotation, and shear remain within their calibrated limits;
- reprojection residuals remain low;
- source landmarks span enough of the product;
- transformed product corners remain in frame.

Translation magnitude is measured and reported, but does not affect the verdict.

### 2. Replace the ±8 textureless fallback with full-frame rigid-template localization

The persisted RGBA alpha mask supplies the source product silhouette. Build a product-bounding-box template from:

- the alpha boundary;
- internal source edges inside an eroded alpha mask;
- masked high-pass appearance samples.

Search every legal integer translation whose translated alpha mask remains fully inside the output canvas. Do not search scale, rotation, or shear. A practical deterministic implementation is:

1. Compute full-output edge and high-pass maps once.
2. Use full-frame template correlation to propose the top spatially distinct x-y candidates from boundary edges, internal edges, and masked high-pass appearance. This avoids an exhaustive Python loop over millions of offsets.
3. Re-evaluate the union of candidates with the current auditable metrics: boundary coverage/distance, internal-edge coverage/distance, and masked high-pass NCC.
4. Select the best passing candidate using a frozen deterministic tie-break rule.
5. Return the absolute output bounding box and `(translation_x_px, translation_y_px)` for the selected product.

Because the template's size and shape are fixed, a scaled, rotated, sheared, warped, or reprojected product cannot align both its outer boundary and internal structure under translation alone. The current anti-dark-blob requirement—internal structure or high-pass appearance, plus a nonzero internal-edge floor—should remain.

This fallback must be explicitly labeled as translation-invariant; reusing the name `alpha_mask_fixed_position_fallback` would make the audit misleading.

### 3. Preserve uncertainty

Return `unverifiable`, rather than pass, when:

- there is no candidate with enough boundary and internal/appearance evidence;
- the product is clipped by the frame;
- two spatially distinct candidates are nearly tied and duplicate/ghost ambiguity cannot be resolved;
- the source has too little silhouette or internal structure to reject a transformed dark object.

Do not silently choose the original position as a fallback.

### 4. Use one retry policy for all views

After a failed first guard, make at most one second image call with a concise invariant reminder that still permits rigid x-y movement. The reminder should say, in substance:

- move only by x-y translation if useful;
- preserve exact view/orientation, projected silhouette, pixel width/height, visible faces, perspective/foreshortening, state, finish, markings, and display content;
- keep the product fully in frame and unoccluded;
- recompose the support and room around the final position.

Do not invoke `system_3p_fixed_position.txt`, do not run a fixed-position Stage-B rewrite, and do not check attempt 2 with `fixed_position=True`.

For the narrowest implementation, keep the successful first Stage-B scene plan and append the translation-permitting invariant reminder for attempt 2. This isolates the repair to product fidelity and avoids changing the scene plan after a guard failure.

### 5. Persist localization for downstream compositing

For the selected attempt, persist:

- verifier method;
- final product bounding box;
- x/y translation;
- affine matrix when available;
- all pass/fail metrics and thresholds;
- selected attempt number.

This makes the moved location explicit for any downstream stage that pastes digital-twin pixels back into the scene.

## Test implications

### Tests that encode the wrong partial policy and must change

- `experimental/adarabi/hp-3p-gpt25/tests/test_pipeline.py:109-123`: remove the assertion that 45% occupancy implies an exact x-y lock. If occupancy metadata remains, prove it does not alter translation permission.
- `experimental/adarabi/hp-3p-gpt25/tests/test_pipeline.py:137-168`: replace the lower-fill-to-fixed retry expectation with an all-view translation-permitting retry.
- `experimental/adarabi/hp-3p-gpt25/tests/test_pipeline.py:193-271`: fixed fallback validation and separate high-fill retry tests are obsolete in the active path.
- `experimental/adarabi/hp-3p-gpt25/tests/test_pipeline.py:463-490`: replace the high/lower-fill assertions with one all-view policy assertion.
- `experimental/adarabi/hp-3p-gpt25/tests/test_prompts.py:39-64`: remove high-fill lock requirements and assert that all views permit only rigid x-y translation.
- `experimental/adarabi/hp-3p-gpt25/tests/test_prompts.py:67-75`: the fixed-position system may be retained as a legacy isolated unit, but the pipeline test must prove it is unreachable in this experiment.
- `experimental/adarabi/hp-3p-gpt25/tests/test_invariants.py:24-33`: change the “locks high fill” case so the same large translation passes regardless of view class.
- `experimental/adarabi/hp-3p-gpt25/tests/test_invariants.py:85-109`: replace bounded ±8 translation tests with full-frame large translations and retain scale/rotation/shear/dark-distractor rejection.
- `experimental/adarabi/hp-3p-gpt25/tests/test_invariants.py:119-213`: fallback dispatch must no longer depend on fixed position; reliable dense affine failures must still remain failures, but large pure translation must pass.

### Required new coverage

1. Large x and y translations pass for textured and textureless laptop and printer fixtures.
2. Identical fixtures at close-up/high occupancy and wide/low occupancy receive the same translation permission.
3. Translation to each legal frame extreme passes; one-pixel clipping fails.
4. Scale up/down, rotation, anisotropic scale, shear, projective-looking warp, redraw, and dark-blob distractors fail after large displacement.
5. Sparse or poorly distributed affine matches dispatch to the full-frame textureless verifier for every view.
6. Reliable dense affine evidence is authoritative and is not overridden by a weaker fallback.
7. Attempt 2 remains translation-permitting in both prompt and guard.
8. Assembled Stage-B and GPT Image prompts contain no high-fill lock, no fixed-position retry, and no density-conditioned permission.
9. The selected result persists the detected final bounding box and translation for downstream pixel replacement.
10. Replays cover the earlier close-up artifacts as well as lower-fill artifacts; do not claim equivalence from a lower-fill-only corpus.

## Recommended implementation boundary

The narrow change is:

1. make rigid x-y translation legal for every view in the main system prompt and all assembled prompt fragments;
2. remove density-conditioned verification and fixed-position retry behavior;
3. keep the current reliable affine checks;
4. generalize only the textureless fallback's localization from ±8 pixels to the full legal frame;
5. retain one bounded translation-permitting retry and full audit evidence.

This directly tests Hooman's hypothesis—whether freeing product position improves furniture and room composition—without also allowing changes to product orientation, projected view, scale, shear, silhouette, crop, or identity.
