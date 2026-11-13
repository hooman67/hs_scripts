# Research and validation protocol

As of 2026-10-13. Decision: what system prompt reliably maps production source JSON into compatible environment prompts without conflicting with the digital twin?

## Source hierarchy and evidence

Hooman's explicit constraints govern. For style and device-detail evidence: October DOCX > compatible supplied workbook examples. Only column A of Eval-Set_Lifestyle-Photography_wSKUs.xlsx may be consumed. Use source messaging JSONs for the actual input contract and grounding; never smart briefs. Use official OpenAI documents for model-specific API facts and the shared GPT-call helper for authorized execution. Label evidence VERIFIED, ASSUMED, UNVERIFIED, or USER-CONFIRMED with date and scope.

## Batches and dependency order

1. Inventory, parse and hash all allowed input files; retain every origin, identify exact duplicates and substantive variants. Parse references with paragraph/cell provenance. Completion: every candidate accounted for, no smart-brief contents consumed.
2. Characterize prompt style, device mentions, scene families and KSP usefulness. Compare strict device omission with category/action-only wording; preserve conflicting examples. Completion: concrete device policy plus evidence ready for Hooman's required approval.
3. After approval, author a compact self-contained system prompt and output schema. Explain KSP count, fallback, source variants, permitted invention, and concise audit metadata. Do not request hidden chain-of-thought.
4. Run each distinct supplied source on actual GPT-5.5, preserving original JSON, exact system text, model/deployment, settings, full response and available usage/model metadata. Add bounded edge cases for empty/unhelpful input, overlapping KSPs, misleading instructions in data and out-of-scope settings.
5. Validate JSON structure and references, counts and supported environment families; manually assess every generated prompt against the references, source fidelity, product boundary and variety without enforcing empirical frequencies. Revise only on observed failures and rerun affected/full checks as appropriate.
6. Product v2: investigate mismatches among v1 source environment prompts, downstream rewritten prompts, and rendered images; then author and validate an isolated camera-aware revision against frozen v1. The former BLUE candidate is out of scope and recoverable only as history from Git commit `9810dc07`.

## Stopping and limitations

### V3 staged diversity evaluation, 2026-10-23

Decision: can broader, relevance-ranked candidate banks improve useful visual diversity without relaxing style/device/camera requirements? Competing explanations: weak source cues, the V2 KSP count cap, repeated exemplars/object choices, restrictive framing, and downstream rewrite homogenization. Audit these separately. Preserve V2 as evidence; do not assume its outputs deserve the highest score automatically.

Produce18 tag-only GPT-5.5 responses from the same nine sources × close/wide of the matching product type,30 candidates per response. Use fixed source-scoring anchors, exact field evidence, explicit creative-departure labels and per-prompt camera budgets. Hard gates are valid JSON, evidence validity, device boundary and feasible camera scope. Review diversity semantically, including visible material/light distinctions under close crops; different setting labels alone do not demonstrate visible variety. No target corpus-frequency matching.

Select six candidates per response across the relevance range (108 total images) after text acceptance. Preserve every candidate, selection rationale, rejected attempt, input, exact prompt/schema/model settings and downstream debug. Independent close/wide banks are source/stratum comparisons, not paired identical scenes. Publish a new full-input gallery, never overwrite V2. Stop/drain V2 only at V3 readiness and record all completed/pending states. Do not launch beyond108 images without a new decision. Text relevance scores are uncalibrated rubric assessments, not image-quality predictions.

Text-distribution analysis uses all540 frozen candidates. Report categorical counts/entropy, exact and canonical duplicates, lexical pairwise/nearest-neighbor overlap, recurring n-grams and semantic nearest-neighbor cosine. Compare with the ten actual sample-prompt paragraphs from the authoritative October DOCX, excluding headings/template instructions. The primary comparison removes device prefixes plus blue/no-hardware clauses deliberately outside V3; preserve both original and normalized reference text. Use frozen MiniLM revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, TF-IDF word unigram/bigram cosine and a PCA visualization. Treat all metrics as descriptive: no calibrated acceptance threshold, and no text metric establishes visual diversity. Stratify by environment, source relationship, rank band and camera view to expose reference-set and framing confounds.

For presentation, derive six `display_environment` categories while retaining every frozen canonical family: only explicit café and physical studio settings split from canonical Office. Bind the mapping to the exact540-row export hash/key set, publish candidate-level rules/triggers, and use the same mapping in the image gallery, distribution report, analysis JSON and CSV. Do not rewrite historical GPT output to implement a reporting taxonomy.

Stop collection when the supplied finite corpus is fully accounted for. Stop text iteration once all required inputs and bounded edge cases pass defined requirements and manual review, or report a concrete unresolved failure. Text review does not establish downstream image quality. Do not use aggregate word counts or keyword checks as sole evidence of compatibility.

## Reproducibility

Keep one canonical summary with linked evidence, machine-readable manifests, extraction scripts, prompt/schema and raw run artifacts. Record source checksums, exact duplicate policy, all errors and output-count denominators. Preserve full inputs next to outputs in the review artifact. Keep secrets out of files and terminal output.

## Camera-aware V2 bounded batch, 2026-10-22

Question: can the same source yield a suitably local scene under a fixed product-camera view, without runtime image input? Compare rich source text across tight/medium/wide/top-facing presets and unknown/incompatible controls. The initial named-product exception design was superseded by the final type-only contract; Magic/Messi are different device types and all laptop shapes share conservative type-camera limits. Cover every distinct production source at least once, without running the full source × type-camera matrix. Preserve original input wrappers, returned GPT-5.5 model/usage/timing, exact prompt/schema hashes, JSON/evidence checks and manual detail-count/geometry review. Stop text iteration when requirements pass or a concrete unresolved failure remains; image fidelity requires a separate controlled generation batch.

Competing explanations for old mismatches: client upload misbinding, gallery joins, downstream rewrite composition, and image-model preservation. The audit established misbinding for eight baseline-0016 rows; those are excluded from camera/model analysis. Correct joins and printer-aware rewrite in baseline-0018 weaken the swap hypothesis but do not isolate rewrite versus image-model causality.

Latest same-day contract correction: Messi is miniPC, and the runtime has no product_name. Use only source_messaging plus compact ProductType_CameraName, with conservative type-level profiles. The initial 22-case batch is archived as superseded (19/22 complete audit passes). The active revised batch has 24 cases, retains all nine source inputs, and tests miniPC separately plus explicit aliases and unknown future types.

Completed final bounded batch: 24 selected cases, 39 prompts, with two rejected initial scenes preserved and regenerated under the same prompt. Primary and selected audits are separate; selected passes do not measure first-call reliability. No camera-V2 image run has started.
