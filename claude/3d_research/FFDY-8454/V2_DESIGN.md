# V2 Full-Assembly Rig Design

## Scope

The rig contains exactly six storyboard-inferred cabinet components:

1. Front frame and attached doors.
2. Left side panel.
3. Right side panel.
4. Bottom panel.
5. Wide rail.
6. Narrow rail.

The sink, faucet, loose plumbing hardware, people, and hands are outside v2.

## User authority

The rig does not encode an authoritative assembly order or duration. It includes a clearly marked example sequence only so every control can be exercised immediately.

Each component has two independent control layers:

- `PROGRESS_<component>.install_progress`: a constrained 0–1 baseline between its flat layout pose and installed pose.
- `MOVE_ROTATE_<component>`: a visible cube handle that accepts arbitrary location and rotation keyframes, additively layered over the baseline.

This means the user chooses:

- Which component moves first.
- When it starts and ends.
- How high it is lifted.
- Its route through space.
- Its intermediate rotations.
- Whether the movement pauses or changes speed.

## Hands

“Hands automatically follow” would mean attaching a hand rig to whichever component is moving. That would introduce automatic behavior and another motion-authoring problem. Because the immediate question is whether the six cabinet parts can be authored comfortably, v2 intentionally excludes hands. They can be added as independently editable controls after the cabinet workflow is validated.

## Geometry caveat

The six-part topology is inferred from `/home/colligo/hs_scripts/claude/3d_research/FFDY-8454/references/storyboard_all_pieces_image7.jpeg`. It is a motion proxy, not CAD, and the exact functions of the two narrow pieces remain provisional.
