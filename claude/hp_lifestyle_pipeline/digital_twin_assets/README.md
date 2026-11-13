# HP digital-twin reference renders

The images themselves live outside Git on local SSD:

`/mnt/localssd/hp_lifestyle_pipeline/digital_twin_renders_first_column`

They are the 42 unique first-column assets from the supplied Foundry viewer. In the viewer data,
that column is labeled `Input: Input 3: First Frame Cond` and classified as a model input.

Tracked provenance files:

- `first_column_manifest.json` maps viewer rows and eval-set IDs to S3 objects, local filenames,
  dimensions, byte sizes, and SHA-256 checksums.
- `first_column_s3_paths.txt` is the plain list of original S3 URIs.
- `build_first_column_manifest.py` reproduces both files from the viewer's `data.json` and the
  downloaded image directory.

Source viewer:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/training_logs/FFP-83052-foundry-FFP-88382-hp12_pr33690_v4_gemini_v3_4seed_step01102000_inference-2026.09.29-11.07.03/inference/hp12_pr33690_v4_gemini_v3_4seed_step01102000_inference_step01102000_ema=False_2026-09-29T11:25:04/compare_old_vs_new_rewriter_2026-09-29T11.40.39/viewer.html

The manifest contains provenance only. It does not identify the exact commercial SKU shown in
each render; that matching is a separate research step.
