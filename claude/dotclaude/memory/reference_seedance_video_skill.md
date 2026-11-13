---
name: reference_seedance_video_skill
description: /generate-video-fal-seedance skill — Seedance 2.5 video gen via fal.ai; fal key location + the 5 hard API rules
metadata: 
  node_type: memory
  type: reference
  originSessionId: 988e6174-d494-4ea5-a025-8678b58141b2
  modified: 2026-08-22T21:09:38.541Z
---

`/generate-video-fal-seedance` generates video with Seedance 2.5 on fal.ai (t2v / i2v / ref modes).
Backed by `hs_scripts/claude/dotclaude/scripts/seedance_video.py` (self-contained CLI, no THD budget
ledger). Distilled from Adobe-Firefly `THD_Proj:.claude/skills/seedance-video/SKILL.md` (branch
`zouyang/thd-tutorial-video`, pulled via `KINETOBOT_GITHUB_API_TOKEN` — that repo is private).

fal key on the colligo box lives in `hs_scripts/claude/thd/creds.txt` as `fal_api_key: <key>` (the
global-CLAUDE `~/.claude/hshariati/credentials.yaml` does NOT exist here). Resolver order:
FAL_KEY → FAL_ENV_FILE → --key-file → credentials.yaml → thd/creds.txt.

Five API rules that cost money to learn: R1 duration is `"auto"` or int 4–22 **as a string** (no 3s;
illegal durations get HTTP 200 then fail on fetch — preflight enforces it); R2 reference framing beats
the prompt; R3 real-person likeness → 422; R4 i2v ignores aspect_ratio; R5 preflight before spending.
720p ≈ $0.46/sec, 1080p is 2.25× for no gain. First-light test (t2v, 5s, 720p+audio) worked:
`hs_scripts/claude/thd/seedance_out/test_strawberry.mp4`. See [[reference_dotclaude_backup]].
