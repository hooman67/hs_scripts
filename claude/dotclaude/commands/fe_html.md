Build a foundry **annotation-viewer** report (the new `data.json` + self-contained `viewer.html` style) from a folder of images, an S3 prefix, or a parquet — and upload it to S3, viewable at `foundry-aws-corp.adobe.io`.

Usage: /fe_html <input> [output_s3] [--title "..."] [--group-by none|subfolder|all] [--no-secure]

Where `<input>` is one of:
- a **local folder** of images/videos (they get uploaded to `<output>/assets/`)
- an **S3 prefix** `s3://bucket/prefix` of media (referenced **in place**, nothing re-uploaded)
- a **`.parquet`** of media references (intermediate path — handed to the vendored foundry CLI)

This produces the SAME two-file report the foundry `generate-html` skill produces — a row-based
`data.json` rendered by one self-contained `viewer.html` (filter/search/sort, side-by-side compare,
a per-row review questionnaire with rubrics/hard-checks/themes, CSV export, one-click publish + a
Summary tab). It is **not** the older 5-file image gallery — for that, see `/render-s3-gallery`.

## When to use which

| You have | Use |
|---|---|
| A reviewable report with a questionnaire, compare mode, publish/Summary | **`/fe_html`** (this) |
| A quick view-only lightbox gallery of a folder | `/render-s3-gallery` |

## How it works

A report is **two files in one S3 directory**: `data.json` (the rows) + `viewer.html` (the renderer).
Assets are referenced by absolute gateway URL, so no pixels are re-encoded for the S3-prefix path.
The heavy lifting — the exact `data.json` contract, `asset_url`, and the viewer deploy — is the
**vendored, verbatim** copy of foundry's `parquet_to_fe_html.py` at `~/.claude/scripts/fe_html/`
(with `annotation_viewer.html` beside it). The wrapper `~/.claude/scripts/fe_html_report.py` only
adds the folder / S3-prefix inputs and reuses that vendored `to_viewer`, so output is identical to
the official tool. **Never hand-edit those two vendored files** — edit upstream and re-vendor (see
`fe_html/VENDORED_FROM.txt`).

## ⚠️ Secure buckets — share the same-origin `viewer.html`, NEVER the dit-scale-up SPA

The correct, working artifact for a **secure foundry bucket** is the vendored **single-file
`viewer.html`** sitting next to `data.json` in the report dir, opened through the gateway:
`https://foundry-aws-corp.adobe.io/asset/<bucket>/<dir>/viewer.html`. That viewer is built for this
exact case — no ES modules, no separate JS/CSS chunks, and it fetches `data.json` **relatively** so
the gateway `user_token` cookie applies; media render via plain `<img>` (which follows the gateway's
302→presigned-S3 redirect fine).

**Do NOT hand the user (or generate) a "New UI" link of the form**
`https://dit-scale-up.s3.us-west-2.amazonaws.com/fe-html/index.html?urls=<brotli+base64url>`
**for secure buckets.** That SPA is hosted on a *public, different origin*, so against a secure
report it fails two ways: (a) its `<script type="module" crossorigin>` gets 302-redirected to
`*.s3.amazonaws.com` and is **CORS-blocked → blank page**; (b) its cross-origin `fetch()` of the
gateway `data.json` returns **403** (`{"detail":"…not logged in…"}`, no `Access-Control-Allow-Origin`)
→ the "json error". The `urls=` blob decodes (brotli → base64url) to `["<gateway data.json URL>"]`.

### If you inherit a broken dit-scale-up link — how to fix (verified 2026-09-03, THD bookshelf eval)
1. `/aws-creds`, then confirm `data.json` is valid and note its dir (`aws s3 ls`/`cp`).
2. Upload the vendored viewer same-origin, and make the data available at the default path:
   ```bash
   source ~/.claude/hshariati/aws_creds.env
   aws s3 cp ~/.claude/scripts/fe_html/annotation_viewer.html s3://<bucket>/<dir>/viewer.html \
       --region us-west-2 --content-type "text/html; charset=utf-8"
   # viewer defaults to ./data.json (override with ?src=<name>); copy if the data is named otherwise:
   aws s3 cp s3://<bucket>/<dir>/fehtml_data.json s3://<bucket>/<dir>/data.json \
       --region us-west-2 --content-type "application/json"
   ```
3. Share `https://foundry-aws-corp.adobe.io/asset/<bucket>/<dir>/viewer.html` (add `?src=<name>` if you
   didn't copy to `data.json`). Verify the gateway serves it: `curl` it → **HTTP 200** (inline).
- **Gotcha:** the gateway S3 role is **no-delete** — you cannot `aws s3 rm` a mistaken upload. Get the
  path/filename right the first time; don't scatter half-working copies you can't clean up.
- The dit-scale-up SPA is only appropriate for genuinely **public** data (`--no-secure`), where the
  data.json lives on the same public origin as the SPA.

## Ask the user first (report header)

Before generating, ask for the report **title** (the viewer's header, and the only record of *what*
the report shows once the link is shared). If the media came from a specific model/checkpoint or
evalset, mention it in the title. Only skip if the user already gave a title in the conversation.

## Steps

1. Get AWS credentials (needed to list/upload/serve): run `/aws-creds` if `~/.claude/hshariati/aws_creds.env`
   is missing or stale.

2. Run the wrapper, sourcing creds in the **same** shell command (env does not persist across calls):

   ```bash
   source ~/.claude/hshariati/aws_creds.env && uv run --script ~/.claude/scripts/fe_html_report.py \
       --input <folder | s3://bucket/prefix | s3://bucket/data.parquet> \
       [--output s3://bucket/report_dir] \
       --title "My report"
   ```

   - `--output` is **auto-derived** for an S3-prefix input (a sibling `_fe-html/<leaf>/` dir next to
     the source prefix). It is **required** for a local folder or a parquet input.
   - `--group-by none` (default) = one image per row (annotation-native). `subfolder` = one row per
     folder with its images side by side. `all` = a single contact-sheet row.
   - `--no-secure` only for genuinely public buckets; the default (`--secure`) emits gateway URLs for
     foundry buckets.
   - Parquet passthrough flags: `--limit N` (0 = all rows), `--id-col`, `--image-cols/--video-cols/--text-cols/--meta-cols`, `--require col1,col2`.

3. The script prints the viewer URL. Return it to the user:

   ```
   https://foundry-aws-corp.adobe.io/asset/<bucket>/<report_dir>/viewer.html
   ```

   It opens on a **setup screen** to define review questions (or "Skip — comment only"). A shared link
   should carry `?ldap=<reviewer>` so publishing resolves their identity.

## Notes

- **Dependencies** install automatically via `uv run --script` (boto3 always; pandas/pyarrow/s3fs are
  only exercised on the parquet path). First run may take a moment to build the env; it is cached after.
- **Credentials** come from your Foundry AWS creds (`~/.claude/hshariati/aws_creds.env`, via `/aws-creds`),
  picked up by boto3 as `AWS_*` env vars — no `foundry_aws_gateway`/Pluto token needed for this skill.
- **Region** defaults to `us-west-2`.
- **Refreshing the vendored viewer/CLI** (when upstream ships fixes): follow `~/.claude/scripts/fe_html/VENDORED_FROM.txt`.
- **Publishing annotations from the viewer** requires opening the report through the gateway `/asset/…`
  URL (which these links are); the gateway's `PUT /asset` writes `annotations/reviewer_<n>.json`.
