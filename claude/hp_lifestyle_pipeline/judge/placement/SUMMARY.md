# Natural product placement judge

## Current provisional application judge (2026-11-13)

[USER-CONFIRMED] Astra P1 / R2 (`v3_2_r2`) is provisionally selected as the
advisory Python/CLI default in Adobe-Firefly/colligo#36039, pending additional
independent annotations. Human review remains mandatory; no automatic acceptance
or rejection. Its historical EliteBook malformed-support-furniture calibration
miss is preserved, not reclassified as a gate pass.

[VERIFIED] Integration commit `69b06a3f8582fe724f405f0db44ea1a2b3378725` is
pushed. Exact rubrics, four-stage message/schema parity, seven original exemplars,
209 historical aggregation-parity cases,258 offline tests and one installed-wheel
actual Astra smoke are verified. These are execution/portability checks, not
held-out accuracy estimates. Generation/HTTP APIs and deployments are unchanged.
All68 remote head checks are terminal:33 success/35 skipped, zero failures or
pending checks. Documentation, managed-service lint/builds/tests and Code Review
pass; GitHub reports mergeability clean. PR remains unmerged. Exact final checks
are preserved in the audit's `remote_ci_receipt.json`.

Recipient guide:
https://github.com/Adobe-Firefly/colligo/blob/69b06a3f8582fe724f405f0db44ea1a2b3378725/managed_services/services/firefly/foundry/standalone_apps/hp_image/prompt_rewrite/placement_judge/README.md

