# Task: improve HP natural-placement judge from exact reviewer feedback

You are the senior research architect for an image-quality judge. Analyze the supplied human feedback and frozen model evidence, then specify a deployable V4 natural-placement judge. The orchestrating agent will independently review your answer before implementing anything. You cannot access the filesystem, tools, or prior chat. Everything you may rely on is included in this request. Three labeled contact sheets follow the evidence JSON. Each labeled row shows the generated scene on the left and its original digital-twin render on the right; all 15 records appear exactly once in JSON order.

## Decision and output needed

Design a judge that takes exactly: (1) generated scene image, (2) original digital-twin render, (3) product type laptop/printer, and (4) original scene prompt. It scores the scene-generation image only. It must return a 0–100 natural-placement score, auditable component evidence, confidence/coverage, and pass/review/fail. Tight crops make some relations unobservable; absence of evidence must not be treated as failure.

Your answer must contain:

1. An evidence-grounded diagnosis of recurring V3 mistakes, explicitly mapping all 15 comments. Do not infer that unreviewed rows passed.
2. A revised judge architecture that can operate unattended. Prefer the simplest method supported by evidence; justify any multi-pass or deterministic merge.
3. The complete proposed V4 system prompt, ready to use verbatim.
4. A complete JSON output schema or a precise amendment to the supplied V3 schema. Keep fields machine-validatable.
5. Deterministic scoring and verdict rules, including how warnings/review differ from failures.
6. Application validation and bounded retry behavior. Persistent failures must return an explicit error, never a silently repaired human-edited answer.
7. A calibration/evaluation plan that avoids claiming accuracy from these 15 development examples. Identify holdout needs and pass criteria.
8. Risks, remaining ambiguities, and at least one credible alternative design.

Use plain, concrete language. Do not merely restate the reviewer comments. Reconcile them into general rules. Do not invent numerical accuracy.

## Stable user contract and natural-placement rules

- Judge whether the product and supporting furniture form a usable, believable scene.
- Printers ordinarily sit on practical tables, credenzas, or dedicated/shared supports, not on occupied personal desks, café tables, coffee tables, or room-center display pedestals unless source context explicitly requires an unusual scenario.
- A printer normally belongs toward the rear or side of a practical support, with paper/output/control access clear and plausible cable/ventilation clearance. It should not be awkwardly foregrounded or stranded in the middle of a large table.
- Laptops should face and reach the actual usable seat or standing position. Nothing should block the keyboard-to-user path. A distant visitor chair or chair for another table is not proof of a laptop user position.
- Chairs move. A slightly displaced or modestly angled chair is ordinarily a warning/review signal, not a fail. A chair clearly facing away, unreachable, or associated with another surface can be material. In a close crop, a missing chair can simply be outside frame.
- Product, support, and nearby furniture should follow coherent 3D room axes. Do not require identical 2D pixel slopes under perspective. Relevant edges should read parallel in the common 3D frame when that relation is observable.
- Product scale, perspective, contact/cast shadow, reflection, support, and physical weight must be plausible.
- The support furniture itself must make sense in the room. A rectangular or square table stranded in a room center, far from a wall and without a coherent use zone, can be unnatural; a round table is more plausible as a free-standing central table. This is contextual, not an absolute furniture-design law.
- Inspect support furniture anatomy and perspective: required legs/supports cannot be missing, nonparallel table geometry can indicate deformation, and table/wall/cabinet relationships must share a coherent perspective. Support-furniture anatomy and perspective are in scope because they determine placement plausibility.
- Distinguish placement from general image artifacts. A malformed support leg or support perspective is placement-relevant. Disfigured eyeglasses or an unrelated prop artifact is normally a general image-quality warning outside placement, unless it blocks use or destroys the scene's spatial narrative.
- Random or incoherent props under/around support furniture can make the placement narrative fail, especially if they create obstacles or contradict the scenario. Do not fail merely because a scene contains ordinary props.
- Judge the actual pixels, not the desired prompt. Use the prompt only to understand intended scenario. The digital twin establishes product identity/orientation; do not penalize differences caused by environment styling.
- When a relation is hidden, mark it unobservable and lower confidence. Do not hallucinate walls, chairs, or access paths.

## Current V3 architecture

