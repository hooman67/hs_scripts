# How to Edit the v1 Rig

## Open it

```bash
/mnt/localssd/blender-poc/blender-5.2.2-linux-x64/blender /home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_motion_rig_v1.blend
```

The current host has no active desktop, so this command requires a desktop/VNC session or copying the `.blend` to a machine with a display.

## Change a motion

1. In the Outliner, select `CTRL_Master_Select_Me` in the `CONTROLS` collection.
2. Open Object Properties, then Custom Properties.
3. Scrub to a frame in the relevant timeline segment.
4. Change the corresponding 0–1 slider:
   - `end_panel_insert` for shot 5.
   - `side_top_spread` and `bottom_piece_insert` for shot 6.
   - `side_top_spread` and `lock_rail_drop` for shot 7.
5. Hover the edited slider and press `I` to insert a keyframe.
6. Play the segment with the Space bar.

The source animations are at frames 1–72, 90–162, and 180–252. The timeline markers switch to the close-up camera for shot 7.

## What is constrained

- Side-wall lower pivots do not translate.
- `side_top_spread=1` means 6 degrees outward per wall.
- The shot-5 end panel can only move on its vertical insertion path.
- The shot-6 bottom proxy can only move along its insertion axis.
- The shot-7 locking piece can only move vertically.

## Hands and references

- `HANDS_OPTIONAL` contains low-detail independent hand guides. Hide the collection if it distracts from product motion.
- `REFERENCES_STORYBOARD` contains the copied storyboard/sketch planes and never appears in renders.

## Rebuild and verify

```bash
/mnt/localssd/blender-poc/blender-5.2.2-linux-x64/blender --background --python /home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/build_laundry_sink_rig.py
/mnt/localssd/blender-poc/blender-5.2.2-linux-x64/blender --background /home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_motion_rig_v1.blend --python /home/colligo/hs_scripts/claude/3d_research/FFDY-8454/scripts/validate_rig.py
```
