# Project state

## Live checkpoint — 2026-11-06, V23.1 integrated and fresh pilot packaging

The printer-wide V23 pilot failure was a guard false rejection, not a product-invariant failure.
Both preserved outputs had 17--18 exceptionally well-distributed inliers and passed every scale,
rotation, shear, residual, rigid-translation, frame and fixed-recovery check. A narrow alternative
reliability path now accepts only 17--19 inliers with ratio >=0.70, span >=0.70/0.60, all four
quadrants, hull >=0.25 and every non-count invariant passing. The ordinary 20-inlier threshold is
unchanged.

V23.1 is integrated into the isolated Foundry source and passes 180 tests, lint, compilation and
diff checks. Its complete replay is 110/110 frozen and 82/82 added checks with zero false
accepts/rejects and zero changes to prior V23 run-3 decisions or selections. Exact implementation:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/IMPLEMENTATION.md`

A new isolated eight-cell pilot is being packaged: the four representative V6.1 cells plus laptop
and printer close/wide relocation-demand diagnostics. Nothing is currently generating.

## Live checkpoint — 2026-11-06, V23 pilot stopped on guard false-rejection candidate

The frozen V23 four-row pilot completed three rows and stopped on the Tassel printer FrontWide row.
Laptop close, laptop wide and printer close passed on their first image attempt. Printer wide made
one movable attempt and one fixed-position recovery; both were rejected. The endpoint is stopped
and no full-160 run started.

Both printer-wide attempts preserved the apparent product view and scale. Their affine evidence
passed every transform, spatial-distribution and translation-residual check but had 18 and 17
inliers against the frozen minimum of 20. The alpha fallback then localized unrelated scene edges,
causing one fail and one fail-closed unobservable result. This is a likely guard false rejection.
A narrow strong-affine-evidence candidate is being replayed across all frozen, added and prior
evidence before any rerun; the threshold will not be changed based only on this case.

The four first attempts moved the product by approximately zero to 1.3 pixels. This run therefore
does not yet demonstrate material translation, even though translation is permitted by the
executable prompt. A follow-up gate must include representative movement-demand cases before
scale-up.

Full result:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/PILOT_RESULT.md`

## Live checkpoint — 2026-11-06, V23 offline gate passed

The corrected all-view experiment is implemented and frozen as V23. Its first scene attempt may
apply one rigid image-plane x-y translation for every camera view, including close/high-fill
views. Exact view, projection, foreshortening, scale, silhouette, identity, details and full
visibility remain hard invariants. Any failed or unobservable first attempt receives one
fixed-position recovery; a second failure is explicit.

The successful Direct OpenAI Astra consultation and reviewed implementation are documented at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/REPORT.md`

Final offline evidence: 178 package tests passed; the frozen synthetic suite is 110/110; the added
V23 suite is 82/82; all 95 compatible prior rows replayed without skips. Among 48 comparable old
selections, five previously rejected rows gain a selection and four wide-view rows lose selection
because their landmark motion is inconsistent with one rigid translation. All close-view
compatibility losses are recovered. Final calibration:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/CALIBRATION_REPORT.md`

No V23 image generation has started. A fresh isolated four-image pilot is being packaged: laptop
close, laptop wide, printer close and printer wide. The old seven-row V22.4.3-R1 run remains
partial-policy evidence only and must not be represented as the all-view experiment.

As of 2026-11-05.

## Live checkpoint — 2026-11-05 23:23 PST

The requested experiment is now explicitly defined as one rigid image-plane x-y translation for
every camera view, including high-fill close-ups. Exact device orientation/view, projection,
foreshortening, pixel width/height, silhouette, identity, details and full visibility remain hard
invariants. The prior V22.4.3 implementation did not satisfy this contract: it locked every
HIGH-FILL/CLOSE row and reverted every failed LOWER-FILL row to fixed position. The exact
file-and-line audit is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/all_view_translation_audit_v1/REPORT.md`

The V22.4.3-R1 pilot was therefore stopped after seven completed close-up rows and is retained only
as partial-policy evidence: five first-job passes, two outer-retry recoveries, and zero terminal
failures. Stop evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1/PARTIAL_POLICY_PILOT_STOP.md`

