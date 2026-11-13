# Brewmaster `utils/` — Agent handoff + Mask-dataset CSV tooling

This file is the single agent-facing doc for `brewmaster/utils/`. It serves three roles:

1. **Brewmaster handoff** — scope, curated `i2i_mask` metric set, code anchors, validation.
2. **Discoverability** — tools that look for a sibling `AGENTS.md` start here.
3. **Operational reference** — the standalone scripts in `brewmaster/utils/` (CSV
   build, dataset registration, master-JSON backfill, version migrations).

Previously split across `AGENT.md` + `AGENTS.md`; the two were merged on
2026-05-20 (commit history: see `git log` for the rename + concat).

---

## Brewmaster docs map

| Doc | Purpose |
|-----|---------|
| **`AGENTS.md`** *(this file)* | Authoritative handoff — mask metrics, anchors, validation, utils tooling |
| **[`I2I_MASK_REVIEW_MAP.md`](I2I_MASK_REVIEW_MAP.md)** | Reviewer-facing 3-part split for stacked mask-edit PRs |
| **[`../eval_metrics/metrics/image/mask_based/vlm_judge/AGENT.md`](../eval_metrics/metrics/image/mask_based/vlm_judge/AGENT.md)** | VLM-as-judge package — EvalHub + General rubrics, GPT + Gemini wiring |

---

## Scope

- Default code scope: `models/colligo/models/firefly/brewmaster/` (do not widen
  into `third_party/`, lockfiles, or generated registry files per repo rules).
- **`i2i_mask`**: image-edit evaluation with explicit **reference image + mask**.
  Metrics split into regions **outside** the mask (preserve / boundary) vs
  **inside** the mask (fidelity vs reference crops).

---

## Curated `i2i_mask` metric set (current)

What the taxonomy, sync policy, and UI filtering treat as the mask-edit set
(`tests/test_i2i_mask_task.py`: `MASK_METRICS`):

**Outside / boundary (preserve edit, blend at boundary)**

- `outside_exact_match_rate`
- `outside_ssim`
- `outside_boundary_ssim`
- `masked_niqe`

**Inside-mask (full-reference fidelity on the masked region)**

- `inside_ssim`
- `inside_psnr`
- `inside_lpips`
- `inside_fid`

**VLM-as-judge (sidecar-driven, runs on the comparison pod)**

- `vlm_judge_evalhub` — 4 EvalHub rubric questions, GPT + Gemini
- `vlm_judge_general` — 3-axis (instruction-following / identity preservation /
  image quality), 1–5 Likert, GPT + Gemini

---

## Review map

See **[`I2I_MASK_REVIEW_MAP.md`](I2I_MASK_REVIEW_MAP.md)** for a reviewer-facing
**3-PR mental stack** (core metrics vs UI/report vs ecosystem wiring).

When comparing a large Brewmaster branch to `main`, use that doc to **scope
mask-only diffs**; the branch may still carry unrelated Brewmaster edits.

---

## Key implementation anchors

Source is authoritative; this list points; paths are relative to
**`brewmaster/`** (one level up from this file):

| Area | Primary files |
|------|----------------|
| Metric definitions & registration | `eval_metrics/metrics/image/mask_based/`, `eval_metrics/config/metrics_registry.py`, `eval_metrics/config/task_taxonomy.py` |
| Presentation / normalization flags | `backend/services/metric_presentation.py` |
| Comparison report (incl. raw/normalized summaries for mask viz) | `backend/services/report_generator/builder.py`, `backend/services/report_generator/utils/scores_processing.py` |
| UI | `frontend/src/components/job/JobResultsVisualization.tsx`, `frontend/src/components/job/VlmJudgePanel.tsx` |
| Task-filtered metrics API / sync dedupe | `backend/services/metric_task_policy.py`, `backend/api/v1/metrics.py`, `backend/services/metric_sync_service.py` |
| CSV → master JSON (+ multi-URL `model__*` cells) | `backend/services/dataset_parser.py`, **`utils/brewmaster_dataset_setup.py`**, **`utils/build_v5_colligo_csv.py`** |
| VLM-as-judge (i2i_mask rubric, GPT + Gemini) | `eval_metrics/metrics/image/mask_based/vlm_judge/` |
| Job recovery + master-JSON backfill | `backend/services/eval/job_recovery.py`, `scripts/recover_brewmaster_job.py`, `scripts/backfill_master_json_from_report.py` |

---

## `utils/` layout

