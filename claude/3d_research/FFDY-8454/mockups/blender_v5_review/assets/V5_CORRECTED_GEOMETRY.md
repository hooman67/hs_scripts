# V5 — Corrected Geometry and Simplified Motion

As of: 2026-09-23

## Outcome

The new versioned file is:

`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v5_corrected_geometry_simplified_motion.blend`

It preserves Hooman's original source file. Frame 324—the last completely
assembled frame before the whole-cabinet stand-up—is treated as the
authoritative fitted state.

## Evidence-based corrections

`VERIFIED` from the authored source keyframes:

| Component | Late source correction | V5 correction |
|---|---:|---|
| `CABINET_04_TOP_WALL` | scale `(0.92, 1.08, 1.00)` at frame 278 | baked into mesh from frame 1; object scale remains `(1,1,1)` |
| `CABINET_05_RIGHT_BOARD_LARGE` | Y scale `1.18` at frame 278 | baked into mesh from frame 1; object scale remains `(1,1,1)` |
| `CABINET_06_RIGHT_BOARD_SMALL` | Y scale `1.25` at frame 324 | baked into mesh from frame 1; object scale remains `(1,1,1)` |

The corrected dimensions therefore never animate. All six components remain
rigid, and all object-scale axes remain locked.

`ASSUMED`, based on when the corrections occur:

- The top-wall position nudge at frame 278 was a fit correction after that wall
  had already been installed. V5 moves it to the wall's frame-192 installation
  endpoint and holds it there.
- The larger narrow-board position nudge at frame 278 was likewise a fit
  correction. V5 makes frame 264 its corrected installed endpoint and holds it
  there.

`USER-CONFIRMED`:

- The larger narrow board is front/back motion-equivalent. V5 removes its
  180-degree X roll and compensates its Z path by 0.049 m, so the installed slab
  occupies the same world-space bounds without an unnecessary flip.

## Preserved uncertainty

The front-frame/door component has a separate relative 180-degree X rotation
during frames 324–348 while `Cabinet_master` stands up the whole cabinet. This
may encode which door face is outward. It was preserved rather than guessed
away. It should be reviewed separately if the goal becomes a perfectly rigid
whole-cabinet stand-up.

The model is still a storyboard-derived proxy, not CAD. These changes preserve
Hooman's fitted result; they do not establish manufacturer-accurate dimensions.

## Validation

Blender 5.2.2 LTS validation passes all checks:

- all scale keys equal `1.0`;
- all six components have locked scale;
- the larger narrow board has no X-rotation keys;
- the top wall stays fixed after frame 192;
- the larger narrow board stays fixed after frame 264;
- every component's world-space bounds at frames 324 and 348 exactly match the
  original file within `2e-5` Blender units; and
- every frame-1 component remains on or above the assembly mat.

Evidence:

- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/rig_validation_v5_corrected_geometry.json`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/hooman_motion_source_animation.json`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/validation/v5_animation_states.json`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/v5_geometry_evidence/old_new_contact_sheet.png`
- `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/renders/v5_geometry_evidence/v5_large_board_no_flip.mp4`

## Reproduction

- Inspection:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/inspect_blend_animation.py`
- Versioned transformation:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/create_corrected_geometry_v5.py`
- Validation:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/validate_corrected_geometry_v5.py`
- Evidence rendering:
  `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/render_v5_geometry_evidence.py`
