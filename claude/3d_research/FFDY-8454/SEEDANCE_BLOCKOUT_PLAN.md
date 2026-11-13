# Blender Blockout to Seedance Plan

## Source

Animated Blender file:
`/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend`

The saved animation has keys through frame 348 at 24 fps. The originally stated final range
`324-248` is treated as `324-348`, based on the authored `Cabinet_master` keys and visible stand-up
motion.

## Shot map

| Gallery tab | Blender range | Source duration | Seedance treatment |
|---|---:|---:|---|
| Shot 2 · 1A | 1-48 | 2.0 s | Stretch/pad to a clear 4 s blockout |
| Shot 3 · 3A | existing gallery result | — | Reuse; no new generation |
| Shot 4 | 48-96 | 2.0 s | Stretch/pad to 4 s |
| Shot 5 | 96-192 | 4.0 s | Keep 4 s; review the narrow-board relocation at 120-144 |
| Shot 6 | 192-216 | 1.0 s | First experiment; stretch/pad to 4 s |
| Shot 7A | 216-278 | 2.6 s | Large narrow board installation; stretch/pad to 4 s |
| Shot 7B | 278-324 | 1.9 s | Small narrow board installation; stretch/pad to 4 s |
| Shot 8 | 324-348 | 1.0 s | Stretch/pad to 4 s and use a wider shot-specific camera |

Shot 7 is split because frames 216-278 and 278-324 contain two distinct component installations.
One state change per request gives Seedance a clearer motion target.

## Input roles for every new Seedance request

- `@Video1`: person-free Blender coarse blockout. It controls only component motion paths, relative
  positions, action order, camera position, and pacing. Its proxy materials and blank environment
  must not carry into the result.
- `@Image1`: person-free photoreal plate. It controls cabinet structure/materials and laundry-room
  appearance, but not motion.
- Text continuity lock: use the byte-identical couple and room clause from
  `/home/colligo/hs_scripts/claude/thd/FFDY-7304/couple_bible.md`.
- People and hands are generated, not supplied in a photoreal reference, because Seedance 2.5 rejects
  photoreal human likenesses in input images and videos.

## First paid experiment: Shot 6

- Motion source: frames 192-216.
- Appearance source:
  `/home/colligo/THD_laundry_sink_storyboard/prep/S6a_box_plate.png`.
- Output: Seedance 2.5 reference-to-video, 4 seconds, 720p, 16:9, audio off.
- No request is submitted until Hooman explicitly approves the paid call.

## Prompt draft for Shot 6

【Generation Goal】
Generate a photoreal continuation of the cabinet assembly. The woman uses both hands to press the two
long white side walls slightly inward so the cabinet locks squarely around the installed panel, while
the man stabilizes the cabinet.

【Reference Asset Roles】
@Video1 is a coarse-blockout reference. Use it only for the small inward motion of the two long side
walls, the fixed cabinet base, component blocking, action timing, and static camera; do not adopt its
proxy geometry, simplified materials, empty scene, or lack of people.
@Image1 defines the white cabinet materials, orange CLICKREADY connectors, dark work mat, light tile
floor, and bright laundry-room appearance; do not change the motion defined by @Video1.

【Subjects and Relationships】
The woman kneels at the near edge with her left hand on the left long side wall and her right hand on
the right long side wall. The man kneels opposite and keeps the cabinet stable. The base, front frame,
installed end wall, and loose pieces remain stationary.
The two people are the SAME throughout: a woman in her early 30s with shoulder-length dark-brown hair in
a plain cream knit sweater and blue jeans, and a man in his early 50s with short salt-and-pepper grey hair
in a plain light-blue polo and blue jeans. Bright modern laundry room, grey wainscoting, light tile floor,
open wood shelves, dark front-load washer/dryer. Plain clothing, no text or logos.

【Event Script】
At the start, the cabinet rests flat on the mat with the two long side walls almost aligned. Following
@Video1, the woman presses both side walls inward by only a small amount while the cabinet base and other
parts stay fixed. Her hands remain in physical contact with the moving walls. At the end, both walls are
square and stationary and the cabinet remains in the same place on the mat.

【Maintain Consistency】
Keep the same two people, cabinet component count, white panels, orange connectors, room layout, camera
axis, and physical hand-to-panel contact throughout. Preserve rigid panel dimensions; do not bend,
duplicate, collapse, or broadly swing the walls.

