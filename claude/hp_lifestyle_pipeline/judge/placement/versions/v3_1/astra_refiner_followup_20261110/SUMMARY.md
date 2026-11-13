# Astra judge follow-up: three proposals and eight complete system prompts

**VERIFIED2026-11-11:** the resumed synthesis finished01:13:57UTC with normal `stop`, returning three materially different proposals and eight complete system-prompt files. Streaming completed on the first resumed attempt in435.256seconds; no resumed timeout/restart was needed. The exact input/brief/model were unchanged. All64-case visual findings,17 refinements, three criterion-labeled examples, three non-gold controls and22 earlier proposal seeds remain preserved.

**LIMIT:** completion is not validation or promotion. Astra recommends P2's unconditional geometry discovery, with P1 as the lower-change comparator. Parent review found that P1's claimed drop-in compatibility is incomplete: its verifier prompts conflict with the actual runner's component-only contract. That conflict must be corrected before evaluation. No existing judge or scores were changed.

## Contents

1. [Evidence and limits](#1-evidence-and-limits)
2. [Actual complete proposals and compatibility](#2-actual-complete-proposals-and-compatibility)
3. [What the images changed](#3-what-the-images-changed)
4. [Recommendation and stopping point](#4-recommendation-and-stopping-point)
5. [Artifact index](#5-artifact-index)

## 1. Evidence and limits

**VERIFIED, source identity/coverage:** live source retrieved2026-11-10T22:53:07UTC:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/refiner_evals/hp_judge_refiner/hpjr-all-fixable-20261109T225123Z/full_evalset.html

HTML SHA-256 `2d6b41494c071224cc0cf1d85cbecf87c0246560b71473ce52e8361579859abf`.64 cases are32 row families with both runs.192 product/baseline/refined image references resolve to97 unique source PNGs.47 passthroughs are byte-identical baseline/refined pairs, NOT47 successful repairs or judge passes. Original human comments were reconciled against screening and kept separate from generated scope decisions and non-gold qualitative notes.

Astra received high-detail, native-dimension JPEG quality94 derivatives, with no crop/resize, plus unchanged historical source JPEGs. Exact PNGs, hashes, transformations, deduplicated image-to-case bindings, complete messages, SDK/model settings and raw responses are durable. Derivatives are lossy; fine-edge interpretation can remain uncertain.

**VERIFIED, execution:** all four visual responses requested/returned `gpt-6-astra`, reasoning high, normal `stop`; exact64-case and6-historical-record coverage. Successful responses account for512,752 reported tokens, not a billing total. SDK transport attempts are not independently instrumented. Two unsuccessful/unresolved synthesis attempts have unknown upstream completion and usage. No credentials were copied into the project.

The resumed text-only synthesis used Direct OpenAI `gpt-6-astra`/high,32,768 completion cap, streaming,1800s inactivity timeout and zero hidden SDK retries. It preserved20,880 actual chunks and110,465 content characters, ending normally with79,314 reported tokens (55,456 input;23,858 completion, including2,938 reasoning). Five successful returned responses total592,066 reported tokens, excluding unknown failed-request usage. Raw-stream SHA-256 `e98e653ab1f278ee3c9cd8243ab6b2d40eff43b10972a0a9fe1baf3a2c958891`; parsed proposal SHA-256 `1f0b8124ce1506c355562174efe4dbd586e8a7267a51b14796ac28fadb25892d`.

**USER-CONFIRMED:** restart transient timeouts until completion, superseding the earlier one-recovery stopping point. The parent-owned supervisor preserves each attempt, progress heartbeat and partial stream; uses one local call at a time with backoff; and does not retry credential/refusal/token-limit/model/schema failures as though they were transport problems. Streaming worked here; this does not establish the root cause of the earlier non-streaming timeouts. The supervisor exited normally after successful export.

**LIMIT:** source feedback describes baseline images, not refined-image acceptance. Positive buttons, selected/excluded repairs and unchanged status do not establish criterion labels. Historical anchors are E2E diagnostics, not a held-out validation of the original scene-stage judge. New visual interpretations below are Astra's findings, not independently certified pixel truth or measured judge improvement.

## 2. Actual complete proposals and compatibility

These are Astra's actual completed P1/P2/P3 drafts, not the earlier parent grouping of proposal seeds. Original prompt text is preserved unchanged.

| Candidate | Actual proposed change | Compatibility and risk |
|---|---|---|
| P1. Complementary attention, unchanged runtime | Four full prompts: support/geometry-first baseline, use/allocation-first compact, proposal verifier and independent verifier. Both primaries retain all five dimensions; concise contrastive geometry/ownership evidence replaces the r2 trace envelope. | Astra claims unchanged schema/scoring/ensemble, but parent found the verifier contract conflict below. Shared primary misses still bypass additions-only verification. Not drop-in to r2's mandatory trace wrapper. |
| P2. Unconditional geometry discovery | Three full prompts: mutually blind geometry and use/location specialists on every scene, then an image-based reconciler. The final output alone enters the existing deterministic scorer. | **Requires new specialist contracts and replacement ensemble orchestration**, not just new rubric text. Geometry runs even when general use appears fine. Three mandatory calls may increase cost/error exposure; allegations are not automatic failures. |
| P3. Selective hypothesis judge | One full prompt explicitly distinguishes compatible perspective, rigid rotation, support distortion and unresolved evidence. Nine criterion decisions lead to fail/review/pass-visible. | **Changes schema and acceptance/scoring policy.** No weighted score or old consensus. Unresolved/unobservable criteria can force review; higher review volume is not successful defect recall. |

**VERIFIED compatibility issue, P1:** Astra's two verifier drafts explicitly demand full `placement-observations-v3` objects with placeholder unrequested components. The frozen r1 harness instead requires `placement-verifier-components-v1`, with only `schema_version` and requested `components`, and sends that strict schema to the API. These are contradictory output instructions, not a verified drop-in replacement. Do not silently relax the runner or modify Astra's original artifacts to hide this.

Source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/run_judge.py:67-80,146,209-218`, compared with the completed P1 proposal/independent verifier artifacts. The primaries' declared scene-reading field types and component code lists agree with the frozen observation schema; no actual new judge outputs have been generated to validate runtime behavior.

Common safeguards proposed by Astra: preserve harmless chair offset/rotation; do not let good contact/access erase a distinct alignment defect; separately assess printer-on-support and support-in-room; do not require functional impossibility before calling material unnaturalness. Sparse décor, artwork asymmetry, preferred reflections and prop-category preferences should not automatically become placement failures. **Policy clarification, not a silent change:** this last boundary conflicts with permissive bare-staging language in the frozen compact prompt and needs explicit reconciliation in a new revision. Optional styling/architectural review must not silently affect placement scores.

## 3. What the images changed

**ASTRA FINDING, development evidence, not new judge results:**

- `07_cashmere_x_Front_Wide_1`: supports no material alignment defect. Compatible product/table width directions and a shifted chair do not establish reversed/blocked use.
- `07_cashmere_x_Front_Wide_4`: supports the C-Tech material alignment label. Astra identified opposed product/table width-family tendencies in the same tabletop region, despite plausible contact and access.
- `13_elitebook_13_Front_Left_Medium_4`: no consequential placement rotation established, but the labeled malformed table **remains unresolved**. Astra could not confidently localize the impossible connection; a slim member could belong to an occluded rear/additional support. Preserve the C-Tech criterion label and disagreement. Do not manufacture a defect, waive the label or claim a verified pass.
- `10_elitebook_13_Front_Wide__run1`: exposed carpet beneath the far-side chairs supports the missing-support concern. Added legs reduce that appearance, but hidden seat-to-leg joins prevent automatic construction certification. The second run has more occlusion and weaker evidence of true absence.
- `27_tassel_Front_CloseUp__run1`: Astra found a separate rigid printer/table direction-family conflict that persists after puzzle relocation. This offers an additional development example, not unseen holdout evidence.
- Cases19/23: low printer-support concerns can persist after unrelated prop edits. Floor/support/context cues matter independently of good contact and clear controls.
- `25_cashmere_x_Front_Left_Medium__run1`: the left-heavy props are an observable styling preference, while the reported odd legs remain uncertain under cropping, glass/reflections and possible panel/frame ownership.

The three stability controls remain non-gold. Clear visible relationships do not certify hidden legs, full room layout, exact dimensions or global quality. Both r1/r2's required-anchor misses and r2's six historical operational errors remain unchanged.

## 4. Recommendation and stopping point

**ASTRA RECOMMENDATION, unvalidated:** prioritize P2 because it changes discovery coverage, rather than expecting additions-only verification to rescue an unproposed concern. Compare with P1 as the lowest-change attention hypothesis, after correcting its verifier protocol conflict. P3 is conditional on accepting an explicit review workload and a different score/acceptance policy.

Astra proposes diagnostic use of the historical examples and fixed refiner families10/12/19/23/25/27, deduplicating passthroughs and keeping both runs/edits in the same partition. Every supplied family informed this consultation and is development material, not holdout. Its suggested fresh36-image scene-stage review set is a proposal, not an existing labeled dataset or an authorized run.

Future evaluation should pin the actual incumbent, compare identical inputs, label criteria before viewing candidate outputs and report material recall, clean-case false positives, abstention, operational errors, cost and latency. Do not call frozen unpromoted r1/r2 the deployed incumbent. Retain the EliteBook evidence disagreement; no invented defect, label waiver, retry-until-label-match or automatic promotion. P3 review is not credit for detecting a material defect.

**COMPLETED scope:** resumed synthesis, raw response preservation, three proposal/eight prompt extraction, all checked source/predecessor identities and exact raw-stream/prompt comparison. No image analysis was repeated, and no new actual judge evaluation, implementation, publication or promotion occurred.

**Historical failures preserved:** the first non-streaming process was stopped without a response after over20minutes; its1800s/zero-retry recovery then timed out waiting for response headers. Neither returned a model response; upstream completion/usage remain unknown. User authorization subsequently reopened timeout recovery and the same291,586-byte input/unchanged brief succeeded with streaming.

**Next exact step:** deliver the complete proposal bundle and compatibility caveat. Before a separately authorized evaluation, correct P1's verifier contract or explicitly choose a changed protocol, and approve the selected candidate's runtime/policy changes. No further Astra request or model monitor is currently pending.

## 5. Artifact index

- Canonical source/media/feedback manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/evidence_manifest.json`
- Four actual visual reviews, raw responses and receipts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/batches`
- All22 unedited proposal seeds with their batch/source bindings: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/astra_proposal_seeds.json`
- Successful visual identity/coverage audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/visual_completion_audit.json`
- **All eight complete prompts in one copyable text file**, plus unchanged Astra compatibility notes and the parent P1 caveat: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis_resumed_20261111/proposal_bundle.txt`
- Exact individual prompt files: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis_resumed_20261111/proposals`
- Complete structured proposals/recommendation/limitations: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis_resumed_20261111/attempt0001/proposals.json`
- Actual raw chunks, receipt, config and progress: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis_resumed_20261111/attempt0001`
- Completed source/stream/prompt identity audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/completion_audit.json`
- First unanswered synthesis input/config/interruption record: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis`
- Identical-input recovery/config/error record: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra_refiner_followup_20261110/synthesis_recovery`

The replacement-prompt drafts and successful synthesis receipt now exist. No demonstrated quality improvement, new judge evaluation, deployment or promotion is claimed.
