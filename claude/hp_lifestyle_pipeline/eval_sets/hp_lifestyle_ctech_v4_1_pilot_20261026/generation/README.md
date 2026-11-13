# V4.1 corrected-render image pilot

Authorized by Hooman on 2026-10-27: generate all120 reviewed V4.1 pilot prompts, one image each, using the corrected laptop/printer white-gallery inputs. The frozen text review is preserved. The separate image manifest supersedes its historical no-image gate.

## Frozen inputs and settings

- Prompt file: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/pilot_prompts.json`, SHA-256 `1e99134ab8e1c1bab1f91eb74dc6d35b22b44c5a33d11b66566d84869957e57a`.
- Image manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/image_generation_manifest.json`, SHA-256 `52a7cb4538510dcd6bf76e1189a022f79dfea36fa163c4275c6f3f2ff08b3a64`.
- Corrected assets/provenance: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/corrected_twin_assets_20261027/selected_renders.json`.
- Exactly four tags: laptop_FrontRightCloseUp, laptop_FrontRightWide, printer_FrontRightCloseUp, printer_FrontRightWide;30 prompts per tag. No miniPC.
- Each new catalogue has one matching image per tag; no product-name inference is needed. Prior Koki/Magic labels are historical context, not verified names in the corrected catalogue.
- Original white-gallery PNGs are2368×1776 RGB. Requests preserve4:3 and use2368×1776, without cropping, rescaling or re-encoding reference bytes. Previous V4 images used16:9; comparisons must account for this changed input.
- Endpoint: `https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev/v1/image/generate`; upload `/v2/storage/image`.
- `x-foundry-model-id=hp-image`, seed42, n1, prompt rewrite enabled, `gemini-3.1-pro`,50 steps. GET metadata/OpenAPI contract checked before launch; metadata identifies `image5_foundry`. No independent weight hash is exposed.

## Run and resume

Run directory:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027`

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/launch_generation.sh status
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/launch_generation.sh validate
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/launch_generation.sh resume
```

Initial four-view integration check uses `smoke`; after root checks its outputs, `start` processes remaining rows and reuses completed records. No additional user approval is required: all120 are authorized. The launcher refuses a duplicate active runner. Generation tmux: `hp_ctech_v4_1_generation_20261027`; smoke tmux: `hp_ctech_v4_1_smoke_20261027`.

The supervisor runs bounded resumable invocations and saves state under the run directory's `launch`. Known jobs are polled on resume; completed bytes are checked. Ambiguous submissions are held rather than blindly repeated. In particular, HTTP5xx does not prove a POST created no job. Missing/mismatched returned `debugData.rawPrompt` is a terminal integrity failure, not a completed result. The raw response is retained for investigation.

`blob_bindings.json` ties each returned blob ID to the exact uploaded PNG SHA-256, bytes, dimensions, device and camera tag. The gallery copies those same original bytes. Rows retain the exact prompt, source data, candidate identity, request payload, returned seed/dimensions, rewritten prompt and debugData.

## Progressive gallery

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generated_v4_1/gallery/index.html

The120-row gallery includes prompt, corrected digital twin, collapsible source/explanation, generated output, rewritten prompt and complete debug/request. Pending and failed rows are explicit. The separate publisher updates every120seconds and stops when120 rows are terminal. Canonical publisher state:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generation_publication/publication.json`

All first uploads and changed files are checked with S3 HEAD and GET SHA-256. First publication required an empty isolated prefix; later updates only modify owned files. IMS code is unchanged. Local browser tests mock IMS only inside the test browser.

AWS refresh uses the approved helper with the Pluto-specific reachable broker:

```bash
PLUTO_TOKEN="$PLUTO_AUTH_TOKEN" uv run --script /home/colligo/.claude/scripts/foundry_aws_creds.py --endpoint https://foundry-aws-pluto.adobe.io/iam/credentials/aws
```

The default corporate broker is unreachable from this dev box. Credentials stay outside tracked files. Publisher refreshes the standard env file as needed.

## Interpretation

The prompts include the disclosed text-pilot correction pass and8 editorial scene edits. This run evaluates those reviewed texts, not one-call writer reliability. Passing identity/format checks does not establish camera preservation or image quality. V2/V3/V4 runs remain stopped; their assets and published results are unchanged.
