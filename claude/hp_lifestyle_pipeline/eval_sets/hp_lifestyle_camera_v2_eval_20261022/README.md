# Camera-aware V2 image evaluation

As of 2026-10-22 Pacific. User-authorized image generation while text review proceeds. V1 remains the selected release; this is an evaluation, not deployment.

## Scope and matching

Use the same nine distinct production source-messaging JSONs as the historical V1 eval: three laptop sources and six printer sources. Pair each with every current high-resolution render of the same effective device type. Hooman explicitly excluded miniPC and confirmed preserving each reference aspect ratio. Do not infer missing tags for historical V1 twins. This new set uses the current catalog’s exact names, including explicit source-to-canonical aliases.

A source plus camera tag defines one GPT-5.5 input; reuse its prompts across all current renders with that tag. Product names remain offline asset provenance only. The unregistered laptop review view uses V2’s explicit unknown-tag fallback and is labeled as such, rather than silently inventing camera knowledge.

Current inventory: 161 laptop and 41 printer PNGs included; 41 miniPC PNGs excluded. Expected 369 distinct source/tag cases and 729 source/render pairs before variable prompt counts; builders must verify these numbers.

## Fixed parameters and differences from the historical eval

Use the frozen camera-V2 prompt SHA-256 00912f74c3ef11dece81c7e3ba7792ffafdf9f3fb12a2330923dd16c75dbd65e, actual GPT-5.5, medium reasoning, 8000 completion-token limit and strict JSON Schema. No runtime images or product names are supplied to the writer.

The downstream endpoint remains https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev. Request prompt rewriting with gemini-3.1-pro, 50 steps, one image, seed 42 where the endpoint supports explicit seed selection. Preserve actual returned settings and current endpoint metadata.

All 202 included 1024×576 source renders retain 16:9 at 2560×1440 output, within the endpoint’s advertised dimensions, pending generation smoke validation. These dimensions and current reference images differ from the historical 2368×1776 eval, so this is not a controlled paired A/B. No padding, cropping, recoloring or product changes are introduced into reference uploads.

## Gates and evidence

1. Verify every included source/render against its recorded SHA-256 and catalog type correction. Exclude miniPC.
2. Generate and validate representative prompt cases, then continue all source/tag cases. Retain raw failed/rejected attempts and citation-path repairs separately.
3. Upload exact original PNG bytes with content type image/png; bind returned blob IDs to actual bytes and the complete source identity. No historical blob cache is reused.
4. Run tight-printer and medium-laptop smoke generations; verify input binding, output dimensions, debug and visible output before the full batch.
5. Preserve pending job IDs before polling and download outputs immediately. Resume only with matching input/prompt/payload provenance.
6. Publish a new run gallery preserving the historical input/output columns, with camera identifiers and visible pending/failed counts. Never overwrite historical V1 publications.

Images and large raw artifacts are stored under backed-up /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022, not solely on volatile scratch. Code, manifests and compact records live alongside this README.

Text acceptance does not prove camera fidelity. The endpoint can add composition instructions; preserve full rewritten prompts/debug to distinguish observed changes from causal hypotheses.

## Live execution and review

The two smoke generations passed reference binding, actual 2560×1440 PNG dimensions and returned seed42. Root inspected both original/output pairs. The tight printer result contains paper and a plant explicitly inserted by the downstream Gemini rewrite despite the zero-prop V2 environment prompt. The laptop rewrite adds a window. Keep these results as evidence; they do not indicate a new client reference swap. Smoke decision record: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/smoke_review.json`.

Full image evaluation is running progressively from accepted prompt cases. The image worker uses up to eight in-flight jobs, but initial completions suggest the endpoint serializes processing at roughly118seconds per image. Even729 source/render pairs with one prompt each would take about24hours at that rate; multiple prompts increase the total. This is an early estimate, not a completion promise.

Live gallery: [https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2/gallery/index.html). The publisher checks every120seconds for changed inputs/results, uploads new outputs, refreshes broker credentials and updates only this run. Unavailable/pending work remains visible.

- Prompt status: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/status_inventory.json`
- Exact accepted prompt records: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/accepted_prompt_cases.json`
- Prompt resume script: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/resume_prompt_eval.sh`
- Image status and completed/pending jobs: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022/summary.json` and `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022/watch_status.json`
- Image resume command: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022/resume_command.txt`
- Publisher state and resume instructions: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/supervisor_state.json` and `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_camera_v2_eval_20261022/publication/README.md`

The accepted map grows during prompt execution; each image binds to the stable accepted case/output rather than the changing whole-map checksum. Durable async job journals prevent a resumed run from submitting already known jobs again. Confirmed safe pre-submission transient failures have a bounded retry budget; ambiguous submissions remain explicit.

## Resume and validation safeguards

A supervisor must not declare completion from an older accepted-map snapshot: prompt generation expands the required row set during the run. The image supervisor now checks the current snapshot hash,369 accepted cases and exact terminal row coverage, with no pending or safe-retry jobs. Twelve focused runner/supervisor tests passed, including the regression where an old335-row batch finishes after the prompt map has grown.

For prompt resumption in an agent/tool session, use a detached session rather than relying on nohup alone. The live watchdog uses setsid and waits for the active prompt writer before resuming, preventing simultaneous accepted-map writers. Read the PID/status files first and do not launch a duplicate watchdog. Semantic retries stop at three successful responses per case across process restarts; transient transport retries have their own separate budget.