```
utils/
├── AGENTS.md                     # This file (handoff + tooling guide)
├── I2I_MASK_REVIEW_MAP.md        # PR split for reviewers
├── brewmaster_dataset_setup.py   # Build mask CSV from inference HTML exports
├── build_v5_colligo_csv.py       # Add a 3rd-model column to an existing v3 CSV using clio.corp.adobe.com HTMLs
└── send_data.py                  # POST dataset + models to the Brewmaster API
```

---

## When to reach for each tool

- **`brewmaster_dataset_setup.py`** — fresh CSV from inference HTML exports
  (teacher + student, or `--model1-url` + `--model2-url`). HTML→CSV with
  single-seed `model__*` cells. Supports legacy and fresh-mask modes.

- **`build_v5_colligo_csv.py`** — *extend* an existing CSV with a third model
  column whose URLs come from clio.corp.adobe.com EvalHub HTMLs (S3-backed,
  accessed via the pod IAM role; no auth file needed). Preserves the existing
  `prompt`/`ref_images`/`student`/`teacher` columns verbatim.

- **`send_data.py`** — thin client that `POST`s the registered dataset + each
  model name to the local Brewmaster API once the CSV is on shared storage.

---

## `brewmaster_dataset_setup.py`

Run from repo root **or** brewmaster dir; the script uses stdlib networking plus
optional `boto3` / `brotli`:

```bash
cd /home/colligo/colligo
source ./m

python models/colligo/models/firefly/brewmaster/utils/brewmaster_dataset_setup.py \
  --model1-url "https://.../eval_run_1" "https://.../eval_run_part2" \
  --model1-name student_mask_evalhub_combined_v3 \
  --model2-url "https://.../teacher_textedits" "https://.../teacher_part1" \
  --model2-name teacher_mask_evalhub_combined_v3 \
  --output /sensei-fs/users/<you>/brewmaster/main_datasets/<name>_v3.csv \
  --img-index 2 \
  --validate-urls
```

### Modes

- **Fresh mask mode** (preferred): `--model1-url/--model1-name/--model2-url/--model2-name`.
  Supports **multiple URLs per side** so you can merge split exports
  (same prompt set split across `_part1` / `_part2` folders).

- **Legacy mode**: `--teacher` / `--student` with optional `--teacher-name` /
  `--student-name` for CSV column prefixes.

### URL shapes accepted

Inference export roots, `index.html`, or literal `data.json` URLs — all normalized.

**`fe-html` viewer links** (`.../fe-html/index.html?urls=...`) decode to embedded
manifest URLs (Base64 + Brotli JSON list). Requires `pip install brotli`.
If decoding fails or is undesirable, paste the resolved `data.json` URLs explicitly.

### Single-seed invariant

Outputs **one URL** per `model__*` column. Extra seeds detected for the same logical
prompt are **dropped after the first**, with stdout explaining counts. Tune which
seed is chosen with **`--img-index`** (defaults to `2` for the first synthesis
slot in the viewer contract the script assumes).

Upstream `dataset_parser.py` **can split comma-separated URLs** inside a cell
into multiple assets, but comparisons are cleaner when each cell intentionally
holds **one** URL matching the CSV column basename used in `MODEL_NAMES`.

### Optional URL probing

`--validate-urls` HEAD-probes refs, masks, and model URLs; failed rows land in a
`<output>_dropped.txt` sidecar so Pluto jobs avoid mass `*_not_found` skips.

Tune concurrency with **`--validate-workers`** (default 32).

### Fetch path

Prefer direct **HTTPS GET** when the URL is reachable anonymously; **`boto3`**
fallback may run when buckets require SDK auth — keep credentials scoped and
never commit them.

---

## `build_v5_colligo_csv.py`

Designed for the case where the v3 CSV already exists (teacher + student
columns from `brewmaster_dataset_setup.py`) and a third model needs to be
spliced in from two new clio.corp.adobe.com EvalHub HTMLs.

```bash
python -m colligo.models.firefly.brewmaster.utils.build_v5_colligo_csv \
  --textedit-html 's3://clio.corp.adobe.com/.../instructedit_w_masks_eval_v5_textedit/i2i_v5_final_<date>.html' \
  --general-html  's3://clio.corp.adobe.com/.../instructedit_w_masks_eval_v5_rewritten_final/i2i_v5_final_<date>.html'
```

- Defaults to the canonical paths under
  `/sensei-fs/users/atono/brewmaster/main_datasets/`.
