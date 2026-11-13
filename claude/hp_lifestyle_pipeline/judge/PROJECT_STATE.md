# Live checkpoint — 2026-11-06, V15.6/V16.4/V16.6/V16.6-no-geometry judge run

Hooman requested the latest evidence-supported natural-placement judge on the 32-row V15.6 /
V16.4 / V16.6 / V16.6-no-geometry V2 E2E comparison, with score and explanation inserted into
collapsible panels at the existing report URL. V4+ judge candidates remain development-only or
rejected, so this run uses the selected V3 consensus-v2 method. The source has 128 generated
outputs (four per row) plus 32 twin inputs. The source is an E2E comparison while V3 was calibrated
for scene-stage images; every artifact and the viewer label this as an out-of-domain diagnostic.

The exact source viewer and all 160 images were hash-frozen. One-record V2 and compact-V3 smoke
calls passed. Both 128-record primary passes completed with zero errors, the two-pass merge
completed 128/128, six disagreements received proposal-aware and independent names-only checks,
and consensus-v2 produced 128 final results. The final verdict distribution is 107 pass, 1 review,
and 20 fail.

The augmented viewer was locally validated with 32 rows, 128 collapsed judge panels and 160
absolute image URLs, then published in place. The exact user-supplied alias and the real source
viewer contain identical bytes (SHA-256
`ba33d6f719b1169eadab5ee5f036611a4edf5a67e961f8d0709b741ca0aa187b`). Direct S3 read-back and
metadata hashes passed. The original HTML is preserved as a hash-named backup. The Pluto host
could not perform a browser-level fetch through the corporate HTML gateway because the gateway
connection timed out; this does not affect the successful direct-S3 publication verification.

Canonical task directory:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/evaluations/v156_v164_v166_v166noguide_v2_20261106/`

Published viewer:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z-viewer/viewer.html`

Results JSON:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/placement_judge_v3_results.json`

---

# Live checkpoint — 2026-11-06, V23.1 strong-affine correction

The printer-wide V23 pilot failure is resolved offline without weakening the global 20-inlier
threshold. V23.1 accepts 17--19 inliers only under strict ratio, span, quadrant, hull and complete
non-count-invariant gates. It passes 180 production tests, 110/110 frozen checks and 82/82 added
checks, and changes no prior accepted V23 decision or selection. Both preserved Tassel attempts now
pass primary affine verification, avoiding the bad alpha-fallback localization.

A fresh eight-cell pilot is being packaged with four representative V6.1 cells and four explicit
movement-demand diagnostics. No model generation is currently active.

Implementation:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/IMPLEMENTATION.md`

---

# Live checkpoint — 2026-11-06, V23 four-row pilot

The V23 pilot completed laptop close, laptop wide and printer close on their first attempts, then
stopped on printer wide after both the movable attempt and fixed recovery were rejected. The
endpoint is stopped and the 160-row run did not begin. The failure is a likely guard false
rejection: both raw printer images appear to preserve the supplied view and scale, and all affine
transform/distribution/residual checks pass except the frozen minimum-inlier count (18 and 17 vs
20). A narrowly defined strong-affine-evidence rule is undergoing full replay before any rerun.

The generated products moved by at most about 1.3 pixels, so this pilot does not yet establish the
benefit of material x-y relocation. A follow-up gate must include representative movement-demand
cases.

Result and evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/PILOT_RESULT.md`

---

# Live checkpoint — 2026-11-06, V23 all-view position experiment

The corrected all-view pipeline candidate has passed its offline gate. It permits one rigid x-y
translation in every camera view while preserving exact product view, projection,
foreshortening, scale, silhouette, identity, details and full visibility. Failed/unobservable
first attempts receive one fixed-position recovery.

Evidence: 178 tests passed; 110/110 frozen synthetic checks and 82/82 added checks passed; all 95
compatible prior rows replayed. Four old wide-view selections are intentionally rejected because
their landmarks do not follow one rigid translation. No V23 generation is active yet. The next
gate is a new four-image laptop/printer close/wide pilot.

Design and evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/REPORT.md`

---

# Live checkpoint — 2026-11-05 23:23 PST

