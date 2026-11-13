# FFDY-7304 — shot-by-shot comparison vs the real THD spot

Goal: recreate the real 67s THD spot (Brightcove 6384961806112) shot by shot, from **storyboard assets only**
(no frames/clips from the target video — that's cheating). Web reference images / tool-motion videos are OK.
For each shot: generate → compare to the target shot → find gaps → iterate until no major gaps → move on.

Target segmented into 22 shots (`reference/mid/sNN.jpg`, contact sheet `reference/contact_sheet.jpg`).
We are NOT bound to identical timing/pacing, but should be close.

## Target shot map (target shot → meaning → our source storyboard asset)
| Tgt | ~time | What it shows | Our beat / source (storyboard only) |
|---|---|---|---|
| S01 | 0–12.2 | Establishing hero: finished sink+cabinet L, washer/dryer R, title overlay | image1 |
| S02 | 12.2–14 | Couple crouch to floor, begin assembly (wide) | 1A / image8 plate |
| S03 | 14–14.8 | Overhead, fitting base panels | 2A / image11 plate |
| S04 | 14.8–15.6 | Overhead CU hands + panel | 2A |
| S05 | 15.6–17 | Woman holds white panel up | 2A |
| S06 | 17–19.9 | Overhead, box panels going up | 2A |
| S07 | 19.9–20.7 | CU cabinet corner + hinges | assembly detail |
| S08 | 20.7–21.9 | Couple slide side panel on | 2A |
| S09 | 21.9–23.5 | Overhead placing panel in box | 2A |
| S10 | 23.5–24.4 | ECU hand pressing panel edge | 3A click |
| S11 | 24.4–25.1 | Couple with box + panel | 2A |
| S12 | 25.1–26 | ECU orange click connector engaging | 3A / image12-14 |
| S13 | 26–26.8 | Man aligns panel top edge | 2A |
| S14 | 26.8–28 | ECU hand on panel edge/connector | 3A |
| S15 | 28–30.9 | Couple place stainless basin + "Drain Kit" SUPER | 4B / image15 plate |
| S16 | 30.9–32.2 | ECU hand on sink deck/rim | 5A / image16 |
| S17 | 32.2–36.8 | Drain strainer macro + pull-down faucet | 5A + drain (image18) |
| S18 | 36.8–49.3 | **White Oak color-variant** establishing (color b-roll) | 1B (colors) — needs synth |
| S19 | 49.3–51.1 | CU cabinet + brushed-nickel pulls | 6A / image20 |
| S20 | 51.1–53.8 | Stainless sink + white cabinet beauty | hero / image22 |
| S21 | 53.8–55.4 | Hand turns on pull-down faucet | 8A/5A / image19 |
| S22 | 55.4–67.7 | Final hero + GLACIER BAY/CLICKREADY end-card | 8B / image1 + endcard (post) |

Note: the real spot recast talent (red-haired woman + younger dark-haired man). We keep our invented
consistent couple (couple_bible.md) — identity need not match the target.

---

## Shot log
(iterations recorded below as we go)

### S01 — establishing hero  ✅ MATCHED (v2)
- Source: storyboard `image1` (i2v). Target: near-static wide hero, title overlay (post).
- v1: push-in TOO aggressive → ended on a tight faucet CU, lost the hero framing. GAP: camera move too strong.
- v2 FIX: "locked-off tripod, camera does not move, hold full wide framing." → holds the establishing
  framing the whole shot; composition/subject/lighting match the target. Only minor: ours slightly tighter
  than target (inherent to image1's crop). No major gap → move on.
- LESSON: for establishing/beauty shots, explicitly say "locked-off tripod, camera does NOT move" — Seedance
  over-zooms on a generic "push-in."

### Coverage of the assembly + feature shots by our EXISTING gens
Many target shots map to shots we already generated (v1). Rather than regenerate, compare + iterate only on
gaps:
- S02–S06, S08–S09, S11, S13 (assembly, couple + panels) ← our **1A**, **2A**
- S07, S10, S12, S14 (ECU click connector / panel edge) ← our **3A**
- S15 (basin placement) ← our **4B**
- S16, S20, S21 (sink deck / beauty / faucet-on) ← our **5A**, **8A**
- S17 (drain strainer macro) ← NEW (storyboard image18) — we lack a drain shot
- S18 (White Oak color variant establishing) ← NEW (1B color b-roll) — we skipped; needs synthesis
- S19 (hardware) ← our **6A**
- S22 (final hero + endcard) ← our **8B** + image1 + endcard (post)

### S17 — drain strainer macro  ✅ MATCHED (v1)
- Source: storyboard `image18` (i2v). Ours matches the target's drain-strainer macro (brushed steel basin,
  centered round drain + grid strainer). Target S17 is a split quick shot (drain + a hand on the faucet);
  the faucet half is covered by our 5A/8A. No major gap.

### S18 — White Oak color-variant establishing  ✅ MATCHED (v1)
- Source: nano-recolored `image1` → warm White Oak wood-grain cabinet (kept sink/faucet/room/washer identical),
  then locked-off i2v hold. Matches the target's "White Oak" establishing (composition, finish, hold). Ours
  slightly tighter framing (inherent to image1). No major gap.
- LESSON: color variants = recolor the hero still with nano (change ONLY the finish), then the same
  locked-off establishing recipe as S01.

### Existing shots vs their target counterparts
Compared our v1 gens (generated fresh from storyboard, never from the target) to the matching target shots:
- 1A/2A (couple assembling), 3A (connector), 4B (basin), 5A/8A (faucet), 6A (hardware) — actions + subjects
  match their targets; couple stays consistent. Main residual gap = **PACING**: our shots are ~5s slow beats
  vs the target's fast <1–2s cuts. Fix in the re-cut (trim each shot), not by regenerating.

### Re-cut to match pacing
`assemble_v2.py` — shots in the target's ORDER, each trimmed to ~2–3s (hero/establishing longer) so the cut
reads at the target's fast montage tempo. No new gens; uses S01/S17/S18 + the existing shots.
