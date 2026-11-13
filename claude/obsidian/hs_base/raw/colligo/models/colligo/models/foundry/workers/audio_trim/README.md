# Audio Trim Worker

Async Colligo worker that trims audio files using FFmpeg. Deployed as part of the `foundry` application.

## API

**Endpoint:** `POST /v1/audio/trim`
**Protocol:** Async (returns 202 + `statusUrl` for polling)

### Request

```json
{
  "audio": { "id": "<uuid>" },
  "start_s": 1.0,
  "end_s": 5.0
}
```

| Field     | Type           | Default | Description                                    |
|-----------|----------------|---------|------------------------------------------------|
| `audio`   | `PublicBinary`  | —       | Audio reference (id, presigned_url, or CC file) |
| `start_s` | `float`        | `0.0`   | Trim start time in seconds (must be >= 0)      |
| `end_s`   | `float \| None` | `None`  | Trim end time in seconds (omit to trim to end) |

### Response

```json
{
  "output": {
    "id": "<uuid>",
    "presigned_url": "https://..."
  }
}
```

## Supported Formats

`audio/wav`, `audio/x-wav`, `audio/mpeg`, `audio/mp3`, `audio/ogg`, `audio/flac`, `audio/aac`

Max file size: 50 MB (configurable via `AudioTrimConfig.max_file_size_bytes`).

## How It Works

1. Downloads the input audio from temp storage
2. Writes it to a temp file with the correct extension
3. Runs `ffmpeg -ss {start} [-to {end}] -i input -c copy output` (stream copy)
4. If stream copy fails, falls back to re-encoding without `-c copy`
5. Uploads the trimmed output to temp storage and returns the reference

Stream copy is attempted first because it's near-instant and lossless. The re-encode fallback handles edge cases where stream copy produces corrupted output (e.g., trimming at non-keyframe boundaries in compressed formats).

## Configuration

- `concurrent_ml_threads=200` — CPU-only, high concurrency
- `session_storage_options.ttl_s=86400` — results persist for 24 hours
- No GPU or model weights required

## Running Tests

```bash
pytest models/colligo/models/foundry/workers/audio_trim/tests/ -v
```

Tests include unit tests (mocked I/O) and real FFmpeg tests (skipped automatically if FFmpeg is not installed). Install FFmpeg locally with `brew install ffmpeg` to run the full suite.

## File Structure

```
audio_trim/
├── AudioTrimPipeline.py    # Core worker logic
├── build.py                # Worker registration
├── colligo.yaml            # Package dependencies
├── types.py                # Request/response types + executor
├── endpoints/
│   └── trim_endpoint.py    # HTTP endpoint definition + request adapter
└── tests/
    └── test_audio_trim.py  # All tests (types, pipeline, real FFmpeg)
```
