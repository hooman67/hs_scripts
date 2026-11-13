## Recommendation

Use the single authorized r2 for **one procedural change: a mandatory, structured alignment-and-construction observation trace before scoring in both primary branches**.

Keep GPT-5.5/high, the five dimensions and weights, severity definitions, scoring, unrelated criteria, and the existing ensemble decision rules. Do not add a third vote, an image-specific override, or another verifier trigger.

The justification is operational: **r1 already contains the relevant rules, but its outputs do not demonstrate that the necessary comparisons were performed.** More general rubric prose is unlikely to address that failure.

I reinspected the attached images directly. **The row13 geometry label remains uncorroborated in this exact attachment.** That disagreement must remain capable of stopping calibration.

This is a design consultation, not an executed r2 calibration.

## 1. Anchor reinspection against the actual r1 text

### `07_cashmere_x_Front_Wide_1`

**What I observe**

- The keyboard/palm-rest faces the near working edge. The immediate tabletop in front of the laptop is clear; the sketchbook and painting materials are beside it.
- The laptop’s front and rear base-width boundaries and the table’s long boundaries have broadly compatible directional tendencies.
- The visible left table end and the laptop’s side edges have different apparent slopes. That alone does not establish rotation: depth-family lines at different lateral positions can fan toward a common vanishing region.
- The upholstered chair is substantially right of the laptop. Its back hides much of the seat and lower-body relationship.

**Counter-evidence and limits**

The chair offset does not establish reversed use, an obstruction, or excessive working-edge depth. Conversely, the crop does not justify certifying complete seated-body clearance.

**Comparison with r1 and C-Tech**

The r1 **non-material alignment finding is supported** and agrees with the supplied criterion feedback. Compact’s partial access assessment is better supported than baseline’s broad observed/high-confidence assurance about the chair-to-keyboard relationship.

This is not a global positive. Neither the C-Tech label nor this inspection certifies every construction, contact, or usability relationship.

---

### `07_cashmere_x_Front_Wide_4`

**What I observe**

- The laptop’s near base-width boundary and rear base-width boundary at the hinge both rise toward the right.
- The table’s near and far long boundaries instead descend toward the right.
- Importantly, this is not just a comparison of two slopes. **The two product-width boundaries and the two support-width boundaries exhibit competing convergence tendencies.** Under a squared arrangement, corresponding width boundaries would belong to the same 3D direction family; these visible pairs support different width families.
- The laptop’s base-depth boundaries are visible, but the table’s end boundaries are cropped. A full corresponding depth-family comparison is therefore unavailable.
- The operating side faces the near edge, and the immediate keyboard approach is not visibly obstructed. Chair centering is irrelevant to the width-family conflict.

**Counter-evidence and limits**

The cropped table ends limit reconstruction; no precise rotation magnitude is warranted. Different slopes alone would be insufficient, and different *width versus depth* families may legitimately have different vanishing points. The concern here is specifically the inconsistent **corresponding width families**, not a demand for one universal vanishing point.

Good contact and usable access do not negate an independently visible alignment defect.

**Comparison with r1 and C-Tech**

I find visible support for C-Tech’s **material laptop/table misalignment** diagnosis, appropriately mapped to:

`orientation_alignment → furniture_axis_conflict`

The actual r1 explanations do not address this evidence:

- Baseline says the edges are squared “within normal perspective” without identifying the paired boundaries or explaining their compatibility.
- Compact substitutes “operating side faces the user side” and “generally squared” for the required product/support comparison. Facing a usable approach is not evidence of squaring.

Both primaries returned severity 0 at medium confidence. This is a substantive false clear relative to both the supplied criterion and my inspection—not a scoring-threshold problem.

---

### `13_elitebook_13_Front_Left_Medium_4` — exact fourth/rightmost attachment

**What I observe**

