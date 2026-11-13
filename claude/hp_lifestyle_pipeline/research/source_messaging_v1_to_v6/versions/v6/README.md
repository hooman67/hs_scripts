# V6 writer: validated text-evaluation candidate

As of 2026-10-30. Hooman approved the retained ordinary props in the edited Markdown, subject to the text/face guidance. The compiled catalogue has 237 entries; removed and uncertain items stay unavailable. The accepted immutable composite `v6-approved-20261029-final-r44` contains actual GPT-5.5 output for all 16 dual-source/camera banks: 160 candidates and a source-ranked 96-prompt set. Five selected banks passed on their initial semantic call and eleven passed after the one allowed complete-bank repair. No scene text or model-authored field received a human edit. The composite replays each bank through one frozen final runtime; it is text/runtime evidence and a reviewed eval artifact, not an image-quality result or a guarantee that every fresh 16-call batch will pass.

Current approval provenance: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/approvals/20261029-r2/provenance.json`. Use `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/approved-20261029-r2.catalog.json`. The r2 internal catalogue revision adds the already approved chalkboard menu to both `chalkboard` and `menu` repetition groups; the user-approved Markdown is unchanged. The compiler preserves both originals and creates a separate decision CSV. C-Tech's rule prefers visual alternatives to text/faces; important menus require non-legible background text, and art/photographs should avoid portraits. Runtime text checks cover explicit unsafe requests; they do not prove image compliance.

Accepted evaluation and exports: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44`. The composite source selection is recorded at `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/composite_source_map_v12.json`; it selects unchanged successful banks from r18, r22, r24, r32, r34, r35, r39 and r42. Earlier revisions and failed banks remain audit evidence and are never copied field-by-field into the accepted export.

Canonical design and research status:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/SUMMARY.md`

## Files

All runtime assets are in `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6`:

| File | Purpose |
| --- | --- |
| `system_prompt.md` | Root-authored scene writing, source scoring, C-Tech style, and prop allocation instructions |
| `input.schema.json`, `model_output.schema.json` | Input and raw model JSON contracts |
| `camera_profiles.json`, `camera.py` | Versioned tag/alias resolution and qualitative camera guidance |
| `reference_library.json` | 18 C-Tech reference cores preserved from V5 |
| `catalog.py`, `prop_lexicon.json` | Compile explicit approvals and resolve known prop synonyms/types |
| `validation.py`, `runtime.py` | Local checks, one semantic repair, application scoring/sorting and audit |
| `provider.py`, `cli.py` | GPT-5.5 transport adapter and recorded command-line entry point |
| `approval_pending.catalog.json` | Current review record compiled with zero approved entries; intentionally unusable |
| `tests/` | Mocked provider, schema, approval, repetition, evidence, camera and failure tests |
| `release_manifest.json` | Byte hashes of this implementation checkpoint, including tests |
| `verification.json` | Local verification scope and results; no live-model claims |

## Runtime contract

Input is one JSON object with exactly these fields:

```json
{
  "smart_brief": {"text": "Example input: a home workspace for studying."},
  "source_messaging": {"text": "Example input: support everyday learning tasks."},
  "camera_tag": "laptop_FrontWide"
}
```

Each document may be a string or JSON object, including empty values. The example above is synthetic documentation, not customer data. The camera must resolve to a registered type/tag; unknown tags are errors before a model call. There is no image or product-name input.

Success returns `status: "ok"`, exactly ten `prompts`, `debug`, and `audit`. Each prompt includes `id`, `text`, `environment`, approved `prop_ids`, `score_components` for both documents, exact source `evidence`, source `relationship` and explanation, creative departures, `ctech_reference_id`, `ctech_reference_score`, C-Tech explanation, and camera-fit explanation. The application adds `source_relevance_score` and IDs; the model does not calculate the combined total.

Combined source score = the sum of the higher supported value for each of setting, activity, materials and use context across the two documents. Maximums are 30, 30, 20, 20. This preserves equal authority without penalizing a sparse document. Sort descending by combined source score, then C-Tech score, retaining input order for exact ties. Both scores are model rubric judgments, not calibrated probabilities. The host never changes scene text or creates evidence.

Failure returns `status: "error"`, an explicit error, and audit; there is no usable `prompts` array. Examples: invalid request, empty catalogue, unknown camera, configuration error, provider refusal/failure, or output still invalid after repair.

## Approval and diversity

The clean review menu is:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/PROPS_FOR_REVIEW.md`

The editable decision record is:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/data/prop_candidates.csv`

Only `reviewer_decision=approve` grants inclusion. Blank, `hold`, and `reject` remain excluded. `runtime_allowed` and `status` cannot grant approval. Preserve rejection reasons. Uncertain categories need explicit environment-specific entries before admission; approval of a broad cross-environment category does not silently allow it everywhere. Additional primary computing devices remain excluded by the device boundary.

Compile once after decisions are recorded and pin the resulting catalogue revision in the application. Compilation reads, but never rewrites, the review CSV. Do not run the older review-menu builder over an edited CSV.

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/cli.py compile-catalog \
  --csv /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/approved_props_v6/data/prop_candidates.csv \
  --revision approved-r1 \
  --output /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/approved-r1.catalog.json

python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/cli.py check-catalog \
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/approved-r1.catalog.json
```

