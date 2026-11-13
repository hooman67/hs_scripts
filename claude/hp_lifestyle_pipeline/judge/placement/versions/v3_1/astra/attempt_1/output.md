## Recommendation: a narrow V3.1 semantic amendment

Keep V3’s architecture and scoring. Change only:

1. **Laptop/chair relation:** ordinary chair angle or lateral offset is not an alignment defect.
2. **Laptop/table alignment:** consequential misalignment remains material; slight edge-direction differences are not automatic failures.
3. **Table/chair construction:** make the existing geometry assessment explicit and systematic, using `scale_perspective`, not a new dimension.

Apply these changes to **both primary rubrics and both verifier rubrics**. Updating compact V3 alone would leave the V2-derived baseline’s chair-alignment veto intact.

## 1. Per-anchor evidence assessment

These are observations from the attached images, separate from the supplied C-Tech labels. They are not production JSON judgments or hand-corrected scores.

### `07_cashmere_x_Front_Wide_1` — V15.6

**Visible evidence**
- The keyboard/palm-rest side faces the near working edge.
- The laptop sits relatively near that edge, with no obvious intervening object.
- Its base-width direction is broadly compatible with the table’s long boundaries.
- The foreground chair is displaced rightward relative to the laptop, nearer the notebook’s position.

**Counter-evidence and uncertainty**
- Chair displacement alone does not establish wrong-facing placement or excessive reach. Much of the seat/body-position relationship is hidden by the chair back and crop.
- Different apparent slopes of depth edges at different image locations are not, by themselves, proof of rotation.
- The visible tabletop, apron and exposed supports do not establish a malformed-furniture defect. Hidden legs cannot be counted as missing.

**Assessment relative to C-Tech**
I agree that this should **not fail because the chair is not aligned or centered with the laptop**. The visible offset also does not independently establish a material reach failure. This is not a global pass: contact, scale, construction and other relationships remain separately assessable.

### `07_cashmere_x_Front_Wide_4` — V16.6 no geometry

**Visible evidence**
- The laptop’s front and rear base-width directions rise toward the right, while the table’s near and far long boundaries descend toward the right.
- Taken as paired boundaries—not merely one screen slope—these show strongly competing width-direction/convergence tendencies.
- The foreground chair faces the working side and is more nearly centered on the laptop than in `_1`.

**Counter-evidence and uncertainty**
- The table ends are cropped, limiting a complete depth-axis reconstruction.
- The laptop appears supported, and the immediate keyboard approach is not visibly blocked. Those facts do not cancel a material alignment defect.
- No additional malformed-furniture claim is needed to explain the placement concern.

**Assessment relative to C-Tech**
I agree with the **material laptop/table misalignment** diagnosis. Its appropriate location is `orientation_alignment` with `furniture_axis_conflict`, not a chair code. Better chair alignment does not rescue it. Under the unchanged scoring rule, a medium/high-confidence material finding produces failure.

### `13_elitebook_13_Front_Left_Medium_4` — V16.6 no geometry

I assessed the supplied `_4.jpg`: the manifest identifies it as the fourth direct-child figure, column index 3, caption/variant **“V16.6 no geometry”** ([exact supplied image URL](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/img/13_elitebook_13_Front_Left_Medium_4.jpg)).

**Visible evidence**
- The keyboard faces the near working side, with clear space immediately before it.
- The laptop’s front edge and table’s long boundary have somewhat different directions, but this is not the pronounced contrast seen in `07_4`.
- The image shows a broad wooden top and front apron, exposed supports near the sides, and partially visible members farther underneath. The foreground chair has its own seat and back-support members.

**Counter-evidence to the geometry label**
- I cannot confidently identify an impossible L-shaped join in this attachment. The visible tabletop can be read as a continuous rectangular surface whose ends are partly outside the crop.
- The visible vertical members do not establish duplicated, disconnected or genuinely extra table legs: some can be ordinary rear supports, and others belong to the foreground chair.
- Several attachment points and lower supports are occluded. That limits diagnosis rather than proving malformed construction.

