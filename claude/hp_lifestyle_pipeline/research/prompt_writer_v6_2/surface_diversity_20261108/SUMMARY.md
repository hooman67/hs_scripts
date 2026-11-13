# V6.2 surface diversity — updated 2026-11-09

## Contents

- [Live image evaluation](#live-image-evaluation)
- [Scope and baseline finding](#scope-and-current-status)
- [Published text results](#published-text-results)
- [Method and next gate](#method-and-next-gate)
- [Isolated pipeline candidate](#isolated-pipeline-candidate)
- [Reproduction and assets](#reproduction-and-assets)

## Live image evaluation

USER-CONFIRMED2026-11-09: use the isolated shape fix. The endpoint is live in tmux at `http://127.0.0.1:8137` with unchanged baseline image/text model, dimensions, quality, one-guide/no-mask input and exact16 twin bytes. Eight purposive smoke images completed; root inspected every output. Three round requests show curved rims. The oval close-up's perimeter is unobservable, while its plan/guide retain oval. Cabinet, credenza, fitted counter and dedicated worktable are visible in the printer cases. The full remaining152 are now running with4 workers, interleaved by device/view. This is an integration gate, not a blinded quality evaluation or exact-pixel guarantee. Additional unrequested props are observed and preserved for review.

Live gallery: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108/generated_surface_shape_r1_env2/report/viewer.html?ldap=hshariati . Its sibling `report/distribution/index.html` uses the same frozen160 texts and tracks artifact availability. The first S3 checks established matching sizes only. The corrected persistent publisher now verifies newly published images, twins and report files by streaming remote SHA-256, with ETag/size-checked reuse of previously verified content. It updates as records change. No old image judgment is carried over.

The first environment produced8 client-initialization failures and0 images, preserved separately. Env2 fixes the missing gateway llm extra and verifies real client construction before accepting jobs. The first valid env2 output was recovered from its existing job after a runner/debug-schema mismatch; no image was resubmitted. The fallback proves the exact single guide-only image call from hashed debug evidence while retaining the raw omitted field. Original failure records remain archived. The current runner suite passes24 tests.

Durable run: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/runs/generated_surface_shape_r1_env2`. Root smoke evidence: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/smoke_review_20261109.json`. Deployment manifest SHA-256 `b2a852792ef8029e867fb37c3c21c394d6e47fed7e81dc103fbe726d0ec0604c`; immutable run SHA-256 `3b3341cb458d03f9c5088706ae59ce1a46d0be8fb04b4f5a320c69613761ae0b`. Next: finish terminal160 accounting, shape-plan audit and final S3 verification. Do not claim completion from smoke results.

## Scope and current status

USER-CONFIRMED: revise V6.2 to produce more varied, plausible laptop/printer supports, regenerate all 160 prompts and images, preserve earlier V6.2 style, prop/phrase diversity, wall composition, shelf population, source ranking, and camera awareness. The old 160 are immutable baseline evidence. Ten prompts per Smart Brief/source/camera bank; Cashmere, EliteBook, Tassel, Magic; four existing views each. No new user input fields or runtime image analysis.

VERIFIED, frozen baseline audit: 11/80 laptop prompts explicitly request round primary tables; 8/10 Café prompts do so. All 8 round Café requests, all 3 round Home requests, and the one oval Office request are overridden by the downstream rectangle-only geometry guide. Source evidence includes the final executable image prompts, not just comments or model explanations. All 80 printer inputs use table-family supports because the old system and validator required tables. Full counts, row IDs, exact quotations, and limits are in `audit.json`, rebuilt by `build_audit.py` in this directory.

Directly inspected representative Cashmere FrontWide p7: requested round café table, final rewrite explicitly requires the square guide footprint, image is square. This confirms a pipeline conflict; it does not establish that a different writer alone can fix round-table outputs. Other image-level assertions require separate visual inspection.

## Published text results

VERIFIED, full160-text census: Cashmere, EliteBook, Tassel and Magic each have four fixed camera banks of ten prompts. Laptop supports:35 round,5 oval,3 explicitly rectangular,37 unspecified. All14 Café prompts are round. Printer supports:23 fitted counters,20 credenzas/sideboards,18 freestanding cabinets,19 tables;61/80 are non-table. Every laptop bank has4–5 round supports; every printer bank covers all four support families and has7–8 non-table supports. These are text counts, not observations from new generated images.

All model-authored fields remain unchanged from each bank's last actual normalized GPT-5.5 response. The source run `v6.2-surfaces-20261109-r4` returned11 successful banks and5 terminal errors. The frozen corrected recognition snapshot `v6.2-surfaces-20261109-r5-recognition` accepts all16 last responses. Original errors and raw request/response provenance remain in the strict export. No earlier-response search, manually edited prompts or extra model calls were used to construct this export. Independent audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/surface_diversity_20261108/r4_text_audit.md`. This acceptance does not establish first-call or deployment reliability.

Published artifacts:

- JSON160: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/source/prompts_all_160.json
- Plain text160: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/source/prompts_all_160.txt
- Distribution and prop audit: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/report/distribution/index.html
- Grouped FE review: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261109/report/viewer.html?ldap=hshariati

On a first FE visit, use the canonical viewer's “Skip (comment only)” button. The shared vendored viewer was not edited. Full prompts, full Smart Brief/source input, source/C-Tech scores, prop evidence and corrected twins are included; image output and judgment remain explicitly pending. Distribution includes environmental/device/view counts, source/C-Tech scores, support families/shapes, per-bank compliance, all declared prop groups, phrase repetition and source quotes. It does not import historical image judgments or infer visible image contents.

Publication verification retrieved81 S3 objects and matched bytes, SHA-256 and content types. Local browser tests of those same files verify the distribution,160 combined rows,10-row group and loaded twin images with no JavaScript errors. This was not an authenticated gateway browser test. Verification artifacts are `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/publication_verified_20261109.json` and `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/browser_smoke_20261109.json`.

## Method and next gate

Current executable checkpoint (2026-11-09): writer and tooling pass297 tests (279 writer,18 export/report). R4 text generation is complete and no text-writer worker is running. The separate image run is active as described above. R1 launch failed before model calls because Python3.12 is required; CLI now enforces it. R2 actual wide pilots produced10 laptop successes and a printer bank rejected by recognition false positives; both unchanged final pilot responses validate after fixes. R3 was erroneously launched after a failed preflight because its shell lacked fail-fast behavior, then interrupted; no r3 output accepted and journals preserved. These earlier calls are not omitted from provenance or represented as unbilled. R5 only freezes corrected recognition and revalidates existing responses; it makes no paid call.

1. COMPLETE: Astra high product-policy review, runtime/validator changes, actual16-bank GPT-5.5 generation, strict final-response export and S3 text review publication.
2. USER-CONFIRMED on2026-11-09: “Use the isolated shape fix (recommended).” Deployment is authorized and the eight-case smoke has passed. This is the documented exception to the earlier same-pipeline requirement; the v23.1 translation experiment remains paused.
3. ACTIVE: complete the remaining image run using its pinned isolated endpoint and immutable160 queue. Verify terminal source/twin/guide/image bindings, the native FE groups and all published artifact hashes. Preserve failures and report visual limitations; do not silently regenerate outputs.

RESEARCHER DECISION following Astra review: at least two round/circular laptop supports per bank, including every Café scene; varied appropriate table/desk/oval forms elsewhere. Printer banks use at least three materially distinct cabinet/credenza/fitted-counter/table families and at least five non-table supports, with clear standing access. This supersedes the prior table-only rule. Numerical coverage floors are research design choices, not customer camera-capacity limits. Main support remains exempt; separate/background furniture remains catalogue-controlled. Application-derived evidence avoids adding model-owned calculations or a new user input.

Astra request r1 exhausted 10,000 completion tokens in reasoning and returned no text; it is explicitly not a successful review. The preserved r2 call used high effort with a 24,000-token ceiling, returned normally with 8,294 completion tokens, and supplied the reviewed replacement policy. See `r2/astra_response.md` and `r2/astra_metadata.json`. GPT-5.5 access was separately verified through the policy-aware Foundry Azure SDK; the model identified itself as `gpt-5.5-2026-04-24`. The legacy credential helper failed and is replaced for this runtime revision without changing the requested model.

## Isolated pipeline candidate

VERIFIED implementation, supplemented by the live smoke above: clean source archived from Foundry commit `8c358bc7989cb0e137e89db0fd325168249e2a22`; geometry supports rectangular, round and oval primary tops projected through the same camera. The requested device pixels, position, size, footprint and orientation remain fixed in the guide. Rectangular guide bytes/metadata remain baseline-compatible. All footprint corners must fit inside curved supports; invalid geometry errors instead of moving the device. Printer support prose preserves cabinet/credenza/counter identity. Root-reviewed Astra product policy is integrated with unrelated sections and printer-wall rules unchanged.

The candidate passes157 applicable offline tests with real dependencies and Ruff. The patch reproduces the reviewed runtime byte-identically from the pinned archive. The wrapper/dependency deployment is separately pinned and now image-tested as above; it does not resume the v23.1 translation experiment. Policy review retains an explicit note rejecting Astra's unrelated wall-anchoring suggestion. Additional preserved inconsistencies, including the inactive reference-histogram version, are listed in the candidate manifest.

- Patch: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/runtime_surface_shape_r1.patch`, SHA-256 `95ddc80d7d62e75c6f7461a45011a6412a35a4bc03a36fada517fdf5888a8843`.
- Manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/local_scene_endpoint/runtime_surface_shape_r1_manifest.json`.
- Authoritative reviewed policy: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_2/surface_diversity_20261108/shape_prompt_review/root_reviewed_policy.json`.

## Reproduction and assets

- Frozen baseline: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/prompts_all_160.json`.
- Writer runtime: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_2`.
- New isolated generation/report tooling: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108`.
- Completed Astra run: `run_astra.py` in this directory; no active worker. Product prompt design only, no general coding delegated through gateway credentials.
- Exact old endpoint: `https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev/api/generate`; payload contains `digitalTwinId`, `cameraId`, `prompt` only. Live catalogue matches old PR4349 / `8c358bc7989c` / V20 lineage on 2026-11-08.
- AWS: broker `/aws-creds` legacy hostname still times out; installed gateway client `maybe_s3_env_vars` succeeds with injected machine auth and writes the private credential env file. No credentials are included in research artifacts.

Known publication issue from the old report: output links reference Pluto job artifact URLs. The new report must publish all images and twins to durable S3 and verify dependencies, not only HTML/JSON.

Accepted export: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json`, SHA-256 `e661123648d8b64bf37b462e482a8015fc8e9219cf3798781271719b99929500`. Its sibling `validation.json` pins all source/request/response journals and records the11/5 source status. `prompts_top6_96.json` is a derivative convenience, not the requested image scope.

To reproduce the export, run `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/export_revalidated_banks.py` with `--source-revision` set to `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/revisions/v6.2-surfaces-20261109-r4`, `--validation-snapshot` set to the sibling `v6.2-surfaces-20261109-r5-recognition`, and `--output-dir` set to a new empty destination. It fails rather than overwrite an existing export. Full build/publish commands and current published paths are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/README.md`.