The compiler can write an empty catalogue as an audit record; the check and runtime reject it. Every requested smaller prop, selected furnishing and named shelf content needs environment-specific approval. Repetition groups are global across all ten: cup/mug, notebook/sketchbook, chair variants, etc. The primary supporting desk/table and fixed architecture are exempt. One response has no knowledge of earlier camera calls; cross-request uniqueness is outside this input contract.

## Camera handling and references

V6 retains the inherited offline framing/elevation labels and aliases for 122 profiles. It replaces every numeric `max_local_props` / `max_background_details` field with qualitative guidance. The validator has no noun-count budget or all-six-environments requirement. Top-oblique and explicit camera-movement checks remain.

These inherited labels are not a new measurement of corrected render capacity. New or changed views require an offline profile update and evaluation. Registry and reference hashes appear in each audit. The C-Tech library is unchanged from V5, including normalized removal of device/no-hardware/blue-control clauses. Reference props still need independent approval.

## Calls, repair and failure accounting

1. Validate input, approved catalogue, camera, references and JSON configuration before creating the provider client.
2. Send the system prompt plus trusted catalogue/camera/reference assets and user-role source data to GPT-5.5 using strict JSON Schema. The schema enumerates the actual approved IDs.
3. Validate the whole bank. On a semantic/schema failure, make **one** complete-bank repair call with specific diagnostic data. Source text and echoed diagnostic values remain outside trusted instruction messages.
4. Revalidate everything. Return explicit failure if still invalid. No manual patch step, hidden text normalization or unbounded regeneration.

Transport defaults: `gpt-5.5`, medium reasoning, `max_completion_tokens=16000`, 180-second request timeout, no temperature, SDK retries disabled. At most three transport attempts per semantic call for 429/5xx/connection/timeout failures: at most six model HTTP attempts across initial generation plus one repair. Numeric, millisecond and HTTP-date Retry-After headers are respected; waits over 60 seconds or invalid headers return a typed error. Refusal, authentication/permanent request error and model substitution are terminal. An interrupted/timeout request may have been processed remotely; its cost is not guaranteed absent.

Audits distinguish semantic calls from transport attempts, retain returned model, usage, settings, error codes, raw/parsed responses, validation failures, and repair text differences. Input, catalogue, system/schema, camera, reference and lexicon provenance is retained. Generic injected-provider exceptions have unknown transport accounting; the supplied adapter records it. Credential values and raw provider error bodies are not copied.

CLI journals save each request before submission and each response afterward. Existing outputs/journals cannot be overwritten. A partially recorded run must be inspected, not blindly resumed. Application callers of `run_writer` must persist requests/results similarly if they need crash recovery.

## Running after approval

The adapter reuses the authorized Foundry client helper at:
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/scripts/probe_gpt55.py`

The existing GPT-call credentials/configuration must be available outside the repository. For another deployment, inject an equivalent SDK client factory; do not copy secrets or silently substitute models. Python dependencies are in the CLI's inline script metadata. `uv` can create the isolated environment:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/cli.py run \
  --input /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/v6_request.json \
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6/approved-r1.catalog.json \
  --output /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/v6_run_001.json
```

The request file must first exist with the actual runtime input. That command makes paid model calls only after valid approval/configuration preflight. It does not generate images.

Local checks, with no network/model dependency:

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python -m pytest research/source_messaging_v1_to_v6/versions/v6/tests -q
```

`build_assets.py` deterministically rebuilds schemas, qualitative camera data and the copied reference library from the frozen V5 files. It does not rebuild the root-authored system prompt or change approvals. Preserve the checkpoint in Git and compare rebuilt hashes to the manifest before using it.

## Validation limits and release gate

VERIFIED locally: 245 tests pass across the V6 runtime and eval runner. The accepted catalogue contains 237 approved entries, with 3 removed ordinary items rejected and 22 uncertain categories held. Preflight makes zero model calls for empty approval or malformed configuration. Tests include deliberately synthetic outputs to isolate orchestration; they do not establish image quality or visual diversity.

Known-phrase checks detect approval/inventory mismatches and repeated synonyms, but cannot prove that arbitrary free prose contains no novel unlisted object. Exact evidence quoting verifies provenance, not semantic entailment. Camera feasibility, meaningful scene diversity and C-Tech scores remain model judgments requiring evaluation; the runtime does not route them to a human editor.

The bounded GPT-5.5 evaluation is complete. Preserve the accepted catalogue, final runtime snapshot, raw result/call journals, source map and final export together. For a new reliability estimate, run a fresh unseen 16-bank batch and report initial, post-one-repair and explicit-failure rates without selecting across historical attempts. Any system change creates a new evaluated revision. The authorized top-six preview evaluation subsequently completed 96/96 images with corrected product/view renders; that establishes mechanical completion and a review artifact, not automatic visual acceptance.

Downstream image rewriting previously added props/hardware absent from the input. It must consume the approval policy before upstream text checks can imply anything about final image compliance. No V5 files or historical evaluations were rewritten.

Official Structured Outputs guidance inspected 2026-10-28:
https://developers.openai.com/api/docs/guides/structured-outputs/
This supports strict-schema/refusal handling; it does not prove GPT-5.5 reliability on this catalogue or camera task.
