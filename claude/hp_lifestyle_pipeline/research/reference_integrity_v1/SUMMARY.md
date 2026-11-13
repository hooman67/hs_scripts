# HP generated-output/reference integrity audit

**As of:** 2026-10-22  
**Scope:** The 192-row `hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1` run, with detailed traces for the three flagged rows. This audit addresses identity and provenance. It does not infer visual-quality causes beyond the saved request/debug evidence.

## Contents

- [Result](#result)
- [Three flagged traces](#three-flagged-traces)
- [Code-path findings](#code-path-findings)
- [Evidence limits](#evidence-limits)
- [Durable evidence](#durable-evidence)

## Result

**[Observed + derived] The two flagged `baseline-0016` rows are part of a confirmed eight-row reference misbinding.** The original smoke command uploaded `00_baseline-0007.jpg`, a laptop twin, and received blob ID `fed63b3c-76ef-4c99-ae98-56054a01291f`. The smoke request then selected the eval's first row, `ee810cf51bb82bb4:p1:baseline-0016`, whose displayed twin is `09_baseline-0016.jpg`, a printer. The legacy `import_smoke` code recorded the already-uploaded laptop blob ID under the row's `baseline-0016` twin ID and claimed filename. The resumed run reported one cached reference and uploaded 29 others, including `baseline-0018` but not `baseline-0016`. Every `baseline-0016` request therefore reused the laptop blob ID.

The eight affected canonical row IDs are:

1. `ee810cf51bb82bb4:p1:baseline-0016`
2. `160db92655412f4d:p1:baseline-0016`
3. `8bbf8af1d8cbf4b2:p1:baseline-0016`
4. `8189f3ad5af37a81:p1:baseline-0016`
5. `8189f3ad5af37a81:p2:baseline-0016`
6. `324b14a617dfedba:p1:baseline-0016`
7. `943faef0af11484f:p1:baseline-0016`
8. `943faef0af11484f:p2:baseline-0016`

The server-saved debug corroborates the misbinding independently: all eight eval rows identify `baseline-0016` as `Printer`, while their first rewritten-prompt entities are `HP laptop` or `dark blue HP laptop`.

**Disposition:** Exclude all eight `baseline-0016` rows from any reference-fidelity or visual-quality analysis of generated v1. The historical run still contains 192 mechanically completed outputs, but only 184 rows remain eligible after this provenance exclusion. Retain the original 192-row gallery, results, and publication unchanged as historical evidence; do not silently delete or relabel its rows. A future corrected run should use a new run identity and provenance-verified reference bindings.

**[Observed] The flagged `baseline-0018` row does not show a client-side reference swap in the available evidence.** Its displayed file is `11_baseline-0018.jpg`; its downloaded SHA-256 exactly matches the eval manifest (`51a538514288680b59e751b718828487c4e12fe1017d55dd19fe1134bbf3b41e`). The run log says it was freshly uploaded through the normal upload path. Its request uses blob ID `9fe9989e-f619-4e4c-a16b-4ec91c176119`, and all eight `baseline-0018` rows use that ID exclusively. Their debug first entities are `HP printer` or `grey HP printer`. The flagged row's rewrite explicitly says to keep the printer's “exact orientation, position, and scale.” This supports correct printer-reference delivery through the server's rewrite stage; it does not prove the server's internal blob-ID-to-byte mapping cryptographically.

**[Observed] The 192-row join audit found no additional identity failure.** There are 192 eval rows, 192 saved result records, and 192 published FE rows. Row IDs, prompt keys/text, twin IDs, result filenames, and published gallery rows agree. The 30 used twins map one-to-one to 30 request blob IDs; no twin has multiple request blob IDs and no request blob ID is shared by different twin IDs. This structural check cannot detect the `baseline-0016` problem by itself because the poisoned cache entry was internally consistent after import.

The correct reporting split is therefore **192 mechanically completed, 8 provenance-invalid and excluded, 184 eligible**. “192 successes” may describe endpoint completion only when stated with that qualification; it must not imply that all 192 outputs used their displayed digital twins.

## Three flagged traces

| Row | Displayed twin | Request blob | Job | Output image ID | Downloaded output SHA-256 | Debug first entity |
|---|---|---|---|---|---|---|
| `ee810cf51bb82bb4:p1:baseline-0016` | `09_baseline-0016.jpg` | `fed63b3c-76ef-4c99-ae98-56054a01291f` | `urn:ff:jobs::47b7b833-b48f-4cae-91d1-f581f225f6de` | `35398935-bd68-4774-b725-d3f9ea523dac` | `84e5e95d574468dc34648b156637e26ae24bd2b0572be769ea268b3870284ff9` | `HP laptop` |
| `ee810cf51bb82bb4:p1:baseline-0018` | `11_baseline-0018.jpg` | `9fe9989e-f619-4e4c-a16b-4ec91c176119` | `urn:ff:jobs::52f3b2db-3c1c-497e-b982-1a150a4560ec` | `183d3d29-26bd-4032-8c32-10ebfa12433c` | `fe901884fba3050eec4dd5fa6367275f0a52bedb16becb35afbb76902d0efdb7` | `HP printer` |
| `160db92655412f4d:p1:baseline-0016` | `09_baseline-0016.jpg` | `fed63b3c-76ef-4c99-ae98-56054a01291f` | `urn:ff:jobs::e94889cf-808d-44d5-8efd-20752f53cbb8` | `8eb1561c-36b8-4617-a402-d08d550ed84e` | `c78959c46c8cb87e25982cddc527b1d9771a1386993d86153892c7ece235b20e` | `dark blue HP laptop` |

The downloaded output MD5s also match the published S3 object ETags for all three rows.

## Code-path findings

The run is traced against frozen commit `ffd0ba95ec9594f4a09d9b7c242b580c007ba97b`, whose historical runner SHA-256 is `194165b20bd39e4e66ac532a84f48cfbc3f28d2dbc64aea75dbc4898709db897`.

- Normal upload reads the selected path's bytes and returns `(twin_id, record)`. The `as_completed` loop writes `mapping[twin_id] = record`, so concurrent completion order does not reorder twins (historical lines 78–130).
- Generation selects `blobs[row["twin_id"]]["id"]`, so a wrong cached binding affects every row using that twin (historical lines 239–280).
- `import_smoke` reads an arbitrary prior upload response, looks up the smoke request row, then assigns the upload ID to that row's twin and claimed filename without validating the originally uploaded path or bytes (historical lines 310–359).
- The gallery builds records keyed by saved `row_id`, iterates eval rows in eval order, displays `row.twin_file`, and displays the saved result's output filename. The gallery join did not create the mismatch.
- Saved responses deliberately remove `presignedUrl`, so the original response URL is unavailable in `results.json`; the stable published URL and downloaded bytes are preserved instead.

## Evidence limits

**[Unknown] No legacy artifact preserves a hash of the exact bytes posted during reference upload.** The old blob cache stored only blob ID, claimed local filename, and time. The historical command path plus server debug makes the `baseline-0016` conclusion definitive at the practical evidence level, but there is no upload-body hash.

**[Unknown] The endpoint's internal blob-ID-to-byte mapping is not inspectable.** The old jobs are no longer queryable from the current endpoint. For `baseline-0018`, the normal upload log, unique request binding, correct downloaded twin hash, and printer-aware server debug are the best available evidence.

**[Observed] The original response download URLs were intentionally stripped and later expired.** The audit retains output image IDs, published gateway URLs, S3 metadata, and locally downloaded output SHA-256 hashes.

## Durable evidence

- Compact historical session excerpts, execution IDs, timestamps, selected-event hashes, affected rows, and smoke debug: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/data/historical_session_evidence.json`
- Compact 192-row mapping audit and full saved request/debug records for the three flagged rows: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/data/reference_audit_evidence.json`
- Audit scripts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/reference_integrity_v1/scripts/`
- Durable raw run artifacts and downloaded source/output images: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reference_integrity/source_artifacts/`
- Full machine audit: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reference_integrity/full_reference_trace_audit.json`
- Side-by-side comparisons: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/local_data/reference_integrity/comparisons/`

The source session is appendable, so its whole-file hash can change. The historical extract therefore stores a SHA-256 for each selected raw event line. Credential material and expired signed URLs are excluded from tracked evidence.
