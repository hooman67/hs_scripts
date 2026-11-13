# Reusable articulated SKU rig

As of: 2026-09-22

## Contents

- [Decision question](#decision-question)
- [Working concept](#working-concept)
- [Separation of responsibilities](#separation-of-responsibilities)
- [Required input package](#required-input-package)
- [First proof-of-concept gate](#first-proof-of-concept-gate)
- [Open questions](#open-questions)

## Decision question

Can a reusable CAD-derived Blender rig let a product expert visually author mechanically correct
motion more easily than describing motion in text or curating a fixed clip for every variant?

## Working concept

Build each known product once as a reusable articulated digital product. The editable artifact is
a Blender scene containing component geometry, joints, constraints, controls, grasp points, and an
animation timeline. A rendered MP4 is a flattened downstream condition for Seedance; it is not the
editable representation.

Hooman is the first user, so direct Blender use is acceptable for the proof of concept.
Customer-facing abstraction is deferred. The live V2 bank contains six product families, not the
five initially assumed; the miter-saw family is the first candidate.

## Separation of responsibilities

- CAD and manufacturer specifications define geometry and allowable mechanics.
- A product-knowledgeable human confirms component boundaries, axes, limits, sequencing, and
  whether the authored movement matches real product operation.
- Astra writes Blender import/cleanup/rigging code, creates validators and visual controls, and
  iterates from rendered feedback.
- Hooman visually authors motion with controls and keyframes.
- Blender renders an approved preview and, later, the Seedance conditioning MP4.
- Seedance is invoked only after explicit approval and a quoted cost.

Astra is an implementation agent, not the authority on product mechanics.

## Required input package

For the selected SKU, acquire and preserve:

1. Exact manufacturer, product family, SKU/model number, and authoritative product page.
2. CAD source, format, revision, units, coordinate convention, license, and component hierarchy.
3. Owner/service manual and exploded-parts diagram.
4. Manufacturer-defined movement limits and safety interlocks.
5. Existing motion-bank clips and metadata for that SKU.
6. Supplemental operation videos for movements missing from the bank, with provenance.
7. Component/joint table: parent, child, joint type, local axis, pivot, limits, and coupled behavior.
8. Hand-grasp table: grasp target, active hand, allowed orientation, and attach/release events.
9. Initial target motions and explicit mechanical pass/fail criteria.
10. Render specification for a clear, appearance-minimized conditioning video.

## First proof-of-concept gate

Prefer the best-covered sliding compound miter saw if authoritative CAD is available. Otherwise
choose the catalog SKU with the best combination of usable CAD, manufacturer specifications, and
operation-video coverage. If none qualifies, use a non-THD mechanical product with both CAD and
public operation videos.

Before any Seedance call, the proof of concept should demonstrate that Hooman can visually create
multiple distinct, mechanically valid motions from one reusable rig without editing Python.

## Candidate selected for input collection

The `ryobi_miter_saw` family leads the current bank with 18 motion labels over 17 unique source
clips. The jigsaw ties it at 17 unique clips, but the miter saw better exercises coupled articulated
motion: head pivot, rail slide, blade spin, retracting guard, turntable/lock, battery insertion, and
hands.

The incumbent image is a strong visual match to the RYOBI PBT01B 18V ONE+ 7-1/4 in. Sliding
Compound Miter Saw. This identification is not proven because the bank has no exact SKU provenance
field. The first source package is preserved at
`/home/colligo/hs_scripts/claude/3d_research/research/articulated-sku-rig/inputs/pbt01b`.

No exact PBT01B CAD was found in the bounded search. Two downloadable CC-licensed Sketchfab meshes
were identified, but the generic model is mechanically crude and the Makita LS1018 appears to be a
surface scan rather than componentized CAD. Anonymous download requires authentication. Details
and preserved previews are at
`/home/colligo/hs_scripts/claude/3d_research/research/articulated-sku-rig/cad-candidates`.

## Execution environment

Blender 5.2.2 LTS is installed at
`/mnt/localssd/blender-poc/blender-5.2.2-linux-x64/blender`. Headless startup, the proposal's Python
scene builder, geometry validation, still rendering, and H.264 encoding were verified. This host is
CPU-only and has no live visual desktop. The fastest visual-authoring path is to open the eventual
`.blend` on Hooman's local Blender 5.2.x installation and use this host for repeatable validation
and rendering. Full evidence is in `/mnt/localssd/blender-poc/VERIFICATION.md`.

GPT-6 Astra access is available through the current Codex environment and was exercised by the
parallel Astra task. No user API key is needed for this path. Astra accepts text and images but not
native video, so operation video should be represented as timestamped frames/contact sheets plus
motion notes. Direct API-key use remains untested and is unnecessary for the proof of concept.

## Open questions

- Is its CAD componentized or delivered as one fused body?
- Does the CAD license permit internal derived animation assets?
- Should guard motion be user-controlled, mechanically driven, or both?
- What is the minimum hand representation that communicates grip and re-grasp without requiring a
  full character rig?