Do not describe that run as Hooman's all-view movement experiment. No replacement generation run
has started. The next version must remove every close-up lock from Stage B, the executable image
prompt, guard dispatch, and retry path. It must also generalize the textureless-product verifier
from a fixed-position +/-8 px search to deterministic full-frame rigid-translation localization;
changing prompt prose or only passing `fixed_position=False` is insufficient.

Four earlier Astra design calls yielded no usable output. A fifth compact 6,988-byte call reached
Astra but exhausted its 8,192-token completion budget in reasoning (`finish=length`) and returned
no visible answer. It is preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v1/`

The byte-identical request is now running in detached tmux as compact-v2 with a 32,768-token
completion budget, high reasoning, one concurrent request, a 600-second request timeout and eight
bounded client retries:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v2/`

Review any Astra answer against the source audit before implementing it. If it again fails, record
that failure and proceed with the independently derived all-view design without attributing it to
Astra.

## Live checkpoint — 2026-11-05 22:55 PST

V22.4.3 completed its offline gate. The only source change routes fixed-position RGBA cases with
structurally inadequate affine evidence to the existing alpha-mask fallback. It passed 172 tests,
31-real/55-synthetic calibration replay with no induced errors, and 60 compatible prior-row replays
with exactly the intended V22.4.2.1 first-row selection change. Evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/`

The isolated full160 launch then stopped on row 1 after two fresh image attempts. Both retained the
requested laptop orientation, but their external silhouette/scale drifted. The unchanged fallback
correctly rejected boundary coverage 0.691 and 0.743 versus the frozen 0.80 threshold; internal
structure remained 0.945 and 0.921. This is a genuine fixed-position product-invariant failure,
not a sparse-affine dispatch bug. The endpoint and runner are stopped, and the complete failure is
preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3/run/`

Do not weaken the guard. A distinct V22.4.3-R1 qualitative-assembly wrapper is being prepared with
one initial endpoint job plus at most one outer job retry only for terminal guard rejection. It must
preserve both job attempts, choose the first passing job, report first-job/recovery/terminal rates,
use new identifiers, and explicitly avoid any native V22.4.3 reliability claim. No further model
call may begin until wrapper tests, freeze, preflight, and exact pipeline/prompt/guard hashes pass.

## Prior live checkpoint — 2026-11-05 22:25 PST

V22.4.1's first full-160 attempt stopped because an affine-fit failure did not dispatch to the
already frozen fixed-position RGBA fallback. V22.4.2 adds only that dispatch. No prompt, threshold,
retry, selection rule, or geometry policy changed. It passed 170 tests, 31-real/55-synthetic replay
with zero regressions, preserved all prior full-eight selections, and replayed the V22.4.1 failed
artifact as a passing attempt 2. Frozen evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_2/`

The V22.4.2 full-160 launch then exposed a wrapper-only audit-contract defect on row 1. The exact
pipeline run completed successfully after one bounded image retry, and selected attempt 2 passed
the product guard (boundary 0.8859, internal-edge coverage 0.9648, translation +1/-1 px). The local
wrapper nevertheless marked the row failed because it required reference-blue
`planning_request.json`/`planning_response.json` artifacts from an execution that intentionally
uses the standard Stage-B branch and records `stage_b_attempt_1_request.json`/
`stage_b_attempt_1_response.json`. No later row ran. The endpoint is stopped and the failure is
preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/run/`

