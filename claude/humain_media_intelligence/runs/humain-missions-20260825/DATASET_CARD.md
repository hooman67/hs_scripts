# Humain missions baseline dataset card

Status: deterministic source/preflight layer complete; MI-derived semantic coverage and final ingestion reconciliation pending.

## Baseline

- Source deliveries: 7 prefixes, 6 mission UUIDs, 5 themes
- Source videos: 11,350
- Canonical unique videos: 9,436
- Exact duplicate copies excluded: 1,914 across 1,909 checksum groups
- Canonical duration: 21.1214 hours
- Canonical bytes: 274,893,017,268 (about 256 GiB)
- Media readability: 9,436/9,436 canonical videos passed `ffprobe`
- Zero-byte objects: 0

The entire 2026-07-27 delivery for mission `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` is content-identical to the 2026-08-17 delivery. The newer delivery is canonical; the older paths remain represented in the provenance manifest.

## Theme distribution

| Theme | Canonical videos | Hours | Bytes |
|---|---:|---:|---:|
| Events | 2,190 | 4.8421 | 85,078,156,936 |
| Food | 1,949 | 4.1626 | 60,043,147,598 |
| Landmarks / Architecture | 1,879 | 4.5050 | 21,713,537,761 |
| Clothing / Fashion | 1,718 | 3.7221 | 58,171,611,078 |
| Lifestyle | 1,700 | 3.8895 | 49,886,563,895 |

Theme balance is fairly even by asset count. Events is the largest theme at 23.2%; Lifestyle is the smallest at 18.0%. Count balance does not establish semantic or geographic coverage.

## Mission distribution

| Mission UUID | Canonical videos |
|---|---:|
| `b149626b-2aae-402f-a382-48c3116a9f53` | 1,949 |
| `3d6deadb-f65a-4489-bb16-9192e44cb8e5` | 1,879 |
| `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` | 1,870 |
| `99367909-29a8-437f-b34d-0caa45949f19` | 1,718 |
| `20655345-d067-431a-98fa-051a39d2cbd1` | 1,700 |
| `6069eaee-a699-435e-93e4-0c8900b18b0a` | 320 |

The smaller 320-video Events mission should remain visible in downstream analysis; aggregate Events results could otherwise be dominated by the 1,870-video mission.

## Technical profile

- Containers/extensions: 5,967 `.mov`, 3,469 `.mp4`
- Video codecs: 8,334 H.264, 1,102 HEVC
- Orientation: 6,097 landscape, 3,335 portrait, 4 square
- Most common resolutions: 3,127 at 3840×2160; 2,880 at 1920×1080; 1,711 at 1080×1920; 1,573 at 2160×3840
- Duration: 208 at ≤5s; 7,882 at 5–10s; 1,322 at 10–20s; 22 at 20–30s; 2 over 30s
- Audio: 8,292 videos have no audio stream; 1,044 have one; 100 have two
- Source-vs-coded dimension mismatches: 1,303, including 1,164 orientation swaps; none prevented decoding

The corpus is predominantly short-form: 83.5% of canonical videos are 5–10 seconds. Only 12.1% contain any audio stream, so speech/language conclusions must report the audio-eligible denominator and must not be generalized to the full corpus.

## Source metadata and governance signals

- Source captions: present for 9,436/9,436 canonical videos
- Dataset-level keywords: present for 9,436/9,436
- Asset-level keywords: present for 2,278/9,436 (24.1%)
- Release-attached flag: true for 5,608; false for 3,828
- `is_gentech`: false for all 9,436
- Source offensive level: 0 for all 9,436

Language IDs are retained as source-system codes rather than interpreted labels until their authoritative mapping is verified: ID 2 appears on 7,234 assets, ID 4 on 2,199, and ID 3 on 3.

## Pending MI-derived sections

After ingestion and postprocessing pass reconciliation, extend this card with:

- per-stage success/failure and retry counts
- speech eligibility, transcription language/content, and silent-audio behavior
- geographic/place and landmark coverage
- food, clothing, activity, event, lifestyle, people, OCR, symbol, and time-of-day distributions
- exact and near-duplicate semantic-cluster density
- representative evidence-backed retrieval queries by theme and mission
- separation of source-data, ingestion, labeling, and retrieval gaps
- target-versus-observed comparison once business/taxonomy weights are signed off

Do not infer nationality, ethnicity, religion, identity, or other sensitive attributes from appearance. MI-generated observations require deterministic/source reconciliation before they are treated as collection gaps.