- The keyboard faces the near working side. There is clear tabletop immediately before the palm-rest; swatches and measuring tape are predominantly lateral.
- The laptop and table width directions are not identical, but I do not see the pronounced competing paired-width relationship present in `07_4`. The cropped table ends limit depth-axis comparison.
- The wooden top and front face/apron read as a continuous surface across the visible span. I cannot trace a visible re-entrant tabletop corner or an impossible L-shaped join.
- Broad wooden supports are visible near the lower left and right sides. A smaller recessed member is visible below the apron, left of the foreground chair; its upper attachment is hidden.
- The foreground chair has its own rounded seat, curved back and supporting posts. These must not be counted automatically as table legs.

**Counter-evidence to the geometry allegation**

The visible members do not establish duplication, disconnection, or a structurally inexplicable extra support. Some attachment points are occluded; some members can plausibly be rear supports or belong to the chair. A continuous rectangular tabletop remains a plausible reading of the visible outline.

**Comparison with r1 and C-Tech**

- The placement/alignment non-failure is supported.
- The supplied C-Tech label alleges malformed L-shaped furniture/multiple legs.
- **I still cannot corroborate that allegation in this exact image.**

R1’s statements that the “visible legs/load path” are structurally coherent are more comprehensive than the attachment visibility supports. But **overstating a clear finding does not itself prove malformed construction**.

Thus, a **source-specific label/evidence disagreement remains**. This is not proof that the manifest points to the wrong source; it is an unresolved disagreement about the identified source. Do not convert it into either invented defect evidence or certification of hidden construction.

## 2. What failed operationally

### The missing element is observable inspection, not another rule

R1 already requires:

- width **and** depth comparisons;
- paired boundaries and convergence;
- table/chair construction inspection;
- named inconsistent members and joins;
- consideration of occlusion and alternative ownership.

Yet its schema accepts “generally squared” or “construction appears coherent” as sufficient evidence. It requires text, but not an auditable correspondence between visible features and conclusions.

### The broad scene reading can substitute for the targeted comparison

The `07_4` compact explanation demonstrates this substitution directly: correct-facing use and harmless chair offset appear inside the alignment justification. Those facts answer other questions, not whether the laptop and rectangular table are materially rotated relative to one another.

Similarly, plausible scale and a recognizable table silhouette do not establish coherent individual attachments.

These outputs show a failure to document the required inspection. They do not reveal whether the internal cause was attention allocation, feature interpretation, or premature scene-level acceptance.

### Agreement does not supply missing detection

Both GPT-5.5 branches can make correlated omissions despite differently worded prompts.

Under the described additions-only mechanism, **no compact material concern means no addition to verify**. When both primaries return zero, the downstream consensus cannot recover an unproposed concern. Changing only verifier language would leave this failure path intact.

The scoring policy already makes medium/high-confidence severity 2 decisive. Neither larger geometry weights nor lower score thresholds would repair two severity-zero observations.

## 3. The one bounded r2 change

### Mandatory evidence-first trace, inside the existing primary evaluations

Require both primaries to emit a short structured trace **before their scene-level conclusions and component judgments**, on every image—not only on disagreements or suspected defects.

Its scope is limited to:

1. Rigid product-base versus supporting-surface alignment.
2. Supporting table/counter and directly associated chair/stool construction.

It does not expand into background-furniture defect hunting, rescore décor, or alter printer placement/access rules. Existing verifiers, when triggered, apply the same evidence requirements to the dimensions they already examine.

This is one observation-contract amendment, not a new judging branch. It places the required inspection where r1 missed the concern, without increasing the number of semantic attempts.

### Why structure is justified

An emitted trace makes four omissions detectable:

- no named product/support boundary correspondence;
- “perspective” invoked without examining direction families;
- construction cleared without locating visible connections;
- a suspected member counted without considering ownership or occlusion.

It cannot guarantee correct perception. That is precisely what the single calibration must test.

## 4. Concise evaluator instruction/schema contract

The following is general runtime guidance. It contains no anchor labels, image-specific directions, coordinates, or prior judgments.

