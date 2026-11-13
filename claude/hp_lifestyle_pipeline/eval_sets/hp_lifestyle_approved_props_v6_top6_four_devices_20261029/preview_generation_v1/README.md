# V6 preview-generation gallery

This directory contains the frozen 96-row V6 preview runner and its progressive/final review gallery. The gallery covers 16 banks (four product-specific views for each of Cashmere, EliteBook, Magic, and Tassel). It presents all 10 authored candidates in every bank: ranks 1–6 retain their generated outputs, while ranks 7–10 are explicitly labeled as prompt-only candidates that were never sent to the endpoint.

The gallery builder is read-only with respect to the endpoint and S3. It does not submit generations, upload references, poll jobs, or publish files. It reads the durable local run, verifies every artifact it displays, and writes only gallery assets and downloadable snapshots under the authorized run directory.

## Inputs and integrity

The builder loads the exact frozen prompt export and manifest used by `run_generation.py`. For each bank, it loads both `smart_brief` and `source_messaging` from:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44/inputs`

All 16 corrected digital-twin PNGs are checked against the manifest byte count, SHA-256, format, and 2368×1776 dimensions before exact copies are placed in the gallery run. Each completed output displayed by the gallery is checked against its durable record byte count, SHA-256, PNG format, dimensions, request payload, prompt provenance, and reference binding. Final mode also requires the generated-image directory to match the 96 validated `done` records exactly.

Credential-bearing fields and presigned URL query parameters are rejected before `data.js`, result downloads, or build metadata are written.

## Build and validate

Run from:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/preview_generation_v1`

Progressive mode shows all 160 authored candidates, organized into 16 separate device + Smart Brief/source pair + camera banks. It marks unfinished rows among the 96 authorized generations as pending and keeps the 64 unsubmitted candidates distinct as prompt-only:

```bash
uv run --with httpx --with pillow python build_gallery.py
uv run --with httpx --with pillow python validate_gallery.py
```

Final mode requires 96 validated `done` records, 64 prompt-only candidates, no pending rows, no failures, and an exact generated-image inventory:

```bash
uv run --with httpx --with pillow python build_gallery.py --final
uv run --with httpx --with pillow python validate_gallery.py --final
```

The local gallery is written to:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_approved_props_v6_top6_four_devices_20261029_preview/gallery/index.html`

The gallery shows one bank at a time through device, source-pair, camera, and bank selectors. Each selected bank shows its 10 candidates together in rank order, with prompt and score metadata, zoomable corrected digital twin and generated output, collapsible Smart Brief/source messaging, collapsible explanation/provenance, collapsed rewritten prompt, and collapsed full debug/request data.

Its download links include the generation manifest, frozen 96-prompt generation export, the complete 160-candidate export, current sanitized results JSONL, the 16 r44 Smart Brief/source-messaging inputs, and the final recovery manifest. The recovery manifest records the one byte-preserved expired-result replacement and confirms its request payload was unchanged.

## Tests

```bash
uv run --with boto3 --with httpx --with pillow python -m unittest \
  test_run_generation.py test_gallery.py test_publish_gallery.py -v
```

The gallery tests rebuild and validate the live progressive view, enforce the 160-candidate/16-bank/96-generation/16-reference contract, require ranks 1–10 in each bank, re-hash every r44 source input, check score and explanation metadata, exercise credential rejection, and enforce the final-gallery gate. Publisher tests use a fake S3 client: they verify local build drift rejection, byte/SHA metadata verification, MIME and cache-control behavior, and that `gallery/index.html` is uploaded last without making a network call.

## Publish

`publish_gallery.py` always rebuilds and validates the requested progressive or final gallery before creating an S3 client. It is pinned to the manifest destination:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/`

It re-hashes the complete build inventory, uploads `gallery/index.html` last, and verifies each remote object's byte count, SHA-256 metadata, content type, and cache control with `HeadObject`. It writes the credential-free local publication record to:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/preview_generation_v1/publication.json`

When publication is authorized, fetch temporary credentials with the permanent-token broker and source them in the same shell as the publisher:

```bash
uv run --script /home/colligo/.claude/scripts/foundry_aws_creds.py
source /home/colligo/.claude/hshariati/aws_creds.env && \
  uv run --script publish_gallery.py
```

Progressive mode publishes the currently validated completed outputs while retaining all 160 candidates in the gallery. Final mode requires all 96 generated outputs, all 64 prompt-only candidates, and the exact final image inventory:

```bash
source /home/colligo/.claude/hshariati/aws_creds.env && \
  uv run --script publish_gallery.py --final
```
