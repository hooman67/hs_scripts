# KDP Lifestyle Image — Real vs Generated Pilot

Published: 2026-10-07

## Reviewer link

This link opens the secure stock `fe-html` viewer with one row per page and the classification question already
configured as `Real / Generated`. The question remains editable, as requested.

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/report/viewer.html?q=W3sidGV4dCI6IklzIHRoZSBjYW5kaWRhdGUgaW1hZ2UgcmVhbCBvciBBSS1nZW5lcmF0ZWQ%2FIiwiaGFyZF9jaGVjayI6ZmFsc2UsInJ1YnJpYyI6eyJrZXkiOiJjdXN0b20iLCJuYW1lIjoiUmVhbCB2cyBHZW5lcmF0ZWQiLCJvcHRpb25zIjpbeyJ2YWx1ZSI6InJlYWwiLCJsYWJlbCI6IlJlYWwiLCJ0b25lIjoibmV1dHJhbCJ9LHsidmFsdWUiOiJnZW5lcmF0ZWQiLCJsYWJlbCI6IkdlbmVyYXRlZCIsInRvbmUiOiJhbHQifV19fV0%3D&hide=item_id&per=1

Base viewer URL without preconfigured questions:

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/report/viewer.html

## Design

- 14 candidate rows: seven real and seven generated.
- Balance is exact within every included SKU: K-Express Black 2+2, Mini Mate Plus Warm Stone 1+1, Mini Mate Plus
  Matte Black 2+2, and K-Supreme Gen 2 Black 2+2.
- Every row shows one opaque `Candidate` and the clean `Reference 1`/`Reference 2` images used for that SKU.
- Every candidate was center-cropped, resized, and re-encoded to metadata-free 1024×1024 RGB PNG.
- Candidate filenames and row IDs are opaque; rows were pre-shuffled with a recorded deterministic seed.
- The uploaded `data.json` contains no truth, source path, scenario, model, or overlap field.
- The private truth map and build metadata remain local and are ignored by Git.

The matched K-Supreme red/pink and Mini Mate Matte Black lavender/yellow source images informed prompt wording.
They are suitable for this scene-matched “spot the generated image” pilot but not a pristine generalization holdout.

## Local artifacts

Builder:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/build_blind_pilot.py`

Public report input:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/report_input.parquet`

Normalized opaque candidates:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/staging/assets/`

Local copy of published `data.json`:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/published/data.json`

Local copy of the unmodified vendored viewer:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/published/viewer.html`

Private answer key — never upload or share with the reviewer:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/private/truth_map.csv`

Private build metadata:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/private/build_metadata.json`

## S3 layout

Opaque normalized candidates:

`s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/assets/`

Secure two-file `fe-html` report:

`s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/report/`

## Validation

- 14 unique opaque candidate files.
- 14 unique opaque row IDs.
- 7 real and 7 generated candidates in the private truth map.
- 36 displayed asset slots: 14 candidates plus 22 repeated per-SKU reference slots.
- 20 unique S3 assets referenced by the report; all 20 returned successful object metadata.
- `viewer.html` content type: `text/html`.
- `data.json` content type: `application/json`.
- No truth map, parquet, source path, checksum, scenario, or prompt-overlap field was uploaded.
- Local `viewer.html` SHA-256 matches the unmodified vendored viewer exactly.
