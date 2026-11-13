## 1. Redesign: evidence first, severity second

The failure is not primarily insufficient instructions; it is **premature holistic acceptance followed by unsupported severity zeros**. Replace narrative-first judging with an ordered, auditable inspection.

Use two stages within one call:

1. **Structural evidence inventory:** localized observations, contradictions, visibility limits, and alternative explanations. No component severities or overall assessment.
2. **Component assignment:** map those observations to the five components, apply severity rules, then perform a final contradiction audit.

This may reduce premature commitment, but the stages are **not genuinely independent** in a single model call. Test the benefit rather than assuming it.

The model should return observations and component severities—not a score or verdict.

---

## 2. Ordered inspection protocol

| Order | Required inspection | Evidence to record |
|---|---|---|
| 1. Establish visibility | Identify product, load-bearing support, visible room boundaries, neighboring furniture, and usable side of the station. | View class; cropped/occluded regions; visible structural landmarks. |
| 2. Test rigid geometry | Trace visible tabletop edges and corners; compare thickness; inspect joints. Compare table, wall, floor, and cabinet geometry. | Which two edges/connections agree or contradict; why ordinary convergence does or does not explain them. |
| 3. Test support structure | Follow tabletop → attachment → leg/pedestal/cantilever → floor or wall. Inspect conspicuously empty support regions. | Visible load paths; exposed attachment points; whether the allegedly missing region is actually visible. |
| 4. Test room anchoring | Examine support-to-wall/floor relationships, stand-off, grouping, circulation, and apparent wall contact. | Visible contextual cues supporting a coherent station or a placement-policy violation. |
| 5. Test contact and collisions | Inspect device base, tabletop contact, plants, curtains, adjacent furniture, and incidental props. | Interpenetration versus overlap/occlusion; crowding versus mere proximity; malformed incidental geometry. |
| 6. Test access | Identify a believable operating position, work area, keyboard/input access, printer access, and chair usability. | Actual obstruction or displacement required—not assumptions about ideal furniture styling. |
| 7. Assign severities and challenge acceptance | Map evidence to components; recheck missing supports, contradictory depth, intersections, and access. | Finding-to-component references; unresolved contradictions; audit result. |

Do not require numerical vanishing-point estimation or metric distances from a single image. Require **specific relational evidence** instead.

---

## 3. Structured output additions

### Required top-level fields

| Field | Bounded values / contents |
|---|---|
| `view_class` | `close / medium / wide` |
| `context_visibility` | `adequate / partial / minimal` |
| `checks` | Fixed required checklist below |
| `findings` | Localized defect/warning records |
| `components` | Exactly the five scored components |
| `advisories` | Unscored creative observations |
| `verification` | Final consistency audit |

### Each check record

- `check_id`: fixed enum.
- `visibility`: `adequate / partial / none`.
- `result`: `consistent / contradiction / ambiguous / unobservable / not_applicable`.
- `evidence`: short description naming visible objects, edges, junctions, or regions.
- `limitation`: `none / crop / occlusion / resolution / insufficient_context`.
- `finding_ids`: references, possibly empty.

Required check IDs:

`rigid_edges_corners`, `thickness_joints`, `support_load_paths`, `room_depth_relations`, `station_anchoring`, `device_support_contact`, `prop_interactions`, `incidental_prop_geometry`, `user_access`.

For structural contradictions, additionally require:

- `alternative`: `perspective / crop_occlusion / pedestal / cantilever / other_visible_support / none`.
- `alternative_status`: `supported / possible_but_unverified / contradicted / not_applicable`.
- Short evidence explaining that status.

For missing-support findings, additionally require:

- `missing_region_visibility`: `exposed / partly_occluded / outside_frame`.
- `support_requirement_basis`: `visible_attachment / visible_design_continuity / visibly_unsupported_load / expectation_only`.

`expectation_only` cannot establish a severe missing-support defect.

### Finding and component records

Each finding includes:

- ID, defect type, image region, short evidence.
- `basis`: `physical_geometry / usability / station_policy / incidental_geometry`.
- One primary component assignment.

Each component includes:

- `severity`: `0 / 1 / 2 / 3 / null`.
- `coverage`: `adequate / partial / unobservable`.
- Supporting check/finding IDs.
- Short rationale.

Use `null` only when the component has no assessable evidence. Do not represent invisibility as a verified zero.

### Requirements by framing

**All checklist records are required in every view.** Framing changes observability, not whether the check exists.

