# Natural placement judge v2

Updated 2026-11-04. Research evaluation; thresholds remain provisional. The writer V6.1 work is paused and unchanged.

## Contents

- [Scope and evidence](#scope-and-evidence)
- [Changed standard](#changed-standard)
- [Scoring](#scoring)
- [Evaluation status](#evaluation-status)
- [Reproduction and files](#reproduction-and-files)

## Scope and evidence

**USER-CONFIRMED:** Hooman rejected all four former review examples: row 25 V14 (printer/table alignment), row 12 V13 (printer placement relative to table/wall), row 9 V14 (laptop/seat reach and access), row 29 V13 (laptop too far from chair despite an appealing narrative). These are development feedback, not a new held-out test.

**VERIFIED:** Live V6 preview storage contains 96 distinct scene images and 16 corrected twin renders, covering p1–p6 in 16 device/view banks. The frozen prompt set contains 160 texts; the other 64 have no image in this preview and are excluded from visual scoring. Original prompts, image bytes, twin bytes and dimensions were matched with zero manifest discrepancies. All are 2368×1776. See `data/v6_assets.json` and its source/hash fields.

**VERIFIED:** The full annotation extraction contains 158 reviewer-row records, 278 structured answers and 92 nonempty text annotations (29 top-level comments plus 63 previously omitted per-variant comments), split into 135 quoted clauses. The 64 placement-related clauses have 42 exact single-variant attributions, one exact both-variant attribution and 21 ambiguous comparison-set attributions. Preference/fidelity/lighting/style votes are context, not absolute placement ground truth. See `data/human_evidence.json` and `HUMAN_EVIDENCE.md`.

Prior V13/V14 feedback-image stage attribution retains its recorded lineage limitations; naming an input `scene_generation` is not independent proof of stage. The V6 preview is the scene-generation endpoint output, not a third-party relit result.

## Changed standard

The root agent authored `system_prompt.md`. It requires:

- Matching device/support axes in 3D, and coherent nearby furniture alignment. Screen-space slopes alone are insufficient because perspective makes parallel edges converge.
- A laptop within ordinary reach of the actual visible chair, with no obstructed working path. No imagined replacement chair to excuse the shown arrangement.
- A sensible dedicated printer position: wall-aligned/set back/toward a practical side when the scene supports that arrangement, with an unobstructed operating front. A narrow dedicated cabinet can center its printer. Exact wall contact is not required where functional clearance is needed.
- A visible, coherent activity connecting furniture, working props and the product. Attractive narrative cannot rescue bad placement.
- Plausible support, scale, perspective, weight/contact, shadows and reflections. Hidden evidence stays unknown.

## Scoring

Weights remain support/scenario 20, access 30, orientation 20, scale/perspective 15 and contact 15. Each observable component has severity 0–4 and score `100 − 25 × severity`. Unobservable components are excluded from that weighted mean; coverage falls instead.

**RESEARCHER POLICY, NOT CALIBRATED:** A clear severity ≥2 defect at medium/high confidence causes fail. The raw weighted component mean is preserved, but the final natural-placement score is capped at 59 for severity 2, 39 for severity 3 and 19 for severity 4. This keeps a material defect from averaging into an apparently good score. These caps are ordinal policy choices, not empirical probabilities.

Pass still requires score ≥80, coverage ≥0.70, adequate confidence and assessable core support/access/orientation without material defects. Review covers uncertainty, insufficient visibility or an invalid/uncertain product match. No score is assigned when all components are unobservable. The scene narrative is written diagnostic evidence, not a sixth score or a way to offset failure.

## Evaluation status

- Prompt-only development regression on four new user failures: 3 fail, 1 incorrect pass (row25 V14 alignment). Row12 V13 fails for alignment but still misses the user's stated position concern.
- The same updated rules plus the five old visual exemplars: 2 fail, 2 incorrect passes (both printers). This demonstrates remaining visual-reasoning difficulty; more stringent aggregation alone cannot fix missed evidence.
- Bounded GPT-5.6-terra prompt-only probe: 3 fail/1 incorrect pass (row25). GPT-6-Astra probe: three rate-limit errors; no judgment produced. Model substitution did not resolve the issue.
- Final protocol: GPT-5.5 high with seven fixed development images (four new user failures, one older floating example, two reference photos). During feedback regression, each target's own image and label/guidance are removed, leaving six examples. All 96 V6 targets receive the same seven examples.
- Final feedback regression: 3 fail/1 incorrect pass (row12's printer position). Another three previously reviewed images detect three of four specifically commented dimensions, with row02 alignment missed. These are development checks, not unseen accuracy estimates. The raw disagreements remain published for audit.
- The 96-image V6 run completed with the frozen prompt/model/policy and zero request failures; see `data/v6_run_freeze.json` and `data/evaluation_summary.json`. No new scene images were generated. All original observations match the raw model responses and deterministic score recomputation; no manual corrections.
- FE annotation entry and reload persistence were browser-tested locally with the exact vendored viewer. Real gateway annotation publication is not simulated or claimed tested. See `data/browser_verification.json`.

| V6 device family | Pass | Fail | Review | Images |
|---|---:|---:|---:|---:|
| Laptop | 27 | 19 | 2 | 48 |
| Printer | 23 | 25 | 0 | 48 |
| Total | 50 | 44 | 2 | 96 |

These are model predictions, not verified human labels. Mean observed per-image latency was 54.44 seconds with four concurrent workers, including fixed exemplars and request overhead. The 96 calls used 1,524,337 total API tokens (including 753,920 cached prompt tokens); this is a measured batch cost/latency profile, not a service guarantee.

A researcher spot check flags `cashmere__laptop_BackRightCloseUp__p1`: the model inferred a user side from props while the chair is out of frame. That may deserve uncertainty rather than an access fail. It is displayed as a review question, not a new gold label or an edited model result. This and the row12 feedback miss show why human calibration is still required.

## Reproduction and files

All paths below are relative to this version directory; user-facing references should show their full absolute paths.

- `system_prompt.md`, `observation_schema.json`, `scoring.py`: root-authored rubric, strict observation contract and deterministic policy.
- `run_judge.py`, `run_batch.py`: model calls, hashes, bounded retries, cache validation and resumable progress.
- `test_v2_scoring.py`: model-free checks for score vetoes, uncertainty, schema consistency, provenance and cache behavior.
- `build_v6_assets.py`, `data/v6_assets.json`: source collection and exact image/twin/prompt mapping.
- `data/regression_user_failures.json`: four feedback cases; human labels never enter target request text.
- `build_fe_report.py`: exact vendored FE viewer plus data; editable human verdict/comments remain separate from model predictions.
- `verify_evaluation.py`, `data/evaluation_summary.json`: all-96 input/response/policy/hash audit and descriptive totals. This verifies pipeline integrity, not image-judgment correctness. Optional Azure latency fields are collected as reported, not mistaken for mandatory scoring-contract fields.
- `data/judgments_v6_96.json`: portable complete predictions with original prompt and image/twin URLs.
- `runs/`: original requests, model responses, judgments and progress. Each request records prompt/schema/scoring/model/image hashes and any fixed examples.

Example validation without API calls:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v2/run_batch.py \
  --manifest /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v2/data/v6_assets.json \
  --run-name v6-validation --validate-only
```

The completed run can be checked and its report rebuilt without new model calls:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v2/verify_evaluation.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v2/build_fe_report.py --separate-four
```

To produce a fresh evaluation with the frozen protocol, use `run_batch.py` with `--manifest` pointing to `data/v6_assets.json`, a new `--run-name`, `--workers 4`, `--model gpt-5.5` and `--visual-anchors`. Exact image bytes must be restored to manifest paths first if the durable ignored cache is absent. Use `build_v6_assets.py` for the V6 cache and v1 `prepare_assets.py` for reference/feedback images, then verify SHA-256. No caller source message or human rating is inserted into target scoring instructions.
