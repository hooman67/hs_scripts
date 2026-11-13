# Placement judge V3.1 — C-Tech alignment and furniture geometry

As of 2026-11-10 UTC. **Calibration gate NOT MET: the fresh V3.1 model still
misses the required row07_4 alignment failure and row13_4 geometry failure.
Fresh historical comparison is complete; do not promote this research candidate.**
This version derives from frozen V3, not V4 or V4.x. Existing active versions and
root project state are not changed.

## Contents

- [Outcome](#outcome)
- [Contract and bounded method](#contract-and-bounded-method)
- [Actual Astra consultation](#actual-astra-consultation)
- [Implementation and compatibility](#implementation-and-compatibility)
- [Fresh historical comparison](#fresh-historical-comparison)
- [Sources and disagreements](#sources-and-disagreements)
- [Testing and reproduction](#testing-and-reproduction)
- [Artifact index and remaining limits](#artifact-index-and-remaining-limits)

## Outcome

VERIFIED: actual Direct OpenAI **`gpt-6-astra` / high** returned substantive
image-grounded product-judge advice, not merely an Astra-named file. V3.1 applies
the reviewed chair/alignment/geometry correction to both primary rubrics and
both component-verifier rubrics. Frozen V3 scoring and observation schema are
byte-identical in V3.1; the selected V3 consensus decision functions are reused
without semantic modification. Ten focused offline tests pass.

VERIFIED first anchor outcomes: V3.1 returns pass/100 for all three anchors.
It clears the rejected row07_1 chair allegation, but both primary GPT-5.5
assessments call row07_4 generally aligned despite the C-Tech requirement and
Astra's contrary image analysis. It also does not detect the supplied row13_4
geometry failure. No response was edited, repaired, replaced or repeatedly
sampled until it matched a label. This is a material model-perception limitation,
not evidence that the C-Tech labels are invalid or that V3.1 is calibrated.

| Supplied source image | C-Tech dimension expectation | Fresh V3 | Fresh V3.1 |
|---|---|---|---|
| `07_cashmere_x_Front_Wide_1.jpg` | Do not fail chair/placement alignment; unrelated dimensions not globally labeled | pass / 92.5 | pass / 100 |
| `07_cashmere_x_Front_Wide_4.jpg` | Fail consequential laptop/table alignment | pass / 100 — miss | pass / 100 — miss |
| `13_elitebook_13_Front_Left_Medium_4.jpg` | No placement failure; fail table geometry | pass / 100 — geometry miss | pass / 100 — geometry miss |

Both V3.1 primary branches confidently/partially clear the required defects,
so the preserved additions-only verification trigger does not fire for these
anchors. The consensus stage cannot recover a concern that neither primary
perceives. These independent fresh draws are not a controlled estimate of
rubric benefit; even fresh V3 now accepts the chair case that the old stored
run rejected. Do not equate fewer failures with better image quality or accuracy.

USER-CONFIRMED scope expansion: freshly evaluate **both selected frozen V3 and
V3.1** on every generated output in the supplied historical viewer, and provide
side-by-side JSON/HTML. Live inventory is **32 rows × 4 variants = 128 outputs**,
with 160 image objects including 32 twin paths (16 distinct twin byte hashes).
All **256 case/version assessments completed successfully**, with **530 preserved
successful raw model responses** and zero terminal call/validation failures.
No judge call on the parent's 90 new generations was performed or is authorized here.

## Contract and bounded method

USER-CONFIRMED: loosen chair/laptop alignment, preserve consequential laptop/table
alignment failures, and strengthen visible table/chair construction scrutiny.
Use actual Astra product-judge design consultation. The initial authorization
was limited to three supplied development anchors; the subsequent explicit user
instruction expanded testing to the complete historical viewer for both judges.
There are no new scene images, publication, deployment, commits or pushes.
The supplied E2E images remain out-of-domain diagnostics for V3's scene-stage contract.

Assumptions: C-Tech labels are authoritative for their stated dimensions, not
global positive labels; occlusion is uncertainty, not missing construction; V3's
other criteria and five scoring dimensions should be preserved. Unknowns to
resolve from evidence: exact rightmost variant, live source bytes, available Astra
route, minimal compatible V3 delta, and actual targeted calibration disagreements.
The user's complete specification permits proceeding without additional questions.

Verified storage: the real Git checkout is `/home/colligo/hs_scripts`, under durable
`/home/colligo`, not volatile `/mnt/localssd`.

The three C-Tech anchors run first in the historical comparison, once per version,
and their exact results also serve as the targeted calibration. There is no
separate preferred-response selection, hand-edited judgment or semantic resampling.

## Actual Astra consultation

VERIFIED authoritative calling documents, read before the consultation:

- `/home/colligo/hs_scripts/claude/monitor/ASTRA_FOUNDRY_GATEWAY_HANDOFF.md`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/libs/aws_gateway_client/README.md`

The approved product-evaluation route is
`foundry_aws_gateway.llm.get_openai()`, **not** the shared Azure Astra route.
The call used model `gpt-6-astra`, high effort, 24,000 maximum completion tokens,
600-second request timeout, SDK transport retries eight and concurrency one.
The actual response finished `stop`: 27,571 prompt tokens, 6,879 completion
tokens, 34,450 total. The SDK versions were Foundry gateway 2.0.0 / OpenAI 3.48.0.
Started 2026-11-10 01:18:37 UTC; finished 01:21:51 UTC.

Exact full text input, six original JPEG payload identities (three scene/twin
pairs, without transformations), configuration, source hashes, complete raw
response, visible output and returned-model/usage metadata are preserved under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/astra/attempt_1/`

The consultation received frozen V2/V3 rubric/schema/scoring/consensus context
and exact C-Tech labels. Evaluation calls do **not** receive those target labels,
old viewer judgments, comments, verdicts or the consultation's per-anchor answer.

## Implementation and compatibility

VERIFIED version lineage is **selected V3 consensus-v2**, whose primary branches
were a V2-exemplar assessment and compact V3. This is not a compact-only judge and
not V4/V4.x under another name. V3/V2 source files are read-only and hash-pinned.

The application still selects the highest confirmed positive component, breaking
ties toward baseline. Newly raised compact material concerns trigger a
proposal-aware check plus a names-only independent check. Shared material codes,
minimum severity/confidence and the same uncertainty/fallback decision rules
are preserved. An old baseline result cannot veto the new chair policy because
V3.1's baseline rubric is itself revised and freshly called.

Changes are confined to:

1. Chair pose/centering alone cannot become alignment, excessive reach, missing
   user position or incoherent activity. Genuine obstruction/working-edge reach
   and completely reversed use remain assessable.
2. Consequential laptop/table rotation still fails; slight offsets and perspective
   differences are not blanket failures. Printer-specific squaring/location/
   approach criteria are preserved, not relaxed from these laptop examples.
3. Explicit visible table **and associated chair/stool** construction inspection:
   outline/thickness/joins, attachment/load path, duplicated or disconnected
   supports, and plausible occlusion/projective geometry. Real L-shaped/multi-leg/
   circular/oval furniture is not inherently wrong; hidden legs are not missing.
   Distinct direction families may have distinct vanishing points.
4. Geometry stays in `scale_perspective` (`malformed_support_furniture` or
   `conflicting_perspective`); do not duplicate it under placement/contact without
   independently demonstrated consequences.
5. As Astra advised, retain the historical schema/code registry, but reject
   newly emitted `chair_alignment_conflict` in V3.1 at runtime, without stripping,
   translating or repairing a raw response.

Schema identifier remains `placement-observations-v3`. All five dimensions,
weights 20/30/20/15/15, severity meanings, material veto, caps, coverage, product
mismatch precedence and provisional thresholds are unchanged. V3.1's two primary
branches use the existing full V3 observation schema; the original V3 comparison
uses the original V2 schema in its baseline branch and V3 schema in compact.
The five final dimensions remain directly comparable. V3.1 is distinguished by
its request protocol `placement-judge-v3.1-consensus-v1` and frozen rubric hashes,
not by silently repurposing the observation schema identifier.

Two historical laptop-exemplar guidance strings explicitly clarify that the
old labels illustrate actual reach, not a chair-pose veto. Exemplar image bytes
remain unchanged. Exact source-to-output diffs are under the version's `deltas/`.

No V4 implementation, geometry threshold, angle criterion or score policy is
imported. The visibility safeguard is directly required by the user and Astra;
the judge-local history's cropped-leg false-positive lesson corroborates it.

### Frozen V3 execution adapter

`frozen_v3.py` calls the **original V2 and compact V3 runner code** for fresh
primary responses. The original component-check runners and consensus functions
are reused too. Only authentication uses the documented policy-aware Azure SDK,
and output-specific freeze plumbing is redirected in memory to this evaluation's
hash-bound protocol. Original prompt bytes, schemas, GPT-5.5/high settings,
12,000-token primaries and 6,000-token component checks are retained. The source
files and their historical predictions are never modified or reused as fresh calls.

## Fresh historical comparison

VERIFIED: both judges freshly assessed the same 128 generated image/twin/prompt
inputs. Actual returned model was **`gpt-5.5-2026-04-24`** for every saved response.
The evaluation ran from **2026-11-10 01:26:49 UTC to 02:07:58 UTC**.

| Model verdict distribution — not human accuracy | Pass | Fail | Review | Total |
|---|---:|---:|---:|---:|
| Fresh selected frozen V3 | 107 | 20 | 1 | 128 |
| Fresh V3.1 research candidate | 113 | 8 | 7 | 128 |

There are **22 verdict changes**: 14 fail→pass, two pass→fail and six pass→review.
The remaining 106 comprise 99 pass→pass, six fail→fail and one review→review.
These changes are not adjudicated improvements: target-selected calibration
still fails, independent model draws vary, and the set is not held-out.

V3 made 128 baseline + 128 compact + five proposal-aware + five names-only
successful calls (**266**). V3.1 made 128 + 128 + four + four (**264**).
The 530 saved responses exclude the separate Astra design consultation.
“Zero failures” means zero terminal call/validation failures, not an assertion
about unobservable SDK-internal retries or model correctness.

The export's 256 successful case/version judgments were recomputed from
unedited raw model responses, with exact target-image/input identities, rubric
hashes, schemas, model identity and deterministic consensus verified. The human
HTML has **128 sections, 256 side-by-side judge panels and 256 valid local image
references**, with the three C-Tech labels and failed-calibration banner.
This is structural/local-asset validation, not a browser/IMS-login claim.

## Sources and disagreements

VERIFIED live viewer (S3 read-back; corporate HTML gateway timed out):

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/viewer.html

The preserved live HTML, full asset URLs, timestamps, ETags, content types, byte
sizes and SHA-256 values are under `sources/` and `evaluation/inventory.json`.
No filenames or variants were guessed. In live row 13, the **fourth direct-child
figure**, index 3, is captioned **V16.6 no geometry** and links to:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/hp-data-artifacts/hp-3p-gpt25/hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/img/13_elitebook_13_Front_Left_Medium_4.jpg

USER-CONFIRMED anchor labels:

- `07_cashmere_x_Front_Wide_1.jpg`: no chair/placement failure; not a global pass.
- `07_cashmere_x_Front_Wide_4.jpg`: consequential laptop/table misalignment fail.
- `13_elitebook_13_Front_Left_Medium_4.jpg`: no product-placement failure, but a
  table-geometry failure for the reported L-form/extra legs.

VERIFIED disagreement: Astra corroborated both row07 placement labels and the
row13 non-failure for slight product/edge misalignment, but **could not corroborate
the row13 L-shaped-table/extra-legs allegation from the exact attachment**. It
considered ordinary rear supports, foreground chair members and occlusion
credible alternatives. The C-Tech geometry-fail label remains authoritative
supplied feedback; no invented visual rationale or forced model failure is added.
Direct local image inspection was limited to the three supplied anchors, not
every image in the full model evaluation.

Access attempts are retained: corporate HTTPS timed out; the shared `aws-creds`
workflow was invoked with `--no-write` and failed on its legacy broker; the
documented gateway's read-only S3 client succeeded. Shared credential files were
not modified, and no credential values were printed or saved in project artifacts.

## Testing and reproduction

VERIFIED offline: `offline_tests_final.xml` contains **10 passed** focused tests,
covering schema-history/new-emission consistency, independent alignment/geometry
vetoes, unknown cropped supports, mild offsets, exact V3 consensus corroboration/
disagreement behavior, immutable source observations, input-label exclusion,
verifier semantics and the frozen V3 legacy-schema adapter. All Python files
compiled successfully. Earlier nine-test evidence is retained separately.

Use the approved Artifactory index and policy-aware Foundry SDK:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
umask 077
mkdir -p "$PWD/judge/placement/versions/v3_1/.work"
export TMPDIR="$PWD/judge/placement/versions/v3_1/.work"
uv run --python 3.12 \
  --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --with beautifulsoup4 --with requests --with jsonschema --with pytest \
  --extra-index-url https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
  python judge/placement/versions/v3_1/run_comparison.py --workers-per-version 4
```

The comparison command resumes saved successes and terminal failures, never
replaces a failed judgment or changes a frozen protocol. Do not delete the
existing run to seek preferred labels. `build_comparison.py` recomputes all
successful cases from unedited raw responses with **no model calls**:

```bash
uv run --python 3.12 --with 'foundry-aws-gateway[llm]>=2.0.0' \
  --with beautifulsoup4 --with jsonschema --with requests \
  --extra-index-url https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
  python judge/placement/versions/v3_1/build_comparison.py
```

`--allow-partial` explicitly exposes pending/errors for integration during the
run; it does not invent scores. The existing protocol freeze is immutable.
`build_version.py` reproduces the reviewed rubric transformations and verifies
frozen output identity, without calling a model.

## Artifact index and remaining limits

All paths below are under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3_1/`

- `SUMMARY.md`: canonical implementation, evidence, uncertainty and exact next step.
- `astra/attempt_1/`: exact actual consultation input/config/raw and visible output.
- `reviewed_rules.json`, `build_version.py`, `prompts/`, `deltas/`: auditable minimal
  rubric delta and exact source transformations.
- `implementation_provenance.json`, `protocol_freeze.json`: model/code/source
  lineage, frozen sources and checksums; no V4 baseline substitution.
- `release_status.json`: machine-readable failed anchor gate and explicit
  non-promotion; no change to other active-version statuses.
- `sources/manifest.json`, `evaluation/inventory.json`, `sources/img/`: source
  labels/URLs and original bytes; images are ignored by Git but durable locally
  and recoverable from preserved S3 URLs.
- `evaluation/runs/{v3,v3_1}/`: exact per-case inputs, requests, prompt/schema
  snapshots, raw model responses, failures and deterministic ensemble output.
- `evaluation/comparison.json`, `evaluation/comparison.html`: machine-readable
  side-by-side export and local human report for parent integration, not published.
- `evaluation/anchor_calibration.json`, `evaluation/evidence_audit.json`: targeted
  label comparisons and unedited-raw-response/recomputation verification.
- `evaluation/report_validation.json`, `evaluation/runtime_packages.json`:
  completed HTML/consumer checks and actual Python/SDK dependency versions.
- `evaluation/progress.json`, `evaluation/run.stdout.log`,
  `evaluation/run.stderr.log`: resumable coverage and failures.

UNVERIFIED: generalization, calibrated thresholds and false-positive rates.
These are reused, user-selected development examples, not held-out accuracy.
The actual source stage is E2E; runtime uses V3's required `scene_generation`
literal solely as an explicitly recorded compatibility adapter. No source-stage
equivalence is claimed. No automatic acceptance or other active-version promotion.

**Stopping point:** the implementation and requested historical comparison are
complete, but the required visual-anchor correctness is not achieved. The parent
can incorporate/link the verified `evaluation/comparison.json` and
`evaluation/comparison.html`; neither was independently published.
Retain V3.1 as **not promoted**. Any different geometry observer/rubric experiment
must preserve this failed calibration rather than overwrite/resample it.
Do not score the 90 new generations without separate explicit authorization.