**Assessment relative to C-Tech**
I agree that slight product/edge misalignment should **not establish a placement failure** here. However, I **cannot corroborate the claimed L-shaped-table/multiple-legs failure from the attached image**.

Preserve that disagreement explicitly. The C-Tech geometry-fail label is authoritative supplied feedback, but it must not become invented visual evidence. If substantiated, its intended mapping is `scale_perspective → malformed_support_furniture`; I would not manufacture that finding or convert the unresolved relationship into a certified geometry pass.

## 2. Concise replacement rubric passages

Use these semantics consistently in all four V3.1 rubric editions.

### A. Laptop/chair relation

> A laptop need not share the chair’s axis or be centered on the chair. Ordinary chair rotation and lateral offset are not placement defects by themselves. Establish the genuinely associated seat and the laptop’s keyboard/palm-rest side; assess visible reach, body space and obstructions separately. A clearly reversed working side—facing completely away from an established user position—is material. Do not infer excessive reach merely from image-plane chair offset, invent another seat, or move the visible chair in the explanation. Preserve uncertainty when seat association or reach is hidden.

This supersedes the old blanket examples treating “laptop away from its chair” as automatically material. Genuine excessive reach and obstruction remain defects.

### B. Device/table alignment

> For laptops on rectangular supports, inspect the rigid base’s width and depth directions against corresponding support directions wherever visible. A clear, consequential rotation that materially breaks the natural squared relationship is a defect, even without collision or blocked use. Slight edge-direction differences or small ordinary rotations are not automatic failures. Distinguish compatible perspective convergence from actual rotation; do not judge from a single raw screen slope, the display, or a raised panel. Different parallel direction families can have different vanishing points. Where evidence is incomplete, state which relation remains uncertain. Circular and oval supports need not provide straight alignment edges.

Keep printer-specific squaring, location and approach rules unchanged. These laptop anchors do not justify relaxing printer placement.

### C. Table/chair geometry

> Inspect the supporting table and directly associated chair/stool for plausible visible construction: tabletop outline and thickness, joins, leg/support attachment, seat/back/leg connections, and coherent occlusion and perspective. Flag clearly duplicated, disconnected or structurally inexplicable supports, impossible joins, or materially inconsistent construction. Multiple legs, an L-shaped design, or unusual furniture are not defects by themselves. Do not demand occluded or out-of-frame supports, prescribe a fixed leg count, or penalize circular/oval tops for lacking straight edges. Different direction families need not share one vanishing point. Report construction defects under scale_perspective; do not recast them as alignment defects.

“Stronger scrutiny” means a more explicit inspection requirement—not stronger confidence, higher severity, or failure by suspicion.

## 3. Dimension and issue-code mapping

| Existing dimension | Weight | V3.1 mapping and boundary |
|---|---:|---|
| `support_scenario` | 20% | Preserve existing criteria. Use `unsupported_base` only for visibly inadequate chassis support. Do not relabel chair offset or malformed furniture as `incoherent_use_arrangement` without an independent activity contradiction. |
| `access_usability` | 30% | Use `excessive_reach` for established excessive reach; `blocked_operating_side`, `blocked_user_workspace`, or `furniture_collision` for their actual visible conditions. Ordinary chair angle/offset is insufficient. A cropped chair is not `no_user_position`. |
| `orientation_alignment` | 20% | Material laptop/table rotation: `furniture_axis_conflict`. Use `corner_facing` only when actual corner-facing placement is established. A completely reversed working side relative to an established seat: `furniture_layout_conflict`. Preserve unrelated existing alignment criteria. |
| `scale_perspective` | 15% | Table **and associated chair/stool construction**: `malformed_support_furniture`. Inconsistent projective geometry: `conflicting_perspective`. Implausible size: `implausible_scale`. Clarify that “support furniture” includes associated seating for this code’s construction meaning. |
| `contact_integration` | 15% | Preserve product/support contact and lighting criteria. A disconnected chair leg belongs under malformed construction, not automatically `floating`. |

