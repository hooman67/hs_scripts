# HP lifestyle writer V5

V5 accepts a smart brief, source messaging and a fixed camera tag. It returns20 camera-compatible environment prompts with source and C-Tech scores, ordered by source relevance. V4.1 is frozen separately.

## Current evaluation status

This is a research candidate. In the final eight-bank GPT-5.5 pilot,3/8 model outputs passed mechanical validation after deterministic finalization. Root separately reviewed160 texts and corrected18 scene texts plus audit/score/citation fields; all8 reviewed banks pass. The reviewed examples demonstrate the intended output, not unaided runtime reliability. Original responses and all changes are preserved. The160 reviewed scene texts are unchanged after the equal-authority clarification; only source-score aggregation and ordering change. Two separate GPT-5.5 sparse-document checks exercise the revised system contract. Keep V4.1 frozen pending C-Tech feedback.

## Runtime

Send `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/system_prompt.md` as the system message. The user message is one JSON object:

```json
{
  "smart_brief": "Complete smart-brief text, or a structured JSON object",
  "source_messaging": "Complete source-messaging text, or a structured JSON object",
  "camera_tag": "laptop_FrontRightWide"
}
```

Binary DOCX/PDF/XLSX parsing is an upstream responsibility. The writer performs no runtime image analysis and receives no product name. The pilot preserves full document text with extraction provenance outside the runtime input.

Request `gpt-5.5`, `reasoning_effort="medium"`, `max_completion_tokens=24000` and strict structured output using `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/output.schema.json`. Do not set temperature. Actual returned model/build, latency and token usage are saved with each response.

After parsing, call `finalize_output(parsed, raw_input=input, registry=registry)` from `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/scripts/finalize_output.py`, then `validate_output(normalized, input, schema, registry)` from the neighboring validator. Preserve raw output and normalization log. Reject semantic/camera violations; do not silently repair scene prose. Validation is necessary but not sufficient for semantic or image-quality acceptance.

## Scores and ordering

Each prompt has `source_relevance_score` and `ctech_reference_score`, both0–100. These are model rubric judgments, not embedding cosines or image-quality scores.

Source components are independently attributed to `score_components.smart_brief` and `.source_messaging`: setting0–30, activity0–30, materials0–20 and use_context0–20. USER-CONFIRMED: the documents have equal authority; use useful information. The combined source score sums the higher supported value for each component across the two documents. It does not average or add document totals. A sparse document does not penalize the other; duplicate cues count once. Complementary evidence can contribute across different components. Unsupported document components must be zero. Verbatim evidence identifies the document and RFC6901 path (empty path for a text string).

The C-Tech score retains V4.1's relation bands:100 exact,80–99 minimal camera edit,70–79 same-category adaptation,60–69 category extension. Prompts sort by descending source score, C-Tech score for ties, stable order for exact ties. IDs p1–p20 are assigned after sorting. Frontends may choose top6 by this order or re-sort by C-Tech score.

## Inherited constraints

The18 normalized C-Tech references and122 offline camera profiles are byte-identical to V4.1. Six separate categories remain Home, Office, Education, Gaming, Café and Creative Studio. No frequency quotas. The complete20-prompt bank covers all six for known views, while top6 prioritizes source relevance.

No target device names or generic device nouns, extra computing hardware, blanket no-device clauses, or blue-coverage instructions. Use familiar places and ordinary detail groupings. Camera limits remain fixed: the tested laptop close-up allows0 props/0 background details; printer close-up1/0; both wide profiles3/2. Unknown tags use the conservative registered fallback. Source disagreement is reported in debug; it never changes camera geometry.

## Reproduction and evidence

Canonical research, scope, caveats and current status: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/SUMMARY.md`.

Pilot: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027`. Four document pairs × close/wide ×20 =160 proposed texts; Cashmere is an explicit mismatched-product test case. Modric desktop is inventoried but excluded by explicit user decision. No V5 images have been requested.

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/scripts/build_system_prompt.py --check
python -m unittest discover -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5/scripts -p 'test*.py' -v
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/build_inputs.py
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/run_gpt55.py --all-authorized --maxconcurrency 2
```

The runner reuses the existing exact-request response instead of producing another semantic draw. `--new-request-revision` permits a response for a changed request only; it does not retry an identical request. All earlier responses remain immutable. Historical r1 prompt/schema/manifest and first40 texts are under the pilot's `experiments/r1` and `records` directories. The raw versus normalized versus human-reviewed statuses must remain distinct.

Compiler depends on the established note renderer at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py`; complete repository checkout preserves it. Generated `system_prompt.md` is self-contained for runtime use.