The movable-device pipeline work found a material scope mismatch. V22.4.3 allowed x-y translation
only for LOWER-FILL/MEDIUM-WIDE rows, while Hooman requested translation permission for all views,
including close-ups. It also reverted any failed lower-fill attempt to fixed position. The pilot
was stopped after seven close-up rows and retained only as partial-policy evidence. The exact audit
and stop record are:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/all_view_translation_audit_v1/REPORT.md`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3_r1/PARTIAL_POLICY_PILOT_STOP.md`

A corrected compact Astra consultation reached the model but exhausted its 8,192-token completion
budget in reasoning and returned no visible answer. Its byte-identical 6,988-byte request is now
running in detached tmux with a 32,768-token completion budget. Evidence is preserved under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v1/`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/astra/all_view_translation_compact_v2/`

No replacement image experiment has started. The next version must permit one rigid x-y
translation for every view while preserving exact orientation/view, projection, pixel dimensions,
silhouette, identity, details and full visibility. It also needs a full-frame translation-invariant
textureless-product guard; the present printer fallback searches only +/-8 pixels.

Judge development is separate. V4.5.4.4 is prepared but has made no model call: it retains the
V4.5.4.3 validator, raises the geometry budget to 16,000 tokens and requires every cited defect to
have visible/partial evidence plus a positive-area normalized region. Its 36 candidate tests and
eight proposal tests pass. It still requires the one-case malformed-table probe before freezing or
Gate A:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5_4_4/`

---

# Prior live checkpoint — 2026-11-05 22:55 PST

The grouped V6.1 review report is complete and published with 16 source-input groups of 10:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/grouped_by_source_input/viewer.html?ldap=hshariati

Four bounded Astra gateway attempts produced no usable answer; the final text-only request also
timed out after 900 seconds. Preserve the attempt evidence under
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/astra_design/`
and do not attribute the local synthesis or later judge revisions to Astra.

Judge V4.5.2 fixed the false `missing_required_support` behavior for a cropped chair case, but its
Gate A geometry observer missed the human-labeled malformed printer table. V4.5.3 made both
table-depth edges mandatory and still called the table coherent despite tracing the decisive
coordinates: left horizontal run/table width 1.55%, right 20.11%, with equal vertical runs. It is
rejected. V4.5.4 added an explicit 3%/15% asymmetry criterion; its first one-case probe exhausted
the 8,500-token geometry budget twice and returned an explicit unassessable error. V4.5.4.1 is
being prepared with the same prompt and a 12,000-token geometry budget. This remains development
tuning; do not freeze or run the six-case gate until the exact malformed-table probe succeeds.

The movable-position V22.4.3 guard change passed 172 tests, 31-real/55-synthetic calibration replay,
and replayed 60 compatible prior rows with exactly one intended selection change. Its fresh full160
launch stopped correctly on row 1: both close-up images preserved orientation but drifted in outer
silhouette/scale and failed the unchanged 0.80 boundary guard at 0.691 and 0.743. The endpoint is
stopped and all evidence is preserved. This is a genuine invariant failure, not a hang or wrapper
bug. A separately named V22.4.3-R1 qualitative-assembly wrapper with at most one transparent outer
job retry is being prepared; it must report native first-job, recovered, and terminal-failure rates
and cannot be described as native per-job V22.4.3 reliability.

---

# Live checkpoint — 2026-11-05 22:25 PST, V4.5.2 Gate A and V22.4.2 wrapper failure

