# V3.1 r2 — bounded failed-anchor correction

As of 2026-11-10 UTC. **CALIBRATION GATE NOT MET — DO NOT PROMOTE.**
The sole authorized r2 revision and single six-case calibration are complete.
It still misses the required laptop/table alignment and table-geometry failures.
**No full128 r2 evaluation was launched. All r1 artifacts remain unchanged.**

## Contents

- [Outcome by criterion](#outcome-by-criterion)
- [Actual Astra analysis](#actual-astra-analysis)
- [The single revision and compatibility](#the-single-revision-and-compatibility)
- [Bounded method and evidence](#bounded-method-and-evidence)
- [Integration and source access](#integration-and-source-access)
- [Artifact index and reproduction](#artifact-index-and-reproduction)
- [Stopping point](#stopping-point)

## Outcome by criterion

USER-CONFIRMED: the supplied C-Tech labels apply to their stated criteria, not
every dimension of an image. VERIFIED below are actual model outputs, **not**
human accuracy or a claim that fewer failures means better judging.

| Exact source case | Required placement/alignment outcome | r2 placement/alignment | Required geometry outcome | r2 geometry | Overall r2 |
|---|---|---|---|---|---|
| `07_cashmere_x_Front_Wide_1` | No chair/placement failure | severity0, no codes — met | Unlabeled | severity0; not certified by the label | pass/100 |
| `07_cashmere_x_Front_Wide_4` | Material laptop/table conflict | severity0, no codes — **MISSED** | Unlabeled | severity0; not certified by the label | pass/100 |
| `13_elitebook_13_Front_Left_Medium_4` | No placement failure | severity0, no codes — met | Material malformed table/supports | severity0, no codes — **MISSED** | pass/100 |

Three preselected stability controls also returned pass/100, with severity0 in
alignment/construction: cropped Cashmere close-up `_2`, cropped Tassel close-up
`_1`, and ADF printer wide `_1`. Neither false missing-leg nor new chair-axis
penalties appeared. These controls were selected from frozen V3/r1 agreement and
inspected for visibility risks; they are **not independently human-certified gold**.
The exact selection and criterion expectations were frozen before Astra/r2 design.

Both r2 primary branches still call row07_4's axes compatible. Their more
structured trace does not establish correct pixel correspondence: one branch's
alignment finding cites only one width boundary for each object, and explanations still
appeal to perspective without recovering the supplied material conflict. The
contract checks schema/reference consistency, not visual truth or reliable
boundary localization. No material compact additions were raised, so the
unchanged consensus trigger called no verifiers. It cannot recover an unperceived
defect.

Row13's geometry remains an unresolved source-specific **label/evidence
disagreement**. Actual Astra again could not identify an impossible L join or
genuinely duplicated/disconnected supports in the exact fourth image. That is
not proof that the supplied source mapping or C-Tech label is wrong. The label
was not waived, transformed into invented evidence, or relabeled as a pass.

## Actual Astra analysis

VERIFIED: Direct OpenAI **`gpt-6-astra` / high**, called through the documented
`foundry_aws_gateway.llm.get_openai()` mechanism. The authoritative handoff and
gateway README were read. No substitute model or Azure quota workaround was used.

The consultation received all six exact scene/twin pairs, the actual twelve r1
primary observations, r1 rubrics/schema/scoring, prior Astra disagreement, and the
frozen criterion labels. Started **04:56:18 UTC**, finished **05:00:29 UTC**;
finish `stop`, 52,545 prompt tokens, 8,304 completion tokens, 60,849 total,
including 4,608 reasoning tokens. Config: high, 24,000 maximum completion tokens,
600-second timeout, eight transport retries, concurrency one. No failed Astra
attempt or semantic resampling occurred in this r2 continuation.

Astra independently reaffirmed row07_4's corresponding-width-family conflict but
could not corroborate row13's alleged malformed geometry. It recommended one
procedural evidence-contract amendment, **not** another vote, trigger, threshold,
model or scoring change. Its substantive input/config/raw output/metadata are
preserved under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/r2/astra/`

## The single revision and compatibility

R2 adds a mandatory evidence-first envelope to each existing model role:
boundary inventory, corresponding width/depth comparisons, tabletop outline/
thickness/joins, owned member connections/occlusion, and separate alignment/
construction findings with evidence references and counter-evidence.
The same concise general instruction precedes all four untouched r1 rubric
bodies. There are no image IDs, expected target labels, copied anchor coordinates,
angle thresholds or per-image exceptions in judge instructions/runtime logic.

The versioned outer contract is `placement-evidence-envelope-v3.1-r2`. Its nested
`observation` retains the historical primary `placement-observations-v3` schema
or existing component-verifier schema. Schema definitions are explicitly hoisted
to the envelope root so historical `$ref` resolution remains valid.
Scoring source/schema bytes, five dimensions, weights, severity rules, product
validity precedence, material veto, caps, primary/verifier roles and budgets,
trigger/consensus/fallback rules remain unchanged. Established material trace
findings cannot disappear into non-material components; invalid output is rejected,
not repaired or resampled. Raw envelope and exact nested observation are both saved.

Selected lineage remains **frozen V3 consensus → r1 C-Tech semantics → one r2
evidence contract**, not V4/V4.x. Source-to-output diffs and function-equivalence
checks are in the provenance artifacts. The independently frozen protocol binds
63 dependencies; a second execution freeze binds selection, gate driver and tests.

## Bounded method and evidence

VERIFIED: one fresh calibration, **05:05:18–05:10:31 UTC**, three case workers.
All six ensembles completed, **12 successful raw responses**, zero terminal
call/validation errors. Every returned judging model was
**`gpt-5.5-2026-04-24`**. Settings remain GPT-5.5/high, 12,000-token primaries and
6,000-token verifiers; only primaries were triggered. Twelve focused offline tests
passed. Every r2 ensemble was recomputed from unchanged raw responses.

Judge inputs contain only the canonical five fields and original pixels, without
control roles, C-Tech labels, r1 verdicts, prior outputs or Astra's case descriptions.
Source stage remains `e2e_comparison_output`; `scene_generation` is the same literal
validator adapter used in r1. This is an out-of-domain diagnostic, not concealed
scene-stage evidence.

Storage is the real durable `/home/colligo/hs_scripts` checkout. All **3,386 r1
manifest-indexed files**, including its original comparison, report, freeze,
raw outputs and judge index, passed before/after hash checks. R2 changed no existing
file outside its own new directory. No root docs, V2/V3/V4 status/source, writer,
generation folder, credential file or service was edited.

## Integration and source access

The final comparison contains all **128** original inventory records and reused
frozen V3 results. Exactly **six** contain new r2 judgments; **122** have
`v3_1.status = "not_run_gate_blocked"` and null verdict/score/components.
No r1 prediction substitutes for an unrun r2 result. The failed calibration did
not authorize a full128 r2 run.

Schema: `placement-v3-v3.1-r2-side-by-side-v1`. Top-level keys:
`schema_version`, `generated_utc`, `source_viewer`, `inventory`, `versions`,
`claim_boundary`, `calibration`, `source_url_availability`, `records`, `summary`.
Record keys preserve the original source/image/prompt fields, `v3`, `v3_1`,
`verdict_changed`, `changed_dimensions`, `ctech_anchor_label`, and add
`calibration_role`, `criterion_checks`. Complete r2 judge objects add
`model_returned` and per-role `evidence_envelopes`; statuses are `complete`,
`error`, or `not_run_gate_blocked`. Detailed keys/hashes are in `INTEGRATION.json`.

The HTML distinguishes **overall verdict** from **placement/alignment** and
**geometry** criterion outcomes, including the two explicit misses. It labels r2
unpromoted prominently. All **256 image src attributes are full original supplied
Foundry gallery URLs**: copying the HTML into `public/judge/comparison.html` or an
iframe requires no local fixture paths or asset rewrite.

Availability limitation: all six no-added-auth HTTPS probes from this Pluto host
ended in `ConnectTimeout`. Full original URLs are preserved, but unauthenticated/
public/browser availability was **not verified**. Original downloaded bytes and
hashes are available locally; previous r1 read-only S3 retrieval provenance remains
unchanged. No independent publication occurred.

## Artifact index and reproduction

Canonical machine comparison:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/r2/evaluation/comparison.json`

Canonical human comparison:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/r2/evaluation/comparison.html`

Other necessary artifacts are the frozen calibration manifest/execution, actual
Astra receipts, protocol freeze, r2 runtime/trace contract and build recipe,
`calibration/results.json`, raw `calibration/runs/`, raw-response
`evaluation/evidence_audit.json`, `evaluation/report_validation.json`,
`implementation_provenance.json`, `release_status.json`, `INTEGRATION.json`, and
`ARTIFACT_MANIFEST.json`, all beneath this same r2 directory.

Offline reproduction of the export requires only the preserved files and
`jsonschema`; `build_comparison.py` makes no model calls. Running it changes
generated timestamps/hashes, so repin any regenerated derivative.
The executed offline command was pytest on `test_r2.py`, with cacheprovider disabled;
the original XML result is frozen. The calibration driver refuses reuse of its
existing run directory. **Do not remove outputs or resample these anchors.**

## Stopping point

USER-CONFIRMED stopping rule applies: calibration still fails, so stop. R2 is
unpromoted; there is no approved final V3.1 replacement. No new-generation judging,
full128 r2 run, deployment, commit/push or publication occurred.

The cheapest unresolved evidence step is a human annotation locating row13's
claimed impossible join/extra supports on the exact preserved source, plus an
explicitly authorized different perception approach for row07's persisting false
clear. This is a future decision, not a third revision or call authorized here.
