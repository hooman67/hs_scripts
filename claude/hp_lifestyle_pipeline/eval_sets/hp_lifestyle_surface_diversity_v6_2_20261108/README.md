# V6.2 surface-diversity generation and report runner

## Current checkpoint — 2026-11-09

The 160-prompt text set is complete and published. On 2026-11-09 Hooman explicitly approved the isolated shape-aware fix, overriding the earlier identical-pipeline requirement for that documented change. The isolated endpoint passed eight smoke cases, and the remaining 152 images are running with four workers. Existing successful jobs are retained. The actual deployment and run identities are frozen separately from the text-only preflight.

Live images: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/generated_surface_shape_r1_env2/report/viewer.html?ldap=hshariati

Live distribution: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/generated_surface_shape_r1_env2/report/distribution/index.html

The run directory is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/runs/generated_surface_shape_r1_env2`. Its `summary.json` is the live completion count. The persistent publisher verifies new or changed public images/report files by streaming S3 GET SHA-256, retaining prior verified hashes only when the current remote ETag and size also match. Initial HEAD-only checks were size checks, not content verification. Final validation requires full remote hash verification of all allowlisted public artifacts. Source files, all 16 twins, prompts and debug evidence remain available beside the images.

Runtime sessions: `hp-v62-shape-endpoint`, `hp-v62-surface-shape-env2-full`, and `hp-v62-surface-shape-env2-publisher`. Do not start duplicate workers. Exact resume launcher: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/launch_surface_shape_candidate.sh`; it pins localhost port 8137, deployment identity, prompt hash and the existing run. Earlier env1 initialization failures and the recovered env2 debug-schema mismatch are retained in the canonical project checkpoint.

Current exact artifacts:

- Frozen export directory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/exports/v6.2-surfaces-20261109-r5-final`.
- All160 JSON SHA-256: `e661123648d8b64bf37b462e482a8015fc8e9219cf3798781271719b99929500`.
- Source calls: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r4`.
- Corrected validation snapshot: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r5-recognition`.
- Text-review preflight/run directory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/runs/text_review_20261109`.
- S3 prefix: `s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/`.

R4 service outcomes were11 successful banks and5 errors. Frozen corrected validation accepts each last actual normalized response without editing model-authored fields. The strict exporter preserves original errors and request/response hashes; it does not cherry-pick previous attempts. All160 texts and aggregate counts were independently audited. Current writer/export/report suites pass297 tests. Candidate pipeline tests pass157 separately. No first-call reliability or image-quality claim is made.

Published review:

- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/source/prompts_all_160.json
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/source/prompts_all_160.txt
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/report/distribution/index.html
- https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/report/viewer.html?ldap=hshariati

Choose “Skip (comment only)” if the canonical FE viewer presents its initial setup. This is expected viewer behavior; its vendored implementation is unchanged. S3 verification covers81 objects, including all16 twins. The browser smoke covers distribution, all160 combined rows and a10-row group using those same files and local copies of verified assets, not gateway login.

Rebuild the current text report without model or image calls:

```bash
TASK_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
uv run "$TASK_ROOT/build_grouped_report.py" \
  --prompts "$TASK_ROOT/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json" \
  --prompts-sha256 e661123648d8b64bf37b462e482a8015fc8e9219cf3798781271719b99929500 \
  --run-dir "$TASK_ROOT/runs/text_review_20261109" \
  --prefix eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109 \
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r5-recognition/runtime/v6_2/approved_catalog.json \
  --title 'HP V6.2 Surface Diversity — 160 prompts; images pending pipeline decision'
```

For any approved image run, create a separate immutable run directory/manifest with its actual endpoint lineage. Do not relabel this text-only old-endpoint preflight as a shape-aware run. The source prompts can remain identical.

## Reusable tooling

This directory contains isolated runner and report code. It makes no calls by itself. The following general commands explain reproduction; replace placeholders with the recorded artifacts above and honor the current image gate.