The grouped 160-row review remains published and unchanged. Four Astra consultations produced no
usable output; the final text-only attempt timed out after 900 seconds, so no judge change is
attributed to Astra. Exact attempt evidence is under
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/astra_design/`.

V4.5.1 was rejected on its first Gate-A repeat because it incorrectly called an off-frame table
support `missing_required_support`, turning the known chair-displacement review case into a fail.
V4.5.2 changes only that visibility rule plus versioned plumbing: missing support now requires raw
pixels that rule out an off-frame support. It passed preflight, 23 tests, schema checks and a
read-only freeze verification before any V4.5.2 model call. Frozen protocol SHA-256:
`7238997f8a43bcb938ee4306b2e5cd6b81080c43bcc059bd4adb7743432e08a1`.

V4.5.2 Gate A is rejected and stopped after 5/18 repeats. The chair case improved as intended:
3/3 review/88, all with `chair_displacement`, none with the forbidden `missing_required_support`.
The first two wide-printer repeats both failed for `misplaced_support_furniture` but both missed the
separate required `malformed_support_furniture` issue. At 0/2 detections, the frozen two-of-three
criterion was mathematically impossible, so the run stopped before repeat 3 or later cases.
Evidence:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5_2/runs/dev_6_gate_a_v4_5_2_gpt55/EARLY_STOP_DIAGNOSTIC.md`.
V4.5.3 is now a development candidate focused on explicit opposite tabletop-edge tracing and gross
asymmetric convergence; do not scale it without a new frozen Gate A and held-out Gate B.

The V22.4.2 pipeline change itself passed 170 tests and deterministic replay. The first full-160
row generated successfully after one bounded retry; attempt 2 passed the frozen product guard at
0.8859 boundary and 0.9648 internal-edge coverage. The local audit wrapper then failed because it
incorrectly required `planning_request.json`/`planning_response.json` even though this standard
Stage-B branch correctly records `stage_b_attempt_1_request.json` and
`stage_b_attempt_1_response.json`. No later row ran. The endpoint was stopped and the failed tree is
preserved at
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/run/`.
A distinct wrapper-only V22.4.2.1 package corrected that audit contract without changing pipeline
bytes and passed 13 tests. Its fresh row 1 then produced two new images which both failed the
V22.4.2 guard. Both had exactly three sparse SIFT matches that yielded meaningless affine fits, so
the fixed-position RGBA fallback was not dispatched. Offline fallback replay passes attempt 1
(boundary 0.8110, internal 0.9534, shift +1/0) and fails attempt 2 (boundary 0.7341). The endpoint
is stopped and the second failed tree is preserved at
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/run/`.
V22.4.3 is evaluating a narrow sparse-affine dispatch with no prompt or threshold change. Do not
launch until full real/synthetic replay and preservation checks pass.

---

# Prior live checkpoint — 2026-11-05 21:33 PST, V4.5 judge redesign and V22.4 guard calibration

The grouped review requested by Hooman is complete and published. It contains exactly 160 rows in
16 device/camera source-input groups of 10:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/grouped_by_source_input/viewer.html?ldap=hshariati

Local builder and bytes:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/grouped_report/build_grouped_report.py`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/fe_reports/v6_1_consensus_v2_grouped_20261105/`

The Astra-derived V4.4 two-pass judge is rejected. Its Gate A ran three independent repeats over
six reused labeled development cases: all 18 results were scoreable, but material-fail recall was
0/9 repeats, majority verdict accuracy was 2/5 and majority required-issue recall was 1/7. The
stable outputs were primarily stable false negatives. Do not run V4.4 on fresh10 or 160. Frozen
diagnostic:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_4/data/gate_a_diagnostic_v1.md`

Diagnostic freeze SHA-256:
`d08bf5ee19f37b17064b1b2d4510fbf002f3ce68f8187fee9e9bf5f40526e066`.

V4.5 is in development. A one-call focused visual probe that removed the scene prompt improved
required-issue recall from 1/7 to 3/7, but only 1/5 labeled verdicts matched because it over-scored
the movable chair and under-scored the stranded table/floor-prop failures. It still missed malformed
support furniture, missing load path, device/support axis conflict and shared-perspective conflict.
This probe is diagnostic only:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/root_probe/focused_probe_diagnostic.md`

