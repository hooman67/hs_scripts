---
description: Upload a generation (prompts + images) to the Adobe Evaluation Hub and get a run ID back.
---

Upload a generation to the Adobe **Evaluation Hub**. Registers a generation (`eval_set`, `model_id`, …), uploads images to S3 keyed by the returned `run_id`, then registers each image with its prompt. Prints the run ID and asset-viewer URL.

## ALWAYS ask the user for these five fields first

Before running anything, use `AskUserQuestion` (or just plain-text ask) to confirm all five of these — even if `$ARGUMENTS` partially specifies them. Don't guess defaults.

| Field | Flag | Example |
|---|---|---|
| Eval set name | `--eval-set` | `humain_t2i_gpt_592` |
| Eval set version | `--version` | `1.0` |
| Model id | `--model-id` | `h06_v13_iter_1026000_expanded_prompts` |
| Created by | `--created-by` | `hshariati` |
| Number of variations | `--num-variations` | `2` |

After the user confirms, echo the five values back so they can spot typos, then proceed.

## Input modes (pick whichever fits the data)

**Mode A — old `<td class="prompt">` viz HTML:**
```
--html <foundry-aws-corp URL or s3://...index.html>
```
Parses prompts + image filenames straight from the HTML, downloads images from the same prefix.

**Mode B — S3 prefix with `row{i}_img{j}` files** (modern `data.json`-driven viewers, training_logs):
```
--source-s3 s3://<bucket>/<prefix>/
--prompts-source <path-or-s3-uri>          # .txt (one per line) or .json (list[str] or list[{prompt: ...}])
[--expanded-prompts-source <path-or-s3-uri>]  # optional; paired by index → dual-prompt format
[--asset-ext jpg]                             # extension under the prefix (default jpg)
```
When `--expanded-prompts-source` is provided:
- `PromptInput.prompt` (the user-facing prompt) ← original
- `Asset.metadata.prompt` ← expanded (set on each variant/seed independently)

Eval Hub renders `metadata.prompt` as a separate field in the viewer, so this keeps the user prompt and expanded prompt cleanly separated instead of concatenating them into one long string.

The two prompt sources must have the same length and align by index.

**Mode C — pre-staged locally:**
```
--prompts-file path/prompts.txt
--asset-dir path/with/row{i}_img{j}.<ext>
[--expanded-prompts-source path]   # optional; paired by index
```

**Mode D — `results.csv` from the `/generate-from-endpoint` skill:**
```
--results-csv <path-or-s3-uri>/results.csv
--images-s3 s3://<bucket>/<prefix>/images/
[--status-ok done]                 # comma-separated statuses to upload (default: done)
```
Reads CSV columns `prompt_id, original_prompt, rewritten_prompt, image_filename, status`. Each `done` row becomes its own asset, so **each seed/variant keeps its own `rewritten_prompt`** (the endpoint rewrites per-generation, so the two seeds of a prompt usually differ). `original_prompt` → `PromptInput.prompt`; `rewritten_prompt` → `Asset.metadata.prompt`. Rows that failed (e.g. `prompt_unsafe`, `http_503`) are skipped automatically, so prompts with 0–2 successful images are all handled. `prompt_id` values are mapped to a 0-based contiguous `eval_set_item_id` index.

`--num-prompts N` caps how many prompts/items to process (default 0 = all). `--num-variations K` sets `num_of_variations` on the generation and (modes A/B) caps which `img0..img{K-1}` columns are taken.

## Credentials

- **EVAL_SERVICE_API_KEY** — upload API key. Default `humain_eval_upload`. Override via `--api-key` or env. (The `eval_service_common` S3Uploader manages its own upload auth via this key — it does not need AWS creds.)
- **AWS creds** (for reading the *source* S3 — modes A/B/D) — get fresh creds with the `/aws-creds` skill (`uv run --script ~/.claude/scripts/foundry_aws_creds.py`), then `source ~/.claude/hshariati/aws_creds.env` in the same shell command and pass `--creds /dev/null` so the script falls back to the sourced env. Alternatively point `--creds` at a `key=value` file containing `aws_access_key_id=…`.
- **ARTIFACTORY_UW2_API_TOKEN** — must be in shell env so `uv --with` can pull `eval_service_common` from Adobe artifactory.

## Run it

```bash
uv run \
  --with "eval_service_common @ https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/pypi-adobeshared-release/eval-service-common/1.3.10/eval_service_common-1.3.10-py3-none-any.whl" \
  --script ~/.claude/scripts/eval_hub_upload.py <args>
```

## Examples

Small smoke test (Mode A):
```
/eval_hub_upload --html https://foundry-aws-corp.adobe.io/asset/.../humain_prompts/index.html \
  --eval-set hs_test --model-id hs_test_model --num-prompts 3 --num-variations 2
```

Full Humain 592 run (Mode B, dual prompts):
```
/eval_hub_upload \
  --source-s3 s3://foundry-humain-default-adobe-assets/training_logs/.../assets/ \
  --prompts-source s3://foundry-humain-default-adobe-assets/eval/humain_rewrite_v13_gpt_merged_input_prompts.txt \
  --expanded-prompts-source s3://foundry-humain-default-adobe-assets/eval/humain_rewrite_v13_gpt_merged.json \
  --eval-set humain_t2i_gpt_592 --version 1.0 \
  --model-id h06_v13_iter_1026000_expanded_prompts \
  --created-by hshariati --num-variations 2
```

Humain 211 from a `/generate-from-endpoint` run (Mode D):
```
source ~/.claude/hshariati/aws_creds.env   # via /aws-creds skill
/eval_hub_upload \
  --results-csv s3://foundry-humain-default-adobe-assets/hs_results/<run>/results.csv \
  --images-s3   s3://foundry-humain-default-adobe-assets/hs_results/<run>/images/ \
  --creds /dev/null \
  --eval-set humain_t2i_gpt_211 --version 1.0 \
  --model-id h06_v13_iter_1026000_expanded_prompts \
  --created-by hshariati --num-variations 2
```

## After it finishes

Report back:
- **Run ID** (final two lines of output).
- Asset-viewer URL: `https://evaluation-hub.adobe.io/asset-viewer?run_ids=<run_id>`.
- Eval set, version, model id, prompt count, total assets uploaded.
- Local staging dir (so the user can inspect what was sent).
