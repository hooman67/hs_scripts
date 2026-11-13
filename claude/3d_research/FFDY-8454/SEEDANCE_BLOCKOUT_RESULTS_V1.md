# Seedance blockout experiment — v1 results

Date: 2026-09-23

## Question

Can a user-authored Blender animation serve as a motion specification for Seedance, and is it better to generate each shot separately or give Seedance all ordered references and let it choose the cuts?

## Inputs

- Authored Blender file: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend`
- Seven rendered Blender blockout clips covering storyboard shots 2, 4, 5, 6, 7A, 7B, and 8
- Existing storyboard appearance plates, with people removed from the model inputs
- A shared text description of the same couple in every call
- Existing shot 3/3A was intentionally retained rather than regenerated

The apparent `324–248` frame range for shot 8 was treated as `324–348`. The authored Blender file contains the stand-up motion through frame 348.

## Runs

Eight Seedance 2.5 jobs completed successfully:

| Run | Output duration | Purpose |
|---|---:|---|
| Shot 2 / 1A | 4.042 s | First broad side-panel lift |
| Shot 4 | 4.042 s | Opposite broad side-panel lift |
| Shot 5 | 4.042 s | Perpendicular cabinet wall installation |
| Shot 6 | 4.042 s | Small close/press motion |
| Shot 7A | 4.042 s | Larger narrow-board installation |
| Shot 7B | 4.042 s | Smaller narrow-board installation |
| Shot 8 | 4.042 s | Stand up the assembled cabinet |
| Combined auto-edit | 22.042 s | All ordered references in one request; Seedance chooses cuts and timing |

Estimated total cost was **$24.21** using the preflight pricing estimate. This is not a provider invoice.

## Main result

The combined request produced **eight visual shots separated by seven detected cuts**, without explicit boundary timestamps in the prompt:

| Inferred segment | Detected range | Intended action |
|---:|---:|---|
| 1 | 0.000–2.083 s | First side lift |
| 2 | 2.083–4.333 s | Connector close-up |
| 3 | 4.333–6.958 s | Opposite side lift |
| 4 | 6.958–9.625 s | Perpendicular wall installation |
| 5 | 9.625–11.958 s | Wall press/connection |
| 6 | 11.958–14.333 s | Larger narrow board |
| 7 | 14.333–16.208 s | Smaller narrow board |
| 8 | 16.208–22.042 s | Cabinet stand-up |

In this trial, the inferred edit structure matched the expected eight-stage sequence unusually well. This is promising evidence for an easier workflow, but it is a single sample and should not yet be treated as a reliable general capability.

## Visual assessment

- **Shot 8 is the strongest result.** The whole cabinet behaves like one rigid assembly, hands visibly interact with it, and the stand-up action is clear.
- **Shots 7A and 7B are readable.** Seedance distinguishes the two narrow-board placements and supplies plausible hand interaction.
- **Shots 4 and 5 generally follow the authored motion.** Shot 5 also interprets the relocation of the two loose boards as a second person's action.
- **Shot 2 captures the lift but not the exact final seated state.** It ends with the panel raised/held rather than conclusively installed.
- **Shot 6 is the weakest motion test.** Its Blender displacement is so small that the result looks nearly static. It preserves the subtle motion, but that makes success hard to judge.
- Character appearance is reasonably consistent across separate calls because the same description and room context were reused, but the people are not pixel-identical.
- Cabinet topology and connector details drift. The videos communicate action better than exact six-part product geometry.
- The combined video preserves the order and edit structure, but it has more risk of temporary duplicate/extra-looking panels and state discontinuity at cuts than the isolated-shot runs.

## Current conclusion

The best workflow suggested by this first experiment is **hybrid**:

1. The user authors one continuous motion in Blender.
2. Render ordered motion references from that timeline.
3. First ask Seedance for one combined auto-edit, allowing it to choose natural cuts and timing.
4. Review motion fidelity and cabinet state at each inferred cut.
5. Regenerate only failed segments as controlled per-shot calls, then edit those replacements into the sequence.

This preserves the low-friction advantage of the combined mode while retaining the retry precision of per-shot generation.

## Next high-value tests

1. Re-render shot 6 with the same start/end states but 2–3× larger, slower visible displacement, then compare whether Seedance follows the intended direction more legibly.
2. Repeat the combined request with one additional seed to measure whether the eight-shot boundary behavior is stable rather than accidental.
3. Score combined versus per-shot outputs on: action direction, final part pose, part count/topology, hand contact, character continuity, and edit continuity.

No additional paid calls were made beyond the eight authorized jobs.

## Stage 7 / Shot 7B minimal retry v3 — 2026-09-24

- Goal: prevent the man from touching the already-installed larger board while installing the final smaller narrow board.
- Inputs sent to Seedance: the exact Shot 7B Blender blockout video, one appearance image (`S6a_box_plate.png`), and the submitted prompt/settings. No contact sheet was sent to the model.
- Prompt strategy: describe only the required action and exclusion; let the blockout define the detailed motion.
- Result: the smaller loose board is installed and the larger installed board remains untouched. The simplified instruction resolves the specific v2 failure in this sample.
- Output: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/seedance_results/blockout_v1/shot07B_minimal_v3/shot07B_minimal_v3.mp4`
- Estimated incremental cost: **$1.64** (not a provider invoice).

## Stage 7 / Shot 7B v4C narrower retry — 2026-09-24

- Base: `shot07B_identity_v4c`; exact same blockout, appearance image, settings, and prompt structure.
- Only prompt change: `approximately one-third` became `approximately one-sixth`, with `and stays that thin throughout` added.
- Result: the moving strip is visibly narrower than v4C while preserving its smooth, direct installation motion.
- Output: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/seedance_results/blockout_v1/shot07B_identity_v4c_narrow_v2/shot07B_identity_v4c_narrow_v2.mp4`
- Estimated incremental cost: **$1.64** (not a provider invoice).
- The failed `shot07B_broad_face_v5` card was removed from the review gallery at Hooman's request. Its source files remain on disk for recoverability.

## Final shot-by-shot cut — 2026-09-24

- Eleven approved clips were assembled in Hooman's exact requested order using full-clip straight cuts.
- Delivery format: H.264, 1920×1080, 24 fps, yuv420p, no audio, browser fast-start.
- Final duration: **54.462 seconds**.
- Output: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.mp4`
- Ordered input manifest: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/final_cuts/final_cut_shot_by_shot_v1.inputs.json`
- Reproduction script: `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/assemble_final_cut_shot_by_shot.py`
