# Product evaluation consultation: V3-derived placement judge V3.1

You are consulting on an HP lifestyle-image product evaluation rubric, not doing
general coding. Review the supplied frozen V3 judge contract and the three actual
images. Recommend the smallest rubric/semantic delta, with a precise mapping to
the existing five dimensions and issue codes. Do not write application code.
V4/V4.x are separate experimental branches and are NOT the requested baseline.

## Authoritative C-Tech feedback supplied by the user

1. Row 07_cashmere_x_Front_Wide: “The chair does not need to align with
the laptop, the laptop should only align with the table.”
Image 07_cashmere_x_Front_Wide_4 MUST fail for consequential laptop/table
misalignment. Image 07_cashmere_x_Front_Wide_1 should NOT fail for
placement/chair alignment; that is NOT a global pass for unrelated dimensions.
2. Row 13_elitebook_13_Front_Left_Medium, rightmost image: would NOT fail for
product placement, but WOULD fail for a hallucinated weird L-shaped table and
multiple legs. Slight product/edge misalignment alone is not blanket failure.
The exact fourth-figure caption and URL are in the source manifest below.
3. Be looser on laptop/chair alignment unless the product faces completely the
wrong direction. Much stronger scrutiny of TABLE and CHAIR geometry: plausible
visible supports/legs, attachment, duplicated/disconnected/extra legs, tabletop
form/thickness, impossible L joins, plausible occlusion and projective geometry.
Do not demand occluded/out-of-frame legs or fail circular/oval tables for lacking
straight edges. Different parallel direction families can have distinct vanishing
points. Do not double-count geometry as alignment or invent angle thresholds.

## Requested review

- Inspect the three attached images yourself; identify visible evidence and
  counter-evidence. Distinguish your observations from the C-Tech labels.
  Preserve disagreements rather than rationalizing labels or inventing geometry.
- Propose concise replacement rubric passages for laptop/chair relation,
  device/table alignment and table/chair geometry. Preserve other V3 criteria.
- Preserve the current schema shape, dimensions, score weights, severity thresholds
  and evidence/uncertainty policy wherever possible. Is retiring
  chair_alignment_conflict from newly emitted codes appropriate? Explain.
- V3 is a V2-exemplar baseline + compact V3 + two independent checks only for
  new compact material concerns. The old baseline cannot remain an uncorrectable
  chair-alignment veto. Recommend a minimal explicit update across both primary
  rubrics and both verifier rubrics, retaining the V3 consensus decision rule.
- Say what is and is not supported by this three-anchor development calibration.
  No broad evaluation, image generation, per-image exceptions, hand-corrected
  judgments, numerical angle cutoffs or claimed accuracy estimates.

Return substantive concise design guidance, a per-anchor evidence assessment,
dimension/code mapping, and limitations. Actual production application code will
be implemented separately by Copilot.
