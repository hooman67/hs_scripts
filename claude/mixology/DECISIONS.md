# Decisions

## 2026-10-20 — Hide model identity from customers

Status: CONFIRMED BY USER / VERIFIED IMPLEMENTATION. Do not identify the image model in the customer UI. Remove provider/model naming not only from visible copy but also from ordinary browser-facing generation and history JSON, result metadata and error details, since network inspection would otherwise disclose it. Retain exact internal configuration and research records server-side. Use generic “Generating” and “generation prompt” language and plain Image N badges.

## 2026-10-20 — User-facing prompting guide

Status: CONFIRMED BY USER / VERIFIED IMPLEMENTATION. Replace the top-right “Foundry direct route” element with a GUIDE button and adapt the supplied sample-prompt document for end users. Omit internal system-prompt filenames, rewriter/model instructions and other deployment mechanics. Preserve useful recipe and arrangement examples while rewriting reference-image guidance to match the UI's real badges and ordering.

Status: IMPLEMENTATION DECISION. Use an in-page modal rather than serving the research Markdown directly. Explain that Stage 1's fixed house cup is Image 1 and uploads begin at Image 2; Stage 2 cards are the authoritative Model Image numbers and renumber after removal; and each Stage 3 target becomes Image 1 independently while the app supplies the fixed Image 2. Make examples copyable and change the Stage 2 default prompt to an immediately valid Image 1/Image 2 lineup request.

## 2026-10-20 — V1 local workflow prototype

Status: CONFIRMED BY USER / VERIFIED EXECUTION. Replace the earlier generic debug endpoint with one integrated Colligo/FastAPI UI containing three sequential sections: generate a fixed-cup drink, combine selected drinks, and add refractions. Automatically promote Stage 1 outputs to Stages 2 and 3 and Stage 2 outputs to Stage 3, with per-image removal. Batch Stage 3 targets independently. Keep history in memory only, but permit restoring old outputs. Expose rather than lock variant count, size and quality under advanced settings.

Status: CONFIRMED BY USER. Stage 1 always supplies the neutral master automatically. Recipe mode uses the frozen recipe clause. Appearance mode keeps the neutral master first and permits more than one user reference for flexibility, while explicitly retaining Image 1 as sole cup/camera authority. This multi-reference appearance behavior is an unvalidated extension and must not be presented as research-proven.

Status: CONFIRMED BY USER / TRANSPORT OVERRIDE. Use `gpt-5.6-sol` with high reasoning for Stages 2 and 3, overriding the handoff's prior GPT-6 Astra recommendation. Use direct Foundry-vended OpenAI for the prototype because it is verified on this Pluto box; defer the intended Firefly 3P Gateway migration. Azure and FAL are unnecessary fallbacks in the completed prototype.

Status: VERIFIED IMPLEMENTATION DECISION. Copy the whole deployment V1 package byte-for-byte into the app and verify every prompt/image hash during worker load. Disable OpenAI SDK retries. Omit `input_fidelity` because a live Sunburst call returned HTTP 400 `invalid_input_fidelity_model`; do not retry or substitute models. Defaults follow the V1 package: one high-quality PNG, 1024×1536 for Stage 1 and 1536×1024 for Stages 2 and 3. The low-quality live smoke is integration evidence only.

## 2026-10-20 — Recipe-driven fixed-cup research and direct transport

Status: RESEARCHER RECOMMENDATION, NOT USER APPROVAL. Eleven jobs complete and published: shared-master conditioning is the next review candidate because all seven anchored recipe outputs retain approximate vessel/view geometry and only 1–2 px sampled edge drift, while three text controls change the rim/taper/base and show 19–26 px drift. No deterministic correction was applied and exact preservation is not proven. Stop before the 12-job ceiling rather than use the final slot without a new question. Hooman should review the canonical master/camera and appearance differences before combining or inventing recipes. Retain all controls, repeats and master provenance. Revisit if the master pose is rejected or new recipes cause drift.

Status: CONFIRMED BY USER. Develop a text/recipe interface using the supplied Norway pilot recipe book and clean originals; background image references are allowed. The leading criterion is the same cup, viewpoint and orientation to the ground across all drinks. Recipe combinations/new recipes come after this works.

Status: RESEARCHER DECISION. Use one shared neutral master derived from the clean cup family, with a text-only control on three contrasting recipes; initially cap at 12 image submissions including preparation. Recipe amounts and visual appearance conventions are separate fields. No claim that a system prompt guarantees exact shape; if geometric enforcement is needed, show raw and processed outputs separately. No target drink photo is passed individually for recipe generation. The amber original informs the common master, so any amber test is in-family/in-source, not held out. Revisit master choice if pose/shape validation fails or Hooman selects a different canonical camera.

