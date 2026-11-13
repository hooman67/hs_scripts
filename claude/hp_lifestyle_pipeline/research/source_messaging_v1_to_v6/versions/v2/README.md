# Camera-aware V2 draft

V1 remains the selected release. This V2 uses offline camera knowledge to reduce scene demands when a fixed view has little room. It contains no blue-coverage work.

## Runtime

Send `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/system_prompt.md` as the system message and this JSON shape as the user message:

```json
{
  "source_messaging": {"KSP1": {}, "ValueProposition": {}},
  "camera_tag": "miniPC_FrontRightMedium"
}
```

There is no product-name field and no image input. Current tag prefixes are `laptop`, `printer`, and `miniPC`. Canonical camera names are compact, such as `laptop_BackLeftCloseUp`. Explicit aliases support selected legacy spellings. Unknown tags produce a conservative surface-and-light fallback and are identified in debug.

Use `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/output.schema.json` as strict JSON Schema response_format. The result contains a nonempty `prompts` list, source mappings and concise explanations, plus `debug.camera` for the resolved type, tag, profile version and simplifications. Device names and camera directions do not appear in scene prose.

Test settings: requested deployment `gpt-5.5`, `reasoning_effort=medium`, `max_completion_tokens=8000`, no explicit temperature. The runner preserves the actual returned model identifier, input, prompt, schema, request hashes, latency and usage. It retries transient errors up to 100 attempts and respects server retry timing.

## Sources of truth

- Behavioral instructions: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/system_prompt.template.md`
- Versioned type-camera profiles: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/camera_profiles.json`
- Design, evidence, limitations and current evaluation outcome: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/camera_aware_v2/SUMMARY.md`
- Current text-evaluation records: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current`
- Superseded experiment, preserved failures and snapshots: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/experiments/initial_mislabeled_messi`

Do not edit the compiled system message directly. Edit the template/profile registry, increment the registry version for changed profiles, and compile. Adding a device type or camera requires offline review and an explicit registry entry; neither image analysis nor name guessing occurs at runtime.

## Reproduce

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_system_prompt.py --check
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/build_eval_cases.py
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/run_gpt55_camera_eval.py --preflight-only
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/run_gpt55_camera_eval.py
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/validate_camera_eval.py
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/rebuild_accepted_selection.py --check
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/build_sample_review.py
```

The execution command makes real API calls for unrecorded cases. Resume reuses only matching request hashes. For a changed prompt/schema/input, provide a new `--output-dir` rather than replacing earlier results. Use the shared GPT-call authentication or the existing authorized configured Azure adapter; do not put secrets in research artifacts.

The review contains full input JSON, every output prompt, debug and matching offline camera references. Reference images are for human review only; they are not sent to GPT-5.5. Text validation does not establish downstream image or camera fidelity.

## Tested candidate and review

As of 2026-10-22, the current draft is researcher-accepted for Hooman’s text review, not selected for production. The complete contract remains `source_messaging` plus `camera_tag` only. Prompt SHA-256: `00912f74c3ef11dece81c7e3ba7792ffafdf9f3fb12a2330923dd16c75dbd65e`; profile version: `camera-v2-draft-2026-10-22-r3`; returned model: `gpt-5.5-2026-04-24`.

All nine distinct production sources are included in a 24-case camera/control suite. The selected set has 39 prompts. Two initial scenes were rejected (too many local objects in case07, and a phone in case19), then regenerated under unchanged instructions. All attempts are preserved: 26 successful model responses, 27 transport attempts including one transient retry. Selected 24/24 pass automated checks and root text review, with zero selected citation repairs. This is selected-sample acceptance, not a statistical success rate or proof of camera preservation.

- Full review: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/review.html`
- Exact selected/rejected records and hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/accepted_samples.json`
- Selected structured outputs: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/accepted_validated_outputs.json`
- Human scene-scope assessment: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/manual_review.json`
- Prompt, schema and registry hashes: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/candidate.json`

## Citation-path validation

After strict-schema validation, the caller can run `normalize_citation_paths(output, source_messaging)` from `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/citation_path_guard.py`. It returns `validated_output`, `citation_repairs` and `failures`. Preserve the original output separately. A path is changed only when the unchanged quote occurs in exactly one direct text field of the same intended message. Do not accept missing, ambiguous, or wrong-message evidence. This guard does not validate scene density, camera geometry or all JSON fields; run the existing schema and behavior checks too. It adds no LLM call.

The initial case07 citation demonstrates why the guard exists even though no selected output needed normalization. Initial raw audit: 22/24; with citation normalization: 23/24. Neither number includes manual scene acceptance.

## Published review

[Open the camera-V2 text review](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_text_review_20261022/gallery/index.html). The publication contains the full review plus the shared Adobe IMS authentication wrapper. S3 object bytes and content types were verified; an authenticated browser rendering was not tested.

Publication manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/publication.json`. The saved served HTML is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/index.html` and the unchanged authentication asset is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/imsauth.js`. To restore the exact published artifact, first run the shared aws-creds skill, then use the following commands with fresh broker credentials. These restore the saved bytes; do not overwrite a review with different samples.

```bash
source /home/colligo/.claude/hshariati/aws_creds.env && aws s3 cp /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/index.html s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_text_review_20261022/gallery/index.html --content-type text/html --region us-west-2
source /home/colligo/.claude/hshariati/aws_creds.env && aws s3 cp /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/publication/imsauth.js s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_text_review_20261022/gallery/imsauth.js --content-type application/javascript --region us-west-2
```

For a changed candidate, rebuild the review from its own accepted manifest and publish under a new prefix. The current publication used the authorized alternate Pluto credential broker recorded in the manifest because the standard broker was unavailable; no credential values are stored here.

## Replay saved selection and isolated retries

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/accepted_samples.json` records the manual acceptance decisions and every selected/rejected record hash. It is an input to reproduction, not a ranking algorithm. To verify it and reproduce the two derived accepted-output files without any API call:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/rebuild_accepted_selection.py --check
```

Omit `--check` to rebuild the derived files from the preserved records. The primary validator intentionally reports the original failed attempts; do not replace those failures with selected-sample pass counts. The selection verifier checks those failed records too.

The two isolated retry commands used for this candidate were:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/run_gpt55_camera_eval.py --case 07_actual_laptop_front_right_medium --output-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/runs/gpt55_type_camera_retries/07_attempt2
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/scripts/run_gpt55_camera_eval.py --case 19_actual_printer_admin_front_right_medium --output-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v2/eval/current/runs/gpt55_type_camera_retries/19_attempt2
```

These commands reuse matching saved records when present; a new output directory makes new model calls. Fresh outputs are nondeterministic and will not reproduce exact response bytes. New attempts require their own review and selection record.

For the final current candidate only, all 26 successful responses used 422,213 reported tokens (370,748 input, 51,465 completion) and 548.603 seconds summed latency. The selected 24 used 391,195 tokens and 510.446 seconds. Latency excludes the failed transport request’s unrecorded duration and its 2.335-second backoff; it is not batch wall time. Earlier prompt experiments are archived separately and are not included in these totals.
