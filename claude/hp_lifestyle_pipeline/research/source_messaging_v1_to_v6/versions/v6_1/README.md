# V6.1 writer: phrase-diverse, camera-aware prompt banks

V6.1 is an isolated successor to frozen V6. It accepts a Smart Brief, source messaging, and a `deviceType_CameraName` tag, then returns exactly ten ranked scene prompts. It keeps the V6 source-scoring and C-Tech style contract while expanding approved scene detail, preventing repeated visual and language families inside a bank, and enforcing natural device placement.

As of 2026-11-03, the production candidate is `v6.1-writer-runtime-r1` with catalogue `hp-v6.1-approved-props-v1`, revision `v6.1-expanded-20261103-r6`. The catalogue contains 261 environment-specific entries and 158 visual families. The approved review source is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6_1/PROPS_FOR_REVIEW.md`

The compiled runtime catalogue is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_1/approved-v6.1-20261103.catalog.json`

V6 remains unchanged at:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6`

## Runtime contract

Input contains exactly `smart_brief`, `source_messaging`, and `camera_tag`. The first two values may be text or JSON. The tag resolves offline; the model does not inspect a camera image at runtime.

A successful response contains exactly ten prompts plus debug and audit data. Each prompt includes scene text, environment, approved prop IDs, exact prop mentions, source score components and evidence, relationship/explanation fields, C-Tech reference score/explanation, and camera-fit explanation. The application calculates the combined source score, assigns IDs, and sorts by source relevance followed by C-Tech score. It does not edit scene prose.

The model may receive one complete-bank repair request. A bank that still fails returns an explicit error and no usable prompts. Transport retries are bounded separately as described in `provider.py`.

## V6.1 behavior

- A visual family can occur only once across a ten-prompt bank. Broad families deliberately merge visually similar props; notebooks, folders, binders, books, and loose papers are one paper-material family.
- Registered lighting, room, atmosphere, composition, and activity phrase families can occur only once per bank, including semantic equivalents such as “warm daylight” and “warm natural light.”
- Each selected prop ID has an exact case-sensitive quotation in `prop_mentions`. This makes declared-prop/prose agreement deterministic without requiring an unbounded synonym recognizer.
- Shelving, display ledges, and pegboards must be populated with additional approved, declared prop families. Empty or blank versions fail validation.
- Printer scenes normally use Office, Home, Education, or Creative Studio. Café or Gaming requires exact source support. The primary printer support must be a dedicated table, worktable, or substantial equipment-scale side table; desks and personal workstations fail validation.
- Detail density is qualitative. Close-up scenes use a compact local arrangement, medium scenes may include one coherent background zone, and wide scenes may use layered room detail. There are no noun-count ceilings.
- Text-bearing details require blank, unmarked, indistinct, non-readable, or background-only treatment as appropriate. Portraits, human faces, additional computing devices, and unavailable hardware remain excluded.

## Files

| File | Purpose |
| --- | --- |
| `system_prompt.md` | Root-authored V6.1 writing and planning instructions |
| `input.schema.json`, `model_output.schema.json` | Request and strict raw-model contracts |
| `approved-v6.1-20261103.catalog.json` | Approved environment-specific entries and visual families |
| `prop_lexicon.json` | Bounded known-object recognition lexicon |
| `camera_profiles.json`, `camera.py` | Offline camera-tag resolution and qualitative guidance |
| `reference_library.json` | 18 C-Tech prompt references |
| `validation.py` | Bank, prop, phrase, source, camera, shelf, and printer-placement validation |
| `runtime.py` | Generation, one repair, finalization, scoring, sorting, and audit |
| `provider.py`, `cli.py` | GPT-5.5 transport and command-line entry point |
| `tests/` | Offline runtime and regression tests |

## Evaluation evidence

The accepted 160-prompt export combines successful GPT-5.5 banks and replays all sixteen through the final frozen r6 runtime:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`

The source map is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/composite_source_map.json`

Thirteen banks come from r4 and three from r6. R4 exposed a validator false negative for the valid phrase “substantial office side table.” An independent audit then found unresolved catalogue alternatives such as “classroom or library chair” in three banks. Both defects were fixed in the system and validator, covered by regression tests, and the three affected banks were rerun under r6. The accepted set uses five first-call banks and eleven one-repair banks, totaling 27 selected semantic calls. No scene text or creative field was manually edited. Deterministic evidence normalization removed three invalid citations and preserved those changes in the audit. Earlier development pilots and superseded banks remain preserved as evidence and are excluded from the accepted export.

The accepted file contains 160 unique prompts across 16 banks. It has no empty shelf/pegboard violation, forbidden printer support, unresolved scene alternative, repeated registered visual family, or repeated registered semantic phrase family. Offline verification passes 229 tests. These are text/runtime results; image quality and downstream rewrite behavior remain unevaluated for V6.1.

## Reproduction

Run local tests without model calls:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  research/source_messaging_v1_to_v6/versions/v6_1/tests \
  eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/test_run_eval.py -q
```

Prepare and verify a new immutable evaluation snapshot:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python \
  eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/run_eval.py prepare \
  --revision <new-unique-revision> \
  --catalog research/source_messaging_v1_to_v6/versions/v6_1/approved-v6.1-20261103.catalog.json
PYTHONDONTWRITEBYTECODE=1 python \
  eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/run_eval.py verify \
  --revision <new-unique-revision>
```

Paid calls require the explicit `--paid-calls-authorized` flag. Never overwrite or silently resume an ambiguous snapshot. Preserve the frozen inputs, runtime, results, call journals, source map, and final export together.