If a completed frozen export contains stale app-derived `primary_support` metadata, `rederive_support_metadata.py` can create a separate immutable derived export without changing prompt text, IDs/order, evidence, props, scores, selection decisions, source records, or recorded raw-result hashes. Both the original export and the explicitly selected `surfaces.py` are SHA-256 pinned before the module is imported. The tool stores exact old/new metadata for all 160 rows, retains replaced bank debug under `original_debug`, labels the replacement audit as derived, and refuses an existing output directory.

```bash
EVAL_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
INPUT=/absolute/path/to/original/frozen/prompts_all_160.json
INPUT_SHA256=<sha256-of-original-export>
SURFACES=/absolute/path/to/explicit/surfaces.py
SURFACES_SHA256=<sha256-of-explicit-surfaces.py>
DERIVED=/absolute/new/path/derived-support-metadata
python "$EVAL_ROOT/rederive_support_metadata.py" \
  --input "$INPUT" --input-sha256 "$INPUT_SHA256" \
  --surfaces "$SURFACES" --surfaces-sha256 "$SURFACES_SHA256" \
  --output-dir "$DERIVED" --include-top6
```

The output contains `prompts_all_160.json`, `prompts_all_160.txt`, `support_metadata_changes.json`, and `manifest.json`; `--include-top6` also writes the compatible `prompts_top6_96.json` and `.txt` subset. The generation/report runner should use the SHA-256 of the derived `prompts_all_160.json` after this derivation is reviewed.

For a source revision whose final recorded responses need complete deterministic revalidation, use `export_revalidated_banks.py` instead of the metadata-only utility. It accepts exactly one source revision and one frozen validation snapshot. For every registered bank it uses only the final actual attempt's `normalized_output`; it never searches earlier attempts or revisions. It verifies both snapshot manifests, byte-identical source inputs, the terminal run record, source runtime assets, and every raw request/response journal. It then imports only `VALIDATION_SNAPSHOT/runtime/v6_2`, requires all 16 banks to pass, runs that frozen finalizer, and proves that text, evidence, props, explanations, C-Tech scores, and every other model field remained unchanged.

Do not run this command until the source revision is terminal and the corrected validation snapshot path is explicitly supplied:

```bash
EVAL_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
SOURCE_REVISION=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r4
VALIDATION_SNAPSHOT=/absolute/path/to/frozen/corrected-validation-snapshot
OUTPUT_DIR=/absolute/new/path/to/strict-revalidated-export
python "$EVAL_ROOT/export_revalidated_banks.py" \
  --source-revision "$SOURCE_REVISION" \
  --validation-snapshot "$VALIDATION_SNAPSHOT" \
  --output-dir "$OUTPUT_DIR"
```

The strict exporter writes all-160 and top-96 JSON/TXT files plus `validation.json`. Each bank audit includes the complete frozen source input and case metadata, source terminal status/error, original and rederived debug, every recorded attempt's validation errors and provider accounting, hashes for every raw request/response journal, and explicit final-attempt-only selection provenance. An original service rejection remains labeled as such even when the frozen corrected validator accepts its final recorded normalized output.

The runner preserves the validated V6.2 endpoint contract: four devices, four fixed views per device, ten prompts per bank, Latin-square interleave, and `POST /api/generate` with only `digitalTwinId`, `cameraId`, and `prompt`. It refuses any live catalog whose generator or rewriter differs from the prior V6.2 run. Its immutable `run_manifest.json` includes a canonical `run_sha256`; resumes must match it exactly.

The run directory contains atomic job, status, output-record, image, twin, and summary checkpoints plus an append-only `journals/events.jsonl`. A saved job is polled again after restart; a valid completed image is skipped. The S3 publisher first requests bucket-scoped credentials through `foundry_aws_gateway.maybe_s3_env_vars(bucket)`, then reads the private `~/.claude/hshariati/aws_creds.env` fallback, then uses ambient boto3 credentials. An explicitly authorized alternative can be passed with `--fallback-creds /mnt/localssd/temp_creds.txt`. Publication is allowlisted: it includes every generated image, all 16 fixed twins, frozen source inputs, catalog, job/status/output records, and every report artifact. It excludes journals, tmux logs, hidden files, and credential/key/token files.

