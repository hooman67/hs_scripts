# Video Composition Worker

Composes multiple video clips into a single output video with per-clip trimming, 2D transforms (scale, rotate, translate), timeline positioning, and audio passthrough.

## How It Works

### The Big Picture

A user in Foundry Studio has an "assembly" — a sequence of video clips arranged on a timeline. Each clip can be trimmed (show only frames 10-50 of a 100-frame source), positioned at a specific point in the output timeline (clip A starts at frame 0, clip B at frame 72), and transformed (scaled down to 50%, rotated 15 degrees, moved 100px to the right).

The video composition worker takes all of this information, downloads the source video files, composites them frame-by-frame into a single output video (with audio), and uploads the result.

### Architecture: Two Layers

```
┌─────────────────────────────────────────────────────────┐
│  video_composition worker (this package)                │
│                                                         │
│  HTTP endpoint → validation → download clips →          │
│  call compositor → upload result                        │
│                                                         │
│  Knows about: ACP storage, colligo protocol,            │
│  worker config, request/response types                  │
│                                                         │
│  Does NOT know about: PyAV, PIL, numpy, frame pixels    │
└──────────────────────────┬──────────────────────────────┘
                           │ calls
┌──────────────────────────▼──────────────────────────────┐
│  media_composition library                              │
│  (colligo/models/foundry/media_composition/)            │
│                                                         │
│  compose_video_timeline() — the actual compositor       │
│                                                         │
│  Knows about: PyAV decoding/encoding, PIL image         │
│  compositing, numpy audio buffers, frame timing         │
│                                                         │
│  Does NOT know about: ACP, HTTP, colligo protocol       │
└─────────────────────────────────────────────────────────┘
```

The **worker** is the "web service" layer — it handles HTTP requests, downloads files from storage, validates inputs, and uploads results. It never touches a pixel.

The **media_composition library** is the "engine" — it decodes video frames, composites them onto a canvas with transforms, extracts and mixes audio, and encodes the output. It has no concept of HTTP or cloud storage.

### Step-by-Step: What Happens When a Request Comes In

```
1. HTTP POST to /v1/video/composition
   ├── clips: [{video: <asset-id>, startFrame: 0, trimStart: 10, trimEnd: 50, transform: {scaleX: 0.5}}]
   ├── timeline: {durationFrames: 120, fps: 24, widthPx: 1920, heightPx: 1080}
   └── output: {targetFolder: <acp-directory>}   (optional)
```

**Step 1: Validation** (`handle_request_validation`)
- At least 1 clip? Check.
- Under the max clip limit (default 10)? Check.
- Every clip has a valid video reference (asset ID, presigned URL, or Creative Cloud file ID)? Check.

**Step 2: Download** (in `handle_request`)
- For each clip, download the source video from ACP/S3 into a temp directory.
- Detect the video's MIME type and save with the correct extension (`.mp4`, `.mov`, etc.).

**Step 3: Map Types**
- The worker has its own `VideoCompositionTransform` type (no PyAV dependency).
- The compositor needs `Transform2D` from `media_composition` (which depends on PyAV).
- The pipeline maps field-by-field: `translate_x_px`, `translate_y_px`, `scale_x_factor`, `scale_y_factor`, `rotation_deg`.
- Similarly, `VideoCompositionTimelineSpec` maps to `TimelineInfo`, and each `VideoCompositionClip` maps to `VideoInfo`.

**Step 4: Compose** (`compose_video_timeline`)

This is where the magic happens, inside the media_composition library:

```
Phase 1: Video (frame-by-frame)
┌─────────────────────────────────────────────────────┐
│ For each output frame (0 to duration_frames):       │
│                                                     │
│   1. Create blank canvas (1920x1080, black)         │
│                                                     │
│   2. For each clip:                                 │
│      - Is this frame within the clip's time range?  │
│        (startFrame + trimStart ≤ frame < trimEnd)   │
│      - If yes, decode the source frame at that time │
│      - Apply transform: scale → rotate → translate  │
│      - Alpha-composite onto the canvas              │
│        (later clips overlay earlier ones)            │
│                                                     │
│   3. Encode the canvas as one H.264 video frame     │
└─────────────────────────────────────────────────────┘

Phase 2: Audio (buffer-based)
┌─────────────────────────────────────────────────────┐
│ Before video encoding starts:                       │
│                                                     │
│   1. Pre-compose audio into a single numpy buffer   │
│      (total_samples = duration_sec * 44100)         │
│                                                     │
│   2. For each clip that has an audio track:          │
│      - Decode audio via PyAV AudioResampler          │
│        (normalises any format → stereo fltp 44100Hz)│
│      - Trim to [trimStartFrame, trimEndFrame]       │
│        (converted to sample indices via fps)        │
│      - Place at startFrame position in the buffer   │
│      - Clips without audio → silence at that spot   │
│                                                     │
│   3. Clamp buffer to [-1.0, 1.0] to prevent         │
│      clipping if overlapping clips both have audio  │
│                                                     │
│   4. After video is done, encode buffer as AAC      │
│      in 1024-sample chunks                          │
│                                                     │
│   Note: if NO clips have audio, the output has      │
│   no audio stream at all (not silence — no stream)  │
└─────────────────────────────────────────────────────┘
```