Validation/provenance:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/pr36039_integration_20261113`.
The raw smoke backup and exact restore paths are bound in its backup manifest.

## Historical V1 snapshot

Historical v1 snapshot. Current work and corrected full annotation counts are in [placement v2](versions/v2/SUMMARY.md). The 29-comment count below was the incomplete v1 extraction; v2 found 63 additional per-variant comments. V1 code/results remain preserved.

As of 2026-11-04. **Research prototype; thresholds are not yet calibrated.** V6.1 remains frozen.

## Contents

- [Current provisional application judge](#current-provisional-application-judge-2026-11-13)
- [Purpose and contract](#purpose-and-contract)
- [Scoring](#scoring)
- [Evidence and limits](#evidence-and-limits)
- [Pilot](#pilot)
- [Reproduce](#reproduce)

## Purpose and contract

[USER-CONFIRMED] Judge the **scene-generation image**, with the original digital twin, product type and original scene prompt as context. Return a natural-placement index from 0–100, component assessments, a pass/review/fail decision and visual explanations. Do not score downstream relighting, image style or general prompt fidelity.

The runtime accepts only laptop/printer. Unknown types and incorrect stage identifiers return validation errors. The twin helps identify the functional front and load-bearing base. It is not the expected lighting of the generated scene. Prompt instructions cannot override visual evidence.

## Scoring

[RESEARCHER DESIGN — PROVISIONAL] Five components:

| Component | Weight | Main question |
|---|---:|---|
| Support and scenario | 20% | Does the support fit this device/task, with its base safely supported and no occupied workstation displaced? |
| Access and usability | 30% | Can someone reach/use it from a believable sitting or standing position? |
| Orientation and furniture alignment | 20% | Does its working direction fit the table, accessible edge and any relevant chair? |
| Scale and perspective | 15% | Does its size/perspective agree with the surrounding furniture? |
| Contact and physical integration | 15% | Does it have convincing weight and contact, without incompatible shadows/reflections? |

Each assessable component receives severity 0–4: no visible problem, minor awkwardness, material awkwardness, major problem, impossible/nonfunctional. Component score = 100 − 25 × severity. The application takes a weighted average over assessable components. These are ordinal judgment scores, **not probabilities or physical measurements**.

Unobservable components are null and do not lower that average. Coverage is reported separately: observed contributes full weight, partial half weight, hidden zero. A perfect score on a very limited view must not be interpreted as a full placement pass.

Initial verdict policy: any clear major issue triggers fail; a score below 60 also fails when confidence is adequate. Pass requires score ≥80, coverage ≥70%, credible support/access/orientation evidence, no material issue and no uncertain product match. Everything else goes to review. A score of 90 can therefore still need review for one material problem. Thresholds and weights are design choices pending human calibration, not customer-approved measurements.

The judge must assess the arrangement as shown. It cannot rescue a poor position by imagining that a chair/product is moved. Conversely, a missing chair or subtle shadow is not automatically wrong; a projecting printer tray is different from unsupported chassis.

## Evidence and limits

[VERIFIED, source snapshot 2026-11-04] Four supplied annotation reports contain five reviewer submissions, 158 reviewer-row records and 278 ratings. The 29 nonempty comments all come from Zach's 30-row V13/V14 report. The initial extraction identified 20 direct placement-comment clauses; only six identify one output. Some mixed scene-layout comments may contain additional placement evidence, so this extraction is not exhaustive ground truth.

No structured question is placement-specific. Overall preference, scene realism, fidelity, lighting and blue ratings cannot become placement pass/fail labels. A blank comment is unlabeled, not a pass. Two reviewers agree exactly on only 5/32 overall choices in the HP16 V13/V14 report; do not interpret that as placement disagreement.

The three HP16 reports reuse 32 cases. They cannot be treated as independent data. The initial pilot uses a case-level split of the 30-row report, with all variants of a case kept together. Product-input SHA-256 hashes are unique across those 30 rows; same devices/view families can still recur. This is not an unseen-SKU test.

[VERIFIED, visual inspection] All 15 supplied printer reference photos were inspected. They include separate printer cabinets, shared worktables and neighboring computer stations. Several show the printer far in the background or hide its support, and one is industrial printing. They illustrate relationships; they are not 15 gold-standard positive labels for this judge. Their accompanying prior analysis is secondary interpretation, not human annotation. The user's current occupied-desk restriction has priority over an old reference.

[VERIFIED / LIMITATION] V13 scene lineage was checked against archived single-call source code and sampled output-byte matches. V14 report/code lineage supports a scene-generation classification, but no raw PNG job manifest was available to complete the artifact chain. Results involving V14 retain that qualification. See data/stage_provenance.json.

## Pilot

Frozen selection: seven development cases (13 images) and six held-out cases (10 images). Held-out comment text and images are kept from prompt-author review until the judge is frozen. Three exact-target defect comments are available in each split; six other pilot comments are comparison-set ambiguous. One selected case has no direct placement comment.

First attempt failed at API schema validation; no judgments were produced. The flattened schema fixed that integration issue.

First successful development run (`pilot_v1a`, GPT-5.5 medium): all 13 outputs passed, including visible problems named by C-Tech. This is a **failed sensitivity baseline**, preserved rather than manually corrected. Revision makes the as-shown user position, paired table/base axes and base-plane contact explicit, and uses GPT-5.5 high reasoning. These two changes are coupled; their individual effect is not established. Held-out images have not been used for the revision.

Final prototype (`pilot_v1c`, GPT-5.5 high) uses three development scene/comment anchors (rows 2, 8, 21) and two printer reference illustrations. Whole demonstration cases, including companion variants, are excluded: the final target set is **8 development + 10 held-out images**, with no manual response edits. All 18 calls returned valid judgments. Forty schema/runtime/aggregation tests passed; these verify code behavior, not visual correctness.

| Held-out evidence | Outcome |
|---|---|
| Three specifically attributed reach complaints (rows9 V14,13 V14,29 V13) | All three detected |
| Additional alignment complaint in row 13 V14 | Missed; score 92.5/pass |
| Two alignment comments with unspecified variant (rows12,26) | Matching issue in one or more candidates for row 12; missed in both row 26 candidates |
| Provisional verdict distribution |7 pass /3 review /0 fail across 10 images |

The exact-target comments contain four mapped defect types; three were detected. This is **not overall accuracy**. Comparison-set matches are not counted as exact-image agreement. The final development set detected expected alignment in at least one row 25 candidate but missed the other three comparison-level labels. First-run anchors were selected from development feedback and must not be reported as independent test performance.

All five prompt/schema/policy/anchor/split hashes matched the pre-held-out freeze after evaluation. Held-out images and labels were inspected only after freezing and scoring; no further tuning was performed. Model returned `gpt-5.5-2026-04-24`. Mean per-image held-out elapsed time was 52.9 seconds including the fixed examples; this is an observed pilot latency, not an SLA.

**Recommendation:** use as a diagnostic research prototype, not an automated acceptance gate. Reach detection is promising within three narrow cases; table-axis alignment and score severity remain unreliable. Better visual reasoning and independent placement-specific human labels are needed. Do not lower a threshold to disguise missed defects. Sparse positive-only defect labels cannot calibrate false positives or pass/fail thresholds. Before automated acceptance/rejection, collect independent placement-specific absolute ratings, including clear passes, borderline failures and tight crops; freeze thresholds on development and evaluate on another untouched set.

## Reproduce

Canonical files live under `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement`.

- system_prompt.md: exact current judge instructions.
- observation_schema.json: model JSON contract.
- scoring.py: independent validation, coverage, aggregation and provisional verdicts.
- run_judge.py: GPT-5.5 Azure multimodal call. Uses established project auth helper; secrets stay outside this directory.
- run_pilot.py: bounded two-worker evaluation, split metadata excluded from model inputs.
- prepare_assets.py: source image downloads and SHA-256 manifest.
- data/: source report snapshots, annotation extraction, stage provenance, splits and label mapping.
- runs/: exact prompts, inputs (paths/hashes), raw model responses, scores and errors per image.
- build_report.py: review gallery builder.

All required small artifacts are durable under /home/colligo. Image bytes are in ignored judge/local_runs/placement_assets and recoverable from the S3 manifest. Originals are submitted without resizing, detail=high. Target-image human ratings, pipeline versions, intermediate rewrites and geometry guides are excluded from the model call. Fixed development example comments are intentionally included and recorded in the anchor manifest.


### Commands

```bash
python -m pytest /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement -q

# Preserve historical outputs: a new run name generates new judgments.
uv run /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/run_pilot.py --split held_out --run replication_01 --visual-anchors

python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/evaluate_pilot.py --run pilot_v1c --split held_out

python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/build_report.py --include-splits development,held_out --evaluation-summary /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/runs/pilot_v1c/all_evaluation.json --review-summary /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/data/review_summary.json
```

For one image, `run_judge.py --input INPUT.json --output NEW_DIRECTORY --visual-anchors` accepts:

```json
{"generated_image":"/absolute/path/scene.png","twin_image":"/absolute/path/twin.png","product_type":"printer","scene_prompt":"A shared office printer table...","image_stage":"scene_generation"}
```

Paths here are illustrative. A rerun of inspected held-out cases is a replication, not a new untouched validation set. Transport failures retry at most three times; model/schema failures stay explicit. Never silently substitute models or hand-edit judgments. The runner binds cache identity to code, wire schema, images, fixed examples and prompt; old runs created before hardening remain archived and are not silently re-used under the changed protocol.
