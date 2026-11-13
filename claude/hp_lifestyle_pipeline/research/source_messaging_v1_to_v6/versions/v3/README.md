# V3: camera-aware diversity with source-relevance ranking

Candidate under evaluation,2026-10-23. V1 remains the selected release and V2 is preserved. This version changes the candidate bank and ranking; it does not introduce runtime vision or blue control.

## Runtime contract

Send the self-contained system message from `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/system_prompt.md` and one user JSON object with exactly `source_messaging` and `camera_tag`. Source messaging is the production KSP/ValueProposition JSON, with `_chatSession` ignored as data. Tag format remains ProductType_CameraName. No product name, image, SKU selector or additional planning message is required.

Use `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/output.schema.json` as strict JSON Schema response_format. The schema fixes the response shape/enums; host validation enforces semantic constraints such as30 candidates, valid evidence and rank arithmetic because the Azure deployment rejected some assertion keywords in the initial schema.

Model: explicitly `gpt-5.5`, medium reasoning, `max_completion_tokens=24000`, no temperature. The larger output budget supports30 candidates and their evidence/debug. Actual token use and returned model snapshot are preserved per run; public documentation does not prove deployment access.

The runtime has a required deterministic finalization/validation step. It sets uncited candidates to zero relevance, recomputes sums, sorts and assigns IDs; it preserves scene text. Store the original response and the normalization report. Semantic camera/style/evidence failures are held rather than repaired by inventing meaning. A system message alone did not reliably satisfy the scoring contract in the initial probes.

### Required finalizer API and checksum

Canonical module: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/scripts/finalize_output.py`.

SHA-256: `a298242bf576d5d791c99a4983f313fc3423022265ad495650359a68cb689f6b`.

```python
from camera_profile_resolver import load_registry
from finalize_output import finalize_output

registry = load_registry()
normalized_output, normalization_log = finalize_output(
    raw_output,
    raw_input=raw_input,
    registry=registry,
)
```

For a preserved eval record, rebuild the normalized output and audit sidecars without modifying the raw record:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/finalize_records.py --case <case_id> --sample <sample_name>
```

The application must retain the raw record SHA, normalized-output file and semantic hashes, and normalization-log hash. This companion is required; the system prompt alone is not the scoring runtime. When input and registry are supplied, it also replaces mismatched `debug.camera` metadata with the exact offline resolver result and records the old/new metadata in `camera_metadata_repair`; it never changes scene text for this repair. Omitting both optional arguments preserves the archived scoring-only behavior.

The original unknown-tag edge remains preserved as a failed raw metadata case. Its separate repaired sidecars pass with `unknown` framing/elevation and unchanged safe fallback prose: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/eval_edges/validation_camera_repaired.json`. The approved18 known-tag production outputs and normalization logs are byte-equivalent under the enhanced API; proof: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/finalizer_camera_metadata_equivalence.json`.

## What changed from V2

- Exactly30 candidates per source/tag replace the useful-KSP count cap.
- Explore grounded, adjacent and broader contexts across Home, Office, Education and Gaming. Cafés and creative studios are Office subsettings.
- At least ten alternatives change the primary task/context instead of moving the same paperwork into another room.
- A fixed score sums setting30, activity30, visible work materials20 and use context20. Scores measure source relevance, not visual quality or probability. Weak sources and tight crops need not produce high scores. Ties are valid.
- Shared exact evidence plus per-candidate evidence IDs establish KSP/ValueProposition mappings. The application derives redundant reverse maps and counts.
- Camera limits, device omission and ordinary photographic scene style remain mandatory. All creative departures must still fit the fixed view. Unsupported source claims are prohibited even when invented scene details are allowed.

## Version and reproduction

The root-authored template is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/system_prompt.template.md`. The compiled prompt embeds a byte-pinned copy of the V2 offline camera registry, not a dependency that silently follows future V2 edits.

Current revision2 compiled SHA-256: `9516c00b1da9a1f3c232619b151ccfc5e4f7801940a86535b880c3829d524293`.

Output schema SHA-256: `218dc0c1fb3d3eef512b4b2969c8a292bc0d7eaedd7f8fdf46ba0bba9f68c7f7`.

Camera registry SHA-256: `59b5e2b322dcd74c21432e772f3dd11513f71c182f6114b99b15e009dbeea68b`.

Compiler:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/scripts/build_system_prompt.py --check
```

The isolated eval is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023`. Its manifest preserves exact inputs/settings/reference IDs and hashes. Use its resumable GPT runner for bounded selected cases; do not regenerate accepted calls solely to improve wording. Exact rejected probes are retained under the version's experiments directory.

## Evaluation scope and limitations

All nine distinct source messages × matching close-up/wide tags =18 banks,540 candidates. Select two candidates from each rank stratum1–10,11–20,21–30, preferring visible-signature diversity within the stratum, followed by semantic review. The initial image budget is108, on four byte-verified Koki laptop/Magic printer renders. Preserve native16:9; use2560×1440, seed42,50 inference steps and the existing Gemini3.1Pro downstream rewrite.

Close/wide banks are independently generated from source+tag. They are compared by source/relevance stratum, not identical scene concepts. The corpus covers four named source products and no gaming-specific source message. Rubric scores remain uncalibrated model judgments; deterministic finalization corrects mechanical contradictions only. The downstream rewrite can introduce repeated lighting and objects, so its full usedPrompt/debug is required beside each image. Image completion does not establish quality or camera fidelity.

Canonical evidence and live findings: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware_v3/SUMMARY.md`. Exact stopping point: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/PROJECT_STATE.md`.