The final bounded Astra architecture consultation is running with six compressed raw scenes after
an 85 MiB request was rejected and a 24-image compressed request exceeded the 12-minute wall-time
cap. Both failed/terminated attempts are preserved beneath:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_5/astra_design/`

Do not scale a V4.5 candidate until it improves the same six-case development gate, then passes the
pre-frozen fresh10 held-out gate. The likely architecture is separate functional/room and
geometry/topology visual scans, deterministic severity/subtype mapping and at most one bounded
adjudication call. Adding more broad rubric prose is not sufficient.

The movable-position image-pipeline experiment is also paused before scale-up. V22.3.3 passed its
fresh eight-case smoke, but the full160 run stopped safely on row 1 because SIFT could not verify a
featureless Cashmere laptop lid. V22.4 adds a fixed-position-only alpha-mask fallback using
silhouette boundary, internal-edge and high-pass evidence with only +/-8-pixel translation search.
The first frozen calibration had 31 real attempts and 55 synthetic attempts. A fresh first-row
development retry showed the visually faithful attempt at 0.832 boundary coverage and its visibly
degraded fallback at 0.655; the initial 0.85 boundary threshold rejected both. A documented 0.80
candidate retains zero synthetic false accepts/rejects, and the strongest forbidden synthetic is
0.749. This threshold is being re-frozen with the fresh row explicitly treated as development
evidence. Do not restart full160 until the remaining smoke gate passes.

Current pipeline evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4/`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_first_row_retry/`

No judge160, treatment160 or S3 treatment publication is currently running. Preserve all prior
artifacts, unrelated working-tree changes and user-owned
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/prompt1.md`.

---

# Prior live checkpoint — 2026-11-05 active Astra judge and movable-position experiment

Hooman authorized four connected tasks. Preserve the published consensus V2 report and its
annotations; all revisions use new immutable prefixes and version folders.

1. Build a grouped FE revision of the 160-row consensus report with exactly 16 source-input groups
   and 10 prompts per group so within-input diversity is reviewable. `/root/grouped_report` owns the
   mechanical build/publication and must verify grouping from source metadata.
2. Retrieve the 15 published comment-only annotations from the consensus combined report and have
   Direct OpenAI GPT-6 Astra analyze them with the complete judge context. `/root/astra_judge_update`
   owns a persistent tmux invocation, durable prompt/output/provenance and an isolated V4 candidate;
   it must not alter V3 or infer missing comments as passes.
3. After V4 is frozen, evaluate the grouped 160 images with it and publish another grouped report.
   This is dependency-ordered work and has not started yet.
4. Reproduce Foundry PR 4349 in an isolated durable checkout, ask Direct OpenAI Astra for the
   smallest system-prompt change that permits x-y relocation while preserving the exact device
   orientation, run a persistent local endpoint, smoke-test, then generate the V6.1 160-prompt
   experiment and evaluate it with the updated judge. `/root/pipeline_experiment` owns preparation
   through smoke testing; the full run begins only after the smoke evidence is checked.

The Astra route is the Direct OpenAI client in
`/home/colligo/hs_scripts/claude/monitor/ASTRA_FOUNDRY_GATEWAY_HANDOFF.md`, concurrency one,
retries eight, timeout 600 seconds. It is separate from the rate-limited Azure eastus2 route.
Astra receives only the explicit self-contained prompt; credentials must never enter prompts or
tracked artifacts. All long processes must run in named detached tmux sessions because the user may
disconnect. Durable work stays beneath `/home/colligo`; `/mnt/localssd` is scratch only.

Current annotation source was independently confirmed accessible at
`s3://foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/combined/annotations/reviewer_0.json`:
15 rows, zero configured questions, SHA-256
`d466958fc707f504f70ec0c7273a433dfc84826aa36a1cbb46a0df201b51a1f3`. Comments repeatedly ask
for less strict movable-chair handling, stronger furniture-leg/deformation checks, wall/table
perspective and room-placement checks, printer wall gap/alignment, and rejection of incoherent floor
props. Exact comments remain primary evidence.

Next exact step: monitor the three active agents; verify persistent Astra/tmux artifacts and the
group definition. When the Astra V4 candidate is frozen, reuse the grouped-report worker for the
dependent V4 160-image evaluation. When the pipeline smoke test passes, inspect the exact prompt
delta and orientation evidence before launching all 160 generations. Update this checkpoint after
each bounded batch. Do not touch unrelated worktree changes or `judge/prompt1.md`.

---

# Prior checkpoint — 2026-11-05 consensus revision complete

