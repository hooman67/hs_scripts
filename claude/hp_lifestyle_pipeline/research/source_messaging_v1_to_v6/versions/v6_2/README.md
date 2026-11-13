# V6.2 writer: spatially coherent, phrase-diverse prompt banks

## Current surface-diversity revision — 2026-11-09

The active runtime is `v6.2-writer-runtime-r3-surface-recognition`. It supersedes the table-only printer and one-round-table laptop rules documented in the historical sections below. The old snapshots and their outputs remain unchanged.

- Every ten-prompt laptop bank contains at least two explicit round/circular primary tables, and every Café candidate uses one. Source-supported non-Café round tables are encouraged where plausible without ranking bonuses.
- Every printer bank contains at least three distinct furniture families and at least five non-table primary supports: substantial tables/worktables, freestanding storage cabinets, low credenzas/sideboards, fitted base cabinetry and countertops. All retain credible placement, stability and standing access. Extra background furniture still requires approval and counts toward repetition.
- `surfaces.py` extracts the first main supporting furniture in the opening sentence, preserves exact text offsets, and audits actual text rather than counting a round prop or background table. The application adds `primary_support` and bank audit metadata. End-user input and raw model schema are unchanged.
- Earlier C-Tech, source scoring, wall placement/population, phrase/prop diversity, text/face safety, and qualitative camera rules remain. No numeric prop quota is introduced.
- GPT-5.5 remains the generation model. The updated provider uses the policy-aware Foundry gateway Azure client after the legacy credential helper failed; token values never enter logs or prompts.

Canonical evidence and pending image-pipeline decision:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/surface_diversity_20261108/SUMMARY.md`

The frozen prior 160 contain 11 round laptop requests, including 8/10 Café scenes. The old downstream rectangular guide explicitly overrides their shape. Writer improvements alone cannot establish successful round-table generations; an isolated pipeline fix versus preserving the old pipeline is awaiting Hooman's decision.

The new text set has 160 actual GPT-5.5 prompts: 35 round laptop tables (all 14 Café scenes), 5 oval tables, and 61/80 printer supports on cabinets, credenzas/sideboards or fitted counters. R4 originally returned 11 successful banks and 5 errors; the frozen r5 recognition snapshot accepts all 16 last actual normalized responses without changing model-authored fields. Raw failures remain in provenance. This reviewed text set is not a fresh first-call reliability trial. The current writer passes 279 offline tests. No new images are generated yet.

## Historical first V6.2 revision

V6.2 is an isolated successor to frozen V6.1. It accepts a Smart Brief, source messaging, and a `deviceType_CameraName` tag, then returns exactly ten ranked scene prompts. It preserves V6.1's source scoring, C-Tech style, prop diversity, and camera adaptation while adding support-shape diversity and more coherent walls, props, furniture, and printer stations.

The research candidate is `v6.2-writer-runtime-r1` with catalogue `hp-v6.2-approved-props-v1`, revision `v6.2-spatial-composition-20261106-r1`. Its 260 environment-specific entries are derived from the approved V6.1 catalogue. No new unapproved props were granted. One home stone arrangement was removed, the office paperweight was limited to clear glass, and wall boards were changed from empty to sparse non-legible geometric content.

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6_1/PROPS_FOR_REVIEW.md`

The compiled runtime catalogue is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_2/approved-v6.2-20261106.catalog.json`

V6.1 remains unchanged at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_1`

## Runtime contract

Input contains exactly `smart_brief`, `source_messaging`, and `camera_tag`. The first two values may be text or JSON. The tag resolves offline; the model does not inspect a camera image at runtime.

A successful response contains exactly ten prompts plus debug and audit data. Each prompt includes scene text, environment, approved prop IDs, exact prop mentions, source score components and evidence, relationship/explanation fields, C-Tech reference score/explanation, and camera-fit explanation. The application calculates the combined source score, assigns IDs, and sorts by source relevance followed by C-Tech score. It does not edit scene prose.

The model may receive one complete-bank repair request. A bank that still fails returns an explicit error and no usable prompts. Transport retries are bounded separately as described in `provider.py`.

## V6.2 behavior

