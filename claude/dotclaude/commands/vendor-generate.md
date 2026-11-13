Submit each row of a Foundry viz HTML to the Deccan Media Studio API and produce a new viz HTML with a "Generated" column added. Resumable, parallelizable, runs against any model_id (UUID or slug) on `https://media-studio-core.platform.deccan.ai`.

Usage: `/vendor-generate <html_url_or_s3_uri> <model_id> [options]`

Parse `$ARGUMENTS` to extract:
- **html**: foundry-aws-corp URL or `s3://<bucket>/<key>.html` for the source viz HTML
- **model_id**: vendor model UUID or slug (e.g. `65987428-6125-5615-9d07-78891590deed` or `img-edit-pro`)
- Optional flags (see Options below)

## Credentials

- **AWS** (for S3 read/write + presigning): exported in `~/Downloads/creds.txt`. Refresh from https://foundry-aws-corp.adobe.io/ → "Get Foundry Developer Credentials".
- **Media Studio API key** (`ms_…` format): also in `~/Downloads/creds.txt` on a line `API_key=ms_…`. The script auto-loads it.

```bash
export $(grep '^export' ~/Downloads/creds.txt | sed 's/^export //')
```

If the file is missing or expired, ask the user to refresh.

## What this does

For each row in the source HTML's `const DATA = [...]` array:
1. Auto-detect which key is the source image (`.src = d.X`) and which is the prompt (`.textContent = d.X`).
2. Convert the source's `foundry-aws-corp.adobe.io` URL → `s3://…` and presign it (24-hour expiry).
3. POST a job to `/v1/jobs` with `{modality, model_ids: [model_id], inputs: {prompt, image_url}}`.
4. Poll `GET /v1/jobs/{id}` until `complete | failed | cancelled`.
5. Download the `result_url` and copy it to our S3 at `<output_prefix>/outputs/<row_idx>__<job_id>.<ext>`.
6. Append a line to `state.jsonl` (resumable).

After all rows finish:
- Modify the source HTML: add `<th>Generated</th>` to thead, fix the `td3` rendering bug (the source's renderPage doesn't actually append the 3rd cell — we patch in `tr.appendChild(td3)`), and replace `DATA` with the new array including a `g` field on each row pointing at the new output's `foundry-aws-corp` URL.
- Upload alongside the source: `<src_dir>/<src_stem>__<model_id>.html`.
- Upload `state.jsonl` to the same prefix.

## Run it

```bash
export $(grep '^export' ~/Downloads/creds.txt | sed 's/^export //')
uv run --script ~/.claude/scripts/vendor_generate.py <html> <model_id> [options]
```

Last stdout line is the `foundry-aws-corp.adobe.io` URL of the output HTML.

## Options

| Flag | Default | Notes |
|---|---|---|
| `--limit N` | none | Run only first N rows (truncates the output HTML too) |
| `--workers N` | 8 | Parallel submit/poll/download workers |
| `--poll-interval` | 5.0 | Seconds between status checks per job |
| `--job-timeout` | 600 | Per-job timeout |
| `--presign-expiry` | 86400 | Seconds — long enough for the vendor's worker to read |
| `--modality` | `image_editing` | Other options: `text_to_image`, `image_to_video`, `video_editing`, `text_to_video`, `text_to_text` |
| `--image-field` | `image_url` | Vendor input field name. Some video models use `video_url` |
| `--output-bucket` | source bucket | Where to write outputs + new HTML |
| `--output-prefix` | `<src_dir>/<src_stem>__<model_id>` | S3 prefix for outputs |
| `--output-html-name` | `<output-prefix>.html` | Full key for the new HTML |
| `--image-key` / `--prompt-key` | auto | Override DATA key auto-detection |
| `--output-key` | `g` | Field added to each DATA row holding the output URL |
| `--output-col-label` | `Generated` | New thead column label |
| `--api-key KEY` | from creds.txt | Media Studio API key |
| `--base-url URL` | `https://media-studio-core.platform.deccan.ai` | Use `.delta.deccan.ai` if you have a key for it |
| `--dry-run` | off | Plan only — list rows + paths, submit nothing |
| `--resume` | off | Skip rows already in `state.jsonl` (success) |
| `--retry-failed` | off | Re-run rows previously marked `failed` / `submit_error` |

## Recommended workflow

1. **Smoke test** with `--limit 2` first to confirm the model accepts the inputs and outputs are sane:
   ```bash
   uv run --script ~/.claude/scripts/vendor_generate.py <html> <model_id> --limit 2
   ```
   Open the output URL in a browser and inspect both rows.

2. **Full run** — drop the limit. State is checkpointed per row, so it's safe to Ctrl-C and resume:
   ```bash
   uv run --script ~/.claude/scripts/vendor_generate.py <html> <model_id> --workers 16
   ```

3. **Resume after interruption**:
   ```bash
   uv run --script ~/.claude/scripts/vendor_generate.py <html> <model_id> --workers 16 --resume
   ```

4. **Retry only the failures**:
   ```bash
   uv run --script ~/.claude/scripts/vendor_generate.py <html> <model_id> --retry-failed
   ```

## Available models on `platform.deccan.ai`

23 models are listed by `GET /v1/models`. Notable image-side ones:
- **image_editing**: only `mock-image-edit` (UUID `65987428-6125-5615-9d07-78891590deed`) is currently listed. The slugs `img-edit-pro / img-edit-new / img-edit-pre / img-edit-latest` from the public `image-editing.html` guide are accepted at submit time but fail with `Model not found` at execution — they're not enabled on this account. Confirm with the vendor before attempting full runs against them.
- **text_to_image**: `image-generate-pro`, `image-generate-fast`, `image-generate-pro-alt1`, `image-generate-pro-alt2`, `mock-image-gen`.

## Critical rules

- **Foundry URLs aren't readable by the vendor** — always presign through S3. The script handles this automatically.
- **API base URL** is `https://media-studio-core.platform.deccan.ai`, NOT `…delta.deccan.ai` (the docs URL). The platform host returns 200 with the current key; delta returns 401.
- **AWS session token expires** (a few hours). For long runs, refresh `~/Downloads/creds.txt` mid-run if you hit S3 401s — the script reads creds at startup, so kill + `--resume` after refreshing.
- **`--limit` truncates the output HTML.** If you want a full HTML with only the first N rows generated, run the full set; partial runs intentionally produce partial HTMLs.

## Working sample

The 1-row mock-image-edit sample built during skill development:
```
https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/htmls/viz/dam_swap_object_vendor_generations_SAMPLE.html
```
