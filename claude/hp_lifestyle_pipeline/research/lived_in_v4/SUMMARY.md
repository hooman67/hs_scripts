# V4: lived-in specificity within fixed camera limits

As of 2026-10-26: **540 final candidates and 108 selected prompts are accepted; Hooman stopped the bounded image run at 60 completed, 7 pending remote job records and 48 selected rows without records.** Both prompt downloads and the last progressive gallery snapshot are published and S3 hash-verified. The local generation and publication services are stopped. Already submitted endpoint jobs may finish remotely, but no local process will collect, extend or republish the run unless explicitly resumed. This is a separate V4 experiment, not a promotion over V1 or a modification of V2/V3.

All 18 accepted banks passed automated structure, source-quote, score and camera checks. An independent GPT-5.6-sol high reviewer read all 540 final texts, and root read all 108 selected paragraphs. Five revision-2 responses were rejected/superseded before acceptance (independent extra props or a nonverbatim quote); all raw attempts remain available. The accepted set is not a first-attempt reliability estimate. Text acceptance does not establish image realism or preservation of the reference camera.

## Objective and scope

Hooman reports C-Tech feedback that previous prompts removed the details that make places feel inhabited and worked in. Produce 540 new candidates and a reviewed 108-row image selection, then launch those 108 images. Keep nine original source messages, 30 candidates for each matching close/wide camera, four original render references, tag-only runtime, fixed 0–100 source-relevance rubric, and labeled creative departures. miniPC remains excluded. Café and Creative Studio are native V4 categories alongside Home, Office, Education and Gaming. No blue policy. The earlier eval-hub upload remains cancelled.

## Evidence and interpretation

The October DOCX is the highest-priority style source; the lifestyle workbook is read only in column A. Source copies are preserved under the backed-up project. The reproducible audit in `data/lived_in_specificity_audit.json` finds a median 45.5 words in ten October examples versus 25.5 in the 108 selected V3 texts. Its lexical cue indicators show fewer consumption/pause, personal and background details in V3. These are text indicators, not validated realism or image-quality metrics. The comparison supports the reported loss of specificity; it does not prove that longer text alone improves images.

Root re-inspected all four render images. Their existing offline limits remain unchanged: laptop close-up zero props/zero fixtures, printer close-up one compact prop/zero fixtures, both wide views up to three props/two background anchors. The registry is intentionally byte-identical to V3. Enrich the state and arrangement of allowed objects rather than adding objects to tight views. Laptop close-ups can carry only surface-use traces and light; their room recognizability and activity diversity are inherently limited.

The V4 prompt asks for coherent moments: marked-up or dog-eared work, a cooling drink, casual placement, familiar furnishings and subtle material wear. It does not require all scenes to look damaged or dirty. Wide scenes use complementary signs of work/life; tight scenes use only what their local crop can contain. Numerical object ceilings are conservative design choices, not measurements of physical capacity. Downstream rewriting may still introduce details and framing changes; retain exact requests, rewritten prompts and reference bindings to distinguish stages.

The first four actual GPT-5.5 probes improved descriptive specificity but exposed extra incidental objects in wide scenes, paperwork-heavy printer alternatives and a few implausible surface treatments. Root revised the instructions to count independent supports such as napkins/rags, reserve ten prop-capable alternatives outside the dominant source artifact family, and keep use traces physically plausible. Two lexical rejections (`phone-room`, furniture `desktop`) were not evidence of visible hardware; the new wording avoids their ambiguity. Preserve all 120 superseded texts under the eval's `text_probe_revision1` directory; do not include them in the final 540.

Semantic counting distinguishes a compact homogeneous group or ordinary container contents from an extra independent prop: two small play tokens can be one group, and a dish's mints or keys can be its contents. A mug plus a coaster and a spoon plus a saucer still each require two slots. Do not reject tiny incidental contents as though they required another workstation. Likewise a café checkout receipt is part of a distinct break activity, not necessarily transplanted administration; retained deviations/ambiguities are reported separately from hard geometry and evidence errors. Independent review also notes repetitive surface-use-plus-light endings and occasional compliance-oriented phrasing. Richer detail does not eliminate these style limitations.

The final audit finds median lengths of 43 words in V4 versus 25 in V3 and 45.5 in the ten October examples. Median lexical nonlighting cue counts are 4, 3 and 8 respectively; the V4 mixture includes 270 tightly constrained close-ups. These indicators support richer text, not proven image improvement. The broad surface-use-plus-light construction remains in 499/540 texts. One laptop-wide bank has nine strict source-artifact-omitting alternatives against the prompt's ten-candidate guidance; root retained this minor exception for the bounded user eval because its study activity is still distinct and its scenes remain feasible. Do not claim perfect compliance with every stylistic instruction.

Final native category counts: Office 211, Home 92, Education 55, Café 65, Creative Studio 78, Gaming 39. These are observations, not quotas. The final audit and manual lineage are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/lived_in_v4/data/V4_FINAL_MANUAL_PROSE_AUDIT.md` and `v4_manual_prose_review.json`; root selection review is `root_text_review.json` in the same directory.

## Reproduction and acceptance

Version directory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v4`.
Eval directory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026`.
Image run directory: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026`.

