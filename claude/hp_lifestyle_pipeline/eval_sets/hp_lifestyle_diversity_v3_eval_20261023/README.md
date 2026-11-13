# HP lifestyle diversity V3 evaluation

This directory is the frozen 2026-10-23 diversity pilot. It contains nine
production source messages paired with matching printer or laptop close/wide
camera tags: 18 independent GPT banks, 30 candidates per bank, and 540 total
candidates. The deterministic selector chose six candidates from each bank
(two from each ordinal rank bin `1-10`, `11-20`, and `21-30`) for 108 image
rows. miniPC inputs and renders are outside this evaluation.

The prompt banks, normalized outputs, and 108 selections have passed root
semantic review. Root approved the four completed image-generation smokes and
released the remaining 104 rows at 2026-10-23 22:40 UTC. The authorized run is
in progress. At the release-status snapshot, five rows were done and four were
submitted. Image completion is not a claim of image quality or camera fidelity.
The approval evidence is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/smoke_review.json`;
it records the release after checking the four rows' reference bindings,
hashes, dimensions, seed, and selected/request text equality.

## Frozen release inputs

These are the approved inputs consumed by the image runner:

| Artifact | SHA-256 |
| --- | --- |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/manifest.json` | `c71276599e225c57e6b3c238549d4e93ebb81ae66629ba77f5c9a68417a72c2b` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/accepted_prompt_cases.json` | `f99463928b998cdd8d638ade80c3c42c49d67eefaaebb3416b861f7a474c9aeb` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/selection_manifest.json` | `158553c25eaff38a346b158083fbf565b19a424126d4584c6f35249ed9a16224` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/root_selection_approval.json` | `3a0fc38beb1e628345097f7872e0715f35c114806172826c46fd956c4ddaf943` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/system_prompt.md` | `9516c00b1da9a1f3c232619b151ccfc5e4f7801940a86535b880c3829d524293` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/output.schema.json` | `218dc0c1fb3d3eef512b4b2969c8a292bc0d7eaedd7f8fdf46ba0bba9f68c7f7` |
| `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/camera_profiles.json` | `59b5e2b322dcd74c21432e772f3dd11513f71c182f6114b99b15e009dbeea68b` |

The root approval records the hashes presented for review before the approval
helper wrote the accepted and selection files above. The image runner binds to
the final approved file hashes in this table.

Verify the frozen files without modifying them:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
sha256sum \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/manifest.json \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/accepted_prompt_cases.json \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/selection_manifest.json \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/root_selection_approval.json
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/scripts/build_system_prompt.py --check
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/run_generation.py --validate-only
```

`--validate-only` performs local provenance and inventory checks and does not
call the endpoint.

## GPT-5.5 prompt-bank reproduction

The actual calls used deployment `gpt-5.5`, medium reasoning,
`max_completion_tokens=24000`, strict JSON Schema, no temperature, at most two
concurrent calls, up to 100 transient transport attempts, and no automatic
semantic retries. The two runtime input fields were `source_messaging` and
`camera_tag`.

The historical command was:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/run_gpt55.py \
  --all-authorized \
  --max-concurrency 2 \
  --max-transient-attempts 100
```

Do not rerun it merely to improve wording or against the approved artifact
tree: it rebuilds progressive accepted-state files while it runs. Raw attempts,
authorized replacement attempts, rejected attempts, normalized sidecars, and
validation sidecars in this directory are the reproducible record.

The deterministic finalizer is a required runtime companion. Its canonical
module is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v3/scripts/finalize_output.py`
with SHA-256
`a298242bf576d5d791c99a4983f313fc3423022265ad495650359a68cb689f6b`.
Production use must call it with both the exact raw input and the pinned camera
registry:

```python
normalized_output, normalization_log = finalize_output(
    raw_output,
    raw_input=raw_input,
    registry=registry,
)
```

The historical sidecar-reconstruction command was:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/finalize_records.py --all-current
```

Do not run that command in this approved active eval tree. Although it
preserves raw record bytes, `finalize_records.py --all-current` rebuilds
`accepted_prompt_cases.json`. Use it only in an isolated full checkout or copy
that retains the repository-relative layout, then compare the derived hashes
to the frozen approved artifacts.

The enhanced finalizer produced byte-equivalent normalized outputs and logs for
all 18 approved production banks. The proof artifact is
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/finalizer_camera_metadata_equivalence.json`.
Do not rerun
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/select_candidates.py`
on the approved tree: the selector intentionally writes a new
`pending_root_semantic_review` manifest.

## Image evaluation and gallery

Standalone prompt exports are available beside this README:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts.json`: all 540 normalized V3 candidates, including relevance/debug fields and selection flags.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts_selected.json`: the exact 108-candidate projection used by the image eval.

The galleries and analysis use a derived six-category `display_environment` for inspection:254 Office,20 Café,24 Creative Studio,111 Home,80 Education and51 Gaming. The model-authored `environment` remains unchanged in both exports. The reproducible rule audit, including every candidate mapping and borderline exclusion, is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/diversity_aware_v3/data/v3_display_environment_taxonomy_audit.json`. It only reassigns canonical Office rows with an explicit café or physical studio setting.

Rebuild or verify both exports with `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/export_generation_prompts.py --check`. The files contain the upstream V3 scene prompts, not the downstream `usedPrompt` rewrites.

Endpoint settings, the authorized run, resumable commands, and the preserved
V2 stop checkpoint are documented in
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation/README.md`.

The progressive gallery is:

`https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generated_v3/gallery/index.html`

Its local publisher state is under
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_diversity_v3_eval_20261023/publication`.
