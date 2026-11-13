# Independent audit — two-pass placement results

As of 2026-11-05, the completed 20-case diagnostic and 64-case extended runs are internally consistent. All 84 manifest IDs are unique and disjoint across the two runs. Their 168 baseline/compact stage joins match the generated-image hash, twin hash, scene-prompt hash, product type and `scene_generation` stage in the manifests. All 504 referenced source request/response/result hashes and all 168 copied raw-response hashes match the current bytes. Raw response observations equal the judgments retained in the combined artifacts, and current scoring reproduces every combined judgment.

## Metric audit

The saved `evaluate.py` outputs reproduce exactly from the current artifacts and current evaluator.

| Run | Check | Baseline V2 | Combined | Result |
|---|---:|---:|---:|---|
| diagnostic-v2 | verdict expectations | 5/11 | 6/11 | +1 |
| diagnostic-v2 | issue-any expectations | 3/15 | 6/15 | +3 |
| extended-v1 | explicit verdict labels | 2/2 | 2/2 | retained |
| extended-v1 | agreement with frozen V2 | 56/56 by definition | 55/56 | one loss |
| extended-v1 | issue-any expectations | 2/6 | 4/6 | +2 |

Diagnostic verdicts changed from pass to fail for `cashmere__laptop_FrontLeftMedium__p6` and `tassel__printer_FrontCloseUp__p5`. Extended verdicts changed from pass to fail for `cashmere__laptop_FrontCloseUp__p5`, `magic__printer_FrontCloseUp__p3` and `tassel__printer_FrontLeftMedium__p6`. The first is the single lost V2-agreement case; the latter two are the two gained issue-any cases. The extended explicit passes remain passes.

The issue-any number has a material interpretation limit. The evaluator unions every emitted issue code and asks whether any expected code appears. It does not check severity, confidence or visibility and does not penalize extra codes. One diagnostic match, `tassel__printer_FrontLeftMedium__p5`, is based on severity-1 medium-confidence codes, so mild findings count. Seven of the ten matched issue checks across both runs also contain extra, unscored codes. No current match relies on low confidence or unobservable evidence. The available mappings cannot establish whether the companion codes are correct; incorrect or unsupported companions would not reduce this metric.

## Annotation separation and provenance nuance

All 168 saved stage requests use only the five canonical target inputs. Recursive searches found zero target annotation field names and zero exact target annotation scalar values in those requests. The evaluated target's own comments and expectations were withheld.

The broader phrase “no human comments were passed” would be inaccurate for baseline V2. Baseline V2 intentionally sends frozen development visual-anchor guidance, including user-confirmed training examples. Target-identical anchors are excluded for the two diagnostic regression targets. Compact V3 sends no anchors. The accurate claim is that target annotations were withheld from both stages.

The saved request snapshots do not serialize image bytes: target inputs are absolute local paths, image metadata contains path plus SHA-256, and no completed two-pass request contains a data-image URI or long base64-like string. The runners construct base64 data-image payloads only in memory for the API call. Future wire-payload snapshots should omit or redact those bytes.

## Privacy scan

A bounded pre-audit-write scan covered 3,107 UTF-8 files and 53,118,396 bytes under V3, including the then-present live-run snapshots. Pattern counts were: PEM private-key header 0; AWS access-key format 0; Slack token 0; bearer credential 0; JWT 0; AWS signed-URL signature 0; named JSON secret value 0; exact secret-bearing JSON key 0. One data-image/base64 marker was a source-code literal; serialized completed request snapshots had 0. No credential serialization was found.

The scan is time-bounded because the new160 runs were live. It is a pattern scan, not proof about arbitrary opaque strings.

## Reproducibility limitation

Combined results record the current combiner and policy hashes, and every recorded value matches. Each stage request's protocol hashes are uniform and match current runner/scoring code and the saved prompt/schema snapshots. The evaluation files do not record an evaluator hash or evaluation creation time. Exact recomputation with the current evaluator establishes present consistency, but it cannot prove which evaluator bytes originally created those files.

Full exact case lists, manifest hashes, source-run counts, protocol hashes and machine-readable checks are in `audit.json` in this directory. Existing tests pass: 9/9 with the pytest cache disabled.
