# THD Article → Video Rewriter — Pipeline (backlog b)

Turns one source how-to **shot** into a Seedance recreation, encoding everything validated on shot 0003
(rounds 1–13). Engine: `rewriter_pipeline.py`. Video/image backends via `~/.claude/scripts/seedance_video.py`
(Seedance 2.5 + nano-banana on fal).

## The stages
1. **Analyze the shot** (human/LLM today; the article-driven auto-version is the remaining piece):
   decide the action, how many **beats** (~1 per distinct sub-action), what each beat shows, the framing,
   whether a person is present, the scene/hardware to preserve, the tool, and the clothing.
   Write it into a **config** (JSON) — see `configs/shot0007.json`.
2. **Extract keyframes** at the chosen beat timestamps.
3. **Build the references — pick a `method`** (config field; falls back to `person_mode`):
   - `cover_body` *(default)* — nano-banana removes head+face+torso but KEEPS the real hands + tool
     (natural hands), and strips baked-in step/TIP graphics. Keyframes stay at one consistent (source)
     scale, which lets the frame hold *and* the beats read.
   - `sketch` — convert each beat frame to a line **sketch** (ordered keyframes for geometry) + paint one
     frame's person out for a photoreal **appearance plate** (trailing ref). Prompt says "render photoreal,
     don't adopt the sketch look." Drives a shot from sketches + one style ref with **no exact source
     frames**; honors tape/tool geometry; includes an anti-"extra motion between beats" clause. (Rounds 14–17.)
   - `none` — frames used as-is (hands-only source, or no person).
4. **Compose the prompt** — vendor ordered-keyframe directives (`@Image1..N as keyframes in that order`,
   `Use @Image1 as the first frame — <beat>`, `Use @ImageN as the last frame — <beat>`) inside the THD
   register (subject/action → look → keep-scene → negatives). Optional per-beat `constraint` reins in drift.
5. **Generate** — reference-to-video, ordered keyframes, `duration ≈ 5 s × n_beats` (clamped 4–22).

## Rules baked in (measured)
- **R3:** a real person's face/head/torso in a reference → 422; hands/forearms are fine → cover the body, keep the hands.
- **Keyframe scale must be consistent** — don't mix a wide plate with tight beat crops (frame collapses or beats blur).
- **~5 s per beat** — 8 s was too short for 3 subtle beats.
- **Keyframes drive the visual; text can't add a pose the keyframe lacks**, but a per-beat text `constraint` fixes drift when the keyframe is right.
- **Negatives + plain clothing** are the THD brief (garbled wordmarks otherwise).
- Numerals/small text never render legibly — add real numbers/captions in post.
- **Lighter touch on the prompt.** To fix a residual artifact, add the SMALLEST clause and keep the rest
  verbatim; heavy all-caps multi-clause "instructions" (and thicker sketch lines) made shot 0003 WORSE, not
  better. Line weight of sketches is not a lever. If a small nudge doesn't fix it, change the keyframes /
  beat timestamps / plate — not a louder prompt. (Approved shot-0003 winner = `sketch` method, 16s, beat2
  "blade STOPS at the plate's near rim", + one short between-beats clause.)
- **cover_body needs CLEAN beat timestamps.** On busy two-handed frames the nano cover-body edit mangles
  the keyframe (drops a held object / hallucinates a wrong action). When a keyframe looks wrong, RE-TIME the
  beat to an unambiguous moment before editing the prompt (shot 0008: 0.98/3.8s → 0.5/2.9s fixed it).

## Run
```bash
python3 pipeline/rewriter_pipeline.py pipeline/configs/shot0007.json
```
Outputs into the config's `work_dir`: `raw/` (extracted frames), `kfN.png` (R3-safe keyframes),
`prompt.txt`, `gen/<id>.mp4` (+ `.json`/`.debug.json`). Review, then add to the gallery.

## Config schema (see configs/shot0007.json)
`id, source, work_dir, beats:[{t, desc, constraint?}], subject, scene_keep, clothing, tool,
framing, method (cover_body|sketch|none), person_mode, resolution`.

## Still TODO for full (b)
- Auto-decompose the **article** into a shot list (LLM) and auto-pick beat timestamps from the source video.
- **Assemble** shots into one film (conform/trim; continuity lock across shots — the byte-identical
  room/light/wardrobe clause + shared reference from the source skill).
- Identity consistency across longer clips (Seedance drifts).
