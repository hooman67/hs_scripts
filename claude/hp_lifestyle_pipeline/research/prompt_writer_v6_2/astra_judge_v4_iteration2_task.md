# HP natural-placement judge V4: targeted calibration redesign

You are advising on a production image judge for HP laptop/printer lifestyle scenes. This is a product LLM integration/evaluation task. Give concrete prompt/schema/scoring changes; do not write application code.

## Runtime and output

GPT-5.5 receives (1) the generated scene image, (2) the original digital-twin render, (3) product type, and (4) the original scene prompt. It judges the scene-generation image only. Application code deterministically converts five component observations into a 0–100 score and pass/review/fail. Hidden relations are unobservable rather than wrong.

Five scored components are support scenario, access/usability, orientation/alignment, scale/perspective, and contact/integration. Wall richness, clipped art, sparse décor, and prop taste are unscored creative advisories unless they produce a physical conflict.

## Calibration result that must be improved

We ran a clean V4 candidate on 35 C-Tech-comment-derived development cases. Expected labels are 19 pass, 14 fail, 2 review. V3 matched 15/35. V4 matched only 16/35: 16 pass→pass, 13 fail→pass, 3 pass→review, 2 review→pass, and 1 fail→review. Therefore V4 is not an improvement worth shipping.

We also reran five missed fail cases with seven preserved human-labeled visual anchors. GPT-5.5 still returned pass/100 for all five, so adding generic few-shot images alone did not solve detection.

## False passes that matter

1. A wide printer scene: C-Tech says the rectangular table is visibly deformed because its two side edges are inconsistent, and it is stranded in the middle of a home room where a rectangular equipment table should normally be near a wall. GPT-5.5 said pass/100.
2. A printer close-up: C-Tech says the rectangular support is unnaturally placed in the room. GPT-5.5 said pass/100.
3. A printer right close-up: wall/table/cabinet perspective makes the table-to-wall geometry impossible; the cabinet is visibly wall-aligned while the foreground table appears to touch the same wall despite incompatible depth. GPT-5.5 said pass/100.
4. Printer medium: a necessary table support/leg is visibly missing. GPT-5.5 described hidden rear structure as plausible and said pass/100.
5. Laptop medium: a necessary table leg is visibly missing. GPT-5.5 said pass/100.
6. Printer medium: excessive gap between wall and printer/equipment station even allowing cable clearance. GPT-5.5 said pass/100.
7. Printer close-up: printer/support appears slanted and a random floor puzzle makes the station incoherent. GPT-5.5 said pass/100.
8. Printer right close-up: table placement is implausible and an unrelated puzzle lies on the floor. GPT-5.5 said pass/100.
9. Wide printer scenes: unrealistic adjacent furniture, mismatched table legs, table warping around curtains, plant intersecting/crowding the printer, and product/props isolated without a coherent station. GPT-5.5 repeatedly said pass/100.

## False reviews that should pass

1. Slightly moved chairs: the user explicitly says chairs move; mild displacement is pass/warning, not review/fail, unless the seat faces far away or there is no believable usable position.
2. A good laptop scene with sparse wall detail should pass placement; wall richness is only a creative advisory.
3. A good laptop scene with framed artwork clipped near the edge should pass placement; framing is only a creative advisory.

## Review cases missed as pass

1. A water carafe visibly crowds the laptop's immediate work area: review.
2. Disfigured reading glasses near an otherwise good printer station: review for malformed incidental prop, without failing overall placement.

## Current prompt already says these things, but GPT-5.5 overlooks them

- Trace device→support, support→room, device→person, visible support structure, and props→station.
- Inspect tabletop corners, thickness, attachments, legs/pedestal, wall/floor boundary, and neighboring furniture.
- A necessary table leg demonstrably absent is severity 3; hidden leg is unobservable.
- Rectangular printer equipment tables in a home normally belong near a wall or purposeful grouping.
- Distinguish perspective convergence from bends, contradictory thickness, impossible corner connections, or missing supports.
- Slight chair displacement is severity 0/1; wall/art/sparsity advisories do not score.

The model nevertheless writes a plausible holistic story, then assigns severity 0 to every component without actually falsifying structural defects.

## Your task

Design a targeted V4 iteration that materially improves detection without merely making the judge globally harsher.

1. Propose an explicit ordered visual inspection protocol that forces GPT-5.5 to test rigid geometry, support structure, room anchoring, device/prop collision, and user access before forming a narrative.
2. Propose additional structured observation fields that make skipped checks detectable. Prefer fields with bounded enums plus short evidence, and explain which should be required for close/medium/wide views.
3. Explain how to prevent the model from filling hidden geometry with optimistic assumptions while also avoiding false failure from crop, occlusion, cantilever, pedestal, or normal perspective convergence.
4. Provide exact system-prompt wording for the structural sweep and final adversarial verification.
5. Say whether a two-pass single-call method (independent defect inventory, then component scoring) is likely to help, and specify it.
6. Propose calibration rules for the above false passes/reviews, including which should be severity 1, 2, or 3.
7. Keep wall richness/art framing/prop taste out of placement scoring unless a physical relation is wrong.
8. Give a small ablation plan: what to test on 5–10 cases before rerunning all 35, and what measured outcome justifies the full rerun.

Return a concise but implementation-ready design. Do not claim expected accuracy; these are development cases, and held-out validation will follow only after development agreement improves.
