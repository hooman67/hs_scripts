# Task: redesign HP natural-placement judge as V4.2

You are advising the engineer implementing an image-placement judge for HP laptop and printer lifestyle generations. This is a product LLM integration/evaluation task. Analyze the exact failed V4.1 evidence and write a concrete deployable V4.2 design. You cannot access files or tools beyond the material embedded in this request.

## Runtime contract

Production supplies only:

1. generated scene image to judge;
2. original digital-twin render for identity/orientation reference;
3. product type (`laptop` or `printer`);
4. original scene prompt.

Production does **not** guarantee product name, camera tag, prompt rank, or a record ID. Optional eval metadata can only strengthen leakage exclusions; it cannot be required.

Return a structured visual assessment. Application code deterministically derives 0–100 score, pass/review/fail, reason codes, and an evidence explanation. Hidden/cropped relations are unobservable and lower confidence; they are not wrong and cannot by themselves cause review/fail. High-confidence visible material defect fails; medium/low-confidence material finding reviews; explicit severity-1 review warning reviews; advisory can pass. Never edit model outputs manually. One bounded retry is allowed only for transport or structurally/semantically invalid output.

## Ground truth scope

Natural placement includes:

- appropriate support and room use zone;
- device position, orientation, usable approach, chair relationship;
- coherent support furniture anatomy, edges, load path, perspective, scale;
- physical contact, shadows/reflections;
- coherent prop narrative when props obstruct or make placement implausible.

Unrelated malformed props are warnings, not placement failures. One physical defect gets one owner/check/code.

## Proven failure

V4 Astra without anchors returned `review` for all 15, matched 3/13 explicit verdicts, and found 0/12 expected issue codes because low coverage forced review while visual defects were missed.

Anchored V4.1 removed low-coverage review and provided four low-resolution anchors from the same 15-case development set. In the seven-case gate it matched 1/6 explicit verdicts, found 0/6 expected issue cases, returned six passes and one review, and introduced one false missing-support warning. The current prompt's evidence prose is often fluent but rationalizes visible geometry as benign. The current neighbor-anchor mechanism is ineffective and contaminating.

The request embeds:

- exact seven V4.1 result envelopes and exact human comments/expected issues;
- the exact V4.1 system prompt and assessment schema;
- the exact V4.1 deterministic scoring implementation;
- the exact V4.1 anchor catalog;
- 25 verified prior-V6 anchor candidates: 10 direct label/ambiguity comments and 15 issue-only comments;
- two contact sheets covering exactly the seven failed-gate scene/twin pairs.

## Mandatory V4.2 architecture requirements

1. **Mandatory visual inventory before judgment.** The same structured response must first record, from pixels:
   - visible support type and room location;
   - product footprint, functional front and surface position;
   - tabletop/support edge families and visible corners;
   - credible legs, panels, pedestal, brackets, wall mount, or other load path;
   - relation to wall, floor, cabinets and nearby furniture;
   - usable user/operating approach and associated chair if visible;
   - prop/activity narrative.

2. **Product-specific trigger questions.** Require explicit `yes` / `no` / `unknown` answers with pixel evidence. Phrase each as a positive condition, such as “Does the visible support have a credible load path?” A `no` must reconcile to exactly one owned issue code and one scored check. `unknown` is allowed only when pixels do not establish the relation and cannot block pass. A visible medium/wide support plus room landmarks cannot be called wholly unknown.

3. **Defect candidate reconciliation.** The model must name plausible defects from the inventory before filling the 13 legacy checks. Every retained defect must appear once in its owner check; every rejected candidate needs a concise visible reason. Prevent both “all-zero rationalization” and duplicate penalties.

4. **Image inputs.** Runtime should provide full scene, original twin, and a deterministic product/support crop. The crop should preserve device, tabletop edges/corners and visible load path; use SIFT/affine twin-to-scene localization when reliable, with a safe fallback. Explain crop provenance and what not to infer from it. Recommend exact minimum match/inlier checks, padding, and fallback behavior without pretending localization is ground truth.

5. **Printer/home rule.** In a home, a dedicated rectangular/square printer support is normally against a wall or room edge. A centrally stranded support is a placement defect unless the image shows a clear central shared-equipment/work narrative. The printer may be correctly placed on a malformed/misplaced table; judge these separately. Printers should be on equipment tables/credenzas/cabinets, not occupied personal desks.

6. **Laptop chair rule.** Distinguish an associated visible chair that is materially misaligned from a chair hidden by a close crop. Chairs move; small displacement is severity-1 advisory/review, not fail. Facing away, blocked access, or no feasible position in a sufficiently visible zone can be material.

7. **Prior-V6 visual calibration pool.** Replace the current 15-derived neighbor anchors with a small pool selected only from the supplied verified prior-V6 corpus. Direct-label anchors may show the exact comment and human label. Issue-only anchors must be clearly marked `no human verdict`; never invent one. For arbitrary runtime targets, deterministically select a bounded, product-type-balanced set using only available hashes/product type. Always exclude exact generated hash, same twin hash and exact prompt hash. If optional camera/device/rank metadata exists, also exclude same near-duplicate family. Target labels/comments never enter target text.

8. **Deterministic score/verdict.** Preserve observed material/review-warning logic. Low coverage/confidence/unobservable must not force review. Unassessable is only for unreadable image, unidentified/conflicting product, or fundamentally unjudgeable product/support.

9. **Six-case first gate only.** Before scaling, use chair warning, home printer support, missing support, printer axis+prop coherence, perspective, and a placement pass. Do not optimize by putting those targets or near duplicates into their own anchor context.

## What to return

Provide all of the following, with implementation-ready specificity:

1. A concise diagnosis tied to the exact seven outputs.
2. The complete proposed V4.2 system prompt, ready to save verbatim.
3. A strict JSON schema design for the mandatory inventory, trigger questions, defect candidates/reconciliation, and 13 checks. You may show exact JSON or an exact field-by-field schema patch, but no vague placeholders.
4. Semantic validation invariants application code must enforce, especially `no` trigger → one owner/code, issue-code provenance, unobservable behavior, and one-defect-one-owner.
5. Deterministic scoring/verdict rules.
6. SIFT/affine crop algorithm and fallback, including thresholds and crop padding.
7. A recommended small prior-V6 anchor pool, naming exact supplied record IDs, which are direct-label vs issue-only, and runtime selection/exclusion rules. Avoid target-neighbor leakage.
8. Six-case gate and explicit acceptance criteria that measure issue detection and false positives, not only verdict match.
9. Risks and what evidence would falsify the design.

Do not recommend a human post-editor, manually correcting outputs, giving target comments to the judge, or scaling to all 160 before the six-case gate. Do not claim an independent accuracy estimate from this development-selected evidence.