The frozen prompt document must carry the deterministic finalizer's `primary_support` metadata on every row. The report uses that metadata directly; it never guesses a production row's support family or shape from prose. The canonical FE rows expose surface family, shape, and exact support evidence as filter fields while preserving pending generation and pending judgment status.

After the parent supplies the frozen source, set these shell variables:

```bash
EVAL_ROOT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
PROMPTS=/absolute/path/to/frozen/prompts_all_160.json
PROMPTS_SHA256=<64-lowercase-hex-digest>
RUN_DIR="$EVAL_ROOT/runs/surface-diversity-v6.2-20261108"
PREFIX=eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108
```

Run a no-generation preflight first. This reads `/api/catalog`, freezes the exact catalog, verifies all device/camera mappings and old generator/rewriter identities, copies and hashes all twins, and writes the immutable run identity:

```bash
uv run --python 3.12 \
  --with 'foundry-aws-gateway>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  "$EVAL_ROOT/run_generation.py" \
  --prompts "$PROMPTS" --prompts-sha256 "$PROMPTS_SHA256" \
  --run-dir "$RUN_DIR" --prefix "$PREFIX" --preflight-only --no-publish
```

Launch the resumable paid run only after that preflight is reviewed:

```bash
"$EVAL_ROOT/launch_tmux.sh" hp-surface-v62 \
  --prompts "$PROMPTS" --prompts-sha256 "$PROMPTS_SHA256" \
  --run-dir "$RUN_DIR" --prefix "$PREFIX" --workers 4 \
  --poll-seconds 2400 --no-publish
```

Build the native canonical FE report at any point. Missing generations and missing new judgments are labeled pending. `--judgments` is optional and accepts only a document whose `source_prompts_sha256` exactly matches the frozen input, preventing old judgments from being copied into this report.

```bash
uv run "$EVAL_ROOT/build_grouped_report.py" \
  --prompts "$PROMPTS" --prompts-sha256 "$PROMPTS_SHA256" \
  --run-dir "$RUN_DIR" --prefix "$PREFIX" \
  --catalog /absolute/path/to/frozen/approved_catalog.json \
  --title 'HP Lifestyle V6.2 — Surface Diversity (160 prompts, GPT Image 2.5)'
```

This also builds `report/distribution/index.html`, a self-contained text-distribution page. It reports environment, product, view, prompt length, declared scores, C-Tech and source-document coverage, primary-support family/shape, round-Café, bank compliance, approved catalog/prop/group frequencies, per-bank prop-group compliance, lexical duplicates/closest pairs, and recurring phrases with declared source quotes. Each prompt links to its exact one-row grouped FE slice. Full final prompt records and complete source inputs are embedded and included in the downloadable analysis. Generated-artifact availability is read only from hash-verified run records, image content audited remains zero, and no prior judge score is imported. Omit `--catalog` when no frozen catalog is available; the page then labels approved-prop frequency unavailable instead of inferring it.

The distribution page can also be rebuilt independently without generation or model calls:

```bash
uv run "$EVAL_ROOT/build_distribution.py" \
  --prompts "$PROMPTS" --prompts-sha256 "$PROMPTS_SHA256" \
  --run-dir "$RUN_DIR" \
  --catalog /absolute/path/to/frozen/approved_catalog.json
```

Publish or republish the complete run tree after report construction:

```bash
uv run --python 3.12 \
  --with 'foundry-aws-gateway>=2.0.0' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  "$EVAL_ROOT/run_generation.py" \
  --prompts "$PROMPTS" --prompts-sha256 "$PROMPTS_SHA256" \
  --run-dir "$RUN_DIR" --prefix "$PREFIX" --publish-only
```

The final report URL is:

```text
https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/report/viewer.html
```

The distribution URL is:

```text
https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/report/distribution/index.html
```

Local tests are offline and make no endpoint or AWS calls:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108
python -m unittest -v test_surface_runner.py
python -m unittest -v test_rederive_support_metadata.py
python -m unittest -v test_export_revalidated_banks.py
```
