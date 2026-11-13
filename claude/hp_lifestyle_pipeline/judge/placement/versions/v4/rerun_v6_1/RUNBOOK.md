# V4 judge rerun on the frozen V6.1 160-image set

Status: **prepared and dependency-gated; no V4 judge call or S3 write has occurred**.

This directory is isolated from V3 and from the existing grouped consensus report. The execution gate is an explicit handoff from `/root` containing the frozen V4 path and SHA-256. Do not copy, edit, infer, or reconstruct V4 from the Astra working folder.

## Frozen inputs already verified

- Evaluation manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json`
- Manifest SHA-256: `fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc`
- Rows: 160 unique scene-generation images; 80 laptop and 80 printer.
- Source-input banks: 16 ordered `device + view.camera_tag` banks, each containing exact prompt ranks 1 through 10.
- Digital twins: 16 unique hash-bound images.
- Local pixel root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/local_runs/v6_1_placement_assets` (about 798 MiB).
- Canonical FE viewer: `/home/colligo/hs_scripts/claude/dotclaude/scripts/fe_html/annotation_viewer.html`; observed SHA-256 `b10c91e5f939b555ce0332f7269baefd2e1ef1b0117c6ae9530188808cbbcc2a`.

The read-only preflight is:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/preflight_v6_1.py
```

It validates every local image hash, prompt hash, row ID, stage, device split, twin count, bank, and prompt rank without creating a run or calling a model.

## Required frozen V4 handoff

Before execution, `/root` must provide all of the following:

1. Absolute frozen V4 root or protocol-manifest path.
2. SHA-256 of the freeze/manifest and, preferably, hashes of the prompt, schema, scoring code, runner, and batch runner.
3. Exact model/deployment name and runner command line.
4. Whether V4 is one call per row or a multi-stage policy.
5. Its cache/resume contract and the expected per-row and run-level artifacts.
6. The V4-compatible FE adapter or a declared result schema that an isolated adapter may validate.
7. The review-question configuration to append to the published viewer URL.

On receipt, write a handoff record beneath this directory containing paths and hashes only. Verify all supplied hashes before `--validate-only` or any live call. Never point the V3 batch runner at V4 files by changing V3 in place.

## Planned execution layout

- Run evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/runs/v4_v6_1_r1/`
- Detached log: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/logs/v4_v6_1_r1.log`
- V4 FE source report: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_r1/`
- Grouped FE report: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_grouped_r1/`
- Publication evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/publication/`
- Tmux session: `hp-placement-v4-v61-160-r1`.

The exact judge invocation remains intentionally blank until the frozen V4 runner arrives. Once supplied, first run its read-only/validate-only mode against the manifest. Then run the exact command inside the named detached tmux session and tee stdout/stderr into the durable log. A completed run must bind all 160 IDs to the manifest hash, bind each result to the frozen V4 hashes, have no errors, and record the exact model returned and usage.

## Resumability

The existing V3 mechanism is resumable by request fingerprint: a valid existing `result.json` is returned from cache, while a failed or different fingerprint is rejected; `progress.json` is atomically updated and pins manifest hash, model, visual-anchor setting, and record order. It makes up to three attempts only for HTTP 429/500/502/503/504.

V4 must preserve an equivalent or stronger contract before the 160-row run begins. If the frozen V4 runner has a different contract, document and test it on the exact manifest in validate-only mode. Never resume by treating a partially written or failed result as complete.

## Runtime, calls, and cost boundary

Historical one-pass measurements on these exact 160 inputs provide bounds, not a V4 promise:

| Saved run | Workers | Wall time | API attempts | Total tokens |
|---|---:|---:|---:|---:|
| V2 baseline with visual anchors | 4 | 32m 58s | 160 | 2,487,713 |
| Compact V3 without anchors | 3 | 25m 55s | 160 | 1,070,462 |

Both returned `gpt-5.5-2026-04-24` with one successful attempt per row. V4 call count is `160 × frozen calls per row`; exact runtime and money cannot be stated until the handoff fixes the model, number of stages, context size, concurrency, and internal Azure price. Before launch, record the fixed pricing source and compute:

`cost = input_tokens × input_rate + cached_input_tokens × cached_rate + output_tokens × output_rate`

Do not substitute public OpenAI pricing for an internal Azure/Foundry deployment without evidence that the rates are the same.

## FE build and grouping

The V3 FE builder validates exact manifest/result identity, protocol hashes, complete progress, original prompts and pixels, and deterministic scoring before producing combined/laptop/printer reports. It is V3-schema-specific and must not be reused blindly for V4. Use the frozen handoff's V4 FE adapter or add an isolated V4 adapter here after the result schema is known.

After a validated V4 combined `data.json` exists, build the 16×10 view without changing that source:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/build_grouped_report.py \
  --source-data /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_r1/combined/data.json \
  --output /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_grouped_r1 \
  --title 'HP natural-placement judge V4 — V6.1 grouped by source input (10 prompts each)' \
  --prefix hp_natural_placement_judge_v4_v6_1_20261105/grouped_by_source_input_r1
```

The builder refuses an existing output directory, requires exact ID equality, and writes one 160-row root plus 16 ten-row reports. Expected publication set: 34 objects (`data.json` and `viewer.html` at the root and in each group). It reuses all input, prompt, image, and judge-evidence fields from the validated V4 FE source.

## Publication plan

Proposed immutable destination:

`s3://foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v4_v6_1_20261105/grouped_by_source_input_r1/`

Expected viewer:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp_natural_placement_judge_v4_v6_1_20261105/grouped_by_source_input_r1/viewer.html`

The prefix has not been confirmed empty because the standard Pluto broker token is absent on this host. The publisher performs 34 `HeadObject` collision checks and refuses any overwrite before its first write. Dry-run validation does not require AWS:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/publish_grouped_report.py \
  --source-root /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_grouped_r1 \
  --bucket foundry-hp-enterprise-adobe-assets \
  --prefix hp_natural_placement_judge_v4_v6_1_20261105/grouped_by_source_input_r1
```

After the report is reviewed locally and publication is authorized by the active task, refresh AWS credentials and execute in the same shell:

```bash
uv run --script /home/colligo/hs_scripts/claude/dotclaude/scripts/foundry_aws_creds.py
source /home/colligo/.claude/hshariati/aws_creds.env && \
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/publish_grouped_report.py \
  --source-root /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v4/rerun_v6_1/fe_reports/v4_v6_1_grouped_r1 \
  --bucket foundry-hp-enterprise-adobe-assets \
  --prefix hp_natural_placement_judge_v4_v6_1_20261105/grouped_by_source_input_r1 \
  --execute
```

Capture the publisher JSON under `publication/`, append the frozen review query to the root and group URLs, and independently list/download/hash the exact 34-object set. Do not upload annotations and do not copy any annotation object from the V3 consensus prefix.

## Credential state

- Judge: the historical runner uses the shared `gpt_call` Azure client, with a configured Azure credential fallback. The frozen V4 handoff must state its actual client route; no credential value belongs in requests or tracked artifacts.
- S3: use the `/aws-creds` workflow and source `/home/colligo/.claude/hshariati/aws_creds.env` in the same shell as the upload.
- Current blocker: `/home/colligo/.claude/hshariati/credentials.yaml`, `/home/colligo/hs_scripts/claude/hshariati/credentials.yaml`, and `/home/colligo/Downloads/creds.txt` are absent, so the broker could not mint S3 credentials during preparation.