- `clio.corp.adobe.com` IS an S3 bucket (not just an HTTP frontend); pod IAM
  role grants read access. Script clears local `AWS_*` env vars before calling
  `aws s3 cp` so a sourced-user creds file doesn't shadow the role.
- Validates `240` textedit + `717` general rows.
- Extracts each row's `image1` field (= **sample 1**, the first generated
  result column after ref + mask in the viewer layout); other generation
  fields (`https_video1..3_ssr`) are intentionally ignored to keep the CSV
  single-seed.
- Writes a 5-column CSV with the new
  `model__colligo_student_mask_evalhub_combined_v3` column.

To bump versions when colligo emits new HTMLs (new checkpoint, same prompt
set), rerun with new `--textedit-html` / `--general-html`, set a new
`--output` filename, then edit `send_data.py`'s `version` field (e.g.
`v1.0` → `v2.0`) and re-register.

---

## `send_data.py`

Thin client for onboarding the CSV produced above:

1. Set **`DATASET_PAYLOAD`** (`storage_url`, names, tags, **`task_type`: `i2i_mask`**).
2. Set **`MODEL_NAMES`** to match the **`model__*` column suffixes** in the CSV
   (characters after `model__`). Mismatches register duplicate models — verify
   with `curl -s http://localhost:8000/api/v1/models | jq` before running.
3. Start the Brewmaster backend, then adjust **`API_BASE_URL`** if needed
   (default targets `localhost:8001`).

```bash
python models/colligo/models/firefly/brewmaster/utils/send_data.py
```

The script tolerates **`400` "already exists"** responses — check logs printed
per resource.

---

## Compatibility / migration notes

- Historic runs may still have DB rows or reports mentioning **removed** mask
  metric names. Non-destructive deduplication / task filtering keeps **only**
  taxonomy-curated names for **`i2i_mask`** where `metric_task_policy` and
  tests apply.
- Regression coverage for API filtering and sync lives mainly in
  **`tests/test_i2i_mask_task.py`** and **`tests/test_mask_metric_alignment.py`**.
- When a job hits a sensei-fs quota mid-run, the master-JSON cache ends up
  sparse but the in-process comparison report is still complete. Recover via
  **`scripts/backfill_master_json_from_report.py <job_id>`** which reads the
  report off sensei-fs and writes per-asset scores into the master JSON in a
  single batched call.

---

## Validation (focused)

From repo root after `source ./m`:

```bash
pytest models/colligo/models/firefly/brewmaster/tests/test_i2i_mask_task.py -q
pytest models/colligo/models/firefly/brewmaster/tests/test_mask_metric_alignment.py -q
pytest models/colligo/models/firefly/brewmaster/tests/test_inside_mask_metrics.py -q
pytest models/colligo/models/firefly/brewmaster/tests/test_scores_processing.py -q
pytest models/colligo/models/firefly/brewmaster/tests/test_vlm_judge_rubric.py -q
```

For mypy/ruff on the whole package:

```bash
./m lint --check --only-envs dev --paths models/colligo/models/firefly/brewmaster
```

---

## Conventions for Colligo assistants

- Do **not** commit host-specific absolute paths besides examples; callers should
  substitute `/sensei-fs/users/<ldap>/...` for their LDAP.
- Respect repo rules: **`uv.lock`** and `third_party/` stay hands-off unless the
  user owns a separate change.
- Helpers under `utils/` are **stdlib-first standalone** scripts where possible —
  avoid importing Brewmaster internals unless extending them deliberately with
  proper package paths and tests.

---

## History

Originally documented in **`f53bc7a5740dd4789cf8b3ab0392e11169a009ec`** (FFP-83032,
curated outside-only mask metrics + ecosystem wiring) when the doc lived at
`brewmaster/AGENT.md`.

Subsequent updates added:

- Inside-mask fidelity metrics (`inside_ssim/psnr/lpips/fid`) + taxonomy alignment
- Comparison **raw/normalized** summaries for visualization-sensitive mask metrics
- `utils/` dataset tooling (now in this doc + `brewmaster_dataset_setup.py`)
- VLM-as-judge (EvalHub + General flavors, GPT + Gemini, sidecar runner)
- Job recovery + master-JSON backfill utilities
- `build_v5_colligo_csv.py` for splicing a third model into existing CSVs
- AGENT.md + AGENTS.md merged into this single file (2026-05-20)

GitHub commits on the private **`Adobe-Firefly/colligo`** repo require enterprise
SSO; use `git show <sha>` locally when SSO blocks the UI.
