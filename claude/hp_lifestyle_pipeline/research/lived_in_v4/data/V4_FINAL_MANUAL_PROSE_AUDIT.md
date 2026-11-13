# V4 actual-prose audit: current 540

Audit date: 2026-10-26

## Scope and result

This audit reads the actual scene prose in the newest normalized record for all 18 authorized cases. It does not use model-reported `visual_signature` as ground truth. All 540 current candidates were manually reviewed; 690 candidate texts were read in total after including superseded replacement banks. No model calls, network generations, uploads, prompt edits, or changes to V3 artifacts were made.

The current 540 have no manually confirmed hard camera-budget, visible-device, camera/lens-instruction, material-wear, or excessive-dirt violations. All nine close-up banks stay within their zero- or one-prop ceilings and do not enlarge the crop with visible people or room fixtures. All nine wide banks stay within three independent local-prop slots after treating packet pages, ordinary container contents, crumbs, marks, and small homogeneous game-piece groups as state or one compact unit.

One accepted near-target guidance exception remains. In `22fdbf19f03d1a31__laptop_FrontRightWide` sample 003, nine candidates clearly omit the business-meeting/administrative paper family; the local prompt guidance asked for ten. Candidates p21, p22, and p24–p30 are the nine clear omissions. Candidate p23 retains a research note sheet and index cards, although library study is a visibly different activity from the source business meeting. Root accepted this bank for bounded image evaluation with the 9-of-10 limitation disclosed.

## Specificity compared with references

| Cohort | N | Median words | Median nonlighting concrete indicators | Surface + light formula |
|---|---:|---:|---:|---:|
| October authoritative guidance | 10 | 45.5 | 8 | 1/10 (10.0%) |
| Lifestyle workbook, column A only | 58 | 57.5 | 4 | 25/58 (43.1%) |
| V3 all candidates | 540 | 25 | 3 | 488/540 (90.4%) |
| V4 current candidates | 540 | 43 | 4 | 499/540 (92.4%) |
| V4 close-up | 270 | 37 | 2 | — |
| V4 wide | 270 | 49 | 6 | — |

V4 restores substantial visible specificity over V3 while respecting the same camera profiles. Its 43-word median approaches the October guidance's 45.5 words. Wide prompts reach a six-indicator median because their geometry permits related props and background anchors; close prompts use two indicators through material, localized use history, and light.

Lexical mid-use indicators occur in 167/540 current V4 texts (30.9%), compared with 130/540 V3 texts (24.1%). Consumption and pause cues rise from 35/540 in V3 (6.5%) to 126/540 in V4 (23.3%). This is the clearest measurable recovery of ordinary human-use detail. V4 still falls well below the October set's eight-indicator median, and its surface-plus-light sentence structure remains more repetitive than the references.

## Representative before/after evidence

The October guidance's laptop home-workspace example names an open notebook, spiral pad, loose papers, pens, half-finished coffee, relaxed curtains, a chair, overgrown plants, shelving, books, and familiar residential objects. It has 69 words and many independent objects, so it is a character reference rather than a feasible close-up inventory.

A representative selected V3 laptop close-up says: “A worn classroom preparation table in pale laminate, empty except for its soft scuffs, with calm daylight spread across the surface.” It has 21 words and relies on generic wear plus light.

A current V4 laptop close-up says: “A small stretch of charcoal laminate in a private focus room, recently wiped but still carrying a faint crescent where a mug once sat and fine sleeve polish along the working edge. Soft overhead light keeps the surface practical and businesslike.” It preserves the zero-prop crop while adding a recent reset, a localized drink trace, and sleeve polish. The mug is causal history, not a requested visible object.

A representative selected V3 printer wide says: “A busy shared office document area with a lightly worn laminate counter, a neat stack of everyday forms and a wrapped paper ream. A simple supply shelf and pinned team notice sit in soft overhead light.” Its character is mostly a room label, two paper objects, generic wear, and light.

A current V4 printer wide alternative says: “A meeting side table with a half-full water glass, a folded linen napkin, and a small bowl with a few wrapped mints. A soft upholstered chair sits behind, angled as if recently used. Diffuse overhead light catches the table’s satin veneer and one faint scuff near the edge.” It uses three coherent local-prop slots, one background anchor, object state, and arrangement without enlarging the shot.

## Camera and physical-feasibility findings

