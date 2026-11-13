# V4.3.1 judge on the original V6.1 160-scene set

Status: **prepared, frozen, and locally validated; no model call or S3 write has been made by this package**.

The input is the verified 160-row scene-generation manifest:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json`

Its required SHA-256 is `fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc`. The run uses V4.3.1 unchanged, requests `gpt-5.5` with high reasoning, and permits at most two concurrent rows. Each row retains the request, selected anchors, support crop and provenance, attempt metadata, raw response or error, deterministic result, and audit hashes.

## Read-only validation

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
uv run --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --with 'jsonschema==4.25.1' \
  --with 'pillow==12.0.0' \
  --with 'opencv-python-headless==4.10.0.84' \
  --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/run_batch.py \
  --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/runs/original_v6_1_full160_r1 \
  --validate-only
```

Validation verifies all 160 prompt and image hashes plus the frozen prompt, schemas, scoring, crop, anchors, runner, batch runner, model, and concurrency contract. It does not create the run directory.

## Authorized launch

Launch only after the active root agent accepts the six-case V4.3.1 gate:

```bash
tmux new-session -d -s hp-placement-v431-v61-160 \
  "cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline && \
   uv run --python 3.12 \
     --with 'foundry-aws-gateway[llm]>=2.0.0' \
     --with 'jsonschema==4.25.1' \
     --with 'pillow==12.0.0' \
     --with 'opencv-python-headless==4.10.0.84' \
     --extra-index-url 'https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple' \
     python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/run_batch.py \
     --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/runs/original_v6_1_full160_r1 \
     --workers 2 \
     --acknowledge-launch-authorized \
   2>&1 | tee /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/runs/original_v6_1_full160_r1.log"
```

The progress ledger is atomic and resumable. On restart, interrupted rows return to pending and valid `result.json` files are checked against the same input fingerprint. A row is complete only after the saved result, deterministic score, protocol hashes, model identity, request input, and attempt evidence validate. Invalid/error results remain errors; they are never silently accepted.

## Grouped FE report

After all 160 rows complete:

```bash
uv run --python 3.12 --with 'jsonschema==4.25.1' \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/build_grouped_report.py \
  --run-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/runs/original_v6_1_full160_r1 \
  --output /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4_3_1/full160_original_v6_1/fe_reports/original_v6_1_full160_r1 \
  --prefix hp_natural_placement_judge_v4_3_1_v6_1_20261106/original/grouped_by_source_input
```

The builder performs no calls or uploads. It refuses an existing output directory, validates all 160 results and the complete progress ledger, recomputes deterministic scoring, and emits one 160-row root report plus 16 ten-row device/camera reports. The generated-scene and twin URLs are reused from the already verified V3 grouped report, with exact manifest ID and generated-image URL checks and a one-to-one mapping of the 16 twin hashes.

The output contains 34 publishable FE objects (`data.json` and `viewer.html` at the root and under each group) plus a local `build_manifest.json`. Publication is deliberately outside this preparation package and must use `/aws-creds` when authorized.
