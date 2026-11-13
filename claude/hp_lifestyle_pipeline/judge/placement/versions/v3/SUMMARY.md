# Natural placement judge V3

As of 2026-11-05. **Research candidate for human review; not an automatic acceptance gate.** V2, every failed V3 experiment and all original model outputs remain preserved. No scene images were generated in this task, and the V6.1 writer remains paused.

## Contents

- [Outcome and limits](#outcome-and-limits)
- [User contract and evidence](#user-contract-and-evidence)
- [Selected method](#selected-method)
- [Development results](#development-results)
- [New 160-image evaluation](#new-160-image-evaluation)
- [Experiment history](#experiment-history)
- [Reproduction and artifact map](#reproduction-and-artifact-map)
- [Next validation](#next-validation)

## Outcome and limits

**VERIFIED:** Continued iteration produced a small development gain: the selected consensus method matches 6/11 mapped verdict checks versus V2's 5/11. It retains both explicit positive examples in the extended check and 55/56 earlier comment agreements with V2; one previously accepted image becomes review because the checks disagree. It retains additional material café-seat and printer-serving-surface concerns. This is a recall/uncertainty tradeoff, not evidence of universally higher accuracy.

**VERIFIED:** All160 new V6.1 scene images were assessed using their actual original twin renders and original prompts. The selected revision yields118 pass,38 fail,4 review. These are model predictions, not human labels. The final verdicts on this set match the frozen V2 baseline; the intermediate single-verifier revision had introduced one additional failure, which the consensus revision removes.

**UNVERIFIED:** Generalization, false-positive rate and calibrated score thresholds remain unknown. Repeated development tuning and inspection of four new-image trigger cases prevent a held-out accuracy claim. Several known cabinet-position and seat-association failures remain. A high model confidence or score100 is not verified human approval.

## User contract and evidence

**USER-CONFIRMED:** Inputs are generated scene image, original digital twin, laptop/printer type and original scene prompt. Score the scene-generation image, not a final relit image. Return0–100, component evidence, confidence/coverage and pass/review/fail. Unobservable relations are distinct from wrong placement. Printers should use practical dedicated/shared supports; laptops should face and reach the actual user position. Product/support/furniture axes should align in3D, not necessarily have identical image slopes.

The published reviewer buttons must be ignored because Hooman used them as image ratings rather than judgment agreement. Comments are authoritative user feedback; blank comments are not positive labels. The two retrieved submissions have45 printer and44 laptop records:84 written comments,5 blank,7 of96 source rows absent. Brief “agreed” is agreement with the displayed V2 assessment, not an independently established absolute label.

Primary submissions, preserved with hashes in `data/feedback_20261105`:

- s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/printers/annotations/reviewer_0.json
- s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_natural_placement_judge_v2_v6_20261104/laptops/annotations/reviewer_0.json

Earlier four report families, training-photo illustrations and direct user failures are catalogued under V2 and the original placement version. The V2 stage intentionally includes seven fixed visual examples with human-derived guidance; the evaluated target's comments are withheld. Do not describe this as “no human feedback anywhere in the model context.” Target-identical anchors were excluded during their development regression checks.

## Selected method

Every image receives two GPT-5.5/high assessments: frozen V2 with its seven fixed examples, and the compact V3 relationship rubric without examples. Both see the original generated image, reference twin, type and source prompt. The V3 rubric checks room→support→device→user relationships, practical surface allocation, real seating, believable prop roles, staging and physical integration.

If compact V3 raises a newly confirmed material component beyond V2, two further checks inspect that component:

1. A proposal-aware verifier sees the earlier concern as a fallible claim and reinspects the image.
2. A separate check sees only component names, not the accusation, score or issue codes. Its rubric explicitly traces keyboard deck, display face and seat position rather than equating the camera-facing lid with the user's side.

A new material component is accepted only when both checks are observed/partial, medium/high confidence, severity≥2, and share an issue code. The application uses shared codes, the lower severity/confidence and quotes both sources. Confident clear/minor counter-evidence rejects the addition. Unconfirmed uncertainty preserves the baseline component and can defer a prior pass to review; disagreements remain visible and cap high reported confidence to medium. Non-trigger components retain the existing two-pass policy. This is one rule for every record, not a per-case selection of the preferred answer.

The five weights remain support20/access30/orientation20/scale15/contact15. Severity0–4 maps to component100–0; unobservable components are excluded from the weighted average. Confirmed material severity≥2 vetoes pass, with59/39/19 caps for worst severity2/3/4. Existing score and coverage thresholds remain provisional. All merge, consensus and final-decision fields are application-derived; raw model assessments are immutable.

**RESEARCHER DECISION:** Use this method for the current review report, with the limitations above. It adds model cost and still preserves V2's existing errors. It is not ready for unattended acceptance or automatic regeneration.

## Development results

The20-case diagnostic has11 nonempty verdict expectations and15 issue expectations mapped from comments. The separate64-case check has2 explicit labels,56 agreements with V2 and6 issue expectations. These sets contain retrospective development material; the broader check was frozen before compact outputs but its source comments had already informed the work.

| Check | V2 | Selected consensus |
|---|---:|---:|
| Diagnostic verdict expectations |5/11|6/11|
| Diagnostic issue-any, including mild findings |3/15|5/15|
| Extended explicit positive labels |2/2|2/2|
| Extended agreement with prior V2 verdict |56/56|55/56|
| Extended issue-any |2/6|3/6|

An issue-any match does not verify every companion code or explanation. In the preceding verified version the diagnostic5 broad matches contained only4 material matches; the fifth was mild staging. Audits expose severity/confidence and unassessed companion codes rather than treating every match as a fully correct judgment. The consensus rule retains the three newly corroborated material components: two café-seat components and one printer-serving-support component. One visitor-chair case becomes review; it is not silently counted as a retained pass.

A six-case repeat of the proposal-aware verifier retained all three original material components, but only3/8 component records were exact repeats, and two other findings flipped mild→material. The later names-only check corrected the new EliteBook orientation accusation but reintroduced the old visitor-chair concern. Those disagreements motivated consensus. No best response was selected from repeated calls.

## New 160-image evaluation

Source gallery:
https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105/gallery/index.html

**VERIFIED input lineage:**160 unique scenes,80 laptops/80 printers,40 per device,16 device/view banks. Live job metadata marks sceneOnly: hero+scene done and harmonization/relighting stages skipped. Scene files are2_scene.png and actual reference renders1_hero_white.png. Four Cashmere input twins differ from the earlier V6 images; the old references were not reused. All pixels and prompts are hash-bound to the manifest.

| Device type |Pass|Fail|Review|Total|
|---|---:|---:|---:|---:|
|Laptop|51|25|4|80|
|Printer|67|13|0|80|
|All|118|38|4|160|

There were160 baseline calls,160 compact calls,4 proposal-aware checks and4 names-only checks for this image set. All328 calls returned GPT-5.5-2026-04-24 successfully without retries. The four trigger cases contained five components; consensus retains one material printer-support addition and rejects four laptop additions. Other baseline concerns still determine those rows' verdicts. No final verdict changes relative to V2 remain.

The intermediate verified report had117 pass/39 fail/4 review. Root visual inspection raised a concern about its sole newly failed row, `elitebook__laptop_BackRightCloseUp__p9`: the visible keyboard deck appears to extend toward the chair. The names-only model separately cleared the alleged reversed orientation. This is a researcher/model disagreement, not a new human gold label. The old report remains preserved; the selected consensus revision is separate. Four trigger images have now informed development, so the final160 is an unlabeled evaluation probe, not an untouched holdout.

Selected reports (full native questionnaire URLs are in the publication manifest):

- combined: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/combined/viewer.html
- laptops: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/laptops/viewer.html
- printers: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/printers/viewer.html

FE reports provide the original scene, exact twin, original prompt, final score/explanation, component provenance and all assessment stages. Two separate native questions ask whether the image is naturally arranged and whether the reviewer agrees with the judge. No test annotations are published. Publication manifests record immutable S3 keys and byte verification. Corporate-gateway automated navigation timed out for the first report; browser proof used the exact downloaded viewer/data bytes and hash-bound local image routes. Interactive user login was not tested automatically.

## Experiment history

| Experiment |Cases|Mapped verdict matches|Decision|
|---|---:|---:|---|
|Initial V3, expanded rules + nine examples|20|3/11|Not selected|
|Initial alternative model/context probe|8|2/6|Not selected; model/context confounded|
|Second V3 + seven examples|20|2/11|Not selected|
|Compact GPT-5.5, no examples|20|4/11|Useful second assessment, not replacement|
|Compact GPT-5.6-terra|20|5/11|New false failure; not selected|
|Full image + four overlapping crops|20|5/11|No replacement gain|
|V2 + compact, worst confirmed components|20+64|6/11|New false failure in broader check|
|Added proposal-aware verification|20+64|6/11|Small gain; stochastic and orientation weaknesses|
|Names-only component probe|10/13 components|Not a whole-judge verdict test|Opposing errors motivate consensus|
|Selected two-check consensus|20+64|6/11|Research review candidate; one additional review|

Sixteen freeform image-first probes did not resolve the core furniture/seat errors. GPT-6-Astra hit three429 attempts on the initial probe; GPT-6-sol returned404. These are access failures, not quality results. No model was silently substituted. Twelve initial verifier requests were rejected with schema400 before usable responses; the schema's missing explicit string type was fixed, and the six valid semantic responses were preserved in a distinct run. Failed requests and snapshots remain auditable.

## Reproduction and artifact map

Project root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3`.

- `data/comment_inventory.json`, `data/diagnostic_cases.json`, `data/extended_validation_cases_20261105.json`: comments, targets and explicit expectation provenance.
- `system_prompt.md`, `observation_schema.json`, `scoring.py`, `run_judge.py`, `run_batch.py`: compact stage, validated inputs and scoring. This single prompt is only one stage of the selected method.
- `protocol_snapshots/initial_v1`, `protocol_snapshots/second_v2`, `data/protocol_freeze_v*.json`: immutable earlier methods.
- `experiments/two_pass/`: deterministic original combination; independent audits under `audit_20261105`.
- `experiments/verify_additions/`: proposal-aware prompt, original six-case checks, repeats and frozen decision policies.
- `experiments/independent_component_check/`: root-authored names-only prompt, ten-case manifest, exact requests/results and comparison.
- `experiments/consensus_policy/`: selected deterministic policy, source snapshots, tests, development84 and new160 results. The exact generator and policy hashes are embedded in each envelope.
- `data/new_v6_1_eval_20261105/manifest.json`: complete original image/twin/prompt lineage, SHA256 `fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc`.
- `runs/v6_1_v2_baseline`, `runs/v6_1_compact_v3`: all320 initial assessments; their freezes are in `data/`.
- `experiments/verify_additions_v6_1/`: four new-image proposal checks and intermediate verified160.
- `build_fe_report.py`, `publish_fe_reports.py`, `data/*publication_manifest*.json`: strict report validation, immutable publication and full review URLs.
- `data/release_status.json`: selected candidate and explicit no-automatic-acceptance status.

Use the source paths/hashes in each consensus run's summary and audit to reproduce the exact merge without model calls. The model-stage commands are recorded in their freezes and input snapshots. New model calls may differ, as the repeat demonstrated; reusing a saved response is not a fresh model evaluation. Keep target feedback outside the five-field runtime whitelist. Raw pixels live under ignored, backed-up `judge/local_runs/`, recoverable from verified S3 manifests. Credentials and image base64 are absent from stored requests.

## Next validation

Collect placement-specific human comments on the selected FE revision. Preserve image quality and judgment agreement separately; do not reuse old misinterpreted buttons. Prioritize false passes, false failures, uncertain seating and whether the explanations describe the correct relations. Keep image/view families together in a prospective split before further tuning. The cheapest useful next evidence is fresh review of these outputs, not another unreported prompt expansion or manual correction of selected results.
