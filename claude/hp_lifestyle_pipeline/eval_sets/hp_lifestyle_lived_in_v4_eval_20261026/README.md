# HP lifestyle lived-in V4 evaluation scaffold

This isolated evaluation reuses the V3 execution mechanics without copying any V3 records,
accepted banks, selections, generation outputs, or publication state. It produces 18 independent
text banks from nine original source records crossed with their matching close and wide camera
tags. Each bank contains 30 candidates, for 540 prompts total. Six candidates per bank are selected
for an explicitly reviewed 108-image generation set.

Canonical prompt, schema, finalizer, and camera-registry files live under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4`

The native environment values are `Home`, `Office`, `Education`, `Gaming`, `Café`, and
`Creative Studio`. No post-hoc display taxonomy is used.

## Workflow

1. Build the immutable source/camera manifest and exact two-field runtime inputs:

   `python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/build_eval_manifest.py`

2. Run GPT-5.5 only after the V4 prompt/schema/registry are final and root authorizes network calls:

   `uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/run_gpt55.py --all-authorized`

   The four-camera probe command accepts repeated `--case` flags and covers close/wide for one
   printer source and one laptop source:

   ```bash
   uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/run_gpt55.py \
     --case ee810cf51bb82bb4__printer_FrontRightCloseUp \
     --case ee810cf51bb82bb4__printer_FrontRightWide \
     --case 22fdbf19f03d1a31__laptop_FrontRightCloseUp \
     --case 22fdbf19f03d1a31__laptop_FrontRightWide \
     --max-concurrency 2
   ```

3. Rebuild or revalidate immutable attempts offline with `finalize_records.py` and
   `revalidate_records.py`. Then run `select_candidates.py`.

4. Root reviews all 108 rows and creates a review JSON with exactly these keys:
   `version`, `reviewer`, `decision`, `selection_manifest_sha256`,
   `accepted_prompt_cases_sha256`, `reviewed_selection_count`, and `notes`. Approval requires
   `reviewer=root`, `decision=approve_for_image_generation`, and
   `reviewed_selection_count=108`. Apply it with `approve_selection.py --review <absolute path>`.

5. Run `export_generation_prompts.py`, then use `generation/run_generation.py` only after the
   manifest and root approval gates pass. The fixed payload uses 2560×1440 for the approved 16:9
   references, seed 42, `n=1`, Gemini 3.1 Pro prompt rewriting, and 50 inference steps.

6. `build_gallery.py` creates a progressive local gallery. The publisher writes only to
   `s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/`
   after all candidate and root-approval gates pass.

No GPT, image-generation, AWS, or publication command is run by this scaffold.

## Scaffold reproduction

These checks are local and do not call a model or endpoint:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONPYCACHEPREFIX=/tmp/hp_lifestyle_v4_pycache python -m compileall -q /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026
PYTHONPYCACHEPREFIX=/tmp/hp_lifestyle_v4_pycache python -m unittest discover -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/tests -p 'test_*.py'
PYTHONPYCACHEPREFIX=/tmp/hp_lifestyle_v4_pycache python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generation/test_run_generation.py
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/preflight_health.py
```

After root explicitly approves read-only network checks, this command checks endpoint health,
OpenAPI, and GPT client credential construction without a completion or generation request:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/preflight_health.py \
  --endpoint --gpt-auth \
  --output /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/preflight_health.json
```

After root has semantically reviewed the frozen 108-row selection and authored
`root_selection_approval.json` with the pending artifact hashes, the exact approval command is:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/approve_selection.py \
  --review /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/root_selection_approval.json
```

The exact full-generation command, only after that approval succeeds and root separately authorizes
endpoint execution, is:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generation/run_generation.py --all
```

For a detached run that survives the invoking shell, create the durable run directory first and
launch the same resumable runner with an absolute log path:

```bash
mkdir -p /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026
setsid -f bash -c 'exec uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generation/run_generation.py --all --workers 2 --upload-workers 2 >> /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026/generation.log 2>&1'
```

Rerunning that command against the same run directory resumes from hash-checked blob bindings,
jobs, and records. Ambiguous submissions remain held instead of being resubmitted automatically.