Compile with `scripts/build_system_prompt.py`, then run the eval README workflow. GPT-5.5 uses medium reasoning, strict JSON schema, 24,000 maximum completion tokens, at most two concurrent calls and 100 transient-only retries. Preserve every raw response and failed/rejected attempt. The deterministic finalizer can repair evidence-free scores/ranking and camera debug metadata; it never rewrites scene text. Review actual prose, source relevance, device exclusions and camera limits after automated checks. Select six per bank across rank strata, review all 108, and freeze approval hashes before images.

Image settings match the earlier bounded V3 eval: the exact four original reference PNGs, 2560×1440 preserving 16:9, seed 42, n=1, Gemini 3.1 Pro rewriting and 50 steps. Close/wide banks are independently generated and are not identical scenes at different cameras. Comparison with V3 is an iterative evaluation, not a controlled paired experiment. Text acceptance is not C-Tech image acceptance. No expansion beyond 108 images is authorized here.

The same endpoint and request settings are used; the remotely served model revision is not independently pinned. The runner verifies reference PNG bytes and durable upload bindings before submission. Eight generation workers and two upload workers run under a detached tmux supervisor. Known pending jobs resume from their IDs; ambiguous submissions and terminal failures are not blindly resubmitted. The supervisor has a twelve-invocation bound and records its state. The publisher refreshes the gallery every 120 seconds when inputs change.

Exact resume/status commands:

```bash
bash /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/launch_generation_and_publisher.sh status
bash /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/launch_generation_and_publisher.sh resume
```

Do not rerun `run_gpt55.py --rebuild-only` or `select_candidates.py` after approval unless deliberately starting a new selection revision: those commands reconstruct pending-review artifacts and invalidate the frozen approval. The final snapshot is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/final_text_evaluation.json`.

Prompt SHA-256: `83cc51a0b139f62a176982f60082070c1686fef3bd780a9e16cf95459178b349`.
Approved map SHA-256: `d247ca2bbae1f1a0ad460476c1277cb42e12b26d2ec0ea0fd16da0a03802fcd8`.
Approved selection SHA-256: `2c9f23f5fc6bed0d802198b1a793e3099761e69d156e63846deed2b43cf87f1e`.
All-540 export SHA-256: `ae881cccb9eecb434b500dac2314401a6de921298cc7b7084267e8fbe01f7c6b`.
Selected-108 export SHA-256: `8242870a03cb02adab34e78c160d7f7fbf6006004124078f17e52c34ae909af1`.

Across both internal prompt revisions, 27 successful GPT-5.5 responses reported 751,258 tokens. The 18 final accepted responses account for 510,076 tokens. This includes rejected/superseded text work and excludes image-endpoint work. Accounting snapshots are linked by hash in `final_text_evaluation.json`.

Published gallery: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/gallery/index.html

Published prompt-distribution analysis: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/gallery/index.html

The distribution report applies the same frozen MiniLM embedding revision and ten scope-adjusted October C-Tech references as the V3 analysis. It reports V4's six native environment categories directly, without post-hoc relabeling: Office 211, Home 92, Creative Studio 78, Café 65, Education 55 and Gaming 39. The median nearest-reference cosine similarity is 0.469835, the normalized environment entropy is 0.907199 and there are no exact or canonical duplicate prompt groups. These are descriptive text-corpus measures; they are not calibrated quality thresholds or evidence of visual diversity. The durable report source is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1`, and the reproducible local build is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reports/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1`.

All 540 prompts: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/generation_prompts.json

Selected 108 prompts: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/generation_prompts_selected.json

V3 preservation checksums are recorded in `data/v3_before_v4_manifest.json`. All research code, records and needed artifacts live under `/home/colligo/hs_scripts`; `/mnt/localssd` is only a volatile convenience copy. The official GPT-5.5 guidance snapshot used during drafting is `data/gpt55_official_guidance.md`.

Final preservation check passed all 312 recorded V3 files unchanged. Gallery/static JavaScript/data checks, contract/export checks, runner and supervisor regressions passed. Browser/Node execution was unavailable and is explicitly marked skipped; publication was verified through S3 object sizes and hashes, not a claimed browser screenshot.

The later distribution report received an independent offline rebuild and JavaScript syntax check. All nine report content artifacts were byte-identical across the two builds; the source manifest differed only by the expected absolute output path. Publication then verified all ten remote objects by GET SHA-256, HEAD size/content type/SHA metadata and an exact S3 key allowlist. The publication record is `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/publication.json`.

Early image spot-check: a completed printer close-up passed selected-text equality, original-reference hash/blob binding, seed 42 and 2560×1440 checks. Root viewed its original PNG and output; apparent framing/orientation look similar in that single example. The slightly chipped coaster requested in text becomes a visibly broken edge in the image, so downstream amplification of wear remains a review question. Preserve this finding in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/early_output_spotcheck.json`; it is not full image acceptance. The progressive gallery already contains initial completed outputs.
