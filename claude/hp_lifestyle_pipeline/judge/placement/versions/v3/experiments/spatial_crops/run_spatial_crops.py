# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests", "pillow>=10"]
# ///
"""Isolated V3 placement experiment with a full scene and four lossless crops."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import math
import mimetypes
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent
V3_ROOT = ROOT.parents[1]
JUDGE_ROOT = V3_ROOT.parents[2]
V3_SYSTEM_PROMPT = V3_ROOT / "system_prompt.md"
EXPERIMENT_PROMPT = ROOT / "system_prompt.md"
FREEZE_PATH = ROOT / "freeze.json"
CROP_ROOT = JUDGE_ROOT / "local_runs/v3_spatial_crops"
PROTOCOL_VERSION = "placement-v3-spatial-crops-request-v1"
OVERLAP_FRACTION = 0.10
MAX_ATTEMPTS = 2
MAX_COMPLETION_TOKENS = 12000
SUPPORTED_IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp"}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load canonical module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if str(V3_ROOT) not in sys.path:
    sys.path.insert(0, str(V3_ROOT))
SCORING = _load_module("placement_v3_spatial_scoring", V3_ROOT / "scoring.py")
CANONICAL = _load_module("placement_v3_spatial_canonical", V3_ROOT / "run_judge.py")
OBSERVATION_SCHEMA = SCORING.OBSERVATION_SCHEMA
WIRE_SCHEMA = CANONICAL.wire_schema(OBSERVATION_SCHEMA)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(raw.encode("utf-8"))


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(
        path,
        (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def image_mime(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in SUPPORTED_IMAGE_MIMES:
        raise ValueError(f"Unsupported image format: {path.name}")
    return mime


def combined_system_prompt() -> tuple[str, dict[str, str]]:
    root_prompt = V3_SYSTEM_PROMPT.read_text(encoding="utf-8")
    experiment_prompt = EXPERIMENT_PROMPT.read_text(encoding="utf-8")
    if not root_prompt.strip() or not experiment_prompt.strip():
        raise ValueError("Root and experiment system prompts must both be nonempty")
    # The experiment prompt is root-authored as the compact V3 prompt plus the
    # spatial-crop instruction.  Require that relationship and send it once.
    if root_prompt.strip() not in experiment_prompt:
        raise ValueError("Experiment prompt must contain the frozen root V3 prompt")
    effective = experiment_prompt.rstrip() + "\n"
    return effective, {
        "root_v3_system_prompt_sha256": sha256_path(V3_SYSTEM_PROMPT),
        "experiment_instruction_sha256": sha256_path(EXPERIMENT_PROMPT),
        "combined_system_prompt_sha256": sha256_bytes(effective.encode("utf-8")),
    }


def current_protocol_state() -> dict[str, Any]:
    _, prompt_hashes = combined_system_prompt()
    batch_path = ROOT / "run_batch.py"
    return {
        "schema_version": "placement-v3-spatial-crops-freeze-v1",
        "protocol_version": PROTOCOL_VERSION,
        "crop_policy": {
            "method": "four_quadrants_each_extended_across_center_seams",
            "overlap_fraction_of_full_dimension_per_quadrant": OVERLAP_FRACTION,
            "encoding": "PNG",
            "resize": False,
            "pixel_policy": "decoded source pixels preserved exactly",
        },
        "request_policy": {
            "model_default": "gpt-5.5",
            "reasoning_effort": "high",
            "max_completion_tokens": MAX_COMPLETION_TOKENS,
            "max_api_attempts": MAX_ATTEMPTS,
            "image_order": [
                "B_original_digital_twin",
                "A_full_scene",
                "A_top_left_crop",
                "A_top_right_crop",
                "A_bottom_left_crop",
                "A_bottom_right_crop",
            ],
        },
        "hashes": {
            "runner_sha256": sha256_path(__file__),
            "batch_runner_sha256": sha256_path(batch_path),
            "root_v3_runner_sha256": sha256_path(V3_ROOT / "run_judge.py"),
            "root_v3_scoring_sha256": sha256_path(V3_ROOT / "scoring.py"),
            "root_v3_observation_schema_sha256": sha256_path(
                V3_ROOT / "observation_schema.json"
            ),
            "wire_schema_sha256": json_sha256(WIRE_SCHEMA),
            **prompt_hashes,
        },
    }


def ensure_frozen() -> dict[str, Any]:
    if not FREEZE_PATH.is_file():
        raise RuntimeError("Spatial-crop protocol is not frozen; run freeze_protocol.py")
    frozen = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    current = current_protocol_state()
    for key in ("schema_version", "protocol_version", "crop_policy", "request_policy", "hashes"):
        if frozen.get(key) != current[key]:
            raise RuntimeError(f"Spatial-crop freeze differs for {key}")
    return frozen


def quadrant_boxes(width: int, height: int) -> list[dict[str, Any]]:
    if width < 2 or height < 2:
        raise ValueError("Source image is too small for four spatial crops")
    low_x = math.floor(width * (0.5 - OVERLAP_FRACTION))
    high_x = math.ceil(width * (0.5 + OVERLAP_FRACTION))
    low_y = math.floor(height * (0.5 - OVERLAP_FRACTION))
    high_y = math.ceil(height * (0.5 + OVERLAP_FRACTION))
    raw = [
        ("top_left", (0, 0, high_x, high_y)),
        ("top_right", (low_x, 0, width, high_y)),
        ("bottom_left", (0, low_y, high_x, height)),
        ("bottom_right", (low_x, low_y, width, height)),
    ]
    return [
        {
            "name": name,
            "box_xyxy_exclusive": list(box),
            "normalized_xyxy_exclusive": [
                round(box[0] / width, 8),
                round(box[1] / height, 8),
                round(box[2] / width, 8),
                round(box[3] / height, 8),
            ],
        }
        for name, box in raw
    ]


def build_crops(source_path: Path, crop_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if crop_dir.exists():
        raise FileExistsError(f"Crop directory already exists: {crop_dir}")
    crop_dir.mkdir(parents=True)
    source_hash = sha256_path(source_path)
    with Image.open(source_path) as source:
        source.load()
        source_format = source.format
        source_mode = source.mode
        width, height = source.size
        original = {
            "path": str(source_path.resolve()),
            "sha256": source_hash,
            "format": source_format,
            "mode": source_mode,
            "width": width,
            "height": height,
        }
        crops: list[dict[str, Any]] = []
        for specification in quadrant_boxes(width, height):
            box = tuple(specification["box_xyxy_exclusive"])
            cropped = source.crop(box)
            path = crop_dir / f"A_{specification['name']}.png"
            cropped.save(path, format="PNG")
            with Image.open(path) as stored:
                stored.load()
                if stored.size != cropped.size or stored.mode != cropped.mode:
                    raise RuntimeError(f"Stored crop representation changed: {path}")
                if ImageChops.difference(cropped, stored).getbbox() is not None:
                    raise RuntimeError(f"Stored crop pixel values changed: {path}")
            crops.append(
                {
                    **specification,
                    "path": str(path.resolve()),
                    "sha256": sha256_path(path),
                    "bytes": path.stat().st_size,
                    "format": "PNG",
                    "mode": cropped.mode,
                    "width": cropped.width,
                    "height": cropped.height,
                    "source_image_sha256": source_hash,
                    "resize_applied": False,
                    "pixel_values_verified": True,
                }
            )
    atomic_json(
        crop_dir / "crop_manifest.json",
        {
            "schema_version": "placement-v3-spatial-crops-v1",
            "overlap_fraction_per_quadrant": OVERLAP_FRACTION,
            "coordinate_convention": "left,top inclusive; right,bottom exclusive",
            "source": original,
            "crops": crops,
        },
    )
    return original, crops


def image_content(path: Path) -> dict[str, Any]:
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{image_mime(path)};base64,"
            + base64.b64encode(path.read_bytes()).decode(),
            "detail": "high",
        },
    }


def build_messages(
    runtime_input: Mapping[str, str], system: str, crops: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    generated = Path(runtime_input["generated_image"])
    twin = Path(runtime_input["twin_image"])
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": json.dumps(
                {
                    "product_type": runtime_input["product_type"],
                    "scene_prompt": runtime_input["scene_prompt"],
                    "image_stage": runtime_input["image_stage"],
                }
            ),
        },
        {
            "type": "text",
            "text": "B — original digital-twin render for product and viewpoint reference.",
        },
        image_content(twin),
        {
            "type": "text",
            "text": "A — full scene-generation image to evaluate. This full image remains the authoritative scene context.",
        },
        image_content(generated),
    ]
    for crop in crops:
        box = crop["box_xyxy_exclusive"]
        normalized = crop["normalized_xyxy_exclusive"]
        content.extend(
            [
                {
                    "type": "text",
                    "text": (
                        f"A {crop['name'].replace('_', ' ')} crop — exact lossless PNG crop "
                        f"from full image A; no resize. Pixel box [left={box[0]}, top={box[1]}, "
                        f"right={box[2]}, bottom={box[3]}) with right/bottom exclusive; "
                        f"normalized box {normalized}. Read this only as a magnified spatial aid "
                        "and preserve the full-scene relationships visible in A."
                    ),
                },
                image_content(Path(crop["path"])),
            ]
        )
    return [{"role": "system", "content": system}, {"role": "user", "content": content}]


def model_identity_matches(requested: str, returned: Any) -> bool:
    if not isinstance(returned, str):
        return False
    return re.fullmatch(rf"{re.escape(requested)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?", returned) is not None


def judge(
    runtime_input: Mapping[str, str],
    output_dir: Path | str,
    crop_dir: Path | str,
    *,
    model: str = "gpt-5.5",
) -> dict[str, Any]:
    freeze = ensure_frozen()
    SCORING.validate_runtime_input(runtime_input)
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a nonempty string")
    output_dir = Path(output_dir)
    crop_dir = Path(crop_dir)
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    system, prompt_hashes = combined_system_prompt()
    generated = Path(runtime_input["generated_image"])
    twin = Path(runtime_input["twin_image"])
    scene_original, crops = build_crops(generated, crop_dir)
    with Image.open(twin) as twin_image:
        twin_image.load()
        twin_original = {
            "path": str(twin.resolve()),
            "sha256": sha256_path(twin),
            "format": twin_image.format,
            "mode": twin_image.mode,
            "width": twin_image.width,
            "height": twin_image.height,
        }
    messages = build_messages(runtime_input, system, crops)
    record: dict[str, Any] = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "protocol_version": PROTOCOL_VERSION,
        "protocol_freeze_sha256": sha256_path(FREEZE_PATH),
        "protocol_freeze": freeze,
        "input": dict(runtime_input),
        "original_images": {
            "generated_scene_A": scene_original,
            "digital_twin_B": twin_original,
        },
        "crop_policy": freeze["crop_policy"],
        "crops": crops,
        "image_order": freeze["request_policy"]["image_order"],
        "message_content_order": [
            "runtime_metadata",
            "B_label",
            "B_image",
            "A_full_label",
            "A_full_image",
            "A_top_left_label",
            "A_top_left_image",
            "A_top_right_label",
            "A_top_right_image",
            "A_bottom_left_label",
            "A_bottom_left_image",
            "A_bottom_right_label",
            "A_bottom_right_image",
        ],
        "model_requested": model,
        "reasoning_effort": "high",
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "max_api_attempts": MAX_ATTEMPTS,
        "image_detail": "high",
        "image_transform_full_inputs": "none; original bytes",
        "crop_transform": "Pillow crop only; PNG lossless; no resize; decoded pixels verified",
        "observation_schema_sha256": sha256_path(V3_ROOT / "observation_schema.json"),
        "scoring_sha256": sha256_path(V3_ROOT / "scoring.py"),
        "wire_schema_sha256": json_sha256(WIRE_SCHEMA),
        **prompt_hashes,
    }
    fingerprint = json_sha256(
        {key: value for key, value in record.items() if key != "started_at"}
    )
    record["fingerprint"] = fingerprint
    atomic_json(output_dir / "request.json", record)
    atomic_bytes(output_dir / "root_v3_system_prompt.md", V3_SYSTEM_PROMPT.read_bytes())
    atomic_bytes(output_dir / "experiment_instruction.md", EXPERIMENT_PROMPT.read_bytes())
    atomic_bytes(output_dir / "system_prompt.md", system.encode("utf-8"))
    atomic_json(output_dir / "observation_schema.json", OBSERVATION_SCHEMA)

    started = time.monotonic()
    record["attempts"] = []
    try:
        api_client, mode = CANONICAL.client()
        record["auth_mode"] = mode
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = api_client.chat.completions.create(
                    model=model,
                    reasoning_effort="high",
                    max_completion_tokens=MAX_COMPLETION_TOKENS,
                    messages=messages,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "placement_observation",
                            "strict": True,
                            "schema": WIRE_SCHEMA,
                        },
                    },
                )
                record["attempts"].append({"attempt": attempt, "status": "ok"})
                break
            except Exception as error:
                status = getattr(error, "status_code", None)
                record["attempts"].append(
                    {
                        "attempt": attempt,
                        "error_type": type(error).__name__,
                        "status": status,
                    }
                )
                if attempt == MAX_ATTEMPTS or status not in (429, 500, 502, 503, 504):
                    raise
                delay = 5
                try:
                    delay = min(
                        60,
                        max(delay, float(error.response.headers.get("retry-after", 0))),
                    )
                except (ValueError, AttributeError):
                    pass
                time.sleep(delay)

        record["model_returned"] = getattr(response, "model", None)
        raw = response.model_dump(mode="json")
        atomic_json(output_dir / "response.json", raw)
        if not model_identity_matches(model, record["model_returned"]):
            raise RuntimeError("Unexpected model returned")
        choice = response.choices[0]
        if choice.finish_reason != "stop" or choice.message.refusal:
            raise RuntimeError("Incomplete/refused judgment")
        observation = json.loads(choice.message.content)
        judgment = SCORING.aggregate_observation(observation)
        atomic_json(output_dir / "observation.json", observation)
        atomic_json(output_dir / "judgment.json", judgment)
        record.update(ok=True, usage=raw.get("usage"), judgment=judgment)
    except Exception as error:
        record.update(
            ok=False,
            error_type=type(error).__name__,
            status_code=getattr(error, "status_code", None),
        )
        if hasattr(error, "errors"):
            record["validation_errors"] = list(error.errors)
    record["elapsed_seconds"] = round(time.monotonic() - started, 2)
    atomic_json(output_dir / "result.json", record)
    return record
