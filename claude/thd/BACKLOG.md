# Door-Lock Rewriter — Backlog

Deferred until (a) — polishing shot 0003 (measure the backset) — is done.

## (b) Build the rewriter pipeline
Generalize the THD composer (`scripts/brand_video/shotlist.py`: clause tables + `compose()`/`write_prompt()`)
into an article → video agent:
- article step → shot plan (beats, scene, camera, talent, entry)
- auto-produce references: person-free plates (nano-banana paint-out) and/or ordered beat keyframes
- compose the prompt in the THD 5-line register + vendor `@ImageN` keyframe roles
- generate via Seedance (reference-to-video with ordered keyframes for beat action)
- continuity lock (verbatim room/light/wardrobe clause + shared room reference) across shots in a film

## (c) Fold the THD register into `seedance_video`
Add the composer vocabularies so every shot is built THD-style by default:
- `SHOT_LINE`, `CAMERA_LINE`, `TALENT_LINE`, `ENTRY_LINE` (mid_action / full_arc / hand_absent_both_ends /
  from_still), `LOOK`, `NEG` — from `shotlist.py`
- a `compose()` helper producing the fixed 5-line order (subject+beats / shot+camera / talent+entry / look+neg)
- optional `@ImageN` keyframe-role emitter for ordered multi-keyframe shots (verified in round 6)