> **Focused observation before scoring**
>
> Judge Image A. Use Image B only to identify the rigid product base and operating front. Before writing scene-level conclusions, record the visible alignment boundaries and support-furniture connections.
>
> **Alignment:** Identify the rigid base’s width and depth boundaries and the corresponding support boundaries wherever visible. Compare paired boundaries and their convergence within corresponding 3D direction families. Do not use the display, raised tray, loose props, or chair pose as substitutes. Raw image-slope differences are insufficient. Explain whether perspective plausibly accounts for the relationship. If one family is hidden, identify it and state whether the remaining evidence independently establishes a material conflict or leaves the comparison unresolved.
>
> **Construction:** Trace the visible tabletop outline, thickness transitions and joins. Identify visible support members, their furniture ownership, and exposed connections toward the supported surface and floor or other support. Inspect associated seating connections separately. Distinguish actual disconnection, duplication or impossible joining from occlusion, frame termination, plausible rear supports, separate furniture and legitimate construction.
>
> Do not assume a fixed leg count, conventional legs, a universal vanishing point, or numerical angle thresholds. Circular/oval surfaces need not provide rectangular alignment axes. An L shape or multiple supports is not itself a defect.
>
> For each conclusion, record supporting evidence, the strongest plausible counter-explanation, and remaining visibility limits. Missing evidence neither proves a defect nor establishes alignment. A crop does not excuse a visible defect or guarantee a pass.
>
> Apply the existing severity and issue-code rules. Movable-chair pose alone remains non-defective; independently established blocked reach, consequential product/support rotation and completely reversed use remain material.

### Required trace fields

Use a versioned **r2 evidence envelope** containing the trace and the unchanged v3 observation payload. Do not silently alter the historical v3 schema.

| Field | Required content |
|---|---|
| `boundary_inventory` | Locally named product-base and support boundaries; owner, geometric role, visible location, and visibility limit. |
| `axis_comparisons.width` / `.depth` | Referenced boundaries; compatible, different-direction-family, indeterminate, or not applicable; projective explanation and counter-evidence. |
| `surface_construction` | Visible outline, thickness transitions and joins; any specific discontinuity, or what cannot be inspected. |
| `member_connections` | Relevant visible members; likely furniture ownership; exposed connections; occluded/out-of-frame termination; plausible alternative interpretation. |
| `focused_findings` | Separate alignment and construction conclusions: material established, no visible material defect, unresolved, or not applicable; evidence references, counter-evidence and consequence. |

These are concise observations, not a request for lengthy free-form reasoning.

### Deterministic integration

1. **Only the existing five components are scored.** The trace supplies evidence, not another score or vote.
2. A trace conclusion of established material product/support rotation must be represented in `orientation_alignment`, using the appropriate existing code and severity at least 2 with medium/high confidence.
3. Established malformed construction must similarly appear in `scale_perspective → malformed_support_furniture`. A projective contradiction uses `conflicting_perspective` when that is the actual finding.
4. The same cue cannot be established as material in the trace but disappear into severity 0/1, or be routed into an unrelated dimension.
5. An unresolved subrelationship does not automatically make the whole component unobservable. Assess the visible evidence, explicitly retain the missing relationship, and apply the existing visibility/confidence policy.
6. Unrelated findings within either component remain possible under the unchanged rubric. The trace must not suppress them.
7. A missing trace or internally inconsistent trace/component pair is an invalid evaluation—not an instruction to promote a score, repair text, or sample again.
8. After validation, use the **unchanged ensemble trigger, confirmation, fallback, scoring and verdict rules**. The trace is not an override.

This deliberately leaves a falsifiable possibility: both primaries may still miss the concern. If so, calibration fails rather than silently adding a new recovery mechanism.

## 5. Stability-control inspection

These are useful regression controls, **not independent human gold**.

