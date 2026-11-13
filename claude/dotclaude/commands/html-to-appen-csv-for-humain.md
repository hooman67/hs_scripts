Convert a Foundry viz HTML into an Appen/Humain annotation CSV by copying all referenced assets into `s3://foundry-appen-humain-enterprise/to_annotate/<html_stem>/` and producing a CSV with `asset_url`, `reference_url[_N]`, `prompt` columns.

Usage: `/html-to-appen-csv-for-humain <html_url_or_s3_uri> [--local-out path] [--dry-run]`

Parse `$ARGUMENTS` to extract:
- **html**: foundry-aws-corp URL (e.g. `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>.html`) or `s3://<bucket>/<key>.html`
- Optional `--local-out <path>`: where to save the CSV locally (defaults to `/tmp/<stem>_appen.csv`)
- Optional `--dry-run`: plan + write CSV without copying to S3
- Optional overrides if auto-detection is wrong: `--reference-keys s,s2` / `--result-key g` / `--prompt-keys e`

## Credentials

AWS credentials live in `~/Downloads/creds.txt` (refresh from https://foundry-aws-corp.adobe.io/ → "Get Foundry Developer Credentials"):

```bash
source ~/Downloads/creds.txt
```

If the file is missing or the creds are expired, ask the user to refresh.

## What this does

1. Reads the viz HTML from S3 (accepts both the foundry-aws-corp.adobe.io URL and an `s3://` URI — they map 1:1).
2. Extracts the embedded `const DATA = [...]` array.
3. Auto-detects field roles by matching `<thead><th>` labels to the `d.X` keys referenced in the renderPage JS:
   - `source` / `input` / `reference` / `original` / `before` → **reference image**
   - `generated` / `result` / `output` / `edited` / `after` / `ai` → **result image** (the "asset")
   - any non-image field (e.g. `edit instruction`, `caption`, `prompt`) → **prompt**
4. Copies each unique image from its source bucket to:
   - `s3://foundry-appen-humain-enterprise/to_annotate/<stem>/references/<basename>` for references
   - `s3://foundry-appen-humain-enterprise/to_annotate/<stem>/generated/<basename>` for results
5. Writes a CSV:
   - Columns: `asset_url, reference_url[, reference_url_2, ...], prompt` (one `reference_url` if only one reference; numbered suffixes for two or more).
   - URLs are the **new** `s3://` URIs in the Humain bucket, not the original ones.
6. Uploads the CSV as `s3://foundry-appen-humain-enterprise/to_annotate/<stem>/annotations.csv` and keeps a local copy.

## Run it

```bash
source ~/Downloads/creds.txt
uv run --script ~/.claude/scripts/html_to_appen_csv.py <html_url_or_s3_uri> [--local-out path] [--dry-run]
```

The script prints diagnostics to stderr (auto-detected role mapping, copy progress, final paths). The last stdout line is the local CSV path.

## When auto-detection fails

If the stderr log shows the wrong role mapping (e.g. `Result: []` or the wrong key tagged as reference), re-run with explicit overrides:

```bash
uv run --script ~/.claude/scripts/html_to_appen_csv.py <url> \
  --reference-keys s,s2 --result-key g --prompt-keys e
```

Keys are the raw DATA keys (see the `Key order:` line in the stderr log).

## After it finishes

Report back to the user:
- Local CSV path
- Destination S3 folder URI
- Row count, unique asset count
- Detected role mapping (so they can sanity-check)
