# V6.3 full160 on exact PR4417 and PR4523

As of 2026-11-10T18:35:10.264932+00:00. Status: generation running.

## Outcome and scope

USER-CONFIRMED: reuse30 completed V6.3 images per pipeline and generate exactly130 additional per pipeline.
The same frozen160 texts,16 prepared product views, model contract and pinned PR sources are used.
No new text generations, image resampling, judgments, commits or production deployments are included.

VERIFIED counts in this checkpoint:

```json
{
  "v6_3_pr4523": {
    "expected": 160,
    "reused": 30,
    "new_expected": 130,
    "new_done": 42,
    "failed": 0,
    "pending": 88,
    "done": 72
  },
  "v6_3_pr4417": {
    "expected": 160,
    "reused": 30,
    "new_expected": 130,
    "new_done": 44,
    "failed": 0,
    "pending": 86,
    "done": 74
  }
}
```

Live report: https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/gallery/index.html

## Evidence and reproduction

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/study_manifest.json`: immutable160 universe, exact reused/new partitions and provider settings.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/execution_commands.json`: reproducible native-runner commands (never run a second worker).
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/execution_status.json`: single tracked generation state and PID.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/input_audit/summary.json`: actual input materialization; no model calls.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/publication_receipt.json`: remote download/hash evidence for each owned allowlisted asset.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/s3_access.py`: refreshed user-supplied credentials through the frozen safe assignment parser; never executed or persisted.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/preserved_files.json`:2854 existing immutable evidence files checked before/after execution.
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/tests.log`: focused partition, no-duplicate-POST, reuse-binding and publication-ownership checks.

## Limitations

The source texts are actual GPT-5.5 r1 outputs from15 successful bank services and one recognition false failure,
accepted unchanged under corrected r2 recognition. This is not a fresh16/16r2 reliability trial.
Style references and stochastic outputs are not pair-controlled. Exact product is instructed, not guaranteed
pixel-locked. Remote native job artifact exports and product bytes/version are verified, but remote raw
model-request image hashes/all image settings are not exposed. No image-quality significance claim or
judge verdict applies. Existing generation records retain their original study/run SHA-256 bindings.

## Recovery and next exact step

The attached generation and bounded progress publisher are active. Do not start a duplicate. Read current execution_status/progress_status and native jobs if interrupted.
Known jobs resume without a duplicate POST. An ambiguous submit_started event without a saved job blocks
continuation and requires investigation; it is never blindly resubmitted. All original failures are retained.
