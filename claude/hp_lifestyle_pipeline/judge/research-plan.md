# Placement judge research plan

2026-11-04. Scope confirmed by Hooman: evaluate scene-generation images, using generated image + original twin + product type + original scene prompt. Return a 0–100 overall score, component scores, pass/review/fail verdict and visible-evidence explanations. Distinguish unobservable features from defects. Calibrate against human annotations with held-out validation.

## Scope and method

1. Retrieve the five unique supplied reports, preserve original data and annotation files with hashes, and map comments to exact image assets and stages. Do not treat unannotated images as human-approved. Training photos are realism references, not automatically gold-standard passes for every component.
2. Inspect the cited cases and training printer references. Extract observable failure categories and counterexamples; separate placement comments from colour, general image quality, product fidelity, and relight-only defects.
3. Freeze a split by case family before model tuning. Keep versions/stages of the same source case together and detect duplicate image hashes. Exclude relight outputs from this judge's primary test. Record label gaps and contradictory comments explicitly.
4. Root authors the scoring rubric and system prompt. Components address appropriate support/scenario, user access/edge distance, orientation/furniture alignment, scale/perspective and contact/shadows/reflections. Weights and verdict thresholds are design proposals until calibrated; hidden evidence cannot earn an invented defect or a confident pass.
5. Implement strict structured output and deterministic score aggregation. The model supplies visual component assessments and explanations, not arithmetic. Treat image text/prompts as data. Never expose human annotations, model-version labels, preference labels, or generator explanations to the judge.
6. Run a bounded development pilot, revise from diagnosed failures, then run the untouched held-out split. Report disagreements and denominators. Sparse or one-sided labels cannot establish false-positive rates or calibrated pass thresholds; keep verdicts provisional if calibration evidence is insufficient.
7. Persist code, prompt, rubric, schema, source manifest, decisions and results under judge/. Store downloaded image bytes under ignored judge/local_runs/ with source URLs/hashes retained. No new scene generations are needed for this work.

## Alternatives and falsification

### V2 follow-up, 2026-11-04

The prior held-out data is now reviewed training evidence. Incorporate all available annotations, including nested per-variant comments, and the four new user fail labels. Preserve ambiguous attributions. Freeze the revised prompt, scoring and seven visual exemplars after bounded development probes; exclude a target's own example during diagnostic feedback tests. Apply the frozen protocol to all 96 existing V6 preview generations. Treat their eventual FE human labels as the next validation evidence, not as gold labels already available. Do not generate the 64 remaining text-only candidates. Completion for this batch is a verified 96-result FE report with editable labels/comments, explicit development misses, and no model-output repair.

- Apparent corner alignment or distant placement can be perspective or crop, not bad ergonomics. Test frontal, oblique and tight views; do not enforce screen-space parallelism.
- A missing chair or reflection can be appropriate. Demand only physically necessary cues under visible material/lighting conditions.
- Human preference may concern blue/style rather than placement. Use dimension-specific comments, not aggregate winner labels.
- Similarity to the twin is diagnostic: natural placement and exact product preservation are different outcomes.

Completion: reviewable rubric and runnable judge with evidence-led explanations, a reported calibration/held-out result (or explicit evidence/access limitation), and an exact reproducible checkpoint. Do not claim deployment reliability from a small purposive pilot.