The new isolated V22.4.2.1 wrapper package fixed only the artifact contract and passed 13 tests,
checksums and preflight. Its fresh first row then generated two new attempts, and both were rejected
by the unchanged guard. Each produced exactly three sparse SIFT matches and therefore a numerically
fitted but meaningless affine transform; because a fit object existed, the fixed-position RGBA
fallback was not dispatched. Offline replay of the frozen fallback passes attempt 1 (boundary
0.811003, internal 0.953368, shift +1/0) and fails attempt 2 (boundary 0.734114). The endpoint is
stopped and the second failed run is preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/run/`

V22.4.3 is a no-model-call guard candidate that may dispatch the existing RGBA fallback only when
fixed-position affine evidence is structurally unreliable (insufficient inliers or spatial
coverage). Dense reliable affine failures must remain failures. It may not change thresholds,
prompts, geometry policy, or retry count. Complete the 31-real/55-synthetic and prior-artifact
replay before considering another isolated launch.

## Live checkpoint — 2026-11-05 21:33 PST

V22.3.3 is the last fully passing eight-case smoke, frozen at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_3_3_guard/`

Its prepared full160 package started and stopped on the first row,
`cashmere__laptop_BackRightCloseUp__p1`, because both raw image attempts returned only one SIFT
match and the affine guard correctly reported `unverifiable`. No later row ran. The preserved failed
run is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_3_3/run/`

V22.4 is a distinct fixed-position textureless-product fallback. It uses the RGBA product alpha
mask, searches only integer translations within +/-8 pixels and checks product-boundary coverage,
internal-edge coverage and masked high-pass correlation. The calibration contains 31 real attempts
and 55 deterministic synthetic attempts, including resize, rotation, shear, anisotropy, excess
translation, brightness shift and solid-dark impostors. Lower-fill products remain affine-only.

The first threshold freeze used boundary coverage >=0.85. A fresh first-row development retry
produced a visually faithful first attempt at 0.8323 boundary / 0.8891 internal coverage and a
degraded second attempt at 0.6553 boundary. Consequently both were rejected and the run stopped.
The exact raw attempts, guard decisions and contact sheet are preserved at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_first_row_retry/`

Recomputing the frozen calibration at boundary >=0.80 retains zero synthetic false accepts, zero
synthetic false rejects and zero fallback false accepts on known fixed-position affine failures.
The strongest forbidden synthetic that otherwise passes the internal checks has boundary 0.7493,
leaving about a 0.05 margin. Because this adjustment follows inspection of the fresh row, that row
is now development evidence. Freeze the 0.80 candidate transparently, rerun deterministic tests and
replay without a new model call, then use the remaining smoke cases as the next gate. Do not launch
full160 or publish S3 until that gate passes.

Active source checkout remains:

`/home/colligo/foundry-pr4349-position-exp`

No full160 generation or S3 publication is currently active.

## Current status