Status: CONFIRMED BY USER / VERIFIED EXECUTION. Test direct `llm.get_openai()`, not Azure; a real Sunburst edit succeeded after access restoration. Use the requested exact direct model for the new research branches. This supersedes the temporary FAL-only transport boundary, while existing FAL samples retain their provider labels. Corrected group-composition reruns use original V1/V2 systems and nine cases; multi-cup refraction has a separate 20-iteration ceiling and actual Astra/high judging. Gallery changes preserve all branches and use a serialized fresh-baseline merge.

## 2026-10-20 — Upright orange replacement and combined FAL experiments

Status: CONFIRMED BY USER. Continue FAL. Replace the leaned-back orange source with `/mnt/localssd/mixology/ref_inputs/TCCC–Crafted-Sept-2026.png`, replacing the seven listed composition outputs. Dependency inspection also found the same old source in the single-drink V3 orange result; apply the user's broad replacement instruction there too. Old results are recoverably archived outside the gallery before canonical outputs are replaced. The two never-generated old-source plans are hidden from the gallery. Future source mappings use the new verified PNG.

Status: CONFIRMED BY USER. Develop a separate system/tab combining drinks and V3-like refractions. Supplied arrangement examples were generated internally and are NOT customer-approved outputs or lighting authority. Preserve each cup; refraction hue follows liquid color/opacity and direction follows one key. This supersedes the prior deferral of merging composition and refraction, while leaving the frozen source prompts unchanged. FAL generation and publication to the existing authorized gallery continue within the requested workflow.

Status: RESEARCHER BOUND. GPT-5.6 Sol at xhigh owns eight source replacements; root integrates the combined branch and shared documents. Combined V1: five cases, including two-/three-/five-cup layouts and a mirrored lighting test. Two V2 staggered follow-ups add one parallel-direction sentence after observed splaying, reaching seven total. V2 does not consistently fix direction and is not promoted. Source identities remain recognizable, but mesh and some shape drift remain; no physical-optics or pixel-fidelity guarantee. Revisit only after user review.

## 2026-10-20 UTC — Azure gateway recovery retry

Status: CONFIRMED BY USER. Retry GPT Image through Foundry Azure credentials after the new Pluto cluster IPs and stage/dev resync were reported fixed. Use the Pluto hostname, not the unreachable corporate hostname.

Status: VERIFIED ACCESS / UNRESOLVED DEPLOYMENT. Stage Azure credential vending and authenticated model listing now work. Exact Sunburst generation still returns HTTP 404 `DeploymentNotFound`; the gateway deployment list contains image deployments only for GPT Image 1 and 1.5. Treat model-catalog presence as distinct from deployment availability.

Status: RESEARCHER BOUND. Do not downgrade to GPT Image 1.5 without Hooman's explicit choice. Preserve the two sanitized failed probe records; no customer call, prompt experiment or gallery change is authorized by this access retry. Revisit after Sunburst is deployed/advertised or the direct Foundry OpenAI route is selected.

## 2026-10-20 UTC — Two- and three-cup example-matched combinations

Status: CONFIRMED BY USER. Add two- and three-cup combinations, trying to match the supplied examples. Retain the separate composition-only stage and existing gallery history.

Status: RESEARCHER BOUND. Five new samples using unchanged composition V1: cola + amber lineup and shallow stagger; red + orange + amber lineup; orange-front and amber-front shallow staggers. These cover the distinct pairings and principal arrangements in the supplied cream-topped generated examples. Original single-drink PNGs alone are model inputs. Examples are displayed as comparison evidence, not passed as image inputs: their lighting and known proportion errors must not become identity authority. Preserve source viewpoints/full syrup details rather than matching the examples' lighting, crop or oversized foreground geometry. Customer PDF straw-drink examples are not these same drinks. One Sunburst/high/1536×1024 image and one advisory Astra critique per case; no prompt revision or refraction merge in this batch. All 23 existing outputs and five live gallery files were snapshotted before edits; live/local gallery bytes matched. Latest AWS broker attempt remains HTTP 403, while existing AWS credentials work and authenticated fal pricing checks return 200.

## 2026-10-20 UTC — User-authorized fal fallback while cluster allowlisting is pending

Status: CONFIRMED BY USER. Hooman requested allowlisting for the new cluster and authorized using fal.ai with credentials in `/mnt/localssd/temp_creds.txt` meanwhile. This authorizes the pending image research through fal, not a gateway policy change or production deployment.