The requested judge iteration and new160-image evaluation are complete. Current research candidate: `placement-consensus-additions-decision-v1`, source-binding implementation frozen in `placement/versions/v3/experiments/consensus_policy/protocol_snapshot_v2`. This is not a production acceptance gate. V2 and the paused V6.1 writer are unchanged.

## Results and limitations

- Development:6/11 mapped verdicts versus V2's5/11;2/2 extended explicit positives retained;55/56 broader V2 agreements retained, one previously accepted visitor-chair case becomes review. Additional café-seat and printer-serving-surface material findings survive. These are posthoc development checks, not accuracy estimates.
- All160 new images complete:118 pass/38 fail/4 review. Laptops51/25/4; printers67/13/0. Final verdicts match V2 on this set. An intermediate proposal-aware verifier introduced an apparent EliteBook direction error; consensus removes that added failure without editing any model result. Four trigger cases informed the final method, so do not claim an untouched holdout.
- Selected method: frozenV2 + compactV3; for newly raised material components, require a proposal-aware verifier and separate names-only check to agree on a material shared code. Conflicting/unknown assessments remain explicit, with confidence/review policy. No per-case model choice.
- New-set API calls328/328 successful, zero errors/retries, all returned GPT-5.5-2026-04-24. No model or image-generation job remains running. All raw evidence preserved.
- Independent audit recomputed244 development+new records and1,220 components, exact sources/trigger coverage/both checks/scoring/policy. No mismatches. Report build and S3 checks verified all22 selected-revision objects byte-for-byte; earlier22 report objects unchanged.
- Browser proof verifies first/last/changed rows, correct source images/twins, score/explanations, both checks and disagreement details, separate image-quality/judge-agreement questions and local comment persistence. No annotations published. Gateway automated navigation timed out; UI proof used exact published bytes over localhost with hash-bound image routes. Interactive user sign-in not tested automatically.

## Selected published review reports

- combined: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/combined/viewer.html
- laptops: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/laptops/viewer.html
- printers: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/printers/viewer.html

Use the full `review_urls` (LDAP + encoded two-question configuration) in `placement/versions/v3/data/v6_1_consensus_v2_fe_publication_manifest_20261105.json` when sharing. Actual selected S3 prefix is `s3://foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/` (no `eval_sets/` in this published prefix). Earlier proposal-verifier report remains archived at the parent prefix; do not overwrite either annotations folder.

## Durable artifacts

- Canonical synthesis: `placement/versions/v3/SUMMARY.md`.
- Selected development84/new160: `placement/versions/v3/experiments/consensus_policy/runs/consensus-84-v2` and `consensus-160-v2`.
- Frozen sources: `placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json`.
- All base/compact assessments: `placement/versions/v3/runs/v6_1_v2_baseline` and `runs/v6_1_compact_v3`.
- Proposal and names-only check artifacts: `experiments/verify_additions_v6_1` and `experiments/independent_component_check`.
- Independent audits: `experiments/two_pass/audit_20261105/consensus_audit.json` plus prior audits.
- Publication/browser proof: `data/v6_1_consensus_v2_fe_publication_manifest_20261105.json` and `data/v6_1_consensus_v2_fe_browser_verification_20261105.json`.
- Exact pixels: ignored `judge/local_runs/v6_1_placement_assets`, backed-up home and recoverable from S3 manifest. No credentials or image base64 in stored requests.

## Next exact step

When Hooman publishes feedback, retrieve reviewer files read-only from the selected consensus report's `printers/annotations/`, `laptops/annotations/` (and combined if used). Preserve image-quality ratings separately from judge-agreement ratings; comments remain primary. Join by exact image hashes and de-duplicate cross-report submissions before counting. Freeze a prospective family-aware development/validation split before changing the next judge. Do not treat absent/blank feedback as a pass, do not resume V6.1 writer automatically, and do not edit user-owned `judge/prompt1.md` or unrelated working-tree changes.

---

## Historical checkpoints (superseded where the live checkpoint differs)

# Placement judge checkpoint — 2026-11-05

## Active v3 iteration — 2026-11-05

