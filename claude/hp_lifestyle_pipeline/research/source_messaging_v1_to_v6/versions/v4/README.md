# V4 lived-in camera-aware writer

Status: 540 final candidates and 108 selected prompts text-reviewed; bounded 108-image evaluation launched, 2026-10-26. V4 is an evaluation candidate, not a production promotion.

Runtime input has only `source_messaging` and `camera_tag`; output has 30 ranked candidates and debug. The six native categories are Home, Office, Education, Gaming, Café and Creative Studio. No runtime image analysis, product names or blue-coverage control.

Root authored `system_prompt.template.md` to restore specific signs of ongoing use and coherent everyday activity while retaining the V3 offline camera geometry. `camera_profiles.json` is deliberately copied unchanged. `scripts/build_system_prompt.py` compiles local notes using the established V2 note-renderer implementation; this is a read-only dependency, not a V2 modification. The local resolver/finalizer are preserved implementations with V4 audit labels. The finalizer never edits prompt text.

Compile:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4/scripts/build_system_prompt.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4/scripts/build_system_prompt.py --check
```

The eval manifest pins the compiled prompt, schema, registry, source messages and reference images. Reproduction, immutable attempts, text review and bounded image launch are documented in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/README.md`. Research rationale and limitations are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/lived_in_v4/SUMMARY.md`.
