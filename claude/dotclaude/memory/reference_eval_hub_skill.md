---
name: reference-eval-hub-skill
description: "/eval_hub_upload skill — uploads prompts+images to Adobe Evaluation Hub, returns a run ID; supports HTML viz, S3 prefix + dual prompts, or pre-staged dirs."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d7506a15-d978-4278-8d36-88190cc25743
---

`/eval_hub_upload` uploads a generation to Adobe's **Evaluation Hub**.

- Skill: `~/.claude/commands/eval_hub_upload.md`
- Script: `~/.claude/scripts/eval_hub_upload.py`
- Asset-viewer URL pattern: `https://evaluation-hub.adobe.io/asset-viewer?run_ids=<run_id>`
- API key default: `humain_eval_upload` (env: `EVAL_SERVICE_API_KEY`). The `eval_service_common` S3Uploader handles its own upload auth via this key — it does NOT need AWS creds.
- AWS creds (only for reading the *source* S3 in modes A/B/D): prefer the `/aws-creds` skill → `source ~/.claude/hshariati/aws_creds.env` then pass `--creds /dev/null` (script falls back to env). `~/Downloads/creds.txt` still works if it has `aws_access_key_id=`.
- Wheel: `eval_service_common` from Adobe artifactory, injected via `uv --with` using `ARTIFACTORY_UW2_API_TOKEN`

Expanded/rewritten prompt handling: `original` → `PromptInput.prompt`; `expanded` → `Asset.metadata.prompt` (set per-variant, so each seed can carry its own rewrite). Eval Hub renders metadata.prompt as a separate field. (Earlier versions concatenated them with a `*`-separator into one prompt field — superseded.)

Four input modes:

- **A** `--html <foundry-aws-corp URL or s3://...index.html>` — old `<td class="prompt">` table viz
- **B** `--source-s3 s3://bucket/prefix/ --prompts-source <txt|json> [--expanded-prompts-source <txt|json>] [--asset-ext jpg]` — modern training_logs/data.json viewers; row{i}_img{j} naming
- **C** `--prompts-file --asset-dir [--expanded-prompts-source]` — pre-staged locally; row{i}_img{j} naming
- **D** `--results-csv <path|s3> --images-s3 s3://.../images/ [--status-ok done]` — `results.csv` from the `/generate-from-endpoint` skill. Columns: prompt_id, original_prompt, rewritten_prompt, image_filename, status. Each done row = one asset with its OWN rewritten prompt; failed rows skipped; prompt_id mapped to 0-based item index. Image filenames kept as-is (e.g. `prompt{i}_seed{N}.png`).

Other useful flags: `--num-prompts N` (0 = all), `--num-variations K` (sets num_of_variations; caps img columns in A/B), `--parallel 24` for S3 download threads.

Internally all modes build a unified `AssetSpec` manifest (local_path, item_index, prompt, expanded). Modes A/B/C use `row{i}_img{j}` naming; mode D keeps original filenames.

See [[feedback-eval-hub-upload-fields]] for the five fields to confirm with the user before each invocation.
