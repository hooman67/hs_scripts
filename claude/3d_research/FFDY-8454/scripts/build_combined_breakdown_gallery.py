#!/usr/bin/env python3
"""Build the self-contained review source for the combined Seedance experiment."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/3d_research/FFDY-8454")
RESULTS = ROOT / "seedance_results/blockout_v1"
OUT = ROOT / "gallery_combined_breakdown"
ASSETS = OUT / "assets"
SOURCE_GALLERY = Path("/home/colligo/hs_scripts/claude/thd/FFDY-7304/gallery")
FINAL_CUT_DIR = ROOT / "final_cuts"


def copy_asset(source: str | Path, name: str) -> str:
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)
    destination = ASSETS / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return f"assets/{name}"


def params(request: dict) -> str:
    return (
        f"fal endpoint: {request['endpoint']} · duration: {request['duration']}s · "
        f"resolution: {request['resolution']} · aspect ratio: {request['aspect_ratio']} · "
        f"audio: {'on' if request.get('generate_audio') else 'off'}"
    )


ASSETS.mkdir(parents=True, exist_ok=True)
shutil.copy2(SOURCE_GALLERY / "build_gallery.py", OUT / "build_gallery.py")
shutil.copy2(SOURCE_GALLERY / "imsauth.js", OUT / "imsauth.js")

final_cut_manifest = json.loads(
    (FINAL_CUT_DIR / "final_cut_shot_by_shot_v1.inputs.json").read_text()
)
final_cut_video = copy_asset(
    FINAL_CUT_DIR / "final_cut_shot_by_shot_v1.mp4",
    "final_cut_shot_by_shot_v1.mp4",
)
final_cut_manifest_asset = copy_asset(
    FINAL_CUT_DIR / "final_cut_shot_by_shot_v1.inputs.json",
    "final_cut_shot_by_shot_v1.inputs.json",
)

combined_dir = RESULTS / "all_references_auto_edit_v1"
combined_request = json.loads((combined_dir / "request.local.json").read_text())
combined_output = copy_asset(
    combined_dir / "all_references_auto_edit_v1.mp4", "combined_auto_edit.mp4"
)
combined_downloads = [
    {"src": copy_asset(combined_dir / filename, f"combined_{filename}"), "label": label}
    for filename, label in [
        ("request.local.json", "Local request JSON"),
        ("request.submitted.json", "Exact submitted fal payload"),
        ("result.json", "Result metadata"),
        ("prompt.txt", "Prompt text"),
    ]
]
detected_sheet = copy_asset(
    RESULTS / "combined_detected_shots_contact_sheet.png",
    "combined_detected_shots_contact_sheet.png",
)
all_refs_sheet = copy_asset(
    RESULTS / "all_references_contact_sheet.png", "all_references_contact_sheet.png"
)

video_labels = [
    "@Video1 · Blender · first side-panel lift",
    "@Video2 · existing photoreal connector macro",
    "@Video3 · Blender · opposite side-panel lift",
    "@Video4 · Blender · perpendicular wall installation",
    "@Video5 · Blender · subtle wall press",
    "@Video6 · Blender · larger narrow-board installation",
    "@Video7 · Blender · smaller narrow-board installation",
    "@Video8 · Blender · rigid cabinet stand-up",
]
image_labels = [
    "@Image1 · initial flat layout and room",
    "@Image2 · CLICKREADY connector appearance",
    "@Image3 · opposite-side installation appearance",
    "@Image4 · perpendicular-wall appearance",
    "@Image5 · later box-completion appearance",
    "@Image6 · upright cabinet and room appearance",
]

combined_video_assets = []
for index, (source, label) in enumerate(zip(combined_request["videos"], video_labels), 1):
    suffix = Path(source).suffix.lower()
    combined_video_assets.append(
        {"src": copy_asset(source, f"combined_input_video_{index:02d}{suffix}"), "label": label}
    )

combined_image_assets = []
for index, (source, label) in enumerate(zip(combined_request["images"], image_labels), 1):
    suffix = Path(source).suffix.lower()
    combined_image_assets.append(
        (copy_asset(source, f"combined_input_image_{index:02d}{suffix}"), label)
    )

# These are objective cut points from ffmpeg scene detection at threshold 0.18.
stages = [
    (1, "Shot 2 / 1A", 0.0, 2.08333, "First broad side-panel lift", 0, 0, "shot02_1A_blockout_v1"),
    (2, "Shot 3 / 3A", 2.08333, 4.33333, "CLICKREADY connector macro", 1, 1, None),
    (3, "Shot 4", 4.33333, 6.95833, "Opposite broad side-panel lift", 2, 2, "shot04_blockout_v1"),
    (4, "Shot 5", 6.95833, 9.625, "Perpendicular wall installation", 3, 3, "shot05_blockout_v1"),
    (5, "Shot 6", 9.625, 11.9583, "Small wall press / connection", 4, 4, "shot06_blockout_v1"),
    (6, "Shot 7A", 11.9583, 14.3333, "Larger narrow-board installation", 5, 4, "shot07A_blockout_v1"),
    (7, "Shot 7B", 14.3333, 16.2083, "Smaller narrow-board installation", 6, 4, "shot07B_blockout_v1"),
    (8, "Shot 8", 16.2083, 22.042, "Stand up the completed cabinet", 7, 5, "shot08_blockout_v1"),
]

event_lines = [
    line.strip()
    for line in combined_request["prompt"].splitlines()
    if line.strip().startswith("Stage ")
]

sections = [
    {
        "kind": "divider",
        "id": "final_cut_shot_by_shot_divider",
        "label": "Final Cut made shot by shot",
        "tab_label": "Final Cut made shot by shot",
        "note": "Eleven approved full-length clips assembled in the exact requested order.",
    },
    {
        "kind": "target",
        "id": "final_cut_shot_by_shot",
        "label": "Final Cut made shot by shot",
        "params": (
            f"{len(final_cut_manifest['shots'])} straight-cut shots · "
            f"{final_cut_manifest['output_duration_seconds']:.3f}s · "
            "H.264 · 1920×1080 · 24 fps · audio off"
        ),
        "note": (
            "Every source clip is used at full duration. The ordered source ledger below links "
            "to the exact videos used to create this final cut."
        ),
        "video": final_cut_video,
        "downloads_label": "Ordered shot source ledger",
        "downloads": [
            {"src": shot["url"], "label": shot["name"]}
            for shot in final_cut_manifest["shots"]
        ]
        + [
            {
                "src": final_cut_manifest_asset,
                "label": "Machine-readable input manifest",
            }
        ],
    },
    {
        "kind": "divider",
        "id": "overview_divider",
        "label": "00 · COMPLETE CALL — exact fal / Seedance inputs",
        "tab_label": "00 · COMPLETE CALL — exact fal / Seedance inputs",
        "note": "All inputs sent to FAL at once.",
    },
    {
        "kind": "target",
        "id": "combined_exact_call",
        "label": "Combined 22.04-second generated montage",
        "params": params(combined_request),
        "note": (
            "EXACT CALL PROVENANCE. The visible labels preserve the submitted @Video1–@Video8 and "
            "@Image1–@Image6 ordering. Open the prompt below to see the full submitted text."
        ),
        "video": combined_output,
        "input_videos_label": "All eight video inputs passed to fal",
        "input_videos": combined_video_assets,
        "input_images_label": "All six image inputs passed to fal",
        "input_images": [
            {"src": source, "label": label} for source, label in combined_image_assets
        ],
        "prompt": combined_request["prompt"],
        "downloads": combined_downloads,
    },
    {
        "kind": "target",
        "id": "combined_detected_structure",
        "label": "Detected edit structure",
        "note": (
            "Scene detection found seven cuts, producing eight segments at 2.083, 4.333, 6.958, "
            "9.625, 11.958, 14.333, and 16.208 seconds. This matched the requested action order "
            "in this one sample; the boundaries were not supplied to Seedance."
        ),
        "frames": [detected_sheet, all_refs_sheet],
    },
]

for stage_num, shot_name, start, end, action, video_index, image_index, isolated_job in stages:
    segment_name = f"generated_stage{stage_num:02d}.mp4"
    segment_path = ASSETS / segment_name
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", str(start), "-to", str(end), "-i", str(ASSETS / "combined_auto_edit.mp4"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-an", "-movflags", "+faststart", str(segment_path),
        ],
        check=True,
    )
    sections.append(
        {
            "kind": "divider",
            "id": f"stage{stage_num:02d}_divider",
            "label": f"Stage {stage_num} · {shot_name} — {action}",
            "note": f"Detected range in the combined output: {start:.3f}–{end:.3f}s.",
        }
    )
    sections.append(
        {
            "kind": "target",
            "id": f"stage{stage_num:02d}_combined_segment",
            "label": "Combined-call stage: primary motion reference → generated segment",
            "params": "Derived review segment; not a separate model call",
            "note": (
                "The left-hand clip is the primary stage reference named in the Event Script. "
                "The right-hand clip was extracted from the combined output at the detected cuts. "
                "All 14 combined-call references—not only the primary pair shown here—were available "
                "to Seedance for this stage."
            ),
            "reference_video": combined_video_assets[video_index]["src"],
            "reference_video_label": combined_video_assets[video_index]["label"],
            "video": f"assets/{segment_name}",
            "video_label": f"Combined output · {start:.3f}–{end:.3f}s",
            "frames_label": image_labels[image_index],
            "frames": [combined_image_assets[image_index][0]],
            "prompt": event_lines[stage_num - 1],
        }
    )

    if isolated_job is None:
        sections.append(
            {
                "kind": "target",
                "id": "stage02_reused_connector",
                "label": "No new isolated call in this experiment",
                "params": "Existing Shot 3 / 3A connector result reused as @Video2",
                "note": (
                    "The photoreal connector clip shown on the left above was itself the ordered "
                    "motion reference for Stage 2. It was not regenerated in the seven isolated "
                    "blockout calls."
                ),
            }
        )
        continue

    job_dir = RESULTS / isolated_job
    request = json.loads((job_dir / "request.local.json").read_text())
    output_source = job_dir / f"{isolated_job}.mp4"
    isolated_motion = copy_asset(
        request["videos"][0], f"{isolated_job}_input_video{Path(request['videos'][0]).suffix.lower()}"
    )
    isolated_images = [
        copy_asset(source, f"{isolated_job}_input_image_{i:02d}{Path(source).suffix.lower()}")
        for i, source in enumerate(request.get("images", []), 1)
    ]
    isolated_output = copy_asset(output_source, f"{isolated_job}_output.mp4")
    isolated_downloads = [
        {"src": copy_asset(job_dir / filename, f"{isolated_job}_{filename}"), "label": label}
        for filename, label in [
            ("request.local.json", "Local request JSON"),
            ("request.submitted.json", "Exact submitted fal payload"),
            ("result.json", "Result metadata"),
            ("prompt.txt", "Prompt text"),
        ]
    ]
    sections.append(
        {
            "kind": "target",
            "id": f"stage{stage_num:02d}_isolated_call",
            "label": "Isolated-shot call — exact fal / Seedance inputs",
            "params": params(request),
            "note": (
                "This was a separate paid generation. The left video, every image below, the full "
                "prompt, and the displayed parameters are the complete model inputs for this call."
            ),
            "reference_video": isolated_motion,
            "reference_video_label": "Exact video input passed to fal",
            "video": isolated_output,
            "video_label": "Generated isolated-shot output",
            "input_images_label": "Every image input passed to fal",
            "input_images": [
                {"src": source, "label": f"@Image{i} · {Path(request['images'][i - 1]).name}"}
                for i, source in enumerate(isolated_images, 1)
            ],
            "prompt": request["prompt"],
            "downloads": isolated_downloads,
        }
    )

    if stage_num == 1:
        retry_id = "shot02_1A_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage01_event_script_retry_v2",
                "label": "RETRY v2 — simplified Event Script",
                "params": params(retry_request) + " · estimated incremental cost: $1.66",
                "note": (
                    "Only the Event Script changed, using Hooman's exact replacement text. The "
                    "unwanted extra 180-degree flip is no longer visible: the panel follows a direct "
                    "flat-to-upright lift. Tradeoff: the camera is higher and the sink enters the "
                    "left foreground, so framing continuity is weaker than v1."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

    if stage_num == 3:
        retry_id = "shot04_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage03_event_script_retry_v2",
                "label": "RETRY v2 — simplified Event Script",
                "params": params(retry_request) + " · estimated incremental cost: $1.67",
                "note": (
                    "Only the Event Script changed, adapting the successful Shot 2 wording to "
                    "preserve Shot 4's already-installed first wall. The opposite panel now follows "
                    "one clean edge lift into the upright position without the awkward intermediate "
                    "handling seen in v1. Tradeoff: the camera is tighter and lower and crops more "
                    "of the couple."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

    if stage_num == 4:
        retry_id = "shot05_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage04_event_script_retry_v2",
                "label": "RETRY v2 — continuous hand-supported wall installation",
                "params": params(retry_request) + " · estimated incremental cost: $2.22",
                "note": (
                    "Only the Event Script changed, using Hooman's approved Option 1 exactly. "
                    "The woman now keeps both hands on the rigid perpendicular wall throughout "
                    "pickup, carry, and seating; the wall no longer moves autonomously. The man "
                    "remains beside the two narrow boards, although their displacement is subtle."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

    if stage_num == 5:
        retry_id = "shot06_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage05_event_script_retry_v2",
                "label": "RETRY v2 — explicit rectangular footprint and supported motion",
                "params": params(retry_request) + " · estimated incremental cost: $1.68",
                "note": (
                    "Only the Event Script changed. It explicitly requires side-to-side width "
                    "greater than front-to-back depth, rigid panels, and visible hand support for "
                    "every moving component. Physics improved: the moving walls are hand-supported "
                    "and the remaining installed panel stays rigid. The proportion fix is only "
                    "partial; the result still reads closer to square than the Blender reference."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

    if stage_num == 6:
        retry_id = "shot07A_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage06_event_script_retry_v2",
                "label": "RETRY v2 — blockout-authoritative proportions and trajectory",
                "params": params(retry_request) + " · estimated incremental cost: $1.83",
                "note": (
                    "Only the Event Script changed. It assigns exact geometry, proportions, "
                    "orientation, camera, and trajectory to @Video1; @Image1 supplies photoreal "
                    "materials and room appearance only. The result keeps the cabinet wide, "
                    "rectangular, and laid flat, while the woman follows a direct two-hand pickup "
                    "and seating path and the man visibly stabilizes the rigid cabinet."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

    if stage_num == 7:
        retry_id = "shot07B_event_script_v2"
        retry_dir = RESULTS / retry_id
        retry_request = json.loads((retry_dir / "request.local.json").read_text())
        retry_motion = copy_asset(
            retry_request["videos"][0],
            f"{retry_id}_input_video{Path(retry_request['videos'][0]).suffix.lower()}",
        )
        retry_images = [
            copy_asset(source, f"{retry_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(retry_request.get("images", []), 1)
        ]
        retry_output = copy_asset(retry_dir / f"{retry_id}.mp4", f"{retry_id}_output.mp4")
        retry_downloads = [
            {"src": copy_asset(retry_dir / filename, f"{retry_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage07_event_script_retry_v2",
                "label": "RETRY v2 — blockout-authoritative final-board installation",
                "params": params(retry_request) + " · estimated incremental cost: $1.64",
                "note": (
                    "Only the Event Script changed. As in successful Stage 6, @Video1 owns exact "
                    "geometry, proportions, orientation, camera, and trajectory while @Image1 "
                    "supplies materials and room appearance only. The cabinet remains wide and "
                    "laid flat; the man maintains two-hand contact through a direct carry and "
                    "seating motion while the woman visibly holds the rigid cabinet fixed."
                ),
                "reference_video": retry_motion,
                "reference_video_label": "Same exact Blender video input as v1",
                "video": retry_output,
                "video_label": "Generated retry v2",
                "input_images_label": "Same exact image input as v1",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(retry_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(retry_images, 1)
                ],
                "prompt": retry_request["prompt"],
                "downloads": retry_downloads,
            }
        )

        minimal_id = "shot07B_minimal_v3"
        minimal_dir = RESULTS / minimal_id
        minimal_request = json.loads((minimal_dir / "request.local.json").read_text())
        minimal_motion = copy_asset(
            minimal_request["videos"][0],
            f"{minimal_id}_input_video{Path(minimal_request['videos'][0]).suffix.lower()}",
        )
        minimal_images = [
            copy_asset(source, f"{minimal_id}_input_image_{i:02d}{Path(source).suffix.lower()}")
            for i, source in enumerate(minimal_request.get("images", []), 1)
        ]
        minimal_output = copy_asset(
            minimal_dir / f"{minimal_id}.mp4", f"{minimal_id}_output.mp4"
        )
        minimal_downloads = [
            {"src": copy_asset(minimal_dir / filename, f"{minimal_id}_{filename}"), "label": label}
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage07_minimal_retry_v3",
                "label": "RETRY v3 — minimal final-board instruction",
                "params": params(minimal_request) + " · estimated incremental cost: $1.64",
                "note": (
                    "The prompt now asks only for installation of the smaller loose board and "
                    "requires the larger installed board to remain untouched, leaving the detailed "
                    "motion to @Video1. In this result, the smaller board is installed while the "
                    "larger installed board remains untouched."
                ),
                "reference_video": minimal_motion,
                "reference_video_label": "Exact video input passed to fal",
                "video": minimal_output,
                "video_label": "Generated retry v3",
                "input_images_label": "Every image input passed to fal",
                "input_images": [
                    {
                        "src": source,
                        "label": f"@Image{i} · {Path(minimal_request['images'][i - 1]).name}",
                    }
                    for i, source in enumerate(minimal_images, 1)
                ],
                "prompt": minimal_request["prompt"],
                "downloads": minimal_downloads,
            }
        )

        identity_variants = [
            (
                "shot07B_identity_v4a",
                "VARIATION v4A — relative-width identity",
                "Best component identity in this three-call batch. The moving piece remains "
                "visibly thinner than the wider installed board and preserves the direct "
                "installation motion. It is the closest visual match to the target far-right "
                "strip, although exact one-third width cannot be verified from the generated view.",
            ),
            (
                "shot07B_identity_v4b",
                "VARIATION v4B — only loose very-thin strip",
                "The direct installation motion is preserved, but the generated moving piece "
                "reads as a substantially wider plank than the target thin strip. This wording "
                "did not solve component identity in this sample.",
            ),
            (
                "shot07B_identity_v4c",
                "VARIATION v4C — exact moving strip",
                "The model follows a direct installation action, but the moving piece again "
                "reads as a broad plank rather than the thinnest cabinet strip. This wording "
                "did not solve component identity in this sample.",
            ),
        ]
        for variant_id, variant_label, variant_note in identity_variants:
            variant_dir = RESULTS / variant_id
            variant_request = json.loads((variant_dir / "request.local.json").read_text())
            variant_motion = copy_asset(
                variant_request["videos"][0],
                f"{variant_id}_input_video{Path(variant_request['videos'][0]).suffix.lower()}",
            )
            variant_images = [
                copy_asset(
                    source,
                    f"{variant_id}_input_image_{i:02d}{Path(source).suffix.lower()}",
                )
                for i, source in enumerate(variant_request.get("images", []), 1)
            ]
            variant_output = copy_asset(
                variant_dir / f"{variant_id}.mp4", f"{variant_id}_output.mp4"
            )
            variant_downloads = [
                {
                    "src": copy_asset(
                        variant_dir / filename, f"{variant_id}_{filename}"
                    ),
                    "label": label,
                }
                for filename, label in [
                    ("request.local.json", "Local request JSON"),
                    ("request.submitted.json", "Exact submitted fal payload"),
                    ("result.json", "Result metadata"),
                    ("prompt.txt", "Prompt text"),
                ]
            ]
            sections.append(
                {
                    "kind": "target",
                    "id": f"stage07_{variant_id}",
                    "label": variant_label,
                    "params": params(variant_request) + " · estimated incremental cost: $1.64",
                    "note": variant_note,
                    "reference_video": variant_motion,
                    "reference_video_label": "Exact video input passed to fal",
                    "video": variant_output,
                    "video_label": "Generated variation output",
                    "input_images_label": "Every image input passed to fal",
                    "input_images": [
                        {
                            "src": source,
                            "label": (
                                f"@Image{i} · "
                                f"{Path(variant_request['images'][i - 1]).name}"
                            ),
                        }
                        for i, source in enumerate(variant_images, 1)
                    ],
                    "prompt": variant_request["prompt"],
                    "downloads": variant_downloads,
                }
            )

        narrow_id = "shot07B_identity_v4c_narrow_v2"
        narrow_dir = RESULTS / narrow_id
        narrow_request = json.loads((narrow_dir / "request.local.json").read_text())
        narrow_motion = copy_asset(
            narrow_request["videos"][0],
            f"{narrow_id}_input_video{Path(narrow_request['videos'][0]).suffix.lower()}",
        )
        narrow_images = [
            copy_asset(
                source,
                f"{narrow_id}_input_image_{i:02d}{Path(source).suffix.lower()}",
            )
            for i, source in enumerate(narrow_request.get("images", []), 1)
        ]
        narrow_output = copy_asset(
            narrow_dir / f"{narrow_id}.mp4", f"{narrow_id}_output.mp4"
        )
        narrow_downloads = [
            {
                "src": copy_asset(narrow_dir / filename, f"{narrow_id}_{filename}"),
                "label": label,
            }
            for filename, label in [
                ("request.local.json", "Local request JSON"),
                ("request.submitted.json", "Exact submitted fal payload"),
                ("result.json", "Result metadata"),
                ("prompt.txt", "Prompt text"),
            ]
        ]
        sections.append(
            {
                "kind": "target",
                "id": "stage07_shot07B_identity_v4c_narrow_v2",
                "label": "RETRY v4C.2 — narrower exact moving strip",
                "params": params(narrow_request) + " · estimated incremental cost: $1.64",
                "note": (
                    "One light edit to v4C changed the target from approximately one-third to "
                    "one-sixth the width of the adjacent board and required it to stay that thin. "
                    "The generated strip is visibly narrower than v4C while the smooth, direct "
                    "installation motion is preserved."
                ),
                "reference_video": narrow_motion,
                "reference_video_label": "Exact video input passed to fal",
                "video": narrow_output,
                "video_label": "Generated narrower-strip retry",
                "input_images_label": "Every image input passed to fal",
                "input_images": [
                    {
                        "src": source,
                        "label": (
                            f"@Image{i} · "
                            f"{Path(narrow_request['images'][i - 1]).name}"
                        ),
                    }
                    for i, source in enumerate(narrow_images, 1)
                ],
                "prompt": narrow_request["prompt"],
                "downloads": narrow_downloads,
            }
        )

manifest = {
    "title": "Laundry Sink — Blender Motion → Seedance (FFDY-8454)",
    "subtitle": (
        "Exact fal inputs, submitted prompts, inferred cut boundaries, and side-by-side outputs "
        "for the 22-second combined montage, seven isolated-shot controls, and additive retries."
    ),
    "sections": sections,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
subprocess.run(["python3", str(OUT / "build_gallery.py")], check=True)
print(f"wrote {OUT / 'index.html'}")
