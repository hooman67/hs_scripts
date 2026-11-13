# PBT01B proof-of-concept input package

As of: 2026-09-22

## Selection status

`CANDIDATE — EXACT BANK IDENTITY UNVERIFIED`

The live bank's `ryobi_miter_saw` family has the largest number of motion labels: 18 labels over
17 unique source clips. The incumbent reference image is a strong visual match to the RYOBI
PBT01B, but the bank has no SKU provenance field. Treat PBT01B as the leading candidate, not as a
proven identity.

Manufacturer identity:

- Product: RYOBI 18V ONE+ 7-1/4 in. Sliding Compound Miter Saw
- Model: PBT01B
- OMSID: 315111309
- UPC: 033287189502
- Official page: https://www.ryobitools.com/products/33287189502

## Available inputs

- `source-images/incumbent-reference.png` — current THD evaluation reference.
- `source-images/official-pbt01b-view-01.jpg` — official isolated product view.
- `source-images/official-pbt01b-view-02.jpg` — official labeled feature view.
- `source-images/official-pbt01b-view-03.jpg` — official operation photo.
- `MOTION_INDEX.md` — all 18 family-level motion labels and their source locations.
- `manifest.yaml` — provenance, hashes, known facts, and explicit gaps.

## Blocking inputs

- No exact, authoritative, componentized PBT01B CAD file has been found.
- No direct PBT01B operator/service manual or exploded-parts diagram has been acquired yet.
- The motion media resides in `s3://colligo-dev-artifacts`; the standard temporary-credential
  workflow and Foundry gateway were unavailable for that bucket in this session. Metadata and
  paths remain available in the live bank.
- A product expert still needs to confirm the joint table, pivots, limits, interlocks, and whether
  the incumbent image is in fact PBT01B.

Do not give this package to Astra as if the missing facts were known. A plausible-looking rig with
invented pivots would not test the intended CAD-derived workflow.
