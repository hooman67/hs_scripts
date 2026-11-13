# V5 dual top-five image generation

This workflow generates the two frozen 40-row selections:

- `smart_brief`: five prompts per each of eight V5 banks, ranked by Smart Brief support.
- `ctech`: five non-overlapping prompts per bank, ranked by C-Tech similarity.

The union contains 80 distinct candidate keys. Each row uses the corrected laptop or printer render selected by its camera tag. miniPC is excluded.

## Frozen request contract

- Endpoint: `https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev/v1/image/generate`
- Header: `x-foundry-model-id: hp-image`
- Size: `2368 × 1776`
- Seed: `42`
- Images per row: `1`
- Prompt rewrite: enabled
- Rewriter: `gemini-3.1-pro`
- Inference steps: `50`

The workflow reuses the four exact blob IDs created by the corrected V4.1 run. It verifies the binding document, source manifest, PNG hashes, dimensions, device type, camera tag, and blob ID before launch. It never uploads substitute reference bytes.

## Durable and scratch locations

Tracked workflow:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/generation_top5_dual`

Resumable generation records and images:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_dual_source_v5_pilot_20261027_top5_dual`

S3 publication prefix:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/generated_top5_dual_v1/`

Public gallery after publication:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/generated_top5_dual_v1/gallery/index.html

## Validation and read-only endpoint preflight

Run from:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027`

```bash
uv run --script generation_top5_dual/run_generation.py --validate-only
uv run --script generation_top5_dual/run_generation.py --preflight-only
```

`--validate-only` performs no endpoint request. `--preflight-only` reads OpenAPI and model metadata but does not upload a reference or submit generation.

## Tests

Run from:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/generation_top5_dual`

```bash
uv run --with httpx --with pillow python -m unittest test_run_generation.py test_gallery.py -v
```

The tests verify the 40+40 inventory, cross-file uniqueness, fixed request payload, exact blob IDs, drift rejection, selection filtering, progressive gallery completeness, score metadata, and final-gallery gate.

## Bounded smoke

List all immutable row IDs:

```bash
uv run --script generation_top5_dual/run_generation.py --list-row-ids
```

Submit only explicitly reviewed rows by repeating `--row-id`:

```bash
uv run --script generation_top5_dual/run_generation.py \
  --workers 4 \
  --row-id '<row-id-1>' \
  --row-id '<row-id-2>'
```

Every submission is journaled before and after the endpoint call. Ambiguous timeouts and 5xx responses are held without blind resubmission. Confirmed connection failures and 429 responses without a job identity have a bounded safe retry budget.

## Full authorized run

After the smoke is reviewed, launch or resume all 80 rows:

```bash
uv run --script generation_top5_dual/run_generation.py --all --workers 4
```

The same command is resumable. Existing job and record identity, payload, provenance, and output bytes must match before reuse.

To refresh the progressive gallery while the runner works:

```bash
python generation_top5_dual/supervise_generation.py --workers 4
```

The supervisor runs the resumable `--all` command and rebuilds the gallery every 30 seconds. It does not publish to S3.

To publish only when the completion counts change, and automatically enforce the final 80-row gate:

```bash
source /home/colligo/.claude/hshariati/aws_creds.env && \
  uv run --script generation_top5_dual/supervise_publication.py --interval-seconds 120
```

The publication supervisor writes local state and a log beside the script. It publishes a progressive gallery while work remains, then changes to final mode only after all 80 rows are validated as done with no failures.

Either selection can also be run independently:

```bash
uv run --script generation_top5_dual/run_generation.py --selection smart_brief --workers 4
uv run --script generation_top5_dual/run_generation.py --selection ctech --workers 4
```

## Gallery build and validation

Progressive mode always shows all 80 rows and marks absent records as pending:

```bash
python generation_top5_dual/build_gallery.py
python generation_top5_dual/validate_gallery.py
```

Final mode requires 80 validated `done` records and fails on pending/error rows:

```bash
python generation_top5_dual/build_gallery.py --final
python generation_top5_dual/validate_gallery.py --final
```

The gallery supports separate selection filtering and includes selection identity, prompt, three headline scores and component scores, corrected reference image, source explanations, output, rewritten prompt, and full sanitized request/debug provenance. Smart Brief and source messaging are stored once per bank in `data.js` and shown in collapsible cells.

## Publish

AWS access must come from the permanent-token credential broker. Run the credential fetch and publication with the environment sourced in the same shell:

```bash
uv run --script /home/colligo/.claude/scripts/foundry_aws_creds.py
source /home/colligo/.claude/hshariati/aws_creds.env && \
  uv run --script generation_top5_dual/publish_gallery.py
```

Publish the final gate only after all 80 rows finish:

```bash
source /home/colligo/.claude/hshariati/aws_creds.env && \
  uv run --script generation_top5_dual/publish_gallery.py --final
```

The publisher uploads dependencies first and `gallery/index.html` last, attaches SHA-256 metadata, verifies every uploaded object with `HeadObject`, and writes the publication record to:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/generation_top5_dual/publication.json`

Presigned output URLs and authorization material are removed from durable records by the runner and rejected by the gallery validator.