- **Close:** assess visible tabletop/contact/prop/access relations; permit support and room checks to be unobservable with a specific crop explanation.
- **Medium:** inspect visible support structure and nearby room boundaries; explicitly identify which load-path segments are hidden.
- **Wide:** require localized room-anchoring, circulation, furniture, and support observations where image resolution permits.

A missing record is a **schema/inspection failure**, not a physical defect. Do not silently convert incomplete output into pass/100.

---

## 4. Exact system-prompt wording

### Structural sweep

> Judge only the generated scene image. Use the digital-twin render to identify the product and its visible product features, not to supply missing room or support geometry. Use the scene prompt to understand intended use, not as evidence that the generated scene satisfies it.
>
> Before writing any overall assessment or component severity, complete the structural evidence inventory in this order:
>
> 1. Identify visible structural landmarks and explicit visibility limits.
> 2. Trace visible tabletop edges, corners, thickness, and joints. Compare neighboring wall, floor, table, and cabinet relationships. Test whether ordinary perspective convergence explains the image; convergence alone is not deformation.
> 3. Follow visible load paths from the tabletop through attachments and supports to the floor or wall. Inspect any visibly empty region alleged to require a support.
> 4. Inspect the station’s visible relationship to the room, including wall stand-off, purposeful grouping, and usable circulation.
> 5. Inspect device-to-support contact, plant/curtain/furniture interactions, prop crowding, and malformed incidental geometry.
> 6. Inspect a believable user operating position and immediate work/access area.
>
> For every check, report a localized observation or a specific visibility limitation. “Looks natural,” “plausible,” and “probably supported behind” are not sufficient evidence.
>
> Do not invent hidden legs, brackets, rear frames, or wall attachments to repair a visible contradiction. Conversely, do not infer a missing leg merely because a conventional table might have four legs. Crop, occlusion, a visible pedestal, or a credible visible cantilever can explain absence.
>
> A severe missing-support finding requires visible evidence of a required but absent support or a visibly unsupported load. A region outside the image or behind an occluder is unobservable, not defective. If evidence is genuinely ambiguous, preserve that ambiguity instead of certifying either correctness or failure.
>
> Finish the evidence inventory before assigning component severities. Keep evidence concise and observable; do not produce a holistic scene narrative.

### Final adversarial verification

> Before finalizing, audit the evidence and component assignments:
>
> - Recheck every recorded structural contradiction. None may disappear from scoring without a specific evidence-based resolution.
> - For every severity 0, identify the checks that support it. Do not use hidden geometry as positive evidence.
> - Revisit any claimed missing support: is its required location visibly exposed, and what establishes that a support is required?
> - Revisit any claimed deformation: could normal perspective, crop, occlusion, or the visible support design explain it?
> - Revisit room placement: distinguish physical impossibility from the explicit home-equipment-station policy.
> - Confirm that mild chair movement, sparse walls, clipped artwork, and prop taste have not escalated placement severity.
> - Confirm that visible work-area crowding and clearly malformed incidental props have not been dismissed merely because the main product looks acceptable.
>
> Report any corrected assignment in the verification record. Do not invent a defect to satisfy this audit. Return the required structured observations and five component severities only; do not return a total score or verdict.

---

## 5. Calibration and routing rules

Define severity consistently:

- **0:** no observed placement problem.
- **1:** minor physical imperfection or mild adjustment; still usable and credible.
- **2:** localized, material concern requiring review.
- **3:** clearly impossible, substantially unusable, or an explicit severe station-policy violation.