Hooman published printer/laptop feedback and requested a judge update before new generations arrive. Both S3 submissions were retrieved: 89 records, 84 nonempty comments, five blank comments, seven source rows absent. Ignore all button selections by explicit user instruction; preserve comments and mixed/ambiguous opinions without manufacturing absolute labels. Blank means no concern raised, not scored ground truth.

V3 is isolated in `placement/versions/v3/`. Root-authored prompt/schema now inspect support-furniture placement in the room, functional scene narrative, empty shelving/bare staging, alternative actual seating and optional-versus-required adjustments. Existing five weights and severity veto remain unchanged. V2 remains reproducible and untouched. Current V6 feedback is development data; future new generations provide fresh evaluation.

Completed 48 real diagnostic calls: initial GPT-5.5 candidate20, GPT-5.6-terra/no-examples probe8, second GPT-5.5 candidate20. All completed without API errors; raw predictions unchanged. Verdict expectation checks: V2 baseline5/11, initialV3 3/11, secondV3 2/11; alternativeprobe2/6 on its eight cases. These are mapped comment-development checks, not held-out accuracy. Second candidate catches more empty/disconnected staging issues but still misses cabinet placement and café seating, and falsely rejects acceptable/ambiguous scenes. Seventeen runtime/scoring tests passed.

V3 is **not promoted**; `data/release_status.json` retains V2 as the comparison baseline. Second candidate protocol is frozen in `data/protocol_freeze_v2.json`; initial source bytes remain under `protocol_snapshots/initial_v1`. Canonical findings and exact reproduction commands: `placement/versions/v3/SUMMARY.md`. Do not overwrite V2 or present either judge as a calibrated acceptance gate.

Next executable action: receive Hooman's new generation manifest/gallery, confirm image/twin/prompt mappings and stage, preserve a fresh split before evaluating. The prior V6 feedback is now development material. Any further candidate improvement must address visual wall-depth/seat-association errors; do not conceal poor test performance with more rules or manual output repair. No new scene generation is currently running. Unrelated V6.1 report edits and monitor changes belong to other work and must remain untouched.

## Completed v2 checkpoint

Natural placement judge v2 evaluation and FE publication are complete after Hooman rejected all four v1 review examples. **Research-only; not ready for automatic image acceptance.** V6.1 remains frozen; no scene images were generated during this judge task.

## Active v2 checkpoint

- New rubric/schema/scoring/runtime are isolated under `placement/versions/v2`; v1 is unchanged.
- Live V6 inventory verified: 96 generated scenes + 16 corrected twins, zero hash/mapping mismatches. Frozen text set has 160 prompts; 64 have no image in this preview.
- Full human evidence now includes 63 previously missed per-variant comments: 92 text annotations, 135 clauses, 278 structured answers preserved separately from placement labels.
- Root-authored rules strengthen device/support/furniture alignment, actual chair reach, clear access, natural printer wall/side placement and coherent scene activity. Severity ≥2 at medium/high confidence now fails; explicit score caps prevent averaging away defects.
- Four-case prompt-only regression: 3 fail/1 incorrect pass. With old 5 visual references: 2 fail/2 incorrect passes. GPT-5.6-terra also misses row25; GPT-6-Astra exhausted three 429 retries. Final GPT-5.5 high protocol uses seven fixed exemplars (four new user failures, older floating example, two reference photos). Feedback regression excludes the target's own exemplar: 3 fail/1 incorrect pass (row12). Another three reviewed images detect 3/4 exact dimensions, missing row02 alignment. No generalization claim.
- Full 96-case run completed with 0 errors: 50 pass, 44 fail, 2 review. Laptop: 27/19/2; printer: 23/25/0. All image/twin/prompt hashes, raw response observations, model identity and recomputed scores verified. No manual output repair. Freeze: `placement/versions/v2/data/v6_run_freeze.json`; audit: `data/evaluation_summary.json`.
- Combined96, laptop48, printer48 and four feedback-example FE reports published; all 19 uploaded objects downloaded and SHA-256 verified. Chromium verified first/last pages, real images, scores, filters and local comment/verdict persistence. Real gateway annotation publication is left to Hooman; no test annotations were sent.
- Publication manifest (including preconfigured editable review URLs): `placement/versions/v2/data/published_report.json`. S3 prefix: `s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/`.
- 2026-11-05 reproducibility correction: the four-case manifest builder now reproduces the latest user feedback in both top-level and nested evaluation metadata. Row12's expected issue is `unmotivated_position`; its older alignment comment/codes remain separately recorded. Original run input snapshot, runtime inputs and model judgments are unchanged. Seven FE tests passed after rebuilding.
- Full live annotation files were re-downloaded read-only and all five byte-match preserved sources: `data/live_annotation_byte_verification.json`.
- 32 core/report tests passed before the final formatting check; final report tests additionally verify score visibility and uncertainty notes. Browser verification: `data/browser_verification.json`.

