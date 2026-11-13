---
description: Generate a video from a prompt (and optional reference images) with Seedance 2.5 via fal.ai. Text-to-video, image-to-video, or reference-to-video.
---

Generate a video with **Seedance 2.5** on fal.ai. Backed by `~/.claude/scripts/seedance_video.py`
(distilled from the Adobe-Firefly `THD_Proj` `seedance-video` skill, 111 measured calls).

**Usage:** `/generate-video-fal-seedance <what to generate>` — or pass flags directly.

## What it does

1. Resolves the fal key (never printed): `FAL_KEY` env → `FAL_ENV_FILE` → `--key-file` →
   `~/.claude/hshariati/credentials.yaml` (`fal_api_key:`) → `~/hs_scripts/claude/thd/creds.txt`.
2. Preflights the request (duration/resolution/refs) **before** submitting, so an illegal call
   never spends.
3. Submits to fal's queue, polls to completion, downloads the mp4, and writes the exact prompt +
   full response next to it.

## How to run it

```bash
# Text-to-video (no reference)
python3 ~/.claude/scripts/seedance_video.py \
  --prompt "A single ripe strawberry falls into a glass of sparkling water. Close-up, static shot. Photoreal." \
  --mode t2v --duration 5 --resolution 720p --name my_shot --out ~/seedance_out

# Reference-to-video: keep a real product's identity (1-2 references is plenty)
python3 ~/.claude/scripts/seedance_video.py \
  --prompt "$(cat prompt.txt)" --mode ref \
  --image hero.jpg --image macro.jpg --duration 6 --name product_shot

# Image-to-video: animate a first frame (do NOT set --aspect; i2v ignores it)
python3 ~/.claude/scripts/seedance_video.py \
  --prompt "The tool turns slowly on a turntable, holding its exact shape." \
  --mode i2v --image seed.jpg --name turntable

# Verify the key resolves without spending anything
python3 ~/.claude/scripts/seedance_video.py --check
```

Flags: `--mode {t2v,i2v,ref}` · `--image` (repeatable) · `--duration` · `--resolution {480p,720p,1080p}`
· `--aspect` · `--audio/--no-audio` · `--prompt` / `--prompt-file` · `--name` · `--out` · `--key-file`.

Output (three files in `--out`): `<name>.mp4`, `<name>.json` (exact prompt + params + response),
`<name>.debug.json` (raw submit/status/result — the only thing that explains a failure).

## Five hard rules (each cost money to learn)

- **R1 — duration is `"auto"` or an integer 4–22 as a string. There is no 3s.** An illegal
  duration is *accepted* into the queue (HTTP 200) and rejected only on result fetch, after budget
  is spent. Generate at `max(4, want)` and trim in post — trimming is free. (Preflight enforces this.)
- **R2 — the seed/reference image's framing beats your prompt.** Need a macro or a wide shot? supply
  a reference that already has that framing.
- **R3 — any reference carrying a real person's likeness → `422 content_policy_violation`** (image
  *or* video). Use person-free references.
- **R4 — `i2v` silently ignores `aspect_ratio`** (returns the seed's aspect). Crop the seed instead;
  the script omits it on i2v automatically.
- **R5 — preflight before you spend.** The script checks duration/resolution/refs before submitting.

## Prompt recipe (5 lines, in order)

```
1  <who> <does what>, on <where>.
2  In order: <beat>; then <beat>; then <beat>.   ← only if the action has beats; NEVER more than 3
3  <shot size>. <camera technique>.
4  <how much of a person may appear>.
5  <look>. <keep the product identical>. <negatives>.
```

Notes: ✅ reliable camera techniques — `static`, `push_in`, `pull_back_reveal`, `handheld`, `pov`;
⚠️ fight it for `overhead`, `probe_lens`, `orbit_360`, `slow_motion`. `t2v` invents logos/text — for
product fidelity use `ref` with a real product still. Music/on-screen text are unreliable; do them in
post. Cost: 720p ≈ **$0.46/sec**; 1080p is 2.25× for no measured gain.

## Cross-reference

Full measured playbook (continuity locks, the 5-level judge, dead ends, the official ByteDance
`【】` template) lives in the source skill:
`Adobe-Firefly/THD_Proj:.claude/skills/seedance-video/SKILL.md` (branch `zouyang/thd-tutorial-video`).
For a multi-shot film or brand-safety gating, read that; this command is the general single-shot path.
