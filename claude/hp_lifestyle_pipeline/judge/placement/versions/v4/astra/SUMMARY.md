# Astra-assisted natural-placement judge V4 research

As of 2026-11-05. This folder is an isolated V4 research candidate. V3 remains unchanged. No V4 judge has been promoted, evaluated on all 160 images, or published.

## Current status

- **VERIFIED:** The published comment-only annotation was fetched from its versioned S3 object. It contains 15 reviewed rows, zero configured questions, and SHA-256 `d466958fc707f504f70ec0c7273a433dfc84826aa36a1cbb46a0df201b51a1f3`.
- **VERIFIED:** Every exact comment is joined to its original scene prompt, generated-scene/twin URLs and hashes, frozen V2 assessment, compact V3 assessment, deterministic merge, and consensus decision in `evidence/joined_feedback_context.json`.
- **VERIFIED:** The first Direct OpenAI Astra attempt used the corporate Foundry URLs and failed with HTTP 400 because OpenAI could not download those URLs. The empty output, exact request manifest, stderr, timestamps, and exit code are preserved in `attempt_1_url_images/`.
- **IN PROGRESS:** A second detached Astra request runs with all 15 scene/twin pairs embedded as hash-bound 1280-pixel JPEG derivatives. It uses Direct OpenAI `gpt-6-astra`, high reasoning, concurrency one, eight retries, and a 600-second timeout.
- **UNVERIFIED:** Astra's eventual proposal is advisory. It must be checked against every exact comment and current evidence before any candidate V4 prompt/schema/runtime is implemented.

## Bounded research question

Can the recurring reviewer corrections be converted into a deployable placement-judge protocol that improves furniture/room reasoning and warning-versus-failure calibration without reintroducing seat-association false positives?

## Evidence boundary

The 15 comments are development evidence. Unreviewed rows are unlabeled. Existing V2/V3 diagnostic and extended checks were repeatedly used during prior design, so they cannot support an unbiased accuracy claim. The generated scene is the judged image; the twin is only product identity/orientation context.

## Key recurring feedback sent to Astra

- Minor chair movement or angle is ordinarily review/pass; clear unusability or wrong-surface association can be material.
- A close crop can hide a valid chair.
- Support furniture placement in the room is distinct from correct device-on-support placement.
- Rectangular/square tables stranded in a room center can be unnatural, while round tables are more plausible as free-standing central furniture.
- Missing furniture legs, malformed/nonparallel table edges, and wall/table/cabinet perspective conflicts are placement-relevant failures.
- Printers can be too far from a wall even after plausible cable clearance.
- A slanted printer and random/incoherent objects under a table can create material placement/narrative failures.
- Disfigured glasses are normally an out-of-scope general rendering warning, not a natural-placement failure.

## Astra call artifacts

- `astra_task.md`: authored self-contained analysis/design request.
- `evidence/reviewer_0.json`: exact published annotation bytes.
- `evidence/source_manifest.json`: S3 provenance and hash.
- `evidence/joined_feedback_context.json`: exact joined textual/model evidence.
- `evidence/image_payload_manifest.json`: source/derivative hashes, dimensions, and pair order.
- `request_manifest.json`: current request configuration and exact 30-image sequence.
- `astra_output.md`, `astra_stderr.log`, `astra_exit_code.txt`: current attempt output and status.

## Next exact step

After tmux session `hp-placement-v4-astra-b64` exits, verify its exit code, response model, finish reason, and nonempty output. Audit Astra's proposal against all 15 comments. Only then implement an isolated V4 candidate and freeze its exact prompt/schema/scoring/runtime before evaluation.
