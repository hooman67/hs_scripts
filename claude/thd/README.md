# THD Article → Video Rewriter

Experiments + pipeline for recreating The Home Depot how-to videos from their articles, using
**Seedance 2.5** (video) and **nano-banana** (image edit) on fal.ai. Working example: *How to Install
a Door Lock*.

## Layout
- **`pipeline/`** — the rewriter engine (backlog b). `rewriter_pipeline.py` (source shot → R3-safe
  keyframes → composed prompt → generated shot), `PIPELINE.md` (how it works + the rules), `configs/`
  (one JSON per shot).
- **`gallery/`** — `build_gallery.py` renders `manifest.json` → a self-contained HTML gallery of every
  experiment round (inputs + prompts + outputs). `imsauth.js` = Adobe IMS auth for the S3 host.
- **`experiments/`** — the one-off driver scripts that produced each round (rounds 1–13, exp A–W),
  kept as a record of what was tried.
- **`creds.txt`** — fal key + Foundry AWS creds. **Git-ignored, never committed.** (`fal_api_key: …`)

## The skill
`/generate-video-fal-seedance` — Seedance 2.5 CLI, lives in `../dotclaude/scripts/seedance_video.py`
(+ `../dotclaude/commands/generate-video-fal-seedance.md`), symlinked into `~/.claude`.

## Learnings / memory
Durable findings are in the auto-memory (in-repo via symlink):
`../dotclaude/memory/project_thd_video_rewriter.md` (+ `reference_seedance_video_skill.md`,
`feedback_*`). That file is the canonical record of what works (R3 boundary, person-free plates,
ordered keyframes, split-role refs, body-cover keyframes, ~5s/beat, per-beat constraints).

## Media & gallery (not in the repo)
Videos/images (source shots, generated mp4s, keyframes, gallery assets) live on the working box at
`/home/colligo/THD_How_to_Install_a_Door_Lock/`. The live gallery (Foundry S3, Adobe SSO):
`https://foundry-aws-corp.adobe.io/asset/foundry-thd-enterprise-adobe-assets/video_rewriter/door_lock/gallery/index.html`

## Rebuild / run
```bash
# rebuild the gallery HTML from the manifest, then upload (needs Foundry AWS creds sourced):
python3 gallery/build_gallery.py
# recreate a shot with the pipeline:
python3 pipeline/rewriter_pipeline.py pipeline/configs/shot0007.json
```
