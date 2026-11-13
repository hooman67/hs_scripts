# Longer-term work

2026-10-28: V6 design is approved and implementation exists separately from V5, with local tests. After individual prop approvals, evaluate unedited GPT-5.5 outputs for 10 prompts with disjoint approved prop types, source-first ranking, plausible environment diversity, qualitative camera guidance and bounded unattended validation/repair. Evaluate raw-model reliability separately from reviewed examples. Prop restrictions also need downstream enforcement; do not infer final-image compliance from upstream text membership alone. Canonical current scope: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/SUMMARY.md`.

2026-10-26 latest update: V4 image generation is stopped. Review the V4.1 small120-text pilot and distribution before any new images or full540-text expansion. Reference proximity and ordinary language are the current priority; runtime reliability still needs a fresh unedited holdout test after the style gate.

2026-10-26 update: implement V4 lived-in specificity using the existing fixed-camera limits; generate 540 text candidates and launch a reviewed 108-image sample. Preserve V2/V3. Assess scene authenticity separately from source relevance and camera/reference fidelity. No larger image run or eval-hub upload in this task.

2026-10-23 update: V3 now addresses candidate diversity using30 ranked prompts/source/tag and a fixed source-relevance rubric. Runtime vision is deferred to an unnumbered future experiment; V3 remains tag-only. Validate text, then the user-approved108-image sample on four fixed renders before any larger eval. Preserve V2 and record its exact stopped generation state. No blue-control work.

USER-CONFIRMED, 2026-10-13: after text-level GPT-5.5 validation, Hooman will generate downstream images and review compatibility with successful reference examples. Revise prompts based on observed failures while preserving inputs, outputs, and prompt versions for comparison.

Reconsider output count with evidence. No downstream rewriter implementation, image-model changes, or deployment is planned in the current phase.

2026-10-14 update: the text phase is complete, with 14 production prompts ready for downstream image review. Keep automatic no-device clauses disabled until Hooman changes the decision after C-Tech consultation. Evaluate missing product coverage when additional SKU-specific source messaging arrives.

2026-10-22 update: Hooman selected v1 as the frozen baseline. The old BLUE candidate was removed from the live tree and remains recoverable from Git commit `9810dc07`. Build the new product v2 as a separate camera-aware revision after investigating mismatches across source environment prompts, downstream rewrites, and rendered images; retain v1 as the comparison and rollback point.

2026-10-22 camera update: evaluate the new type-and-camera V2 first using offline visual profiles. V3 can compare per-request image analysis against those profiles for added accuracy, latency, cost, and variability. V2 text acceptance must precede a bounded same-reference image comparison; use the same verified upload bytes, dimensions and seed, and preserve downstream rewritten prompts. Compare the environment writer and downstream composition separately. The historical generated_v1 set has 184 eligible rows and eight retained reference-binding failures; never use the latter as evidence against the image model. Blue coverage is handled outside this project.

V5 (2026-10-27): retain frozen V4.1 while dual-source text pilot is reviewed. Runtime promotion requires better unaided camera/score/citation reliability than the observed3/8 bank pass; no V5 image run is active or authorized. Resolve strict weighting and unsupported Modric camera coverage before expanding scope.
