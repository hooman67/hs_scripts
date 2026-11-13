---
description: Build a prompt × seed comparison HTML from an eval-hub-style CSV (public image URLs, no download).
---

Build a self-contained HTML that lays out every **seed/variant of each prompt side by side**, with the prompt text above, from a CSV that has an image-URL column and a prompt column. Images are referenced by their (public) URLs, so the page renders anywhere with **no auth and no download** — ideal for eyeballing an Eval Hub run whose assets live on the public `clio-web-app` S3 bucket.

## When to use

- You have an Eval Hub run (or any generation) whose images are public and named `prompt<N>_seed<S>.png`, and a CSV listing them (e.g. a Humain study export with `AssetURL, Asset, Prompt, ...`).
- You want a quick visual seed-vs-seed comparison per prompt without pulling the images down.

The runId in an Eval Hub asset-viewer URL is usually the **S3 prefix** on `clio-web-app`, and those objects are public (GET works, but `ListBucket` is denied) — so the CSV is how you get the filename list. This skill turns that CSV into the gallery.

## How it works

Script: `~/.claude/scripts/eval_seed_gallery.py` (PEP 723, no deps). It:
1. Reads the CSV, dedupes by image URL.
2. Parses `prompt<N>_seed<S>` from the filename (the `Asset` column, else the URL) → groups by **prompt number**, labels each image `seed <S>`, sorts prompts numerically and seeds within a prompt.
   - Fallback: if that pattern isn't present, it groups by **prompt text** and labels images by filename.
3. Emits one card per prompt: prompt text on top, all seeds side by side (click for full-res), dark theme.

## Run it

```bash
uv run --script ~/.claude/scripts/eval_seed_gallery.py --csv <study.csv>
# → ~/Downloads/<csvname>_seed_gallery.html
```

Flags:
- `--csv` (required) — CSV with an image-URL column and a prompt column.
- `--out` — output path (default `~/Downloads/<csvname>_seed_gallery.html`).
- `--url-col` (default `AssetURL`), `--prompt-col` (default `Prompt`), `--asset-col` (default `Asset`, used to parse `prompt<N>_seed<S>`; falls back to the URL).
- `--limit N` — only the first N prompts (0 = all). Good for a quick 3-prompt smoke test first.
- `--title` — custom page title.

## Examples

```bash
# 3-prompt smoke test
uv run --script ~/.claude/scripts/eval_seed_gallery.py --csv ~/Downloads/Foundry_Humain_06232026(Study).csv --limit 3

# full run
uv run --script ~/.claude/scripts/eval_seed_gallery.py --csv ~/Downloads/Foundry_Humain_06232026(Study).csv --out ~/Downloads/humain_211_seeds.html

# a differently-shaped CSV (e.g. /generate-from-endpoint results.csv with a URL column)
uv run --script ~/.claude/scripts/eval_seed_gallery.py --csv results.csv --url-col image_url --prompt-col original_prompt --asset-col image_filename
```

## Notes

- Output is a **plain self-contained HTML** (inline CSS, no JS, no IMS auth) since it only references already-public image URLs — open it locally in a browser. If you later want it hosted behind `foundry-aws-corp.adobe.io`, add the IMS scaffolding and upload with `/render-s3-gallery` conventions.
- Related: `/eval_hub_upload` (uploads generations to Eval Hub); this skill is the lightweight "look at a run's images" counterpart.
