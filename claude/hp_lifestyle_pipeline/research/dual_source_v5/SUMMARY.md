# V5 — smart brief and source messaging

As of 2026-10-27. Status: V5 research candidate and reviewed160-text pilot complete; runtime reliability has known limitations. No V5 images started or authorized.

## Contents
- [Decision and contract](#decision-and-contract)
- [Evidence and exclusions](#evidence-and-exclusions)
- [Method and stopping rule](#method-and-stopping-rule)
- [Artifacts and next step](#artifacts-and-next-step)

## Decision and contract
USER-CONFIRMED: freeze V4.1 while awaiting C-Tech feedback. V5 takes smart_brief + source_messaging + camera_tag and returns20 prompts. Preserve V4.1 style, tone, detail vocabulary, six environments, fixed-camera limits and device/color boundary. Return both source and C-Tech scores, ordered by source score.

USER-CONFIRMED: equal authority/use useful information, not a50/50 average. Implement source score as the sum of per-component maxima from independently justified document components. A sparse document has no penalty; repeated evidence counts once. The earlier50/50 pilot aggregation is archived, and the same160reviewed scene texts are re-scored/reranked without pretending they were regenerated. Source-first ordering, C-Tech tie-break; frontend can re-sort. Scores are model rubric judgments, not measured semantic cosine or image-quality predictions.

## Evidence and exclusions
VERIFIED:10 originals,5 folder-based pairs, copied from volatile /mnt/localssd to durable home with byte hashes. The six TXT files are plain text, not JSON. Runtime wraps text (or structured document JSON) in an outer JSON contract. Full extraction and source provenance remain available.

Three clean laptop/printer pairs: Elitebook, Deskjet2955 and Laserjet (the printer briefs have explicit product-spec caveats). Cashmere is a product-identity conflict: non-Flip brief versus Flip source messaging. Test it separately as a conflict case, using compatible common environment cues rather than merging device-dependent claims. Modric is an all-in-one desktop, excluded from this laptop/printer pilot by explicit user decision; its source evidence is preserved.

Detailed inventory: findings.md; machine evidence: inputs/normalized/pair_reviews.json and extraction_manifest.json. Original documents are source data, including authoring directions and qualified assumptions, never instructions to the rewriter.

## Method and stopping rule
Root authors the V5 prompt; GPT-5.6-sol high handles mechanical extraction, runner and validation. Copy unchanged V4.1 camera registry and normalized18-reference library. Explicitly keep previous versions frozen.

Bounded pilot: four laptop/printer pairs × close/wide =8 banks ×20 =160 texts; Cashmere's40 are labeled conflict cases. First run two banks (Elitebook wide, Deskjet close) as integration checks, then the remaining six if protocol and substantive behavior are suitable. GPT-5.5, medium reasoning, strict JSON schema, max24000 completion tokens, at most2 concurrent calls. Retry transient transport failures only; preserve every successful response, including failures. No unbounded semantic resampling. If needed, one documented prompt correction wave may follow observed failures; never hide first-call performance.

Checks: input projection completeness, schema/exact count, camera/device boundaries, ordinary C-Tech language, source citation authenticity and meaning, independent document score arithmetic, source-first sorting, C-Tech reference classification, six-category coverage and distinct texts. Finalization may correct arithmetic, missing-evidence component zeros, deterministic camera metadata and ranking; it must not rewrite scene prose or invent evidence. Root reviews semantic behavior after mechanical checks. A source-rich brief may change category frequencies; compatibility, not exact historical frequencies, is required. A source-ablation comparison would be necessary to attribute improvements causally to the brief.

Publish a text-only review/distribution with both full sources, each prompt, both scores, explanations and camera tags; export all prompts and top6 per bank. No images until user asks. Preserve first-pass/repaired distinctions. Freeze V4.1 at116 completed images +4 terminal timeouts, not120 completed or image-quality approval.

## Artifacts and next step
- Runtime: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5
- Pilot: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027
- Original/extracted inputs: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/inputs
- Frozen V4.1 manifest: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/freeze_20261027/manifest.json

Next: Hooman reviews the published V5 text/distribution and confirms weighting or pairing corrections. Do not generate V5 images or promote the runtime to replace frozen V4.1 without that next decision.

## Pilot findings and method amendment

VERIFIED two40-text integration waves (r1/r2) are preserved. R1 revealed wide background overcounts; some initial rejection codes were validator mistakes caused by the new plain-text contract, fixed with13 regression tests. Under corrected validation, the initial Deskjet close bank passes mechanically; Elitebook does not. R2 improved feasibility but still had isolated camera/evidence errors. Root additionally found substantive over-scoring of generic stationery and source paperwork imported into all20 Deskjet alternatives, which weakened the requested C-Tech diversity.

RESEARCHER DECISION: make one final bounded runtime revision r3 with explicit source-score calibration and at least six C-Tech-led alternatives that omit source-specific work materials. Run its eight cases once, preserve every response, and stop tuning after that wave for review. No unbounded semantic retries. The earlier one-correction stopping rule is amended because r2 exposed a new substantive failure; this is not evidence of successful raw-model reliability. Report remaining issues rather than silently passing or replacing them.

## Completed r3 pilot and limits

VERIFIED:8 final-revision GPT-5.5 responses,20 candidates each,160 texts, no transport retries. Returned modelgpt-5.5-2026-04-24; median successful call111.10seconds. Earlier r1/r2 contain4 additional responses/80 superseded texts. After deterministic arithmetic/ranking/camera-metadata finalization,3/8 r3 banks passed mechanical validation. Five failed because of excess background demands, missing explicit supports or nonverbatim evidence. Independent review also found inflated source-context credit and misclassified C-Tech adaptations. This is not a production-ready reliability result.

Root separately prepared a reviewed160-text set with18 scene edits and253 individual field changes, including evidence/score/debug corrections. Original model output is untouched. All8 reviewed banks pass mechanical validation; an independent replay verified byte-identical outputs/logs and confirmed all14 independent review findings were addressed. The review set demonstrates the intended output, not unaided runtime behavior. Scores remain uncalibrated rubric judgments even after review. No V5images.

Reviewed distribution: Home40, Office40, Café22, Creative Studio22, Education20, Gaming16. Current equal-authority mean source score43.438 and C-Tech score77.794; scores measure different criteria and should not be compared as if on one calibrated scale. Top6 per8bank export has48 prompts. The V4.1 reference comparison is descriptive: input documents and candidate counts differ.

Links (published separately by the tracked publisher):

- Review: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/gallery/index.html
- Distribution: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/gallery/index.html#distribution
- Current system prompt: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/runtime/system_prompt.md
- Content-pinned system prompt: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/runtime/by_sha256/9f070b31198c62a5a56e3fda1d2d7356af55569fdd818aa2aaa9addb9f2e3619/system_prompt.md
- Compact prompts JSON: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/data/prompts_only.json
- Prompt text: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/data/prompts_all.txt
- Top6 per bank: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/data/prompts_top6_per_bank.txt

Publication VERIFIED:139 objects,39,750,693 bytes at initial publication; S3 GET hashes and Content-Type match. Follow-up runtime README/status metadata updates are separately recorded. Corporate-browser visual rendering was not tested in this session. Publication manifest: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/publication.json.

## Confirmed scoring update

The user confirmed equal authority/use useful information and exclusion of Modric. Finalizer and validator now use per-component maxima (15 regression tests pass). All160 reviewed texts remain identical to the earlier reviewed set; only source scores/order change. The earlier50/50 runtime/review are hash-archived under experiments/r3_50_50_runtime and experiments/r3_reviewed_50_50. review_scoring_policy.json identifies original scene-generation versus current runtime hashes. Two new20-prompt actual GPT-5.5 checks exercise each one-document-only direction, outside the160-text pilot.

Final scoring check VERIFIED: two actualGPT-5.5calls/40 separatecandidate texts under currentSHA9f070b31198c62a5a56e3fda1d2d7356af55569fdd818aa2aaa9addb9f2e3619. Both one-document directions showed zero empty-document components and exact max-per-component aggregation; source-only Elitebook reached60 and brief-only Deskjet reached90, establishing no50point ceiling from a missing document. Neither bank passed every semantic check: one retained close-up background demand; the other misclassified two C-Tech relations. Some abstract-work activity/context credit remains debatable. This verifies scoring arithmetic/authority behavior, not overall production reliability. No more GPT calls; no V5images.

Updated independent check confirms all160reviewed texts unchanged, all8updatedreviewedbanks pass, all14priorreviewfindings remainaddressed, and allscores/ranks matchtheconfirmedformula. The separate40smoketexts are diagnostics, not partof160or48exports.

Final publication VERIFIED after confirmed scoring update:199 objects/41,660,174 bytes GET/hash/content-type checked at the same review URL; no V5scene text changed during rescoring. V4.1 still matches all84 freeze hashes. Git contains the frozen V4.1 checkpoint and V5 code/evidence; publication manifest records object recovery paths.