- Close-up ceiling: laptop close-up uses zero visible local props; printer close-up uses at most one. Causal phrases such as “where hands rest” and negative phrases such as “no loose objects” are not visible people or props.
- Wide ceiling: three independent local-prop slots. A cup plus coaster or saucer counts as two. A packet and its pages, a bowl and ordinary contents, or two tiny homogeneous tokens count as one compact unit unless the prose gives them separate spatial roles.
- Backgrounds: wide scenes use subordinate chairs, shelves, boards, curtains, partitions, or similar anchors. Close scenes do not add fixtures to simulate a larger room.
- Material behavior: writing impressions occur on wood, laminate, linoleum, or similarly plausible surfaces. Quartz, stone, and marble use wipe streaks, rings, sheen, or surface residue rather than pressure dents.
- Dirt and distress: art-room paint specks, clay dust, sawdust, a tiny sample-stone chip, and a slightly chipped coaster are context-appropriate handled-object or activity traces. None rises to severe dirt, damage, or neglect.
- Device and camera language: zero current candidates request visible phones, tablets, screens, computers, printers, or other computing hardware; zero add camera, lens, rendering, zoom, or crop instructions. “Fax cover sheet” names a document type and does not request fax hardware.

## Repetition and limitations

V4 is richer but remains highly templated. The lexical screen finds a material/surface-plus-light formula in 499/540 candidates (92.4%), compared with 488/540 V3 candidates (90.4%) and 1/10 October authoritative examples (10%). Wipe streaks, rubbed edges, uneven polish, scuffs, burnish, and softened corners recur frequently, especially in zero-prop close-ups.

The active prose screen finds paper/document language in 277/540 candidates, writing tools in 141/540, and food/drink/pause artifacts in 119/540. Source-relevant document banks naturally dominate their high-ranked candidates, while the broader alternatives introduce café pauses, game pieces, textile or ceramic samples, domestic drop zones, and breakfast traces. The accepted 22f wide bank reaches nine rather than ten clear non-paperwork alternatives.

Some feasible texts expose compliance logic rather than describing the scene directly, including “a clipped-looking report packet implied only by its squared page stack” and “North-facing daylight is suggested.” These are prose-quality limitations, not geometry failures.

Rule-based noun parsing is only a screen. It overcounts words inside document packets, treats causal “hands rest” as a visible person, and can pair a ceramic mug elsewhere in a sentence with plausible writing impressions in wood. Manual judgments in `v4_manual_prose_review.json` resolve those flags. Image-level cue survival, product salience, occlusion, and whether subtle marks render visibly remain untested by this prose-only audit.

## Provenance

- Current V4 manifest: SHA-256 `c1f7007cf68593f6a0e4e7f02464bdbe05db3175243383c029501d1527f38258`
- Current V4 system prompt from manifest: SHA-256 `83cc51a0b139f62a176982f60082070c1686fef3bd780a9e16cf95459178b349`
- Camera profiles: SHA-256 `59b5e2b322dcd74c21432e772f3dd11513f71c182f6114b99b15e009dbeea68b`
- October guidance DOCX: SHA-256 `1f1605f034f581e03679d101fddd9cd52f00601b75ba2a9ec64783206fb78293`
- Lifestyle workbook: SHA-256 `7bf4c6ad2b6ce324fb3c9d1d9d52846411529e29f1b1765d1f4e8bff7ded980a`
- V3 all 540: SHA-256 `3db71a433357edcc2fd0ef0804c9584355ff3e13d6eff98afc983f57a7138cc1`
- V3 selected 108: SHA-256 `1fd643995e57e509dc5d7e56eb7638ca5437a6f763ceff0e60e5ccb6dafed641`
- Current replacement raw records:
  - 22f laptop wide sample 003: `385ec8a9a8d5d8197580fdb26410c356aa2b78af4ff1a16d065014e5bd54891c`
  - 943f printer wide sample 002: `d0ceca4470dded8c6ab3755252c421d4a6bddf553c6bc3b5766edf1b88a43551`
  - d60 laptop wide sample 003: `c2731ccdf0cbd1a00e78a079cc18d0ce4db541ed6c2fd95ed6f081a4a9a414b1`

The machine-readable actual-prose audit records every current normalized output and matching validation raw record with size and SHA-256. The separate manual review records current and superseded replacement findings so candidate IDs remain tied to their source sample.