Next executable action: collect Hooman's published annotations from the four new report `annotations/` prefixes. Preserve raw submissions and deduplicate image/reviewer records across combined and per-device reports. Compare human labels to untouched predictions, especially the row12 development miss and the tight Cashmere case highlighted as an uncertainty question. New V6 labels must be split by case/device-view family before tuning and fresh validation. Do not treat the current predictions as human-approved or resume V6.1 automatically.

Review entry points (append the `review_query` from fe_build.json to skip questionnaire setup):
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/combined/viewer.html
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/laptops/viewer.html
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/printers/viewer.html
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/user_feedback_regressions/viewer.html

Canonical current synthesis: `placement/versions/v2/SUMMARY.md`. All needed code/data/results live under backed-up /home/colligo; downloaded pixels are ignored in Git and recoverable from verified S3 manifests. Preserve unrelated monitor deletions and user-owned judge/prompt1.md.


## Frozen v1 history

- Four-report annotation inventory (5 reviewer submissions, 158 records); 15 printer reference photos visually inspected.
- 101 source images downloaded and SHA-256 verified under durable ignored local_runs/ (30 twins, 56 generations, 15 references).
- Five-component scoring, strict output schema, unknown/coverage behavior and provisional pass/review/fail; 40 tests pass.
- Text-only GPT-5.5 medium/high trials, small GPT-5.6-terra comparison; GPT-6-Astra diagnostic exhausted 3 rate-limit retries. Raw responses/errors preserved.
- Final GPT-5.5 high + 5 fixed visual examples run: 18 target images (8 development, 10 held-out), all valid. Three demonstration case families excluded. Prompt/schema/policy/anchors/split hashes frozen before held-out and unchanged afterward.
- Held-out reach complaints detected in all 3 specifically attributed images. Missed additional alignment complaint in row 13 V14 and comparison-set alignment complaint in row 26. Thresholds not calibrated: no absolute placement labels or reliable clear-pass controls. See placement/SUMMARY.md.
- Review gallery built with inputs, twin, scene, all 5 fixed examples, scores/components, exact human evidence and raw artifacts. JavaScript rendering test: 18 cards, 90 component assessments, 10 held-out filter rows, 5 anchors; all 33 image assets present. No full browser/IMS login check in this environment.

## Artifacts

- Canonical findings/rubric: placement/SUMMARY.md.
- Code: placement/run_judge.py, scoring.py, observation_schema.json.
- Final results: placement/runs/pilot_v1c.
- Report source/bundle: placement/build_report.py, placement/report/gallery (generated bundle ignored).
- Publication target: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v1_20261104/gallery/index.html
- Publication completion and byte hashes: placement/data/published_report.json (132 files downloaded and byte-hash verified).

## Historical v1 next step (superseded by v2 above)

Use the published evidence gallery to collect independent placement-specific ratings for clear passes, borderline/material/major defects, and tight/unobservable crops. Improve table/product-axis visual reasoning on DEVELOPMENT cases, then calibrate weights/severity/verdict thresholds and test another untouched case-family split. The current held-out images have now been reviewed; do not reuse them as a new untouched test.

No access blocker for AWS/GPT-5.5. GPT-6-Astra rate-limited in a bounded probe. V14 scene code/report lineage is supported but raw-PNG stage chain remains incomplete. Never silently turn this research prototype into an acceptance gate. Preserve unrelated monitor working-tree deletions and judge/prompt1.md user input file.