- PR #4349 was fetched into an isolated durable checkout.
- Exact prompt locks and the guide-only/no-mask image call were identified.
- The deployed 8016 UI explicitly identifies PR #4349, but its web-server wrapper is absent from the PR checkout.
- Astra attempt 1 ended with `finish_reason=length`, 10,190 total tokens, and no usable answer. Its one-byte output and logs are archived with `attempt1` names. Attempt 2 completed with `finish_reason=stop`, 6,554 total tokens, medium reasoning and a 24,000-token completion budget. Its reviewed answer is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/output.md`.
- The accepted prompt-only translation design is implemented in `/home/colligo/foundry-pr4349-position-exp` without a commit. Scale and full 3D orientation/view are fixed; only common product/support x-y translation is permitted. Stage A and the guide renderer stay at baseline coordinates.
- A source and assembled-prompt contradiction audit found and removed the less-obvious absolute lock emitted by `describe_geometry()`. Old absolute-lock phrases now occur only in negative test assertions.
- The documented Python 3.12 environment passes all 144 tests. `ruff 0.16.8 check --select F,E9,I hp3p tests` and `git diff --check` also pass. An earlier Python 3.10 run produced baseline `hashlib.file_digest` setup errors because this package explicitly requires Python 3.12; those errors are superseded by the documented-environment result.
- The unrelated `70620ce...` ref discrepancy is resolved: it was Colligo PR #4349, while the requested Foundry PR #4349 is `8c358bc...`.
- The existing short-lived AWS environment remains valid for read-only S3 inputs. Credential refresh could not mint a new session because this machine currently has no broker Pluto token; no credential values were copied into project files.
- The deployed wrapper is unavailable. A clearly labeled thin local experiment API now invokes the exact isolated PR4349 `hp3p.pipeline.run_row`; it does not reimplement or claim parity with the unavailable deployed wrapper. It runs at `http://127.0.0.1:8126` in tmux `hp-position-endpoint` and pins the accepted source hashes at startup. A cached dry fixture reached `run_row` without an outbound model call and reproduced the treatment output byte-for-byte.
- The exact-PR-code controlled smoke completed successfully for four predetermined fixtures: Cashmere laptop close/wide and Magic printer close/wide. Every treatment reused the byte-identical frozen control guide, selection and Stage-A geometry, made one Astra writing call and one GPT Image call, with API retries disabled and no best-of. The verified manifest is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/treatment/manifest.json`, audit is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/treatment/MECHANICAL_AUDIT.md`, and comparison sheet is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/treatment/control_vs_treatment.jpg`.
- The first pre-contract smoke is separately archived as a failed mechanical attempt because Stage B copied `reference tabletop`, which the unseen-image guard rejected. It was not manually repaired or selected. See `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/archived/FAILED_MECHANICAL_SMOKE_20261106T023241Z.md`.
- The full frozen V6.1 160-row treatment started in tmux `hp-position-full160`. It submits serially through the local API, stops on the first failure, persists job artifacts/status, and validates both the export SHA-256 and every record-to-export prompt before generation. Each uncached row receives one live Stage-B call and one live unmasked image edit, with no best-of or manual repair.

## Next exact step

Monitor the persistent full-160 run. On the first error, preserve the failing row without repair and diagnose before any continuation. After 160/160 complete, build the equivalent grouped FE report at a new S3 prefix and run the updated natural-placement judge.

## Position-policy and guard update — 2026-11-05 20:12 PST

- The v21 full-160 run above was paused after 12 completed rows. Its outputs and
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160/V21_PAUSED_PILOT_MANIFEST.json`
  are retained as an inconclusive pilot. No full-160 process is active.
- V22 through V22.2.1 tested independent support recomposition and camera-density-aware x-y freedom. HIGH-FILL now has a hard x-y/scale/view lock. LOWER-FILL may translate in x-y while preserving product raster geometry. These prompt iterations and their smoke evidence remain frozen under
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/`
  and
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/`.
- LOWER-FILL prompt constraints were not mechanically reliable enough by themselves. The calibrated v22.3 guard fits a full affine transform from product landmarks, records both singular values, anisotropy/shear, polar rotation, residual median/p95, landmark spread/quadrants/hull, translation, and transformed corners. One failed or unverifiable attempt receives exactly one fixed-position fallback. A second failure returns an explicit contract error and preserves both raw attempts.
- Calibration over all 28 prior smoke outputs and frozen thresholds are documented in
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/AFFINE_GUARD_CALIBRATION.md`.
- The initial v22.3 mechanical smoke exposed strict-JSON serialization of NumPy booleans before fallback. Two completed error rows and logs are preserved at
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_3_guard_failed_json_serialization/`.
- V22.3.1 recursively normalizes every persisted guard/result value to native JSON, with round-trip tests covering pass, fail, unverifiable, fallback success and double failure. The documented Python 3.12 environment now passes 153 tests; ruff E9/F/I and `git diff --check` pass. Its frozen source hashes and diff are at
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_3_1/`.
- The fresh eight-row v22.3.1 guard smoke is active in tmux `hp_position_v22_3_1_guard_smoke`. It includes laptop/printer close neutral and adversarial cases plus laptop/printer wide neutral and relocation cases. Output is
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_3_1_guard/`.

## Current next exact step

Finish and audit the eight-row v22.3.1 guard smoke. Do not launch another full-160 run until Hooman/root reviews the raw attempts, guard decisions, quantitative metrics and contact sheets.