Status: VERIFIED ACCESS / RESEARCHER BOUND. Official fal schemas expose exact Sunburst `openai/gpt-image-2.5/sunburst/edit` and a vision router accepting exact Astra `openai/gpt-6-astra`. Read-only authenticated pricing requests succeeded with the first supplied fal key. Retain frozen refraction V3 and composition V1, source ordering and high quality. Run one refraction first to verify inference, then the remaining four plus two composition cases. Retain the previously defined ceiling of at most two targeted composition follow-ups; no refraction V4 or wholesale prompt changes. Use new `v3fal` / `v1fal` run IDs, preserving all original outputs and prepared Foundry-route cases.

Status: RESEARCHER TRANSPORT DECISION. The user's explicit fal API choice supersedes the prior imagegen-CLI transport for these new runs only; do not modify the bundled CLI. Fal's router does not expose the previous Astra reasoning-effort setting or backend model snapshot in its output schema, so do not claim transport equivalence or returned-model verification. Request model fallback disabled, one image per call, safety checks enabled, no automatic submission retry, payload-history storage disabled, and generated-file lifetime 24 hours; record these requested controls without asserting backend enforcement. Send original image data URIs, store exact local references/prompts/hashes and queue IDs under home, and download all outputs for the existing access-controlled gallery. Credentials remain outside the project and gallery.

Status: OBSERVED FAILURE / BOUNDED FOLLOW-UP. The first Astra request rejected `reasoning=false` with HTTP 400, before any image call. Retained the failed queue/error record and retried the same system/user/images once with mandatory `reasoning=true`; both model stages then completed. All seven initial images completed. Direct and advisory review identified a taller/slimmer cola in the composition lineup. Test one generic sentence against uniform cup-height/base simplification in composition V2, once per arrangement (two further images, reaching the predeclared cap). All other composition inputs/settings remain unchanged; refraction V3 remains frozen. This is a single-sample prompt hypothesis, not evidence that the new clause will necessarily improve fidelity.

## 2026-10-19 — Restart recovery and two parallel research branches

Status: CONFIRMED BY USER. Run the five finished-drink images in `/mnt/localssd/mixology/ref_inputs` through the existing refraction system; exclude `white_cap.png` and `empty_cup.png`. Separately develop a multi-reference grouping system preserving each cup's proportions, with side-by-side or grouped arrangement controlled by the user prompt. Put composition in a new tab of the existing gallery. Combining composition with refractions is deferred.

Status: RESEARCHER BOUND. One frozen-V3 refraction image per finished drink; single-cup style preset 003 is unpaired lighting guidance only. Composition starts with two all-five-drink cases (lineup and shallow stagger), with at most two targeted follow-ups after measured failures. White background, no added refractions in composition, no forced common cup silhouette, no claim of pixel-exact preservation from a prompt. Source family dimensions are not physically measured. The supplied specification supports this bounded preparation; unprovided physical tolerances remain unknown.

Status: CONFIRMED BY USER. SSD data is volatile and must not be the sole copy of needed research work. Keep the repo and durable files under `/home/colligo`; warn if a real checkout lies elsewhere. Optional image backups may use `/sensei-fs/users/hshariati/claude_backup`. Implemented in the single shared playbook and global pointer, without moving or deleting any repository.

Status: VERIFIED RECOVERY DECISION. Source snapshot is copied under `/home/colligo/mixology_data`; all 157 previously published files are recovered from S3 and hash-verified. Preserve old absolute-path provenance via a compatibility symlink into durable home storage, not a rewrite of historical records. New Python environment also lives under home. Fresh model credential vending returns HTTP 403; prepare prompts and inputs but do not pretend model runs completed. User was asked to restore authorized Foundry access or identify an existing token file, never to paste secrets or AWS keys in chat.

## 2026-10-19 — Local Colligo endpoint POC

Status: CONFIRMED BY USER. Build a local-only Colligo pipeline in `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/mixology` that accepts one or more reference images plus a user prompt, exposes variant count, size and quality in the debug UI, defaults to one 1080p-class output, and sends both copied system V3 and the user prompt to GPT Image 2.5. Deployment, CAI, metadata and production hardening are deferred.

Status: VERIFIED IMPLEMENTATION DECISION. Azure's deployment-style `images/edits` route returned HTTP 404 for `gpt-image-2.5-sunburst` despite listing the model. The local POC therefore uses `foundry_aws_gateway.llm.get_async_openai()`, the direct Foundry-vended route already verified for this model. FAL was not needed. Revisit the transport when Firefly 3P Gateway integration begins.

## 2026-10-19 — Corrected-input V3 reruns and gallery narrative

Status: CONFIRMED BY USER. The cleaned overhead input from 013 looks good; keep it beside other inputs. Remove the one-off input-preparation experiment from the main HTML narrative, while retaining its underlying files. Also correct cropped group input 023 by removing external shadows/light from customer output 027. Run V3 on both corrected inputs without changing the system prompt. Show the resulting refraction runs together with all actual prompts and model inputs.

