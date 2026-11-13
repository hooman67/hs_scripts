# V5 dual-source text pilot

Canonical method/findings: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/SUMMARY.md.

Runtime candidate: /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v5.

The current manifest pins8 source/camera calls and160 prompts. Cashmere is an explicit mismatched-product case; Modric desktop is excluded. All inputs are durable under research/dual_source_v5; runtime wrappers preserve complete text. Twelve total GPT-5.5 responses include four superseded r1/r2 integration calls. Currentr3 normalized model validation passed3/8 banks. reviewed_prompt_cases.json is a separate root-reviewed set with18 scene edits and253 loggedfieldchanges; it is not raw model output. Allreviewedbanks pass validation and independentreplay. No V5images.

Rebuild the review without any model call:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/build_reviewed.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/build_review.py --accepted /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027/reviewed_prompt_cases.json --baseline /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/accepted_prompt_cases.json
```

After fetching AWS credentials with the shared helper, source its env file in the same shell as `uv run --script` on publish_review.py. Publisher uploads dependencies before HTML and GET-verifies each object; it never generates images or calls GPT. Existing model calls are immutable and reused by request hash. Runtime promotion requires a new bounded reliability evaluation, not hidden retries of this bank.

USER-CONFIRMED scoring update: equal authority/use useful information; no50/50average. review_scoring_policy.json distinguishes original160scene-generationSHA45f207... from updatedscoring runtimeSHA9f070.... Existing reviewed160scene texts are unchanged and reranked by sum of per-component maxima. Two separate20-prompt checks in scoring_contract_smoke validate either-document-only behavior; both pass arithmetic but retain unrelated semantic errors. Modric explicitly excluded. The archived50/50review/runtime remains under experiments.
