# MuxingComponent - Video/Audio Muxing Pipeline

## Overview

The `MuxingComponent` is a sophisticated media processing pipeline that combines (muxes) multiple videos, audio tracks, and images into a single output file. It handles complex scenarios like overlapping videos, timeline gaps, picture-in-picture overlays, and multi-track audio mixing.

## Table of Contents

1. [Architecture](#architecture)
2. [Data Models](#data-models)
3. [Main Processing Flow](#main-processing-flow)
4. [Key Components](#key-components)
5. [Feature Details](#feature-details)
6. [Visual Flow Diagram](#visual-flow-diagram)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MuxingComponent                              │
├─────────────────────────────────────────────────────────────────┤
│  Input: Videos + Audios + Images → Output: Single Media File    │
└─────────────────────────────────────────────────────────────────┘
```

The component inherits from `BaseComponent` and uses FFmpeg for all media processing operations.

---

## Data Models

### InputMuxInfo (Video Information)
```python
source: Path          # Path to the video file
volume: int = 100     # Audio volume (0-100%)
start: float = 0.0    # Start time within the source video (seconds)
duration: float       # Duration to use from the source
inset: float = 0.0    # Position in the output timeline (seconds)
overlay: VideoOverlayConfig | None  # If set, this video becomes a PiP overlay
```

### InputAudioInfo (Audio Information)
```python
source: Path          # Path to the audio file
volume: int = 100     # Audio volume (0-100%)
start: float          # Start time within the source audio
duration: float       # Duration to use
inset: float          # Position in the output timeline
```

### InputImageInfo (Image Information)
```python
source: Path          # Path to the image file
inset: float          # When to show the image (seconds)
duration: float       # How long to display the image
```

### TimelineSegment (Internal)
```python
start: float          # Segment start time in timeline
end: float            # Segment end time in timeline
video_indices: list   # Which videos are active in this segment
```

---

## Main Processing Flow

### Entry Point: `_run()`

```
┌──────────────────────────────────────────────────────────────────┐
│                         _run()                                    │
│  ↓                                                                │
│  mux_videos_with_audios(videos, audios, output, has_audio, imgs) │
└──────────────────────────────────────────────────────────────────┘
```

### High-Level Flow: `mux_videos_with_audios()`

```
Step 1: Video Processing
┌────────────────────────────────────────────────────────────────────┐
│ IF multiple videos OR has images:                                  │
│   └→ concat_videos() → Produces single concatenated video         │
│ ELSE IF single video:                                              │
│   └→ Use video as-is                                               │
└────────────────────────────────────────────────────────────────────┘
                              ↓
Step 2: Audio Processing  
┌────────────────────────────────────────────────────────────────────┐
│ IF no audio tracks:                                                │
│   └→ Copy video to output (keep existing audio if any)            │
│ ELSE:                                                              │
│   └→ Mix all audio tracks with video audio using FFmpeg           │
└────────────────────────────────────────────────────────────────────┘
                              ↓
Step 3: Output
┌────────────────────────────────────────────────────────────────────┐
│ Final muxed video/audio file written to output_path               │
└────────────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Video Concatenation: `concat_videos()`

This is the main orchestrator for video processing. It handles three major scenarios:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        concat_videos()                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Step 1: Separate base videos from overlay videos            │   │
│  │         • Base videos: Regular videos on timeline           │   │
│  │         • Overlay videos: PiP (picture-in-picture)          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Step 2: Fill timeline gaps                                   │   │
│  │         • Detect gaps between videos                         │   │
│  │         • Generate black video to fill gaps                  │   │
│  │         • Handle video overlaps                              │   │
│  │         • Extend timeline for images/audio if needed         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Step 3: Concatenate base videos                              │   │
│  │         • Use _concat_videos_internal()                      │   │
│  │         • Apply trim, scale, FPS normalization               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Step 4: Overlay images (if any)                              │   │
│  │         • Convert each image to video                        │   │
│  │         • Overlay at specified inset times                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Step 5: Apply circular video overlay (if any)                │   │
│  │         • Create picture-in-picture effect                   │   │
│  │         • Circular mask with configurable position           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Timeline Gap Filling: `_fill_timeline_gaps()`

Ensures a continuous video timeline by:

```
Timeline Example:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input Videos on Timeline:
0s        5s        10s       15s       20s       25s
├─────────┤         ├─────────────────────┤
│ Video 1 │   GAP   │      Video 2        │   (needs extension for audio)
└─────────┘         └─────────────────────┘

After Gap Filling:
0s        5s        10s       15s       20s       25s       30s
├─────────┼─────────┼─────────────────────┼─────────────────────┤
│ Video 1 │  BLACK  │      Video 2        │       BLACK         │
└─────────┴─────────┴─────────────────────┴─────────────────────┘
                                                    ↑
                                          Extended for audio track
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Overlap Handling: `_process_timeline_with_overlaps()`

When videos overlap on the timeline, this method creates composite segments:

```
Overlap Scenario:
0s        5s        10s       15s       20s
├─────────────────────────────┤           Video A (0-15s)
          ├─────────────────────────────┤ Video B (5-20s)
          
Result after processing:
0s        5s        10s       15s       20s
├─────────┼─────────────────────┼───────┤
│ A only  │  A+B Composite      │B only │
└─────────┴─────────────────────┴───────┘

First video in array order = Foreground (on top)
```

### 4. Circular Video Overlay: `overlay_video_circular()`

Creates a picture-in-picture effect with a circular mask:

```
┌─────────────────────────────────────────────┐
│                                             │
│            Background Video                 │
│                                             │
│                                     ┌─────┐ │
│                                     │ ●●● │ │  ← Circular PiP
│                                     │ ●●● │ │    overlay video
│                                     └─────┘ │
└─────────────────────────────────────────────┘
                                        ↑
                              Positioned at bottom-right
                              with configurable margins
```

Configuration options:
- `radius`: Circle radius in pixels (default: 120px)
- `right_margin`: Right margin as percentage (default: 2%)
- `bottom_margin`: Bottom margin as percentage (default: 3.7%)

### 5. Image Overlay: `overlay_image_video()`

Converts images to video segments and overlays them on the main video:

```
Timeline:
0s           5s          10s          15s
├────────────┼────────────┼────────────┤
│ Background │ IMAGE      │ Background │
│   Video    │ (overlay)  │   Video    │
└────────────┴────────────┴────────────┘
              ↑
        Image shown from 5s to 10s (duration: 5s)
```

---

## Feature Details

### Resolution Handling

The component intelligently determines output resolution:

1. **Priority 1**: Use first video's resolution
2. **Priority 2**: Use first image's resolution (if no videos)
3. **Priority 3**: Default to 1920x1080 (HD)

All dimensions are normalized to:
- Even numbers (required by H.264)
- Maximum 4K (3840px) to avoid encoding issues

### FPS Handling

```
IF all videos have same FPS:
  └→ Use that FPS
ELSE:
  └→ Default to 30 FPS
```

### Audio Processing

The audio pipeline supports:

1. **Video Audio**: Each video's audio track with individual volume control
2. **External Audio**: Additional audio tracks mixed at specific timeline positions
3. **Silent Audio**: Auto-generated for videos without audio tracks

```
Audio Mix Example:
──────────────────────────────────────────────────────────────────
Timeline:  0s        5s        10s       15s       20s

Video Audio:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  (volume: 80%)

Audio Track 1:        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓              (volume: 100%)
                      ↑ inset: 5s

Audio Track 2:                      ▓▓▓▓▓▓▓▓▓▓▓▓  (volume: 60%)
                                    ↑ inset: 12s

Result: All tracks mixed together using FFmpeg amix filter
──────────────────────────────────────────────────────────────────
```

### Output Codec Selection

- **Windows users or .mp4 output**: AAC audio codec
- **Other platforms**: PCM S16LE (uncompressed)

---

## Visual Flow Diagram

```
                              ┌─────────────────┐
                              │   User Input    │
                              │  - Videos[]     │
                              │  - Audios[]     │
                              │  - Images[]     │
                              └────────┬────────┘
                                       │
                                       ▼
                         ┌─────────────────────────┐
                         │        _run()           │
                         └────────────┬────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │    mux_videos_with_audios()      │
                    └────────────────┬─────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
        ┌─────────────────────┐           ┌─────────────────────┐
        │   Has Videos/Imgs?  │           │   Audio Processing  │
        └──────────┬──────────┘           └──────────┬──────────┘
                   │                                  │
        ┌──────────┴──────────┐                      │
        │                     │                       │
        ▼                     ▼                       │
  Single Video          Multiple Videos               │
  (copy as-is)               │                        │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │   concat_videos()   │             │
        │         └──────────┬──────────┘             │
        │                    │                        │
        │    ┌───────────────┼───────────────┐        │
        │    ▼               ▼               ▼        │
        │ Separate     Fill Timeline   Process       │
        │ Overlay vs   Gaps with       Overlapping    │
        │ Base Videos  Black Video     Segments       │
        │    │               │               │        │
        │    └───────────────┼───────────────┘        │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │ _concat_videos_     │             │
        │         │   internal()        │             │
        │         └──────────┬──────────┘             │
        │                    │                        │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │ Overlay Images?     │             │
        │         └──────────┬──────────┘             │
        │                    │ Yes                    │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │ overlay_image_video │             │
        │         │   (for each image)  │             │
        │         └──────────┬──────────┘             │
        │                    │                        │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │ Has PiP Overlay?    │             │
        │         └──────────┬──────────┘             │
        │                    │ Yes                    │
        │                    ▼                        │
        │         ┌─────────────────────┐             │
        │         │overlay_video_       │             │
        │         │  circular()         │             │
        │         └──────────┬──────────┘             │
        │                    │                        │
        └────────────────────┼────────────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Mix Audio Tracks   │
                  │  (FFmpeg amix)      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Final Output     │
                  │  (Muxed Video/Audio)│
                  └─────────────────────┘
```

---

## Summary of FFmpeg Operations Used

| Operation | FFmpeg Filter/Feature |
|-----------|----------------------|
| Trim video | `trim=start=X:end=Y` |
| Trim audio | `atrim=start=X:end=Y` |
| Reset timestamps | `setpts=PTS-STARTPTS` |
| Scale video | `scale=W:H` |
| Pad video | `pad=W:H:(ow-iw)/2:(oh-ih)/2` |
| Normalize FPS | `fps=N` |
| Concatenate | `concat=n=N:v=1:a=1` |
| Overlay video | `overlay=x=X:y=Y` |
| Circular mask | `geq` (general equation filter) |
| Mix audio | `amix=inputs=N` |
| Adjust volume | `volume=V` |
| Delay audio | `adelay=delays=MS` |
| Generate silence | `anullsrc` |

---

## Error Handling

- Videos without audio tracks: Silent audio is auto-generated
- Resolution mismatch: Videos are scaled/padded to match
- FPS mismatch: Videos are normalized to common FPS
- Missing content: Validation ensures at least one video/image exists
- Temporary files: Automatically cleaned up after processing
