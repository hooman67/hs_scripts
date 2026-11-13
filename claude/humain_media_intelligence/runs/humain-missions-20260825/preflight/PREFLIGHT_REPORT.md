# Humain MI preflight report

Generated: 2026-08-25T22:02:36.691448+00:00

## Outcome

- Ready for ingestion: **True**
- Source media objects: 11,350
- Canonical unique videos: 9,436
- Exact duplicate copies removed: 1,914
- Canonical duration: 21.12 hours
- Canonical bytes: 274,893,017,268
- Probe results: {'ok': 9436}

All canonical videos opened successfully with ffprobe. Source-dimension differences are retained in `dimension_mismatches.parquet`; most are width/height orientation swaps, and none caused a probe failure.

## Primary-theme totals

| Theme | Unique videos | Hours | Bytes |
|---|---:|---:|---:|
| Clothing / Fashion | 1,718 | 3.72 | 58,171,611,078 |
| Events | 2,190 | 4.84 | 85,078,156,936 |
| Food | 1,949 | 4.16 | 60,043,147,598 |
| Landmarks / Architecture | 1,879 | 4.50 | 21,713,537,761 |
| Lifestyle | 1,700 | 3.89 | 49,886,563,895 |

## Duplicate decision

The 2026-07-27 and 2026-08-17 deliveries for mission `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` contain the same 1,870 media objects by S3 checksum. The newer delivery is canonical. Exact duplicates within and across other themes were also collapsed; every source association remains in `provenance.parquet` and `duplicates.parquet`.