- A visual family can occur only once across a ten-prompt bank. Broad families deliberately merge visually similar props; notebooks, folders, binders, books, and loose papers are one paper-material family.
- Registered lighting, room, atmosphere, composition, and activity phrase families can occur only once per bank, including semantic equivalents such as “warm daylight” and “warm natural light.”
- A laptop bank includes at least one naturally compatible round/circular table scene. Other support shapes remain scene-driven. Printer supports remain sturdy rectilinear equipment tables.
- Visible walls use one coherent, approved treatment when the camera permits. Artwork belongs substantially within the composition and relates to the furniture grouping below it. Empty wall boards are unavailable.
- Printer tables read as wall-oriented equipment stations with an open standing approach. Round printer tables, drinkware on the equipment support, seating aligned as a personal workstation, and unrelated puzzle/game/toy clutter on or beneath the station fail validation.
- Liquids are kept to a safe side of laptop work areas; arbitrary stones and random floor props are not used to fill allocation slots.
- Each selected prop ID has an exact case-sensitive quotation in `prop_mentions`. This makes declared-prop/prose agreement deterministic without requiring an unbounded synonym recognizer.
- Shelving, display ledges, and pegboards must be populated with additional approved, declared prop families. Empty or blank versions fail validation.
- Printer scenes normally use Office, Home, Education, or Creative Studio. Café or Gaming requires exact source support. The primary printer support must be a dedicated table, worktable, or substantial equipment-scale side table; desks and personal workstations fail validation.
- Detail density is qualitative. Close-up scenes use a compact local arrangement, medium scenes may include one coherent background zone, and wide scenes may use layered room detail. There are no noun-count ceilings.
- Text-bearing details require blank, unmarked, indistinct, non-readable, or background-only treatment as appropriate. Portraits, human faces, additional computing devices, and unavailable hardware remain excluded.

## Files

| File | Purpose |
| --- | --- |
| `system_prompt.md` | Root-authored V6.2 writing and planning instructions |
| `input.schema.json`, `model_output.schema.json` | Request and strict raw-model contracts |
| `approved-v6.2-20261106.catalog.json` | V6.2 derivation of the approved environment-specific catalogue |
| `build_v62_catalog.py` | Reproducible V6.1-to-V6.2 catalogue derivation |
| `prop_lexicon.json` | Bounded known-object recognition lexicon |
| `camera_profiles.json`, `camera.py` | Offline camera-tag resolution and qualitative guidance |
| `reference_library.json` | 18 C-Tech prompt references |
| `validation.py` | Bank, prop, phrase, source, camera, shelf, and printer-placement validation |
| `runtime.py` | Generation, one repair, finalization, scoring, sorting, and audit |
| `provider.py`, `cli.py` | GPT-5.5 transport and command-line entry point |
| `tests/` | Offline runtime and regression tests |

## Baseline and evaluation status

The frozen V6.1 160-prompt export remains the baseline:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`

The source map is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/composite_source_map.json`

V6.2 is not yet handed off. Its 231 text/runtime tests and six immutable-evaluation-runner tests pass locally. The exact R3 research pilot is frozen at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-pilot-20261106-r3`

R3 contains four device/camera banks and 40 unique prompts: Cashmere laptop FrontCloseUp, EliteBook laptop FrontWide, Tassel printer FrontCloseUp, and Magic printer FrontWide. All four banks passed the final runtime validator with ten prompts each, at least one compatible round support in each laptop bank, no forbidden printer-support placement, and no manual prose edits. Every bank used the single allowed automatic repair call. The initial responses produced eight undeclared-known-prop errors and one repetition-group error; the repair resolved all nine. This is evidence for the bounded repair design, not evidence that one-shot model output is deployment-ready.

The R3 environment distribution is Office 12, Home 9, Creative Studio 8, Education 6, Café 3, and Gaming 2. The prompt export and validation record are:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-pilot-20261106-r3/pilot_export/prompts_pilot_40.json`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-pilot-20261106-r3/pilot_export/validation.json`

The two prompts using an “empty architectural letter tray” follow the approved catalogue entry `V61-OFF-006`. The wording is retained in the immutable pilot and flagged for future catalogue review; it is not an empty-shelf violation.

R1 and R2 remain preserved as development evidence. R1 exposed printer-support scenes that still read as personal activity surfaces. R2 enforced the stronger printer rule but exposed a shelf-population recognizer bug for singular “floating shelf holding”; that deterministic bug was fixed before R3. A distribution review and image evaluation remain required before a full 160-prompt release.

The exact C-Tech annotations, joined prompt/judge evidence, Astra review request, and Astra response are preserved under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2`

The high-effort Astra review recommended keeping wall richness outside the natural-placement score, using round tables selectively rather than across every scene, and treating malformed furniture as a downstream visual defect that the writer can only weakly influence. Following the user's explicit support-shape requirement, the runtime requires one context-compatible round table in every ten-prompt laptop bank while keeping the other nine scene-driven. Wall treatment remains crop-aware, and visual geometry detection belongs to the separate V4 judge.

## Reproduction

Run local tests without model calls:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  research/source_messaging_v1_to_v6/versions/v6_2/tests -q
```

Prepare and verify a new immutable evaluation snapshot:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python \
  eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/run_eval.py prepare \
  --revision <new-unique-revision> \
  --catalog research/source_messaging_v1_to_v6/versions/v6_2/approved-v6.2-20261106.catalog.json
PYTHONDONTWRITEBYTECODE=1 python \
  eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/run_eval.py verify \
  --revision <new-unique-revision>
```

Paid calls require the explicit `--paid-calls-authorized` flag. Never overwrite or silently resume an ambiguous snapshot. Preserve the frozen inputs, runtime, results, call journals, source map, and final export together.
