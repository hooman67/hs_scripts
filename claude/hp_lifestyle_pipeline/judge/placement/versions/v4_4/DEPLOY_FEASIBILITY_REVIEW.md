# V4.4 deploy-feasibility review

Final static review: 2026-11-05 PT. No V4.4 model calls were made during this review.

## Decision

V4.4 is cleared to run **Gate A only**: three independent repeats of the six reused labeled development cases. This clearance does not extend to the frozen ten, the full 160, production deployment, or a claim of judge accuracy.

The current protocol freeze is:

- SHA-256: `56504eb067c93a0ea1bd6d6a96aee5e7137d46228cc8395f5822c841e884c7dd`
- 19 frozen files
- zero hash mismatches at final review
- zero files under the V4.4 run directory before launch
- local tests: 28 passed

Any source, prompt, schema, scoring, geometry, runner, manifest, preflight, test, or design-boundary change invalidates this clearance and requires a new freeze and review.

## Verified contract

- The scout and verifier are both called for every scoreable run. The verifier is called with an empty proposal list when the scout has no positives.
- Every scout positive, including severity 1, requires independent verifier confirmation.
- Severity is restricted to 1–3 throughout schemas, prompts, local validation, and scoring.
- Confirmed findings require visible or partial observability and a positive region. `uncertain` cannot be hidden. A hidden rejected proposal requires a visibility limit and reconciles to unobservable.
- Six ambiguous tests enforce polarity-consistent scout subtypes. The verifier independently emits the observed subtype for confirmed findings.
- Public issue codes and scores are application-derived.
- Neither `cause_id` nor `same_cause_as` exists in the scout schema, verifier schema, or score path. Injecting either field is rejected by strict validation. Penalties depend only on frozen application-owned groups in `scoring.py`.
- One shared repair is permitted across both stages, with at most three total model requests. SDK retries are disabled. Refusal and non-`stop` completion are technical failures.
- Exhausted failures return the public numeric error sentinel with `score_valid:false` and `verdict:review`.
- Cache reuse requires matching input and protocol hashes; stale results fail closed.
- Runtime payload tests show that record IDs, camera tags, candidate ranks, expectations, and human labels are not sent to the model.
- Response IDs, timestamps, latency, token counts, model identity, input fingerprint, prompt/schema/code hashes, and derived-result hash are persisted.
- Scout and verifier wire schemas are compact and prose-bounded. Completion caps are 9,000 and 4,000 tokens.
- Gate A verifies the protocol freeze before every model invocation and on resume, persists every result, and aborts immediately after the first error or non-scoreable result.
- The six-case preflight resolves all six records and verifies immutable input, crop, and overlay hashes.

## Gate A interpretation and stop conditions

Gate A is a development regression and consistency check. Its cases were used during development. Before any broader run, inspect all 18 outputs against the frozen case expectations and require the expected verdict/issue behavior across all three repeats. Report inconsistency and technical-failure rates separately.

Stop Gate A immediately if:

- strict structured output is rejected by the gateway;
- a response is truncated or refused after the one shared retry;
- any frozen hash changes;
- any result has `status != ok` or `score_valid:false`;
- the returned model does not match the requested GPT-5.5 deployment;
- the actual request count exceeds the frozen bound.

The 9,000/4,000 completion caps and current strict-schema dialect have not yet been exercised against the live route. Gate A is their bounded compatibility canary. A failure requires diagnosis and a newly frozen protocol, not an ad hoc continuation.

## Fresh-ten claim boundary

The ten-case selection was frozen before any V4.4 call, has distinct scene hashes, and excludes the six gate cases and prior calibration anchors. Runtime does not load or send the expectation file.

It is nevertheless **not prospective validation**. The cases and expectations were selected from an existing annotated corpus, selection was label-informed, and implementation authors could read the labels. It is historical held-out development evidence only. A production-readiness claim requires an implementation-frozen blind set whose labels are unavailable until predictions are immutable, or newly generated cases labeled after prediction.

## Residual risks after Gate A clearance

- The score is a deterministic policy score, not a calibrated probability. Static groups intentionally deduplicate related tests, but their weights and verdict thresholds still need empirical calibration.
- The six-case gate is too small and too reused to estimate accuracy, false-positive rate, subgroup performance, or production reliability.
- The live route may expose strict-schema or token-cap behavior not covered by mocks. Gate A fails closed on those conditions.
- Visual accuracy remains the primary unknown. Passing the software contract does not show that GPT-5.5 correctly sees placement defects.
