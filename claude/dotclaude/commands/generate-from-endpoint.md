Run a customer's generation endpoint over a prompt set, upload outputs to S3, and produce a foundry-aws-corp gallery.

Usage:
- Fresh run: `/generate-from-endpoint <customer> <prompts-csv-or-s3-uri> [--seeds 333,777] [--ids 1,2,3] [--limit N] [--skip-ids X,Y] [--run-name foo] [--workers 8] [--retries 2] [--no-upload]`
- Retry only the transient failures from a previous run: `/generate-from-endpoint <customer> --retry-failed-from <run-dir-or-results.csv>`

## What it does

1. Reads a prompts CSV (columns: `id, Category, Prompt, Aspect Ratio`).
2. For each (prompt × seed) pair, calls the customer's async generate endpoint and polls until done.
3. Captures: model-returned seed, image, `rewritten_prompt`, `rewritten_negative_prompt`. Records `prompt_unsafe` / `http_*` failures cleanly in the CSV.
4. Writes `results.csv`, `run_info.txt`, and the 5-file IMS-auth gallery (`gallery/index.html`, `imsauth.js`, `style.css`, `main.js`, `data.js`).
5. Uploads everything to `s3://<customer-bucket>/hs_results/<YYYY-MM-DD>_<prompt_set>[_<run-name>]/`.

## Pre-flight

- **Bearer token** for the endpoint must be at `/tmp/auth_token.txt` (paste the bearer token from a working browser request — the `authorization: Bearer <...>` value). Ask the user to refresh if 401s.
- **AWS creds** must be at `~/Downloads/creds.txt` (from `https://foundry-aws-corp.adobe.io/`). Ask the user to refresh on `ExpiredToken`.
- Prompts CSV can be a local file or `s3://...` (download first with `aws s3 cp`).

## How to invoke

The script lives at `~/.claude/scripts/generate_from_endpoint/runner.py`. Run it with `uv` so inline PEP 723 deps (httpx, boto3, tqdm) are resolved automatically:

```bash
# 1. If the prompts source is s3://..., copy it down first
source ~/Downloads/creds.txt
set -a; . ~/Downloads/creds.txt; set +a
export AWS_ACCESS_KEY_ID="$aws_access_key_id" AWS_SECRET_ACCESS_KEY="$aws_secret_access_key" AWS_SESSION_TOKEN="$aws_session_token"
aws s3 cp s3://.../prompts.csv /tmp/prompts.csv --region us-west-2

# 2. Run the generation
cd ~/.claude/scripts/generate_from_endpoint
uv run runner.py \
  --customer <customer_module_name> \
  --prompts-csv /tmp/prompts.csv \
  --token-file /tmp/auth_token.txt \
  --seeds 333,777 \
  [--ids 131,190,191]   # cherry-pick specific prompt ids
  [--limit 5]           # smoke-test with first N
  [--skip-ids 1]        # skip known-unsafe ids
  [--run-name smoke5]   # suffix for the run folder
  [--workers 8]         # parallel in-flight gens (default 8)
  [--no-upload]         # skip S3 upload (debug only)
```

For long runs, kick off via `Bash` with `run_in_background=true` so you're notified on completion instead of polling.

## Reliability

- **Per-task retries**: each (prompt × seed) auto-retries up to `--retries N` times (default 2 = up to 3 total attempts) on transient errors — `submit_error`, `poll_exception`, `download_error`, `job_canceled`, `job_timeout`, `runtime_error`, `timeout`, `worker_exception`. `prompt_unsafe` and HTTP 4xx are never retried.
- **S3 upload retries**: `aws s3 sync`/`cp` calls are looped up to 5 times with backoff. Since sync is idempotent it's safe to loop.
- **Resume a partial run**: if a long run finished but some tasks failed transiently (DNS blip, brief endpoint hiccup), use `--retry-failed-from <run-dir>` to re-run only the retryable rows and merge results back. No new run folder is created — the existing `results.csv`, gallery, and S3 prefix are updated in place.

```bash
cd ~/.claude/scripts/generate_from_endpoint
uv run runner.py \
  --customer humain_t2i \
  --retry-failed-from ~/.claude/scripts/generate_from_endpoint/runs/2026-05-22_humain_prompts
```

## Adding a new customer / workflow

Create `~/.claude/scripts/generate_from_endpoint/customers/<name>.py` exposing:

- `ENDPOINT_URL` — POST URL for the async generate endpoint
- `RESULT_URL_TEMPLATE` — GET URL with `{job_id}` placeholder
- `X_API_KEY` — the `x-api-key` header value
- `S3_BUCKET`, `S3_ROOT_PREFIX`, `AWS_REGION` — where uploads land
- `ASPECT_RATIO_TO_SIZE` dict + `aspect_to_size(ar) -> (w, h)`
- `build_payload(prompt, seed, aspect_ratio) -> dict` — request body
- `parse_result(resp) -> dict` returning `{status, model_seed, presigned_url, image_id, rewritten_prompt, rewritten_negative_prompt, error_code, error_message}`. Status must be `"in_progress" | "done" | "failed"`.

See `customers/humain_t2i.py` as the reference.

## Output layout

```
s3://<bucket>/hs_results/<date>_<promptset>[_<run-name>]/
├── images/                        prompt<id>_seed<model_seed>.png
├── results.csv                    prompt_id, category, aspect_ratio, original_prompt,
│                                  input_seed, model_seed, image_filename, s3_image_uri,
│                                  rewritten_prompt, rewritten_negative_prompt,
│                                  status, error_code, error_message
├── run_info.txt                   summary (counts, timestamp, endpoint, etc.)
└── gallery/                       5-file IMS-auth gallery
    ├── index.html
    ├── imsauth.js                 verbatim from gallery_template/
    ├── style.css                  dark theme matching /render-s3-gallery
    ├── main.js                    renders prompt cards with seed grid + lightbox
    └── data.js                    GALLERY_DATA = { meta, prompts: [...] }
```

View at: `https://foundry-aws-corp.adobe.io/asset/<bucket>/hs_results/<run-folder>/gallery/index.html`
