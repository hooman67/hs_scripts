# KDP Lifestyle Hero Image POC Research

## Goal

Validate whether an existing third-party image model, initially GPT Image 2.5, can generate
on-brand lifestyle hero images of Keurig brewers from product/SKU reference imagery for a
Foundry 4.0 proof of concept.

The research supports two decisions:

1. Which scraped SKU/reference assets are strong enough for an engineering POC.
2. Whether generated lifestyle images can pass a blinded comparison against genuine lifestyle imagery.

## Scope

- Inventory and quality-check the scrape under
  `s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/`.
- Evaluate the two ticket SKUs separately:
  - K-Duo Gen 2, Moonlight Gray (`5000396548`)
  - K-Supreme Gen 2, Black (`5000393168`)
- Select additional SKU candidates by strength of reference-to-lifestyle evidence.
- Build a visual candidate gallery showing every reviewed input and comparison image.
- Generate a bounded POC image set, then design a balanced blind real-vs-generated C-Tech evaluation.

## Explicit exclusions

- No claim that scraped public imagery is approved production training or marketing material.
- No use of watermarked, overlaid-text, composited-ad, competitor, or ambiguous-product imagery as a
  clean generation reference.
- No external publication or outreach. Foundry-internal model calls and S3 gallery uploads are authorized for
  this POC.

## Evidence rules

- Folder names and supplied pair labels are discovery evidence, not ground truth.
- Product identity, variant/color, image role, watermark/text, composition, and quality are visually checked.
- Material claims use `VERIFIED`, `ASSUMED`, `UNVERIFIED`, or `USER-CONFIRMED` labels and an as-of date.
- Full S3 URIs or absolute local paths accompany evidence.

## Authorization and privacy

- S3 inspection and local downloading are authorized by Hooman for this research.
- Credentials remain outside the project and must never be copied into tracked files or reports.
- Foundry-internal model calls and S3 gallery uploads are authorized for the active POC phase.
- Reviewable HTML artifacts are uploaded to Foundry S3 with IMS authentication; they are not handed off only as
  local files.
- Local file paths shown to Hooman must be complete absolute paths rendered as plain text, not only as links.

## File map

- `PROJECT_STATE.md` — exact checkpoint, blockers, and next action.
- `DECISIONS.md` — confirmed decisions and unresolved proposals.
- `LEARNINGS.md` — durable cross-topic findings.
- `LONG_TERM_PLANS.md` — later POC and evaluation phases.
- `research-plan.md` — method, evidence schema, and stopping rules.
- `research/dataset/SUMMARY.md` — canonical dataset assessment and SKU recommendations.
- `research/dataset/data/` — downloaded or normalized metadata required for audit.
- `research/dataset/artifacts/` — candidate review gallery and related artifacts.

## Success criteria

The discovery phase is complete when the scrape is reconciled, the two ticket SKUs are assessed,
at least two strong POC candidates have visually verified reference and real-lifestyle evidence,
known limitations are explicit, and a human-readable candidate gallery is available.