V3 is a research candidate, not an automatic gate. Each image receives two GPT-5.5/high assessments:

- Frozen V2 with seven fixed visual anchors.
- Compact V3 without examples, inspecting room → support → device → user relations.

Five components are weighted: support/scenario 20, access/usability 30, orientation/alignment 20, scale/perspective 15, contact/integration 15. Severity 0–4 maps to component scores 100,75,50,25,0. Unobservable components are excluded. Material severity ≥2 caps the total and prevents pass. Current thresholds are provisional.

For a new material defect raised only by compact V3, V3 invokes two more checks: a proposal-aware verifier and a names-only independent component check. It accepts the addition only when both independently support a material issue and share an issue code. This reduced one false failure but is expensive and still inherits V2 errors.

The model output distinguishes visibility observed/partial/unobservable, severity 0–4 or null, confidence low/medium/high, evidence, consequence, and component-specific issue codes. It also emits scene-reading fields: functional front, support surface, usable approach edge, actual user position, access path, device/support axes, neighboring furniture, narrative status/evidence, support placement in room, usable-space distribution, alternative user positions, prop relationships, and lived-in evidence.

## Verified experiment history and limitations

- Frozen V2 matched 5/11 retrospective development verdict expectations and 3/15 issue expectations.
- A compact V3 single pass matched 4/11 verdict and 4/15 issue checks.
- A two-pass merge matched 6/11 verdict and 6/15 issue checks, but introduced one false failure in a broader 64-case development set by treating a visitor/background chair as the only possible laptop user position.
- Proposal-aware verification and a separate names-only check were added. The selected consensus matched 6/11 verdict and 5/15 issue checks; it retained 55/56 prior comment agreements, turning one visitor-chair case into review rather than pass. These are repeatedly tuned development checks, not unbiased accuracy estimates.
- The current 160-image V6.1 set produced 118 pass, 38 fail, 4 review. These are model predictions, not human labels. Fifteen newly published comments are the evidence for this task.
- Known failure modes before these comments: models rationalized a printer cabinet stranded in a room; confused visitor chairs with user seating; missed laptops centered away from a user; sometimes over-penalized minor chair displacement; and missed furniture geometry. Cropped-image experiments did not establish an improvement.
- Raw stage outputs must remain immutable and distinguishable from deterministic application-derived fields. No manual correction is allowed in deployment.

## Component vocabulary in V3

The five current components and representative issue codes are:

- support_scenario: unsupported_surface, inappropriate_printer_surface, occupied_workstation, implausible_scenario, incoherent_use_arrangement, misplaced_support_furniture, unpopulated_storage, bare_staged_setting
- access_usability: excessive_reach, precarious_edge, blocked_operating_side, no_user_position, furniture_collision, blocked_paper_or_lid_path, blocked_user_workspace
- orientation_alignment: corner_facing, furniture_axis_conflict, chair_alignment_conflict, furniture_layout_conflict, ancillary_axis_conflict
- scale_perspective: implausible_scale, conflicting_perspective, malformed_support_furniture
- contact_integration: floating, sinking_or_intersection, inconsistent_shadow, inconsistent_reflection

You may reorganize these components or add tightly scoped codes if the feedback supports it. Avoid one-off codes that merely memorize a single image.

## Evidence interpretation rules

- The annotation is a comment-only submission: exactly 15 rows and zero configured questions. Comments are authoritative user feedback. There are no button values to interpret.
- Every embedded assessment is the exact frozen current evidence for that row. It may be wrong. Analyze discrepancies rather than treating model text as ground truth.
- Image pairs are generated scene followed by original twin. Use the twin only for product identity/orientation comparison; judge placement in the generated scene.
- Explicitly separate material placement defects, review-level placement warnings, and out-of-scope general rendering artifacts.
- If an image cannot establish a relation, preserve uncertainty rather than forcing pass or fail.

## Exact comments and compact joined evidence

The following compact JSON is appended verbatim by the runner. It contains all 15 exact comments, IDs, products, cameras, environments, original prompts, image hashes, current final verdicts and summaries, plus the exact V2 and compact-V3 evidence for components implicated by each comment. The full frozen evidence remains preserved outside this request; the compact transport omits unrelated component prose to stay within a bounded request size.