Use the most specific code supported by the evidence. A single malformed join should not also become alignment, support-scenario and contact penalties unless separate visible consequences independently justify those findings.

### Retiring `chair_alignment_conflict`

**Yes—from newly emitted V3.1 codes.**

- Keep it in the schema/code registry for historical compatibility.
- Explicitly prohibit its new emission in all four V3.1 rubrics.
- Do not automatically translate it into another failure code.
- Reassess the relationship: ordinary chair misalignment produces no defect; genuinely reversed use maps to `furniture_layout_conflict`; independently demonstrated reach or obstruction maps to access codes.

Deleting the code alone is insufficient: the old veto could otherwise reappear as `excessive_reach`, `furniture_layout_conflict`, or `incoherent_use_arrangement`.

## 4. Minimal update across the V3 ensemble

Create versioned **V3.1-derived rubric editions or an explicit overriding amendment**; retain frozen V2/V3 artifacts as historical sources.

| Rubric | Required explicit change |
|---|---|
| **V2-exemplar primary** | Replace conflicting chair/access language, categorical diagonal-mismatch language, and corresponding severity examples. Add the table/chair construction passage and authorize existing V3 code `malformed_support_furniture` in its code guidance. |
| **Compact V3 primary** | Apply the same laptop tolerances; expand the existing brief construction instruction; retire new chair-code emission. |
| **Proposal-aware verifier** | Apply identical semantics; require evidence for and against the proposed alignment or geometry concern. Proposals remain fallible. Assess only supplied components. |
| **Names-only verifier** | Apply identical semantics independently; remove chair-axis equivalence and explicitly include table/chair construction. Continue receiving component names, not proposals or anchor labels. |

The baseline’s existing visual exemplars can remain, but **the V3.1 amendment must explicitly take precedence over conflicting legacy chair-alignment interpretations**. This is a general rule correction, not an image-specific exemption or edited verdict.

Do not reuse an unpatched baseline judgment and expect additions-only verification to repair it.

### Preserve the existing decision rule

- Retain the frozen **new compact material concern trigger**. Do not expand verification to every image or every disagreement.
- Confirm additions only when both checks are observed/partial, medium/high confidence, severity at least 2, and share an issue code.
- Retain minimum severity/confidence, partial visibility if either is partial, shared codes only, and evidence quoting both checks.
- Preserve rejected-addition fallback to baseline, disagreement recording and high-confidence cap to medium.
- Preserve unconfirmed-addition handling: retain baseline; defer otherwise-passing baseline/merged outcomes to review; preserve an existing fail.
- Preserve nontrigger merging, baseline tie-breaking and fallback behavior, including its low-confidence fallback.

No hand edits, code-stripping repairs, per-anchor exceptions, or new override mechanism are needed.

## 5. Contract preservation and limitations

Preserve the current schema shape and `placement-observations-v3` schema identifier. Record V3.1 rubric/ensemble provenance separately. Existing evidence fields can describe geometry and counter-evidence; no new fields are necessary.

Keep unchanged:

- all five weights;
- severity meanings and medium/high-confidence severity-2 veto;
- score calculation, caps, pass/fail thresholds and coverage rules;
- core-pass components;
- product-match review precedence;
- visibility, uncertainty and evidence requirements;
- preservation of the digital twin in suggested corrections.

Geometry already participates in the material-defect veto despite its 15% weight. It does **not** need a larger weight or new core-pass status to produce failure.

These three anchors support a narrow semantic correction and expose one unresolved label/evidence disagreement. They do not establish runtime reliability, calibrated thresholds, accuracy, printer performance, or generalization. They cover only two laptop rows, with a repeated product reference, and are explicitly **end-to-end development images outside V3’s scene-generation input domain**. Keep that boundary and the existing provisional-calibration status; do not relabel these assets as scene-generation inputs or present this consultation as held-out validation.