| Control | Directly visible evidence | Principal false-positive risk |
|---|---|---|
| `01_cashmere_x_Front_CloseUp_2` | The laptop base is visible on a continuous wooden top. The near edge and visible rear boundary are broadly compatible with its width direction. Cup and notebook are lateral. The foreground chair back and crop hide lower construction; table-end depth boundaries are not available for a complete comparison. | Inferring missing legs, wrong scale from product prominence, or unsupported construction from the tight crop. The crop must not become an exemption from any visible defect either. |
| `17_tassel_Front_CloseUp_1` | The printer rests on a continuous wooden surface with a visible front apron and a left support meeting it. That support continues beyond the bottom frame; most remaining support construction is not shown. The notebook is beside the operating area. | Demanding additional visible legs, certifying hidden attachments, or using the lid rather than rigid-body boundaries for alignment. No associated chair is required for printer operation. |
| `31_adf_printer_Front_Wide_1` | A long wall-side wooden top has a dark front rail and a visible dark vertical support at the left. The chair obscures part of the lower/right area; the shelving’s wooden upright is a separate furniture member. The printer’s rigid width boundaries are broadly compatible with the support’s long boundaries. | Requiring a conventional four-legged table, counting shelving or chair members as extra counter supports, or inventing hidden wall fixings. A fitted/support-frame interpretation is plausible, but its hidden attachment method is not established. |

I do not see an established material alignment or construction defect in these controls. That does not justify certifying unseen construction or freezing every r1 visibility/confidence value.

For the wide printer, the chair is to the right of the printer’s operating front; it should not become an automatic blocking or occupied-workstation penalty. The raised black product element must not substitute for a rigid-base edge.

## 6. One calibration and the stopping rule

Before running, freeze the single r2 prompt/contract, model configuration, ensemble roles, and validation rules. Use the six already-selected cases and original assets. Each scheduled role runs once within the fixed evaluation procedure; no alternative prompt attempts, best-of selection, or semantic resampling.

Keep expectations outside model inputs. Runtime receives no C-Tech labels, control roles, r1 outputs, or this consultation’s image descriptions.

### Evaluate each criterion, not just each overall verdict

The frozen manifest has ten explicitly labeled alignment/construction checks; the two unlabeled geometry cells must remain unlabeled.

Acceptance requires:

- The first Cashmere anchor remains non-material on alignment, without chair pose reappearing as another placement penalty.
- The second Cashmere anchor produces the material **product/table alignment** finding—not merely some unrelated overall failure, a severity-1 refinement, or review.
- Row13 remains non-material on placement/alignment. Its required geometry finding must be supported by an identifiable visible construction defect, not merely match the expected code.
- Each control satisfies its alignment and construction stability expectations without invented supports, crop-based exemptions, or unrelated penalty leakage.
- Evidence contracts and ordinary scoring/ensemble validation pass.

Partial visibility is legitimate. It is neither an automatic calibration failure nor a way to count an unassessed relationship as demonstrated success. An unresolved required positive is not a recovered detection.

### Stop and block the broad run if any criterion fails

In particular, stop if:

- `07_4` remains falsely clear;
- harmless chair pose again causes a penalty;
- row13 still lacks defensible geometry evidence;
- a control acquires a material concern that violates the frozen stability gate;
- the target labels appear only through unsupported evidence or incorrect dimension mapping;
- an evaluation is invalid or the evidence contract is not followed.

A newly reported control defect could conceivably be real rather than a false positive. Preserve it for adjudication; do not erase it to obtain stability. It still prevents this calibration from authorizing expansion.

**Row13 uncertainty must not be waived.** If its label cannot be substantiated, the honest outcome is a blocked calibration plus an unresolved source/label adjudication request—not fabricated legs, another sample, or a revised acceptance condition.

All r1 artifacts remain immutable. Preserve r2 outputs and disagreements separately. Only after every criterion passes may the authorized scope expand to the **original historical 128 images**—not PR4523/PR4417’s 120-image study or old30. Preserve their historical image-stage provenance.

Even a clean six-case result would establish only that this bounded revision passed these development checks. **A successful consultation—and even successful calibration—is not proof that the judge is correct or generally reliable.**