Status: CONFIRMED BY USER. Keep the previous outputs until Hooman reviews the replacements; deletion is deferred, not authorized now. The no-cleanup-experiments-in-HTML request overrides the earlier all-generations gallery preference only for these one-off input corrections, not for actual refraction experiments.

Status: RESEARCHER EXECUTION BOUND. One corrected-input overhead refraction output and one corrected-input group refraction output; one group cleanup edit followed by source-preservation work as needed. User explicitly requested fan-out: independent overhead, group and gallery-code tasks delegated; parent integrates shared state and publishes. No V4, broad quality sweep, or cleanup-history destruction.

Status: VERIFIED EXECUTION UPDATE. The three initial workers and two compact-context retries returned no usable messages or artifacts before interruption. The parent resumed their bounded work directly, overlapping model execution with gallery/documentation work. No background workers remain assigned to mutate shared files; no duplicate image generation was needed.

## 2026-10-19 — Freeze system V3; repair the overhead input

Status: CONFIRMED BY USER. Leave the refraction system at V3 for now. Preserve the system prompt and prior 12-output gallery; this is a working-version decision, not a blanket acceptance of every generated sample. Gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html .

Status: CONFIRMED BY USER. Image 012 is an unsuitable input because it is cropped. Build a new overhead input from customer image 013 by removing its external shadows/refractions while keeping cups, contents and its existing framing. Do not overwrite image 012 or relabel historical runs as if they used the replacement. Do not run a new refraction-prompt iteration as part of this cleanup.

## 2026-10-19 — Refraction batch handoff

Status: RESEARCHER RECOMMENDATION, NOT CUSTOMER-APPROVED. Prefer system_v3 plus a fixed view-specific style image as the starting preset. Rationale: compact request contract and observed quality comparable to V2; no proof of statistical superiority. Keep all 12 samples for review. No production rollout or further generation is part of this bounded batch.

Status: RESEARCHER DECISION. Preserve original crop for "Add refractions." A separate final diagnostic uses "Add refractions and show the full cups." It addresses the visible crop difference in the strongest accepted pair without silently changing the default. Revisit after the user reviews both policies.

Status: RESEARCHER ASSUMPTION. Publish only this requested gallery to the existing TCCC enterprise bucket under a new dated Mixology prefix, based on the customer PDF's TCCC branding. An optional bucket preference was asked but not answered. The prefix was verified empty. No objects are deleted and no bucket policies are changed.

## 2026-10-19 — Refraction system-prompt experiments

Status: CONFIRMED BY USER. Use the customer PDF and curated examples to develop a system prompt for simple user requests. Use GPT Image 2.5, generate/judge/revise across several iterations, and publish all generations with complete system/user/image prompts and reference inputs using render-s3-gallery.

Status: CONFIRMED BY USER. Pair 023→027 is strongest. Pair 012→013 is positive. Output 015 is negative because the light looks like veins; favor the lightning-like branching effect. Outputs 003, 002 and 029 are positive, but exact inputs for 002/029 are not established. Never promote a conjectured pairing to ground truth.

Status: RESEARCHER DECISION. Begin with a direct customer page-5 baseline and a text-only Astra rewriter on three representative inputs; use "Add refractions." as the runtime user request. Use Sunburst/high/auto and preserve all versions. Approximately 10–12 images is the initial bound, with actual failures driving revisions. Scope/model/corpus are sufficiently specified to proceed; default-reframing and publication-bucket preferences were asked asynchronously. Baseline preserves crop until clarified. Revisit if output evaluation shows insufficient receiving surface or systematic style failure.

## 2026-10-19 — Initial access check

Status: CONFIRMED BY USER. Establish access to GPT Image 2.5 using Foundry, load research rules, and review the three named projects. User supplied `/mnt/localssd/temp_creds.txt` for credentials if needed; never copy secret values into the project.

Status: RESEARCHER DECISION. Use `gpt-image-2.5-sunburst`, the exact image-edit deployment used in KDP and confirmed by current official documentation. Test one synthetic reference edit at 1024×1024, low quality. Alternative: listing models only would not prove inference; a customer-image batch would require missing inputs. Revisit model/quality once the styling brief is available. No conclusion about customer image quality follows from this probe.

Status: RESEARCHER DECISION. The current request is sufficiently explicit for a bounded model-access check under section 2 of the research playbook. Defer the five creative-research questions until the styling task is defined; do not invent answers or begin broader experiments. The model-access specification does not require those answers.

Status: RESEARCHER DECISION. Follow the user-requested Foundry API path and existing imagegen CLI rather than its default built-in transport. Obtain credentials from the gateway; do not repurpose research credentials for coding/productivity configuration. Reversible: environment and outputs are isolated to this project.
