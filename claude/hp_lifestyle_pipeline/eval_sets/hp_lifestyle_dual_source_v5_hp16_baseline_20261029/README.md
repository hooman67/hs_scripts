# V5 top-96 baseline on HP16

This evaluation replays the frozen V5 top-six selection through the HP16 five-stage endpoint. It does not regenerate or edit the V5 prompt text.

Source prompt set:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/data/prompts_top6_96.json`

Pinned Git source: `ae1de8f1b07d8b72b6b4c21bc9da17f9113e7d42`

Pinned source SHA-256: `882f60c772fff18b3a008567e46ff112e42af141001fa22bdc5277716497b804`

Endpoint:

`https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev`

## Fixed mapping

| V5 device | HP16 digitalTwinId |
| --- | --- |
| Cashmere | `cashmere_x` |
| EliteBook | `elitebook_13` |
| Tassel | `tassel` |
| Magic | `adf_printer` |

The V5 `source_camera_name` is passed unchanged as HP16 `cameraId`. The endpoint catalog was checked on 2026-10-29: every selected device exposes all four required views.

Exactly one HP16 request is planned for each of the 96 frozen rows. The baseline image is `6_relight_3d.png`. The run also retains `1_hero_white.png`, `1_hero_mask.png`, `2_scene.png`, `3_ibl.exr`, `3_ibl_preview.png`, `4_backplate.png`, and the final endpoint manifest.

## Safety and resume behavior

- The runner verifies the pinned source hash, exact row count, unique keys, SKU mapping, and live endpoint catalog before submission.
- Four private cookie sessions are used by default. Cookie files are mode 600, kept under untracked `local_data`, and never uploaded.
- A returned job ID is durably recorded before polling.
- A submitted job is resumed by job ID. It is not submitted again.
- A submission timeout or connection failure is marked `submit_ambiguous`. It is not automatically retried because the endpoint may have accepted it.
- `done=true` is accepted only when hero, scene, IBL, backplate, and relight all report `done`.
- Artifacts are hashed locally and uploaded individually. Completion records contain no credentials or cookies.
- The runner never changes prompt text and does not silently replace failed rows.

## Credentials

A valid S3D bearer token must be supplied via `S3D_BEARER_TOKEN` or a mode-600 token file passed with `--token-file`. Do not commit the token. `PLUTO_AUTH_TOKEN` was tested and rejected by the HP16 credential endpoint; it is not a substitute.

For S3 publication, obtain temporary Foundry AWS credentials with:

```bash
uv run --script /home/colligo/hs_scripts/claude/dotclaude/scripts/foundry_aws_creds.py
```

Source `/home/colligo/.claude/hshariati/aws_creds.env` in the same shell that launches the runner.

## Commands

Local input/catalog validation, with no paid generation:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029/run_hp16.py --validate-only
```

One-row smoke test:

```bash
set -a
source /home/colligo/.claude/hshariati/aws_creds.env
set +a
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029/run_hp16.py \
  --token-file /tmp/hp16_s3d_token.txt --limit 1 --workers 1
```

Full run/resume:

```bash
set -a
source /home/colligo/.claude/hshariati/aws_creds.env
set +a
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029/run_hp16.py \
  --token-file /tmp/hp16_s3d_token.txt --workers 4
```

Default S3 destination:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029/`

The initial baseline is complete only after 96 terminal-success records, 96 verified final images, complete stage accounting, S3 object verification, and publication of a review gallery containing the prompt and all inputs beside each output.

After completion, build and upload that gallery with:

```bash
set -a
source /home/colligo/.claude/hshariati/aws_creds.env
set +a
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029/build_gallery.py
```