| Case | Calibration rule |
|---|---|
| Deformed rectangular tabletop | **3** for clear incompatible corners, bent rigid edges, or impossible connections. **2** for a localized visible deformation with limited extent. Normal convergence: **0**. Route to orientation/alignment. |
| Impossible table/wall/cabinet depth | **3** when visible contacts and relative depth cannot coexist. Mere differing edge directions are insufficient. Route to scale/perspective. |
| Missing printer/laptop table support | **3** when demonstrably required and visibly absent. Hidden/cropped support: unobservable. Genuine visible structural concern without conclusive absence: **2**, not automatic failure. |
| Stranded printer table / excessive wall gap | Apply the narrow station policy below. Slight nonideal positioning: **1**; material but ambiguous incoherence: **2**; clearly established policy violation: **3**. Route to support scenario. |
| Slanted printer/support | Perspective or camera roll: **0**. Visible misalignment needing attention: **2**. Clearly unstable or impossible support/product relationship: **3**. |
| Random floor puzzle | Taste alone: advisory, **0**. Actual access encroachment: **2**; substantial unusability/trip obstruction: **3**, based on visible layout—not the object category. |
| Mismatched legs / adjacent furniture | Stylistic mismatch: **0**. Malformed geometry: **2**; broken load path or impossible construction: **3**. |
| Table warping around curtains | **3** for clear rigid deformation/interpenetration; ordinary curtain overlap is not a defect. |
| Plant near printer | Nearby decoration: **0**. Material operating-area crowding: **2**. Clear interpenetration or substantial access blockage: **3**. |
| Slightly moved chair | **0**, or **1** for mild repositioning. **2** only for a material access concern; **3** only when no believable usable position exists. |
| Sparse wall / clipped artwork | Advisory only, **0**, unless a separate physical conflict exists. |
| Carafe crowding laptop work area | **2**, access/usability. Proximity without actual crowding is not enough. |
| Clearly disfigured reading glasses | **2**, contact/integration, subtype `incidental_geometry`; capped at review for malformation alone. Do not generalize this exception into prop-taste scoring. |

### Make the anchoring policy explicit

“Near a wall” is not a law of physics. If C-Tech wants stranded home printer stations to fail, encode that as a **client placement policy**, not invented geometric impossibility:

> A conventional rectangular home printer equipment table should form a coherent equipment station: wall-associated, furniture-grouped, or visibly purposeful as a freestanding station. A clearly nonfunctional stand-off combined with visibly incoherent station placement is a severe station-policy violation. Distance alone, lack of décor, or absence of context is insufficient. Purposeful islands and usable freestanding groupings are acceptable.

Require at least two localized contextual cues for severity 3. A close-up that cannot establish room placement must not inherit a fail from the comment alone. Such cases need label/evidence adjudication if agreement remains impossible.

---

## 6. Deterministic scoring changes

Use **maximum finding severity within each component**, not a count of suspicious details. Assign each finding to one primary component unless there are independently evidenced consequences.

Required status gates:

- Any component **3** → **fail**.
- Otherwise any component **2** → **review**.
- Otherwise → **pass**, with warnings for severity 1.
- Unobservable checks produce no penalty and remain visible in coverage reporting.

If the existing numeric converter does not enforce these gates, a simple replacement is:

- Component penalties: **0 → 0, 1 → 2, 2 → 10, 3 → 20**.
- Raw score: `100 − sum(component penalties)`.
- Review score capped at **79**.
- Fail score capped at **49**.

This yields pass scores 90–100, review scores 50–79, and fail scores 0–49. These are policy scores, not probabilities.

A score of 100 means **no observed scored defect**, not complete verification of hidden structure. Display coverage separately. Keep numeric scoring fixed during detection ablations so improved perception is not confused with harsher arithmetic.

---

## 7. Small ablation before all 35

Use ten preserved development images:

- **Five fails:** warped tabletop; impossible wall/table depth; missing support; excessive stand-off/stranded station; wide-scene collision or malformed furniture.
- **Three passes:** moved chair; sparse wall; clipped artwork.
- **Two reviews:** carafe crowding; malformed glasses.

Where possible, choose a pass image with legitimately cropped or occluded supports to test overreach.

Compare:

1. **Baseline:** current V4.
2. **Evidence-only change:** ordered checks and visibility schema, otherwise existing severity rules.
3. **Staged change:** add inventory-before-scoring and adversarial verification.
4. **Full iteration:** add the explicit calibration/routing rules and station policy.

Keep images, reference render, prompt, and runtime settings identical. Run each condition twice; do not add generic anchors during this ablation.

Measure separately:

- Human-confirmed defect detection.
- Correct component/severity after detection.
- False escalation on clean/creative-control cases.
- Unsupported hidden-structure explanations.
- Missing checks and evidence-free zero assignments.
- Repeat stability.

**Predeclare the full-rerun gate:** in both full-iteration runs, at least **4/5 fails**, all **3 passes**, and both **reviews** correctly classified; missing-support and impossible-depth defects specifically detected; no fabricated structural evidence or omitted required checks.

If a comment’s defect cannot be localized by human inspection, adjudicate that case rather than tuning the prompt to reproduce its label. Passing this gate justifies rerunning all 35—not shipping or claiming expected accuracy. Held-out validation follows only after development agreement improves.
