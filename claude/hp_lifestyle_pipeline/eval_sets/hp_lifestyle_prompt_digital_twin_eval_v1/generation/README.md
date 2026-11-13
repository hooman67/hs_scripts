# HP endpoint generation

This runner sends all 192 prompt × compatible-digital-twin rows to the HP image endpoint. It uploads each of the 30 unique twins once, records its reference-blob ID and source provenance, runs one generation per row, downloads each output immediately, preserves the complete `debugData`, and resumes only when prior records match the current inputs.

```bash
uv run /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation/run_generation.py \
  --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/provenance_verified_v1 \
  --workers 8 \
  --retries 2
```

The request is fixed to 2368×1776, one output, prompt rewriting enabled, `gemini-3.1-pro`, and 50 inference steps. No bearer token is embedded or required by the supplied Pluto endpoint at the time of this run.

## Reference-integrity guards

Before upload, the runner reads each twin file once, hashes those exact bytes, verifies the byte count and SHA-256 against `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/digital_twin_assets/first_column_manifest.json`, and sends the same in-memory bytes to the upload endpoint. Each cached blob binding records the blob ID, twin ID, manifest filename, actual source path, byte count, image dimensions, source SHA-256, complete source-manifest SHA-256, and upload endpoint. Every cached binding is checked against the current manifest before reuse.

Completed-row records include hashes of the prompt and canonical request payload plus the complete reference binding and source-manifest hash. A completed record is skipped only when its row identity, prompt, exact payload, reference binding, and manifest hash still match. Legacy `blob_ids.json` entries or completed records without these provenance fields fail clearly. Use a new run directory to regenerate verified bindings and records; the runner does not silently trust, repair, or overwrite historical runs.

Smoke imports require explicit `--smoke-twin-id`, `--smoke-source-path`, and `--smoke-source-sha256` arguments. The row must name that twin, the supplied source bytes and declared hash must match the manifest entry, and the saved request payload must match the current prompt, settings, and returned blob ID. The file passed through `--smoke-blob-path` must preserve both the upload response's `images` list and an `upload_provenance` object recorded at upload time with `twin_id`, `local_filename`, resolved `source_path`, `source_sha256`, `source_bytes`, `width`, `height`, `source_manifest_sha256`, and `upload_endpoint`. Raw legacy upload responses are rejected because they cannot prove which bytes produced the blob. For example:

```bash
uv run /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation/run_generation.py \
  --run-dir /mnt/localssd/hp_lifestyle_pipeline/generation_runs/new_verified_run \
  --import-smoke \
  --smoke-blob-path /tmp/hp_verified_blob_probe.json \
  --smoke-twin-id baseline-0016 \
  --smoke-source-path /mnt/localssd/hp_lifestyle_pipeline/digital_twin_renders_first_column/09_baseline-0016.jpg \
  --smoke-source-sha256 ea37612566c142ce1a31461708f6219fb68549f13998e5b58b33b4fbb0629301
```

The upload service returns a blob ID but does not echo a content digest. For ordinary runner-managed uploads, provenance is bound directly to the bytes sent. A smoke import cross-checks upload-time provenance, the explicitly supplied local source, the current manifest, and the saved request, but it cannot independently query the service to recover or hash the already-uploaded blob bytes. Upload-time provenance must therefore be captured as part of the smoke upload operation rather than reconstructed afterward.

Run the local regressions without endpoint calls:

```bash
python -m unittest discover -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation -p test_reference_integrity.py -v
```

## FE viewer input

Build the parquet consumed by the shared `$fe-html` publisher from a completed run:

```bash
uv run /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation/build_fe_input.py \
  --run-dir /mnt/localssd/hp_lifestyle_pipeline/generation_runs/hp_lifestyle_prompt_digital_twin_eval_v1_generated_v1
```

The resulting `/mnt/localssd/hp_lifestyle_pipeline/generation_runs/hp_lifestyle_prompt_digital_twin_eval_v1_generated_v1/fe_html_input.parquet` contains all 192 rows, with digital-twin and generated-output images plus prompt, source messaging, explanation, rewritten prompt, and complete generation debug data.

Historical published FE viewer (contains eight excluded baseline-0016 reference-mismatch rows; these guards were added after that run): `https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1/fe_html/viewer.html`

The frozen V1 release is unchanged. Its 192 successful outputs mean endpoint completion only; eight are invalid reference comparisons and 184 remain eligible for visual analysis. See `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity/SUMMARY.md`. Do not resume the historical generated_v1 run with this hardened runner or describe legacy entries as hash-verified.