**Step 5: Upload**
- Read the composed MP4 from disk.
- If `target_folder` was provided → upload to ACP (Adobe Creative Cloud) and return the asset ID.
- Otherwise → upload to temp S3 storage and return a presigned download URL.

### Key Design Decisions

**Why two separate transform types?**
The worker types (`VideoCompositionTransform`) live in `types.py` which can be imported anywhere — tests, macOS dev machines, CI — without needing PyAV installed. The library types (`Transform2D`) live inside `media_composition` which requires PyAV. The pipeline maps between them at runtime.

**Why pre-compose audio before opening the output container?**
PyAV requires all streams (video + audio) to be declared before the first packet is muxed. By pre-composing the audio buffer first, we know upfront whether any clip has audio — and only add an AAC stream if needed. This avoids silent audio tracks in video-only compositions.

**Why frame-by-frame compositing instead of FFmpeg filter_complex?**
The `media_composition` library was built for the Wan video generation pipeline where each frame needs individual transform control. Frame-by-frame gives us full control over per-clip scale/rotate/translate without fighting FFmpeg's filter graph syntax. The tradeoff is speed — this re-encodes every frame. For assembly download (typically <100 clips, <5 minutes total), this is acceptable.

**Why fixed 44100 Hz audio output sample rate?**
Simplicity. Source clips may have different sample rates and formats (int16, float, mono, stereo). PyAV's `AudioResampler` normalises all sources to stereo float-planar at 44100 Hz before processing. This handles format conversion and sample rate resampling correctly regardless of the source codec.

## File Structure

```
video_composition/
├── __init__.py
├── types.py                          # Request/response/config types (no PyAV dependency)
├── VideoCompositionPipeline.py       # Download → compose → upload orchestration
├── build.py                          # Worker registration (deploy_worker)
├── colligo.yaml                      # Package metadata + dependency declarations
├── endpoints/
│   ├── __init__.py
│   └── composition_endpoint.py       # HTTP endpoint, API types, request adapter
└── tests/
    ├── __init__.py
    ├── test_video_composition_types.py      # Type validation unit tests
    └── test_video_composition_pipeline.py   # Pipeline + endpoint integration tests

media_composition/                    # The compositor engine (separate package)
├── types.py                          # Transform2D, TimelineInfo, VideoInfo
├── transforms.py                     # PIL-based scale/rotate/translate
├── video_timeline.py                 # compose_video_timeline() + audio support
└── tests/
    ├── conftest.py                   # Shared test helpers (make_test_video, read_output_info, etc.)
    ├── test_media_composition.py     # E2E compositing (sequential, trimming, transforms, gaps, backgrounds)
    ├── test_audio_passthrough.py     # Audio extraction/trim/mix tests
    ├── test_audio_edge_cases.py      # Mono, 48kHz, 22050Hz, overlapping, silence gaps, mixed rates
    ├── test_codecs_and_containers.py # H.264/H.265/VP9/ProRes/MJPEG, AAC/Opus/PCM/MP3, MP4/MOV/MKV/WebM
    ├── test_resolution.py            # 4K canvas, 2x2 minimum, portrait/landscape, mismatched resolutions
    ├── test_error_handling.py        # Corrupt files, empty files, audio-only, odd dimensions, validation
    └── test_boundary_conditions.py   # Single frame, 10 clips, trim beyond source, same source twice
```

## Test Coverage (119 tests)

| Test File | Count | What it covers |
|-----------|-------|---------------|
| `test_video_composition_types.py` | 19 | Pydantic validation: transforms, clips, timeline specs, config, executor |
| `test_video_composition_pipeline.py` | 17 | Pipeline orchestration (mocked I/O): validation, download, compose, upload paths |
| `test_media_composition.py` | 19 | E2E compositor: sequential clips, trimming, transforms, gaps, backgrounds, overlay order |
| `test_audio_passthrough.py` | 6 | Audio round-trip: preservation, concatenation, mixed clips, trimming, offset silence |
| `test_audio_edge_cases.py` | 8 | Mono source, 48kHz/22050Hz resampling, overlapping audio mix, silence gaps, mixed rates |
| `test_codecs_and_containers.py` | 13 | H.264/H.265/VP9/ProRes/MJPEG video codecs, AAC/Opus/PCM/MP3 audio, MP4/MOV/MKV/WebM containers |
| `test_resolution.py` | 7 | 4K canvas, 2x2 minimum, portrait/landscape, mismatched input resolutions |
| `test_error_handling.py` | 7 | Corrupt/empty/text files, audio-only input, odd dimensions, zero duration, trim beyond source |
| `test_boundary_conditions.py` | 7 | Single frame, 10 clips, same source twice, large canvas, many short clips |
| `test_pipeline_integration.py` | 6 | Real compositor with mocked storage: transform mapping, trim passthrough |

### Remaining Gaps

1. **No long-duration stress test** — all tests use tiny videos (24-48 frames). A 5-minute 1080p composition would exercise memory and encoding performance.
2. **No real e2e with cloud storage** — pipeline integration tests mock storage downloads/uploads.
