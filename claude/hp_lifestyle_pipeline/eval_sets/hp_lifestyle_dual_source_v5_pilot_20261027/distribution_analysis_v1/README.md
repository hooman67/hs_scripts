# V5 distribution report

This report deliberately reuses the V4.1 distribution report structure while
adding V5 dual-source scoring and evidence. It includes the semantic map,
environment and C-Tech distributions, reference coverage, repetition checks,
closest and farthest examples, and the full candidate explorer from V4.1. V5
adds source-score distributions, source-versus-C-Tech score plotting, top-six
selection analysis, separate Smart Brief/source-messaging support diagnostics,
and both complete input documents in the explorer.

Build and validate from the repository root:

```bash
python eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/distribution_analysis_v1/build_analysis.py \
  --output eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/distribution_analysis_v1/built
python eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/distribution_analysis_v1/validate_analysis.py \
  eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/distribution_analysis_v1/built
```

The builder loads the frozen MiniLM revision from
`/mnt/localssd/hp_lifestyle_pipeline/cache/huggingface` with
`local_files_only=True`. If the ignored V4.1 baseline analysis is absent, it is
rebuilt from the tracked V4.1 sources before V5 is analyzed.

Publication copies the built `gallery/` and `downloads/` directories into the
V5 eval root, copies `source_manifest.json` to `build_manifest.json`, obtains
Foundry credentials with `/aws-creds`, and runs `publish_review.py`. The
publisher uploads dependencies before `gallery/index.html` and verifies every
S3 object by bytes, SHA-256, and content type.

The V4.1 comparison is descriptive because V5 uses different dual-source inputs
and a different case inventory. No V5 images are claimed or included.
